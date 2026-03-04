"""table_unflip theme -- Calmly puts the table back.

The anti-rage response: a calm face walks across the bar and
respectfully puts the table back at completion.

Rendering tiers:
- emoji: Block fill, calm face, table unflip with box-drawing table
- unicode: Same
- ascii: Hash fill, calm face, table put-back
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
        Frame(lines=("(\u00b0_\u00b0)",)),    # (°_°)
        Frame(lines=("(\u00b0\u203f\u00b0)",)),  # (°‿°)
    )
    completion = Frame(lines=(
        "\u252c\u2500\u252c\u30ce(\u00b0_\u00b0\u30ce)",
    ))  # ┬─┬ノ(°_°ノ)
    return Animation(
        name="table_unflip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2588",)
    sprites = (
        Frame(lines=("(\u00b0_\u00b0)",)),
        Frame(lines=("(\u00b0\u203f\u00b0)",)),
    )
    completion = Frame(lines=(
        "\u252c\u2500\u252c\u30ce(\u00b0_\u00b0\u30ce)",
    ))
    return Animation(
        name="table_unflip",
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
        Frame(lines=("(o-o)",)),
    )
    completion = Frame(lines=("|__| (o_o)",))
    return Animation(
        name="table_unflip",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("table_unflip", _create)
