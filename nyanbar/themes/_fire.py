"""fire theme -- Fire spreading across the progress bar.

Fire emoji blazes across red/orange ANSI-colored blocks.
At completion, sparkles celebrate the inferno.

Rendering tiers:
- emoji: Red/orange ANSI blocks, fire emoji, fire + sparkles
- unicode: Red/orange ANSI blocks, fire kaomoji, fire + sparkles
- ascii: "#" fill, "^" sprite, "^*^" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
_YEL = "\033[33m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2593{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f525",))    # fire emoji
    sprite_b = Frame(lines=("\U0001f525",))
    completion = Frame(lines=("\U0001f525\u2728",))   # fire + sparkles
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2593{_RST}",
    )
    sprite_a = Frame(lines=("^v^",))
    sprite_b = Frame(lines=("/v\\",))
    completion = Frame(lines=("^v^\u2728",))
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprite_a = Frame(lines=("^",))
    sprite_b = Frame(lines=("^",))
    completion = Frame(lines=("^*^",))
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("fire", _create)
