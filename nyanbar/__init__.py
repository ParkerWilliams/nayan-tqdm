"""nyanbar - Animated progress bars for Python.

Drop-in replacement for tqdm with animated themes.
"""
from __future__ import annotations

from typing import Any

from .core import NyanBar
from .core import NyanBar as tqdm
from .models import Animation, AnimationMode, Frame
from .registry import set_theme, list_themes, get_theme

__all__ = [
    "NyanBar",
    "tqdm",
    "trange",
    "Animation",
    "AnimationMode",
    "Frame",
    "set_theme",
    "list_themes",
    "get_theme",
]


def trange(n: int, **kwargs: Any) -> NyanBar:
    """Shorthand for ``NyanBar(range(n), ...)``."""
    return NyanBar(range(n), **kwargs)
