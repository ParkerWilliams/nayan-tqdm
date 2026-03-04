"""bee theme -- Bee pollinating a trail of flowers.

A bee buzzes across a meadow of flowers.

Rendering tiers:
- emoji: mixed flower emoji trail, bee sprite, bee + honey completion
- unicode: ANSI-colored flower chars, "z>" sprite
- ascii: "*" fill, "z>" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_YEL = "\033[33m"
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
        "\U0001f33b",  # sunflower
        "\U0001f338",  # cherry blossom
        "\U0001f33c",  # blossom
        "\U0001f337",  # tulip
        "\U0001f33a",  # hibiscus
    )
    sprite_a = Frame(lines=("\U0001f41d",))  # bee
    sprite_b = Frame(lines=("\U0001f41d",))
    completion = Frame(lines=("\U0001f41d\U0001f36f",))  # bee + honey pot
    return Animation(
        name="bee",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_YEL}*{_RST}",
        f"{_GRN}*{_RST}",
        f"{_YEL}\u273f{_RST}",
        f"{_GRN}\u2740{_RST}",
    )
    sprite_a = Frame(lines=("z>",))
    sprite_b = Frame(lines=("z>",))
    completion = Frame(lines=("z>*",))
    return Animation(
        name="bee",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("*", ".", "*", ".")
    sprite_a = Frame(lines=("z>",))
    sprite_b = Frame(lines=("z>",))
    completion = Frame(lines=("z>*",))
    return Animation(
        name="bee",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("bee", _create)
