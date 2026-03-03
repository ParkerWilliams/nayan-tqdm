"""music theme -- Musical notes trail with guitar sprite.

A guitar rocks across a trail of musical notes.

Rendering tiers:
- emoji: music note emoji trail, guitar sprite, guitar + fire completion
- unicode: ANSI note symbols, ">>" sprite
- ascii: "~" fill, ">>" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_CYN = "\033[36m"
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
        "\U0001f3b5",  # musical note
        "\U0001f3b6",  # musical notes
    )
    sprite_a = Frame(lines=("\U0001f3b8",))  # guitar
    sprite_b = Frame(lines=("\U0001f3b8",))
    completion = Frame(lines=("\U0001f3b8\U0001f525",))  # guitar + fire
    return Animation(
        name="music",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u266a{_RST}",
        f"{_CYN}\u266b{_RST}",
    )
    sprite_a = Frame(lines=(">>",))
    sprite_b = Frame(lines=(">>",))
    completion = Frame(lines=(">>*",))
    return Animation(
        name="music",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~", ".", "~")
    sprite_a = Frame(lines=(">>",))
    sprite_b = Frame(lines=(">>",))
    completion = Frame(lines=(">>*",))
    return Animation(
        name="music",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("music", _create)
