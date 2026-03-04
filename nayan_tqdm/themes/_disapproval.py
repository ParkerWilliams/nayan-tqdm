"""disapproval theme -- Look of disapproval turns to approval.

The iconic ಠ_ಠ face walks across the bar, alternating between
disapproval and neutral. At completion, it softens to approval.

Rendering tiers:
- emoji: Gradient block fill, Kannada-letter eyes
- unicode: Same
- ascii: Gradient fill, "o_o" / "O_O" ASCII faces
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
    sprites = (
        Frame(lines=("\u0ca0_\u0ca0",)),    # ಠ_ಠ
        Frame(lines=("\u0ca0\u203f\u0ca0",)),  # ಠ‿ಠ
    )
    completion = Frame(lines=("\u0ca0\u203f\u0ca0",))  # ಠ‿ಠ
    return Animation(
        name="disapproval",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2591", "\u2592", "\u2593", "\u2588")
    sprites = (
        Frame(lines=("\u0ca0_\u0ca0",)),
        Frame(lines=("\u0ca0\u203f\u0ca0",)),
    )
    completion = Frame(lines=("\u0ca0\u203f\u0ca0",))
    return Animation(
        name="disapproval",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", ":", "|", "#")
    sprites = (
        Frame(lines=("o_o",)),
        Frame(lines=("O_O",)),
    )
    completion = Frame(lines=("^_^",))
    return Animation(
        name="disapproval",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("disapproval", _create)
