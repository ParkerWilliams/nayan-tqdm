"""Tests for all 5 themes at 5 progress points x 3 tiers, plus registry and models."""
from __future__ import annotations

import os
import warnings
from unittest.mock import MagicMock, patch

import pytest

from nyanbar.models import Animation, AnimationMode, Frame
from nyanbar.engine import render_animation
from nyanbar.renderer import has_unclosed_ansi
from nyanbar.utils import disp_len
from nyanbar.registry import (
    register_theme, get_theme, list_themes, set_theme,
    get_default_theme, resolve_render_tier,
    _themes, _cache, _clear_cache,
)
from nyanbar.terminal import ColorTier, TerminalInfo

import nyanbar.themes  # noqa: F401 -- trigger registration


ALL_THEMES = ["cat_walk", "cat_bounce", "nyan", "fish", "rocket"]
TIERS = ("emoji", "unicode", "ascii")
PROGRESS_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
WIDTH = 60

# Expected heights per theme
THEME_HEIGHTS = {
    "cat_walk": 1, "cat_bounce": 2, "nyan": 3, "fish": 3, "rocket": 4,
}
# Expected modes per theme
THEME_MODES = {
    "cat_walk": AnimationMode.WALK,
    "cat_bounce": AnimationMode.WALK,
    "nyan": AnimationMode.WALK,
    "fish": AnimationMode.WALK,
    "rocket": AnimationMode.CYCLE,
}


# ── Theme rendering tests (parametrized over all themes) ─────


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_is_animation(theme: str, tier: str) -> None:
    assert isinstance(get_theme(theme, tier), Animation)


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_mode(theme: str, tier: str) -> None:
    assert get_theme(theme, tier).mode == THEME_MODES[theme]


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
def test_theme_frame_height(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    expected = THEME_HEIGHTS[theme]
    for frame in anim.frames:
        assert frame.height == expected


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_frame_widths_consistent(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    widths = {f.display_width for f in anim.frames}
    assert len(widths) == 1, f"Inconsistent widths: {widths}"


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_has_completion_frame(theme: str, tier: str) -> None:
    assert get_theme(theme, tier).completion_frame is not None


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_theme_completion_frame_height(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    expected = THEME_HEIGHTS[theme]
    assert anim.completion_frame is not None
    assert anim.completion_frame.height == expected


@pytest.mark.parametrize("theme", ALL_THEMES)
@pytest.mark.parametrize("tier", TIERS)
@pytest.mark.parametrize("progress", PROGRESS_LEVELS)
def test_theme_renders_at_progress(theme: str, tier: str, progress: float) -> None:
    anim = get_theme(theme, tier)
    lines = render_animation(anim, progress, WIDTH, 0.0)
    assert isinstance(lines, list)
    expected_height = THEME_HEIGHTS[theme]
    assert len(lines) == expected_height
    for line in lines:
        assert disp_len(line) == WIDTH, (
            f"theme={theme} tier={tier} progress={progress}: "
            f"disp_len={disp_len(line)} != {WIDTH}"
        )


# ── Theme-specific tests ────────────────────────────────────


@pytest.mark.parametrize("tier", TIERS)
def test_cat_walk_completion_width_matches(tier: str) -> None:
    anim = get_theme("cat_walk", tier)
    frame_w = anim.frames[0].display_width
    assert anim.completion_frame is not None
    comp_w = anim.completion_frame.display_width
    assert comp_w == frame_w


@pytest.mark.parametrize("tier", TIERS)
def test_nyan_frame_heights_consistent(tier: str) -> None:
    anim = get_theme("nyan", tier)
    heights = {f.height for f in anim.frames}
    assert heights == {3}


@pytest.mark.parametrize("tier", TIERS)
def test_nyan_completion_width_matches(tier: str) -> None:
    anim = get_theme("nyan", tier)
    fw = anim.frames[0].display_width
    assert anim.completion_frame is not None
    cw = anim.completion_frame.display_width
    assert cw == fw


@pytest.mark.parametrize("theme", ["nyan", "fish", "rocket"])
@pytest.mark.parametrize("tier", ("emoji", "unicode"))
def test_no_unclosed_ansi_in_frames(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    for i, frame in enumerate(anim.frames):
        for j, line in enumerate(frame.lines):
            assert not has_unclosed_ansi(line), (
                f"theme={theme} tier={tier} frame={i} line={j} has unclosed ANSI"
            )


@pytest.mark.parametrize("theme", ["nyan", "fish", "rocket"])
@pytest.mark.parametrize("tier", ("emoji", "unicode"))
def test_no_unclosed_ansi_in_completion(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.completion_frame is not None
    for j, line in enumerate(anim.completion_frame.lines):
        assert not has_unclosed_ansi(line), (
            f"theme={theme} tier={tier} completion line={j} has unclosed ANSI"
        )


def test_nyan_ascii_rainbow_has_patterns() -> None:
    anim = get_theme("nyan", "ascii")
    all_text = ""
    for frame in anim.frames:
        for line in frame.lines:
            all_text += line
    patterns_found = sum(1 for ch in ("=", "~", "-", ".") if ch in all_text)
    assert patterns_found >= 3


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


def test_animation_completion_frame_default_none(_frames: tuple[Frame, ...]) -> None:
    anim = Animation(name="cat", frames=_frames)
    assert anim.completion_frame is None


def test_animation_completion_frame_set(_frames: tuple[Frame, ...]) -> None:
    done = Frame(lines=("done!",))
    anim = Animation(name="cat", frames=_frames, completion_frame=done)
    assert anim.completion_frame is done


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
    return Animation(name=name, frames=(Frame(lines=("X",)),), fps=12.0, mode=AnimationMode.WALK)


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
    import nyanbar.registry as reg
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
    register_theme("cat_walk", _make_factory("cat_walk"))
    set_theme("cat_walk")
    assert get_default_theme() == "cat_walk"


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
    return TerminalInfo(is_tty=True, color_support=color, width=80, is_notebook=False)


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
        result = resolve_render_tier(_make_info(ColorTier.TRUE_COLOR), render_level="ascii")
        assert result == "ascii"


def test_render_level_override_emoji() -> None:
    with utf8_locale():
        result = resolve_render_tier(_make_info(ColorTier.NONE), render_level="emoji")
        assert result == "emoji"
