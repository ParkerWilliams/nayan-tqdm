"""fire theme -- Dragon leaving a trail of flames.

A dragon blazes across the bar leaving fire in its wake.

Rendering tiers:
- emoji: fire emoji trail, dragon sprite, dragon + trophy completion
- unicode: "~" fill with red/yellow ANSI, "}>" sprite
- ascii: "~" fill, "}>" sprite
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
    fill = ("\U0001f525",)  # fire emoji trail
    sprite_a = Frame(lines=("\U0001f409",))  # dragon
    sprite_b = Frame(lines=("\U0001f409",))
    completion = Frame(lines=("\U0001f409\U0001f3c6",))  # dragon + trophy
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}~{_RST}",
        f"{_YEL}~{_RST}",
        f"{_RED}^{_RST}",
        f"{_YEL}~{_RST}",
    )
    sprite_a = Frame(lines=("}>",))
    sprite_b = Frame(lines=("}>",))
    completion = Frame(lines=("}>*",))
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~", "^", "~", "~")
    sprite_a = Frame(lines=("}>",))
    sprite_b = Frame(lines=("}>",))
    completion = Frame(lines=("}>*",))
    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("fire", _create)
