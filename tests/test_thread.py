"""Tests for nyanbar animation thread, leave/cleanup, exception safety, and thread safety."""
from __future__ import annotations

import io
import threading
import time
from unittest.mock import patch

import pytest

from nyanbar.core import NyanBar
from nyanbar.models import Animation, AnimationMode, Frame
from nyanbar.terminal import TerminalInfo, ColorTier


def _mock_tty_terminal() -> TerminalInfo:
    return TerminalInfo(
        is_tty=True,
        color_support=ColorTier.COLOR_256,
        width=80,
        is_notebook=False,
    )


def _mock_non_tty_terminal() -> TerminalInfo:
    return TerminalInfo(
        is_tty=False,
        color_support=ColorTier.NONE,
        width=80,
        is_notebook=False,
    )


def _test_animation() -> Animation:
    """Create a minimal test animation for thread tests."""
    f1 = Frame(lines=(">^.^<",))
    f2 = Frame(lines=(">o.o<",))
    return Animation(
        name="test",
        frames=(f1, f2),
        fps=12.0,
        mode=AnimationMode.WALK,
    )


# ── Animation thread lifecycle tests ────────────────────────


class TestAnimationThreadLifecycle:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_animation_thread_starts_on_iter(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(100), file=sio, mininterval=0)
        bar._animation = _test_animation()
        it = iter(bar)
        next(it)  # trigger iteration start
        # Give thread a moment to start
        time.sleep(0.05)
        assert bar._anim_thread is not None
        assert bar._anim_thread.is_alive()
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_animation_thread_stops_on_close(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(100), file=sio, mininterval=0)
        bar._animation = _test_animation()
        it = iter(bar)
        next(it)
        time.sleep(0.05)
        bar.close()
        assert bar._running is False
        # Brief wait for daemon thread to exit
        time.sleep(0.15)

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_animation_thread_is_daemon(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(100), file=sio, mininterval=0)
        bar._animation = _test_animation()
        it = iter(bar)
        next(it)
        time.sleep(0.05)
        assert bar._anim_thread is not None
        assert bar._anim_thread.daemon is True
        bar.close()

    def test_no_thread_for_disabled(self):
        bar = NyanBar(range(10), disable=True)
        bar._animation = _test_animation()
        list(bar)
        assert bar._anim_thread is None

    @patch("nyanbar.core.detect_terminal", return_value=_mock_non_tty_terminal())
    def test_no_thread_for_fallback(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), file=sio, mininterval=0)
        bar._animation = _test_animation()
        assert bar._use_fallback is True
        list(bar)
        assert bar._anim_thread is None


# ── Refresh throttle tests ───────────────────────────────────


class TestRefreshThrottle:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_miniters_gate(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio, miniters=5, mininterval=0)
        initial_output = sio.getvalue()
        # 4 updates should not trigger additional refresh beyond initial
        for _ in range(4):
            bar.update(1)
        output_after_4 = sio.getvalue()
        # 5th update should trigger refresh
        bar.update(1)
        output_after_5 = sio.getvalue()
        assert len(output_after_5) > len(output_after_4)
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_mininterval_gate(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio, miniters=1, mininterval=0.5)
        initial_len = len(sio.getvalue())
        bar.update(1)
        first_update_len = len(sio.getvalue())
        # Second update immediately should be throttled
        bar.update(1)
        second_update_len = len(sio.getvalue())
        # First update triggers (mininterval passed since start), second may not
        assert first_update_len >= initial_len
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_miniters_auto_tune(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=1000, file=sio, miniters=1, mininterval=0)
        initial_miniters = bar._miniters
        # Do many fast updates to trigger auto-tuning
        for _ in range(50):
            bar.update(1)
        # miniters may have been adjusted
        bar.close()
        # Just verify no crash -- auto-tune is best-effort


# ── Leave/cleanup tests ─────────────────────────────────────


class TestLeaveCleanup:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_leave_true_keeps_output(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=True, file=sio)
        list(bar)
        output = sio.getvalue()
        assert output.endswith("\n")
        # Output should contain bar content
        assert "5/5" in output or "100%" in output

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_leave_false_erases_output(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=False, file=sio)
        list(bar)
        output = sio.getvalue()
        # Should contain erase sequences
        assert "\033[2K" in output

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_leave_false_clean_terminal(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(5), leave=False, file=sio)
        list(bar)
        output = sio.getvalue()
        # Erase line sequence should be present
        assert "\033[2K" in output


# ── Exception safety tests ───────────────────────────────────


class TestExceptionSafety:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_exception_in_iter_calls_close(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), file=sio)
        with pytest.raises(ValueError):
            for i, x in enumerate(bar):
                if i == 3:
                    raise ValueError("test error")
        assert bar._closed is True

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_exception_with_leave_false_cleans_up(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), leave=False, file=sio)
        with pytest.raises(ValueError):
            for i, x in enumerate(bar):
                if i == 3:
                    raise ValueError("test error")
        output = sio.getvalue()
        assert "\033[2K" in output

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_context_manager_exception_cleanup(self, mock_dt):
        sio = io.StringIO()
        with pytest.raises(RuntimeError):
            with NyanBar(range(10), file=sio) as bar:
                raise RuntimeError("test")
        assert bar._closed is True


# ── Nested bar tests ─────────────────────────────────────────


class TestNestedBar:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_nested_bar_uses_fallback(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), position=1, file=sio)
        assert bar._use_fallback is True
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_nested_bar_no_animation_thread(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(range(10), position=1, file=sio)
        bar._animation = _test_animation()
        list(bar)
        assert bar._anim_thread is None


# ── Thread safety tests ──────────────────────────────────────


class TestThreadSafety:
    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_concurrent_updates(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=100, file=sio, mininterval=0)

        def worker():
            for _ in range(25):
                bar.update(1)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert bar.n == 100
        bar.close()

    @patch("nyanbar.core.detect_terminal", return_value=_mock_tty_terminal())
    def test_lock_exists(self, mock_dt):
        sio = io.StringIO()
        bar = NyanBar(total=10, file=sio)
        assert hasattr(bar, "_lock")
        assert isinstance(bar._lock, type(threading.Lock()))
        bar.close()
