"""Tests for the rocket theme."""
from __future__ import annotations

import pytest

from nyanbar.models import Animation, AnimationMode
from nyanbar.engine import render_animation
from nyanbar.renderer import has_unclosed_ansi
from nyanbar.utils import disp_len
from nyanbar.registry import get_theme

import nyanbar.themes._rocket  # noqa: F401

TIERS = ("emoji", "unicode", "ascii")
PROGRESS_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
WIDTH = 60


class TestRocket:
    @pytest.mark.parametrize("tier", TIERS)
    def test_is_animation(self, tier: str) -> None:
        assert isinstance(get_theme("rocket", tier), Animation)

    @pytest.mark.parametrize("tier", TIERS)
    def test_mode_is_cycle(self, tier: str) -> None:
        assert get_theme("rocket", tier).mode == AnimationMode.CYCLE

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_frames(self, tier: str) -> None:
        assert get_theme("rocket", tier).frame_count >= 2

    @pytest.mark.parametrize("tier", TIERS)
    def test_fps_positive(self, tier: str) -> None:
        assert get_theme("rocket", tier).fps > 0

    @pytest.mark.parametrize("tier", TIERS)
    def test_height_is_4(self, tier: str) -> None:
        anim = get_theme("rocket", tier)
        for frame in anim.frames:
            assert frame.height == 4

    @pytest.mark.parametrize("tier", TIERS)
    def test_widths_consistent(self, tier: str) -> None:
        anim = get_theme("rocket", tier)
        widths = {f.display_width for f in anim.frames}
        assert len(widths) == 1

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_completion(self, tier: str) -> None:
        assert get_theme("rocket", tier).completion_frame is not None

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_height_4(self, tier: str) -> None:
        assert get_theme("rocket", tier).completion_frame.height == 4

    @pytest.mark.parametrize("tier", TIERS)
    @pytest.mark.parametrize("progress", PROGRESS_LEVELS)
    def test_renders_at_progress(self, tier: str, progress: float) -> None:
        anim = get_theme("rocket", tier)
        lines = render_animation(anim, progress, WIDTH, 0.0)
        assert len(lines) == 4
        for line in lines:
            assert disp_len(line) == WIDTH

    @pytest.mark.parametrize("tier", ("emoji", "unicode"))
    def test_no_unclosed_ansi(self, tier: str) -> None:
        anim = get_theme("rocket", tier)
        for frame in anim.frames:
            for line in frame.lines:
                assert not has_unclosed_ansi(line)
        for line in anim.completion_frame.lines:
            assert not has_unclosed_ansi(line)
