"""Tests for nyanbar.terminal — terminal capability detection."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from nyanbar.terminal import ColorTier, TerminalInfo, detect_terminal


# ── TerminalInfo ────────────────────────────────────────────


class TestTerminalInfo:
    """TerminalInfo is a frozen, immutable value object."""

    def test_construction(self) -> None:
        info = TerminalInfo(is_tty=True, color_support=ColorTier.COLOR_256, width=80, is_notebook=False)
        assert info.is_tty is True
        assert info.color_support == ColorTier.COLOR_256
        assert info.width == 80
        assert info.is_notebook is False

    def test_frozen_raises(self) -> None:
        info = TerminalInfo(is_tty=True, color_support=ColorTier.NONE, width=80, is_notebook=False)
        with pytest.raises(AttributeError):
            info.is_tty = False  # type: ignore[misc]

    def test_frozen_width_raises(self) -> None:
        info = TerminalInfo(is_tty=True, color_support=ColorTier.NONE, width=80, is_notebook=False)
        with pytest.raises(AttributeError):
            info.width = 120  # type: ignore[misc]


# ── ColorTier ───────────────────────────────────────────────


class TestColorTier:
    """ColorTier enum represents color support levels."""

    def test_values(self) -> None:
        assert ColorTier.NONE == 0
        assert ColorTier.COLOR_16 == 1
        assert ColorTier.COLOR_256 == 2
        assert ColorTier.TRUE_COLOR == 3

    def test_comparison(self) -> None:
        assert ColorTier.TRUE_COLOR > ColorTier.COLOR_256
        assert ColorTier.COLOR_256 > ColorTier.COLOR_16
        assert ColorTier.COLOR_16 > ColorTier.NONE


# ── detect_terminal ─────────────────────────────────────────


class TestDetectTerminal:
    """detect_terminal() probes the environment for terminal capabilities."""

    def _make_stream(self, is_tty: bool) -> MagicMock:
        stream = MagicMock()
        stream.isatty.return_value = is_tty
        return stream

    # TTY detection

    def test_tty_stream(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            info = detect_terminal(stream)
        assert info.is_tty is True

    def test_non_tty_stream(self) -> None:
        stream = self._make_stream(False)
        info = detect_terminal(stream)
        assert info.is_tty is False

    def test_non_tty_returns_no_color(self) -> None:
        stream = self._make_stream(False)
        with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=False):
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.NONE

    def test_non_tty_returns_width_80(self) -> None:
        stream = self._make_stream(False)
        info = detect_terminal(stream)
        assert info.width == 80

    # Color tier detection

    def test_truecolor_via_colorterm(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"COLORTERM": "truecolor", "TERM": "xterm"}, clear=False):
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.TRUE_COLOR

    def test_truecolor_via_24bit(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"COLORTERM": "24bit", "TERM": "xterm"}, clear=False):
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.TRUE_COLOR

    def test_256color_via_term(self) -> None:
        stream = self._make_stream(True)
        env = {"TERM": "xterm-256color"}
        # Remove COLORTERM if present to avoid interference
        with patch.dict(os.environ, env, clear=False):
            os.environ.pop("COLORTERM", None)
            os.environ.pop("NO_COLOR", None)
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.COLOR_256

    def test_basic_16_color(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            os.environ.pop("COLORTERM", None)
            os.environ.pop("NO_COLOR", None)
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.COLOR_16

    def test_dumb_terminal(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"TERM": "dumb"}, clear=False):
            os.environ.pop("COLORTERM", None)
            os.environ.pop("NO_COLOR", None)
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.NONE

    def test_no_color_env_var(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"NO_COLOR": "1", "TERM": "xterm-256color"}, clear=False):
            info = detect_terminal(stream)
        assert info.color_support == ColorTier.NONE

    # Width detection

    def test_terminal_width_from_shutil(self) -> None:
        stream = self._make_stream(True)
        with patch("shutil.get_terminal_size", return_value=os.terminal_size((120, 40))):
            with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
                info = detect_terminal(stream)
        assert info.width == 120

    # Notebook detection

    def test_notebook_detected(self) -> None:
        stream = self._make_stream(True)
        mock_shell = MagicMock()
        mock_shell.__class__ = type("ZMQInteractiveShell", (), {})
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            with patch("nyanbar.terminal._get_ipython_shell", return_value=mock_shell):
                info = detect_terminal(stream)
        assert info.is_notebook is True

    def test_no_ipython(self) -> None:
        stream = self._make_stream(True)
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            with patch("nyanbar.terminal._get_ipython_shell", return_value=None):
                info = detect_terminal(stream)
        assert info.is_notebook is False

    def test_terminal_interactive_shell(self) -> None:
        stream = self._make_stream(True)
        mock_shell = MagicMock()
        mock_shell.__class__ = type("TerminalInteractiveShell", (), {})
        with patch.dict(os.environ, {"TERM": "xterm"}, clear=False):
            with patch("nyanbar.terminal._get_ipython_shell", return_value=mock_shell):
                info = detect_terminal(stream)
        assert info.is_notebook is False

    # Default stream

    def test_default_stream_uses_stderr(self) -> None:
        """detect_terminal() with no args uses sys.stderr by default."""
        import sys
        with patch.object(sys, "stderr", self._make_stream(False)):
            info = detect_terminal()
        assert info.is_tty is False

    # Stream without isatty

    def test_stream_without_isatty(self) -> None:
        stream = MagicMock(spec=[])  # No isatty
        info = detect_terminal(stream)
        assert info.is_tty is False
