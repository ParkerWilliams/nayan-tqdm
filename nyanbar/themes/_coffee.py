"""coffee theme -- Coffee brewing, warm brown tones with rising steam.

A cozy coffee bar with the actual coffee emoji as sprite, steam wisps
and coffee bean alternating fill, and steam-above/bean-below decoration.

Rendering tiers:
- emoji: Real U+2615 coffee emoji (2 cols), steam/bean ANSI fill, steam decoration
- unicode: ANSI-colored "c[_]" sprite (4 cols), same steam/bean fill and decoration
- ascii: Plain "c[_]" sprite, steam "~" / "." fill, plain decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_BRN = "\033[33m"   # yellow/brown (coffee bean)
_WHT = "\033[37m"   # white (steam)
_DRK = "\033[90m"   # dark gray (espresso crema)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Steam/bean fill: white steam wisps alternating with brown coffee beans
    fill = (
        f"{_WHT}\u2022{_RST}",   # white bullet (steam wisp) -- 1 col
        f"{_BRN}\u25c6{_RST}",   # brown diamond (coffee bean) -- 1 col
        f"{_WHT}\u00b7{_RST}",   # white middle dot (steam) -- 1 col
        f"{_BRN}\u2022{_RST}",   # brown bullet (bean) -- 1 col
        f"{_WHT}\u25c6{_RST}",   # white diamond (steam) -- 1 col
        f"{_BRN}\u00b7{_RST}",   # brown middle dot (bean) -- 1 col
    )
    # Real U+2615 hot beverage emoji is 2 display cols
    sprite_a = Frame(lines=("\u2615",))    # coffee emoji (2 cols)
    sprite_b = Frame(lines=("\u2615",))    # same, animation from decoration
    completion = Frame(lines=("\u2615\u2605",))  # coffee + star (3 cols)

    # Decoration: steam rising above, coffee bean pattern below
    dec_a = Frame(lines=(
        "  ~    \u00b0       ~         \u00b0   ~       \u00b0    ~         \u00b0   ~       \u00b0    ~   \u00b0",
        "  \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))
    dec_b = Frame(lines=(
        "     \u00b0  ~        \u00b0  ~  \u00b0    ~        \u00b0  ~  \u00b0    ~        \u00b0  ~  \u00b0    ~  \u00b0",
        "  \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))
    dec_done = Frame(lines=(
        "  ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~",
        "  \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))

    return Animation(
        name="coffee",
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
        f"{_WHT}\u2022{_RST}",   # white bullet (steam wisp) -- 1 col
        f"{_BRN}\u25c6{_RST}",   # brown diamond (coffee bean) -- 1 col
        f"{_WHT}\u00b7{_RST}",   # white middle dot (steam) -- 1 col
        f"{_BRN}\u2022{_RST}",   # brown bullet (bean) -- 1 col
        f"{_WHT}\u25c6{_RST}",   # white diamond (steam) -- 1 col
        f"{_BRN}\u00b7{_RST}",   # brown middle dot (bean) -- 1 col
    )
    # ANSI-colored c[_] sprite (4 cols)
    sprite_a = Frame(lines=(f"{_BRN}c[_]{_RST}",))
    sprite_b = Frame(lines=(f"{_BRN}c[_]{_RST}",))
    completion = Frame(lines=(f"{_BRN}c[_]{_RST}*",))  # 5 cols

    dec_a = Frame(lines=(
        "  ~    \u00b0       ~         \u00b0   ~       \u00b0    ~         \u00b0   ~       \u00b0    ~   \u00b0",
        "  \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))
    dec_b = Frame(lines=(
        "     \u00b0  ~        \u00b0  ~  \u00b0    ~        \u00b0  ~  \u00b0    ~        \u00b0  ~  \u00b0    ~  \u00b0",
        "  \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))
    dec_done = Frame(lines=(
        "  ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~ \u00b0 ~",
        "  \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022 \u00b7 \u2022",
    ))

    return Animation(
        name="coffee",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("~", ".", "~", ".")  # steam wisps pattern, 1 col each
    sprite_a = Frame(lines=("c[_]",))
    sprite_b = Frame(lines=("c[_]",))
    completion = Frame(lines=("c[_]*",))

    dec_a = Frame(lines=(
        "  ~    o       ~         o   ~       o    ~         o   ~       o    ~   o   ~",
        "  . o .   o .   o .   o .   o .   o .   o .   o .   o .   o .   o .   o .  .",
    ))
    dec_b = Frame(lines=(
        "     o  ~        o  ~  o    ~        o  ~  o    ~        o  ~  o    ~  o   ~  o",
        "  o . o   . o   . o   . o   . o   . o   . o   . o   . o   . o   . o   . o  .",
    ))
    dec_done = Frame(lines=(
        "  ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~ o ~",
        "  . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o . o .",
    ))

    return Animation(
        name="coffee",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("coffee", _create)
