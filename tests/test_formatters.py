"""Tests for nyanbar.formatters — stats formatting utilities."""
from __future__ import annotations

import pytest

from nyanbar.formatters import EMA, si_format, format_interval, format_meter
from nyanbar.utils import strip_ansi


# ── EMA class tests ──────────────────────────────────────────


class TestEMA:
    def test_ema_value_none_initially(self):
        ema = EMA(alpha=0.3)
        assert ema.value is None

    def test_ema_first_sample_is_seed(self):
        ema = EMA(alpha=0.3)
        ema.update(10.0)
        assert ema.value == 10.0

    def test_ema_smoothing(self):
        ema = EMA(alpha=0.3)
        for v in [10, 20, 10, 20, 10]:
            ema.update(v)
        assert 10.0 < ema.value < 20.0

    def test_ema_converges(self):
        ema = EMA(alpha=0.3)
        for _ in range(20):
            ema.update(5.0)
        assert abs(ema.value - 5.0) < 0.01


# ── si_format tests ──────────────────────────────────────────


class TestSiFormat:
    def test_si_small_value(self):
        assert si_format(42.0) == "42.00"

    def test_si_kilo(self):
        assert si_format(1500.0) == "1.50k"

    def test_si_mega(self):
        assert si_format(2_500_000.0) == "2.50M"

    def test_si_giga(self):
        assert si_format(3_000_000_000.0) == "3.00G"

    def test_si_precision(self):
        assert si_format(1500.0, precision=1) == "1.5k"

    def test_si_zero(self):
        assert si_format(0.0) == "0.00"

    def test_si_negative(self):
        assert si_format(-1500.0) == "-1.50k"


# ── format_interval tests ────────────────────────────────────


class TestFormatInterval:
    def test_interval_seconds(self):
        assert format_interval(42) == "00:42"

    def test_interval_minutes(self):
        assert format_interval(65) == "01:05"

    def test_interval_hours(self):
        assert format_interval(3661) == "1:01:01"

    def test_interval_zero(self):
        assert format_interval(0) == "00:00"

    def test_interval_float_truncation(self):
        assert format_interval(65.9) == "01:05"


# ── format_meter tests ───────────────────────────────────────


class TestFormatMeter:
    def test_meter_determinate(self):
        result = format_meter(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
        )
        assert "50%" in result
        assert "50/100" in result
        assert "00:05" in result
        assert "10.00it/s" in result
        # Bar portion present
        assert "|" in result

    def test_meter_indeterminate(self):
        result = format_meter(
            n=1000, total=None, elapsed=5.0, rate=200.0, unit="it",
        )
        assert "1000it" in result
        assert "00:05" in result
        assert "200.00it/s" in result
        # No percentage or bar for indeterminate
        assert "%" not in result

    def test_meter_no_rate(self):
        result = format_meter(
            n=0, total=100, elapsed=0.0, rate=None, unit="it", ncols=80,
        )
        assert "?it/s" in result
        assert "?" in result  # ETA should be "?"

    def test_meter_with_desc(self):
        result = format_meter(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
            ncols=80, desc="download",
        )
        assert result.startswith("download: ")

    def test_meter_with_postfix(self):
        result = format_meter(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it",
            ncols=80, postfix_str="loss=0.5",
        )
        assert "loss=0.5" in result

    def test_meter_unit_scale(self):
        result = format_meter(
            n=1500, total=10000, elapsed=5.0, rate=300.0, unit="B",
            ncols=80, unit_scale=True,
        )
        assert "1.50k" in result
        assert "10.00k" in result

    def test_meter_bar_width(self):
        result = format_meter(
            n=50, total=100, elapsed=5.0, rate=10.0, unit="it", ncols=80,
        )
        # Bar should have # characters proportional to 50% progress
        # Find the bar portion between | delimiters
        parts = result.split("|")
        assert len(parts) >= 3
        bar_part = parts[1]
        hashes = bar_part.count("#")
        spaces = bar_part.count(" ")
        total_bar = hashes + spaces
        assert total_bar > 0
        # 50% progress means roughly half filled
        ratio = hashes / total_bar
        assert 0.4 <= ratio <= 0.6
