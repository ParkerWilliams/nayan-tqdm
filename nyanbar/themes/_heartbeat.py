"""heartbeat theme -- Heart pulse with heart-character fill and pulse decoration.

Heart unicode characters fill the bar in alternating magenta/red ANSI
colors, with a heartbeat pulse line flickering above and small hearts below.

Rendering tiers:
- emoji: Heart unicode fill (magenta/red ANSI), heart sprites, pulse decoration
- unicode: Same fill, "<3" sprite, heartbeat line decoration
- ascii: "<" and "3" alternating fill, "<3" sprite, "-" and "^" decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_RED = "\033[31m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Heart fill: alternating solid/outline hearts in magenta/red ANSI
    # U+2661 = white heart (outline), U+2665 = black heart suit -- both 1 col
    fill = (
        f"{_MAG}\u2665{_RST}",   # magenta solid heart
        f"{_RED}\u2665{_RST}",   # red solid heart
        f"{_MAG}\u2661{_RST}",   # magenta white heart
        f"{_RED}\u2665{_RST}",   # red solid heart
        f"{_MAG}\u2665{_RST}",   # magenta solid heart
        f"{_RED}\u2661{_RST}",   # red white heart
    )
    # Use heart suit (1 col) for sprite -- consistent 1-col frames
    sprite_a = Frame(lines=(f"{_MAG}\u2665{_RST}",))
    sprite_b = Frame(lines=(f"{_RED}\u2665{_RST}",))
    completion = Frame(lines=(f"{_MAG}\u2665{_RST}\u2728",))  # heart + sparkles

    # Decoration: heartbeat/pulse line above, scattered hearts below
    dec_a = Frame(lines=(
        "  ~  ^  ~     ^  ~  ^     ~  ^  ~",
        f"  {_MAG}\u2661{_RST}         {_RED}\u2661{_RST}          {_MAG}\u2661{_RST}",
    ))
    dec_b = Frame(lines=(
        "    ^  ~  ^     ~  ^  ~     ^  ~",
        f"     {_RED}\u2661{_RST}          {_MAG}\u2661{_RST}         {_RED}\u2661{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  {_MAG}\u2665{_RST} {_RED}\u2661{_RST} {_MAG}\u2665{_RST}   {_RED}\u2665{_RST} {_MAG}\u2661{_RST}   {_RED}\u2665{_RST} {_MAG}\u2665{_RST}   {_RED}\u2661{_RST} {_MAG}\u2665{_RST}",
        f"  {_RED}\u2661{_RST} {_MAG}\u2665{_RST} {_RED}\u2661{_RST}   {_MAG}\u2661{_RST} {_RED}\u2665{_RST}   {_MAG}\u2661{_RST} {_RED}\u2661{_RST}   {_MAG}\u2665{_RST} {_RED}\u2661{_RST}",
    ))

    return Animation(
        name="heartbeat",
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
        f"{_MAG}\u2665{_RST}",
        f"{_RED}\u2665{_RST}",
        f"{_MAG}\u2661{_RST}",
        f"{_RED}\u2665{_RST}",
        f"{_MAG}\u2665{_RST}",
        f"{_RED}\u2661{_RST}",
    )
    sprite_a = Frame(lines=("<3",))
    sprite_b = Frame(lines=("<3",))
    completion = Frame(lines=("<3!",))

    dec_a = Frame(lines=(
        "  ~  ^  ~     ^  ~  ^     ~  ^  ~",
        "  \u2661         \u2661          \u2661",
    ))
    dec_b = Frame(lines=(
        "    ^  ~  ^     ~  ^  ~     ^  ~",
        "     \u2661          \u2661         \u2661",
    ))
    dec_done = Frame(lines=(
        "  \u2665 \u2661 \u2665   \u2665 \u2661   \u2665 \u2665   \u2661 \u2665",
        "  \u2661 \u2665 \u2661   \u2661 \u2665   \u2661 \u2661   \u2665 \u2661",
    ))

    return Animation(
        name="heartbeat",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    # Fill that reads as partial hearts: alternating < and 3
    fill = ("<", "3", "<", "3", "<", "3")
    sprite_a = Frame(lines=("<3",))
    sprite_b = Frame(lines=("<3",))
    completion = Frame(lines=("<3!",))

    dec_a = Frame(lines=(
        "  -  ^  -     ^  -  ^     -  ^  -",
        "  .         .          .",
    ))
    dec_b = Frame(lines=(
        "    ^  -  ^     -  ^  -     ^  -",
        "     .          .         .",
    ))
    dec_done = Frame(lines=(
        "  ^ - ^   ^ -   ^ ^   - ^",
        "  - ^ -   - ^   - -   ^ -",
    ))

    return Animation(
        name="heartbeat",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("heartbeat", _create)
