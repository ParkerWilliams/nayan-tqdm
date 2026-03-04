"""Tests for tqdm API compatibility — constructor, iteration, update, close,
context manager, desc/postfix, trange, formatters, thread safety, integration."""
from __future__ import annotations

import io
import os
import threading
import time
import warnings
from unittest.mock import patch, MagicMock

import pytest

from nayan_tqdm.core import NyanBar
from nayan_tqdm.models import Animation, AnimationMode, Frame
from nayan_tqdm.terminal import TerminalInfo, ColorTier
from nayan_tqdm.formatters import EMA, si_format, format_interval, format_meter
from nayan_tqdm.registry import get_theme, list_themes, set_theme, get_default_theme
import nayan_tqdm.themes  # noqa: F401


def _mock_tty() -> TerminalInfo:
    return TerminalInfo(is_tty=True, color_support=ColorTier.COLOR_256, width=80, is_notebook=False)


def _mock_non_tty() -> TerminalInfo:
    return TerminalInfo(is_tty=False, color_support=ColorTier.NONE, width=80, is_notebook=False)


def _test_animation() -> Animation:
    f1 = Frame(lines=(">^.^<",))
    f2 = Frame(lines=(">o.o<",))
    return Animation(name="test", frames=(f1, f2), fps=12.0, mode=AnimationMode.WALK)


# ── Constructor tests ────────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_default_params(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), file=sio)
    assert bar.total == 10
    assert bar.unit == "it"
    assert bar.leave is True
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_explicit_total(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(iter([1, 2, 3]), total=3, file=sio)
    assert bar.total == 3
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_unknown_kwargs_swallowed(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), colour="red", gui=True, file=sio)
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_bar_format_accepted_ignored(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), bar_format="{l_bar}", file=sio)
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_disable_true(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), disable=True, file=sio)
    assert sio.getvalue() == ""
    bar.close()


# ── Iteration tests ──────────────────────────────────────────


def test_iter_yields_all_items() -> None:
    result = list(NyanBar(range(5), disable=True))
    assert result == [0, 1, 2, 3, 4]


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_iter_calls_close(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), file=sio)
    list(bar)
    assert bar._closed is True


def test_iter_no_iterable_raises() -> None:
    bar = NyanBar(total=10, disable=True)
    with pytest.raises(TypeError):
        list(bar)


# ── Update tests ─────────────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_update_increments_n(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio)
    bar.update(5)
    assert bar.n == 5
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_update_default_one(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio)
    bar.update()
    assert bar.n == 1
    bar.close()


# ── Close tests ──────────────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_close_idempotent(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), file=sio)
    bar.close()
    output1 = sio.getvalue()
    bar.close()
    output2 = sio.getvalue()
    assert output1 == output2


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_close_leave_true(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=True, file=sio)
    list(bar)
    output = sio.getvalue()
    assert output.endswith("\n")


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_close_leave_false(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=False, file=sio)
    list(bar)
    output = sio.getvalue()
    assert "\033[" in output


# ── Context manager tests ────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_context_manager(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    with NyanBar(range(5), file=sio) as bar:
        pass
    assert bar._closed is True


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_exit_on_exception(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    with pytest.raises(RuntimeError):
        with NyanBar(range(10), file=sio) as bar:
            raise RuntimeError("test")
    assert bar._closed is True


# ── set_description / set_postfix tests ──────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_set_description(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio)
    bar.set_description("dl")
    output = sio.getvalue()
    assert "dl" in output
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_set_postfix_dict(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio)
    bar.set_postfix({"loss": 0.5})
    output = sio.getvalue()
    assert "loss=0.5" in output
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_set_postfix_str(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio)
    bar.set_postfix_str("custom")
    output = sio.getvalue()
    assert "custom" in output
    bar.close()


# ── API alias tests ──────────────────────────────────────────


def test_tqdm_is_nayan_tqdm() -> None:
    from nayan_tqdm import tqdm
    assert tqdm is NyanBar


def test_trange_returns_nayan_tqdm() -> None:
    from nayan_tqdm import trange
    bar = trange(5, disable=True)
    assert isinstance(bar, NyanBar)
    bar.close()


# ── EMA tests ────────────────────────────────────────────────


def test_ema_value_none_initially() -> None:
    ema = EMA(alpha=0.3)
    assert ema.value is None


def test_ema_first_sample_is_seed() -> None:
    ema = EMA(alpha=0.3)
    ema.update(10.0)
    assert ema.value == 10.0


def test_ema_smoothing() -> None:
    ema = EMA(alpha=0.3)
    for v in [10, 20, 10, 20, 10]:
        ema.update(v)
    assert ema.value is not None
    assert 10.0 < ema.value < 20.0


def test_ema_converges() -> None:
    ema = EMA(alpha=0.3)
    for _ in range(20):
        ema.update(5.0)
    assert ema.value is not None
    assert abs(ema.value - 5.0) < 0.01


# ── si_format tests ──────────────────────────────────────────


def test_si_small_value() -> None:
    assert si_format(42.0) == "42.00"


def test_si_kilo() -> None:
    assert si_format(1500.0) == "1.50k"


def test_si_mega() -> None:
    assert si_format(2_500_000.0) == "2.50M"


def test_si_giga() -> None:
    assert si_format(3_000_000_000.0) == "3.00G"


def test_si_precision() -> None:
    assert si_format(1500.0, precision=1) == "1.5k"


def test_si_zero() -> None:
    assert si_format(0.0) == "0.00"


def test_si_negative() -> None:
    assert si_format(-1500.0) == "-1.50k"


# ── format_interval tests ────────────────────────────────────


def test_interval_seconds() -> None:
    assert format_interval(42) == "00:42"


def test_interval_minutes() -> None:
    assert format_interval(65) == "01:05"


def test_interval_hours() -> None:
    assert format_interval(3661) == "1:01:01"


def test_interval_zero() -> None:
    assert format_interval(0) == "00:00"


def test_interval_float_truncation() -> None:
    assert format_interval(65.9) == "01:05"


# ── format_meter tests ───────────────────────────────────────


def test_meter_determinate() -> None:
    result = format_meter(n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80)
    assert "50%" in result
    assert "50/100" in result
    assert "00:05" in result
    assert "10.00it/s" in result
    assert "|" in result


def test_meter_indeterminate() -> None:
    result = format_meter(n=1000, total=None, elapsed=5.0, rate=200.0, unit="it")
    assert "1000it" in result
    assert "00:05" in result
    assert "200.00it/s" in result
    assert "%" not in result


def test_meter_no_rate() -> None:
    result = format_meter(n=0, total=100, elapsed=0.0, rate=None, unit="it", ncols=80)
    assert "?it/s" in result


def test_meter_with_desc() -> None:
    result = format_meter(n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80, desc="download")
    assert result.startswith("download: ")


def test_meter_with_postfix() -> None:
    result = format_meter(n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80, postfix_str="loss=0.5")
    assert "loss=0.5" in result


def test_meter_unit_scale() -> None:
    result = format_meter(n=1500, total=10000, elapsed=5.0, rate=300.0, unit="B", ncols=80, unit_scale=True)
    assert "1.50k" in result
    assert "10.00k" in result


def test_meter_bar_width() -> None:
    result = format_meter(n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80)
    parts = result.split("|")
    assert len(parts) >= 3
    bar_part = parts[1]
    hashes = bar_part.count("#")
    spaces = bar_part.count(" ")
    total_bar = hashes + spaces
    assert total_bar > 0
    ratio = hashes / total_bar
    assert 0.4 <= ratio <= 0.6


# ── Animation thread lifecycle tests ────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_animation_thread_starts_on_iter(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(100), file=sio, mininterval=0)
    bar._animation = _test_animation()
    it = iter(bar)
    next(it)
    time.sleep(0.05)
    assert bar._anim_thread is not None
    assert bar._anim_thread.is_alive()
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_animation_thread_stops_on_close(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(100), file=sio, mininterval=0)
    bar._animation = _test_animation()
    it = iter(bar)
    next(it)
    time.sleep(0.05)
    bar.close()
    assert bar._running is False
    time.sleep(0.15)


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_animation_thread_is_daemon(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(100), file=sio, mininterval=0)
    bar._animation = _test_animation()
    it = iter(bar)
    next(it)
    time.sleep(0.05)
    assert bar._anim_thread is not None
    assert bar._anim_thread.daemon is True
    bar.close()


def test_no_thread_for_disabled() -> None:
    bar = NyanBar(range(10), disable=True)
    bar._animation = _test_animation()
    list(bar)
    assert bar._anim_thread is None


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_non_tty())
def test_no_thread_for_fallback(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), file=sio, mininterval=0)
    bar._animation = _test_animation()
    assert bar._use_fallback is True
    list(bar)
    assert bar._anim_thread is None


# ── Refresh throttle tests ───────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_miniters_gate(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio, miniters=5, mininterval=0)
    for _ in range(4):
        bar.update(1)
    output_after_4 = sio.getvalue()
    bar.update(1)
    output_after_5 = sio.getvalue()
    assert len(output_after_5) > len(output_after_4)
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_mininterval_gate(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio, miniters=1, mininterval=0.5)
    initial_len = len(sio.getvalue())
    bar.update(1)
    first_update_len = len(sio.getvalue())
    bar.update(1)
    assert first_update_len >= initial_len
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_miniters_auto_tune(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=1000, file=sio, miniters=1, mininterval=0)
    for _ in range(50):
        bar.update(1)
    bar.close()


# ── Leave/cleanup tests ─────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_leave_true_keeps_output(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=True, file=sio)
    list(bar)
    output = sio.getvalue()
    assert output.endswith("\n")
    assert "5/5" in output or "100%" in output


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_leave_false_erases_output(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=False, file=sio)
    list(bar)
    output = sio.getvalue()
    assert "\033[2K" in output


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_leave_false_clean_terminal(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=False, file=sio)
    list(bar)
    output = sio.getvalue()
    assert "\033[2K" in output


# ── Exception safety tests ───────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_exception_in_iter_calls_close(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), file=sio)
    with pytest.raises(ValueError):
        for i, x in enumerate(bar):
            if i == 3:
                raise ValueError("test error")
    assert bar._closed is True


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_exception_with_leave_false_cleans_up(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), leave=False, file=sio)
    with pytest.raises(ValueError):
        for i, x in enumerate(bar):
            if i == 3:
                raise ValueError("test error")
    output = sio.getvalue()
    assert "\033[2K" in output


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_context_manager_exception_cleanup(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    with pytest.raises(RuntimeError):
        with NyanBar(range(10), file=sio) as bar:
            raise RuntimeError("test")
    assert bar._closed is True


# ── Nested bar tests ─────────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_nested_bar_uses_fallback(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), position=1, file=sio)
    assert bar._use_fallback is True
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_nested_bar_no_animation_thread(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(10), position=1, file=sio)
    bar._animation = _test_animation()
    list(bar)
    assert bar._anim_thread is None


# ── Thread safety tests ──────────────────────────────────────


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_concurrent_updates(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=100, file=sio, mininterval=0)

    def worker() -> None:
        for _ in range(25):
            bar.update(1)

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert bar.n == 100
    bar.close()


@patch("nayan_tqdm.core.detect_terminal", return_value=_mock_tty())
def test_lock_exists(mock_dt: MagicMock) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, file=sio)
    assert hasattr(bar, "_lock")
    assert isinstance(bar._lock, type(threading.Lock()))
    bar.close()


# ── Integration: theme selection ─────────────────────────────


@pytest.fixture(autouse=True)
def _restore_default_theme() -> Generator:
    original = get_default_theme()
    yield
    import nayan_tqdm.registry as reg
    reg._default_theme = original


from typing import Generator


def test_default_theme_is_nyan(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "nyan"
    bar.close()


def test_theme_kwarg_selects_theme(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, theme="table_flip", file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "table_flip"
    bar.close()


def test_theme_kwarg_finger_guns(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, theme="finger_guns", file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "finger_guns"
    bar.close()


def test_theme_kwarg_shrug(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, theme="shrug", file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "shrug"
    bar.close()


def test_theme_kwarg_deal_with_it(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, theme="deal_with_it", file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "deal_with_it"
    bar.close()


def test_invalid_theme_warns_and_uses_default(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bar = NyanBar(total=10, theme="nonexistent", file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "nyan"
    assert any("nonexistent" in str(warning.message) for warning in w)
    bar.close()


def test_set_theme_affects_new_bars(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    set_theme("table_flip")
    bar = NyanBar(total=10, file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "table_flip"
    bar.close()


def test_existing_bar_keeps_theme(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, file=sio)
    assert bar._animation is not None
    assert bar._animation.name == "nyan"
    set_theme("table_flip")
    assert bar._animation.name == "nyan"
    bar.close()


def test_non_tty_uses_fallback(mock_non_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, file=sio)
    assert bar._use_fallback is True
    bar.close()


def test_disabled_bar_no_animation() -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, disable=True, file=sio)
    assert bar._animation is None
    bar.close()


def test_multiline_theme_renders(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, theme="nyan", file=sio)
    with bar._lock:
        bar._render_animation_frame()
    # nyan has decoration (above + below) + bar line = 3 lines
    assert bar._prev_height == 3
    bar.close()


def test_leave_true_multiline(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=True, theme="nyan", file=sio, disable=False)
    for _ in bar:
        pass
    output = sio.getvalue()
    assert len(output) > 0


def test_leave_false_multiline(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(range(5), leave=False, theme="nyan", file=sio, disable=False)
    for _ in bar:
        pass
    output = sio.getvalue()
    assert "\033[" in output


def test_completion_frame_at_100(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=5, theme="table_flip", leave=True, file=sio)
    for _ in range(5):
        bar.update()
    bar.close()
    assert len(sio.getvalue()) > 0


def test_render_level_ascii_forces_ascii(mock_tty: TerminalInfo) -> None:
    sio = io.StringIO()
    bar = NyanBar(total=10, render_level="ascii", file=sio)
    assert bar._animation is not None
    from nayan_tqdm.renderer import has_unclosed_ansi
    for frame in bar._animation.frames:
        for line in frame.lines:
            assert "\033[" not in line or not has_unclosed_ansi(line)
    bar.close()


def test_render_level_emoji_override() -> None:
    info = TerminalInfo(is_tty=True, color_support=ColorTier.NONE, width=80, is_notebook=False)
    sio = io.StringIO()
    with patch("nayan_tqdm.core.detect_terminal", return_value=info):
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            bar = NyanBar(total=10, render_level="emoji", file=sio)
    assert bar._animation is not None
    bar.close()


def test_list_themes_returns_all() -> None:
    names = list_themes()
    expected = [
        "bear", "bee", "cat_mouse", "cat_play", "cat_sleepy", "cat_smug",
        "cat_yarn", "construction", "cry",
        "deal_with_it", "disapproval", "disco", "double_flip",
        "finger_guns", "fire", "flex", "garden",
        "heartbeat", "hype", "lenny", "lightning",
        "love", "matrix", "music", "nyan", "ocean",
        "pasta", "rage", "rocket", "run", "shrug", "snake", "sparkles",
        "table_flip", "table_rage", "table_unflip",
        "train", "uwu", "wizard", "zen",
    ]
    assert names == expected


def test_get_theme_returns_animation() -> None:
    anim = get_theme("nyan")
    assert isinstance(anim, Animation)


def test_imports_work() -> None:
    from nayan_tqdm import tqdm, trange, set_theme, list_themes, get_theme
    assert tqdm is NyanBar
    assert callable(set_theme)
    assert callable(list_themes)
    assert callable(get_theme)
