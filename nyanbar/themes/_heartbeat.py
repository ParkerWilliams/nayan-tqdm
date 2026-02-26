"""heartbeat theme -- Heart pulse with pink fill.

A heart alternates between sizes as it pulses across pink ANSI blocks.
At completion, a sparkling heart appears.

Rendering tiers:
- emoji: Pink ANSI blocks, heart emoji, sparkling heart
- unicode: Pink ANSI blocks, heart kaomoji, heart + "!"
- ascii: "~" fill, "<3" sprite, "<3!" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

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
        f"{_MAG}\u2588{_RST}",
        f"{_MAG}\u2593{_RST}",
        f"{_MAG}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("\u2764",))       # heart
    sprite_b = Frame(lines=("\u2764",))       # heart
    completion = Frame(lines=("\U0001f496",))  # sparkling heart
    return Animation(
        name="heartbeat",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u2588{_RST}",
        f"{_MAG}\u2593{_RST}",
        f"{_MAG}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("\u2764",))
    sprite_b = Frame(lines=("\u2665",))
    completion = Frame(lines=("\u2764!",))
    return Animation(
        name="heartbeat",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("~",)
    sprite_a = Frame(lines=("<3",))
    sprite_b = Frame(lines=("<3",))
    completion = Frame(lines=("<3!",))
    return Animation(
        name="heartbeat",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("heartbeat", _create)
