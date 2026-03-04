"""bear theme -- Cute bear face walks across the bar.

The ʕ•ᴥ•ʔ bear blinks as it walks. At completion it shows love.

Rendering tiers:
- emoji: Bullet fill, bear with IPA/phonetic chars
- unicode: Same
- ascii: Dot fill, "(ouo)" face
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    fill = ("\u2022",)   # bullet
    sprites = (
        Frame(lines=("\u0295\u2022\u1d25\u2022\u0294",)),   # ʕ•ᴥ•ʔ
        Frame(lines=("\u0295\u00b0\u1d25\u00b0\u0294",)),   # ʕ°ᴥ°ʔ
    )
    completion = Frame(lines=("\u0295\u2022\u1d25\u2022\u0294\u2661",))  # ʕ•ᴥ•ʔ♡
    return Animation(
        name="bear",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _unicode() -> Animation:
    fill = ("\u2022",)
    sprites = (
        Frame(lines=("\u0295\u2022\u1d25\u2022\u0294",)),
        Frame(lines=("\u0295\u00b0\u1d25\u00b0\u0294",)),
    )
    completion = Frame(lines=("\u0295\u2022\u1d25\u2022\u0294\u2661",))
    return Animation(
        name="bear",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


def _ascii() -> Animation:
    fill = ("o",)
    sprites = (
        Frame(lines=("(ouo)",)),
        Frame(lines=("(ovo)",)),
    )
    completion = Frame(lines=("(ouo)<3",))
    return Animation(
        name="bear",
        frames=sprites,
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
    )


register_theme("bear", _create)
