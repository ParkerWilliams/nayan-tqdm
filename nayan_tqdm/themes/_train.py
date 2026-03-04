"""train theme -- Locomotive pulling a trail of train cars.

A steam locomotive chugs along with train cars behind it.

Rendering tiers:
- emoji: train car emoji trail, locomotive sprite
- unicode: ANSI blocks, "[=" sprite
- ascii: "=" fill, "[=" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = ("\U0001f683",)  # railway car
    sprite_a = Frame(lines=("\U0001f682",))  # locomotive
    sprite_b = Frame(lines=("\U0001f682",))
    completion = Frame(lines=("\U0001f682\U0001f389",))  # locomotive + party
    return Animation(
        name="train",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2588{_RST}",
        "\u2593",
    )
    sprite_a = Frame(lines=("[=",))
    sprite_b = Frame(lines=("[=",))
    completion = Frame(lines=("[=*",))
    return Animation(
        name="train",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("=",)
    sprite_a = Frame(lines=("[=",))
    sprite_b = Frame(lines=("[=",))
    completion = Frame(lines=("[=*",))
    return Animation(
        name="train",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("train", _create)
