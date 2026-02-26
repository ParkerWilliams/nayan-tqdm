"""disco theme -- Disco ball with glittery sparkle fill.

A mirror ball sweeps across a glittering floor of magenta/cyan/white
sparkle and diamond symbols -- visually distinct from nyan's solid
rainbow blocks.  At completion, the disco ball and music note celebrate.

Rendering tiers:
- emoji: Sparkle/diamond glitter fill, mirror ball emoji, ball + music note
- unicode: Sparkle/diamond glitter fill, "(o)" / "(O)" sprite, "(O)!" completion
- ascii: Glittery "*./+" fill, "(o)" / "(O)" sprite, "(O)!" completion
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_MAG = "\033[35m"
_CYN = "\033[36m"
_WHT = "\033[97m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Sparkle/diamond characters in magenta/cyan/white -- creates disco-ball
    # glitter effect.  Distinct from nyan's solid full-block rainbow.
    # Each character is 1 display col (verified: ✳ ♦ ★ • all width 1).
    fill = (
        f"{_MAG}\u2733{_RST}",   # eight-spoked asterisk (magenta)
        f"{_CYN}\u2666{_RST}",   # diamond (cyan)
        f"{_WHT}\u2605{_RST}",   # star (white/bright)
        f"{_MAG}\u2022{_RST}",   # bullet (magenta)
        f"{_CYN}\u2733{_RST}",   # eight-spoked asterisk (cyan)
        f"{_WHT}\u2666{_RST}",   # diamond (white/bright)
    )
    # Mirror ball emoji -- 2 display cols, same for both frames
    sprite_a = Frame(lines=("\U0001faa9",))
    sprite_b = Frame(lines=("\U0001faa9",))
    # Mirror ball + music note at completion
    completion = Frame(lines=("\U0001faa9\U0001f3b5",))
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = (
        f"{_MAG}\u2733{_RST}",
        f"{_CYN}\u2666{_RST}",
        f"{_WHT}\u2605{_RST}",
        f"{_MAG}\u2022{_RST}",
        f"{_CYN}\u2733{_RST}",
        f"{_WHT}\u2666{_RST}",
    )
    sprite_a = Frame(lines=("(o)",))
    sprite_b = Frame(lines=("(O)",))
    completion = Frame(lines=("(O)!",))
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    # Glittery ASCII pattern
    fill = ("*", ".", "+", ".", "*", ".")
    sprite_a = Frame(lines=("(o)",))
    sprite_b = Frame(lines=("(O)",))
    completion = Frame(lines=("(O)!",))
    return Animation(
        name="disco",
        frames=(sprite_a, sprite_b),
        fps=6.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("disco", _create)
