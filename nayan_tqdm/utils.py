"""Display width measurement and ANSI escape sequence utilities.

Zero-dependency utilities for terminal-accurate string width calculation
and ANSI escape sequence handling.
"""
from __future__ import annotations

import re
import unicodedata

__all__ = ["disp_len", "strip_ansi"]

# Matches all ANSI escape sequences: SGR (colors), cursor movement, erase, etc.
_ANSI_RE = re.compile(r"\033\[[0-9;]*[a-zA-Z]")


def strip_ansi(text: str) -> str:
    """Remove all ANSI escape sequences from *text*, returning plain text."""
    return _ANSI_RE.sub("", text)


def disp_len(text: str) -> int:
    """Return the terminal display width of *text* in columns.

    - East Asian Wide (W) and Fullwidth (F) characters count as 2 columns.
    - Combining diacritical marks count as 0 columns.
    - ANSI escape sequences count as 0 columns.
    - All other characters count as 1 column.

    The string is NFC-normalized before measurement so that precomposed
    forms (e.g. ``e\\u0301`` → ``\\u00e9``) are handled consistently.
    """
    # Strip ANSI sequences first — they occupy zero display columns
    text = strip_ansi(text)
    # NFC normalize to collapse base + combining where possible
    text = unicodedata.normalize("NFC", text)

    width = 0
    for char in text:
        # Combining characters occupy zero columns
        if unicodedata.combining(char):
            continue
        eaw = unicodedata.east_asian_width(char)
        width += 2 if eaw in ("W", "F") else 1
    return width
