"""Integration tests for the theme system wired into NyanBar."""
from __future__ import annotations

import io
import os
import warnings
from unittest.mock import patch

import pytest

from nyanbar.core import NyanBar
from nyanbar.models import Animation, AnimationMode
from nyanbar.terminal import TerminalInfo, ColorTier
from nyanbar.registry import get_theme, list_themes, set_theme, get_default_theme
import nyanbar.themes  # noqa: F401 -- ensure all themes registered


# ── Fixtures ─────────────────────────────────────────


@pytest.fixture
def mock_tty():
    """Mock a TTY with COLOR_256 and UTF-8 locale."""
    info = TerminalInfo(
        is_tty=True, color_support=ColorTier.COLOR_256,
        width=80, is_notebook=False,
    )
    with patch("nyanbar.core.detect_terminal", return_value=info):
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8", "LC_ALL": "", "LC_CTYPE": ""}):
            yield info


@pytest.fixture
def mock_non_tty():
    """Mock a non-TTY (piped output)."""
    info = TerminalInfo(
        is_tty=False, color_support=ColorTier.NONE,
        width=80, is_notebook=False,
    )
    with patch("nyanbar.core.detect_terminal", return_value=info):
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            yield info


@pytest.fixture(autouse=True)
def _restore_default_theme():
    """Ensure default theme is restored after each test."""
    original = get_default_theme()
    yield
    import nyanbar.registry as reg
    reg._default_theme = original


# ── Theme selection tests ────────────────────────────


class TestThemeSelection:
    def test_default_theme_is_nyan(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, file=sio)
        assert bar._animation is not None
        assert bar._animation.name == "nyan"
        bar.close()

    def test_theme_kwarg_selects_theme(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, theme="cat_walk", file=sio)
        assert bar._animation is not None
        assert bar._animation.name == "cat_walk"
        bar.close()

    def test_theme_kwarg_fish(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, theme="fish", file=sio)
        assert bar._animation.name == "fish"
        bar.close()

    def test_theme_kwarg_rocket(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, theme="rocket", file=sio)
        assert bar._animation.name == "rocket"
        bar.close()

    def test_theme_kwarg_cat_bounce(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, theme="cat_bounce", file=sio)
        assert bar._animation.name == "cat_bounce"
        bar.close()


class TestInvalidTheme:
    def test_invalid_theme_warns_and_uses_default(self, mock_tty):
        sio = io.StringIO()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bar = NyanBar(total=10, theme="nonexistent", file=sio)
        assert bar._animation.name == "nyan"
        assert any("nonexistent" in str(warning.message) for warning in w)
        bar.close()


class TestRenderLevel:
    def test_render_level_ascii_forces_ascii(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, render_level="ascii", file=sio)
        assert bar._animation is not None
        # ASCII tier frames should have no ANSI color codes
        from nyanbar.renderer import has_unclosed_ansi
        for frame in bar._animation.frames:
            for line in frame.lines:
                assert "\033[" not in line or not has_unclosed_ansi(line)
        bar.close()

    def test_render_level_emoji_override(self):
        """Force emoji tier even with NONE color terminal."""
        info = TerminalInfo(
            is_tty=True, color_support=ColorTier.NONE,
            width=80, is_notebook=False,
        )
        sio = io.StringIO()
        with patch("nyanbar.core.detect_terminal", return_value=info):
            with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
                bar = NyanBar(total=10, render_level="emoji", file=sio)
        assert bar._animation is not None
        bar.close()


class TestSetTheme:
    def test_set_theme_affects_new_bars(self, mock_tty):
        sio = io.StringIO()
        set_theme("fish")
        bar = NyanBar(total=10, file=sio)
        assert bar._animation.name == "fish"
        bar.close()

    def test_existing_bar_keeps_theme(self, mock_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, file=sio)
        assert bar._animation.name == "nyan"
        set_theme("fish")
        # Existing bar still has nyan
        assert bar._animation.name == "nyan"
        bar.close()


class TestFallbackBars:
    def test_non_tty_uses_fallback(self, mock_non_tty):
        sio = io.StringIO()
        bar = NyanBar(total=10, file=sio)
        assert bar._use_fallback is True
        bar.close()

    def test_disabled_bar_no_animation(self):
        sio = io.StringIO()
        bar = NyanBar(total=10, disable=True, file=sio)
        assert bar._animation is None
        bar.close()


class TestMultilineRendering:
    def test_multiline_theme_renders(self, mock_tty):
        """Multi-line theme (nyan, 3-line) renders via animation frame method."""
        sio = io.StringIO()
        bar = NyanBar(total=10, theme="nyan", file=sio)
        # Manually trigger a render to check it works
        with bar._lock:
            bar._render_animation_frame()
        # Should have rendered 4 lines (3 animation + 1 stats)
        assert bar._prev_height == 4
        bar.close()

    def test_leave_true_multiline(self, mock_tty):
        """Multi-line theme with leave=True preserves output."""
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=True, theme="nyan", file=sio, disable=False)
        for _ in bar:
            pass
        output = sio.getvalue()
        # Should have content (not erased)
        assert len(output) > 0

    def test_leave_false_multiline(self, mock_tty):
        """Multi-line theme with leave=False erases output."""
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=False, theme="nyan", file=sio, disable=False)
        for _ in bar:
            pass
        output = sio.getvalue()
        # Should contain erase sequences
        assert "\033[" in output


class TestCompletionFrame:
    def test_completion_frame_at_100(self, mock_tty):
        """At 100% completion, theme with completion frame uses it."""
        sio = io.StringIO()
        bar = NyanBar(total=5, theme="cat_walk", leave=True, file=sio)
        for _ in range(5):
            bar.update()
        bar.close()
        # The bar rendered to completion -- output should contain data
        assert len(sio.getvalue()) > 0


class TestPublicAPI:
    def test_list_themes_returns_all_five(self):
        names = list_themes()
        expected = ["cat_bounce", "cat_walk", "fish", "nyan", "rocket"]
        assert names == expected

    def test_get_theme_returns_animation(self):
        anim = get_theme("nyan")
        assert isinstance(anim, Animation)

    def test_imports_work(self):
        from nyanbar import tqdm, trange, set_theme, list_themes, get_theme
        assert tqdm is NyanBar
        assert callable(set_theme)
        assert callable(list_themes)
        assert callable(get_theme)
