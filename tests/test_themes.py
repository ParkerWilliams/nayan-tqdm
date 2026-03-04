"""Tests for all 6 themes at 5 progress levels x 3 tiers, plus themed bar
rendering, registry, and model tests."""
from __future__ import annotations

import warnings
from unittest.mock import MagicMock, patch

import pytest

from nayan_tqdm.models import Animation, AnimationMode, Frame
from nayan_tqdm.engine import (
    build_themed_fill, render_animation, render_themed_bar,
)
from nayan_tqdm.formatters import format_stats_left, format_stats_right
from nayan_tqdm.renderer import has_unclosed_ansi
from nayan_tqdm.utils import disp_len
from nayan_tqdm.registry import (
    register_theme, get_theme, list_themes, set_theme,
    get_default_theme, resolve_render_tier,
    _themes, _cache, _clear_cache,
)
from nayan_tqdm.terminal import ColorTier, TerminalInfo

import nayan_tqdm.themes  # noqa: F401 -- trigger registration


ALL_THEMES = [
    "bear", "cat_mouse", "cat_play", "cat_sleepy", "cat_smug",
    "cat_yarn", "construction", "cry",
    "deal_with_it", "disapproval", "disco", "double_flip",
    "finger_guns", "flex", "garden",
    "heartbeat", "hype", "lenny", "lightning", "matrix", "nyan", "ocean",
    "rage", "rocket", "run", "shrug", "sparkles",
    "table_flip", "table_rage", "table_unflip",
    "uwu", "wizard", "zen",
]
TIERS = ("emoji", "unicode", "ascii")
PROGRESS_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
WIDTH = 80


# ── Themed bar rendering tests (all themes use bar_fill) ────


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_is_animation(theme: str, tier: str) -> None:
    assert isinstance(get_theme(theme, tier), Animation)


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_has_bar_fill(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.bar_fill is not None


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_has_frames(theme: str, tier: str) -> None:
    assert get_theme(theme, tier).frame_count >= 2


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_fps_positive(theme: str, tier: str) -> None:
    assert get_theme(theme, tier).fps > 0


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_has_completion_frame(theme: str, tier: str) -> None:
    assert get_theme(theme, tier).completion_frame is not None


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_frame_widths_consistent(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    widths = {f.display_width for f in anim.frames}
    assert len(widths) == 1, f"Inconsistent widths: {widths}"


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_single_line_sprites(theme: str, tier: str) -> None:
    """All themed sprites are single-line (bar_fill themes)."""
    anim = get_theme(theme, tier)
    for frame in anim.frames:
        assert frame.height == 1


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
@pytest.mark.parametrize("progress", PROGRESS_LEVELS)
def test_themed_bar_renders_at_progress(
    theme: str, tier: str, progress: float,
) -> None:
    anim = get_theme(theme, tier)
    stats_left = format_stats_left(
        int(progress * 100), 100, desc=None, unit_scale=False,
    )
    stats_right = format_stats_right(
        int(progress * 100), 100, 5.0, 10.0,
        unit="it", postfix_str=None, unit_scale=False,
    )
    lines = render_themed_bar(
        anim, progress, WIDTH, 0.0, stats_left, stats_right,
    )
    assert isinstance(lines, list)
    assert len(lines) >= 1
    # The bar line should be exactly WIDTH display cols
    bar_line = lines[-1] if anim.decoration is None else lines[1] if len(lines) == 3 else lines[0]
    # Find the bar line (has pipes)
    for line in lines:
        if "|" in line:
            assert disp_len(line) == WIDTH, (
                f"theme={theme} tier={tier} progress={progress}: "
                f"disp_len={disp_len(line)} != {WIDTH}"
            )
            break


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_themed_bar_completion_renders(theme: str, tier: str) -> None:
    """At 100%, the completion frame sprite should be used."""
    anim = get_theme(theme, tier)
    stats_left = format_stats_left(100, 100)
    stats_right = format_stats_right(100, 100, 10.0, 10.0)
    lines = render_themed_bar(anim, 1.0, WIDTH, 0.0, stats_left, stats_right)
    assert len(lines) >= 1
    # Completion sprite should appear in one of the lines
    comp = anim.completion_frame
    assert comp is not None
    full_output = "".join(lines)
    assert comp.lines[0] in full_output


# ── Nyan-specific tests ────────────────────────────────────


@pytest.mark.parametrize("tier", TIERS)
def test_nyan_has_decoration(tier: str) -> None:
    anim = get_theme("nyan", tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None


@pytest.mark.parametrize("tier", TIERS)
def test_nyan_renders_3_lines(tier: str) -> None:
    """Nyan has decoration above + bar + decoration below = 3 lines."""
    anim = get_theme("nyan", tier)
    stats_left = format_stats_left(50, 100)
    stats_right = format_stats_right(50, 100, 5.0, 10.0)
    lines = render_themed_bar(anim, 0.5, WIDTH, 0.0, stats_left, stats_right)
    assert len(lines) == 3


@pytest.mark.parametrize("tier", ("emoji", "unicode"))
def test_nyan_rainbow_fill_has_colors(tier: str) -> None:
    anim = get_theme("nyan", tier)
    assert anim.bar_fill is not None
    # Rainbow fill chars should contain ANSI color codes
    for char in anim.bar_fill:
        assert "\033[" in char


def test_nyan_ascii_fill_is_plain() -> None:
    anim = get_theme("nyan", "ascii")
    assert anim.bar_fill is not None
    for char in anim.bar_fill:
        assert "\033[" not in char


# ── Theme-specific completion tests ────────────────────────


def test_table_flip_completion_has_table() -> None:
    anim = get_theme("table_flip", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u253b" in comp  # table part


def test_deal_with_it_completion_has_sunglasses() -> None:
    anim = get_theme("deal_with_it", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u25a0" in comp  # sunglasses


def test_lenny_completion_winks() -> None:
    anim = get_theme("lenny", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "~" in comp  # winking eye


def test_shrug_completion_same_as_sprite() -> None:
    anim = get_theme("shrug", "emoji")
    assert anim.completion_frame is not None
    assert anim.completion_frame.lines[0] == anim.frames[0].lines[0]


def test_finger_guns_completion_has_star() -> None:
    anim = get_theme("finger_guns", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star



def test_rocket_completion_has_star() -> None:
    anim = get_theme("rocket", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2b50" in comp  # star



def test_ocean_completion_has_sun() -> None:
    anim = get_theme("ocean", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2600" in comp  # sun emoji


def test_matrix_completion_has_done() -> None:
    anim = get_theme("matrix", "ascii")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert ">" in comp  # ">>>" in ascii tier


def test_heartbeat_completion_has_exclamation() -> None:
    anim = get_theme("heartbeat", "ascii")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "!" in comp  # "<3!" in ascii tier


def test_disco_completion_has_note() -> None:
    anim = get_theme("disco", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f3b5" in comp  # music note emoji


def test_zen_completion_has_sparkle() -> None:
    anim = get_theme("zen", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2728" in comp  # sparkles emoji


def test_construction_completion_has_ok() -> None:
    anim = get_theme("construction", "ascii")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "OK" in comp  # "[OK]" in ascii tier


def test_wizard_completion_has_sparkles() -> None:
    anim = get_theme("wizard", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2728" in comp  # sparkles (wizard casts final sparkle)



def test_garden_completion_has_sparkles() -> None:
    anim = get_theme("garden", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2728" in comp  # sparkles


def test_lightning_completion_has_bolt() -> None:
    anim = get_theme("lightning", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u26a1" in comp  # high voltage


def test_table_unflip_completion_has_table() -> None:
    anim = get_theme("table_unflip", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u252c" in comp  # ┬ (table upright)


def test_table_rage_completion_has_table() -> None:
    anim = get_theme("table_rage", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u253b" in comp  # ┻ (flipped table)


def test_double_flip_completion_has_two_tables() -> None:
    anim = get_theme("double_flip", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    # Should have ┻━┻ on both sides
    assert comp.count("\u253b") >= 4  # at least 4 ┻ chars (2 tables)



def test_cat_yarn_completion_has_heart_eyes() -> None:
    anim = get_theme("cat_yarn", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f63b" in comp  # heart-eyes cat


def test_cat_mouse_completion_has_smirking_cat() -> None:
    anim = get_theme("cat_mouse", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f63c" in comp  # smirking cat



def test_cat_smug_completion_has_crown() -> None:
    anim = get_theme("cat_smug", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f451" in comp  # crown


def test_cat_sleepy_completion_has_zzz() -> None:
    anim = get_theme("cat_sleepy", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f4a4" in comp  # zzz


def test_cat_play_completion_has_sparkles() -> None:
    anim = get_theme("cat_play", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2728" in comp  # sparkles


# ── Decoration tests for reworked and new themes ───────────


@pytest.mark.parametrize("theme", ["heartbeat", "wizard", "rocket"])
@pytest.mark.parametrize("tier", TIERS)
def test_reworked_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None


@pytest.mark.parametrize("theme", ["garden", "lightning"])
@pytest.mark.parametrize("tier", TIERS)
def test_new_decorated_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None


@pytest.mark.parametrize("theme", ["cat_mouse", "cat_yarn"])
@pytest.mark.parametrize("tier", TIERS)
def test_chase_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None


DECORATED_THEMES = [
    "cat_mouse", "cat_play", "cat_sleepy", "cat_smug",
    "cat_yarn", "garden",
    "heartbeat", "lightning", "nyan", "rocket", "wizard",
]


@pytest.mark.parametrize("theme", DECORATED_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_decorated_themes_render_3_lines(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    stats_left = format_stats_left(50, 100)
    stats_right = format_stats_right(50, 100, 5.0, 10.0)
    lines = render_themed_bar(anim, 0.5, WIDTH, 0.0, stats_left, stats_right)
    assert len(lines) == 3, f"{theme}/{tier} should render 3 lines, got {len(lines)}"


# ── No themes without bar_fill ─────────────────────────────


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_all_themes_use_bar_fill(theme: str, tier: str) -> None:
    """All new themes must use the themed bar rendering path."""
    anim = get_theme(theme, tier)
    assert anim.bar_fill is not None


# ── Decoration minimum width ──────────────────────────────

MIN_DECORATION_WIDTH = 70


@pytest.mark.parametrize("theme", DECORATED_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_decoration_lines_min_width(theme: str, tier: str) -> None:
    """Decoration lines must span at least MIN_DECORATION_WIDTH display cols.

    Short decoration lines cause visible gaps where the stars/symbols
    stop partway across the bar. This catches that common authoring bug.
    """
    anim = get_theme(theme, tier)
    if anim.decoration is None:
        return
    for i, dec_frame in enumerate(anim.decoration):
        for j, line in enumerate(dec_frame.lines):
            w = disp_len(line)
            assert w >= MIN_DECORATION_WIDTH, (
                f"{theme}/{tier} decoration[{i}].lines[{j}] "
                f"is {w} display cols, need >= {MIN_DECORATION_WIDTH}"
            )
    if anim.completion_decoration is not None:
        for j, line in enumerate(anim.completion_decoration.lines):
            w = disp_len(line)
            assert w >= MIN_DECORATION_WIDTH, (
                f"{theme}/{tier} completion_decoration.lines[{j}] "
                f"is {w} display cols, need >= {MIN_DECORATION_WIDTH}"
            )


# ── build_themed_fill tests ────────────────────────────────


def test_build_themed_fill_basic() -> None:
    result = build_themed_fill(("A", "B", "C"), 6)
    assert result == "ABCABC"


def test_build_themed_fill_single_char() -> None:
    result = build_themed_fill(("#",), 5)
    assert result == "#####"


def test_build_themed_fill_zero_cols() -> None:
    result = build_themed_fill(("A", "B"), 0)
    assert result == ""


def test_build_themed_fill_empty_tuple() -> None:
    result = build_themed_fill((), 5)
    assert result == ""


def test_build_themed_fill_ansi_colors() -> None:
    fill = ("\033[31m\u2588\033[0m", "\033[32m\u2588\033[0m")
    result = build_themed_fill(fill, 3)
    # Display width should be 3 (3 block chars)
    assert disp_len(result) == 3
    # But string length includes ANSI codes
    assert len(result) > 3


# ── render_themed_bar tests ────────────────────────────────


def _make_themed_anim(
    bar_fill: tuple[str, ...] = ("#",),
    sprite: str = ">",
    completion_sprite: str = "!",
) -> Animation:
    return Animation(
        name="test",
        frames=(Frame(lines=(sprite,)), Frame(lines=(sprite,))),
        fps=12.0,
        mode=AnimationMode.WALK,
        completion_frame=Frame(lines=(completion_sprite,)),
        bar_fill=bar_fill,
    )


def test_render_themed_bar_basic() -> None:
    anim = _make_themed_anim()
    lines = render_themed_bar(anim, 0.5, 40, 0.0, " 50%", " 50/100 [00:05]")
    assert len(lines) == 1
    assert "|" in lines[0]
    assert disp_len(lines[0]) == 40


def test_render_themed_bar_at_zero() -> None:
    anim = _make_themed_anim()
    lines = render_themed_bar(anim, 0.0, 40, 0.0, "  0%", " 0/100 [00:00]")
    assert len(lines) == 1
    bar_content = lines[0].split("|")[1]
    # At 0%, fill should be empty (just sprite + spaces)
    assert "#" not in bar_content


def test_render_themed_bar_at_100() -> None:
    anim = _make_themed_anim()
    lines = render_themed_bar(anim, 1.0, 40, 0.0, "100%", " 100/100 [00:10]")
    assert len(lines) == 1
    # Completion sprite should appear
    assert "!" in lines[0]


def test_render_themed_bar_exact_width() -> None:
    anim = _make_themed_anim()
    for width in (40, 60, 80, 100, 120):
        stats_left = " 50%"
        stats_right = " 50/100 [00:05]"
        lines = render_themed_bar(
            anim, 0.5, width, 0.0, stats_left, stats_right,
        )
        assert disp_len(lines[0]) == width, f"width={width}"


def test_render_themed_bar_with_decoration() -> None:
    dec = Frame(lines=("stars above", "stars below"))
    anim = Animation(
        name="test",
        frames=(Frame(lines=(">",)),),
        fps=12.0,
        mode=AnimationMode.WALK,
        completion_frame=Frame(lines=("!",)),
        bar_fill=("#",),
        decoration=(dec,),
    )
    lines = render_themed_bar(anim, 0.5, 40, 0.0, " 50%", " 50/100")
    # Should have 3 lines: decoration above + bar + decoration below
    assert len(lines) == 3


def test_render_themed_bar_narrow_graceful() -> None:
    """Even with a very wide sprite, rendering shouldn't crash."""
    anim = _make_themed_anim(sprite="a_very_long_sprite_here")
    lines = render_themed_bar(anim, 0.5, 40, 0.0, " 50%", " 50/100")
    assert len(lines) >= 1


def test_render_themed_bar_no_bar_fill_returns_empty() -> None:
    """Animation without bar_fill returns empty list."""
    anim = Animation(
        name="test",
        frames=(Frame(lines=(">",)),),
        fps=12.0,
    )
    lines = render_themed_bar(anim, 0.5, 40, 0.0, " 50%", " 50/100")
    assert lines == []


# ── format_stats_left / format_stats_right tests ───────────


def test_format_stats_left_determinate() -> None:
    result = format_stats_left(50, 100)
    assert "50%" in result


def test_format_stats_left_with_desc() -> None:
    result = format_stats_left(50, 100, desc="dl")
    assert result.startswith("dl: ")
    assert "50%" in result


def test_format_stats_left_indeterminate() -> None:
    result = format_stats_left(42, None)
    assert "42" in result
    assert "%" not in result


def test_format_stats_right_determinate() -> None:
    result = format_stats_right(50, 100, 5.0, 10.0)
    assert "50/100" in result
    assert "00:05" in result


def test_format_stats_right_indeterminate() -> None:
    result = format_stats_right(42, None, 5.0, 10.0)
    assert "00:05" in result
    # No count/total like "42/100", but it/s is fine
    assert "42/" not in result


def test_format_stats_right_with_postfix() -> None:
    result = format_stats_right(50, 100, 5.0, 10.0, postfix_str="loss=0.5")
    assert "loss=0.5" in result


# ── ANSI integrity for colored themes ─────────────────────


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", ("emoji", "unicode"))
def test_themed_bar_no_unclosed_ansi(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    stats_left = format_stats_left(50, 100)
    stats_right = format_stats_right(50, 100, 5.0, 10.0)
    lines = render_themed_bar(anim, 0.5, WIDTH, 0.0, stats_left, stats_right)
    for i, line in enumerate(lines):
        assert not has_unclosed_ansi(line), (
            f"theme={theme} tier={tier} line={i} has unclosed ANSI"
        )


# ── Frame / Animation model tests ───────────────────────────


def test_frame_basic_construction() -> None:
    frame = Frame(lines=("=^.^=", " || "))
    assert frame.lines == ("=^.^=", " || ")


def test_frame_display_width_ascii() -> None:
    frame = Frame(lines=("=^.^=", " || "))
    assert frame.display_width == 5


def test_frame_display_width_multiline_max() -> None:
    frame = Frame(lines=("abc", "abcdef"))
    assert frame.display_width == 6


def test_frame_display_width_cjk() -> None:
    frame = Frame(lines=("\u4e16\u754c",))
    assert frame.display_width == 4


def test_frame_display_width_with_ansi() -> None:
    frame = Frame(lines=("\033[31mhi\033[0m",))
    assert frame.display_width == 2


def test_frame_height() -> None:
    frame = Frame(lines=("a", "b", "c"))
    assert frame.height == 3


def test_frame_height_single_line() -> None:
    frame = Frame(lines=("hello",))
    assert frame.height == 1


def test_frame_empty_lines() -> None:
    frame = Frame(lines=())
    assert frame.display_width == 0
    assert frame.height == 0


def test_frame_frozen_lines() -> None:
    frame = Frame(lines=("a",))
    with pytest.raises(AttributeError):
        frame.lines = ("b",)  # type: ignore[misc]


def test_frame_frozen_display_width() -> None:
    frame = Frame(lines=("a",))
    with pytest.raises(AttributeError):
        frame.display_width = 99  # type: ignore[misc]


def test_animation_mode_walk() -> None:
    assert AnimationMode.WALK.value == "walk"


def test_animation_mode_cycle() -> None:
    assert AnimationMode.CYCLE.value == "cycle"


def test_animation_mode_fill() -> None:
    assert AnimationMode.FILL.value == "fill"


@pytest.fixture
def _frames() -> tuple[Frame, ...]:
    return (Frame(lines=("=^.^=",)), Frame(lines=("=^o^=",)))


def test_animation_construction(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.name == "cat"
    assert anim.frames == _frames


def test_animation_default_fps(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.fps == 12.0


def test_animation_custom_fps(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames, fps=24.0)
    assert anim.fps == 24.0


def test_animation_default_mode(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.mode == AnimationMode.WALK


def test_animation_custom_mode(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames, mode=AnimationMode.CYCLE)
    assert anim.mode == AnimationMode.CYCLE


def test_animation_frame_count(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.frame_count == 2


def test_animation_completion_frame_default_none(
    _frames: tuple[Frame, ...],
) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.completion_frame is None


def test_animation_completion_frame_set(_frames: tuple[Frame, ...]) -> None:
    done = Frame(lines=("done!",))
    anim = Animation(name="cat", frames=_frames, completion_frame=done)
    assert anim.completion_frame is done


def test_animation_bar_fill_default_none(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.bar_fill is None


def test_animation_bar_fill_set(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames, bar_fill=("#",))
    assert anim.bar_fill == ("#",)


def test_animation_decoration_default_none(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.decoration is None


def test_animation_decoration_set(_frames: tuple[Frame, ...]) -> None:
    dec = Frame(lines=("* *",))
    anim = Animation(name="cat", frames=_frames, decoration=(dec,))
    assert anim.decoration == (dec,)


def test_animation_frozen_name(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    with pytest.raises(AttributeError):
        anim.name = "dog"  # type: ignore[misc]


def test_animation_frozen_fps(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    with pytest.raises(AttributeError):
        anim.fps = 60.0  # type: ignore[misc]


def test_animation_single_frame() -> None:
    frame = Frame(lines=("x",))
    anim = Animation(name="one", frames=(frame,))
    assert anim.frame_count == 1


def test_animation_empty_frames() -> None:
    anim = Animation(name="empty", frames=())
    assert anim.frame_count == 0


# ── Registry tests ──────────────────────────────────────────


def _make_animation(name: str = "test") -> Animation:
    return Animation(
        name=name, frames=(Frame(lines=("X",)),),
        fps=12.0, mode=AnimationMode.WALK,
    )


def _make_factory(name: str = "test") -> MagicMock:
    return MagicMock(return_value=_make_animation(name))


@pytest.fixture(autouse=True)
def _clean_registry() -> None:
    orig_themes = dict(_themes)
    orig_default = get_default_theme()
    _clear_cache()
    yield  # type: ignore[misc]
    _themes.clear()
    _themes.update(orig_themes)
    _clear_cache()
    import nayan_tqdm.registry as reg
    reg._default_theme = orig_default


def test_register_theme() -> None:
    factory = _make_factory("custom")
    register_theme("custom", factory)
    assert "custom" in list_themes()


def test_register_theme_overwrites() -> None:
    factory_a = _make_factory("a")
    factory_b = _make_factory("b")
    register_theme("dup", factory_a)
    register_theme("dup", factory_b)
    get_theme("dup", "ascii")
    factory_b.assert_called_once_with("ascii")
    factory_a.assert_not_called()


def test_list_themes_returns_sorted() -> None:
    register_theme("zebra", _make_factory())
    register_theme("apple", _make_factory())
    register_theme("mango", _make_factory())
    names = list_themes()
    custom_names = [n for n in names if n in ("zebra", "apple", "mango")]
    assert custom_names == ["apple", "mango", "zebra"]


def test_get_theme_calls_factory() -> None:
    factory = _make_factory("caller")
    register_theme("caller", factory)
    get_theme("caller", "ascii")
    factory.assert_called_once_with("ascii")


def test_get_theme_returns_animation() -> None:
    register_theme("anim_test", _make_factory("anim_test"))
    result = get_theme("anim_test", "ascii")
    assert isinstance(result, Animation)


def test_get_theme_caches_result() -> None:
    factory = _make_factory("cached")
    register_theme("cached", factory)
    a = get_theme("cached", "ascii")
    b = get_theme("cached", "ascii")
    assert a is b
    factory.assert_called_once()


def test_get_theme_different_tiers_cached_separately() -> None:
    factory = _make_factory("tiered")
    register_theme("tiered", factory)
    get_theme("tiered", "ascii")
    get_theme("tiered", "emoji")
    assert factory.call_count == 2


def test_get_theme_invalid_warns() -> None:
    register_theme("nyan", _make_factory("nyan"))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        get_theme("nonexistent", "ascii")
    assert len(w) == 1
    assert "nonexistent" in str(w[0].message)
    assert issubclass(w[0].category, UserWarning)


def test_get_theme_invalid_falls_back_to_default() -> None:
    register_theme("nyan", _make_factory("nyan"))
    result = get_theme("nonexistent", "ascii")
    assert result.name == "nyan"


def test_default_theme_is_nyan() -> None:
    assert get_default_theme() == "nyan"


def test_set_theme_changes_default() -> None:
    register_theme("table_flip", _make_factory("table_flip"))
    set_theme("table_flip")
    assert get_default_theme() == "table_flip"


def test_set_theme_invalid_warns() -> None:
    original = get_default_theme()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        set_theme("nonexistent")
    assert len(w) == 1
    assert "nonexistent" in str(w[0].message)
    assert get_default_theme() == original


def test_factory_not_called_on_register() -> None:
    factory = _make_factory("lazy")
    register_theme("lazy", factory)
    factory.assert_not_called()


def test_factory_called_on_first_get() -> None:
    factory = _make_factory("lazy2")
    register_theme("lazy2", factory)
    get_theme("lazy2", "ascii")
    factory.assert_called_once()


# ── resolve_render_tier tests ────────────────────────────────


def _make_info(color: ColorTier = ColorTier.TRUE_COLOR) -> TerminalInfo:
    return TerminalInfo(
        is_tty=True, color_support=color, width=80, is_notebook=False,
    )


from tests.conftest import utf8_locale, no_utf8_locale


def test_true_color_returns_emoji() -> None:
    with utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.TRUE_COLOR)) == "emoji"


def test_color_256_returns_emoji() -> None:
    with utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.COLOR_256)) == "emoji"


def test_color_16_returns_unicode() -> None:
    with utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.COLOR_16)) == "unicode"


def test_no_color_returns_ascii() -> None:
    with utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.NONE)) == "ascii"


def test_no_utf8_locale_returns_ascii() -> None:
    with no_utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.TRUE_COLOR)) == "ascii"


def test_render_level_override_ascii() -> None:
    with utf8_locale():
        result = resolve_render_tier(
            _make_info(ColorTier.TRUE_COLOR), render_level="ascii",
        )
        assert result == "ascii"


def test_render_level_override_emoji() -> None:
    with utf8_locale():
        result = resolve_render_tier(
            _make_info(ColorTier.NONE), render_level="emoji",
        )
        assert result == "emoji"
