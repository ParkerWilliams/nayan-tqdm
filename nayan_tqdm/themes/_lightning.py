"""lightning theme -- Electric bolt charging across the bar.

Electric crackle fills the bar in blue/cyan/white ANSI colors, with
sparks crackling above and a ground strike below. The lightning bolt
(U+26A1, 2-col) leads the charge.

Rendering tiers:
- emoji: Blue/cyan/white ANSI electric fill, lightning sprite, spark decoration
- unicode: Same fill, "/>" / "/>" sprites, "." and "*" spark decoration
- ascii: "#" and "=" fill, "/>" sprite, "." and "*" decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_CYN = "\033[36m"   # cyan (electric arc)
_BLU = "\033[34m"   # blue (charge)
_WHT = "\033[37m"   # white (bright flash)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Electric crackle fill: blue/cyan/white blocks and shades
    fill = (
        f"{_CYN}\u2588{_RST}",   # cyan full block
        f"{_BLU}\u2588{_RST}",   # blue full block
        f"{_WHT}\u2588{_RST}",   # white full block
        f"{_CYN}\u2593{_RST}",   # cyan dark shade
        f"{_BLU}\u2588{_RST}",   # blue full block
        f"{_WHT}\u2592{_RST}",   # white medium shade
    )
    # U+26A1 = high voltage (2 cols)
    sprite_a = Frame(lines=(f"{_WHT}\u26a1{_RST}",))
    sprite_b = Frame(lines=(f"{_CYN}\u26a1{_RST}",))
    completion = Frame(lines=(f"{_WHT}\u26a1{_RST}",))

    # Decoration: electric sparks above, ground strike below
    dec_a = Frame(lines=(
        f"  {_WHT}\u00b7{_RST}    {_CYN}\u2022{_RST}       {_WHT}\u00b7{_RST}         {_CYN}\u2022{_RST}   {_WHT}\u00b7{_RST}       {_CYN}\u2022{_RST}    {_WHT}\u00b7{_RST}         {_CYN}\u2022{_RST}   {_WHT}\u00b7{_RST}       {_CYN}\u2022{_RST}    {_WHT}\u00b7{_RST}   {_CYN}\u2022{_RST}   {_WHT}\u00b7{_RST}",
        f"  {_CYN}\u2022{_RST}        {_WHT}\u00b7{_RST}     {_CYN}\u2022{_RST}           {_WHT}\u00b7{_RST}        {_CYN}\u2022{_RST}     {_WHT}\u00b7{_RST}           {_CYN}\u2022{_RST}        {_WHT}\u00b7{_RST}     {_CYN}\u2022{_RST}  {_WHT}\u00b7{_RST}  {_CYN}\u2022{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_CYN}\u2022{_RST}      {_WHT}\u00b7{_RST}         {_CYN}\u2022{_RST}   {_WHT}\u00b7{_RST}      {_CYN}\u2022{_RST}       {_WHT}\u00b7{_RST}   {_CYN}\u2022{_RST}      {_WHT}\u00b7{_RST}         {_CYN}\u2022{_RST}      {_WHT}\u00b7{_RST}   {_CYN}\u2022{_RST}   {_WHT}\u00b7{_RST}",
        f"{_WHT}\u00b7{_RST}        {_CYN}\u2022{_RST}     {_WHT}\u00b7{_RST}        {_CYN}\u2022{_RST}        {_WHT}\u00b7{_RST}     {_CYN}\u2022{_RST}        {_WHT}\u00b7{_RST}        {_CYN}\u2022{_RST}     {_WHT}\u00b7{_RST}        {_CYN}\u2022{_RST}  {_WHT}\u00b7{_RST}  {_CYN}\u2022{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST}",
        f"  {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST} {_WHT}\u00b7{_RST} {_CYN}\u2022{_RST}",
    ))

    return Animation(
        name="lightning",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _unicode() -> Animation:
    fill = (
        f"{_CYN}\u2588{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_WHT}\u2588{_RST}",
        f"{_CYN}\u2593{_RST}",
        f"{_BLU}\u2588{_RST}",
        f"{_WHT}\u2592{_RST}",
    )
    # "/>" is 2 cols -- consistent
    sprite_a = Frame(lines=("/>",))
    sprite_b = Frame(lines=("/>",))
    completion = Frame(lines=("/>!",))

    dec_a = Frame(lines=(
        "  .    *       .         *   .       *    .         *   .       *    .   *   .",
        "  *        .     *           .        *     .           *        .     *  .  .",
    ))
    dec_b = Frame(lines=(
        "     *      .         *   .      *       .   *      .         *      .   *   .",
        ".        *     .        *        .     *        .        *     .        *  .  .",
    ))
    dec_done = Frame(lines=(
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . *",
        "  * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
    ))

    return Animation(
        name="lightning",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("#", "=", "#", "=")
    sprite_a = Frame(lines=("/>",))
    sprite_b = Frame(lines=("/>",))
    completion = Frame(lines=("/>!",))

    dec_a = Frame(lines=(
        "  .    *       .         *   .       *    .         *   .       *    .   *   .",
        "  *        .     *           .        *     .           *        .     *  .  .",
    ))
    dec_b = Frame(lines=(
        "     *      .         *   .      *       .   *      .         *      .   *   .",
        ".        *     .        *        .     *        .        *     .        *  .  .",
    ))
    dec_done = Frame(lines=(
        "  . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . *",
        "  * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * . * .",
    ))

    return Animation(
        name="lightning",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("lightning", _create)
