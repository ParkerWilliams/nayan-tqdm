"""table_rage theme -- Maximum rage table flip.

Even angrier than table_flip. Uses Kannada ಠ and CJK 益/皿
for peak fury. At completion, a violent table launch.

Rendering tiers:
- emoji: Dark block fill, ಠ益ಠ rage face, violent table flip
- unicode: Same
- ascii: Hash/equals fill, angry face, table toss
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
    fill = ("\u2593", "\u2588")   # ▓█
    sprites = (
        Frame(lines=("(\u0ca0\u76ca\u0ca0)",)),   # (ಠ益ಠ)
        Frame(lines=("(\u0ca0\u76bf\u0ca0)",)),   # (ಠ皿ಠ)
    )
    completion = Frame(lines=(
        "(\u30ce\u0ca0\u76ca\u0ca0)\u30ce\ufe35\u253b\u2501\u253b",
    ))  # (ノಠ益ಠ)ノ︵┻━┻
    return Animation(
        name="table_rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2593", "\u2588")
    sprites = (
        Frame(lines=("(\u0ca0\u76ca\u0ca0)",)),
        Frame(lines=("(\u0ca0\u76bf\u0ca0)",)),
    )
    completion = Frame(lines=(
        "(\u30ce\u0ca0\u76ca\u0ca0)\u30ce\ufe35\u253b\u2501\u253b",
    ))
    return Animation(
        name="table_rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#", "=")
    sprites = (
        Frame(lines=("(>__<)",)),
        Frame(lines=("(>oo<)",)),
    )
    completion = Frame(lines=("(>__<)/ ~|__|",))
    return Animation(
        name="table_rage",
        frames=sprites,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("table_rage", _create)
