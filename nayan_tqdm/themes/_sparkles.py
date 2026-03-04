"""sparkles theme -- Throwing sparkles across the bar.

The (ﾉ◕ヮ◕)ﾉ face joyfully flings sparkles as it walks.

Rendering tiers:
- emoji: Sparkle char fill, halfwidth-katakana face
- unicode: Same
- ascii: Dot/star fill, "(n>w<)n" face
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
    fill = ("\u2727", "\u2726", "\u2727", "\u22c6")   # ✧✦✧⋆
    sprites = (
        Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89",)),   # (ﾉ◕ヮ◕)ﾉ
        Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89",)),
    )
    completion = Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89\u2727",))  # +✧
    return Animation(
        name="sparkles",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2727", "\u2726", "\u2727", "\u22c6")
    sprites = (
        Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89",)),
        Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89",)),
    )
    completion = Frame(lines=("(\uff89\u25d5\u30ee\u25d5)\uff89*",))
    return Animation(
        name="sparkles",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", "*", ".", "+")
    sprites = (
        Frame(lines=("(n>w<)n",)),
        Frame(lines=("(n>w<)n",)),
    )
    completion = Frame(lines=("(n>w<)n *",))
    return Animation(
        name="sparkles",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("sparkles", _create)
