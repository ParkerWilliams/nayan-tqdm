"""cat_smug theme -- Smug cat strolling confidently, leaving paw prints and fish.

A self-satisfied cat saunters across the bar, its expression alternating
between two smug poses, leaving cozy warm-colored paw trails behind.
Fish and purr wisps drift above and below.

Rendering tiers:
- emoji: Magenta ANSI kaomoji (=^.^=), cozy fill, fish/paw decoration
- unicode: Same ANSI-colored sprites, same fill and decoration
- ascii: Plain (=^.^=) / (=^w^=) sprites, dot/tilde fill, simple decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_MAG = "\033[35m"   # magenta (smug cat)
_YEL = "\033[33m"   # yellow (warm paw prints)
_CYN = "\033[36m"   # cyan (cool paw prints)
_RED = "\033[31m"   # red (heart completion)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Cozy paw-print-like dot fill: alternating magenta/yellow/cyan -- all 1 display col
    fill = (
        f"{_MAG}\u2022{_RST}",   # magenta bullet (paw dot) -- 1 col
        f"{_YEL}\u00b7{_RST}",   # yellow middle dot (paw dot) -- 1 col
        f"{_CYN}\u2022{_RST}",   # cyan bullet (paw dot) -- 1 col
        f"{_MAG}\u00b7{_RST}",   # magenta middle dot (paw dot) -- 1 col
    )
    # Smug alternating expressions -- 7 display cols each
    sprite_a = Frame(lines=(f"{_MAG}(=^.^=){_RST}",))   # smug face (7 cols)
    sprite_b = Frame(lines=(f"{_MAG}(=^w^=){_RST}",))   # smug wide-eye variant (7 cols)
    # Completion: heart-nose smug -- \u2665 is heart suit (1 col), so (=^♥^=) = 7 cols
    completion = Frame(lines=(f"{_RED}(=^\u2665^=){_RST}",))  # heart-nose (7 cols)

    # Decoration: fish drifting above, purr wisps below
    dec_a = Frame(lines=(
        "  ><>    \u00b7       ><>      \u00b7   ><>",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     \u00b7  ><>        \u00b7  ><>  \u00b7    ><>",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  ><> \u00b7 ><> \u00b7 ><> \u00b7 ><> \u00b7 ><>",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_smug",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u2022{_RST}",   # magenta bullet -- 1 col
        f"{_YEL}\u00b7{_RST}",   # yellow middle dot -- 1 col
        f"{_CYN}\u2022{_RST}",   # cyan bullet -- 1 col
        f"{_MAG}\u00b7{_RST}",   # magenta middle dot -- 1 col
    )
    sprite_a = Frame(lines=(f"{_MAG}(=^.^=){_RST}",))
    sprite_b = Frame(lines=(f"{_MAG}(=^w^=){_RST}",))
    completion = Frame(lines=(f"{_RED}(=^\u2665^=){_RST}",))

    dec_a = Frame(lines=(
        "  ><>    .       ><>      .   ><>",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     .  ><>        .  ><>  .    ><>",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  ><> . ><> . ><> . ><> . ><>",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_smug",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = (".", "~", ".", "~")
    sprite_a = Frame(lines=("(=^.^=)",))  # 7 cols
    sprite_b = Frame(lines=("(=^w^=)",))  # 7 cols
    completion = Frame(lines=("(=^w^=)",))  # 7 cols -- satisfied smug

    dec_a = Frame(lines=(
        "  ><>    .       ><>      .   ><>",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     .  ><>        .  ><>  .    ><>",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  ><> . ><> . ><> . ><> . ><>",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_smug",
        frames=(sprite_a, sprite_b),
        fps=2.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("cat_smug", _create)
