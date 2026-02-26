"""Tests for nyanbar.models — Frame, Animation, AnimationMode."""
from __future__ import annotations

import pytest

from nyanbar.models import Animation, AnimationMode, Frame


# ── Frame ───────────────────────────────────────────────────


class TestFrame:
    """Frame is a frozen dataclass representing a single animation frame."""

    def test_basic_construction(self) -> None:
        frame = Frame(lines=("=^.^=", " || "))
        assert frame.lines == ("=^.^=", " || ")

    def test_display_width_ascii(self) -> None:
        frame = Frame(lines=("=^.^=", " || "))
        assert frame.display_width == 5

    def test_display_width_multiline_max(self) -> None:
        frame = Frame(lines=("abc", "abcdef"))
        assert frame.display_width == 6

    def test_display_width_cjk(self) -> None:
        # 世界 = 4 display columns
        frame = Frame(lines=("\u4e16\u754c",))
        assert frame.display_width == 4

    def test_display_width_with_ansi(self) -> None:
        frame = Frame(lines=("\033[31mhi\033[0m",))
        assert frame.display_width == 2

    def test_height(self) -> None:
        frame = Frame(lines=("a", "b", "c"))
        assert frame.height == 3

    def test_height_single_line(self) -> None:
        frame = Frame(lines=("hello",))
        assert frame.height == 1

    def test_empty_lines(self) -> None:
        frame = Frame(lines=())
        assert frame.display_width == 0
        assert frame.height == 0

    def test_frozen_lines(self) -> None:
        frame = Frame(lines=("a",))
        with pytest.raises(AttributeError):
            frame.lines = ("b",)  # type: ignore[misc]

    def test_frozen_display_width(self) -> None:
        frame = Frame(lines=("a",))
        with pytest.raises(AttributeError):
            frame.display_width = 99  # type: ignore[misc]


# ── AnimationMode ───────────────────────────────────────────


class TestAnimationMode:
    """AnimationMode enum defines sprite behavior modes."""

    def test_walk(self) -> None:
        assert AnimationMode.WALK.value == "walk"

    def test_cycle(self) -> None:
        assert AnimationMode.CYCLE.value == "cycle"

    def test_fill(self) -> None:
        assert AnimationMode.FILL.value == "fill"


# ── Animation ───────────────────────────────────────────────


class TestAnimation:
    """Animation is a frozen dataclass holding a sequence of frames."""

    @pytest.fixture
    def frames(self) -> tuple[Frame, ...]:
        return (
            Frame(lines=("=^.^=",)),
            Frame(lines=("=^o^=",)),
        )

    def test_construction(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        assert anim.name == "cat"
        assert anim.frames == frames

    def test_default_fps(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        assert anim.fps == 12.0

    def test_custom_fps(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames, fps=24.0)
        assert anim.fps == 24.0

    def test_default_mode(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        assert anim.mode == AnimationMode.WALK

    def test_custom_mode(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames, mode=AnimationMode.CYCLE)
        assert anim.mode == AnimationMode.CYCLE

    def test_frame_count(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        assert anim.frame_count == 2

    def test_completion_frame_default_none(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        assert anim.completion_frame is None

    def test_completion_frame_set(self, frames: tuple[Frame, ...]) -> None:
        done = Frame(lines=("done!",))
        anim = Animation(name="cat", frames=frames, completion_frame=done)
        assert anim.completion_frame is done

    def test_frozen_name(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        with pytest.raises(AttributeError):
            anim.name = "dog"  # type: ignore[misc]

    def test_frozen_fps(self, frames: tuple[Frame, ...]) -> None:
        anim = Animation(name="cat", frames=frames)
        with pytest.raises(AttributeError):
            anim.fps = 60.0  # type: ignore[misc]

    def test_single_frame(self) -> None:
        frame = Frame(lines=("x",))
        anim = Animation(name="one", frames=(frame,))
        assert anim.frame_count == 1

    def test_empty_frames(self) -> None:
        anim = Animation(name="empty", frames=())
        assert anim.frame_count == 0
