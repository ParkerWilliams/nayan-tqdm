"""cat_mouse theme -- Cat chasing a mouse.

A cat sprints after a mouse, leaving paw-print trails across the bar.
Cheese crumbs drift above and mouse footprints appear below.

Rendering tiers:
- emoji: Colored paw-print fill, cat+mouse compound sprite, cheese decoration
- unicode: ANSI-colored fill, text-art cat chasing mouse @, dot decoration
- ascii: Dot/comma fill, text-art cat chasing mouse @, dot/comma decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_YEL = "\033[33m"   # yellow (cheese crumbs)
_WHT = "\033[97m"   # white (mouse fur)
_GRY = "\033[37m"   # grey (footprints)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Paw-print trail fill: yellow/white/grey unicode chars -- all 1 display col
    fill = (
        f"{_YEL}\u2022{_RST}",   # yellow bullet (cheese crumb)
        f"{_WHT}\u00b7{_RST}",   # white middle-dot (paw pad)
        f"{_GRY}\u2022{_RST}",   # grey bullet (paw print)
        f"{_YEL}\u00b7{_RST}",   # yellow middle-dot (crumb)
        f"{_WHT}\u2022{_RST}",   # white bullet (paw pad)
        f"{_GRY}\u00b7{_RST}",   # grey middle-dot (footprint)
    )
    # Chase mechanic: cat(2) + space(1) + mouse(2) = 5 cols; cat(2) + mouse(2) + space(1) = 5 cols
    sprite_a = Frame(lines=("\U0001f431 \U0001f42d",))   # cat space mouse (5 cols)
    sprite_b = Frame(lines=("\U0001f431\U0001f42d ",))   # cat mouse space (5 cols)
    completion = Frame(lines=("\U0001f63c\U0001f42d",))  # smirking cat + mouse (4 cols)

    # Decoration: cheese crumbs above, mouse footprints below
    dec_a = Frame(lines=(
        f"  {_YEL}\u00b7{_RST}    {_YEL}\u00b7{_RST}       {_YEL}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_YEL}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_YEL}\u00b7{_RST}",
        f"  {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_YEL}\u00b7{_RST}      {_YEL}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}      {_YEL}\u00b7{_RST}        {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}      {_YEL}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}   {_YEL}\u00b7{_RST}",
        f"  {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST} {_YEL}\u00b7{_RST}",
        f"  {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST} {_WHT},{_RST} {_GRY}\u00b7{_RST}",
    ))

    return Animation(
        name="cat_mouse",
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
        f"{_YEL}\u2022{_RST}",
        f"{_WHT}\u00b7{_RST}",
        f"{_GRY}\u2022{_RST}",
        f"{_YEL}\u00b7{_RST}",
        f"{_WHT}\u2022{_RST}",
        f"{_GRY}\u00b7{_RST}",
    )
    # Both frames 6 cols for consistent display_width
    sprite_a = Frame(lines=(">^.^ @",))   # cat face chasing mouse @ (6 cols)
    sprite_b = Frame(lines=(">^.^@ ",))   # cat face catching mouse @ (6 cols)
    completion = Frame(lines=(">^.^@!",))  # caught with celebration (6 cols)

    dec_a = Frame(lines=(
        "  . ,      .        ,  .      .   ,      .        ,  .      ,   .   ,  .   ,",
        "  . , .   , .   , .   , .   , .   , .   , .   , .   , .   , .   , .   , .  ,",
    ))
    dec_b = Frame(lines=(
        "     ,  .        .  ,  .    ,  .        .  ,  .    ,  .        .  ,  .  ,  .",
        "  , . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,  .",
    ))
    dec_done = Frame(lines=(
        "  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
        "  . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , .",
    ))

    return Animation(
        name="cat_mouse",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = (".", ",", ".", ",")
    sprite_a = Frame(lines=(">^.^ @",))
    sprite_b = Frame(lines=(">^.^@ ",))
    completion = Frame(lines=(">^.^@!",))

    dec_a = Frame(lines=(
        "  . ,      .        ,  .      .   ,      .        ,  .      ,   .   ,  .   ,",
        "  . , .   , .   , .   , .   , .   , .   , .   , .   , .   , .   , .   , .  ,",
    ))
    dec_b = Frame(lines=(
        "     ,  .        .  ,  .    ,  .        .  ,  .    ,  .        .  ,  .  ,  .",
        "  , . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,   . ,  .",
    ))
    dec_done = Frame(lines=(
        "  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .",
        "  . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , . , .",
    ))

    return Animation(
        name="cat_mouse",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("cat_mouse", _create)
