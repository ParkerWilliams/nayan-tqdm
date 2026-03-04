"""nyan theme -- Rainbow bar fill with cat sprite and twinkling stars.

The progress bar fill cycles through 6 rainbow colors.  A cat emoji
walks at the leading edge.  Twinkling star decorations appear above
and below the bar.

Rendering tiers:
- emoji: ANSI-colored rainbow blocks, cat emoji, sparkle decorations
- unicode: ANSI-colored rainbow blocks, ``=^.^=`` cat, star decorations
- ascii: Plain ``#`` fill, ``=^.^=`` cat, ``*`` decorations
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes for rainbow
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
    rainbow = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRN}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
    )
    cat = "\U0001f431"  # cat face emoji
    cat_done = "\U0001f63a"  # grinning cat

    dec_a = Frame(lines=(
        "  ✦       ★                    ✦            ★            ✦       ★   ✦  ",
        "  ★    ✦              ★              ✦              ★    ✦         ★  ",
    ))
    dec_b = Frame(lines=(
        "     ★          ✦         ★               ✦         ★         ✦      ★  ",
        "✦         ★         ✦            ★         ✦         ★    ✦         ★  ",
    ))
    dec_done = Frame(lines=(
        "  ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★",
        "  ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦ ★ ✦",
    ))

    return Animation(
        name="nyan",
        frames=(Frame(lines=(cat,)), Frame(lines=(cat,))),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=Frame(lines=(cat_done,)),
        bar_fill=rainbow,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    rainbow = (
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_GRN}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
    )
    cat = "=^.^="
    cat_done = "=^\u2764^="

    dec_a = Frame(lines=(
        "  *       .                    *            .            *       .   *  ",
        "  .    *              .              *              .    *         .  * ",
    ))
    dec_b = Frame(lines=(
        "     .          *         .               *         .         *      .  ",
        "*         .         *            .         *         .    *         .  * ",
    ))
    dec_done = Frame(lines=(
        "  *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .",
        "  .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *",
    ))

    return Animation(
        name="nyan",
        frames=(Frame(lines=(cat,)), Frame(lines=(cat,))),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=Frame(lines=(cat_done,)),
        bar_fill=rainbow,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("#",)
    cat = "=^.^="
    cat_done = "=^w^="

    dec_a = Frame(lines=(
        "  *       .                    *            .            *       .   *  ",
        "  .    *              .              *              .    *         .  * ",
    ))
    dec_b = Frame(lines=(
        "     .          *         .               *         .         *      .  ",
        "*         .         *            .         *         .    *         .  * ",
    ))
    dec_done = Frame(lines=(
        "  *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .",
        "  .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *   .   *",
    ))

    return Animation(
        name="nyan",
        frames=(Frame(lines=(cat,)), Frame(lines=(cat,))),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=Frame(lines=(cat_done,)),
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("nyan", _create)
