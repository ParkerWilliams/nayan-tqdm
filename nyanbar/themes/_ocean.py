"""ocean theme -- Wave surfing across a blue/cyan gradient fill.

A wave emoji surfs across blue/cyan ANSI-colored blocks.
At completion, the sun comes out.

Rendering tiers:
- emoji: Blue/cyan ANSI blocks, wave emoji, sun emoji
- unicode: Blue/cyan ANSI blocks, wave kaomoji, sun kaomoji
- ascii: "~" fill, "~^~" sprite, "\\o/" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_BLU = "\033[34m"
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
        f"{_BLU}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2593{_RST}",
        f"{_CYN}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f30a",))    # wave emoji
    sprite_b = Frame(lines=("\U0001f30a",))
    completion = Frame(lines=("\u2600",))      # sun emoji
    return Animation(
        name="ocean",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_BLU}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2593{_RST}",
        f"{_CYN}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("~^~",))
    sprite_b = Frame(lines=("~v~",))
    completion = Frame(lines=("\\o/",))
    return Animation(
        name="ocean",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~",)
    sprite_a = Frame(lines=("~^~",))
    sprite_b = Frame(lines=("~v~",))
    completion = Frame(lines=("\\o/",))
    return Animation(
        name="ocean",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("ocean", _create)
