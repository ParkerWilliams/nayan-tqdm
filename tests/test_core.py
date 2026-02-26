"""Tests for nyanbar.core — NyanBar class with tqdm-compatible API."""
from __future__ import annotations

import io
from unittest.mock import patch, MagicMock

import pytest

from nyanbar.core import NyanBar
from nyanbar.terminal import TerminalInfo, ColorTier


def _mock_tty_terminal() -> TerminalInfo:
    """Return a mock TTY terminal info."""
    return TerminalInfo(
        is_tty=True,
        color_support=ColorTier.COLOR_256,
        width=80,
        is_notebook=False,
    )


def _mock_non_tty_terminal() -> TerminalInfo:
    """Return a mock non-TTY terminal info."""
    return TerminalInfo(
        is_tty=False,
        color_support=ColorTier.NONE,
        width=80,
        is_notebook=False,
    )


# ── Constructor tests ────────────────────────────────────────


class TestConstructor:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_default_params(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), file=sio)
        assert bar.total == 10  # inferred from len(range(10))
        assert bar.unit == "it"
        assert bar.leave is True
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_explicit_total(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(iter([1, 2, 3]), total=3, file=sio)
        assert bar.total == 3
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_unknown_kwargs_swallowed(self, mock_dt):
        sio = io.StringIO()
        # Should not raise any error
        bar = NyanBar(range(10), colour="red", gui=True, file=sio)
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_bar_format_accepted_ignored(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), bar_format="{l_bar}", file=sio)
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_disable_true(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), disable=True, file=sio)
        assert sio.getvalue() == ""
        bar.close()


# ── Iteration tests ──────────────────────────────────────────


class TestIteration:
    def test_iter_yields_all_items(self):
        result = list(NyanBar(range(5), disable=True))
        assert result == [0, 1, 2, 3, 4]

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_iter_calls_close(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), file=sio)
        list(bar)
        assert bar._closed is True

    def test_iter_no_iterable_raises(self):
        bar = NyanBar(total=10, disable=True)
        with pytest.raises(TypeError):
            list(bar)  # advancing the generator triggers TypeError


# ── Update tests ─────────────────────────────────────────────


class TestUpdate:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_update_increments_n(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio)
        bar.update(5)
        assert bar.n == 5
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_update_default_one(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio)
        bar.update()
        assert bar.n == 1
        bar.close()


# ── Close tests ──────────────────────────────────────────────


class TestClose:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_close_idempotent(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), file=sio)
        bar.close()
        output1 = sio.getvalue()
        bar.close()
        output2 = sio.getvalue()
        assert output1 == output2  # second close adds nothing

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_close_leave_true(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=True, file=sio)
        list(bar)
        output = sio.getvalue()
        assert output.endswith("\n")

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_close_leave_false(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=False, file=sio)
        list(bar)
        output = sio.getvalue()
        # Should contain erase sequences
        assert "\033[" in output


# ── Context manager tests ────────────────────────────────────


class TestContextManager:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_context_manager(self, mock_dt):
        sio = io.StringIO()
        with NyanBar(range(5), file=sio) as bar:
            pass
        assert bar._closed is True

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_exit_on_exception(self, mock_dt):
        sio = io.StringIO()
        with pytest.raises(RuntimeError):
            with NyanBar(range(10), file=sio) as bar:
                raise RuntimeError("test")
        assert bar._closed is True


# ── set_description / set_postfix tests ──────────────────────


class TestDescriptionPostfix:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_set_description(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio)
        bar.set_description("dl")
        output = sio.getvalue()
        assert "dl" in output
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_set_postfix_dict(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio)
        bar.set_postfix({"loss": 0.5})
        output = sio.getvalue()
        assert "loss=0.5" in output
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_set_postfix_str(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio)
        bar.set_postfix_str("custom")
        output = sio.getvalue()
        assert "custom" in output
        bar.close()


# ── API alias tests ──────────────────────────────────────────


class TestAliases:
    def test_tqdm_is_nyanbar(self):
        from nyanbar import tqdm
        assert tqdm is NyanBar

    def test_trange_returns_nyanbar(self):
        from nyanbar import trange
        bar = trange(5, disable=True)
        assert isinstance(bar, NyanBar)
        bar.close()
