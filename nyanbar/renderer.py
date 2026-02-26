"""ANSI escape sequence renderer for nyanbar.

Produces cursor-movement and line-erase sequences to draw animation
frames in the terminal.  All functions are pure/stateless -- they take
a stream and data, produce output, and return state for the next call.
"""
from __future__ import annotations

import re
from typing import IO, Sequence

__all__ = [
    "CURSOR_UP",
    "ERASE_LINE",
    "RESET",
    "CR",
    "erase_lines",
    "render_frame",
    "ensure_reset",
    "has_unclosed_ansi",
]

# ── ANSI constants ──────────────────────────────────────────

CURSOR_UP = "\033[{n}A"   # Move cursor up *n* lines
ERASE_LINE = "\033[2K"    # Erase entire current line
RESET = "\033[0m"         # Reset all SGR attributes
CR = "\r"                 # Carriage return

# Matches any SGR sequence (colors, bold, reset, etc.)
_SGR_RE = re.compile(r"\033\[[0-9;]*m")


# ── Public API ──────────────────────────────────────────────


def erase_lines(stream: IO[str], count: int) -> None:
    """Erase *count* previously rendered lines above the cursor.

    Does nothing when *count* is zero or negative.
    """
    if count <= 0:
        return
    # Move cursor to the top of the previous frame
    stream.write(CURSOR_UP.format(n=count))
    # Clear each line
    for i in range(count):
        stream.write(ERASE_LINE)
        if i < count - 1:
            stream.write("\n")
    # Return cursor to the start of the first cleared line
    if count > 1:
        stream.write(CURSOR_UP.format(n=count - 1))
    stream.write(CR)


def render_frame(
    lines: Sequence[str],
    prev_height: int,
    stream: IO[str],
) -> int:
    """Render *lines* to *stream*, erasing the previous frame first.

    Parameters
    ----------
    lines:
        Lines to render (one per row).
    prev_height:
        Number of lines in the previous frame (0 on first render).
    stream:
        Output stream (e.g. ``sys.stderr``).

    Returns
    -------
    int
        The height (line count) of the frame just rendered, to be
        passed as *prev_height* on the next call.
    """
    if prev_height > 0:
        erase_lines(stream, prev_height)

    for line in lines:
        stream.write(ensure_reset(line) + "\n")
    stream.flush()
    return len(lines)


def ensure_reset(line: str) -> str:
    """Append ``RESET`` if *line* contains ANSI SGR codes but doesn't
    already end with a reset sequence.

    Plain-text lines are returned unchanged.
    """
    if not line:
        return line
    if not _SGR_RE.search(line):
        return line
    if line.endswith(RESET):
        return line
    return line + RESET


def has_unclosed_ansi(text: str) -> bool:
    """Return ``True`` if *text* contains SGR colour opens without a
    matching ``\\033[0m`` reset at the end.

    Useful for verification/testing, not in the hot path.
    """
    if not text:
        return False

    matches = list(_SGR_RE.finditer(text))
    if not matches:
        return False

    # Track open/closed state: any non-reset SGR opens, \033[0m closes
    is_open = False
    for m in matches:
        seq = m.group()
        if seq == RESET:
            is_open = False
        else:
            is_open = True
    return is_open
