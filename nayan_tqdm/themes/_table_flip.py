"""table_flip theme -- Angry face flips the table at completion.

Plain block fill with an increasingly angry kaomoji sprite.
At 100%, the sprite becomes the iconic table flip.

Rendering tiers:
- emoji: Block fill, angry face, table flip with emoji table
- unicode: Block fill, angry face, table flip
- ascii: Hash fill, angry face, table flip (ASCII-safe)
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
    fill = ("\u2588",)
    sprites = (
        Frame(lines=("(\u00b0\u25a1\u00b0)",)),   # (°□°)
        Frame(lines=("(\u00b0_\u00b0)",)),         # (°_°)
    )
    completion = Frame(lines=(
        "(\u256f\u00b0\u25a1\u00b0)\u256f\ufe35 \u253b\u2501\u253b",
    ))
    return Animation(
        name="table_flip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2588",)
    sprites = (
        Frame(lines=("(\u00b0\u25a1\u00b0)",)),
        Frame(lines=("(\u00b0_\u00b0)",)),
    )
    completion = Frame(lines=(
        "(\u256f\u00b0\u25a1\u00b0)\u256f\ufe35 \u253b\u2501\u253b",
    ))
    return Animation(
        name="table_flip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprites = (
        Frame(lines=("(o_o)",)),
        Frame(lines=("(O_O)",)),
    )
    completion = Frame(lines=("(>_<)/ ~|__|",))
    return Animation(
        name="table_flip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("table_flip", _create)
