"""cat_sleepy theme -- Drowsy cat drifting off to sleep.

A sleepy cat nods off, leaving a trail of zzz's behind.

Rendering tiers:
- emoji: zzz trail, drowsy/sleeping cat faces, peaceful completion
- unicode: blue ANSI z's, droopy-eyed kaomoji, heart completion
- ascii: z fill, droopy-eyed kaomoji, simple completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

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
    fill = ("\U0001f4a4",)  # zzz emoji trail
    sprite_a = Frame(lines=("\U0001f63a",))  # open-mouth cat (trying to stay awake)
    sprite_b = Frame(lines=("\U0001f63f",))  # crying cat (eyes watering from yawns)
    completion = Frame(lines=("\U0001f63d\U0001f4a4",))  # kissing cat (peaceful) + zzz

    # zzz floating above (💤=2col), soft dream stars below (✩=1col)
    dec_a = Frame(lines=(
        "     \U0001f4a4       \U0001f4a4            \U0001f4a4       \U0001f4a4            \U0001f4a4       \U0001f4a4            \U0001f4a4       ",
        "  \u2729           \u2729           \u2729           \u2729           \u2729           \u2729           \u2729           \u2729",
    ))
    dec_b = Frame(lines=(
        "  \U0001f4a4            \U0001f4a4       \U0001f4a4       \U0001f4a4            \U0001f4a4       \U0001f4a4            \U0001f4a4       ",
        "        \u2729           \u2729           \u2729           \u2729           \u2729           \u2729           \u2729",
    ))
    dec_done = Frame(lines=(
        "  \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4 \U0001f4a4",
        "  \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729   \u2729",
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
        f"{_BLU}z{_RST}",
        f"{_MAG}z{_RST}",
        f"{_BLU}Z{_RST}",
        " ",
    )
    sprite_a = Frame(lines=(f"{_BLU}(-._.-){_RST}",))  # drooping eyes (7 cols)
    sprite_b = Frame(lines=(f"{_BLU}(u._.u){_RST}",))  # eyes closing (7 cols)
    completion = Frame(lines=(f"{_MAG}(-.\u2665.-){_RST}",))  # dreaming of love (7 cols)

    dec_a = Frame(lines=(
        f"     {_BLU}z{_RST}       {_BLU}Z{_RST}  {_BLU}z{_RST}           {_BLU}z{_RST}       {_BLU}Z{_RST}  {_BLU}z{_RST}           {_BLU}z{_RST}       {_BLU}Z{_RST}  {_BLU}z{_RST}        {_BLU}z{_RST}",
        f"  {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"  {_BLU}Z{_RST}  {_BLU}z{_RST}          {_BLU}Z{_RST}       {_BLU}z{_RST}       {_BLU}Z{_RST}  {_BLU}z{_RST}          {_BLU}Z{_RST}       {_BLU}z{_RST}       {_BLU}Z{_RST}     {_BLU}z{_RST}  ",
        f"        {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}           {_MAG}\u00b7{_RST}  ",
    ))
    dec_done = Frame(lines=(
        f"  {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST} {_BLU}z{_RST} {_BLU}Z{_RST}",
        f"  {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_MAG}\u00b7{_RST}",
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
    fill = ("z", " ", "Z", " ")
    sprite_a = Frame(lines=("(-._.-)",))  # 7 cols
    sprite_b = Frame(lines=("(u._.u)",))  # 7 cols
    completion = Frame(lines=("(-._.-)~",))  # 8 cols -- peaceful

    dec_a = Frame(lines=(
        "     z       Z  z           z       Z  z           z       Z  z        z    ",
        "  .           .           .           .           .           .           .  ",
    ))
    dec_b = Frame(lines=(
        "  Z  z          Z       z       Z  z          Z       z       Z     z       ",
        "        .           .           .           .           .           .        ",
    ))
    dec_done = Frame(lines=(
        "  z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z Z z",
        "  .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   . ",
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
