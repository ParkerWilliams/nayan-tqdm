"""Tests for fallback decision logic, plain-text bar, and terminal detection."""
from __future__ import annotations

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from nayan_tqdm.fallback import should_use_fallback, render_fallback_bar
from nayan_tqdm.terminal import ColorTier, TerminalInfo, detect_terminal
from nayan_tqdm.utils import strip_ansi


# ── Helpers ─────────────────────────────────────────────────


def _make_info(
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


def _make_stream(is_tty: bool) -> MagicMock:
    stream = MagicMock()
    stream.isatty.return_value = is_tty
    return stream


# ── should_use_fallback ─────────────────────────────────────


def test_fallback_non_tty() -> None:
    info = _make_info(is_tty=False)
    assert should_use_fallback(info) is True


def test_dumb_terminal_tty_allows_animation() -> None:
    """Dumb TTY terminals get ASCII-tier animation, not plain fallback."""
    info = _make_info(color_support=ColorTier.NONE)
    assert should_use_fallback(info) is False


def test_non_tty_no_color_uses_fallback() -> None:
    """Non-TTY with no color still falls back (piped output)."""
    info = _make_info(is_tty=False, color_support=ColorTier.NONE)
    assert should_use_fallback(info) is True


def test_fallback_narrow_terminal() -> None:
    info = _make_info(width=25)
    assert should_use_fallback(info) is True


def test_fallback_width_exactly_30() -> None:
    info = _make_info(width=30)
    assert should_use_fallback(info) is False


def test_fallback_disabled() -> None:
    info = _make_info()
    assert should_use_fallback(info, disable=True) is True


def test_fallback_nested_bar() -> None:
    info = _make_info()
    assert should_use_fallback(info, position=1) is True


def test_fallback_position_zero() -> None:
    info = _make_info()
    assert should_use_fallback(info, position=0) is False


def test_no_fallback_normal_tty() -> None:
    info = _make_info()
    assert should_use_fallback(info) is False


# ── render_fallback_bar ─────────────────────────────────────


def test_fallback_bar_determinate() -> None:
    result = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
    )
    assert "50%" in result
    assert "50/100" in result
    assert "00:05" in result
    assert "10.00it/s" in result
    assert "|" in result


def test_fallback_bar_zero_progress() -> None:
    result = render_fallback_bar(
        n=0, total=100, elapsed=0.0, rate=None, unit="it", ncols=80,
    )
    assert "0%" in result
    assert "0/100" in result
    assert "?it/s" in result


def test_fallback_bar_complete() -> None:
    result = render_fallback_bar(
        n=100, total=100, elapsed=10.0, rate=10.0, unit="it", ncols=80,
    )
    assert "100%" in result
    assert "##########" in result  # fully filled bar


def test_fallback_bar_indeterminate() -> None:
    result = render_fallback_bar(
        n=1000, total=None, elapsed=5.0, rate=200.0, unit="it",
    )
    assert "1000it" in result
    assert "00:05" in result
    assert "200.00it/s" in result
    assert "%" not in result


def test_fallback_bar_with_desc() -> None:
    result = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
        ncols=80, desc="dl",
    )
    assert result.startswith("dl: ")


def test_fallback_bar_with_postfix() -> None:
    result = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
        ncols=80, postfix_str="loss=0.5",
    )
    assert "loss=0.5" in result


def test_fallback_bar_unit_scale() -> None:
    result = render_fallback_bar(
        n=1500, total=10000, elapsed=5.0, rate=300.0, unit="B",
        ncols=80, unit_scale=True,
    )
    assert "1.50k" in result
    assert "10.00k" in result


def test_fallback_bar_no_ansi() -> None:
    result = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
    )
    # Output must contain zero ANSI sequences
    assert strip_ansi(result) == result


def test_fallback_bar_narrow_ncols() -> None:
    result = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=40,
    )
    # Bar should still have stats; bar portion shrinks but stats present
    assert "50%" in result
    assert "|" in result
    # The bar portion is smaller than at 80 cols
    wide = render_fallback_bar(
        n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
    )
    assert len(result) < len(wide)


# ── TerminalInfo ────────────────────────────────────────────


def test_terminal_info_construction() -> None:
    info = TerminalInfo(is_tty=True, color_support=ColorTier.COLOR_256, width=80, is_notebook=False)
    assert info.is_tty is True
    assert info.color_support == ColorTier.COLOR_256
    assert info.width == 80
    assert info.is_notebook is False


def test_terminal_info_frozen_raises() -> None:
    info = TerminalInfo(is_tty=True, color_support=ColorTier.NONE, width=80, is_notebook=False)
    with pytest.raises(AttributeError):
        info.is_tty = False  # type: ignore[misc]


def test_terminal_info_frozen_width_raises() -> None:
    info = TerminalInfo(is_tty=True, color_support=ColorTier.NONE, width=80, is_notebook=False)
    with pytest.raises(AttributeError):
        info.width = 120  # type: ignore[misc]


# ── ColorTier ───────────────────────────────────────────────


def test_color_tier_values() -> None:
    assert ColorTier.NONE == 0
    assert ColorTier.COLOR_16 == 1
    assert ColorTier.COLOR_256 == 2
    assert ColorTier.TRUE_COLOR == 3


def test_color_tier_comparison() -> None:
    assert ColorTier.TRUE_COLOR > ColorTier.COLOR_256
    assert ColorTier.COLOR_256 > ColorTier.COLOR_16
    assert ColorTier.COLOR_16 > ColorTier.NONE


# ── detect_terminal ─────────────────────────────────────────


def test_detect_tty_stream() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
        info = detect_terminal(stream)
    assert info.is_tty is True


def test_detect_non_tty_stream() -> None:
    stream = _make_stream(False)
    info = detect_terminal(stream)
    assert info.is_tty is False


def test_detect_non_tty_returns_no_color() -> None:
    stream = _make_stream(False)
    with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=False):
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.NONE


def test_detect_non_tty_returns_width_80() -> None:
    stream = _make_stream(False)
    info = detect_terminal(stream)
    assert info.width == 80


def test_detect_truecolor_via_colorterm() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"COLORTERM": "truecolor", "TERM": "xterm"}, clear=False):
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.TRUE_COLOR


def test_detect_truecolor_via_24bit() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"COLORTERM": "24bit", "TERM": "xterm"}, clear=False):
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.TRUE_COLOR


def test_detect_256color_via_term() -> None:
    stream = _make_stream(True)
    env = {"TERM": "xterm-256color"}
    with patch.dict(os.environ, env, clear=False):
        os.environ.pop("COLORTERM", None)
        os.environ.pop("NO_COLOR", None)
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.COLOR_256


def test_detect_basic_16_color() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
        os.environ.pop("COLORTERM", None)
        os.environ.pop("NO_COLOR", None)
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.COLOR_16


def test_detect_dumb_terminal() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"TERM": "dumb"}, clear=False):
        os.environ.pop("COLORTERM", None)
        os.environ.pop("NO_COLOR", None)
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.NONE


def test_detect_no_color_env_var() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"NO_COLOR": "1", "TERM": "xterm-256color"}, clear=False):
        info = detect_terminal(stream)
    assert info.color_support == ColorTier.NONE


def test_detect_terminal_width_from_shutil() -> None:
    stream = _make_stream(True)
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((120, 40))):
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            info = detect_terminal(stream)
    assert info.width == 120


def test_detect_notebook() -> None:
    stream = _make_stream(True)
    mock_shell = MagicMock()
    mock_shell.__class__ = type("ZMQInteractiveShell", (), {})
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
        with patch("nayan_tqdm.terminal._get_ipython_shell", return_value=mock_shell):
            info = detect_terminal(stream)
    assert info.is_notebook is True


def test_detect_no_ipython() -> None:
    stream = _make_stream(True)
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
        with patch("nayan_tqdm.terminal._get_ipython_shell", return_value=None):
            info = detect_terminal(stream)
    assert info.is_notebook is False


def test_detect_terminal_interactive_shell() -> None:
    stream = _make_stream(True)
    mock_shell = MagicMock()
    mock_shell.__class__ = type("TerminalInteractiveShell", (), {})
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
        with patch("nayan_tqdm.terminal._get_ipython_shell", return_value=mock_shell):
            info = detect_terminal(stream)
    assert info.is_notebook is False


def test_detect_default_stream_uses_stderr() -> None:
    """detect_terminal() with no args uses sys.stderr by default."""
    with patch.object(sys, "stderr", _make_stream(False)):
        info = detect_terminal()
    assert info.is_tty is False


def test_detect_stream_without_isatty() -> None:
    stream = MagicMock(spec=[])  # No isatty
    info = detect_terminal(stream)
    assert info.is_tty is False
