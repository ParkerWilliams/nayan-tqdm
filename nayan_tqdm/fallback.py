"""Fallback rendering for nayan_tqdm.

Provides decision logic for when to use fallback (non-animated) rendering,
and a plain-text tqdm-style progress bar with no ANSI escape sequences.

Self-contained: uses inline helpers rather than importing from formatters.py
to keep modules independent during parallel development.
"""
from __future__ import annotations

from .terminal import TerminalInfo, ColorTier

__all__ = ["should_use_fallback", "render_fallback_bar"]


# ── Decision logic ───────────────────────────────────────────


def should_use_fallback(
    info: TerminalInfo,
    disable: bool = False,
    position: int | None = None,
) -> bool:
    """Determine whether to use plain-text fallback rendering.

    Returns ``True`` if animation should be skipped and a simple text
    bar used instead.  Falls back silently -- no warnings emitted.

    Parameters
    ----------
    info:
        Terminal capabilities snapshot.
    disable:
        If ``True``, the bar is fully disabled (force fallback).
    position:
        Bar position index.  ``0`` is the primary bar; ``> 0`` means
        nested (which gets fallback to avoid multi-bar animation conflicts).
    """
    if disable:
        return True
    if not info.is_tty:
        return True
    # Note: ColorTier.NONE on a TTY (dumb terminal) does NOT force fallback.
    # Dumb TTY terminals get ASCII-tier theme animation instead.
    if info.width < 30:
        return True
    if position is not None and position > 0:
        return True
    return False


# ── Inline formatting helpers (self-contained) ───────────────


_SI_SUFFIXES = ("", "k", "M", "G", "T", "P", "E", "Z", "Y")


def _fb_si_format(value: float, precision: int = 2) -> str:
    """Format *value* with SI suffixes."""
    negative = value < 0
    value = abs(value)
    idx = 0
    while value >= 1000.0 and idx < len(_SI_SUFFIXES) - 1:
        value /= 1000.0
        idx += 1
    formatted = f"{value:.{precision}f}{_SI_SUFFIXES[idx]}"
    return f"-{formatted}" if negative else formatted


def _fb_format_interval(seconds: float) -> str:
    """Format *seconds* as ``MM:SS`` or ``H:MM:SS``."""
    total = int(seconds)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


# ── Plain text bar rendering ─────────────────────────────────


def render_fallback_bar(
    n: int,
    total: int | None,
    elapsed: float,
    rate: float | None,
    unit: str = "it",
    ncols: int = 80,
    desc: str | None = None,
    postfix_str: str | None = None,
    unit_scale: bool = False,
) -> str:
    """Render a plain-text tqdm-style progress bar.

    Returns a single line string with NO ANSI escape sequences.
    The caller handles cursor positioning (``\\r`` for TTY, ``\\n`` for pipe).

    Parameters
    ----------
    n:
        Current iteration count.
    total:
        Total iterations, or ``None`` for indeterminate mode.
    elapsed:
        Seconds elapsed.
    rate:
        Current rate in iterations/second, or ``None`` if unknown.
    unit:
        Iteration unit label (e.g. ``"it"``).
    ncols:
        Target line width in columns.
    desc:
        Optional description prefix.
    postfix_str:
        Optional postfix string appended to stats.
    unit_scale:
        If ``True``, format counts and rate with SI suffixes.
    """

    def _fmt_count(v: int) -> str:
        return _fb_si_format(float(v)) if unit_scale else str(v)

    def _fmt_rate(r: float | None) -> str:
        if r is None:
            return f"?{unit}/s"
        if unit_scale:
            return f"{_fb_si_format(r)}{unit}/s"
        return f"{r:.2f}{unit}/s"

    desc_prefix = f"{desc}: " if desc else ""
    postfix_suffix = f", {postfix_str}" if postfix_str else ""

    n_str = _fmt_count(n)

    if total is not None:
        # Determinate mode
        pct = (n / total * 100) if total > 0 else 0.0
        total_str = _fmt_count(total)
        rate_str = _fmt_rate(rate)
        if rate is not None and rate > 0:
            eta_str = _fb_format_interval((total - n) / rate)
        else:
            eta_str = "?"
        elapsed_str = _fb_format_interval(elapsed)
        time_stats = f" [{elapsed_str}<{eta_str}, {rate_str}]"
        count_str = f" {n_str}/{total_str}"

        # Calculate bar width
        pct_str = f"{pct:3.0f}%"
        # Fixed parts: desc + pct + "||" + count + time + postfix
        fixed_parts = f"{desc_prefix}{pct_str}||{count_str}{time_stats}{postfix_suffix}"
        fixed_len = len(fixed_parts)
        bar_width = max(ncols - fixed_len, 10)
        filled = int(bar_width * pct / 100)
        bar = "#" * filled + " " * (bar_width - filled)
        return f"{desc_prefix}{pct_str}|{bar}|{count_str}{time_stats}{postfix_suffix}"
    else:
        # Indeterminate mode
        elapsed_str = _fb_format_interval(elapsed)
        rate_str = _fmt_rate(rate)
        return f"{desc_prefix}{n_str}{unit} [{elapsed_str}, {rate_str}]{postfix_suffix}"
