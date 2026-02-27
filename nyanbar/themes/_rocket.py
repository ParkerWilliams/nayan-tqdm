"""rocket theme -- Rocket with flame trail and starfield decoration.

A rocket emoji blasts across a dynamic exhaust trail, with stars and
space debris parallaxing above and exhaust particles below.

Rendering tiers:
- emoji: Dynamic exhaust fill (red/yellow ANSI shades), rocket emoji, starfield decoration
- unicode: Same fill, "|=>" / "]=>" sprites, "*" and "." space decoration
- ascii: "~" and "=" fill, "=>" sprite, "*" and "." decoration
"""
from __future__ import annotations

from ..models import Animation, AnimationMode, Frame
from ..registry import register_theme

__all__: list[str] = []

_RED = "\033[31m"
_YEL = "\033[33m"
_CYN = "\033[36m"
_WHT = "\033[37m"
_RST = "\033[0m"


def _create(tier: str) -> Animation:
    if tier == "emoji":
        return _emoji()
    elif tier == "unicode":
        return _unicode()
    else:
        return _ascii()


def _emoji() -> Animation:
    # Dynamic exhaust trail: mix of full blocks and shades for texture
    fill = (
        f"{_RED}\u2588{_RST}",   # red full block
        f"{_YEL}\u2588{_RST}",   # yellow full block
        f"{_YEL}\u2592{_RST}",   # yellow medium shade
        f"{_RED}\u2593{_RST}",   # red dark shade
        f"{_YEL}\u2588{_RST}",   # yellow full block
        f"{_RED}\u2591{_RST}",   # red light shade (trailing exhaust)
    )
    sprite_a = Frame(lines=("\U0001f680",))     # rocket emoji (2 cols)
    sprite_b = Frame(lines=("\U0001f680",))
    completion = Frame(lines=("\U0001f680\u2605",))   # rocket + star

    # Decoration: starfield above, exhaust particles below -- parallax effect
    dec_a = Frame(lines=(
        f"\u2605  {_WHT}\u00b7{_RST}       {_CYN}\u2726{_RST}        {_WHT}\u00b7{_RST}  \u2605       {_CYN}\u2726{_RST}    {_WHT}\u00b7{_RST}  \u2605       {_CYN}\u2726{_RST}    {_WHT}\u00b7{_RST}  \u2605",
        f"  {_YEL}\u2022{_RST}    {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}   {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}    {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}   {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}",
    ))
    dec_b = Frame(lines=(
        f"  {_WHT}\u00b7{_RST}   \u2605          {_WHT}\u2726{_RST}         \u2605               {_CYN}\u00b7{_RST}   \u2605    {_WHT}\u2726{_RST}         \u2605   {_CYN}\u00b7{_RST}",
        f"     {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}   {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}   {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}   {_RED}\u00b7{_RST}        {_YEL}\u2022{_RST}",
    ))
    dec_done = Frame(lines=(
        f"  \u2605   {_CYN}\u2726{_RST}   \u2605       {_WHT}\u2726{_RST}   \u2605       {_CYN}\u2726{_RST}   \u2605       {_WHT}\u2726{_RST}   \u2605       {_CYN}\u2726{_RST}   \u2605",
        f"  {_CYN}\u2726{_RST}   \u2605   {_WHT}\u2726{_RST}       \u2605   {_CYN}\u2726{_RST}       \u2605   {_WHT}\u2726{_RST}       \u2605   {_CYN}\u2726{_RST}       \u2605   {_WHT}\u2726{_RST}",
    ))

    return Animation(
        name="rocket",
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
        f"{_RED}\u2588{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_YEL}\u2592{_RST}",
        f"{_RED}\u2593{_RST}",
        f"{_YEL}\u2588{_RST}",
        f"{_RED}\u2591{_RST}",
    )
    sprite_a = Frame(lines=("|=>",))
    sprite_b = Frame(lines=("]=>",))
    completion = Frame(lines=("|=>*",))

    dec_a = Frame(lines=(
        "*  \u00b7       \u2726        \u00b7  *       \u2726    \u00b7  *       \u2726    \u00b7  *       \u2726   \u00b7  *",
        "  \u2022    \u00b7        \u2022   \u00b7        \u2022    \u00b7        \u2022   \u00b7        \u2022    \u00b7   \u2022",
    ))
    dec_b = Frame(lines=(
        "  \u00b7   *          \u2726         *               \u00b7   *    \u2726         *   \u00b7   *",
        "     \u00b7        \u2022   \u00b7        \u2022   \u00b7        \u2022   \u00b7        \u2022   \u00b7   \u2022   \u00b7",
    ))
    dec_done = Frame(lines=(
        "  *   \u2726   *       \u2726   *       \u2726   *       \u2726   *       \u2726   *   \u2726   *",
        "  \u2726   *   \u2726       *   \u2726       *   \u2726       *   \u2726       *   \u2726   *   \u2726",
    ))

    return Animation(
        name="rocket",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


def _ascii() -> Animation:
    fill = ("~", "=", "~", "=")
    sprite_a = Frame(lines=("=>",))
    sprite_b = Frame(lines=("=>",))
    completion = Frame(lines=("=>*",))

    dec_a = Frame(lines=(
        "*  .       *        .  *       .    *  .       *        .  *       .   *  .",
        "  .    .        .   .        .    .        .   .        .    .      .   .  .",
    ))
    dec_b = Frame(lines=(
        "  .   *          *         *               .   *    .          *      .  *  .",
        "     .        .   .        .   .        .   .        .   .        .   .  .  .",
    ))
    dec_done = Frame(lines=(
        "  *   .   *       .   *       .   *       .   *       .   *       .   *  .  *",
        "  .   *   .       *   .       *   .       *   .       *   .       *   .  *  .",
    ))

    return Animation(
        name="rocket",
        frames=(sprite_a, sprite_b),
        fps=3.0,
        mode=AnimationMode.WALK,
        completion_frame=completion,
        bar_fill=fill,
        decoration=(dec_a, dec_b),
        completion_decoration=dec_done,
    )


register_theme("rocket", _create)
