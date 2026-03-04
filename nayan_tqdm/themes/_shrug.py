"""shrug theme -- Medium shade fill with shrug kaomoji.

The progress bar fills with medium shade blocks and the shrug
kaomoji walks at the leading edge.  Same sprite at completion.

Rendering tiers:
- emoji: Medium shade blocks, shrug kaomoji
- unicode: Medium shade blocks, shrug kaomoji
- ascii: Hash fill, shrug ASCII approximation
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
    fill = ("\u2593",)  # medium shade
    sprite = Frame(lines=("\u00af\\_(\u30c4)_/\u00af",))
    return Animation(
        name="shrug",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=sprite,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2593",)
    sprite = Frame(lines=("\u00af\\_(\u30c4)_/\u00af",))
    return Animation(
        name="shrug",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=sprite,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprite = Frame(lines=("shrug",))
    completion = Frame(lines=("shrug",))
    return Animation(
        name="shrug",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("shrug", _create)
