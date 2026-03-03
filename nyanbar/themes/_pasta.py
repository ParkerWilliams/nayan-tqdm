"""pasta theme -- Spaghetti trail with chef sprite.

A chef leaves a trail of spaghetti across the bar.

Rendering tiers:
- emoji: spaghetti trail, chef sprite, chef + OK completion
- unicode: "~" fill, "d>" sprite
- ascii: "~" fill, "d>" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = ("\U0001f35d",)  # spaghetti trail
    sprite_a = Frame(lines=("\U0001f468\u200d\U0001f373",))  # chef
    sprite_b = Frame(lines=("\U0001f468\u200d\U0001f373",))
    completion = Frame(lines=("\U0001f468\u200d\U0001f373\U0001f44c",))  # chef + OK
    return Animation(
        name="pasta",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("~",)
    sprite_a = Frame(lines=("d>",))
    sprite_b = Frame(lines=("d>",))
    completion = Frame(lines=("d>*",))
    return Animation(
        name="pasta",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~",)
    sprite_a = Frame(lines=("d>",))
    sprite_b = Frame(lines=("d>",))
    completion = Frame(lines=("d>*",))
    return Animation(
        name="pasta",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("pasta", _create)
