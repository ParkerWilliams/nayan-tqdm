"""cat_yarn theme -- Cat chasing a ball of yarn.

A cat sprints across the bar chasing a yarn ball, leaving a colorful
yarn-strand trail. Yarn balls drift above and paw prints appear below.

Rendering tiers:
- emoji: Colored yarn-strand fill, cat+yarn compound sprite, paw decoration
- unicode: ANSI-colored fill, text-art cat chasing yarn-o, paw decoration
- ascii: Tilde/dash fill, text-art cat chasing yarn-o, dot/tilde decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_MAG = "\033[35m"   # magenta (yarn strands)
_YEL = "\033[33m"   # yellow (yarn strands)
_RED = "\033[31m"   # red (yarn)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Yarn-colored fill: magenta/yellow/red unicode chars -- all 1 display col
    fill = (
        f"{_MAG}\u2022{_RST}",   # magenta bullet (yarn strand)
        f"{_YEL}\u25c6{_RST}",   # yellow diamond (yarn knot)
        f"{_RED}\u2022{_RST}",   # red bullet (yarn strand)
        f"{_MAG}\u25c6{_RST}",   # magenta diamond (yarn knot)
        f"{_YEL}\u2022{_RST}",   # yellow bullet (yarn strand)
        f"{_RED}\u25c6{_RST}",   # red diamond (yarn knot)
    )
    # Chase mechanic: cat(2) + space(1) + yarn(2) = 5 cols; cat(2) + yarn(2) + space(1) = 5 cols
    sprite_a = Frame(lines=("\U0001f431 \U0001f9f6",))   # cat space yarn (5 cols)
    sprite_b = Frame(lines=("\U0001f431\U0001f9f6 ",))   # cat yarn space (5 cols)
    completion = Frame(lines=("\U0001f63b\U0001f9f6",))  # heart-eyes cat + yarn (4 cols)

    # Decoration: yarn balls above, paw prints below
    dec_a = Frame(lines=(
        f"  {_MAG}\u00b7{_RST}    {_YEL}\u00b7{_RST}       {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}       {_YEL}\u00b7{_RST}    {_MAG}\u00b7{_RST}",
        f"  {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_YEL}\u00b7{_RST}      {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}      {_YEL}\u00b7{_RST}        {_MAG}\u00b7{_RST}   {_YEL}\u00b7{_RST}      {_MAG}\u00b7{_RST}         {_YEL}\u00b7{_RST}   {_MAG}\u00b7{_RST}",
        f"  {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST} {_MAG}~{_RST} {_YEL}\u00b7{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST} {_YEL}\u00b7{_RST} {_MAG}\u00b7{_RST}",
        f"  {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST} {_YEL}~{_RST} {_MAG}~{_RST}",
    ))

    return Animation(
        name="cat_yarn",
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
        f"{_MAG}\u2022{_RST}",
        f"{_YEL}\u25c6{_RST}",
        f"{_RED}\u2022{_RST}",
        f"{_MAG}\u25c6{_RST}",
        f"{_YEL}\u2022{_RST}",
        f"{_RED}\u25c6{_RST}",
    )
    # Both frames 6 cols for consistent display_width
    sprite_a = Frame(lines=(">^.^ o",))   # cat face chasing yarn ball (6 cols)
    sprite_b = Frame(lines=(">^.^o ",))   # cat face catching yarn ball (6 cols)
    completion = Frame(lines=(">^.^o!",))  # caught with celebration (6 cols)

    dec_a = Frame(lines=(
        "  .    .       .         .   .       .    .         .   .       .    .   .   .",
        "  ~ . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~  .",
    ))
    dec_b = Frame(lines=(
        "     .      .         .   .      .        .   .      .       .  .      .  .   .",
        "  . ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .  ~",
    ))
    dec_done = Frame(lines=(
        "  . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o .",
        "  ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_yarn",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("~", "-", "~", "-")
    sprite_a = Frame(lines=(">^.^ o",))
    sprite_b = Frame(lines=(">^.^o ",))
    completion = Frame(lines=(">^.^o!",))

    dec_a = Frame(lines=(
        "  .    .       .         .   .       .    .         .   .       .    .   .   .",
        "  ~ . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~   . ~  .",
    ))
    dec_b = Frame(lines=(
        "     .      .         .   .      .        .   .      .       .  .      .  .   .",
        "  . ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .   ~ .  ~",
    ))
    dec_done = Frame(lines=(
        "  . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o .",
        "  ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~ . ~",
    ))

    return Animation(
        name="cat_yarn",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("cat_yarn", _create)
