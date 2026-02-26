"""Tests for nyanbar.engine — animation timing and mode positioning."""
from __future__ import annotations

import pytest

from nyanbar.engine import (
    cycle_position,
    fill_pattern,
    render_animation,
    select_frame_index,
    walk_position,
)
from nyanbar.models import Animation, AnimationMode, Frame


# ── select_frame_index ──────────────────────────────────────


class TestSelectFrameIndex:
    """Frame index is determined by wall-clock elapsed time, not iterations."""

    def test_zero_elapsed(self) -> None:
        assert select_frame_index(4, 0.0, 12.0) == 0

    def test_basic_advance(self) -> None:
        # 0.1s * 12fps = 1.2 -> int(1.2) = 1
        assert select_frame_index(4, 0.1, 12.0) == 1

    def test_half_second(self) -> None:
        # 0.5s * 12fps = 6.0 -> 6 % 4 = 2
        assert select_frame_index(4, 0.5, 12.0) == 2

    def test_wraps_around(self) -> None:
        # 1.0s * 12fps = 12 -> 12 % 4 = 0
        assert select_frame_index(4, 1.0, 12.0) == 0

    def test_single_frame_always_zero(self) -> None:
        assert select_frame_index(1, 0.0, 12.0) == 0
        assert select_frame_index(1, 5.0, 12.0) == 0

    def test_custom_fps(self) -> None:
        # 0.5s * 24fps = 12 -> 12 % 3 = 0
        assert select_frame_index(3, 0.5, 24.0) == 0
        # 0.25s * 24fps = 6 -> 6 % 3 = 0
        assert select_frame_index(3, 0.25, 24.0) == 0

    def test_high_elapsed(self) -> None:
        # Many seconds elapsed, still wraps properly
        idx = select_frame_index(4, 100.0, 12.0)
        assert 0 <= idx < 4


# ── walk_position ───────────────────────────────────────────


class TestWalkPosition:
    """Walk mode: sprite position proportional to progress."""

    def test_zero_progress(self) -> None:
        assert walk_position(0.0, 80, 5) == 0

    def test_full_progress(self) -> None:
        assert walk_position(1.0, 80, 5) == 75

    def test_half_progress(self) -> None:
        assert walk_position(0.5, 80, 5) == 37

    def test_clamp_negative(self) -> None:
        assert walk_position(-0.1, 80, 5) == 0

    def test_clamp_over_one(self) -> None:
        assert walk_position(1.5, 80, 5) == 75

    def test_sprite_fills_bar(self) -> None:
        # sprite_width >= width means no room to move
        assert walk_position(0.5, 5, 5) == 0
        assert walk_position(0.5, 5, 10) == 0


# ── cycle_position ──────────────────────────────────────────


class TestCyclePosition:
    """Cycle mode: sprite stays centered."""

    def test_centered(self) -> None:
        # (80 - 5) // 2 = 37
        assert cycle_position(80, 5) == 37

    def test_narrow_bar(self) -> None:
        # (10 - 8) // 2 = 1
        assert cycle_position(10, 8) == 1

    def test_sprite_wider_than_bar(self) -> None:
        # Clamp to 0
        assert cycle_position(5, 10) == 0


# ── fill_pattern ────────────────────────────────────────────


class TestFillPattern:
    """Fill mode: tile frame content across bar width."""

    def test_basic_tiling(self) -> None:
        frame = Frame(lines=("ab",))
        result = fill_pattern(frame, 6)
        assert len(result) == 1
        assert result[0] == "ababab"

    def test_truncates_at_width(self) -> None:
        frame = Frame(lines=("abc",))
        result = fill_pattern(frame, 5)
        assert len(result) == 1
        assert result[0] == "abcab"

    def test_multiline(self) -> None:
        frame = Frame(lines=("ab", "cd"))
        result = fill_pattern(frame, 4)
        assert result == ["abab", "cdcd"]

    def test_empty_frame(self) -> None:
        frame = Frame(lines=())
        result = fill_pattern(frame, 10)
        assert result == []

    def test_exact_fit(self) -> None:
        frame = Frame(lines=("abc",))
        result = fill_pattern(frame, 6)
        assert result[0] == "abcabc"


# ── render_animation ────────────────────────────────────────


class TestRenderAnimation:
    """render_animation composes frame selection + mode positioning."""

    @pytest.fixture
    def walk_anim(self) -> Animation:
        return Animation(
            name="test",
            frames=(
                Frame(lines=("=>",)),
                Frame(lines=("->",)),
            ),
            fps=12.0,
            mode=AnimationMode.WALK,
        )

    @pytest.fixture
    def cycle_anim(self) -> Animation:
        return Animation(
            name="test",
            frames=(
                Frame(lines=("*",)),
                Frame(lines=("+",)),
            ),
            fps=12.0,
            mode=AnimationMode.CYCLE,
        )

    @pytest.fixture
    def fill_anim(self) -> Animation:
        return Animation(
            name="test",
            frames=(Frame(lines=("ab",)),),
            fps=12.0,
            mode=AnimationMode.FILL,
        )

    def test_walk_at_zero_progress(self, walk_anim: Animation) -> None:
        lines = render_animation(walk_anim, 0.0, 20, 0.0)
        assert len(lines) == 1
        # Sprite at position 0
        assert lines[0].startswith("=>")

    def test_walk_at_full_progress(self, walk_anim: Animation) -> None:
        lines = render_animation(walk_anim, 1.0, 20, 0.0)
        assert len(lines) == 1
        # Sprite at rightmost position
        assert lines[0].rstrip().endswith("=>")

    def test_walk_frame_changes_with_time(self, walk_anim: Animation) -> None:
        lines_t0 = render_animation(walk_anim, 0.5, 20, 0.0)
        lines_t1 = render_animation(walk_anim, 0.5, 20, 0.1)
        # Different elapsed times may select different frames
        # (0.0 * 12 % 2 = 0 vs 0.1 * 12 % 2 = 1)
        assert lines_t0[0] != lines_t1[0]

    def test_cycle_stays_centered(self, cycle_anim: Animation) -> None:
        lines = render_animation(cycle_anim, 0.0, 20, 0.0)
        # Centered: (20-1)//2 = 9 spaces before
        assert lines[0][9] in ("*", "+")

    def test_fill_tiles_across(self, fill_anim: Animation) -> None:
        lines = render_animation(fill_anim, 0.5, 10, 0.0)
        assert lines[0] == "ababababab"

    def test_completion_frame_at_100(self) -> None:
        done = Frame(lines=("DONE",))
        anim = Animation(
            name="test",
            frames=(Frame(lines=("run",)),),
            fps=12.0,
            completion_frame=done,
        )
        lines = render_animation(anim, 1.0, 20, 0.0)
        assert "DONE" in lines[0]

    def test_no_completion_frame_at_100(self, walk_anim: Animation) -> None:
        # Without completion_frame, uses normal frame
        lines = render_animation(walk_anim, 1.0, 20, 0.0)
        assert len(lines) == 1
        assert "=>" in lines[0] or "->" in lines[0]

    def test_single_frame_animation(self) -> None:
        anim = Animation(
            name="single",
            frames=(Frame(lines=("X",)),),
            fps=12.0,
        )
        lines = render_animation(anim, 0.5, 10, 0.0)
        assert "X" in lines[0]

    def test_output_line_width(self, walk_anim: Animation) -> None:
        lines = render_animation(walk_anim, 0.5, 20, 0.0)
        # Each output line should be exactly 20 chars (padded)
        assert len(lines[0]) == 20

    def test_multiline_frame(self) -> None:
        anim = Animation(
            name="multi",
            frames=(Frame(lines=("ab", "cd")),),
            fps=12.0,
        )
        lines = render_animation(anim, 0.5, 10, 0.0)
        assert len(lines) == 2
        assert len(lines[0]) == 10
        assert len(lines[1]) == 10
