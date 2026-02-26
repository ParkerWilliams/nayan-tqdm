"""Stats formatting utilities for nyanbar.

Provides EMA rate tracking, SI suffix formatting, time interval formatting,
and tqdm-compatible meter string building.  All functions are pure/stateless
except the EMA class which maintains smoothed state.
"""
from __future__ import annotations

from .utils import disp_len

__all__ = ["EMA", "si_format", "format_interval", "format_meter"]


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

    def _fmt_count(v: int) -> str:
        return si_format(float(v)) if unit_scale else str(v)

    def _fmt_rate(r: float | None) -> str:
        if r is None:
            return f"?{unit}/s"
        if unit_scale:
            return f"{si_format(r)}{unit}/s"
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
            eta_str = format_interval((total - n) / rate)
        else:
            eta_str = "?"
        elapsed_str = format_interval(elapsed)
        time_stats = f" [{elapsed_str}<{eta_str}, {rate_str}]"
        count_str = f" {n_str}/{total_str}"

        # Build the bar portion
        pct_str = f"{pct:3.0f}%"
        # Calculate remaining space for the bar
        fixed_parts = f"{desc_prefix}{pct_str}||{count_str}{time_stats}{postfix_suffix}"
        fixed_len = disp_len(fixed_parts)
        bar_width = max(ncols - fixed_len, 10)
        filled = int(bar_width * pct / 100)
        bar = "#" * filled + " " * (bar_width - filled)
        return f"{desc_prefix}{pct_str}|{bar}|{count_str}{time_stats}{postfix_suffix}"
    else:
        # Indeterminate mode
        elapsed_str = format_interval(elapsed)
        rate_str = _fmt_rate(rate)
        return f"{desc_prefix}{n_str}{unit} [{elapsed_str}, {rate_str}]{postfix_suffix}"
