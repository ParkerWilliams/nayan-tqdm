"""cat_sleepy theme -- Drowsy cat drifting along, soft pastel dreamy fill.

A sleepy cat barely keeping its eyes open, drifting slowly with dreamy
pastel-colored fill. z's float above and soft dreamy clouds drift below.

Rendering tiers:
- emoji: Blue ANSI kaomoji (-._.-), dreamy pastel fill, zzz decoration
- unicode: Same ANSI-colored sprites, same fill and decoration
- ascii: Plain (-._.-) / (u._.u) sprites, dot/dash fill, plain z decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_BLU = "\033[34m"   # blue (drowsy cat)
_MAG = "\033[35m"   # magenta (dreamy dots)
_CYN = "\033[36m"   # cyan (dreamy dots)
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
    # Pastel dreamy fill: soft blue/magenta/cyan dots -- all 1 display col
    fill = (
        f"{_BLU}\u2022{_RST}",   # blue bullet -- 1 col
        f"{_MAG}\u00b7{_RST}",   # magenta middle dot -- 1 col
        f"{_CYN}\u2022{_RST}",   # cyan bullet -- 1 col
        f"{_BLU}\u00b7{_RST}",   # blue middle dot -- 1 col
    )
    # Drowsy alternating expressions -- 7 display cols each
    # (-._.-) = ( - . _ . - ) = 7 chars, all 1 col
    sprite_a = Frame(lines=(f"{_BLU}(-._.-){_RST}",))   # drooping eyes (7 cols)
    # (u._.u) = ( u . _ . u ) = 7 chars, all 1 col
    sprite_b = Frame(lines=(f"{_BLU}(u._.u){_RST}",))   # closed drowsy eyes (7 cols)
    # Completion: dreaming of love -- (-.\u2665.-) = ( - . \u2665 . - ) = 7 cols
    completion = Frame(lines=(f"{_RED}(-.\u2665.-){_RST}",))  # heart dream (7 cols)

    # Decoration: z's floating above (sleeping), soft dots below
    dec_a = Frame(lines=(
        "  z    .       z         .   z",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     .  z        .  z  .    z",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  z . z . z . z . z . z",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_sleepy",
        frames=(sprite_a, sprite_b),
        fps=1.5,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    fill = (
        f"{_BLU}\u2022{_RST}",   # blue bullet -- 1 col
        f"{_MAG}\u00b7{_RST}",   # magenta middle dot -- 1 col
        f"{_CYN}\u2022{_RST}",   # cyan bullet -- 1 col
        f"{_BLU}\u00b7{_RST}",   # blue middle dot -- 1 col
    )
    sprite_a = Frame(lines=(f"{_BLU}(-._.-){_RST}",))
    sprite_b = Frame(lines=(f"{_BLU}(u._.u){_RST}",))
    completion = Frame(lines=(f"{_RED}(-.\u2665.-){_RST}",))

    dec_a = Frame(lines=(
        "  z    .       z         .   z",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     .  z        .  z  .    z",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  z . z . z . z . z . z",
        "  ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_sleepy",
        frames=(sprite_a, sprite_b),
        fps=1.5,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = (".", "-", ".", "-")
    sprite_a = Frame(lines=("(-._.-)",))  # 7 cols
    sprite_b = Frame(lines=("(u._.u)",))  # 7 cols
    completion = Frame(lines=("(-._!-)",))  # 7 cols -- wake-up moment!

    dec_a = Frame(lines=(
        "  z    .       z         .   z",
        "  . - .   - .   - .   - .",
    ))
    dec_b = Frame(lines=(
        "     .  z        .  z  .    z",
        "  - . -   . -   . -   . -",
    ))
    dec_done = Frame(lines=(
        "  z . z . z . z . z . z",
        "  - . - . - . - . - . -",
    ))

    return Animation(
        name="cat_sleepy",
        frames=(sprite_a, sprite_b),
        fps=1.5,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("cat_sleepy", _create)
