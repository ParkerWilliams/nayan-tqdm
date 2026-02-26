"""duck_bread theme -- Duck chasing a piece of bread.

A duck waddles after a bread slice across a water-ripple trail.
Water ripples drift above and breadcrumbs appear below.

Rendering tiers:
- emoji: Cyan/yellow water fill, duck+bread compound sprite, ripple decoration
- unicode: ANSI-colored fill, text-art duck chasing bread crumb, ripple decoration
- ascii: Tilde/dot fill, text-art duck chasing crumb, ripple/crumb decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

# ANSI color codes
_CYN = "\033[36m"   # cyan (water ripples)
_YEL = "\033[33m"   # yellow (bread crumbs)
_BLU = "\033[34m"   # blue (water)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Breadcrumb/water fill: cyan/yellow/blue unicode chars -- all 1 display col
    fill = (
        f"{_CYN}~{_RST}",       # cyan tilde (water ripple)
        f"{_YEL}\u2022{_RST}",  # yellow bullet (breadcrumb)
        f"{_BLU}\u00b7{_RST}",  # blue middle-dot (water drop)
        f"{_CYN}\u2022{_RST}",  # cyan bullet (ripple)
        f"{_YEL}\u00b7{_RST}",  # yellow middle-dot (crumb)
        f"{_BLU}~{_RST}",       # blue tilde (water)
    )
    # Chase mechanic: duck(2) + space(1) + bread(2) = 5 cols; duck(2) + bread(2) + space(1) = 5 cols
    sprite_a = Frame(lines=("\U0001f986 \U0001f35e",))   # duck space bread (5 cols)
    sprite_b = Frame(lines=("\U0001f986\U0001f35e ",))   # duck bread space (5 cols)
    completion = Frame(lines=("\U0001f986\u2605",))      # duck + star (3 cols)

    # Decoration: water ripples above, breadcrumbs below
    dec_a = Frame(lines=(
        f"  {_CYN}~{_RST}    {_CYN}~{_RST}       {_CYN}~{_RST}         {_CYN}~{_RST}   {_CYN}~{_RST}",
        f"  {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST}   {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST}   {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST}",
    ))
    dec_b = Frame(lines=(
        f"     {_CYN}~{_RST}      {_BLU}~{_RST}         {_CYN}~{_RST}   {_BLU}~{_RST}      {_CYN}~{_RST}",
        f"  {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST}   {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST}   {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_CYN}~{_RST} {_BLU}~{_RST} {_CYN}~{_RST}   {_BLU}~{_RST} {_CYN}~{_RST}   {_BLU}~{_RST} {_CYN}~{_RST}   {_BLU}~{_RST} {_CYN}~{_RST}",
        f"  {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST} {_CYN}\u00b7{_RST} {_YEL}\u00b7{_RST}",
    ))

    return Animation(
        name="duck_bread",
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
        f"{_CYN}~{_RST}",
        f"{_YEL}\u2022{_RST}",
        f"{_BLU}\u00b7{_RST}",
        f"{_CYN}\u2022{_RST}",
        f"{_YEL}\u00b7{_RST}",
        f"{_BLU}~{_RST}",
    )
    # Both frames 4 cols for consistent display_width
    sprite_a = Frame(lines=("=< o",))   # duck face chasing bread crumb (4 cols)
    sprite_b = Frame(lines=("=<o ",))   # duck face catching crumb (4 cols)
    completion = Frame(lines=("=<o!",))  # caught with celebration (4 cols)

    dec_a = Frame(lines=(
        "  ~    ~       ~         ~   ~",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     ~      ~         ~   ~      ~",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~",
        "  . ~ . ~ . ~ . ~ . ~ .",
    ))

    return Animation(
        name="duck_bread",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("~", ".", "~", ".")
    sprite_a = Frame(lines=("=< o",))
    sprite_b = Frame(lines=("=<o ",))
    completion = Frame(lines=("=<o!",))

    dec_a = Frame(lines=(
        "  ~    ~       ~         ~   ~",
        "  . ~ .   ~ .   ~ .   ~ .",
    ))
    dec_b = Frame(lines=(
        "     ~      ~         ~   ~      ~",
        "  ~ . ~   . ~   . ~   . ~",
    ))
    dec_done = Frame(lines=(
        "  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~",
        "  . ~ . ~ . ~ . ~ . ~ .",
    ))

    return Animation(
        name="duck_bread",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("duck_bread", _create)
