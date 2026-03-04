"""lenny theme -- Gradient fill with Lenny face.

The progress bar fills with a 4-char gradient pattern
and a Lenny face walks at the leading edge.  At completion,
Lenny winks.

Rendering tiers:
- emoji: Gradient blocks, Lenny face
- unicode: Gradient blocks, Lenny face
- ascii: Gradient chars, Lenny ASCII approximation
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
    fill = ("\u2591", "\u2592", "\u2593", "\u2588")
    sprite = Frame(lines=("( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",))
    completion = Frame(lines=("( \u0361~ \u035c\u0296 \u0361\u00b0)",))
    return Animation(
        name="lenny",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2591", "\u2592", "\u2593", "\u2588")
    sprite = Frame(lines=("( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",))
    completion = Frame(lines=("( \u0361~ \u035c\u0296 \u0361\u00b0)",))
    return Animation(
        name="lenny",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", ":", "|", "#")
    sprite = Frame(lines=("(o_o)",))
    completion = Frame(lines=("(~_o)",))
    return Animation(
        name="lenny",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("lenny", _create)
