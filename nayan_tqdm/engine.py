"""Animation engine for nayan_tqdm.

Composes wall-clock frame selection with mode-based positioning to
produce renderable output lines.  All functions are pure -- no side
effects, no I/O.
"""
from __future__ import annotations

import unicodedata

from .models import Animation, AnimationMode, Frame
from .utils import disp_len, strip_ansi

__all__ = [
    "select_frame_index",
    "walk_position",
    "cycle_position",
    "fill_pattern",
    "render_animation",
    "build_themed_fill",
    "render_themed_bar",
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


# ── Themed bar rendering ──────────────────────────────────


def build_themed_fill(bar_fill: tuple[str, ...], filled_cols: int) -> str:
    """Build a themed fill string exactly *filled_cols* display columns wide.

    Cycles through *bar_fill* characters, which may be wider than 1 display
    column (e.g. emojis).  Characters may contain ANSI color codes.
    Any remainder is padded with spaces.
    """
    if not bar_fill or filled_cols <= 0:
        return ""
    parts: list[str] = []
    count = len(bar_fill)
    total_w = 0
    i = 0
    while total_w < filled_cols:
        char = bar_fill[i % count]
        char_w = disp_len(char)
        if total_w + char_w > filled_cols:
            break
        parts.append(char)
        total_w += char_w
        i += 1
    if total_w < filled_cols:
        parts.append(" " * (filled_cols - total_w))
    return "".join(parts)


def _trunc_to_width(text: str, target: int) -> str:
    """Truncate *text* to exactly *target* display columns.

    Preserves ANSI escape sequences (zero-width).  Pads with spaces if
    the target falls in the middle of a wide character.
    """
    result: list[str] = []
    width = 0
    i = 0
    while i < len(text) and width < target:
        # Pass ANSI escape sequences through without counting width
        if text[i] == "\033" and i + 1 < len(text) and text[i + 1] == "[":
            j = i + 2
            while j < len(text) and not text[j].isalpha():
                j += 1
            if j < len(text):
                j += 1  # include the final letter
            result.append(text[i:j])
            i = j
            continue

        char = text[i]
        if unicodedata.combining(char):
            result.append(char)
            i += 1
            continue

        eaw = unicodedata.east_asian_width(char)
        char_w = 2 if eaw in ("W", "F") else 1
        if width + char_w > target:
            break
        result.append(char)
        width += char_w
        i += 1

    if width < target:
        result.append(" " * (target - width))
    return "".join(result)


def _tile_decoration(line: str, target: int) -> str:
    """Tile *line* to fill exactly *target* display columns.

    Repeats the decoration content and truncates cleanly, handling ANSI
    escape sequences and wide characters.  Appends a reset code if the
    source contained ANSI to avoid unclosed sequences after truncation.
    """
    line_w = disp_len(line)
    if line_w <= 0:
        return " " * target
    if line_w >= target:
        return _trunc_to_width(line, target)
    repeats = (target // line_w) + 2
    result = _trunc_to_width(line * repeats, target)
    if "\033" in line:
        result += "\033[0m"
    return result


def render_themed_bar(
    animation: Animation,
    progress: float,
    ncols: int,
    elapsed: float,
    stats_left: str,
    stats_right: str,
) -> list[str]:
    """Render a themed progress bar with fill + sprite at the leading edge.

    Returns a list of output lines (1 bar line + optional decoration lines).
    The bar line is exactly *ncols* display columns wide.
    """
    if animation.bar_fill is None:
        return []

    left_width = disp_len(stats_left)
    right_width = disp_len(stats_right)
    # Inner bar width between the pipes
    inner = max(ncols - left_width - right_width - 2, 0)

    # Select sprite frame
    is_complete = progress >= 1.0
    if is_complete and animation.completion_frame is not None:
        sprite_frame = animation.completion_frame
    else:
        idx = select_frame_index(animation.frame_count, elapsed, animation.fps)
        sprite_frame = animation.frames[idx] if animation.frames else Frame(lines=())

    # Sprite is single-line for the bar; use first line
    sprite = sprite_frame.lines[0] if sprite_frame.lines else ""
    sprite_w = disp_len(sprite)

    # Fillable space = inner minus sprite
    fillable = max(inner - sprite_w, 0)
    clamped = max(0.0, min(1.0, progress))
    filled_cols = int(fillable * clamped)
    empty_cols = fillable - filled_cols

    fill = build_themed_fill(animation.bar_fill, filled_cols)
    empty = " " * empty_cols

    bar_line = f"{stats_left}|{fill}{sprite}{empty}|{stats_right}"

    # Pad or truncate to exact ncols
    bar_width = disp_len(bar_line)
    if bar_width < ncols:
        bar_line = bar_line + " " * (ncols - bar_width)

    lines: list[str] = []

    # Decoration above
    if animation.decoration is not None:
        if is_complete and animation.completion_decoration is not None:
            dec_frame = animation.completion_decoration
        else:
            dec_idx = select_frame_index(
                len(animation.decoration), elapsed, animation.fps,
            )
            dec_frame = animation.decoration[dec_idx]
        if dec_frame.lines:
            lines.append(_tile_decoration(dec_frame.lines[0], ncols))

    lines.append(bar_line)

    # Decoration below
    if animation.decoration is not None:
        if is_complete and animation.completion_decoration is not None:
            dec_frame = animation.completion_decoration
        else:
            dec_idx = select_frame_index(
                len(animation.decoration), elapsed, animation.fps,
            )
            dec_frame = animation.decoration[dec_idx]
        if len(dec_frame.lines) > 1:
            lines.append(_tile_decoration(dec_frame.lines[1], ncols))

    return lines
