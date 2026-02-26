"""Tests for cat_walk and cat_bounce themes."""
from __future__ import annotations

import pytest

from nyanbar.models import Animation, AnimationMode
from nyanbar.engine import render_animation
from nyanbar.utils import disp_len
from nyanbar.registry import get_theme

# Trigger registration
import nyanbar.themes._cat_walk   # noqa: F401
import nyanbar.themes._cat_bounce  # noqa: F401


TIERS = ("emoji", "unicode", "ascii")
PROGRESS_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
WIDTH = 60


# ── cat_walk tests ───────────────────────────────────


class TestCatWalk:
    @pytest.mark.parametrize("tier", TIERS)
    def test_is_animation(self, tier: str) -> None:
        assert isinstance(get_theme("cat_walk", tier), Animation)

    @pytest.mark.parametrize("tier", TIERS)
    def test_mode_is_walk(self, tier: str) -> None:
        assert get_theme("cat_walk", tier).mode == AnimationMode.WALK

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_frames(self, tier: str) -> None:
        assert get_theme("cat_walk", tier).frame_count >= 2

    @pytest.mark.parametrize("tier", TIERS)
    def test_fps_positive(self, tier: str) -> None:
        assert get_theme("cat_walk", tier).fps > 0

    @pytest.mark.parametrize("tier", TIERS)
    def test_height_is_1(self, tier: str) -> None:
        anim = get_theme("cat_walk", tier)
        for frame in anim.frames:
            assert frame.height == 1

    @pytest.mark.parametrize("tier", TIERS)
    def test_frame_widths_consistent(self, tier: str) -> None:
        anim = get_theme("cat_walk", tier)
        widths = {f.display_width for f in anim.frames}
        assert len(widths) == 1, f"Inconsistent widths: {widths}"

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_completion_frame(self, tier: str) -> None:
        assert get_theme("cat_walk", tier).completion_frame is not None

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_frame_height(self, tier: str) -> None:
        anim = get_theme("cat_walk", tier)
        assert anim.completion_frame.height == 1

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_frame_width_matches(self, tier: str) -> None:
        anim = get_theme("cat_walk", tier)
        frame_w = anim.frames[0].display_width
        comp_w = anim.completion_frame.display_width
        assert comp_w == frame_w, f"Completion width {comp_w} != frame width {frame_w}"

    @pytest.mark.parametrize("tier", TIERS)
    @pytest.mark.parametrize("progress", PROGRESS_LEVELS)
    def test_renders_at_progress(self, tier: str, progress: float) -> None:
        anim = get_theme("cat_walk", tier)
        lines = render_animation(anim, progress, WIDTH, 0.0)
        assert isinstance(lines, list)
        assert len(lines) >= 1
        for line in lines:
            assert disp_len(line) == WIDTH, (
                f"tier={tier} progress={progress}: "
                f"disp_len={disp_len(line)} != {WIDTH}"
            )


# ── cat_bounce tests ─────────────────────────────────


class TestCatBounce:
    @pytest.mark.parametrize("tier", TIERS)
    def test_is_animation(self, tier: str) -> None:
        assert isinstance(get_theme("cat_bounce", tier), Animation)

    @pytest.mark.parametrize("tier", TIERS)
    def test_mode_is_walk(self, tier: str) -> None:
        assert get_theme("cat_bounce", tier).mode == AnimationMode.WALK

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_frames(self, tier: str) -> None:
        assert get_theme("cat_bounce", tier).frame_count >= 2

    @pytest.mark.parametrize("tier", TIERS)
    def test_fps_positive(self, tier: str) -> None:
        assert get_theme("cat_bounce", tier).fps > 0

    @pytest.mark.parametrize("tier", TIERS)
    def test_height_is_2(self, tier: str) -> None:
        anim = get_theme("cat_bounce", tier)
        for frame in anim.frames:
            assert frame.height == 2

    @pytest.mark.parametrize("tier", TIERS)
    def test_frame_widths_consistent(self, tier: str) -> None:
        anim = get_theme("cat_bounce", tier)
        widths = {f.display_width for f in anim.frames}
        assert len(widths) == 1, f"Inconsistent widths: {widths}"

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_completion_frame(self, tier: str) -> None:
        assert get_theme("cat_bounce", tier).completion_frame is not None

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_frame_height(self, tier: str) -> None:
        anim = get_theme("cat_bounce", tier)
        assert anim.completion_frame.height == 2

    @pytest.mark.parametrize("tier", TIERS)
    @pytest.mark.parametrize("progress", PROGRESS_LEVELS)
    def test_renders_at_progress(self, tier: str, progress: float) -> None:
        anim = get_theme("cat_bounce", tier)
        lines = render_animation(anim, progress, WIDTH, 0.0)
        assert isinstance(lines, list)
        assert len(lines) >= 2
        for line in lines:
            assert disp_len(line) == WIDTH, (
                f"tier={tier} progress={progress}: "
                f"disp_len={disp_len(line)} != {WIDTH}"
            )
