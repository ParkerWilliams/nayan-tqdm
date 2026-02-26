"""rocket theme -- a rocket launching with flame animation.

Four-line theme using CYCLE mode.  The rocket stays centered while
flames flicker below it.

Layout:
- Line 0: Rocket nose/tip
- Line 1: Rocket body
- Line 2: Flame exhaust (animated)
- Line 3: Ground / launch pad

Rendering tiers:
- emoji: Rocket with fire emoji flames
- unicode: Arrow rocket with ANSI-colored block flames
- ascii: ``/\\`` rocket with ``*`` and ``^`` flames
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
_YEL = "\033[33m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    """Create rocket Animation at the given rendering tier."""
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
        name="rocket",
        frames=frames,
        fps=8.0,
        mode=AnimationMode.CYCLE,
        completion_frame=completion,
    )


# ── Emoji tier ───────────────────────────────────────
# 4 lines, each 6 display cols wide


def _emoji_frames() -> tuple[Frame, ...]:
    nose = "  /\\  "    # 6 cols
    body = "  ||  "    # 6 cols
    gnd  = "======" # 6 cols
    return (
        Frame(lines=(nose, body, "  **  ", gnd)),  # small flame
        Frame(lines=(nose, body, " **** ", gnd)),  # medium flame
        Frame(lines=(nose, body, " *^^* ", gnd)),  # large flame
    )


def _emoji_completion() -> Frame:
    return Frame(lines=(
        "  /\\  ",  # 6 cols: rocket nose
        "  ||  ",  # 6 cols: body
        "      ",  # 6 cols: no flame (in space)
        " .  . ",  # 6 cols: stars
    ))


# ── Unicode tier ─────────────────────────────────────
# 4 lines, each 6 display cols wide


def _unicode_frames() -> tuple[Frame, ...]:
    nose = "  /\\  "  # 6 cols
    body = "  ||  "  # 6 cols
    gnd  = "\u2550" * 6  # double horizontal x6 (6 cols)
    flame_s = f"  {_RED}**{_RST}  "   # 6 display cols
    flame_m = f" {_YEL}*{_RST}{_RED}**{_RST}{_YEL}*{_RST} "  # 6 display cols
    flame_l = f" {_RED}*{_RST}{_YEL}^^{_RST}{_RED}*{_RST} "  # 6 display cols
    return (
        Frame(lines=(nose, body, flame_s, gnd)),
        Frame(lines=(nose, body, flame_m, gnd)),
        Frame(lines=(nose, body, flame_l, gnd)),
    )


def _unicode_completion() -> Frame:
    return Frame(lines=(
        "  /\\  ",
        "  ||  ",
        "      ",
        " .  . ",
    ))


# ── ASCII tier ───────────────────────────────────────
# 4 lines, each 6 display cols wide


def _ascii_frames() -> tuple[Frame, ...]:
    nose = "  /\\  "  # 6 cols
    body = "  ||  "  # 6 cols
    gnd  = "======"  # 6 cols
    return (
        Frame(lines=(nose, body, "  **  ", gnd)),  # small
        Frame(lines=(nose, body, " **** ", gnd)),  # medium
        Frame(lines=(nose, body, " *^^* ", gnd)),  # large
    )


def _ascii_completion() -> Frame:
    return Frame(lines=(
        "  /\\  ",
        "  ||  ",
        "      ",
        " .  . ",
    ))


register_theme("rocket", _create)
