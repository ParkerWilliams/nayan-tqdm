"""mario theme -- Super Mario mushroom running with brick fill.

A mushroom sprite runs across brick-colored blocks.
At completion, a star celebrates the finish.

Rendering tiers:
- emoji: Brick-colored ANSI blocks, mushroom emoji, star emoji
- unicode: Brick-colored ANSI blocks, mushroom kaomoji, star
- ascii: Hash fill, ">o>" sprite, "*o*" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI colors
_RED = "\033[31m"
_YEL = "\033[33m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Brick-colored fill: alternating red and dark red blocks
    fill = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("\U0001f344",))   # mushroom emoji
    sprite_b = Frame(lines=("\U0001f344",))   # mushroom emoji
    completion = Frame(lines=("\u2605",))     # star
    return Animation(
        name="mario",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("(o)",))
    sprite_b = Frame(lines=("(O)",))
    completion = Frame(lines=("(*)",))
    return Animation(
        name="mario",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprite_a = Frame(lines=(">o>",))
    sprite_b = Frame(lines=(">O>",))
    completion = Frame(lines=("*o*",))
    return Animation(
        name="mario",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("mario", _create)
