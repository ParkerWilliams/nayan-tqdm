"""cat_smug theme -- Self-satisfied cat strolling through its fish collection.

A smirking cat saunters across a trail of fish it already caught.

Rendering tiers:
- emoji: fish trail, wry-smile cat sprite, cat + crown completion
- unicode: ANSI-colored fish, half-lidded kaomoji, heart completion
- ascii: fish fill, half-lidded kaomoji, simple completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_CYN = "\033[36m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = (
        "\U0001f41f",  # fish
        "\U0001f41f",  # fish
        "\U0001f41f",  # fish
        "\U0001f365",  # fish cake (variety)
    )
    sprite_a = Frame(lines=("\U0001f63c",))  # cat with wry smile (THE smug cat)
    sprite_b = Frame(lines=("\U0001f63c",))
    completion = Frame(lines=("\U0001f63c\U0001f451",))  # smug cat + crown

    # fish above (🐟=2col), soft dots below
    dec_a = Frame(lines=(
        "  \U0001f41f       \U0001f41f          \U0001f41f       \U0001f41f          \U0001f41f       \U0001f41f          \U0001f41f       \U0001f41f  ",
        "  \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7",
    ))
    dec_b = Frame(lines=(
        "       \U0001f41f          \U0001f41f       \U0001f41f          \U0001f41f       \U0001f41f          \U0001f41f       \U0001f41f       ",
        "     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7     \u00b7  ",
    ))
    dec_done = Frame(lines=(
        "  \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f \U0001f41f",
        "  \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7 \u00b7",
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
        f"{_CYN}>{_RST}",
        f"{_CYN}<{_RST}",
        f"{_CYN}>{_RST}",
        " ",
    )
    sprite_a = Frame(lines=(f"{_MAG}(=^\u2310^=){_RST}",))  # raised-brow smug (7 cols)
    sprite_b = Frame(lines=(f"{_MAG}(=^~^=){_RST}",))       # wink (7 cols)
    completion = Frame(lines=(f"{_MAG}(=^\u2665^=){_RST}",))  # heart-nose (7 cols)

    dec_a = Frame(lines=(
        f"  {_CYN}><>{_RST}       {_CYN}><>{_RST}          {_CYN}><>{_RST}       {_CYN}><>{_RST}          {_CYN}><>{_RST}       {_CYN}><>{_RST}       {_CYN}><>{_RST}",
        f"  {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}  {_MAG}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"       {_CYN}><>{_RST}          {_CYN}><>{_RST}       {_CYN}><>{_RST}          {_CYN}><>{_RST}       {_CYN}><>{_RST}       {_CYN}><>{_RST}       {_CYN}><>{_RST}",
        f"     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}     {_MAG}\u00b7{_RST}  {_MAG}\u00b7{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST} {_CYN}><>{_RST}",
        f"  {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST} {_MAG}\u00b7{_RST}",
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
    fill = (">", "<", ">", " ")
    sprite_a = Frame(lines=("(=^-_-^=)",))  # half-lidded (9 cols)
    sprite_b = Frame(lines=("(=^~_~^=)",))  # winking smug (9 cols)
    completion = Frame(lines=("(=^-_-^=)*",))  # 10 cols

    dec_a = Frame(lines=(
        "  ><>       ><>          ><>       ><>          ><>       ><>       ><>      ",
        "  .     .     .     .     .     .     .     .     .     .     .     .     .  ",
    ))
    dec_b = Frame(lines=(
        "       ><>          ><>       ><>          ><>       ><>       ><>       ><> ",
        "     .     .     .     .     .     .     .     .     .     .     .     .     .",
    ))
    dec_done = Frame(lines=(
        "  ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><> ><>  ",
        "  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
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
