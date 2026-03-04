"""cat_play theme -- Hyper cat chasing a laser pointer.

A wide-eyed cat darts after an elusive red dot, leaving paw prints behind.

Rendering tiers:
- emoji: paw print trail, grinning/weary cat faces, heart-eyes completion
- unicode: ANSI-colored paw dots, excited kaomoji, heart completion
- ascii: dot fill, excited kaomoji, simple completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_GRN = "\033[32m"
_RED = "\033[31m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = ("\U0001f43e",)  # paw prints trail
    sprite_a = Frame(lines=("\U0001f63a",))  # open-mouth grinning cat
    sprite_b = Frame(lines=("\U0001f640",))  # weary/startled cat
    completion = Frame(lines=("\U0001f63b\u2728",))  # heart-eyes cat + sparkles

    # laser dots above (🔴=2col), paw prints below (🐾=2col)
    # each line must be >= 70 display cols
    dec_a = Frame(lines=(
        "  \U0001f534              \U0001f534                \U0001f534              \U0001f534                \U0001f534              \U0001f534  ",
        "  \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e  ",
    ))
    dec_b = Frame(lines=(
        "         \U0001f534                \U0001f534              \U0001f534                \U0001f534              \U0001f534           ",
        "    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e    \U0001f43e  ",
    ))
    dec_done = Frame(lines=(
        "  \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728   \u2728",
        "  \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e \U0001f43e",
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
        f"{_GRN}\u2022{_RST}",
        f"{_GRN}\u00b7{_RST}",
        f"{_GRN}\u2022{_RST}",
        " ",
    )
    sprite_a = Frame(lines=(f"{_GRN}(=^OoO^=){_RST}",))  # wide-eyed pounce (9 cols)
    sprite_b = Frame(lines=(f"{_GRN}(=^>.<^=){_RST}",))  # locked-on focus (9 cols)
    completion = Frame(lines=(f"{_RED}(=^\u2665.\u2665^=){_RST}",))  # heart-eyes (10 cols)

    dec_a = Frame(lines=(
        f"  {_RED}\u2022{_RST}              {_RED}\u2022{_RST}                {_RED}\u2022{_RST}              {_RED}\u2022{_RST}                {_RED}\u2022{_RST}              {_RED}\u2022{_RST}",
        f"  {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"         {_RED}\u2022{_RST}              {_RED}\u2022{_RST}                {_RED}\u2022{_RST}              {_RED}\u2022{_RST}                {_RED}\u2022{_RST}     ",
        f"    {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}   {_GRN}\u00b7{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}   {_RED}\u2665{_RST}",
        f"  {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST} {_GRN}\u00b7{_RST}",
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
    fill = (".", " ", ".", " ")
    sprite_a = Frame(lines=("(=^OoO^=)",))  # 9 cols
    sprite_b = Frame(lines=("(=^>.<^=)",))  # 9 cols
    completion = Frame(lines=("(=^o.o^=)!",))  # 10 cols

    dec_a = Frame(lines=(
        "  o                  o                     o                  o              ",
        "  . .   . .   . .   . .   . .   . .   . .   . .   . .   . .   . .   . .   . .",
    ))
    dec_b = Frame(lines=(
        "            o                    o                   o              o        ",
        "  .   . .   . .   . .   . .   . .   . .   . .   .   . .   . .   . .   . .   .",
    ))
    dec_done = Frame(lines=(
        "  !   !   !   !   !   !   !   !   !   !   !   !   !   !   !   !   !   !   !",
        "  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
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
