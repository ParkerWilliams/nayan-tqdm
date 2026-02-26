"""cat_bounce theme -- a cat bouncing above a ground line.

Two-line theme using WALK mode.  The cat bounces up and down as it
moves across the bar with progress.  Four bounce frames cycle through
up/down positions.

Rendering tiers:
- emoji: Cat emoji bouncing over block ground
- unicode: Text-art cat over box-drawing ground
- ascii: Simple ASCII cat over dash ground
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []


def _create(tier: str) -> Animation:
    """Create cat_bounce Animation at the given rendering tier."""
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
        name="cat_bounce",
        frames=frames,
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
    )


# ── Emoji tier ───────────────────────────────────────
# Each frame: 2 lines, all lines 2 display columns wide


def _emoji_frames() -> tuple[Frame, ...]:
    cat = "\U0001f431"   # cat face (2 cols)
    sp = "  "            # 2 spaces (2 cols)
    gnd = "\u2584\u2584"  # lower half block x2 (2 cols)
    return (
        Frame(lines=(cat, gnd)),  # up
        Frame(lines=(sp, cat)),   # down
        Frame(lines=(cat, gnd)),  # up
        Frame(lines=(sp, cat)),   # down
    )


def _emoji_completion() -> Frame:
    return Frame(lines=("\U0001f63a", "\u2584\u2584"))  # grinning cat on ground


# ── Unicode tier ─────────────────────────────────────
# Each frame: 2 lines, all lines 5 display columns wide


def _unicode_frames() -> tuple[Frame, ...]:
    cat = "/\\_/\\"     # 5 cols
    sp  = "     "       # 5 cols
    gnd = "\u2500" * 5  # horizontal box line x5 (5 cols)
    return (
        Frame(lines=(cat, gnd)),   # up
        Frame(lines=(sp,  cat)),   # down (cat on ground row)
        Frame(lines=(cat, gnd)),   # up
        Frame(lines=(sp,  cat)),   # down
    )


def _unicode_completion() -> Frame:
    return Frame(lines=("=^.^=", "\u2500" * 5))  # sitting cat on ground


# ── ASCII tier ───────────────────────────────────────
# Each frame: 2 lines, all lines 5 display columns wide


def _ascii_frames() -> tuple[Frame, ...]:
    cat1 = "=^.^="    # 5 cols
    cat2 = "=^_^="    # 5 cols
    sp   = "     "    # 5 cols
    gnd  = "-----"    # 5 cols
    return (
        Frame(lines=(cat1, gnd)),   # up, pose 1
        Frame(lines=(sp,   cat1)),  # down, pose 1
        Frame(lines=(cat2, gnd)),   # up, pose 2
        Frame(lines=(sp,   cat2)),  # down, pose 2
    )


def _ascii_completion() -> Frame:
    return Frame(lines=("=^w^=", "-----"))  # sitting cat on ground


register_theme("cat_bounce", _create)
