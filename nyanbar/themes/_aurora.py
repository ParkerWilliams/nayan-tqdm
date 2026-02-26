"""aurora theme -- Northern lights shimmering across the sky.

Aurora color waves sweep across the bar in green/cyan/magenta/blue ANSI
blocks. Shimmering light wisps float above, dark sky dots glow below.

Rendering tiers:
- emoji: Green/cyan/blue/magenta ANSI aurora fill, star sprite, shimmer decoration
- unicode: Same fill, "*" sprite, "." and "*" decoration
- ascii: "#" "=" "~" fill, "*" sprite, "." and "~" decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_GRN = "\033[32m"   # green (lower aurora band)
_CYN = "\033[36m"   # cyan (middle aurora)
_BLU = "\033[34m"   # blue (upper aurora)
_MAG = "\033[35m"   # magenta (aurora edge)
_WHT = "\033[37m"   # white (star)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Aurora fill: 8-char cycle through aurora colors -- sweeping gradient
    fill = (
        f"{_GRN}\u2588{_RST}",   # green full block
        f"{_CYN}\u2588{_RST}",   # cyan full block
        f"{_BLU}\u2588{_RST}",   # blue full block
        f"{_MAG}\u2588{_RST}",   # magenta full block
        f"{_CYN}\u2588{_RST}",   # cyan full block
        f"{_GRN}\u2588{_RST}",   # green full block
        f"{_BLU}\u2588{_RST}",   # blue full block
        f"{_MAG}\u2588{_RST}",   # magenta full block
    )
    # Use U+2605 (black star, 1 col) -- reliably 1 col unlike U+2B50
    sprite_a = Frame(lines=(f"{_WHT}\u2605{_RST}",))
    sprite_b = Frame(lines=(f"{_CYN}\u2605{_RST}",))
    completion = Frame(lines=(f"{_WHT}\u2605{_RST}\u2728",))   # star + sparkles

    # Decoration: shimmering wisps above, dark sky dots below
    dec_a = Frame(lines=(
        f"  {_GRN}\u2605{_RST} {_CYN}\u00b7{_RST}       {_MAG}\u2726{_RST}         {_GRN}\u00b7{_RST}  {_CYN}\u2605{_RST}",
        f"  {_BLU}\u00b7{_RST}    {_MAG}\u00b7{_RST}              {_CYN}\u00b7{_RST}              {_GRN}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_CYN}\u00b7{_RST}     {_GRN}\u2605{_RST}      {_MAG}\u2726{_RST}         {_CYN}\u2605{_RST}          {_GRN}\u00b7{_RST}",
        f"{_MAG}\u00b7{_RST}         {_BLU}\u00b7{_RST}         {_CYN}\u00b7{_RST}            {_MAG}\u00b7{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_GRN}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST}   {_MAG}\u2726{_RST} {_GRN}\u2605{_RST}   {_CYN}\u2726{_RST} {_BLU}\u2605{_RST}   {_MAG}\u2726{_RST} {_GRN}\u2605{_RST}",
        f"  {_CYN}\u00b7{_RST} {_BLU}\u00b7{_RST} {_MAG}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_CYN}\u00b7{_RST}   {_BLU}\u00b7{_RST} {_MAG}\u00b7{_RST}   {_GRN}\u00b7{_RST} {_CYN}\u00b7{_RST}",
    ))

    return Animation(
        name="aurora",
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
        f"{_GRN}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
        f"{_CYN}\u2588{_RST}",
        f"{_GRN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_MAG}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("*",))
    sprite_b = Frame(lines=("*",))
    completion = Frame(lines=("*!",))

    dec_a = Frame(lines=(
        "  * .       *         .  *",
        "  .    .              .              .",
    ))
    dec_b = Frame(lines=(
        "     .     *      *         *          .",
        ".         .         .            .",
    ))
    dec_done = Frame(lines=(
        "  * . *   . *   . *   . *   . *",
        "  . * .   * .   * .   * .   * .",
    ))

    return Animation(
        name="aurora",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("#", "=", "~", "#", "=", "~")
    sprite_a = Frame(lines=("*",))
    sprite_b = Frame(lines=("*",))
    completion = Frame(lines=("*!",))

    dec_a = Frame(lines=(
        "  * .       *         .  *",
        "  .    ~              .              ~",
    ))
    dec_b = Frame(lines=(
        "     .     *      ~         *          .",
        "~         .         ~            .",
    ))
    dec_done = Frame(lines=(
        "  * ~ *   ~ *   ~ *   ~ *   ~ *",
        "  ~ * ~   * ~   * ~   * ~   * ~",
    ))

    return Animation(
        name="aurora",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("aurora", _create)
