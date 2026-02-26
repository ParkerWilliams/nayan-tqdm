"""nyan theme -- Nyan Cat with rainbow trail and twinkling stars.

Three-line theme using WALK mode.  Faithful to the original meme:
pop-tart body cat, rainbow trail, starfield background.

Rendering tiers:
- emoji: ANSI-colored rainbow, cat emoji, sparkle stars
- unicode: ANSI-colored bars, text-art cat, unicode stars
- ascii: Patterned stripes (=, ~, -, .) for rainbow, text cat, asterisks
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes for rainbow stripes
_RED = "\033[31m"
_YEL = "\033[33m"
_GRN = "\033[32m"
_CYN = "\033[36m"
_BLU = "\033[34m"
_MAG = "\033[35m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    """Create nyan Animation at the given rendering tier."""
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
        name="nyan",
        frames=frames,
        fps=8.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
    )


# ── Emoji tier ───────────────────────────────────────
# 3 lines, each 12 display columns wide
# Cat sprite is ~4 cols, rainbow trail is ~6 cols, plus stars

_E_W = 12  # display width for emoji tier


def _emoji_frames() -> tuple[Frame, ...]:
    # Frame 0: stars pattern A
    cat = "\U0001f431"  # 2 cols
    rainbow = (
        f"{_RED}\u2588\u2588{_RST}"    # red block   2 cols
        f"{_YEL}\u2588\u2588{_RST}"    # yellow      2 cols
        f"{_GRN}\u2588\u2588{_RST}"    # green       2 cols
    )  # total rainbow: 6 display cols
    # Stars take remaining 4 cols per line (top/bottom)
    stars_a_top = " .  "   # 4 cols
    stars_a_mid = ""       # rainbow + cat fills this line
    stars_a_bot = "  . "   # 4 cols

    stars_b_top = "  . "   # 4 cols
    stars_b_mid = ""
    stars_b_bot = " .  "   # 4 cols

    # Line layout: [stars (4 cols)] [rainbow (6 cols)] [cat (2 cols)] = 12 cols
    f0_top = stars_a_top + f"{_CYN}\u2588\u2588{_RST}" + f"{_BLU}\u2588\u2588{_RST}" + "  "
    f0_mid = rainbow + f"{_MAG}\u2588\u2588{_RST}" + cat
    f0_bot = stars_a_bot + f"{_CYN}\u2588\u2588{_RST}" + f"{_BLU}\u2588\u2588{_RST}" + "  "

    f1_top = stars_b_top + f"{_BLU}\u2588\u2588{_RST}" + f"{_CYN}\u2588\u2588{_RST}" + "  "
    f1_mid = rainbow + f"{_MAG}\u2588\u2588{_RST}" + cat
    f1_bot = stars_b_bot + f"{_BLU}\u2588\u2588{_RST}" + f"{_CYN}\u2588\u2588{_RST}" + "  "

    return (
        Frame(lines=(f0_top, f0_mid, f0_bot)),
        Frame(lines=(f1_top, f1_mid, f1_bot)),
    )


def _emoji_completion() -> Frame:
    cat = "\U0001f63a"  # grinning cat, 2 cols
    rainbow = (
        f"{_RED}\u2588\u2588{_RST}"
        f"{_YEL}\u2588\u2588{_RST}"
        f"{_GRN}\u2588\u2588{_RST}"
    )
    top = " *  " + f"{_CYN}\u2588\u2588{_RST}" + f"{_BLU}\u2588\u2588{_RST}" + "  "
    mid = rainbow + f"{_MAG}\u2588\u2588{_RST}" + cat
    bot = "  * " + f"{_CYN}\u2588\u2588{_RST}" + f"{_BLU}\u2588\u2588{_RST}" + "  "
    return Frame(lines=(top, mid, bot))


# ── Unicode tier ─────────────────────────────────────
# 3 lines, each 12 display columns wide

_U_W = 12


def _unicode_frames() -> tuple[Frame, ...]:
    cat1 = "/\\_/\\"  # 5 cols
    cat2 = "(\\_/)"   # 5 cols
    # Rainbow trail: 5 display cols (colored bars)
    rb = (
        f"{_RED}={_RST}"
        f"{_YEL}={_RST}"
        f"{_GRN}={_RST}"
        f"{_CYN}={_RST}"
        f"{_BLU}={_RST}"
    )  # 5 display cols

    # Layout: [stars 2 cols] [rainbow 5 cols] [cat 5 cols] = 12 cols
    f0 = Frame(lines=(
        ". " + f"{_CYN}~~~~~{_RST}" + "  .  ",   # 12 cols: star + wave + star
        rb + cat1 + "  ",                            # 12 cols: rainbow + cat + pad
        " ." + f"{_BLU}~~~~~{_RST}" + " .   ",    # 12 cols
    ))
    f1 = Frame(lines=(
        " ." + f"{_BLU}~~~~~{_RST}" + " .   ",    # 12 cols
        rb + cat2 + "  ",                            # 12 cols
        ". " + f"{_CYN}~~~~~{_RST}" + "  .  ",    # 12 cols
    ))
    return (f0, f1)


def _unicode_completion() -> Frame:
    cat = "(=^.^=)"  # 7 cols
    rb = (
        f"{_RED}={_RST}"
        f"{_YEL}={_RST}"
        f"{_GRN}={_RST}"
        f"{_CYN}={_RST}"
        f"{_BLU}={_RST}"
    )
    return Frame(lines=(
        " *" + f"{_CYN}~~~~~{_RST}" + "  *  ",
        rb + cat,
        " *" + f"{_BLU}~~~~~{_RST}" + "  *  ",
    ))


# ── ASCII tier ───────────────────────────────────────
# 3 lines, each 12 display columns wide
# Rainbow uses patterned stripes: =, ~, -, .

_A_W = 12


def _ascii_frames() -> tuple[Frame, ...]:
    cat1 = "=^.^="  # 5 cols
    cat2 = "=^_^="  # 5 cols
    # Rainbow: 5 chars with pattern stripes
    rb = "=~-.="  # 5 cols

    # Layout: [stars 2 cols] [rainbow 5 cols] [cat 5 cols] = 12 cols
    f0 = Frame(lines=(
        "* " + "~=-.~" + "  *  ",   # 12 cols
        rb + cat1 + "  ",            # 12 cols
        " *" + "=~-.=" + " *   ",   # 12 cols
    ))
    f1 = Frame(lines=(
        " *" + "=~-.=" + " *   ",   # 12 cols
        rb + cat2 + "  ",            # 12 cols
        "* " + "~=-.~" + "  *  ",   # 12 cols
    ))
    return (f0, f1)


def _ascii_completion() -> Frame:
    cat = "=^w^="  # 5 cols
    rb = "=~-.="   # 5 cols
    return Frame(lines=(
        " *" + "=~-.=" + " *   ",
        rb + cat + "  ",
        "* " + "~=-.~" + "  *  ",
    ))


register_theme("nyan", _create)
