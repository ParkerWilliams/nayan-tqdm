"""pac_man theme -- Pac-Man eating dots across the progress bar.

Pac-Man alternates between open and closed mouth as it moves
across a fill of dots.  At completion, the ghost appears.

Rendering tiers:
- emoji: Middle dot fill, Pac-Man open/close, ghost emoji
- unicode: Middle dot fill, Pac-Man kaomoji, ghost kaomoji
- ascii: Dot fill, "C" / "c" sprite, "O" completion
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
    fill = ("\u00b7",)   # middle dot
    # Both frames use 2-col-wide emoji for consistent display_width
    sprite_open = Frame(lines=("\U0001f7e1",))    # yellow circle (open mouth)
    sprite_closed = Frame(lines=("\U0001f7e0",))  # orange circle (closed mouth)
    completion = Frame(lines=("\U0001f47b",))      # ghost emoji
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u00b7",)
    sprite_open = Frame(lines=("C",))
    sprite_closed = Frame(lines=("c",))
    completion = Frame(lines=("(^_^)",))
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = (".",)
    sprite_open = Frame(lines=("C",))
    sprite_closed = Frame(lines=("c",))
    completion = Frame(lines=("O",))
    return Animation(
        name="pac_man",
        frames=(sprite_open, sprite_closed),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("pac_man", _create)
