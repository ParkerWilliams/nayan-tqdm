# CLAUDE.md — nayan_tqdm

## Project Overview

**nayan_tqdm** is a drop-in replacement for `tqdm` that renders cute animated progress bars in the terminal. It subclasses `tqdm` directly so all existing tqdm code works — users just swap the import. The core innovation is an animation engine that renders multi-frame ASCII/Unicode sprite animations synchronized with progress, using ANSI escape codes for in-place redraw.

## Core Principles

- **Drop-in compatible**: `from nayan_tqdm import tqdm` must work everywhere `from tqdm import tqdm` works. All tqdm kwargs are preserved.
- **Zero required dependencies beyond tqdm**: The base package depends only on `tqdm`. Rich/color support is optional.
- **Graceful degradation**: If the terminal doesn't support ANSI (piped output, dumb terminals, CI), fall back to standard tqdm rendering automatically.
- **Performance-safe**: Animation rendering must never bottleneck the wrapped iterator. Use `mininterval` and decouple frame cycling from iteration rate.

## Architecture

### Project Structure

```
nayan_tqdm/
├── __init__.py          # Public API: tqdm, trange, set_theme, Animation, Frame
├── core.py              # NyanBar class (subclasses tqdm.tqdm), overrides display()
├── renderer.py          # ANSIRenderer: cursor movement, color, multi-line redraw
├── themes/
│   ├── __init__.py      # Theme registry, get_theme(), list_themes()
│   ├── base.py          # Animation, Frame, Sprite dataclasses
│   ├── cat_walk.py      # Cat walking across the bar
│   ├── cat_bounce.py    # Cat bouncing on top of filled portion
│   ├── nyan.py          # Nyan cat with rainbow trail
│   ├── fish.py          # Fish swimming, water level = progress
│   └── rocket.py        # Rocket launch, lifts off as progress completes
├── utils.py             # Terminal detection: width, color support, is_tty, is_notebook
├── compat.py            # Fallback logic, Jupyter/notebook support
└── py.typed             # PEP 561 marker
tests/
├── test_core.py         # Drop-in compatibility tests, kwargs passthrough
├── test_renderer.py     # ANSI output correctness
├── test_themes.py       # Each theme renders without error at 0%, 50%, 100%
└── test_compat.py       # Fallback behavior in non-TTY environments
pyproject.toml
README.md
LICENSE                  # MIT
```

### Key Classes

#### `Frame` (dataclass)
```python
@dataclass
class Frame:
    lines: list[str]       # Each string is one row of the frame
    width: int             # Character width of this frame (auto-calculated)
```

#### `Animation` (dataclass)
```python
@dataclass
class Animation:
    name: str
    frames: list[Frame]
    fps: float = 8.0
    is_multiline: bool     # Derived from max(len(f.lines) for f in frames)
    mode: str = "walk"     # "walk" = sprite moves with progress, "cycle" = sprite stays in place and animates, "fill" = animation fills the bar area

    def render(self, progress: float, width: int, elapsed: float) -> list[str]:
        """Return the lines to display for the given progress [0.0, 1.0], terminal width, and elapsed time (for frame selection)."""
```

#### `NyanBar(tqdm)` — in `core.py`
- Subclasses `tqdm.tqdm`
- Constructor accepts extra kwargs: `theme: str = "cat_walk"`, `animation: Animation | None = None`, `show_stats: bool = True`
- Overrides `display(msg=None, pos=None)` to render the animation instead of the default bar
- Frame selection uses wall-clock time (`time.monotonic()`), not iteration count
- Stats line (rate, ETA, percentage) renders below or beside the animation depending on terminal width
- On close/completion, render a final "done" frame if the theme defines one (e.g., cat sitting down, rocket in space)

#### `ANSIRenderer` — in `renderer.py`
- `move_cursor_up(n: int) -> str` — returns `\033[{n}A`
- `clear_line() -> str` — returns `\r\033[K`
- `render_frame(lines: list[str], prev_height: int) -> str` — builds the full escape sequence to overwrite previous output
- `supports_color() -> bool`
- `supports_unicode() -> bool` — for falling back to ASCII-only sprites
- All output goes to `self.fp` (defaults to `sys.stderr`, same as tqdm)

### Theme System

Each theme module registers itself by defining a `THEME` variable of type `Animation` at module level. The `themes/__init__.py` collects them:

```python
# themes/__init__.py
REGISTRY: dict[str, Animation] = {}

def register(animation: Animation):
    REGISTRY[animation.name] = animation

def get_theme(name: str) -> Animation:
    return REGISTRY[name]

def list_themes() -> list[str]:
    return list(REGISTRY.keys())
```

Themes are lazily imported on first access so unused themes don't slow down import.

### Public API (`__init__.py`)

```python
from nayan_tqdm.core import NyanBar as tqdm
from nayan_tqdm.core import trange
from nayan_tqdm.themes import list_themes, get_theme
from nayan_tqdm.themes.base import Animation, Frame

_default_theme = "cat_walk"

def set_theme(name: str):
    """Set the global default theme."""
    global _default_theme
    _default_theme = name
```

## Theme Specifications

Build these five themes. Each theme needs 3-6 frames. Use Unicode box-drawing and emoji where possible, with ASCII fallbacks.

### 1. `cat_walk` (default)
- A small cat sprite (3-4 chars wide) walks left to right across the terminal
- Position = `progress * (width - sprite_width)`
- Behind the cat: filled bar characters (e.g., `━` or `█`)
- Ahead of the cat: empty bar characters (e.g., `╌` or `░`)
- Walk cycle: 2-3 frames alternating legs
- Completion frame: cat sits down (`=^.^=`)
- Single-line mode

Example at 40%:
```
 ╱•ᴥ•╲━━━━━━━━━━━━━━━╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌  40% 4.2it/s 00:12
```

### 2. `cat_bounce`
- Standard filled/empty bar on the bottom line
- Cat sprite bounces up and down above the filled portion (2-line animation)
- Bounce follows a sine wave on elapsed time
- Multi-line mode (2 lines + stats line)

### 3. `nyan`
- Nyan cat sprite moves with progress
- Rainbow trail behind it using ANSI colors (red, orange, yellow, green, blue, purple bands)
- Stars (`✦`, `·`) scattered in the empty space ahead, twinkling between frames
- Multi-line mode (3 lines + stats line)
- Graceful fallback: no color terminals get `=` trail instead of rainbow

### 4. `fish`
- Fish sprites (`><>`, `<><`) swim back and forth independent of progress
- "Water level" rises from bottom as progress increases
- Water uses `~` and `≋` characters
- Multi-line mode (3 lines + stats line)

### 5. `rocket`
- Rocket sprite (`🚀` or ASCII `/^\ | |`) at bottom
- Flame animation below (`🔥` cycling or `*` / `^`)
- As progress increases, rocket moves upward (cursor position changes)
- Stars appear above
- On completion: rocket disappears upward, "✨ Done!" message
- Multi-line mode (4 lines + stats line)

### moon — Moon phases from 🌑 to 🌕
duck — A rubber duck bobbing in rising water


### ?? - \inf
- no reason to limit the project to just these, be creative!

## Implementation Notes

### Animation Timing
```python
# In NyanBar.display():
elapsed = time.monotonic() - self.start_t  # tqdm already tracks this
frame_index = int(elapsed * animation.fps) % len(animation.frames)
```

### Terminal Width Handling
- Use `shutil.get_terminal_size().columns` (tqdm already does this)
- Reserve rightmost column to avoid line-wrap issues
- Stats string (percentage, rate, ETA) width is calculated first, remaining space goes to animation
- If terminal is too narrow for the animation (<30 cols), fall back to plain tqdm

### Multi-line Rendering Strategy
tqdm assumes single-line output. For multi-line themes:
1. Track `_prev_height` (number of lines in last render)
2. On each refresh: move cursor up `_prev_height - 1` lines, then overwrite all lines
3. On close: clear all animation lines before printing the final summary
4. If `position` (nested bars) is used, disable multi-line and fall back to single-line mode

### Notebook Support
- Detect notebook via `tqdm.utils.IS_WIN` and IPython checks (same as tqdm.notebook)
- In notebooks, use HTML rendering with CSS animations instead of ANSI — this is a stretch goal, not required for v1. For v1, just fall back to standard tqdm.notebook behavior.

### Non-TTY / Piped Output
- If `self.fp.isatty()` is False, skip all animation and delegate to `super().display()`
- Same for `TERM=dumb` environments

## Testing Requirements

- `test_core.py`: Verify NyanBar is a subclass of tqdm. Verify all standard tqdm kwargs work (desc, total, unit, etc.). Verify iteration produces correct n/total values. Test with `file=StringIO()` to capture output.
- `test_renderer.py`: Verify ANSI escape sequences are correct. Test `render_frame` output against expected strings.
- `test_themes.py`: For each theme, call `animation.render(progress, width=80, elapsed=t)` at progress 0.0, 0.25, 0.5, 0.75, 1.0 and verify output is non-empty and fits within width. Verify the frame count matches expected range.
- `test_compat.py`: Mock `isatty() -> False` and verify fallback to plain tqdm. Test with very narrow terminal width.

Run tests with `pytest`. No test should take more than 2 seconds.

## Package Configuration (`pyproject.toml`)

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "nayan_tqdm"
version = "0.1.0"
description = "tqdm but with cute animations 🐱"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
dependencies = ["tqdm>=4.60"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "rich"]
```

## Build Order

Implement in this order, verifying each step works before moving on:

1. **`themes/base.py`** — Frame and Animation dataclasses
2. **`renderer.py`** — ANSI rendering utilities
3. **`utils.py`** — Terminal detection helpers
4. **`themes/cat_walk.py`** — First theme (single-line, simplest)
5. **`themes/__init__.py`** — Theme registry
6. **`core.py`** — NyanBar subclass with display override. Test it: `python -c "from nayan_tqdm import tqdm; import time; [time.sleep(0.03) for _ in tqdm(range(100))]"`
7. **`__init__.py`** — Public API
8. **`compat.py`** — Fallback logic
9. **Remaining themes** — cat_bounce, nyan, fish, rocket
10. **Tests**
11. **README.md** — With terminal GIF recordings (can use `terminalizer` or `asciinema`)

## Style Guide

- Python 3.10+ (use `X | Y` union syntax, not `Union[X, Y]`)
- Type hints on all public functions and methods
- Docstrings on all public classes and functions (Google style)
- No runtime dependencies beyond tqdm
- Keep each theme module self-contained (define frames inline, don't load external files)
- Use `__all__` in `__init__.py` modules
