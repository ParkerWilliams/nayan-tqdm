"""construction theme -- Bulldozer building a road.

A construction vehicle pushes along, leaving paved road behind it.
At completion, the building is done.

Rendering tiers:
- emoji: Yellow/gray paved-road fill, construction sign emoji, house emoji
- unicode: Yellow/gray ANSI block fill, bulldozer kaomoji, "[OK]" completion
- ascii: Alternating "=-" fill, "[=]" / "[-]" sprite, "[OK]" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_YEL = "\033[33m"
_GRAY = "\033[90m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Alternating yellow/gray blocks -- looks like paved road or laid bricks
    fill = (
        f"{_YEL}\u2588{_RST}",
        f"{_GRAY}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRAY}\u2588{_RST}",
    )
    # Construction sign emoji -- 2 display cols, consistent between frames
    sprite_a = Frame(lines=("\U0001f6a7",))
    sprite_b = Frame(lines=("\U0001f6a7",))
    # House emoji -- "building complete!"
    completion = Frame(lines=("\U0001f3e0",))
    return Animation(
        name="construction",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_YEL}\u2588{_RST}",
        f"{_GRAY}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRAY}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("[=]",))
    sprite_b = Frame(lines=("[-]",))
    completion = Frame(lines=("[OK]",))
    return Animation(
        name="construction",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("=", "-")
    sprite_a = Frame(lines=("[=]",))
    sprite_b = Frame(lines=("[-]",))
    completion = Frame(lines=("[OK]",))
    return Animation(
        name="construction",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("construction", _create)
