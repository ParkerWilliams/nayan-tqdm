"""snake theme -- Snake slithering across a green fill.

A snake emoji slithers across green-colored blocks.
At completion, the snake finds its apple.

Rendering tiers:
- emoji: Green ANSI blocks, snake emoji, snake + apple
- unicode: Green ANSI blocks, snake kaomoji, snake + apple
- ascii: "=" fill, "~>" sprite, "~>@" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_GRN = "\033[32m"
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
        f"{_GRN}\u2588{_RST}",
        f"{_GRN}\u2593{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f40d",))    # snake emoji
    sprite_b = Frame(lines=("\U0001f40d",))    # snake emoji
    completion = Frame(lines=("\U0001f40d\U0001f34e",))   # snake + apple
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_GRN}\u2588{_RST}",
        f"{_GRN}\u2593{_RST}",
    )
    sprite_a = Frame(lines=("~>",))
    sprite_b = Frame(lines=("=>",))
    completion = Frame(lines=("~>@",))
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("=",)
    sprite_a = Frame(lines=("~>",))
    sprite_b = Frame(lines=("=>",))
    completion = Frame(lines=("~>@",))
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("snake", _create)
