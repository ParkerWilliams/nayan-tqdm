"""rage theme -- Angry rage face across the bar.

The (╬°□°) face rages across the bar. At completion, it
flips out with a dramatic arm raise.

Rendering tiers:
- emoji: Dark shade/block fill, box-drawing anger vein
- unicode: Same
- ascii: Hash/equals fill, "(>_<)" face
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
    fill = ("\u2593", "\u2588")   # ▓█
    sprites = (
        Frame(lines=("(\u256c\u00b0\u25a1\u00b0)",)),    # (╬°□°)
        Frame(lines=("(\u256c\u00b0\u0414\u00b0)",)),    # (╬°Д°)
    )
    completion = Frame(lines=("(\u256c\u00b0\u25a1\u00b0)\u256f",))  # (╬°□°)╯
    return Animation(
        name="rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2593", "\u2588")
    sprites = (
        Frame(lines=("(\u256c\u00b0\u25a1\u00b0)",)),
        Frame(lines=("(\u256c\u00b0\u0414\u00b0)",)),
    )
    completion = Frame(lines=("(\u256c\u00b0\u25a1\u00b0)\u256f",))
    return Animation(
        name="rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#", "=")
    sprites = (
        Frame(lines=("(>_<)",)),
        Frame(lines=("(>o<)",)),
    )
    completion = Frame(lines=("(>_<)!",))
    return Animation(
        name="rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("rage", _create)
