"""nyanbar - Animated progress bars for Python.

Drop-in replacement for tqdm with animated themes.
"""
from __future__ import annotations

from .core import NyanBar
from .core import NyanBar as tqdm
from .models import Animation, AnimationMode, Frame

__all__ = [
    "NyanBar",
    "tqdm",
    "trange",
    "Animation",
    "AnimationMode",
    "Frame",
]


def trange(n: int, *args: object, **kwargs: object) -> NyanBar:
    """Shorthand for ``NyanBar(range(n), ...)``."""
    return NyanBar(range(n), *args, **kwargs)
