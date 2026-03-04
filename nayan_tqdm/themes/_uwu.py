"""uwu theme -- Cute uwu face across the bar.

The (◕ᴗ◕) face walks cutely. At completion, a flower appears.

Rendering tiers:
- emoji: Heart/circle fill, filled-circle eyes
- unicode: Same
- ascii: Dot/o fill, "(owo)" face
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
    fill = ("\u2661", "\u25e6")   # ♡◦
    sprites = (
        Frame(lines=("(\u25d5\u1d17\u25d5)",)),    # (◕ᴗ◕)
        Frame(lines=("(\u25d5\u203f\u25d5)",)),    # (◕‿◕)
    )
    completion = Frame(lines=("(\u25d5\u1d17\u25d5\u273f)",))  # (◕ᴗ◕✿)
    return Animation(
        name="uwu",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2661", "\u25e6")
    sprites = (
        Frame(lines=("(\u25d5\u1d17\u25d5)",)),
        Frame(lines=("(\u25d5\u203f\u25d5)",)),
    )
    completion = Frame(lines=("(\u25d5\u1d17\u25d5*)",))
    return Animation(
        name="uwu",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", "o")
    sprites = (
        Frame(lines=("(owo)",)),
        Frame(lines=("(uwu)",)),
    )
    completion = Frame(lines=("(uwu)~",))
    return Animation(
        name="uwu",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("uwu", _create)
