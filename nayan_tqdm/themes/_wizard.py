"""wizard theme -- Wizard leaving a colorful magical symbol trail.

A wizard emoji glides forward, leaving a trail of 10+ colorful magical
symbols: stars, sparkles, diamonds, snowflakes, comets, and more.
Twinkling magical sparkles float above and below the bar.

Rendering tiers:
- emoji: 10+ colorful magical symbol fill, wizard emoji, sparkle decoration
- unicode: Same fill, "*>" / "~>" sprite, "*" and "." decoration
- ascii: Expanded magical ASCII fill, "*>" / "~>" sprite, "*" and "." decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_CYN = "\033[36m"
_BLU = "\033[34m"
_YEL = "\033[33m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # 10 diverse 1-col magical symbols in varied ANSI colors
    fill = (
        f"{_MAG}\u2605{_RST}",   # black star (magenta)
        f"{_CYN}\u2733{_RST}",   # eight-spoked asterisk (cyan)
        f"{_BLU}\u2666{_RST}",   # diamond (blue)
        f"{_MAG}\u2606{_RST}",   # white star (magenta)
        f"{_CYN}\u2744{_RST}",   # snowflake (cyan)
        f"{_BLU}\u2604{_RST}",   # comet (blue)
        f"{_YEL}\u2721{_RST}",   # star of david (yellow) -- 1 col
        f"{_MAG}\u2234{_RST}",   # therefore (magenta) -- 1 col
        f"{_CYN}\u2302{_RST}",   # house/hat (cyan) -- 1 col, whimsical
        f"{_BLU}\u2726{_RST}",   # black four-pointed star (blue) -- 1 col
    )
    sprite_a = Frame(lines=("\U0001f9d9",))    # wizard emoji (2 cols)
    sprite_b = Frame(lines=("\U0001f9d9",))
    completion = Frame(lines=("\U0001f9d9\u2728",))   # wizard + sparkles

    # Decoration: floating sparkles above and below, twinkling
    dec_a = Frame(lines=(
        f"   {_MAG}\u2726{_RST}       {_CYN}\u2605{_RST}           {_BLU}\u00b7{_RST}       {_MAG}\u2726{_RST}       {_CYN}\u2605{_RST}    {_BLU}\u00b7{_RST}       {_MAG}\u2726{_RST}   {_CYN}\u2605{_RST}        {_BLU}\u00b7{_RST}    {_MAG}\u2726{_RST}",
        f"  {_CYN}\u2605{_RST}    {_BLU}\u00b7{_RST}              {_MAG}\u2605{_RST}              {_CYN}\u2726{_RST}              {_MAG}\u2605{_RST}   {_CYN}\u2726{_RST}   {_BLU}\u00b7{_RST}       {_MAG}\u2605{_RST}    {_CYN}\u2726{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_CYN}\u2605{_RST}          {_MAG}\u2726{_RST}         {_BLU}\u2605{_RST}               {_CYN}\u00b7{_RST}       {_MAG}\u2726{_RST}   {_CYN}\u2605{_RST}   {_BLU}\u2726{_RST}      {_MAG}\u00b7{_RST}    {_CYN}\u2605{_RST}",
        f"{_MAG}\u2726{_RST}         {_CYN}\u2605{_RST}         {_BLU}\u2726{_RST}            {_MAG}\u2605{_RST}         {_CYN}\u2726{_RST}    {_BLU}\u2605{_RST}   {_MAG}\u2726{_RST}   {_CYN}\u2605{_RST}        {_BLU}\u00b7{_RST}    {_MAG}\u2726{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST}",
        f"  {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST} {_BLU}\u2605{_RST} {_MAG}\u2726{_RST} {_CYN}\u2605{_RST} {_BLU}\u2726{_RST} {_MAG}\u2605{_RST} {_CYN}\u2726{_RST}",
    ))

    return Animation(
        name="wizard",
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
        f"{_MAG}\u2605{_RST}",
        f"{_CYN}\u2733{_RST}",
        f"{_BLU}\u2666{_RST}",
        f"{_MAG}\u2606{_RST}",
        f"{_CYN}\u2744{_RST}",
        f"{_BLU}\u2604{_RST}",
        f"{_YEL}\u2721{_RST}",
        f"{_MAG}\u2234{_RST}",
        f"{_CYN}\u2302{_RST}",
        f"{_BLU}\u2726{_RST}",
    )
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))

    dec_a = Frame(lines=(
        "   *       .           \u00b7       *       .    \u00b7       *       .    *   \u00b7   *",
        "  .    \u00b7              .              *              .    \u00b7         *  .   *",
    ))
    dec_b = Frame(lines=(
        "     .          *         .               \u00b7       *          .       \u00b7  .  *",
        "*         .         *            .         *         .    *         .  *   .",
    ))
    dec_done = Frame(lines=(
        "  * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . *",
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
    ))

    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    # Expanded 10-char variety of magical-ish ASCII characters
    fill = ("*", "~", "+", ".", "^", "~", "*", "+", ".", "~")
    sprite_a = Frame(lines=("*>",))
    sprite_b = Frame(lines=("~>",))
    completion = Frame(lines=("*>*",))

    dec_a = Frame(lines=(
        "   *       .                    *                    .       *   .       *   .",
        "  .    *              .              *              .    *         .   *   .  .",
    ))
    dec_b = Frame(lines=(
        "     .          *         .               *         .          *       .  *  .",
        "*         .         *            .         *         .    *         .  *   .  .",
    ))
    dec_done = Frame(lines=(
        "  * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . *",
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
    ))

    return Animation(
        name="wizard",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("wizard", _create)
