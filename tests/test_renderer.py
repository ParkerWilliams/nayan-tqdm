"""Tests for nyanbar.renderer — ANSI frame rendering."""
from __future__ import annotations

import io

import pytest

from nyanbar.renderer import (
    CURSOR_UP,
    ERASE_LINE,
    RESET,
    ensure_reset,
    erase_lines,
    has_unclosed_ansi,
    render_frame,
)


# ── erase_lines ─────────────────────────────────────────────


class TestEraseLines:
    """erase_lines clears previously rendered lines via ANSI sequences."""

    def test_zero_count_noop(self) -> None:
        buf = io.StringIO()
        erase_lines(buf, 0)
        assert buf.getvalue() == ""

    def test_negative_count_noop(self) -> None:
        buf = io.StringIO()
        erase_lines(buf, -1)
        assert buf.getvalue() == ""

    def test_single_line_erase(self) -> None:
        buf = io.StringIO()
        erase_lines(buf, 1)
        output = buf.getvalue()
        assert "\033[1A" in output  # cursor up 1
        assert ERASE_LINE in output

    def test_multi_line_erase(self) -> None:
        buf = io.StringIO()
        erase_lines(buf, 3)
        output = buf.getvalue()
        assert "\033[3A" in output  # cursor up 3
        assert output.count(ERASE_LINE) == 3


# ── render_frame ─────────────────────────────────────────────


class TestRenderFrame:
    """render_frame outputs lines and returns height for next erase."""

    def test_first_render_no_erase(self) -> None:
        buf = io.StringIO()
        height = render_frame(["hello", "world"], 0, buf)
        output = buf.getvalue()
        assert height == 2
        assert "hello" in output
        assert "world" in output
        # No cursor-up on first render
        assert "\033[" not in output.split("hello")[0]

    def test_second_render_erases_previous(self) -> None:
        buf = io.StringIO()
        height = render_frame(["new"], 3, buf)
        output = buf.getvalue()
        assert height == 1
        assert "\033[3A" in output  # erase previous 3 lines
        assert output.count(ERASE_LINE) == 3

    def test_height_transition_3_to_2(self) -> None:
        buf = io.StringIO()
        height = render_frame(["a", "b"], 3, buf)
        assert height == 2
        output = buf.getvalue()
        assert "\033[3A" in output
        assert output.count(ERASE_LINE) == 3

    def test_height_transition_1_to_3(self) -> None:
        buf = io.StringIO()
        height = render_frame(["a", "b", "c"], 1, buf)
        assert height == 3
        output = buf.getvalue()
        assert "\033[1A" in output
        assert output.count(ERASE_LINE) == 1

    def test_returns_line_count(self) -> None:
        buf = io.StringIO()
        assert render_frame(["x"], 0, buf) == 1
        buf2 = io.StringIO()
        assert render_frame(["a", "b", "c", "d"], 0, buf2) == 4

    def test_flushes_stream(self) -> None:
        buf = io.StringIO()
        render_frame(["hi"], 0, buf)
        # StringIO.flush is a no-op but calling it should not error
        assert buf.getvalue() != ""


# ── ensure_reset ─────────────────────────────────────────────


class TestEnsureReset:
    """ensure_reset appends RESET if ANSI sequences are present but unclosed."""

    def test_plain_text_unchanged(self) -> None:
        assert ensure_reset("hello") == "hello"

    def test_already_reset_unchanged(self) -> None:
        line = "\033[31mhello\033[0m"
        assert ensure_reset(line) == line

    def test_adds_reset_to_unclosed(self) -> None:
        line = "\033[31mhello"
        result = ensure_reset(line)
        assert result.endswith(RESET)

    def test_empty_string(self) -> None:
        assert ensure_reset("") == ""

    def test_only_reset_code(self) -> None:
        assert ensure_reset("\033[0m") == "\033[0m"


# ── has_unclosed_ansi ────────────────────────────────────────


class TestHasUnclosedAnsi:
    """has_unclosed_ansi detects color sequences without matching reset."""

    def test_clean_text(self) -> None:
        assert has_unclosed_ansi("hello") is False

    def test_properly_closed(self) -> None:
        assert has_unclosed_ansi("\033[31mhello\033[0m") is False

    def test_unclosed_red(self) -> None:
        assert has_unclosed_ansi("\033[31mhello") is True

    def test_unclosed_bold(self) -> None:
        assert has_unclosed_ansi("\033[1mtext") is True

    def test_empty_string(self) -> None:
        assert has_unclosed_ansi("") is False

    def test_multiple_opens_one_close(self) -> None:
        # \033[0m resets ALL attributes, so this is closed
        assert has_unclosed_ansi("\033[1m\033[31mtext\033[0m") is False

    def test_no_ansi_at_all(self) -> None:
        assert has_unclosed_ansi("plain text") is False
