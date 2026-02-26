"""Core NyanBar class with tqdm-compatible API.

Provides the main progress bar class that users interact with.
Supports iteration protocol, context manager, update/close lifecycle,
and all standard tqdm keyword arguments.
"""
from __future__ import annotations

import sys
import time
import threading
from collections.abc import Iterable, Iterator
from typing import IO, Any

from .terminal import detect_terminal, ColorTier
from .formatters import EMA, format_meter
from .fallback import should_use_fallback, render_fallback_bar
from .engine import render_animation
from .renderer import render_frame, erase_lines
from .registry import get_theme, get_default_theme, resolve_render_tier
import nyanbar.themes  # noqa: F401 -- trigger built-in theme registration

__all__ = ["NyanBar"]


class NyanBar:
    """Animated progress bar with tqdm-compatible API.

    Drop-in replacement for ``tqdm.tqdm``.  Accepts all tqdm keyword
    arguments; unknown kwargs are silently swallowed.

    Parameters
    ----------
    iterable:
        Iterable to wrap.  If ``None``, use :meth:`update` manually.
    desc:
        Optional description prefix for the progress bar.
    total:
        Total number of iterations.  Inferred from ``len(iterable)``
        if available.
    leave:
        If ``True`` (default), keep the bar on screen after completion.
    file:
        Output stream.  Defaults to ``sys.stderr``.
    ncols:
        Fixed bar width in columns.  ``None`` uses terminal width.
    mininterval:
        Minimum seconds between display refreshes.
    maxinterval:
        Maximum seconds between refreshes (forces refresh on stall).
    miniters:
        Minimum iterations between refreshes.
    ascii:
        Accepted for tqdm compatibility; ignored.
    disable:
        If ``True``, suppress all output.
    unit:
        Iteration unit name (e.g. ``"it"``, ``"B"``).
    unit_scale:
        If ``True``, format counts with SI suffixes.
    dynamic_ncols:
        If ``True``, re-query terminal width on each refresh.
    smoothing:
        EMA smoothing factor for rate estimation.
    bar_format:
        Accepted for tqdm compatibility; silently ignored.
    initial:
        Starting iteration count.
    position:
        Bar position index.  ``0`` is primary; ``> 0`` triggers fallback.
    postfix:
        Initial postfix dict.
    unit_divisor:
        Divisor for SI scaling.
    **kwargs:
        Unknown keyword arguments are silently swallowed.
    """

    def __init__(
        self,
        iterable: Iterable[Any] | None = None,
        desc: str | None = None,
        total: int | None = None,
        leave: bool = True,
        file: IO[str] | None = None,
        ncols: int | None = None,
        mininterval: float = 0.1,
        maxinterval: float = 10.0,
        miniters: int | None = None,
        ascii: bool | None = None,
        disable: bool = False,
        unit: str = "it",
        unit_scale: bool = False,
        dynamic_ncols: bool = False,
        smoothing: float = 0.3,
        bar_format: str | None = None,  # accepted, silently ignored
        initial: int = 0,
        position: int | None = None,
        postfix: dict[str, Any] | None = None,
        unit_divisor: int = 1000,
        theme: str | None = None,
        render_level: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.iterable = iterable
        self.desc = desc
        self.total = total
        if total is None and iterable is not None and hasattr(iterable, "__len__"):
            self.total = len(iterable)  # type: ignore[arg-type]
        self.leave = leave
        self.file: IO[str] = file if file is not None else sys.stderr
        self.ncols = ncols
        self.mininterval = mininterval
        self.maxinterval = maxinterval
        self._miniters = miniters if miniters is not None else 1
        self.disable = disable
        self.unit = unit
        self.unit_scale = unit_scale
        self.dynamic_ncols = dynamic_ncols
        self.smoothing = smoothing
        self.position = position
        self.unit_divisor = unit_divisor

        self.n = initial
        self._desc = desc
        self._postfix_str: str | None = None
        if postfix is not None:
            self.set_postfix(postfix, refresh=False)

        self._closed = False
        self._lock = threading.Lock()
        self._start_t = time.monotonic()
        self._last_print_t = self._start_t
        self._last_print_n = initial

        self._ema_dn = EMA(alpha=smoothing)
        self._ema_dt = EMA(alpha=smoothing)

        self._prev_height = 0

        # Terminal detection
        self._terminal = detect_terminal(self.file)

        # Fallback decision
        self._use_fallback = should_use_fallback(
            self._terminal, disable=self.disable, position=self.position,
        )

        # Theme resolution
        self._animation = None
        if not self.disable:
            tier = resolve_render_tier(self._terminal, render_level)
            theme_name = theme or get_default_theme()
            try:
                self._animation = get_theme(theme_name, tier)
            except Exception:
                # Safety net -- if theme loading fails, fall back to no animation
                self._animation = None

        self._anim_thread: threading.Thread | None = None
        self._running = False

        # Render initial state
        if not self.disable:
            if not self._use_fallback and self._animation is not None:
                self._render_animation_frame()
            else:
                self._refresh()

    def __iter__(self) -> Iterator[Any]:
        """Yield each item from the wrapped iterable, updating progress."""
        if self.iterable is None:
            raise TypeError(
                "NyanBar with iterable=None cannot be used as an iterator. "
                "Use update() instead.",
            )
        if self.disable:
            yield from self.iterable
            return

        # Start animation thread if we have an animation and not in fallback
        self._start_animation_thread()

        # Hot-path local variables
        mininterval = self.mininterval
        miniters = self._miniters
        last_print_n = self._last_print_n
        last_print_t = self._last_print_t
        n = self.n

        try:
            for obj in self.iterable:
                yield obj
                n += 1

                if n - last_print_n >= miniters:
                    cur_t = time.monotonic()
                    dt = cur_t - last_print_t
                    if dt >= mininterval:
                        self.n = n
                        dn = n - last_print_n
                        self._ema_dn.update(dn)
                        self._ema_dt.update(dt)
                        self._refresh()
                        last_print_n = n
                        last_print_t = cur_t
                        self._last_print_n = last_print_n
                        self._last_print_t = last_print_t
                        self._auto_tune_miniters(dn, dt)
                        miniters = self._miniters
        except GeneratorExit:
            # Generator was garbage collected or closed externally
            self.n = n
            self.close()
            return
        except BaseException:
            self.n = n
            self.close()
            raise

        self.n = n
        self.close()

    def update(self, n: int = 1) -> None:
        """Increment the counter by *n* and optionally refresh display."""
        with self._lock:
            self.n += n
            if self.disable:
                return

            dn = self.n - self._last_print_n
            if dn < self._miniters:
                return

            cur_t = time.monotonic()
            dt = cur_t - self._last_print_t

            # Two-gate throttle: miniters AND mininterval
            if dt < self.mininterval:
                # maxinterval override: force refresh on stall
                if dt < self.maxinterval:
                    return

            self._ema_dn.update(dn)
            self._ema_dt.update(dt)
            self._refresh()
            self._last_print_n = self.n
            self._last_print_t = cur_t
            self._auto_tune_miniters(dn, dt)

    def close(self) -> None:
        """Finalize the bar.  Idempotent -- safe to call multiple times."""
        if self._closed:
            return
        self._closed = True
        self._stop_animation_thread()

        if self.disable:
            return

        with self._lock:
            if self.leave:
                self._render_final()
                self.file.write("\n")
            else:
                if self._prev_height > 0:
                    erase_lines(self.file, self._prev_height)
                elif self._terminal.is_tty:
                    # Fallback mode: single line, just erase it
                    self.file.write("\r\033[2K")
            self.file.flush()

    def __enter__(self) -> NyanBar:
        """Enter context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager -- always calls close()."""
        self.close()

    def set_description(self, desc: str | None = None, refresh: bool = True) -> None:
        """Set the bar description."""
        self._desc = desc
        if refresh and not self._closed and not self.disable:
            self._refresh()

    def set_postfix(
        self,
        ordered_dict: dict[str, Any] | None = None,
        refresh: bool = True,
        **kwargs: Any,
    ) -> None:
        """Set postfix from a dict and/or keyword arguments."""
        items: dict[str, Any] = {}
        if ordered_dict is not None:
            items.update(ordered_dict)
        items.update(kwargs)
        self._postfix_str = ", ".join(f"{k}={v}" for k, v in items.items())
        if refresh and not self._closed and not self.disable:
            self._refresh()

    def set_postfix_str(self, s: str, refresh: bool = True) -> None:
        """Set postfix from a raw string."""
        self._postfix_str = s
        if refresh and not self._closed and not self.disable:
            self._refresh()

    @classmethod
    def write(cls, s: str, file: IO[str] | None = None, end: str = "\n") -> None:
        """Write a message clearing the current bar line first."""
        fp = file if file is not None else sys.stdout
        fp.write("\r\033[2K")
        fp.write(s + end)
        fp.flush()

    # ── Animation thread ───────────────────────────────────────

    def _start_animation_thread(self) -> None:
        """Start the background animation thread if appropriate."""
        if self._use_fallback or self.disable or self._animation is None:
            return
        if self._running:
            return  # already started
        self._running = True
        t = threading.Thread(target=self._animation_loop, daemon=True)
        t.start()
        self._anim_thread = t

    def _stop_animation_thread(self) -> None:
        """Signal the animation thread to stop."""
        self._running = False
        # Don't join -- daemon thread dies naturally

    def _animation_loop(self) -> None:
        """Background animation loop.  Lock held only during render."""
        fps = self._animation.fps if self._animation else 12.0
        interval = 1.0 / fps
        while self._running:
            time.sleep(interval)
            with self._lock:
                if not self._running or self._closed:
                    break
                self._render_animation_frame()

    def _render_animation_frame(self) -> None:
        """Render one animation frame.  Called from daemon thread with lock held."""
        if self._animation is None:
            return
        elapsed = time.monotonic() - self._start_t
        progress = (self.n / self.total) if self.total and self.total > 0 else 0.0
        ncols = self._effective_width()

        # Get animation lines
        anim_lines = render_animation(
            self._animation, progress, ncols, elapsed,
        )

        # Get stats string
        rate = self._compute_rate()
        stats = format_meter(
            n=self.n,
            total=self.total,
            elapsed=elapsed,
            rate=rate,
            unit=self.unit,
            ncols=ncols,
            desc=self._desc,
            postfix_str=self._postfix_str,
            unit_scale=self.unit_scale,
        )

        # Compose: animation lines + stats on last line
        if anim_lines:
            composed = list(anim_lines)
            composed.append(stats)
        else:
            composed = [stats]

        self._prev_height = render_frame(composed, self._prev_height, self.file)

    # ── Internal methods ─────────────────────────────────────

    def _refresh(self) -> None:
        """Refresh the display with current progress."""
        # When animation thread is running, it handles all rendering
        if self._running:
            return

        # When animation is available but thread hasn't started yet
        # (e.g. manual update() mode), render animation frame directly
        if not self._use_fallback and self._animation is not None:
            self._render_animation_frame()
            return

        elapsed = time.monotonic() - self._start_t
        rate = self._compute_rate()
        ncols = self._effective_width()

        line = render_fallback_bar(
            n=self.n,
            total=self.total,
            elapsed=elapsed,
            rate=rate,
            unit=self.unit,
            ncols=ncols,
            desc=self._desc,
            postfix_str=self._postfix_str,
            unit_scale=self.unit_scale,
        )

        if self._terminal.is_tty:
            self.file.write("\r" + line)
        else:
            self.file.write(line + "\n")
        self.file.flush()

    def _render_final(self) -> None:
        """Render the final bar state (for leave=True)."""
        elapsed = time.monotonic() - self._start_t
        rate = self._compute_rate()
        ncols = self._effective_width()

        if self._animation is not None and not self._use_fallback:
            # Render final animation frame (completion state)
            anim_lines = render_animation(
                self._animation, 1.0, ncols, elapsed,
            )
            stats = format_meter(
                n=self.n, total=self.total, elapsed=elapsed, rate=rate,
                unit=self.unit, ncols=ncols, desc=self._desc,
                postfix_str=self._postfix_str, unit_scale=self.unit_scale,
            )
            composed = list(anim_lines) + [stats] if anim_lines else [stats]
            self._prev_height = render_frame(composed, self._prev_height, self.file)
        else:
            line = render_fallback_bar(
                n=self.n,
                total=self.total,
                elapsed=elapsed,
                rate=rate,
                unit=self.unit,
                ncols=ncols,
                desc=self._desc,
                postfix_str=self._postfix_str,
                unit_scale=self.unit_scale,
            )

            if self._terminal.is_tty:
                self.file.write("\r" + line)
            else:
                self.file.write(line)

    def _compute_rate(self) -> float | None:
        """Compute current iteration rate from EMA."""
        if self._ema_dn.value is not None and self._ema_dt.value is not None:
            if self._ema_dt.value > 0:
                return self._ema_dn.value / self._ema_dt.value
        return None

    def _effective_width(self) -> int:
        """Return effective bar width in columns."""
        if self.ncols is not None:
            return self.ncols
        if self.dynamic_ncols:
            import shutil
            width = shutil.get_terminal_size(fallback=(80, 24)).columns
        else:
            width = self._terminal.width
        return max(width - 1, 10)  # reserve 1 col to prevent line wrap

    def _auto_tune_miniters(self, dn: float, dt: float) -> None:
        """Auto-tune miniters based on recent refresh performance."""
        if dt <= 0:
            return
        self._miniters = max(
            1,
            int(
                self.smoothing * dn * (self.mininterval / dt)
                + (1 - self.smoothing) * self._miniters
            ),
        )
