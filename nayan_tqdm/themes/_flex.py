"""flex theme -- Flexing muscles across the bar.

The ᕦ(°_°)ᕤ face flexes as it walks. At completion, it smiles.

Rendering tiers:
- emoji: Solid block fill, Canadian Syllabics arms
- unicode: Same
- ascii: Hash fill, "d(o_o)b" face
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
    fill = ("\u2588",)   # solid block
    sprites = (
        Frame(lines=("\u1566(\u00b0_\u00b0)\u1564",)),   # ᕦ(°_°)ᕤ
        Frame(lines=("\u1566(\u00b0\u203f\u00b0)\u1564",)),  # ᕦ(°‿°)ᕤ
    )
    completion = Frame(lines=("\u1566(\u00b0\u25bd\u00b0)\u1564",))  # ᕦ(°▽°)ᕤ
    return Animation(
        name="flex",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2588",)
    sprites = (
        Frame(lines=("\u1566(\u00b0_\u00b0)\u1564",)),
        Frame(lines=("\u1566(\u00b0\u203f\u00b0)\u1564",)),
    )
    completion = Frame(lines=("\u1566(\u00b0\u25bd\u00b0)\u1564",))
    return Animation(
        name="flex",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprites = (
        Frame(lines=("d(o_o)b",)),
        Frame(lines=("d(O_O)b",)),
    )
    completion = Frame(lines=("d(^_^)b",))
    return Animation(
        name="flex",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("flex", _create)
