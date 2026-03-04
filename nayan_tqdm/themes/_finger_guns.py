"""finger_guns theme -- Sparkle fill with finger-gun kaomoji.

The progress bar fills with sparkle characters and a finger-gun
kaomoji walks at the leading edge.

Rendering tiers:
- emoji: Sparkle chars, finger guns with fullwidth chars
- unicode: Sparkle chars, finger guns
- ascii: Dot fill, pointing hand ASCII art
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
    fill = ("\u2727", "\u2726", "\u2727", "\u2606")
    sprite = Frame(lines=("(\u261e\uff9f\u2200\uff9f)\u261e",))
    completion = Frame(lines=("(\u261e\uff9f\u2200\uff9f)\u261e \u2605",))
    return Animation(
        name="finger_guns",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2727", "\u2726", "\u2727", "\u2606")
    sprite = Frame(lines=("(\u261e\uff9f\u2200\uff9f)\u261e",))
    completion = Frame(lines=("(\u261e\uff9f\u2200\uff9f)\u261e *",))
    return Animation(
        name="finger_guns",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".", "*", ".", "+")
    sprite = Frame(lines=("(>-)>",))
    completion = Frame(lines=("(>-)> *",))
    return Animation(
        name="finger_guns",
        frames=(sprite, sprite),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("finger_guns", _create)
