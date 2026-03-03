"""snake theme -- Snake growing across the bar.

A snake head leads a growing body of green segments.

Rendering tiers:
- emoji: green square trail, snake head sprite
- unicode: ANSI green blocks, "~S" sprite
- ascii: "o" fill, "~S" sprite
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
        "\U0001f7e9",  # green square
        "\U0001f7e9",
    )
    sprite_a = Frame(lines=("\U0001f40d",))  # snake
    sprite_b = Frame(lines=("\U0001f40d",))
    completion = Frame(lines=("\U0001f40d\U0001f34e",))  # snake + apple
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_GRN}\u2588{_RST}",
        f"{_GRN}\u2593{_RST}",
    )
    sprite_a = Frame(lines=("~S",))
    sprite_b = Frame(lines=("~S",))
    completion = Frame(lines=("~S@",))
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("o", "o")
    sprite_a = Frame(lines=("~S",))
    sprite_b = Frame(lines=("~S",))
    completion = Frame(lines=("~S@",))
    return Animation(
        name="snake",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("snake", _create)
