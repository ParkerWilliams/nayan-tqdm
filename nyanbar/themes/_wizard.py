"""wizard theme -- Magic wizard with purple sparkle fill.

A wizard emoji casts spells across purple ANSI sparkle blocks.
At completion, the wizard's star shines.

Rendering tiers:
- emoji: Purple ANSI fill, wizard emoji, wizard + star
- unicode: Purple ANSI fill, wizard kaomoji, wizard + star
- ascii: "~" fill, "*>" sprite, "*>*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
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
        f"{_MAG}\u2588{_RST}",
        f"{_MAG}\u2592{_RST}",
        f"{_MAG}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f9d9",))      # wizard emoji
    sprite_b = Frame(lines=("\U0001f9d9",))
    completion = Frame(lines=("\U0001f9d9\u2605",))   # wizard + star
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u2588{_RST}",
        f"{_MAG}\u2592{_RST}",
        f"{_MAG}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~",)
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("wizard", _create)
