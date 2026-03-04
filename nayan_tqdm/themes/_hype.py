"""hype theme -- Excited arms-up face across the bar.

The \\(°o°)/ face hypes across the bar with arms raised.
At completion, maximum excitement with \\(°▽°)/.

Rendering tiers:
- emoji: Dark/light shade fill, degree-sign eyes
- unicode: Same
- ascii: Hash/dot fill, "\\(o_o)/" face
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
    fill = ("\u2593", "\u2591")   # ▓░
    sprites = (
        Frame(lines=("\\(\u00b0o\u00b0)/",)),    # \(°o°)/
        Frame(lines=("\\(\u00b0O\u00b0)/",)),    # \(°O°)/
    )
    completion = Frame(lines=("\\(\u00b0\u25bd\u00b0)/",))  # \(°▽°)/
    return Animation(
        name="hype",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2593", "\u2591")
    sprites = (
        Frame(lines=("\\(\u00b0o\u00b0)/",)),
        Frame(lines=("\\(\u00b0O\u00b0)/",)),
    )
    completion = Frame(lines=("\\(\u00b0\u25bd\u00b0)/",))
    return Animation(
        name="hype",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#", ".")
    sprites = (
        Frame(lines=("\\(o_o)/",)),
        Frame(lines=("\\(O_O)/",)),
    )
    completion = Frame(lines=("\\(^o^)/",))
    return Animation(
        name="hype",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("hype", _create)
