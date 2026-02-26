"""Tests for nyanbar.utils — display width and ANSI stripping."""
from __future__ import annotations

import pytest

from nyanbar.utils import disp_len, strip_ansi


# ── strip_ansi ──────────────────────────────────────────────


class TestStripAnsi:
    """strip_ansi removes ANSI escape sequences, preserving plain text."""

    def test_removes_sgr_color(self) -> None:
        assert strip_ansi("\033[31mhello\033[0m") == "hello"

    def test_removes_bold_and_color(self) -> None:
        assert strip_ansi("\033[1;34mworld\033[0m") == "world"

    def test_removes_cursor_movement(self) -> None:
        assert strip_ansi("\033[2K\033[1A") == ""

    def test_preserves_plain_text(self) -> None:
        assert strip_ansi("hello world") == "hello world"

    def test_handles_empty_string(self) -> None:
        assert strip_ansi("") == ""

    def test_handles_adjacent_sequences(self) -> None:
        assert strip_ansi("\033[31m\033[1mhi\033[0m") == "hi"

    def test_removes_erase_line(self) -> None:
        assert strip_ansi("\033[2Ktext") == "text"

    def test_removes_256_color(self) -> None:
        assert strip_ansi("\033[38;5;196mred\033[0m") == "red"

    def test_removes_truecolor(self) -> None:
        assert strip_ansi("\033[38;2;255;0;0mred\033[0m") == "red"


# ── disp_len ────────────────────────────────────────────────


class TestDispLen:
    """disp_len returns terminal display width, not Python len()."""

    def test_ascii_text(self) -> None:
        assert disp_len("hello") == 5

    def test_empty_string(self) -> None:
        assert disp_len("") == 0

    def test_cjk_wide_chars(self) -> None:
        # 世界 — two CJK chars, each 2 columns
        assert disp_len("\u4e16\u754c") == 4

    def test_emoji_wide(self) -> None:
        # 😀 — fullwidth emoji, 2 columns
        assert disp_len("\U0001f600") == 2

    def test_mixed_ascii_cjk(self) -> None:
        # "hi世界" — 2 ASCII + 2 CJK wide = 6
        assert disp_len("hi\u4e16\u754c") == 6

    def test_combining_diacritical_marks(self) -> None:
        # e + combining acute accent = 1 visible char
        assert disp_len("e\u0301") == 1

    def test_ansi_sequences_ignored(self) -> None:
        # ANSI color codes should not contribute to width
        assert disp_len("\033[31mhi\033[0m") == 2

    def test_ansi_with_cjk(self) -> None:
        # ANSI + CJK: only CJK width counts
        assert disp_len("\033[31m\u4e16\u754c\033[0m") == 4

    def test_tab_counts_as_one(self) -> None:
        # Tab is a single char column in our measurement
        assert disp_len("\t") == 1

    def test_multiple_combining_marks(self) -> None:
        # a + combining grave + combining acute = 1 visible char
        assert disp_len("a\u0300\u0301") == 1

    def test_fullwidth_latin(self) -> None:
        # Ａ (fullwidth A, U+FF21) = 2 columns
        assert disp_len("\uff21") == 2

    def test_halfwidth_katakana(self) -> None:
        # ｱ (halfwidth katakana, U+FF71) = 1 column
        assert disp_len("\uff71") == 1
