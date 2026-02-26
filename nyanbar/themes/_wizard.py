"""wizard theme -- Wizard leaving a colorful magical symbol trail.

A wizard emoji glides forward, leaving a trail of colorful magical
symbols: stars, sparkles, diamonds, snowflakes, and comets.
At completion, the wizard casts a final sparkle.

Rendering tiers:
- emoji: Colorful magical symbol fill, wizard emoji, wizard + sparkles
- unicode: Colorful magical symbol fill, "*>" / "~>" sprite, "*>*" completion
- ascii: Varied magical ASCII fill, "*>" / "~>" sprite, "*>*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_CYN = "\033[36m"
_BLU = "\033[34m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Diverse colorful magical symbols -- each is 1 display col
    fill = (
        f"{_MAG}\u2605{_RST}",   # star (magenta)
        f"{_CYN}\u2733{_RST}",   # eight-spoked asterisk (cyan)
        f"{_BLU}\u2666{_RST}",   # diamond (blue)
        f"{_MAG}\u2606{_RST}",   # hollow star (magenta)
        f"{_CYN}\u2744{_RST}",   # snowflake (cyan)
        f"{_BLU}\u2604{_RST}",   # comet (blue)
    )
    # Wizard emoji -- 2 display cols, both frames identical for consistent width
    sprite_a = Frame(lines=("\U0001f9d9",))
    sprite_b = Frame(lines=("\U0001f9d9",))
    # Wizard + sparkles at completion
    completion = Frame(lines=("\U0001f9d9\u2728",))
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u2605{_RST}",
        f"{_CYN}\u2733{_RST}",
        f"{_BLU}\u2666{_RST}",
        f"{_MAG}\u2606{_RST}",
        f"{_CYN}\u2744{_RST}",
        f"{_BLU}\u2604{_RST}",
    )
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    # Variety of magical-ish ASCII characters
    fill = ("*", "~", "+", ".", "*", "~")
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))
    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("wizard", _create)
