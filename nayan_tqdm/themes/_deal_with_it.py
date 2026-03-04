"""deal_with_it theme -- Sunglasses drop at completion.

Plain block fill with a face sprite.  At 100%, sunglasses
drop into place for the classic meme.

Rendering tiers:
- emoji: Block fill, face, sunglasses
- unicode: Block fill, face, sunglasses
- ascii: Hash fill, face, sunglasses (ASCII)
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
        Frame(lines=("( \u2022_\u2022)",)),
        Frame(lines=("( \u2022_\u2022)",)),
    )
    completion = Frame(lines=("(\u2310\u25a0_\u25a0)",))
    return Animation(
        name="deal_with_it",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2588",)
    sprites = (
        Frame(lines=("( \u2022_\u2022)",)),
        Frame(lines=("( \u2022_\u2022)",)),
    )
    completion = Frame(lines=("(\u2310\u25a0_\u25a0)",))
    return Animation(
        name="deal_with_it",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprites = (
        Frame(lines=("( o_o)",)),
        Frame(lines=("( o_o)",)),
    )
    completion = Frame(lines=("( B_B)",))
    return Animation(
        name="deal_with_it",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("deal_with_it", _create)
