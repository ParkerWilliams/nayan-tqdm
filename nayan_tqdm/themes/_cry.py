"""cry theme -- Crying face turns happy at completion.

The (╥_╥) face sobs across the bar. At 100%, tears dry
and it becomes a happy (◕‿◕).

Rendering tiers:
- emoji: Light shade fill, box-drawing tears
- unicode: Same
- ascii: Tilde fill, "(T_T)" face
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
    fill = ("\u2591", "\u2592")   # ░▒
    sprites = (
        Frame(lines=("(\u2565_\u2565)",)),    # (╥_╥)
        Frame(lines=("(\u2565\u203f\u2565)",)),  # (╥‿╥)
    )
    completion = Frame(lines=("(\u25d5\u203f\u25d5)",))  # (◕‿◕)
    return Animation(
        name="cry",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2591", "\u2592")
    sprites = (
        Frame(lines=("(\u2565_\u2565)",)),
        Frame(lines=("(\u2565\u203f\u2565)",)),
    )
    completion = Frame(lines=("(\u25d5\u203f\u25d5)",))
    return Animation(
        name="cry",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", "~")
    sprites = (
        Frame(lines=("(T_T)",)),
        Frame(lines=("(T~T)",)),
    )
    completion = Frame(lines=("(^_^)",))
    return Animation(
        name="cry",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("cry", _create)
