"""matrix theme -- Digital rain with binary digit fill.

Binary digits rain down in green ANSI as the bar progresses.
At completion, the matrix reveals "DONE".

Rendering tiers:
- emoji: Green ANSI "0"/"1" fill, ">" cursor, green "DONE"
- unicode: Green ANSI "0"/"1" fill, ">" cursor, green "DONE"
- ascii: "01" fill, ">" sprite, ">>>" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_GRN = "\033[32m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = (
        f"{_GRN}0{_RST}",
        f"{_GRN}1{_RST}",
        f"{_GRN}1{_RST}",
        f"{_GRN}0{_RST}",
    )
    sprite_a = Frame(lines=(f"{_GRN}>{_RST}",))
    sprite_b = Frame(lines=(f"{_GRN}>{_RST}",))
    completion = Frame(lines=(f"{_GRN}DONE{_RST}",))
    return Animation(
        name="matrix",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_GRN}0{_RST}",
        f"{_GRN}1{_RST}",
        f"{_GRN}1{_RST}",
        f"{_GRN}0{_RST}",
    )
    sprite_a = Frame(lines=(f"{_GRN}>{_RST}",))
    sprite_b = Frame(lines=(f"{_GRN}>{_RST}",))
    completion = Frame(lines=(f"{_GRN}DONE{_RST}",))
    return Animation(
        name="matrix",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("0", "1", "1", "0")
    sprite_a = Frame(lines=(">",))
    sprite_b = Frame(lines=(">",))
    completion = Frame(lines=(">>>",))
    return Animation(
        name="matrix",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("matrix", _create)
