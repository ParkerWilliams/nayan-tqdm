"""double_flip theme -- Flips TWO tables at once.

Peak frustration: the face gets increasingly angry, then at
completion flips tables on BOTH sides simultaneously.

Rendering tiers:
- emoji: Block fill, angry face, double table flip with box-drawing
- unicode: Same
- ascii: Hash fill, angry face, double ASCII table flip
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
        Frame(lines=("(\u00b0\u0414\u00b0)",)),   # (°Д°)
    )
    completion = Frame(lines=(
        "\u253b\u2501\u253b\ufe35\u30fd(\u00b0\u25a1\u00b0)\uff89\ufe35\u253b\u2501\u253b",
    ))  # ┻━┻︵ヽ(°□°)ﾉ︵┻━┻
    return Animation(
        name="double_flip",
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
        Frame(lines=("(\u00b0\u0414\u00b0)",)),
    )
    completion = Frame(lines=(
        "\u253b\u2501\u253b\ufe35\u30fd(\u00b0\u25a1\u00b0)\uff89\ufe35\u253b\u2501\u253b",
    ))
    return Animation(
        name="double_flip",
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
    completion = Frame(lines=("|__| /(O_O)\\ |__|",))
    return Animation(
        name="double_flip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("double_flip", _create)
