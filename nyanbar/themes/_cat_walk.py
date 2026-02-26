"""cat_walk theme -- a cat walking across the progress bar.

Single-line theme using WALK mode.  The cat moves left-to-right
as progress increases.  Two walking frames alternate legs.

Rendering tiers:
- emoji: Cat emoji variants
- unicode: Text-art cat faces
- ascii: Simple ASCII cat ``=^.^=``
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []


def _create(tier: str) -> Animation:
    """Create cat_walk Animation at the given rendering tier."""
    if tier == "emoji":
        frames = _emoji_frames()
        completion = _emoji_completion()
    elif tier == "unicode":
        frames = _unicode_frames()
        completion = _unicode_completion()
    else:
        frames = _ascii_frames()
        completion = _ascii_completion()
    return Animation(
        name="cat_walk",
        frames=frames,
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
    )


# ── Emoji tier ───────────────────────────────────────


def _emoji_frames() -> tuple[Frame, ...]:
    # Two walking poses -- both are 2 display columns wide
    return (
        Frame(lines=("\U0001f408",)),   # cat (2 cols)
        Frame(lines=("\U0001f431",)),   # cat face (2 cols)
    )


def _emoji_completion() -> Frame:
    return Frame(lines=("\U0001f63a",))  # grinning cat face (2 cols)


# ── Unicode tier ─────────────────────────────────────


def _unicode_frames() -> tuple[Frame, ...]:
    # All frames: 7 display columns wide
    return (
        Frame(lines=(" /\\_/\\.",)),   # 7 cols
        Frame(lines=(" (\\_/).",)),    # 7 cols
    )


def _unicode_completion() -> Frame:
    return Frame(lines=("(=^.^=)",))    # 7 cols


# ── ASCII tier ───────────────────────────────────────


def _ascii_frames() -> tuple[Frame, ...]:
    # All frames: 5 display columns wide
    return (
        Frame(lines=("=^.^=",)),
        Frame(lines=("=^_^=",)),
    )


def _ascii_completion() -> Frame:
    return Frame(lines=("=^w^=",))


register_theme("cat_walk", _create)
