"""pac_man theme -- Pac-Man eating dots with text-art wedge sprite.

A yellow text-art wedge alternates open/closed as it moves across a
trail of pellet dots.  At completion, the ghost appears.

Rendering tiers:
- emoji: Middle dot fill, yellow ANSI "<" / "-" wedge sprite, ghost emoji
- unicode: Middle dot fill, "<" / "-" sprite, ghost kaomoji
- ascii: Dot fill, "<" / "-" sprite, "O" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

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
    fill = ("\u00b7",)  # middle dot pellet -- 1 display col
    # Yellow ANSI text-art wedge: "<" is open mouth, "-" is closed
    # Both are 1 display col, consistent frame widths
    sprite_open = Frame(lines=(f"{_YEL}<{_RST}",))
    sprite_closed = Frame(lines=(f"{_YEL}-{_RST}",))
    # Ghost emoji at completion -- 2 display cols, rendered separately at 100%
    completion = Frame(lines=("\U0001f47b",))
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u00b7",)  # middle dot
    sprite_open = Frame(lines=("<",))
    sprite_closed = Frame(lines=("-",))
    completion = Frame(lines=("(^o^)",))
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".",)
    sprite_open = Frame(lines=("<",))
    sprite_closed = Frame(lines=("-",))
    completion = Frame(lines=("O",))
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("pac_man", _create)
