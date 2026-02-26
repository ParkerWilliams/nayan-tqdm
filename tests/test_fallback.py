"""Tests for nyanbar.fallback — fallback decision logic and plain text bar."""
from __future__ import annotations

import pytest

from nyanbar.fallback import should_use_fallback, render_fallback_bar
from nyanbar.terminal import TerminalInfo, ColorTier
from nyanbar.utils import strip_ansi


# ── should_use_fallback tests ────────────────────────────────


class TestShouldUseFallback:
    def _make_info(
        self,
        is_tty: bool = True,
        color_support: ColorTier = ColorTier.COLOR_256,
        width: int = 80,
        is_notebook: bool = False,
    ) -> TerminalInfo:
        return TerminalInfo(
            is_tty=is_tty,
            color_support=color_support,
            width=width,
            is_notebook=is_notebook,
        )

    def test_fallback_non_tty(self):
        info = self._make_info(is_tty=False)
        assert should_use_fallback(info) is True

    def test_dumb_terminal_tty_allows_animation(self):
        """Dumb TTY terminals get ASCII-tier animation, not plain fallback."""
        info = self._make_info(color_support=ColorTier.NONE)
        assert should_use_fallback(info) is False

    def test_non_tty_no_color_uses_fallback(self):
        """Non-TTY with no color still falls back (piped output)."""
        info = self._make_info(is_tty=False, color_support=ColorTier.NONE)
        assert should_use_fallback(info) is True

    def test_fallback_narrow_terminal(self):
        info = self._make_info(width=25)
        assert should_use_fallback(info) is True

    def test_fallback_width_exactly_30(self):
        info = self._make_info(width=30)
        assert should_use_fallback(info) is False

    def test_fallback_disabled(self):
        info = self._make_info()
        assert should_use_fallback(info, disable=True) is True

    def test_fallback_nested_bar(self):
        info = self._make_info()
        assert should_use_fallback(info, position=1) is True

    def test_fallback_position_zero(self):
        info = self._make_info()
        assert should_use_fallback(info, position=0) is False

    def test_no_fallback_normal_tty(self):
        info = self._make_info()
        assert should_use_fallback(info) is False


# ── render_fallback_bar tests ────────────────────────────────


class TestRenderFallbackBar:
    def test_fallback_bar_determinate(self):
        result = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
        )
        assert "50%" in result
        assert "50/100" in result
        assert "00:05" in result
        assert "10.00it/s" in result
        assert "|" in result

    def test_fallback_bar_zero_progress(self):
        result = render_fallback_bar(
            n=0, total=100, elapsed=0.0, rate=None, unit="it", ncols=80,
        )
        assert "0%" in result
        assert "0/100" in result
        assert "?it/s" in result

    def test_fallback_bar_complete(self):
        result = render_fallback_bar(
            n=100, total=100, elapsed=10.0, rate=10.0, unit="it", ncols=80,
        )
        assert "100%" in result
        assert "##########" in result  # fully filled bar

    def test_fallback_bar_indeterminate(self):
        result = render_fallback_bar(
            n=1000, total=None, elapsed=5.0, rate=200.0, unit="it",
        )
        assert "1000it" in result
        assert "00:05" in result
        assert "200.00it/s" in result
        assert "%" not in result

    def test_fallback_bar_with_desc(self):
        result = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
            ncols=80, desc="dl",
        )
        assert result.startswith("dl: ")

    def test_fallback_bar_with_postfix(self):
        result = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
            ncols=80, postfix_str="loss=0.5",
        )
        assert "loss=0.5" in result

    def test_fallback_bar_unit_scale(self):
        result = render_fallback_bar(
            n=1500, total=10000, elapsed=5.0, rate=300.0, unit="B",
            ncols=80, unit_scale=True,
        )
        assert "1.50k" in result
        assert "10.00k" in result

    def test_fallback_bar_no_ansi(self):
        result = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
        )
        # Output must contain zero ANSI sequences
        assert strip_ansi(result) == result

    def test_fallback_bar_narrow_ncols(self):
        result = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=40,
        )
        # Bar should still have stats; bar portion shrinks but stats present
        # Note: when stats alone exceed ncols, line may overflow (same as tqdm)
        assert "50%" in result
        assert "|" in result
        # The bar portion is smaller than at 80 cols
        wide = render_fallback_bar(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
        )
        assert len(result) < len(wide)
