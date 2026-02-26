"""fire theme -- Fire spreading across the progress bar.

Fire emoji blazes across red/orange ANSI-colored blocks with smoke
and flame particles flickering above and below the bar.

Rendering tiers:
- emoji: Red/orange/yellow ANSI flame blocks, fire emoji, smoke/flame decoration
- unicode: Red/orange ANSI blocks, kaomoji sprites, ~ and . decoration
- ascii: "#" fill, "^" sprite, simple "." and "~" decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
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
    # Flickering flame fill: red/yellow/dark-shade cycle for dynamic fire feel
    fill = (
        f"{_RED}\u2588{_RST}",   # red full block
        f"{_YEL}\u2588{_RST}",   # yellow full block
        f"{_RED}\u2593{_RST}",   # red dark shade
        f"{_YEL}\u2588{_RST}",   # yellow full block
        f"{_YEL}\u2593{_RST}",   # yellow dark shade
        f"{_RED}\u2588{_RST}",   # red full block
    )
    sprite_a = Frame(lines=("\U0001f525",))    # fire emoji
    sprite_b = Frame(lines=("\U0001f525",))
    completion = Frame(lines=("\U0001f525\u2728",))   # fire + sparkles

    # Decoration: smoke/flame particles flickering above and below
    dec_a = Frame(lines=(
        f"  {_YEL}~{_RST}    {_RED}.{_RST}       {_YEL}~{_RST}         {_RED}.{_RST}   {_YEL}~{_RST}",
        f"  {_RED}.{_RST}        {_YEL}~{_RST}     {_RED}.{_RST}           {_YEL}.{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_RED}.{_RST}      {_YEL}~{_RST}         {_RED}.{_RST}   {_YEL}~{_RST}      {_RED}.{_RST}",
        f"{_YEL}~{_RST}        {_RED}.{_RST}     {_YEL}~{_RST}        {_RED}.{_RST}        {_YEL}~{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_YEL}~{_RST} {_RED}.{_RST} {_YEL}~{_RST}   {_RED}.{_RST} {_YEL}~{_RST}   {_RED}.{_RST} {_YEL}~{_RST}   {_RED}.{_RST} {_YEL}~{_RST}   {_RED}.{_RST} {_YEL}~{_RST}",
        f"  {_RED}.{_RST} {_YEL}~{_RST} {_RED}.{_RST}   {_YEL}~{_RST} {_RED}.{_RST}   {_YEL}~{_RST} {_RED}.{_RST}   {_YEL}~{_RST} {_RED}.{_RST}   {_YEL}~{_RST} {_RED}.{_RST}",
    ))

    return Animation(
        name="fire",
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
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2593{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_YEL}\u2593{_RST}",
        f"{_RED}\u2588{_RST}",
    )
    sprite_a = Frame(lines=("^v^",))
    sprite_b = Frame(lines=("/v\\",))
    completion = Frame(lines=("^v^\u2728",))

    dec_a = Frame(lines=(
        "  ~    .       ~         .   ~",
        "  .        ~     .           .",
    ))
    dec_b = Frame(lines=(
        "     .      ~         .   ~      .",
        "~        .     ~        .        ~",
    ))
    dec_done = Frame(lines=(
        "  ~ . ~   . ~   . ~   . ~   . ~",
        "  . ~ .   ~ .   ~ .   ~ .   ~ .",
    ))

    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("#",)
    sprite_a = Frame(lines=("^",))
    sprite_b = Frame(lines=("^",))
    completion = Frame(lines=("^*^",))

    dec_a = Frame(lines=(
        "  ~    .       ~         .   ~",
        "  .        ~     .           .",
    ))
    dec_b = Frame(lines=(
        "     .      ~         .   ~      .",
        "~        .     ~        .        ~",
    ))
    dec_done = Frame(lines=(
        "  ~ . ~   . ~   . ~   . ~   . ~",
        "  . ~ .   ~ .   ~ .   ~ .   ~ .",
    ))

    return Animation(
        name="fire",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("fire", _create)
