"""train theme -- Steam engine chugging along railroad tracks.

A locomotive chugs forward with steam billowing above and track
texture below, filling the bar with railroad-colored blocks.

Rendering tiers:
- emoji: Dark ANSI railroad fill, locomotive emoji, steam/track decoration
- unicode: Same fill, "[TTT]" / "[===]" sprites, steam and track decoration
- ascii: "=" and "-" fill, "[TTT]" sprite, "." and "o" steam decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_DRK = "\033[90m"   # dark gray (rail ties)
_BRN = "\033[33m"   # yellow/brown (wooden ties)
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Railroad fill: alternating dark/brown blocks for ties and rails
    fill = (
        f"{_DRK}\u2588{_RST}",   # dark gray full block
        f"{_BRN}\u2588{_RST}",   # brown full block
        f"{_DRK}\u2593{_RST}",   # dark gray dark shade
        f"{_BRN}\u2588{_RST}",   # brown full block
        f"{_DRK}\u2588{_RST}",   # dark gray full block
        f"{_BRN}\u2592{_RST}",   # brown medium shade
    )
    # Locomotive emoji is 2 cols; both frames identical for consistent width
    sprite_a = Frame(lines=("\U0001f682",))    # locomotive (2 cols)
    sprite_b = Frame(lines=("\U0001f682",))
    completion = Frame(lines=("\U0001f682\u2605",))   # locomotive + star

    # Decoration: steam puffs above, track texture below
    dec_a = Frame(lines=(
        f"  {_DRK}.{_RST} \u00b0      {_DRK}\u2022{_RST}        \u00b0  {_DRK}.{_RST}",
        f"  {_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-{_BRN}={_RST}-+",
    ))
    dec_b = Frame(lines=(
        f"     \u00b0  {_DRK}.{_RST}        {_DRK}\u2022{_RST}  \u00b0  {_DRK}.{_RST}    \u00b0",
        f"  {_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}={_BRN}-{_RST}=+",
    ))
    dec_done = Frame(lines=(
        f"  \u2605 \u00b0 \u2605   \u00b0 \u2605   \u00b0 \u2605   \u00b0 \u2605   \u00b0 \u2605",
        f"  {_BRN}={_RST}-{_BRN}={_RST}-+={_BRN}-{_RST}={_BRN}-{_RST}+={_BRN}-{_RST}={_BRN}-{_RST}+={_BRN}-{_RST}+",
    ))

    return Animation(
        name="train",
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
        f"{_DRK}\u2588{_RST}",
        f"{_BRN}\u2588{_RST}",
        f"{_DRK}\u2593{_RST}",
        f"{_BRN}\u2588{_RST}",
        f"{_DRK}\u2588{_RST}",
        f"{_BRN}\u2592{_RST}",
    )
    # Both sprites 5 cols for consistent width
    sprite_a = Frame(lines=("[TTT]",))
    sprite_b = Frame(lines=("[===]",))
    completion = Frame(lines=("[TTT]*",))

    dec_a = Frame(lines=(
        "  . o      .        o  .",
        "  =-=-=-=-=-=-=-=-=-=+",
    ))
    dec_b = Frame(lines=(
        "     o  .        .  o  .    o",
        "  -=-=-=-=-=-=-=-=-=-=-=+",
    ))
    dec_done = Frame(lines=(
        "  * o * o * o * o * o *",
        "  =-+=-+=-+=-+=-+=-+=+",
    ))

    return Animation(
        name="train",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("=", "-", "=", "-")
    sprite_a = Frame(lines=("[TTT]",))
    sprite_b = Frame(lines=("[TTT]",))
    completion = Frame(lines=("[TTT]*",))

    dec_a = Frame(lines=(
        "  . o      .        o  .",
        "  =-=-=-=-=-=-=-=-=-=+",
    ))
    dec_b = Frame(lines=(
        "     o  .        .  o  .    o",
        "  -=-=-=-=-=-=-=-=-=-=-=+",
    ))
    dec_done = Frame(lines=(
        "  * o * o * o * o * o *",
        "  =-+=-+=-+=-+=-+=-+=+",
    ))

    return Animation(
        name="train",
        frames=(sprite_a, sprite_b),
        fps=4.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("train", _create)
