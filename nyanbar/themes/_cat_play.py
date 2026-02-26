"""cat_play theme -- Playful cat batting at toys, energetic and colorful.

A hyperactive cat bats at toys left and right with wild energy, leaving
a trail of colorful toy bits. Bouncing toys drift above and scuff marks
appear below.

Rendering tiers:
- emoji: Green ANSI kaomoji batting left/right, colorful toy fill, toy decoration
- unicode: Same ANSI-colored sprites, same fill and decoration
- ascii: Plain batting sprites, star/tilde fill, bouncing ball decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_GRN = "\033[32m"   # green (playful cat)
_RED = "\033[31m"   # red (toy)
_YEL = "\033[33m"   # yellow (toy)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Colorful toy fill: red/green/yellow dots and diamonds -- all 1 display col
    fill = (
        f"{_RED}\u2022{_RST}",    # red bullet (toy dot) -- 1 col
        f"{_GRN}\u25c6{_RST}",   # green diamond (toy) -- 1 col
        f"{_YEL}\u2022{_RST}",   # yellow bullet (toy dot) -- 1 col
        f"{_RED}\u25c6{_RST}",   # red diamond (toy) -- 1 col
        f"{_GRN}\u2022{_RST}",   # green bullet (toy dot) -- 1 col
        f"{_YEL}\u25c6{_RST}",   # yellow diamond (toy) -- 1 col
    )
    # Chase mechanic: batting right then batting left -- 8 display cols each
    # (=^.^=)~ = ( = ^ . ^ = ) ~ = 8 chars all 1 col
    sprite_a = Frame(lines=(f"{_GRN}(=^.^=)~{_RST}",))   # batting right (8 cols)
    # ~(=^.^=) = ~ ( = ^ . ^ = ) = 8 chars all 1 col
    sprite_b = Frame(lines=(f"{_GRN}~(=^.^=){_RST}",))   # batting left (8 cols)
    # Completion: happy relaxed -- (=^\u2665^=) = 7 cols (width can differ at 100%)
    completion = Frame(lines=(f"{_GRN}(=^\u2665^=){_RST}",))  # heart-nose happy (7 cols)

    # Decoration: bouncing toys above, paw scuffs below
    dec_a = Frame(lines=(
        "  o    *       o         *   o",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_b = Frame(lines=(
        "     *  o        *  o  *    o",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_done = Frame(lines=(
        "  o * o * o * o * o * o",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_play",
        frames=(sprite_a, sprite_b),
        fps=5.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    fill = (
        f"{_RED}\u2022{_RST}",    # red bullet -- 1 col
        f"{_GRN}\u25c6{_RST}",   # green diamond -- 1 col
        f"{_YEL}\u2022{_RST}",   # yellow bullet -- 1 col
        f"{_RED}\u25c6{_RST}",   # red diamond -- 1 col
        f"{_GRN}\u2022{_RST}",   # green bullet -- 1 col
        f"{_YEL}\u25c6{_RST}",   # yellow diamond -- 1 col
    )
    sprite_a = Frame(lines=(f"{_GRN}(=^.^=)~{_RST}",))
    sprite_b = Frame(lines=(f"{_GRN}~(=^.^=){_RST}",))
    completion = Frame(lines=(f"{_GRN}(=^\u2665^=){_RST}",))

    dec_a = Frame(lines=(
        "  o    *       o         *   o",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_b = Frame(lines=(
        "     *  o        *  o  *    o",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_done = Frame(lines=(
        "  o * o * o * o * o * o",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_play",
        frames=(sprite_a, sprite_b),
        fps=5.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("*", "~", "*", "~")
    sprite_a = Frame(lines=("(=^.^=)~",))  # 8 cols -- batting right
    sprite_b = Frame(lines=("~(=^.^=)",))  # 8 cols -- batting left
    completion = Frame(lines=("(=^o^=)",))  # 7 cols -- happy face!

    dec_a = Frame(lines=(
        "  o    *       o         *   o",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_b = Frame(lines=(
        "     *  o        *  o  *    o",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_done = Frame(lines=(
        "  o * o * o * o * o * o",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_play",
        frames=(sprite_a, sprite_b),
        fps=5.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("cat_play", _create)
