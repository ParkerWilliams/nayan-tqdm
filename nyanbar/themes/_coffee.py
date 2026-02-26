"""coffee theme -- Coffee brewing, warm brown tones.

A cozy coffee-colored bar with warm brown and dark blocks, like watching
espresso brew. Simple and comforting, no decoration needed.

Note: U+2615 (hot beverage emoji) is 2 display cols; we use the
text-art sprite "c[_]" for a consistent single-column-per-char look.

Rendering tiers:
- emoji: Brown/dark ANSI blocks, coffee cup sprite, warm completion
- unicode: Same fill, "c[_]" sprite (4 cols), "c[_]*" completion
- ascii: "#" fill, "c[_]" sprite, "c[_]*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_BRN = "\033[33m"   # yellow/brown (espresso)
_DRK = "\033[90m"   # dark gray (espresso crema)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Coffee/espresso fill: brown and dark gray blocks for crema look
    fill = (
        f"{_BRN}\u2588{_RST}",   # brown full block
        f"{_DRK}\u2588{_RST}",   # dark gray full block
        f"{_BRN}\u2593{_RST}",   # brown dark shade
        f"{_DRK}\u2592{_RST}",   # dark gray medium shade
    )
    # Use text-art "c[_]" (4 cols) -- both frames identical for consistent width
    sprite_a = Frame(lines=("c[_]",))
    sprite_b = Frame(lines=("c[_]",))
    completion = Frame(lines=("c[_]\u2605",))   # coffee cup + star

    return Animation(
        name="coffee",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_BRN}\u2588{_RST}",
        f"{_DRK}\u2588{_RST}",
        f"{_BRN}\u2593{_RST}",
        f"{_DRK}\u2592{_RST}",
    )
    sprite_a = Frame(lines=("c[_]",))
    sprite_b = Frame(lines=("c[_]",))
    completion = Frame(lines=("c[_]*",))

    return Animation(
        name="coffee",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprite_a = Frame(lines=("c[_]",))
    sprite_b = Frame(lines=("c[_]",))
    completion = Frame(lines=("c[_]*",))

    return Animation(
        name="coffee",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("coffee", _create)
