"""candy theme -- Colorful candy trail.

A candy emoji leaves a trail of colorful candy-colored shapes.
Simple and sweet, no decoration needed.

Rendering tiers:
- emoji: Pink/cyan/yellow/green ANSI candy symbols, candy emoji
- unicode: Same fill, "(o)" / "{o}" sprites
- ascii: "o" "." "*" fill, "(o)" sprite
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_PNK = "\033[35m"   # pink (magenta)
_CYN = "\033[36m"   # cyan
_YEL = "\033[33m"   # yellow
_GRN = "\033[32m"   # green
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Candy fill: colorful bullet, diamond, circle in candy colors
    # All are reliably 1 display col
    fill = (
        f"{_PNK}\u2022{_RST}",   # pink bullet
        f"{_CYN}\u2666{_RST}",   # cyan diamond
        f"{_YEL}\u25cf{_RST}",   # yellow circle
        f"{_GRN}\u2022{_RST}",   # green bullet
        f"{_PNK}\u2666{_RST}",   # pink diamond
        f"{_CYN}\u25cf{_RST}",   # cyan circle
    )
    # Candy emoji is 2 cols; both frames identical
    sprite_a = Frame(lines=("\U0001f36c",))    # candy (2 cols)
    sprite_b = Frame(lines=("\U0001f36c",))
    completion = Frame(lines=("\U0001f36c\u2605",))   # candy + star

    return Animation(
        name="candy",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_PNK}\u2022{_RST}",
        f"{_CYN}\u2666{_RST}",
        f"{_YEL}\u25cf{_RST}",
        f"{_GRN}\u2022{_RST}",
        f"{_PNK}\u2666{_RST}",
        f"{_CYN}\u25cf{_RST}",
    )
    sprite_a = Frame(lines=("(o)",))
    sprite_b = Frame(lines=("{o}",))
    completion = Frame(lines=("(o)!",))

    return Animation(
        name="candy",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("o", ".", "*", "o", ".", "*")
    sprite_a = Frame(lines=("(o)",))
    sprite_b = Frame(lines=("(o)",))
    completion = Frame(lines=("(o)!",))

    return Animation(
        name="candy",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("candy", _create)
