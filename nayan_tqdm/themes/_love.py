"""love theme -- Hearts trail with cupid arrow.

A trail of colorful hearts fills the bar with love.

Rendering tiers:
- emoji: mixed heart emoji trail, cupid arrow sprite
- unicode: ANSI-colored heart symbols, "<3" sprite
- ascii: "<3" fill, "<3>" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
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
        "\u2764\ufe0f",   # red heart
        "\U0001f49b",      # yellow heart
        "\U0001f49a",      # green heart
        "\U0001f499",      # blue heart
        "\U0001f49c",      # purple heart
    )
    sprite_a = Frame(lines=("\U0001f498",))  # heart with arrow
    sprite_b = Frame(lines=("\U0001f496",))  # sparkling heart
    completion = Frame(lines=("\U0001f496\u2728",))  # sparkling heart + sparkles
    return Animation(
        name="love",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2665{_RST}",
        f"{_MAG}\u2665{_RST}",
        f"{_RED}\u2764{_RST}",
        f"{_MAG}\u2764{_RST}",
    )
    sprite_a = Frame(lines=("<3>",))
    sprite_b = Frame(lines=("<3>",))
    completion = Frame(lines=("<3>*",))
    return Animation(
        name="love",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("<", "3", " ")
    sprite_a = Frame(lines=("<3>",))
    sprite_b = Frame(lines=("<3>",))
    completion = Frame(lines=("<3>*",))
    return Animation(
        name="love",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("love", _create)
