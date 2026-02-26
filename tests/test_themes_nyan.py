"""Tests for the nyan theme."""
from __future__ import annotations

import pytest

from nyanbar.models import Animation, AnimationMode
from nyanbar.engine import render_animation
from nyanbar.renderer import has_unclosed_ansi
from nyanbar.utils import disp_len
from nyanbar.registry import get_theme

import nyanbar.themes._nyan  # noqa: F401

TIERS = ("emoji", "unicode", "ascii")
PROGRESS_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
WIDTH = 60


class TestNyan:
    @pytest.mark.parametrize("tier", TIERS)
    def test_is_animation(self, tier: str) -> None:
        assert isinstance(get_theme("nyan", tier), Animation)

    @pytest.mark.parametrize("tier", TIERS)
    def test_mode_is_walk(self, tier: str) -> None:
        assert get_theme("nyan", tier).mode == AnimationMode.WALK

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_frames(self, tier: str) -> None:
        assert get_theme("nyan", tier).frame_count >= 2

    @pytest.mark.parametrize("tier", TIERS)
    def test_fps_positive(self, tier: str) -> None:
        assert get_theme("nyan", tier).fps > 0

    @pytest.mark.parametrize("tier", TIERS)
    def test_height_is_3(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        for frame in anim.frames:
            assert frame.height == 3

    @pytest.mark.parametrize("tier", TIERS)
    def test_frame_widths_consistent(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        widths = {f.display_width for f in anim.frames}
        assert len(widths) == 1, f"Inconsistent widths: {widths}"

    @pytest.mark.parametrize("tier", TIERS)
    def test_frame_heights_consistent(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        heights = {f.height for f in anim.frames}
        assert heights == {3}

    @pytest.mark.parametrize("tier", TIERS)
    def test_has_completion_frame(self, tier: str) -> None:
        assert get_theme("nyan", tier).completion_frame is not None

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_frame_height(self, tier: str) -> None:
        assert get_theme("nyan", tier).completion_frame.height == 3

    @pytest.mark.parametrize("tier", TIERS)
    def test_completion_frame_width_matches(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        fw = anim.frames[0].display_width
        cw = anim.completion_frame.display_width
        assert cw == fw

    @pytest.mark.parametrize("tier", TIERS)
    @pytest.mark.parametrize("progress", PROGRESS_LEVELS)
    def test_renders_at_progress(self, tier: str, progress: float) -> None:
        anim = get_theme("nyan", tier)
        lines = render_animation(anim, progress, WIDTH, 0.0)
        assert isinstance(lines, list)
        assert len(lines) == 3
        for line in lines:
            assert disp_len(line) == WIDTH, (
                f"tier={tier} progress={progress}: "
                f"disp_len={disp_len(line)} != {WIDTH}"
            )

    @pytest.mark.parametrize("tier", ("emoji", "unicode"))
    def test_no_unclosed_ansi_in_frames(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        for i, frame in enumerate(anim.frames):
            for j, line in enumerate(frame.lines):
                assert not has_unclosed_ansi(line), (
                    f"tier={tier} frame={i} line={j} has unclosed ANSI"
                )

    @pytest.mark.parametrize("tier", ("emoji", "unicode"))
    def test_no_unclosed_ansi_in_completion(self, tier: str) -> None:
        anim = get_theme("nyan", tier)
        for j, line in enumerate(anim.completion_frame.lines):
            assert not has_unclosed_ansi(line), (
                f"tier={tier} completion line={j} has unclosed ANSI"
            )

    def test_ascii_rainbow_has_patterns(self) -> None:
        """ASCII tier uses patterned stripes (=, ~, -, .) per CONTEXT.md."""
        anim = get_theme("nyan", "ascii")
        all_text = ""
        for frame in anim.frames:
            for line in frame.lines:
                all_text += line
        # At least 3 of the 4 pattern characters should be present
        patterns_found = sum(1 for ch in ("=", "~", "-", ".") if ch in all_text)
        assert patterns_found >= 3, (
            f"Only {patterns_found} pattern chars found in ASCII rainbow"
        )
