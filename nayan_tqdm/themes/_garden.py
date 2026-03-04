"""garden theme -- Growing garden with flowers and leaves.

A sunflower blooms at the leading edge, leaving a colorful trail of
flowers and leaves. Petals drift above and grass grows below.

Rendering tiers:
- emoji: Green/yellow/magenta floral symbols, sunflower emoji, petal decoration
- unicode: Colored symbols, "@" / "*" sprites, petal and grass decoration
- ascii: "*" "." "~" "o" fill, "@" sprite, "." "~" decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_GRN = "\033[32m"   # green (leaves)
_YEL = "\033[33m"   # yellow (flowers)
_MAG = "\033[35m"   # magenta (blooms)
_CYN = "\033[36m"   # cyan (morning dew)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Garden fill: bullet, diamond, star in green/yellow/magenta -- all 1 col
    fill = (
        f"{_GRN}\u2022{_RST}",   # green bullet (leaf)
        f"{_YEL}\u2605{_RST}",   # yellow star (flower center)
        f"{_MAG}\u2666{_RST}",   # magenta diamond (bloom)
        f"{_GRN}\u2605{_RST}",   # green star (plant)
        f"{_YEL}\u2022{_RST}",   # yellow bullet (bud)
        f"{_MAG}\u2022{_RST}",   # magenta bullet (petal)
    )
    # Sunflower emoji is 2 cols; both frames identical
    sprite_a = Frame(lines=("\U0001f33b",))    # sunflower (2 cols)
    sprite_b = Frame(lines=("\U0001f33b",))
    completion = Frame(lines=("\U0001f33b\u2728",))   # sunflower + sparkles

    # Decoration: petals/butterflies above, grass/soil below
    dec_a = Frame(lines=(
        f"  {_MAG}\u00b7{_RST}    {_YEL}\u00b7{_RST}       {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_MAG}\u00b7{_RST}   {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}",
        f"  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_YEL}\u00b7{_RST}      {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}      {_YEL}\u00b7{_RST}        {_MAG}\u00b7{_RST}      {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}      {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}   {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}",
        f"  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST} {_YEL}\u2605{_RST} {_MAG}\u00b7{_RST}",
        f"  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}  {_GRN}~{_RST}",
    ))

    return Animation(
        name="garden",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    fill = (
        f"{_GRN}\u2022{_RST}",
        f"{_YEL}\u2605{_RST}",
        f"{_MAG}\u2666{_RST}",
        f"{_GRN}\u2605{_RST}",
        f"{_YEL}\u2022{_RST}",
        f"{_MAG}\u2022{_RST}",
    )
    sprite_a = Frame(lines=("@",))    # flower shape
    sprite_b = Frame(lines=("*",))
    completion = Frame(lines=("@!",))

    dec_a = Frame(lines=(
        "  .    .       .         .   .       .    .         .   .       .    .   .   .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))
    dec_b = Frame(lines=(
        "     .      .         .   .      .        .     .      .         .   .   .   .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))
    dec_done = Frame(lines=(
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))

    return Animation(
        name="garden",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("*", ".", "~", "o", "*", ".")
    sprite_a = Frame(lines=("@",))
    sprite_b = Frame(lines=("@",))
    completion = Frame(lines=("@!",))

    dec_a = Frame(lines=(
        "  .    .       .         .   .       .    .         .   .       .    .   .   .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))
    dec_b = Frame(lines=(
        "     .      .         .   .      .        .     .      .         .   .   .   .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))
    dec_done = Frame(lines=(
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
        "  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~  ~",
    ))

    return Animation(
        name="garden",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("garden", _create)
