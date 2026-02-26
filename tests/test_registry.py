"""Tests for the theme registry module."""
from __future__ import annotations

import os
import warnings
from unittest.mock import MagicMock

import pytest

from nyanbar.registry import (
    register_theme,
    get_theme,
    list_themes,
    set_theme,
    get_default_theme,
    resolve_render_tier,
    _themes,
    _cache,
    _clear_cache,
)
from nyanbar.models import Animation, AnimationMode, Frame
from nyanbar.terminal import ColorTier, TerminalInfo


# ── Helpers ──────────────────────────────────────────

def _make_animation(name: str = "test") -> Animation:
    """Create a minimal Animation for testing."""
    return Animation(
        name=name,
        frames=(Frame(lines=("X",)),),
        fps=12.0,
        mode=AnimationMode.WALK,
    )


def _make_factory(name: str = "test"):
    """Return a factory function that builds a test Animation."""
    mock = MagicMock(return_value=_make_animation(name))
    return mock


@pytest.fixture(autouse=True)
def _clean_registry():
    """Snapshot and restore registry state around each test."""
    orig_themes = dict(_themes)
    orig_default = get_default_theme()
    _clear_cache()
    yield
    _themes.clear()
    _themes.update(orig_themes)
    _clear_cache()
    # Restore default by direct mutation (bypass validation)
    import nyanbar.registry as reg
    reg._default_theme = orig_default


# ── Registration tests ───────────────────────────────


def test_register_theme():
    factory = _make_factory("custom")
    register_theme("custom", factory)
    assert "custom" in list_themes()


def test_register_theme_overwrites():
    factory_a = _make_factory("a")
    factory_b = _make_factory("b")
    register_theme("dup", factory_a)
    register_theme("dup", factory_b)
    anim = get_theme("dup", "ascii")
    factory_b.assert_called_once_with("ascii")
    factory_a.assert_not_called()


def test_list_themes_returns_sorted():
    register_theme("zebra", _make_factory())
    register_theme("apple", _make_factory())
    register_theme("mango", _make_factory())
    names = list_themes()
    # At minimum, our three are in sorted order
    custom_names = [n for n in names if n in ("zebra", "apple", "mango")]
    assert custom_names == ["apple", "mango", "zebra"]


# ── get_theme tests ──────────────────────────────────


def test_get_theme_calls_factory():
    factory = _make_factory("caller")
    register_theme("caller", factory)
    get_theme("caller", "ascii")
    factory.assert_called_once_with("ascii")


def test_get_theme_returns_animation():
    register_theme("anim_test", _make_factory("anim_test"))
    result = get_theme("anim_test", "ascii")
    assert isinstance(result, Animation)


def test_get_theme_caches_result():
    factory = _make_factory("cached")
    register_theme("cached", factory)
    a = get_theme("cached", "ascii")
    b = get_theme("cached", "ascii")
    assert a is b
    factory.assert_called_once()


def test_get_theme_different_tiers_cached_separately():
    factory = _make_factory("tiered")
    register_theme("tiered", factory)
    get_theme("tiered", "ascii")
    get_theme("tiered", "emoji")
    assert factory.call_count == 2


def test_get_theme_invalid_warns():
    # Ensure at least default "nyan" is registered
    register_theme("nyan", _make_factory("nyan"))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        get_theme("nonexistent", "ascii")
    assert len(w) == 1
    assert "nonexistent" in str(w[0].message)
    assert issubclass(w[0].category, UserWarning)


def test_get_theme_invalid_falls_back_to_default():
    register_theme("nyan", _make_factory("nyan"))
    result = get_theme("nonexistent", "ascii")
    assert result.name == "nyan"


# ── set_theme / get_default_theme tests ──────────────


def test_default_theme_is_nyan():
    assert get_default_theme() == "nyan"


def test_set_theme_changes_default():
    register_theme("cat_walk", _make_factory("cat_walk"))
    set_theme("cat_walk")
    assert get_default_theme() == "cat_walk"


def test_set_theme_invalid_warns():
    original = get_default_theme()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        set_theme("nonexistent")
    assert len(w) == 1
    assert "nonexistent" in str(w[0].message)
    assert get_default_theme() == original


# ── Lazy loading tests ───────────────────────────────


def test_factory_not_called_on_register():
    factory = _make_factory("lazy")
    register_theme("lazy", factory)
    factory.assert_not_called()


def test_factory_called_on_first_get():
    factory = _make_factory("lazy2")
    register_theme("lazy2", factory)
    get_theme("lazy2", "ascii")
    factory.assert_called_once()


# ── resolve_render_tier tests ────────────────────────


def _make_info(color: ColorTier = ColorTier.TRUE_COLOR) -> TerminalInfo:
    return TerminalInfo(
        is_tty=True, color_support=color, width=80, is_notebook=False,
    )


def test_true_color_returns_emoji():
    with _utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.TRUE_COLOR)) == "emoji"


def test_color_256_returns_emoji():
    with _utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.COLOR_256)) == "emoji"


def test_color_16_returns_unicode():
    with _utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.COLOR_16)) == "unicode"


def test_no_color_returns_ascii():
    with _utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.NONE)) == "ascii"


def test_no_utf8_locale_returns_ascii():
    with _no_utf8_locale():
        assert resolve_render_tier(_make_info(ColorTier.TRUE_COLOR)) == "ascii"


def test_render_level_override_ascii():
    with _utf8_locale():
        result = resolve_render_tier(_make_info(ColorTier.TRUE_COLOR), render_level="ascii")
        assert result == "ascii"


def test_render_level_override_emoji():
    with _utf8_locale():
        result = resolve_render_tier(_make_info(ColorTier.NONE), render_level="emoji")
        assert result == "emoji"


# ── Locale helpers ───────────────────────────────────

from contextlib import contextmanager
from unittest.mock import patch


@contextmanager
def _utf8_locale():
    with patch.dict(os.environ, {"LANG": "en_US.UTF-8", "LC_ALL": "", "LC_CTYPE": ""}):
        yield


@contextmanager
def _no_utf8_locale():
    with patch.dict(os.environ, {"LANG": "C", "LC_ALL": "", "LC_CTYPE": ""}, clear=False):
        # Ensure no UTF-8 in any locale var
        env = {k: v for k, v in os.environ.items() if k not in ("LANG", "LC_ALL", "LC_CTYPE")}
        env["LANG"] = "C"
        env["LC_ALL"] = ""
        env["LC_CTYPE"] = ""
        with patch.dict(os.environ, env, clear=True):
            yield
