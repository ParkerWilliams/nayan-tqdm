"""run theme -- Running person across the bar.

Box-drawing arms alternate to give a running motion.
At completion, switches to the happy running guy ᕕ( ᐛ )ᕗ.

Rendering tiers:
- emoji: Equals/double-line fill, box-drawing runner
- unicode: Same
- ascii: Dash/equals fill, "/(>_<)\\" runner
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
    fill = ("=", "\u2550")   # = ═
    sprites = (
        Frame(lines=("\u250c(>_<)\u2518",)),   # ┌(>_<)┘
        Frame(lines=("\u2514(>_<)\u2510",)),   # └(>_<)┐
    )
    completion = Frame(lines=("\u1555( \u141b )\u1557",))  # ᕕ( ᐛ )ᕗ
    return Animation(
        name="run",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("=", "\u2550")
    sprites = (
        Frame(lines=("\u250c(>_<)\u2518",)),
        Frame(lines=("\u2514(>_<)\u2510",)),
    )
    completion = Frame(lines=("\u1555( \u141b )\u1557",))
    return Animation(
        name="run",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("=", "-")
    sprites = (
        Frame(lines=("/(>_<)\\",)),
        Frame(lines=("\\(>_<)/",)),
    )
    completion = Frame(lines=(">(^_^)>",))
    return Animation(
        name="run",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("run", _create)
