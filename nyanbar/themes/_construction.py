"""construction theme -- Under construction with hazard pattern fill.

A construction sign walks across a yellow/black hazard pattern.
At completion, a check mark signals the work is done.

Rendering tiers:
- emoji: Yellow/black ANSI hazard fill, construction emoji, check mark emoji
- unicode: Yellow/black ANSI hazard fill, hard hat kaomoji, check mark
- ascii: "#-" fill, "!" sprite, "[OK]" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_YEL = "\033[33m"
_BLK = "\033[30m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Hazard pattern: alternating yellow and dark blocks
    fill = (
        f"{_YEL}\u2588{_RST}",
        f"{_BLK}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_BLK}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f6a7",))     # construction sign emoji
    sprite_b = Frame(lines=("\U0001f6a7",))
    completion = Frame(lines=("\u2714",))        # check mark
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
        f"{_BLK}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_BLK}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("[!]",))
    sprite_b = Frame(lines=("[!]",))
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
    fill = ("#", "-")
    sprite_a = Frame(lines=("!",))
    sprite_b = Frame(lines=("!",))
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
