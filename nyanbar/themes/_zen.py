"""zen theme -- Calm meditation with light shade fill.

A lotus sprite meditates across light shade blocks.
At completion, a sparkle appears for inner peace.

Rendering tiers:
- emoji: Light shade blocks, lotus emoji, lotus + sparkle
- unicode: Light shade blocks, lotus kaomoji, lotus + sparkle
- ascii: "." fill, "@" sprite, "@*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = ("\u2591",)   # light shade
    sprite_a = Frame(lines=("\U0001fab7",))      # lotus emoji
    sprite_b = Frame(lines=("\U0001fab7",))
    completion = Frame(lines=("\U0001fab7\u2728",))   # lotus + sparkles
    return Animation(
        name="zen",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2591",)
    sprite_a = Frame(lines=("~o~",))
    sprite_b = Frame(lines=("-o-",))
    completion = Frame(lines=("~o~*",))
    return Animation(
        name="zen",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".",)
    sprite_a = Frame(lines=("@",))
    sprite_b = Frame(lines=("@",))
    completion = Frame(lines=("@*",))
    return Animation(
        name="zen",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("zen", _create)
