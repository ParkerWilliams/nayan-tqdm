"""fish theme -- a fish swimming through water.

Three-line theme using WALK mode.  The fish swims left-to-right
as progress increases, with a water surface and bubbles.

Layout:
- Line 0: Sky / air above water
- Line 1: Water surface (waves)
- Line 2: Underwater with fish

Rendering tiers:
- emoji: Fish emoji, wave emoji, bubble emoji
- unicode: Unicode fish, tilde waves with ANSI blue, circle bubbles
- ascii: ``><>`` fish, ``~`` waves, ``o`` bubbles
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_BLU = "\033[34m"
_CYN = "\033[36m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    """Create fish Animation at the given rendering tier."""
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
        name="fish",
        frames=frames,
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
    )


# ── Emoji tier ───────────────────────────────────────
# 3 lines, each 6 display cols wide


def _emoji_frames() -> tuple[Frame, ...]:
    # Fish: 2 cols, bubbles: 2 cols each
    # Frame 0: bubble high
    # Frame 1: bubble low
    # Frame 2: no bubble
    return (
        Frame(lines=(
            "   o  ",  # 6 cols: bubble high
            "~~~~~~",  # 6 cols: waves
            " ><>  ",  # 6 cols: fish
        )),
        Frame(lines=(
            "      ",  # 6 cols: empty sky
            "~~~~~~",  # 6 cols: waves
            " ><> o",  # 6 cols: fish + bubble
        )),
        Frame(lines=(
            "  o   ",  # 6 cols: bubble popping
            "~~~~~~",  # 6 cols: waves
            " ><>  ",  # 6 cols: fish
        )),
    )


def _emoji_completion() -> Frame:
    return Frame(lines=(
        "  ><> ",  # 6 cols: fish jumping out
        "~~**~~",  # 6 cols: splash
        "      ",  # 6 cols: underwater empty
    ))


# ── Unicode tier ─────────────────────────────────────
# 3 lines, each 8 display cols wide


def _unicode_frames() -> tuple[Frame, ...]:
    wave = f"{_CYN}~~~~~~~~{_RST}"  # 8 display cols
    return (
        Frame(lines=(
            "    o   ",  # 8 cols
            wave,
            "  ><>   ",  # 8 cols
        )),
        Frame(lines=(
            "        ",  # 8 cols
            wave,
            "  ><> o ",  # 8 cols
        )),
        Frame(lines=(
            "   o    ",  # 8 cols
            wave,
            "  ><>   ",  # 8 cols
        )),
    )


def _unicode_completion() -> Frame:
    wave = f"{_CYN}~~{_RST}" + f"{_BLU}**{_RST}" + f"{_CYN}~~{_RST}" + "  "
    return Frame(lines=(
        "   ><>  ",
        wave,
        "        ",
    ))


# ── ASCII tier ───────────────────────────────────────
# 3 lines, each 8 display cols wide


def _ascii_frames() -> tuple[Frame, ...]:
    return (
        Frame(lines=(
            "    o   ",  # 8 cols
            "~~~~~~~~",  # 8 cols
            "  ><>   ",  # 8 cols
        )),
        Frame(lines=(
            "        ",  # 8 cols
            "~~~~~~~~",  # 8 cols
            "  ><> o ",  # 8 cols
        )),
        Frame(lines=(
            "   o    ",  # 8 cols
            "~~~~~~~~",  # 8 cols
            "  ><>   ",  # 8 cols
        )),
    )


def _ascii_completion() -> Frame:
    return Frame(lines=(
        "   ><>  ",  # 8 cols: fish jumping
        "~~****~~",  # 8 cols: splash
        "        ",  # 8 cols
    ))


register_theme("fish", _create)
