"""Tests for ANSI renderer output, display width, animation engine."""
from __future__ import annotations

import io

import pytest

from nyanbar.utils import disp_len, strip_ansi
from nyanbar.renderer import (
    CURSOR_UP, ERASE_LINE, RESET,
    ensure_reset, erase_lines, has_unclosed_ansi, render_frame,
)
from nyanbar.engine import (
    cycle_position, fill_pattern, render_animation,
    select_frame_index, walk_position,
)
from nyanbar.models import Animation, AnimationMode, Frame


# ── strip_ansi ──────────────────────────────────────────────


def test_strip_ansi_removes_sgr_color() -> None:
    assert strip_ansi("\033[31mhello\033[0m") == "hello"


def test_strip_ansi_removes_bold_and_color() -> None:
    assert strip_ansi("\033[1;34mworld\033[0m") == "world"


def test_strip_ansi_removes_cursor_movement() -> None:
    assert strip_ansi("\033[2K\033[1A") == ""


def test_strip_ansi_preserves_plain_text() -> None:
    assert strip_ansi("hello world") == "hello world"


def test_strip_ansi_handles_empty_string() -> None:
    assert strip_ansi("") == ""


def test_strip_ansi_handles_adjacent_sequences() -> None:
    assert strip_ansi("\033[31m\033[1mhi\033[0m") == "hi"


def test_strip_ansi_removes_erase_line() -> None:
    assert strip_ansi("\033[2Ktext") == "text"


def test_strip_ansi_removes_256_color() -> None:
    assert strip_ansi("\033[38;5;196mred\033[0m") == "red"


def test_strip_ansi_removes_truecolor() -> None:
    assert strip_ansi("\033[38;2;255;0;0mred\033[0m") == "red"


# ── disp_len ────────────────────────────────────────────────


def test_disp_len_ascii_text() -> None:
    assert disp_len("hello") == 5


def test_disp_len_empty_string() -> None:
    assert disp_len("") == 0


def test_disp_len_cjk_wide_chars() -> None:
    assert disp_len("\u4e16\u754c") == 4


def test_disp_len_emoji_wide() -> None:
    assert disp_len("\U0001f600") == 2


def test_disp_len_mixed_ascii_cjk() -> None:
    assert disp_len("hi\u4e16\u754c") == 6


def test_disp_len_combining_diacritical_marks() -> None:
    assert disp_len("e\u0301") == 1


def test_disp_len_ansi_sequences_ignored() -> None:
    assert disp_len("\033[31mhi\033[0m") == 2


def test_disp_len_ansi_with_cjk() -> None:
    assert disp_len("\033[31m\u4e16\u754c\033[0m") == 4


def test_disp_len_tab_counts_as_one() -> None:
    assert disp_len("\t") == 1


def test_disp_len_multiple_combining_marks() -> None:
    assert disp_len("a\u0300\u0301") == 1


def test_disp_len_fullwidth_latin() -> None:
    assert disp_len("\uff21") == 2


def test_disp_len_halfwidth_katakana() -> None:
    assert disp_len("\uff71") == 1


# ── erase_lines ─────────────────────────────────────────────


def test_erase_lines_zero_count_noop() -> None:
    buf = io.StringIO()
    erase_lines(buf, 0)
    assert buf.getvalue() == ""


def test_erase_lines_negative_count_noop() -> None:
    buf = io.StringIO()
    erase_lines(buf, -1)
    assert buf.getvalue() == ""


def test_erase_lines_single_line() -> None:
    buf = io.StringIO()
    erase_lines(buf, 1)
    output = buf.getvalue()
    assert "\033[1A" in output
    assert ERASE_LINE in output


def test_erase_lines_multi_line() -> None:
    buf = io.StringIO()
    erase_lines(buf, 3)
    output = buf.getvalue()
    assert "\033[3A" in output
    assert output.count(ERASE_LINE) == 3


# ── render_frame ─────────────────────────────────────────────


def test_render_frame_first_no_erase() -> None:
    buf = io.StringIO()
    height = render_frame(["hello", "world"], 0, buf)
    output = buf.getvalue()
    assert height == 2
    assert "hello" in output
    assert "world" in output
    assert "\033[" not in output.split("hello")[0]


def test_render_frame_second_erases_previous() -> None:
    buf = io.StringIO()
    height = render_frame(["new"], 3, buf)
    output = buf.getvalue()
    assert height == 1
    assert "\033[3A" in output
    assert output.count(ERASE_LINE) == 3


def test_render_frame_height_transition_3_to_2() -> None:
    buf = io.StringIO()
    height = render_frame(["a", "b"], 3, buf)
    assert height == 2
    output = buf.getvalue()
    assert "\033[3A" in output
    assert output.count(ERASE_LINE) == 3


def test_render_frame_height_transition_1_to_3() -> None:
    buf = io.StringIO()
    height = render_frame(["a", "b", "c"], 1, buf)
    assert height == 3
    output = buf.getvalue()
    assert "\033[1A" in output
    assert output.count(ERASE_LINE) == 1


def test_render_frame_returns_line_count() -> None:
    buf = io.StringIO()
    assert render_frame(["x"], 0, buf) == 1
    buf2 = io.StringIO()
    assert render_frame(["a", "b", "c", "d"], 0, buf2) == 4


def test_render_frame_flushes_stream() -> None:
    buf = io.StringIO()
    render_frame(["hi"], 0, buf)
    assert buf.getvalue() != ""


# ── ensure_reset ─────────────────────────────────────────────


def test_ensure_reset_plain_text_unchanged() -> None:
    assert ensure_reset("hello") == "hello"


def test_ensure_reset_already_reset_unchanged() -> None:
    line = "\033[31mhello\033[0m"
    assert ensure_reset(line) == line


def test_ensure_reset_adds_reset_to_unclosed() -> None:
    line = "\033[31mhello"
    result = ensure_reset(line)
    assert result.endswith(RESET)


def test_ensure_reset_empty_string() -> None:
    assert ensure_reset("") == ""


def test_ensure_reset_only_reset_code() -> None:
    assert ensure_reset("\033[0m") == "\033[0m"


# ── has_unclosed_ansi ────────────────────────────────────────


def test_has_unclosed_ansi_clean_text() -> None:
    assert has_unclosed_ansi("hello") is False


def test_has_unclosed_ansi_properly_closed() -> None:
    assert has_unclosed_ansi("\033[31mhello\033[0m") is False


def test_has_unclosed_ansi_unclosed_red() -> None:
    assert has_unclosed_ansi("\033[31mhello") is True


def test_has_unclosed_ansi_unclosed_bold() -> None:
    assert has_unclosed_ansi("\033[1mtext") is True


def test_has_unclosed_ansi_empty_string() -> None:
    assert has_unclosed_ansi("") is False


def test_has_unclosed_ansi_multiple_opens_one_close() -> None:
    assert has_unclosed_ansi("\033[1m\033[31mtext\033[0m") is False


def test_has_unclosed_ansi_no_ansi_at_all() -> None:
    assert has_unclosed_ansi("plain text") is False


# ── select_frame_index ──────────────────────────────────────


def test_frame_index_zero_elapsed() -> None:
    assert select_frame_index(4, 0.0, 12.0) == 0


def test_frame_index_basic_advance() -> None:
    assert select_frame_index(4, 0.1, 12.0) == 1


def test_frame_index_half_second() -> None:
    assert select_frame_index(4, 0.5, 12.0) == 2


def test_frame_index_wraps_around() -> None:
    assert select_frame_index(4, 1.0, 12.0) == 0


def test_frame_index_single_frame_always_zero() -> None:
    assert select_frame_index(1, 0.0, 12.0) == 0
    assert select_frame_index(1, 5.0, 12.0) == 0


def test_frame_index_custom_fps() -> None:
    assert select_frame_index(3, 0.5, 24.0) == 0
    assert select_frame_index(3, 0.25, 24.0) == 0


def test_frame_index_high_elapsed() -> None:
    idx = select_frame_index(4, 100.0, 12.0)
    assert 0 <= idx < 4


# ── walk_position ───────────────────────────────────────────


def test_walk_position_zero_progress() -> None:
    assert walk_position(0.0, 80, 5) == 0


def test_walk_position_full_progress() -> None:
    assert walk_position(1.0, 80, 5) == 75


def test_walk_position_half_progress() -> None:
    assert walk_position(0.5, 80, 5) == 37


def test_walk_position_clamp_negative() -> None:
    assert walk_position(-0.1, 80, 5) == 0


def test_walk_position_clamp_over_one() -> None:
    assert walk_position(1.5, 80, 5) == 75


def test_walk_position_sprite_fills_bar() -> None:
    assert walk_position(0.5, 5, 5) == 0
    assert walk_position(0.5, 5, 10) == 0


# ── cycle_position ──────────────────────────────────────────


def test_cycle_position_centered() -> None:
    assert cycle_position(80, 5) == 37


def test_cycle_position_narrow_bar() -> None:
    assert cycle_position(10, 8) == 1


def test_cycle_position_sprite_wider_than_bar() -> None:
    assert cycle_position(5, 10) == 0


# ── fill_pattern ────────────────────────────────────────────


def test_fill_pattern_basic_tiling() -> None:
    frame = Frame(lines=("ab",))
    result = fill_pattern(frame, 6)
    assert len(result) == 1
    assert result[0] == "ababab"


def test_fill_pattern_truncates_at_width() -> None:
    frame = Frame(lines=("abc",))
    result = fill_pattern(frame, 5)
    assert len(result) == 1
    assert result[0] == "abcab"


def test_fill_pattern_multiline() -> None:
    frame = Frame(lines=("ab", "cd"))
    result = fill_pattern(frame, 4)
    assert result == ["abab", "cdcd"]


def test_fill_pattern_empty_frame() -> None:
    frame = Frame(lines=())
    result = fill_pattern(frame, 10)
    assert result == []


def test_fill_pattern_exact_fit() -> None:
    frame = Frame(lines=("abc",))
    result = fill_pattern(frame, 6)
    assert result[0] == "abcabc"


# ── render_animation ────────────────────────────────────────


@pytest.fixture
def walk_anim() -> Animation:
    return Animation(
        name="test", frames=(Frame(lines=("=>",)), Frame(lines=("->",))),
        fps=12.0, mode=AnimationMode.WALK,
    )


@pytest.fixture
def cycle_anim() -> Animation:
    return Animation(
        name="test", frames=(Frame(lines=("*",)), Frame(lines=("+",))),
        fps=12.0, mode=AnimationMode.CYCLE,
    )


@pytest.fixture
def fill_anim() -> Animation:
    return Animation(
        name="test", frames=(Frame(lines=("ab",)),),
        fps=12.0, mode=AnimationMode.FILL,
    )


def test_walk_at_zero_progress(walk_anim: Animation) -> None:
    lines = render_animation(walk_anim, 0.0, 20, 0.0)
    assert len(lines) == 1
    assert lines[0].startswith("=>")


def test_walk_at_full_progress(walk_anim: Animation) -> None:
    lines = render_animation(walk_anim, 1.0, 20, 0.0)
    assert len(lines) == 1
    assert lines[0].rstrip().endswith("=>")


def test_walk_frame_changes_with_time(walk_anim: Animation) -> None:
    lines_t0 = render_animation(walk_anim, 0.5, 20, 0.0)
    lines_t1 = render_animation(walk_anim, 0.5, 20, 0.1)
    assert lines_t0[0] != lines_t1[0]


def test_cycle_stays_centered(cycle_anim: Animation) -> None:
    lines = render_animation(cycle_anim, 0.0, 20, 0.0)
    assert lines[0][9] in ("*", "+")


def test_fill_tiles_across(fill_anim: Animation) -> None:
    lines = render_animation(fill_anim, 0.5, 10, 0.0)
    assert lines[0] == "ababababab"


def test_completion_frame_at_100() -> None:
    done = Frame(lines=("DONE",))
    anim = Animation(
        name="test", frames=(Frame(lines=("run",)),),
        fps=12.0, completion_frame=done,
    )
    lines = render_animation(anim, 1.0, 20, 0.0)
    assert "DONE" in lines[0]


def test_no_completion_frame_at_100(walk_anim: Animation) -> None:
    lines = render_animation(walk_anim, 1.0, 20, 0.0)
    assert len(lines) == 1
    assert "=>" in lines[0] or "->" in lines[0]


def test_single_frame_animation() -> None:
    anim = Animation(name="single", frames=(Frame(lines=("X",)),), fps=12.0)
    lines = render_animation(anim, 0.5, 10, 0.0)
    assert "X" in lines[0]


def test_output_line_width(walk_anim: Animation) -> None:
    lines = render_animation(walk_anim, 0.5, 20, 0.0)
    assert len(lines[0]) == 20


def test_multiline_frame() -> None:
    anim = Animation(name="multi", frames=(Frame(lines=("ab", "cd")),), fps=12.0)
    lines = render_animation(anim, 0.5, 10, 0.0)
    assert len(lines) == 2
    assert len(lines[0]) == 10
    assert len(lines[1]) == 10
