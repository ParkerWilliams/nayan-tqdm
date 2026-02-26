# Phase 2: Core Integration - Research

**Researched:** 2026-02-25
**Domain:** Python progress bar — tqdm-compatible API, thread-safe background tick, EMA rate smoothing, terminal cleanup, fallback rendering
**Confidence:** HIGH

## Summary

Phase 2 implements the `NyanBar` class: a standalone, zero-dependency reimplementation of tqdm's user-facing API. It draws on the Phase 1 primitives (`models.py`, `terminal.py`, `renderer.py`, `engine.py`) and integrates them into a single cohesive class that handles iteration, stat computation, refresh throttling, background animation ticking, fallback rendering, and terminal cleanup.

The design is deliberately tqdm-compatible at the API surface without inheriting from or importing tqdm. All tqdm kwargs are accepted (`desc`, `unit`, `unit_scale`, `leave`, `disable`, `file`, `ncols`, `mininterval`, `position`, etc.). Unknown kwargs are silently swallowed via `**kwargs`. The stats format mirrors tqdm exactly: `  0%|          | 0/100 [00:00<?, ?it/s]` with EMA smoothing at `smoothing=0.3` for stable rate display.

The most complex subdomain is the two-gate refresh throttle (iteration count gate + time gate) combined with the background animation daemon thread. These two must be carefully coordinated with a single `threading.Lock`: the main thread owns all state mutations, the daemon thread only reads state and calls render. Terminal cleanup (`leave=True/False`), exception safety (`__exit__`), and nested bar isolation (`position > 0` → single-line fallback) round out the implementation surface.

**Primary recommendation:** Build `NyanBar` as a standalone class in `nyanbar/core.py` with a clear internal separation between (a) state tracking, (b) refresh-throttle logic, (c) stat formatting, and (d) the background animation thread lifecycle.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Stats Display Format
- Match tqdm's exact format string: `  0%|          | 0/100 [00:00<?, ?it/s]`
- Stats appear on the same line as the animation, to the right
- Rate/ETA use exponential moving average (EMA) smoothing with `smoothing=0.3` default — stable, not jumpy
- `set_description()` and `set_postfix()` match tqdm behavior exactly: desc= prefix, postfix appends key=value pairs
- `unit_scale=True` auto-formats with SI suffixes (k, M, G, T)
- `total=None` (indeterminate): no bar, just count + rate + elapsed like tqdm: `1000it [00:05, 200it/s]`

#### Plain Text Fallback
- tqdm-style text bar: `50%|#####     | 50/100 [00:05<00:05, 10it/s]`
- Uses `\r` carriage return to overwrite in-place when terminal supports it; falls through to newlines only when truly piped
- Triggers silently — no warning or stderr notice when falling back
- Fallback conditions (from Phase 1 context): non-TTY, piped output, TERM=dumb, terminal width < 30 columns

#### tqdm API Surface
- Full instance API: `__iter__`, `__enter__`/`__exit__`, `update()`, `close()`, `set_description()`, `set_postfix()`, `set_postfix_str()`, `write()`
- `tqdm.write()` class/static method supported (clears bar, prints, redraws)
- `tqdm.pandas()` NOT supported — out of scope
- `bar_format=` silently accepted but ignored (no format string parser)
- Unknown kwargs silently accepted via `**kwargs` — maximum compatibility, scripts just work
- All display kwargs honored: `desc=`, `unit=`, `unit_scale=`, `leave=`, `disable=`, `file=`, `ncols=`, `mininterval=`, `position=`
- `trange(n)` works identically to `tqdm(range(n))`

#### Refresh Throttling
- Match tqdm's mininterval/maxinterval system: `mininterval=0.1s` (10Hz cap), `maxinterval=10s` (force redraw if stalled)
- Dynamic miniters with auto-tuning — critical for tight loops (millions of iterations/sec) to avoid write overhead
- Animation frame rate decoupled from stats refresh rate
- Background daemon thread for animation ticks at theme FPS (e.g., 12Hz)
- **Thread simplicity constraint:** daemon thread ONLY ticks frame counter and calls render. All state updates (n, rate, etc.) happen in main thread with a lock. No thread pools, no async, no queues.
- Thread dies automatically via daemon flag if main thread crashes

### Claude's Discretion
- Internal NyanBar class architecture (method decomposition, private helpers)
- Exact miniters auto-tuning algorithm
- Lock granularity for thread safety
- How animation thread lifecycle integrates with `__enter__`/`__exit__`
- Stats string formatting implementation details

### Deferred Ideas (OUT OF SCOPE)
- Wander mode (rate-proportional sprite movement for `total=None`) — Phase 3
- Chase mode (two sprites, cat chases mouse/yarn ball for `total=None`) — Phase 3
- Frustrated worker emoji / table flip Easter eggs — future phase or theme personality
- `tqdm.pandas()` integration — out of scope for v1
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CORE-01 | NyanBar implements tqdm-compatible API (total, desc, unit, disable, file, etc.) with zero dependencies | tqdm `__init__` parameter list verified; silent `**kwargs` swallow enables forward compatibility |
| CORE-02 | `from nyanbar import tqdm` works as a drop-in replacement for `from tqdm import tqdm` | `nyanbar/__init__.py` exports `NyanBar as tqdm`; `trange` is a thin wrapper |
| CORE-03 | `trange(n)` shorthand works identically to `tqdm(range(n))` | `trange = lambda n, *args, **kwargs: NyanBar(range(n), *args, **kwargs)` |
| CORE-04 | NyanBar implements `__iter__`, `__enter__`/`__exit__`, `update()`, `close()`, `set_description()`, `set_postfix()` | Patterns verified from tqdm source; `__exit__` must call `close()` even on exception |
| CORE-05 | Non-TTY and piped output falls back to plain built-in text bar with no ANSI sequences | `TerminalInfo.is_tty` from Phase 1; fallback uses `\r` overwrite or plain newlines |
| CORE-06 | Dumb terminal (`TERM=dumb`) falls back to plain built-in text bar | `TerminalInfo.color_support == ColorTier.NONE` already detected by Phase 1 `terminal.py` |
| CORE-07 | Terminal width < 30 columns falls back to plain built-in text bar | Width read from `TerminalInfo.width`; threshold check in `_should_use_fallback()` |
| CORE-08 | Stats display (percentage, rate, ETA) renders alongside animation | EMA-smoothed rate (`smoothing=0.3`); ETA = `(total - n) / rate`; SI suffix for `unit_scale=True` |
| CORE-09 | `leave=True` preserves final animation frame; `leave=False` cleans up all lines | `close()` checks `leave` flag; `erase_lines()` from Phase 1 `renderer.py` handles cleanup |
| CORE-10 | Nested bars (`position > 0`) disable multi-line and use single-line fallback | `position` kwarg check in `__init__`; single-line fallback path reused from CORE-05–07 |
| CORE-11 | Exception during iteration cleans up terminal state correctly | `__exit__(exc_type, ...)` calls `close()` unconditionally; close erases lines before re-raising |
| CORE-12 | Thread safety via `threading.Lock` for concurrent access | Single `threading.Lock` guards `n`, `_rate_ema`, `_last_print_t`, `_prev_height`; daemon thread holds lock only during render calls |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `threading` (stdlib) | Python 3.10+ | Background animation daemon thread + Lock | Built-in, zero-dep, daemon=True auto-terminates on main exit |
| `time` (stdlib) | Python 3.10+ | `time.monotonic()` for elapsed, throttle gates | Already used in Phase 1 engine; monotonic, immune to clock adjustments |
| `io` (stdlib) | Python 3.10+ | `io.StringIO` for file= kwarg type | Used in tests; `IO[str]` type annotation |
| `sys` (stdlib) | Python 3.10+ | `sys.stderr` default output stream | Matches tqdm convention |
| All Phase 1 modules | — | `models.py`, `terminal.py`, `renderer.py`, `engine.py`, `utils.py` | Already built and tested |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `shutil` (stdlib) | Python 3.10+ | `get_terminal_size()` for dynamic ncols | When `ncols=None` and `dynamic_ncols=True` |
| `contextlib` (stdlib) | Python 3.10+ | Optionally used for `external_write_mode`-style context | For `write()` classmethod implementation |
| `unicodedata` (stdlib) | Python 3.10+ | Already in `utils.py`; used in stat string width calc | Reuse `disp_len()` from Phase 1 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Standalone `NyanBar` class | Subclass `tqdm.tqdm` | Subclassing adds tqdm as a dependency — violates zero-dep constraint |
| `threading.Lock` | `threading.RLock` | RLock only needed for reentrant locking; a plain Lock is sufficient and faster |
| Daemon thread for animation | `asyncio` or `threading.Timer` | asyncio requires `async`-aware callers; Timer fires once. Daemon loop is simpler and matches constraint |
| Custom EMA class | Rolling deque with mean | EMA is O(1) per update, well-understood, and matches tqdm's `smoothing=0.3` default |

**Installation:** None required — all stdlib.

## Architecture Patterns

### Recommended Project Structure
```
nyanbar/
├── __init__.py       # Exports NyanBar as tqdm, trange (Phase 4 finalizes; Phase 2 stub)
├── core.py           # NEW: NyanBar class — the entire Phase 2 deliverable
├── models.py         # Phase 1 — Frame, Animation
├── utils.py          # Phase 1 — disp_len, strip_ansi
├── terminal.py       # Phase 1 — TerminalInfo, detect_terminal
├── renderer.py       # Phase 1 — erase_lines, render_frame, ensure_reset
└── engine.py         # Phase 1 — render_animation, select_frame_index, walk_position
```

Phase 2 adds exactly one new file: `nyanbar/core.py`.

### Pattern 1: Two-Gate Refresh Throttle
**What:** Each call to `update(n)` checks iteration count gate (`self.n - self._last_print_n >= self._miniters`) AND time gate (`dt >= self.mininterval`). Only when both pass does a display refresh occur.
**When to use:** In `update()` and inlined in `__iter__` for performance.
**Example:**
```python
def update(self, n: int = 1) -> None:
    with self._lock:
        self.n += n
        if self.n - self._last_print_n >= self._miniters:
            cur_t = time.monotonic()
            dt = cur_t - self._last_print_t
            if dt >= self.mininterval:
                self._refresh(cur_t, dt)
                self._last_print_n = self.n
                self._last_print_t = cur_t
                self._auto_tune_miniters(dt, n)
```

### Pattern 2: EMA Rate Smoothing
**What:** Track rate using exponential moving average over (dn, dt) pairs. `rate = ema_dn / ema_dt`.
**When to use:** In `_refresh()` after each gate-passing update.
**Example:**
```python
# alpha = smoothing = 0.3
def _update_ema(self, dn: float, dt: float) -> None:
    alpha = self.smoothing
    if self._ema_dn is None:
        # First sample — seed the EMA
        self._ema_dn = dn
        self._ema_dt = dt
    else:
        self._ema_dn = alpha * dn + (1 - alpha) * self._ema_dn
        self._ema_dt = alpha * dt + (1 - alpha) * self._ema_dt

def _rate(self) -> float | None:
    """Returns iterations per second, or None if unknown."""
    if self._ema_dt and self._ema_dt > 0:
        return self._ema_dn / self._ema_dt
    return None
```

### Pattern 3: Background Animation Daemon Thread
**What:** A single daemon thread runs a `while self._running:` loop, sleeping at the animation frame interval, acquiring the lock briefly to read state and call render.
**When to use:** Started in `__enter__` (or `__init__` for non-context-manager use), stopped in `close()`.
**Example:**
```python
def _start_animation_thread(self) -> None:
    self._running = True
    t = threading.Thread(target=self._animation_loop, daemon=True)
    t.start()
    self._anim_thread = t

def _animation_loop(self) -> None:
    interval = 1.0 / self._animation.fps  # e.g., 1/12 ≈ 83ms
    while self._running:
        time.sleep(interval)
        with self._lock:
            self._render_frame()

def _stop_animation_thread(self) -> None:
    self._running = False
    # No join — daemon thread; let it die naturally
```

### Pattern 4: Fallback Path Decision
**What:** At construction time, compute whether to use ANSI animation or plain-text fallback. Store as `self._use_fallback: bool`. All render paths check this flag.
**When to use:** Once, in `__init__`, based on `TerminalInfo`.
**Example:**
```python
def _should_use_fallback(self, info: TerminalInfo, ncols: int | None) -> bool:
    if self.disable:
        return True
    if not info.is_tty:
        return True  # piped / non-TTY
    if info.color_support == ColorTier.NONE:
        return True  # TERM=dumb or NO_COLOR
    effective_width = ncols or info.width
    if effective_width < 30:
        return True  # too narrow
    if self.position is not None and self.position > 0:
        return True  # nested bar — single-line fallback
    return False
```

### Pattern 5: tqdm-Format Stats String
**What:** Build the stats string matching tqdm format: `  X%|bar | n/total [elapsed<eta, rate]`
**When to use:** In `_render_frame()` for both fallback (full bar) and animated (stats only, bar replaced by animation).
**Example:**
```python
def _format_stats(self, width: int) -> str:
    """Return a tqdm-compatible stats string, sized to fit width."""
    pct = (self.n / self.total * 100) if self.total else 0
    elapsed = time.monotonic() - self._start_t
    rate = self._rate()

    # Rate display with optional SI suffix
    if rate is None:
        rate_str = "?it/s"
    elif self.unit_scale:
        rate_str = f"{_si_format(rate)}{self.unit}/s"
    else:
        rate_str = f"{rate:.2f}{self.unit}/s"

    # ETA
    if self.total and rate:
        eta = (self.total - self.n) / rate
        eta_str = _format_interval(eta)
    else:
        eta_str = "?"

    elapsed_str = _format_interval(elapsed)

    if self.total:
        prefix = f"{pct:3.0f}%"
        suffix = f" {self.n}/{self.total} [{elapsed_str}<{eta_str}, {rate_str}]"
    else:
        # Indeterminate: no bar, no pct
        prefix = ""
        suffix = f"{self.n}{self.unit} [{elapsed_str}, {rate_str}]"

    # Add desc and postfix
    desc = (self.desc + ": ") if self.desc else ""
    postfix = (", " + self._postfix_str) if self._postfix_str else ""
    return desc + prefix + suffix + postfix
```

### Pattern 6: close() with leave and Cleanup
**What:** `close()` stops the animation thread, erases the bar lines, optionally reprints the final state, and handles `leave` semantics.
**When to use:** Called by `__exit__`, user code, and at natural end of iteration.
**Example:**
```python
def close(self) -> None:
    if self._closed:
        return
    self._closed = True
    self._stop_animation_thread()
    with self._lock:
        if self.disable:
            return
        if self.leave:
            # Print final bar and move to new line
            self._render_final()
            self.file.write("\n")
        else:
            # Erase all bar lines — leave terminal clean
            from nyanbar.renderer import erase_lines
            erase_lines(self.file, self._prev_height)
        self.file.flush()
```

### Anti-Patterns to Avoid
- **Acquiring lock in daemon thread for long periods:** Daemon thread should hold lock for the duration of a single render call only — never during `time.sleep()`.
- **Checking time inside lock:** Read `time.monotonic()` before acquiring the lock; pass the timestamp in. Reduces lock contention.
- **Starting animation thread for disabled/fallback bars:** Check `self._use_fallback` before starting the thread. Plain-text fallback has no animation thread.
- **Not guarding `close()` with `_closed` flag:** `close()` may be called multiple times (iterator exhausted AND `with` block exit). Always guard.
- **Forgetting `__iter__` optimization:** tqdm inlines local variable references for speed in the hot path. For tight loops, `update()` method call overhead is significant. Consider inlining the two-gate check in `__iter__`.
- **Using `threading.Event` for `_running` flag:** A plain `bool` guarded by the lock is simpler and sufficient; `Event` adds complexity with no benefit here.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Monotonic timing | Custom `time.time()` delta | `time.monotonic()` (Phase 1 pattern) | Already in use; immune to NTP/DST jumps |
| Terminal cleanup | Custom ANSI erase logic | `erase_lines()` from `renderer.py` | Already built and tested in Phase 1 |
| Terminal detection | Re-detect per update | `TerminalInfo` from Phase 1 `detect_terminal()` | Detect once at construction; frozen dataclass |
| SI suffix formatting | External library | Simple inline loop: `while val >= 1000: val /= 1000; i += 1` | Zero-dep requirement; the algorithm is 5 lines |
| Time interval formatting | `datetime.timedelta` | Simple `f"{int(s//3600):02d}:{int(s%3600//60):02d}:{int(s%60):02d}"` | Zero-dep; tqdm format is HH:MM:SS |
| Unicode width | Manual char-width table | `disp_len()` from `utils.py` | Already built and tested in Phase 1 |

**Key insight:** The entire Phase 1 layer exists precisely to avoid hand-rolling these in Phase 2. Reference Phase 1 modules; don't rebuild.

## Common Pitfalls

### Pitfall 1: Race Between Main Thread and Daemon Thread
**What goes wrong:** Daemon thread renders a stale bar (with old `n`) while main thread is mid-update, causing flickering or incorrect stats.
**Why it happens:** `n` and display state are shared without synchronization.
**How to avoid:** Single `threading.Lock` acquired by daemon thread for the entire `_render_frame()` call. Main thread acquires the same lock in `update()` for all state mutations.
**Warning signs:** Progress percentage jumps backward; rate shows 0 mid-run.

### Pitfall 2: Animation Thread Not Stopped on Exception
**What goes wrong:** Exception in the user's loop (`for x in tqdm(items): ...`) propagates without calling `close()`. Animation thread keeps running after the loop ends.
**Why it happens:** `__exit__` not called, or called with `exc_type` but not handling cleanup.
**How to avoid:** `__exit__` must call `close()` unconditionally regardless of `exc_type`. `daemon=True` on the thread ensures it dies when the Python process exits, but in a long-lived process the thread would persist until GC.
**Warning signs:** Animation keeps printing after an exception; terminal left in dirty state.

### Pitfall 3: Double-Close
**What goes wrong:** `close()` called twice (once by `__iter__` on exhaustion, once by `__exit__`). Second call erases a line that was already cleaned up, corrupting terminal.
**Why it happens:** tqdm's pattern calls `close()` at the natural end of iteration AND `__exit__` calls it again.
**How to avoid:** Guard with `if self._closed: return` at the top of `close()`.
**Warning signs:** Final bar disappears or extra blank lines appear after the loop.

### Pitfall 4: miniters Auto-Tuning Overshoot in Burst Loops
**What goes wrong:** A burst of fast iterations early in a loop auto-tunes `miniters` very high. When iteration slows down (e.g., network I/O), the bar stalls for up to `maxinterval` seconds before refreshing.
**Why it happens:** `dynamic_miniters` sets `miniters` proportionally to throughput. High throughput → high `miniters`. Then rate drops; `miniters` too high for new rate.
**How to avoid:** The `maxinterval` gate catches this: if `dt >= maxinterval (10s)`, force a refresh and re-tune `miniters`. Implement both gates.
**Warning signs:** Bar freezes mid-loop when processing speed drops.

### Pitfall 5: `disable=True` Still Starting Thread
**What goes wrong:** Even with `disable=True`, the animation daemon thread starts, consuming resources for no benefit.
**Why it happens:** Thread start called unconditionally in `__init__`.
**How to avoid:** Check `self.disable` (and `self._use_fallback`) before calling `_start_animation_thread()`.
**Warning signs:** `disable=True` bars still show CPU usage; test captures unexpected thread activity.

### Pitfall 6: `write()` Classmethod Race With Active Bars
**What goes wrong:** `tqdm.write("message")` prints a line while the animation thread is mid-render, garbling the output.
**Why it happens:** `write()` and the animation thread write to the same file concurrently.
**How to avoid:** `write()` should acquire the instance lock (or use a class-level lock if managing multiple instances), erase the current bar line, print the message, then redraw the bar.
**Warning signs:** Print output appears in the middle of the progress bar line.

### Pitfall 7: First-Render Edge Case with `_prev_height`
**What goes wrong:** On first render, `_prev_height = 0`, but if `erase_lines(0)` is called before the guard check, some terminals emit a cursor-up-0 sequence with undefined behavior.
**Why it happens:** Forgetting the `if prev_height > 0:` guard in `erase_lines()`.
**How to avoid:** Phase 1 `renderer.py` already has this guard (`if count <= 0: return`). Always pass `_prev_height` through Phase 1 `render_frame()`. Don't bypass it.
**Warning signs:** First bar render shows garbled text or extra blank lines.

### Pitfall 8: `ncols` vs `TerminalInfo.width` Confusion
**What goes wrong:** Bar renders wider than the terminal, causing line wrapping and destroying the animation.
**Why it happens:** Using `TerminalInfo.width` when the user passed `ncols=` explicitly.
**How to avoid:** `effective_width = self.ncols or self._terminal.width`. Always use `effective_width` for bar sizing. Reserve 1 column to prevent wrap at exact terminal width.
**Warning signs:** Animation wraps to next line; cursor positioning is off by 1 line.

### Pitfall 9: `set_postfix()` dict ordering
**What goes wrong:** Postfix dict renders in unpredictable order across Python versions.
**Why it happens:** Plain `dict` iteration order is insertion-ordered in 3.7+ but users may pass `**kwargs` which may arrive in any order.
**How to avoid:** Use `collections.OrderedDict` if user passes an ordered dict; for `**kwargs` form, sort keys or maintain insertion order per Python 3.7+ guarantee.
**Warning signs:** Postfix keys shuffle between renders.

## Code Examples

Verified patterns from tqdm source (fetched 2026-02-25) and stdlib documentation:

### NyanBar Class Skeleton
```python
# nyanbar/core.py
from __future__ import annotations

import sys
import time
import threading
from collections.abc import Iterable, Iterator
from typing import IO, Any

from .terminal import detect_terminal, ColorTier
from .renderer import erase_lines, render_frame, ensure_reset
from .engine import render_animation
from .models import Animation, AnimationMode


class NyanBar:
    """tqdm-compatible animated progress bar. Zero dependencies."""

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
        postfix: dict | None = None,
        unit_divisor: int = 1000,
        **kwargs: Any,   # unknown kwargs silently swallowed
    ) -> None:
        ...
```

### Two-Gate Throttle in `__iter__`
```python
def __iter__(self) -> Iterator[Any]:
    if self.iterable is None:
        raise TypeError("NyanBar requires an iterable")
    # Inline references for hot-path performance
    mininterval = self.mininterval
    miniters = self._miniters
    last_print_n = self._last_print_n
    last_print_t = self._last_print_t
    n = self.n

    for obj in self.iterable:
        yield obj
        n += 1
        if n - last_print_n >= miniters:
            cur_t = time.monotonic()
            if cur_t - last_print_t >= mininterval:
                self._update_display(n, cur_t, last_print_n, last_print_t)
                last_print_n = n
                last_print_t = cur_t
                miniters = self._miniters  # re-read after auto-tune
    self.n = n
    self.close()
```

### EMA Rate Tracker
```python
class _EMA:
    """Exponential moving average for rate smoothing."""
    def __init__(self, alpha: float = 0.3) -> None:
        self.alpha = alpha
        self._value: float | None = None

    def update(self, x: float) -> None:
        if self._value is None:
            self._value = x
        else:
            self._value = self.alpha * x + (1 - self.alpha) * self._value

    @property
    def value(self) -> float | None:
        return self._value
```

### SI Suffix Formatter (Zero-Dep)
```python
_SI_SUFFIXES = ("", "k", "M", "G", "T", "P", "E", "Z", "Y")

def _si_format(value: float, precision: int = 2) -> str:
    """Format value with SI suffix. 1500 → '1.50k'."""
    i = 0
    while abs(value) >= 1000.0 and i < len(_SI_SUFFIXES) - 1:
        value /= 1000.0
        i += 1
    return f"{value:.{precision}f}{_SI_SUFFIXES[i]}"
```

### Interval Formatter (Zero-Dep)
```python
def _format_interval(seconds: float) -> str:
    """Format seconds as MM:SS or HH:MM:SS."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
```

### Stats String for Indeterminate Mode
```python
# total=None: "1000it [00:05, 200.00it/s]"
def _format_indeterminate(self, elapsed: float) -> str:
    rate = self._ema_dn.value / self._ema_dt.value if (
        self._ema_dn.value and self._ema_dt.value
    ) else None
    n_str = _si_format(self.n) if self.unit_scale else str(self.n)
    rate_str = f"{_si_format(rate)}{self.unit}/s" if rate else f"?{self.unit}/s"
    return f"{n_str}{self.unit} [{_format_interval(elapsed)}, {rate_str}]"
```

### `trange` Shorthand
```python
def trange(n: int, *args: Any, **kwargs: Any) -> NyanBar:
    """Shorthand for NyanBar(range(n), ...)."""
    return NyanBar(range(n), *args, **kwargs)
```

### `write()` Classmethod
```python
@classmethod
def write(cls, s: str, file: IO[str] | None = None, end: str = "\n") -> None:
    """Print message without disturbing active bars."""
    fp = file if file is not None else sys.stdout
    # Erase current bar line, print message, let next tick redraw
    fp.write("\r\033[K")  # CR + erase line
    fp.write(s + end)
    fp.flush()
```

### Fallback Plain-Text Bar
```python
def _render_fallback(self, file: IO[str]) -> None:
    """Plain tqdm-style ASCII bar. No ANSI animation sequences."""
    width = self._effective_width()
    if self.total:
        pct = self.n / self.total
        bar_width = max(width - 40, 10)  # reserve space for stats
        filled = int(pct * bar_width)
        bar = "#" * filled + " " * (bar_width - filled)
        line = f"\r{pct*100:3.0f}%|{bar}| {self.n}/{self.total} [{self._elapsed_str()}<{self._eta_str()}, {self._rate_str()}]"
    else:
        line = f"\r{self.n}{self.unit} [{self._elapsed_str()}, {self._rate_str()}]"
    file.write(line)
    file.flush()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `tqdm` subclass | Standalone reimplementation | Phase 2 design decision | Zero-dep; no tqdm import; full control |
| Iteration-count-only throttle | Two-gate throttle (miniters + mininterval) | tqdm 3.x+, now standard | Handles both CPU-bound and IO-bound loops |
| Simple rate average | EMA smoothing (`smoothing=0.3`) | tqdm 4.x | Stable rate display; doesn't jump on bursts |
| Global `_instances` list for write() | Per-instance lock | Design preference | Simpler; avoid global state |
| `time.time()` for timing | `time.monotonic()` | Phase 1 established | Immune to clock adjustments |

**Deprecated/outdated:**
- `time.clock()`: Removed in Python 3.8. Not applicable; we use `time.monotonic()`.
- Subclassing `tqdm.tqdm`: Violates zero-dep constraint per REQUIREMENTS.md. Use standalone implementation.

## Open Questions

1. **`write()` classmethod: global lock vs per-instance**
   - What we know: tqdm uses a class-level `_instances` WeakSet to track all active bars and clear them all in `write()`. This requires class-level state.
   - What's unclear: Is per-instance coordination sufficient for Phase 2's single-bar use case, or does Phase 2 need to handle multiple simultaneous instances properly?
   - Recommendation: For Phase 2, track instances in a class-level `WeakSet` with a class-level lock. This is the correct approach even if nested bars (CORE-10) are handled via fallback — `write()` still needs to clear all active bars.

2. **Animation thread start point: `__init__` vs `__enter__`**
   - What we know: CONTEXT.md leaves animation thread lifecycle to Claude's discretion. Starting in `__init__` means the thread starts even for non-`with` users (e.g., `bar = NyanBar(range(100)); for x in bar: ...`).
   - What's unclear: Starting in `__iter__` is more correct (thread lives only while iterating), but adds complexity.
   - Recommendation: Start in `__iter__` and stop in `close()`. This handles both context-manager and direct iteration use cases. Guard against double-start with `_anim_thread_started: bool` flag.

3. **`miniters` auto-tuning: EMA vs simple rescaling**
   - What we know: tqdm's auto-tuning (from source): `miniters = smoothing * delta_it * (mininterval / delta_t) + (1 - smoothing) * self.miniters` when no `maxinterval` override. When `delta_t >= maxinterval`, rescale proportionally.
   - What's unclear: Whether the full EMA-based tuning or a simpler `miniters = max(1, int(delta_it * mininterval / delta_t))` is sufficient.
   - Recommendation: Implement the full EMA auto-tune to match tqdm behavior (ensures TEST-01 compatibility).

## Sources

### Primary (HIGH confidence)
- tqdm `std.py` source (fetched 2026-02-25 via WebFetch) — `__init__` parameters, `update()` two-gate logic, EMA implementation, `close()` leave handling, `write()` classmethod
- Python `threading` documentation — `daemon=True` behavior, `Lock` primitives
- Python `time.monotonic` documentation — monotonic clock behavior
- Phase 1 codebase (`models.py`, `terminal.py`, `renderer.py`, `engine.py`) — verified existing interfaces

### Secondary (MEDIUM confidence)
- tqdm issue #609 (EMA smoothing) — confirmed `smoothing=0.3` default rationale
- tqdm documentation (tqdm.github.io/docs/tqdm/) — parameter defaults and descriptions
- Real Python threading guides — daemon thread lifecycle patterns
- WebSearch: tqdm mininterval/miniters auto-tuning pattern — multiple sources confirm dual-gate approach

### Tertiary (LOW confidence)
- C tqdm reimplementation article (Medium) — SI suffix algorithm; matches stdlib-verifiable pattern so upgraded to MEDIUM confidence for the algorithm itself
- WebSearch: `write()` static vs classmethod implementations — Ultralytics pattern cited; tqdm's own classmethod pattern is HIGH confidence via direct source fetch

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib; Phase 1 modules already built and tested
- Architecture: HIGH — directly derived from tqdm source code (fetched) + Phase 1 primitives
- Pitfalls: HIGH — derived from tqdm source patterns, threading documentation, and Phase 1 established patterns
- EMA/throttle: HIGH — verified against tqdm source; formulas cross-checked

**Research date:** 2026-02-25
**Valid until:** 2026-05-25 (stable stdlib APIs + tqdm API is stable; 90-day validity)
