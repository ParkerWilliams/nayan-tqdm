"""Stats formatting utilities for nayan_tqdm.

Provides EMA rate tracking, SI suffix formatting, time interval formatting,
and tqdm-compatible meter string building.  All functions are pure/stateless
except the EMA class which maintains smoothed state.
"""
from __future__ import annotations

from .utils import disp_len

__all__ = [
    "EMA",
    "si_format",
    "format_interval",
    "format_meter",
    "format_stats_left",
    "format_stats_right",
]


# ── EMA rate tracker ─────────────────────────────────────────


class EMA:
    """Exponential Moving Average tracker for smoothed rate estimation.

    Parameters
    ----------
    alpha:
        Smoothing factor in [0, 1].  Higher values weight recent samples
        more heavily.  Default ``0.3``.
    """

    __slots__ = ("_alpha", "_value")

    def __init__(self, alpha: float = 0.3) -> None:
        self._alpha = alpha
        self._value: float | None = None

    def update(self, x: float) -> None:
        """Feed a new sample *x* into the tracker."""
        if self._value is None:
            self._value = x
        else:
            self._value = self._alpha * x + (1 - self._alpha) * self._value

    @property
    def value(self) -> float | None:
        """Current smoothed value, or ``None`` if no samples yet."""
        return self._value


# ── SI suffix formatting ─────────────────────────────────────

_SI_SUFFIXES = ("", "k", "M", "G", "T", "P", "E", "Z", "Y")


def si_format(value: float, precision: int = 2) -> str:
    """Format *value* with SI suffixes (k, M, G, ...).

    Examples
    --------
    >>> si_format(1500.0)
    '1.50k'
    >>> si_format(42.0)
    '42.00'
    """
    negative = value < 0
    value = abs(value)
    idx = 0
    while value >= 1000.0 and idx < len(_SI_SUFFIXES) - 1:
        value /= 1000.0
        idx += 1
    formatted = f"{value:.{precision}f}{_SI_SUFFIXES[idx]}"
    return f"-{formatted}" if negative else formatted


# ── Time interval formatting ─────────────────────────────────


def format_interval(seconds: float) -> str:
    """Format *seconds* as ``MM:SS`` or ``H:MM:SS``.

    Fractional seconds are truncated (not rounded).

    Examples
    --------
    >>> format_interval(65)
    '01:05'
    >>> format_interval(3661)
    '1:01:01'
    """
    total = int(seconds)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


# ── Stats helpers (used by themed bar rendering) ──────────────


def format_stats_left(
    n: int,
    total: int | None,
    desc: str | None = None,
    unit_scale: bool = False,
) -> str:
    """Build the left-side stats string for themed bar rendering.

    Returns a string like ``" 50%"`` or ``"desc:  50%"``.
    For indeterminate mode (total is None), returns ``" 42it"`` style.
    """
    desc_prefix = f"{desc}: " if desc else ""
    if total is not None:
        pct = (n / total * 100) if total > 0 else 0.0
        return f"{desc_prefix}{pct:3.0f}%"
    n_str = si_format(float(n)) if unit_scale else str(n)
    return f"{desc_prefix}{n_str}"


def format_stats_right(
    n: int,
    total: int | None,
    elapsed: float,
    rate: float | None,
    unit: str = "it",
    postfix_str: str | None = None,
    unit_scale: bool = False,
) -> str:
    """Build the right-side stats string for themed bar rendering.

    Returns a string like ``" 50/100 [00:02<00:02, 29.00it/s]"``.
    """

    def _fmt_count(v: int) -> str:
        return si_format(float(v)) if unit_scale else str(v)

    def _fmt_rate(r: float | None) -> str:
        if r is None:
            return f"?{unit}/s"
        if unit_scale:
            return f"{si_format(r)}{unit}/s"
        return f"{r:.2f}{unit}/s"

    postfix_suffix = f", {postfix_str}" if postfix_str else ""
    n_str = _fmt_count(n)
    elapsed_str = format_interval(elapsed)
    rate_str = _fmt_rate(rate)

    if total is not None:
        total_str = _fmt_count(total)
        if rate is not None and rate > 0:
            eta_str = format_interval((total - n) / rate)
        else:
            eta_str = "?"
        return f" {n_str}/{total_str} [{elapsed_str}<{eta_str}, {rate_str}]{postfix_suffix}"
    else:
        return f" [{elapsed_str}, {rate_str}]{postfix_suffix}"


# ── Meter string builder ─────────────────────────────────────


def format_meter(
    n: int,
    total: int | None,
    elapsed: float,
    rate: float | None,
    unit: str = "it",
    ncols: int = 80,
    desc: str | None = None,
    postfix_str: str | None = None,
    unit_scale: bool = False,
    unit_divisor: int = 1000,
) -> str:
    """Build a tqdm-compatible stats line.

    Parameters
    ----------
    n:
        Current iteration count.
    total:
        Total iterations (``None`` for indeterminate mode).
    elapsed:
        Seconds elapsed.
    rate:
        Current rate in iterations/second (``None`` if unknown).
    unit:
        Iteration unit label.
    ncols:
        Target line width in columns.
    desc:
        Optional description prefix.
    postfix_str:
        Optional postfix string appended to stats.
    unit_scale:
        If ``True``, format counts with SI suffixes.
    unit_divisor:
        Divisor for SI scaling (default 1000).

    Returns
    -------
    str
        Formatted stats line matching tqdm's output format.
    """

    stats_left = format_stats_left(n, total, desc=desc, unit_scale=unit_scale)
    stats_right = format_stats_right(
        n, total, elapsed, rate,
        unit=unit, postfix_str=postfix_str, unit_scale=unit_scale,
    )

    if total is not None:
        # Determinate mode — build the bar portion
        pct = (n / total * 100) if total > 0 else 0.0
        fixed_parts = f"{stats_left}||{stats_right}"
        fixed_len = disp_len(fixed_parts)
        bar_width = max(ncols - fixed_len, 10)
        filled = int(bar_width * pct / 100)
        bar = "#" * filled + " " * (bar_width - filled)
        return f"{stats_left}|{bar}|{stats_right}"
    else:
        # Indeterminate mode
        return f"{stats_left}{unit}{stats_right}"
