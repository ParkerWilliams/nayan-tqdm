"""disco theme -- Disco ball with cycling rainbow fill.

A mirror ball sparkle cycles across rainbow ANSI-colored blocks.
At completion, a disco ball and music note celebrate.

Rendering tiers:
- emoji: Cycling ANSI color blocks, sparkle emoji, disco ball + note
- unicode: Cycling ANSI color blocks, sparkle kaomoji, sparkle + note
- ascii: "=" fill, "*" sprite, "*!*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
_YEL = "\033[33m"
_GRN = "\033[32m"
_CYN = "\033[36m"
_BLU = "\033[34m"
_MAG = "\033[35m"
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
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRN}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
    )
    # Both frames use 2-col-wide emoji for consistent display_width
    sprite_a = Frame(lines=("\u2728",))          # sparkles emoji (2 cols)
    sprite_b = Frame(lines=("\u2728",))          # sparkles emoji (2 cols)
    completion = Frame(lines=("\u2728\U0001f3b5",))  # sparkles + music note emoji
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRN}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("\u2605",))
    sprite_b = Frame(lines=("\u2606",))
    completion = Frame(lines=("\u2605\u266b",))  # star + music note
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("=",)
    sprite_a = Frame(lines=("*",))
    sprite_b = Frame(lines=("*",))
    completion = Frame(lines=("*!*",))
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("disco", _create)
