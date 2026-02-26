"""Animation engine for nyanbar.

Composes wall-clock frame selection with mode-based positioning to
produce renderable output lines.  All functions are pure -- no side
effects, no I/O.
"""
from __future__ import annotations

from .models import Animation, AnimationMode, Frame
from .utils import disp_len

__all__ = [
    "select_frame_index",
    "walk_position",
    "cycle_position",
    "fill_pattern",
    "render_animation",
]


# ── Frame selection ─────────────────────────────────────────


def select_frame_index(frame_count: int, elapsed: float, fps: float) -> int:
    """Return the animation frame index for *elapsed* seconds at *fps*.

    Frame index wraps around when elapsed time exceeds a full cycle.
    """
    if frame_count <= 0:
        return 0
    return int(elapsed * fps) % frame_count


# ── Mode positioning ────────────────────────────────────────


def walk_position(progress: float, width: int, sprite_width: int) -> int:
    """Compute sprite position for walk mode (linear, no easing).

    Position is proportional to *progress* across the available space.
    Clamped to ``[0, width - sprite_width]``.
    """
    available = max(width - sprite_width, 0)
    clamped = max(0.0, min(1.0, progress))
    return int(clamped * available)


def cycle_position(width: int, sprite_width: int) -> int:
    """Compute fixed center position for cycle mode."""
    return max((width - sprite_width) // 2, 0)


def fill_pattern(frame: Frame, width: int) -> list[str]:
    """Tile each line of *frame* to fill *width* display columns.

    For ASCII-only lines, characters are repeated to fill.  The result
    is truncated cleanly at the *width* boundary.
    """
    result: list[str] = []
    for line in frame.lines:
        line_len = len(line)
        if line_len == 0:
            result.append(" " * width)
            continue
        # Repeat enough times to cover width, then slice
        repeats = (width // line_len) + 1
        result.append((line * repeats)[:width])
    return result


# ── Composite rendering ────────────────────────────────────


def _pad_line(line: str, position: int, width: int) -> str:
    """Place *line* at *position* within a field of *width* columns."""
    line_width = disp_len(line)
    left = " " * position
    right_space = max(width - position - line_width, 0)
    right = " " * right_space
    return left + line + right


def render_animation(
    animation: Animation,
    progress: float,
    width: int,
    elapsed: float,
) -> list[str]:
    """Produce renderable output lines for the given animation state.

    Parameters
    ----------
    animation:
        The animation to render.
    progress:
        Current progress fraction (0.0 to 1.0).
    width:
        Available bar width in terminal columns.
    elapsed:
        Seconds since animation started (for frame selection).

    Returns
    -------
    list[str]
        Output lines, each exactly *width* display columns wide.
    """
    # Completion frame at 100%
    if progress >= 1.0 and animation.completion_frame is not None:
        frame = animation.completion_frame
        pos = max(width - frame.display_width, 0)
        return [_pad_line(line, pos, width) for line in frame.lines]

    # Select current frame by elapsed time
    idx = select_frame_index(animation.frame_count, elapsed, animation.fps)
    frame = animation.frames[idx] if animation.frames else Frame(lines=())

    if animation.mode == AnimationMode.FILL:
        return fill_pattern(frame, width)

    if animation.mode == AnimationMode.CYCLE:
        pos = cycle_position(width, frame.display_width)
    else:  # WALK (default)
        pos = walk_position(progress, width, frame.display_width)

    return [_pad_line(line, pos, width) for line in frame.lines]
