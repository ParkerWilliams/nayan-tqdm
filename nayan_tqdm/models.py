"""Core data model for nayan_tqdm animations.

Defines the immutable :class:`Frame` and :class:`Animation` dataclasses
that represent sprite data.  These are the public API for custom themes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .utils import disp_len

__all__ = ["AnimationMode", "Frame", "Animation"]


class AnimationMode(Enum):
    """How the sprite interacts with the progress bar."""

    WALK = "walk"    # Sprite moves across bar with progress
    CYCLE = "cycle"  # Sprite stays in place, frames cycle over time
    FILL = "fill"    # Animation pattern fills bar area


@dataclass(frozen=True, slots=True)
class Frame:
    """A single animation frame -- immutable sprite data.

    Parameters
    ----------
    lines:
        Tuple of strings, one per row of the sprite.
    """

    lines: tuple[str, ...]
    display_width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self) -> None:
        # Bypass frozen guard to set computed fields
        object.__setattr__(
            self,
            "display_width",
            max((disp_len(line) for line in self.lines), default=0),
        )
        object.__setattr__(self, "height", len(self.lines))


@dataclass(frozen=True, slots=True)
class Animation:
    """A named animation consisting of a sequence of :class:`Frame` objects.

    Parameters
    ----------
    name:
        Theme name identifier (e.g. ``"nyan"``).
    frames:
        Tuple of frames forming the animation cycle (sprite at leading edge).
    fps:
        Frames per second for playback.  Default ``12.0``.
    mode:
        How the sprite interacts with the progress bar.
    completion_frame:
        Optional frame shown at 100 % progress.
    bar_fill:
        Optional tuple of 1-display-col strings cycled to fill the bar.
        When set, activates themed bar rendering (fill + sprite at edge).
    decoration:
        Optional animated decoration frames (e.g. twinkling stars)
        rendered above and below the bar line.
    completion_decoration:
        Optional decoration frame shown at 100 % progress.
    """

    name: str
    frames: tuple[Frame, ...]
    fps: float = 12.0
    mode: AnimationMode = AnimationMode.WALK
    completion_frame: Optional[Frame] = None
    bar_fill: tuple[str, ...] | None = None
    decoration: tuple[Frame, ...] | None = None
    completion_decoration: Optional[Frame] = None
    frame_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "frame_count", len(self.frames))
