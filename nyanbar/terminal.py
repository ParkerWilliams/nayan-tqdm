"""Terminal capability detection for nyanbar.

Detects TTY status, color support tier, terminal width, and notebook
environments. Returns a frozen ``TerminalInfo`` dataclass.
"""
from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import IO, Optional

__all__ = ["ColorTier", "TerminalInfo", "detect_terminal"]


class ColorTier(IntEnum):
    """Terminal color support levels, ordered for comparison."""

    NONE = 0        # No color (piped, dumb, NO_COLOR)
    COLOR_16 = 1    # Basic ANSI 16 colors
    COLOR_256 = 2   # 256-color palette
    TRUE_COLOR = 3  # 24-bit true color


@dataclass(frozen=True, slots=True)
class TerminalInfo:
    """Immutable snapshot of terminal capabilities."""

    is_tty: bool
    color_support: ColorTier
    width: int
    is_notebook: bool


def _get_ipython_shell() -> object | None:
    """Return the current IPython shell instance, or *None*."""
    try:
        from IPython import get_ipython  # type: ignore[import-untyped]

        return get_ipython()
    except (ImportError, NameError):
        return None


def _detect_color(term: str, colorterm: str, no_color: bool) -> ColorTier:
    """Determine color tier from environment variables."""
    if no_color or term == "dumb":
        return ColorTier.NONE
    if colorterm in ("truecolor", "24bit"):
        return ColorTier.TRUE_COLOR
    if "256color" in term:
        return ColorTier.COLOR_256
    if term:
        return ColorTier.COLOR_16
    return ColorTier.NONE


def detect_terminal(stream: Optional[IO[str]] = None) -> TerminalInfo:
    """Detect terminal capabilities.

    Parameters
    ----------
    stream:
        The output stream to inspect.  Defaults to ``sys.stderr``
        (matching tqdm convention).

    Returns
    -------
    TerminalInfo
        Frozen dataclass with ``is_tty``, ``color_support``, ``width``,
        and ``is_notebook``.
    """
    if stream is None:
        stream = sys.stderr

    # TTY detection
    is_tty = hasattr(stream, "isatty") and stream.isatty()

    # Terminal width
    width = shutil.get_terminal_size(fallback=(80, 24)).columns if is_tty else 80

    # Color support — only meaningful for TTYs
    if is_tty:
        term = os.environ.get("TERM", "")
        colorterm = os.environ.get("COLORTERM", "")
        no_color = "NO_COLOR" in os.environ
        color_support = _detect_color(term, colorterm, no_color)
    else:
        color_support = ColorTier.NONE

    # Notebook detection
    shell = _get_ipython_shell()
    is_notebook = shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"

    return TerminalInfo(
        is_tty=is_tty,
        color_support=color_support,
        width=width,
        is_notebook=is_notebook,
    )
