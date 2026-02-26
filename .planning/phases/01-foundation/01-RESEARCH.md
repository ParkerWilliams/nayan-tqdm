# Phase 1: Foundation - Research

**Researched:** 2026-02-25
**Domain:** Python terminal rendering primitives — dataclasses, ANSI escape sequences, terminal detection, animation timing
**Confidence:** HIGH

## Summary

Phase 1 builds four independent subsystems that later phases compose: (1) Frame/Animation frozen dataclasses as the sprite data model, (2) a `disp_len()` function using `unicodedata.east_asian_width` for terminal-accurate width measurement, (3) a terminal detection module that identifies TTY, color tier, terminal width, and notebook environments, and (4) an ANSI renderer that produces cursor-up/clear-line sequences for multi-line frame output with proper color reset.

All four subsystems are pure Python with zero dependencies, using only stdlib modules (`dataclasses`, `unicodedata`, `os`, `sys`, `shutil`, `time`). The animation engine uses `time.monotonic()` for wall-clock frame selection, decoupled from iteration count — a pattern well-established in game development for frame-rate-independent animation.

**Primary recommendation:** Build each subsystem as a separate module (`models.py`, `utils.py`, `terminal.py`, `renderer.py`) with pure-function interfaces where possible, making them independently testable before integration.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Each theme ships in multiple art-style variants using suffix naming: `cat_walk` (Unicode default), `cat_walk.ascii`, `cat_walk.emoji`
- Unicode is the default when user selects a base theme name (e.g., `theme='cat_walk'` → Unicode variant)
- If Unicode can't render in the current terminal, auto-downgrade silently to the `.ascii` variant
- Every theme must have an `.ascii` variant; `.emoji` variants only where natural
- One theme file per theme containing all variants as separate Animation objects
- Theme-matched bar characters — each theme picks fill/empty chars that fit its aesthetic
- Per-theme color palettes — each theme defines its own ANSI colors inline
- Keep sprites compact: max 4-5 chars wide, 3 lines tall
- Completion frames are nice-to-have — include where natural
- No terminal bell/beep — visual only
- `list_themes()` returns grouped listing: `{'cat_walk': ['unicode', 'ascii', 'emoji'], ...}`
- `theme='random'` picks a random built-in theme each time
- `python -m nyanbar demo` shows all themes with a sample progress run
- Animation/Frame dataclasses are the public custom theme API
- Default 12 FPS (configurable per theme)
- Walk mode: linear movement (position = progress * bar width), no easing
- Visual speed ceiling for rate-proportional effects
- Indeterminate mode with Wander and Chase modes
- Physics-style bounce for cat_bounce theme
- Idle animation on stall
- Sprite moves backward if progress goes backward
- Completion frame at 100%
- Error during iteration: just clean up terminal, no error sprite
- Seamless resume after pause
- Multiple simultaneous bars: independent clocks
- Three color tiers: true color (24-bit) / 256 color / 16 color (basic ANSI)
- Non-TTY / piped output / TERM=dumb / width < 30 cols → plain built-in text bar
- Environment variable support: `NYANBAR_THEME=nyan`, `NYANBAR_DISABLE=1`
- Configuration via `nyanbar.config()`
- nyanbar reimplements tqdm's user-facing API from scratch, zero dependencies
- Stats placement: adaptive — right of animation for single-line themes, below for multi-line
- Stats format: match tqdm's exact format string
- Terminal resize: re-check width only if `dynamic_ncols=True`

### Claude's Discretion
- Exact ANSI escape sequence implementation details
- Internal renderer architecture (pure function vs class)
- `disp_len()` implementation for Unicode width measurement
- Performance optimization details (pre-computation, caching)
- Exact physics curve for cat_bounce
- Chase mode movement algorithm for the mouse/yarn ball

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| FOUND-01 | Frame and Animation dataclasses define sprite data with frozen immutability | Frozen dataclass pattern with `@dataclass(frozen=True, slots=True)` — stdlib only |
| FOUND-02 | Animation.render() returns correct frame lines for given progress, width, and elapsed time | Wall-clock frame selection via `time.monotonic()`, mode-based positioning (walk/cycle/fill) |
| FOUND-03 | Frame width uses terminal display width (custom disp_len), not Python len() | `unicodedata.east_asian_width()` — W/F chars count as 2 columns, combining chars as 0 |
| FOUND-04 | Terminal detection identifies TTY, color support, terminal width, and notebook environments | `sys.stdout.isatty()`, `shutil.get_terminal_size()`, TERM env var parsing, `get_ipython()` check |
| FOUND-05 | ANSI renderer produces correct cursor-up, clear-line, and color reset escape sequences | `\033[{n}A` (cursor up), `\033[2K` (erase line), `\033[0m` (reset) — no external deps |
| FOUND-06 | Renderer handles multi-line frame erase with correct prev_height tracking | Track previous frame height, emit cursor-up + erase-line for each previous line before redraw |
| FOUND-07 | All ANSI color sequences are properly closed with reset codes | Every color open must pair with `\033[0m` reset; verified by checking no unclosed sequences in output |
| ANIM-01 | Frame selection uses wall-clock time (time.monotonic), not iteration count | `elapsed = time.monotonic() - start_time; frame_index = int(elapsed * fps) % len(frames)` |
| ANIM-02 | Animation FPS is configurable per theme | FPS stored as field on Animation dataclass, default 12, used in frame selection math |
| ANIM-03 | Walk mode positions sprite based on progress percentage | `sprite_pos = int(progress * (width - sprite_width))` — linear mapping, no easing |
| ANIM-04 | Cycle mode keeps sprite in place and cycles animation frames | Sprite stays at fixed position, only frame index advances with time |
| ANIM-05 | Fill mode fills the bar area with animation | Tile/repeat frame pattern across the entire bar width |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `dataclasses` (stdlib) | Python 3.10+ | Frozen immutable Frame/Animation types | Built-in, zero-dep, `frozen=True` + `slots=True` for performance |
| `unicodedata` (stdlib) | Python 3.10+ | East Asian Width character measurement | Only reliable stdlib way to get terminal display widths |
| `os` / `sys` (stdlib) | Python 3.10+ | TTY detection, environment variables | `os.isatty()`, `sys.stdout`, `os.environ` |
| `shutil` (stdlib) | Python 3.10+ | Terminal size detection | `shutil.get_terminal_size()` with fallback support |
| `time` (stdlib) | Python 3.10+ | Monotonic clock for animation timing | `time.monotonic()` never goes backward, immune to clock adjustments |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `typing` (stdlib) | Python 3.10+ | Type annotations | All public interfaces |
| `enum` (stdlib) | Python 3.10+ | Animation mode enum (walk/cycle/fill) | Mode selection in Animation |
| `functools` (stdlib) | Python 3.10+ | `lru_cache` for disp_len optimization | Cache char width lookups for performance |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `unicodedata.east_asian_width` | `wcwidth` library | More accurate but adds a dependency — violates zero-dep constraint |
| Custom ANSI sequences | `colorama` or `blessed` | Would add dependency; raw ANSI is simpler and sufficient |
| `@dataclass(frozen=True)` | `NamedTuple` | NamedTuple lacks `__post_init__`, less flexible for computed fields |
| `@dataclass(frozen=True)` | `attrs` | attrs is more powerful but adds a dependency |

**Installation:** None required — all stdlib.

## Architecture Patterns

### Recommended Project Structure
```
nyanbar/
├── __init__.py       # Public API (Phase 4)
├── models.py         # Frame, Animation dataclasses
├── utils.py          # disp_len(), strip_ansi()
├── terminal.py       # Terminal detection (TTY, color, size, notebook)
├── renderer.py       # ANSI rendering (cursor movement, line erase, color)
└── themes/           # Theme modules (Phase 3)
    └── __init__.py   # Theme registry
```

### Pattern 1: Frozen Dataclass with Computed Fields
**What:** Use `@dataclass(frozen=True, slots=True)` for Frame/Animation with `object.__setattr__` in `__post_init__` for derived fields.
**When to use:** Frame needs `display_width` computed from content; Animation needs frame count derived from frames list.
**Example:**
```python
from dataclasses import dataclass, field
from typing import Sequence

@dataclass(frozen=True, slots=True)
class Frame:
    """A single animation frame — immutable sprite data."""
    lines: tuple[str, ...]          # Each line of the frame
    display_width: int = field(init=False)  # Computed terminal width

    def __post_init__(self) -> None:
        # Bypass frozen to set computed field
        object.__setattr__(self, 'display_width', max(disp_len(line) for line in self.lines))
```

### Pattern 2: Wall-Clock Frame Selection
**What:** Select animation frame using elapsed wall-clock time, not iteration count.
**When to use:** Always — this is the core animation timing model.
**Example:**
```python
def select_frame(
    frames: Sequence[Frame],
    start_time: float,
    fps: float = 12.0,
) -> int:
    elapsed = time.monotonic() - start_time
    return int(elapsed * fps) % len(frames)
```

### Pattern 3: Terminal Capability Detection as Value Object
**What:** Detect terminal capabilities once, return as a frozen dataclass.
**When to use:** At NyanBar construction time — detect once, use throughout lifecycle.
**Example:**
```python
@dataclass(frozen=True, slots=True)
class TerminalInfo:
    is_tty: bool
    color_support: ColorTier  # TRUE_COLOR | COLOR_256 | COLOR_16 | NONE
    width: int
    is_notebook: bool
```

### Pattern 4: Stateless Renderer Functions
**What:** Renderer as pure functions that take frame data + terminal info and return escape sequence strings.
**When to use:** For the ANSI renderer — no mutable state, easy to test.
**Example:**
```python
def render_frame(
    lines: Sequence[str],
    prev_height: int,
    stream: IO[str],
) -> int:
    """Render frame lines, return new height for next erase."""
    if prev_height > 0:
        # Move up and clear previous lines
        stream.write(f'\033[{prev_height}A')
        for _ in range(prev_height):
            stream.write('\033[2K\n')
        stream.write(f'\033[{prev_height}A')
    for line in lines:
        stream.write(line + '\n')
    stream.flush()
    return len(lines)
```

### Anti-Patterns to Avoid
- **Iteration-based frame selection:** Tying animation speed to `update()` call frequency makes animation jerky at variable throughput rates.
- **Mutable Frame/Animation objects:** Mutation after construction creates race conditions with concurrent access and makes debugging harder.
- **Hardcoded ANSI sequences in theme data:** Themes should define color values; the renderer applies them. Keeps themes portable across color tiers.
- **Using `time.time()` for animation:** System clock adjustments (NTP, DST) cause animation jumps. Always use `time.monotonic()`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Character width measurement | Custom width tables | `unicodedata.east_asian_width()` | Unicode standard is comprehensive; custom tables go stale |
| Terminal size detection | `ioctl` + `TIOCGWINSZ` | `shutil.get_terminal_size()` | stdlib handles all edge cases, provides fallback |
| Monotonic timing | `time.time()` delta | `time.monotonic()` | Immune to system clock changes, NTP adjustments |
| ANSI color codes | Color name → code mapping | Enum with standard SGR codes | Well-defined standard, finite set |

**Key insight:** Every one of these subsystems has a correct stdlib solution. The risk is not "can we build it?" but "will we get the edge cases right?" — using stdlib ensures edge cases are handled.

## Common Pitfalls

### Pitfall 1: Frozen Dataclass `__post_init__` Assignment
**What goes wrong:** `FrozenInstanceError` when trying to set computed fields in `__post_init__`.
**Why it happens:** `frozen=True` blocks all `__setattr__` calls, including in `__post_init__`.
**How to avoid:** Use `object.__setattr__(self, 'field_name', value)` to bypass the frozen guard in `__post_init__` only.
**Warning signs:** `FrozenInstanceError` raised during construction.

### Pitfall 2: `disp_len()` Missing Combining Characters
**What goes wrong:** Combining diacritical marks (e.g., `e\u0301` = e with accent) counted as width 1 when they should be 0.
**Why it happens:** Naive implementation only checks for W/F width, doesn't handle combining chars.
**How to avoid:** Check `unicodedata.combining(c)` — if nonzero, width is 0. Also normalize with `unicodedata.normalize('NFC', text)` before measuring.
**Warning signs:** Strings with accented characters measure too wide.

### Pitfall 3: ANSI Sequences Counted in Display Width
**What goes wrong:** `\033[31m` (red) adds 5 chars to measured width but displays as 0 columns.
**Why it happens:** Forgetting to strip ANSI sequences before width measurement.
**How to avoid:** Strip ANSI with regex `re.compile(r'\033\[[0-9;]*m')` before passing to `disp_len()`.
**Warning signs:** Bar alignment is off when colors are used.

### Pitfall 4: Cursor-Up Count Off-By-One
**What goes wrong:** Multi-line frame erase leaves ghost lines or overwrites the line above.
**Why it happens:** Confusion between "number of lines" and "number of newlines" — a 3-line frame has 2 line-breaks between lines but cursor needs to go up 2 (not 3) if the cursor is already on the last line.
**How to avoid:** Track `prev_height` as the count of lines written. Cursor-up by `prev_height - 1` if cursor is at end of last line, or `prev_height` if cursor is on a new line after the frame.
**Warning signs:** Frame drifts down the terminal over time, or first line of previous frame remains.

### Pitfall 5: First Render Edge Case
**What goes wrong:** First render tries to erase 0 previous lines but emits cursor-up 0, which some terminals interpret differently.
**Why it happens:** `prev_height` starts at 0, and `\033[0A` behavior is undefined in some terminals.
**How to avoid:** Guard: `if prev_height > 0:` before emitting any erase sequences. First render is just a plain write.
**Warning signs:** Garbled first frame on some terminals.

### Pitfall 6: Unclosed ANSI Color Sequences
**What goes wrong:** After bar output, subsequent terminal text inherits the bar's colors.
**Why it happens:** A colored line is written but `\033[0m` reset is omitted at the end.
**How to avoid:** Every line that contains any `\033[...m` sequence MUST end with `\033[0m`. Verify with a `has_unclosed_ansi(text)` utility.
**Warning signs:** Terminal text after the bar appears colored.

### Pitfall 7: `shutil.get_terminal_size()` in Non-TTY
**What goes wrong:** Returns `(80, 24)` fallback even when actual terminal is wider/narrower.
**Why it happens:** When stdout is piped, the function can't query the terminal and returns fallback.
**How to avoid:** Check `is_tty` first. In non-TTY, use fallback width for plain text bar. Don't rely on `get_terminal_size()` for animation sizing in non-TTY.
**Warning signs:** Bar width doesn't match terminal in piped scenarios (which is fine — we fall back to text anyway).

## Code Examples

Verified patterns from Python stdlib documentation and established projects:

### Display Width Measurement
```python
import unicodedata

def disp_len(text: str) -> int:
    """Terminal display width of text, accounting for wide/combining chars.

    - East Asian Wide (W) and Fullwidth (F) characters count as 2 columns
    - Combining characters count as 0 columns
    - ANSI escape sequences count as 0 columns
    - All other characters count as 1 column
    """
    # Strip ANSI escape sequences first
    import re
    text = re.sub(r'\033\[[0-9;]*m', '', text)

    width = 0
    for char in unicodedata.normalize('NFC', text):
        if unicodedata.combining(char):
            continue
        eaw = unicodedata.east_asian_width(char)
        width += 2 if eaw in ('W', 'F') else 1
    return width
```
Source: Python `unicodedata` documentation + tqdm issue #803 pattern

### Terminal Detection
```python
import os
import sys
import shutil
from enum import Enum

class ColorTier(Enum):
    TRUE_COLOR = 3   # 24-bit
    COLOR_256 = 2    # 256 color
    COLOR_16 = 1     # Basic ANSI
    NONE = 0         # No color

def detect_terminal(stream=None) -> 'TerminalInfo':
    """Detect terminal capabilities. Returns frozen TerminalInfo."""
    if stream is None:
        stream = sys.stderr

    is_tty = hasattr(stream, 'isatty') and stream.isatty()

    # Terminal width
    width = shutil.get_terminal_size(fallback=(80, 24)).columns if is_tty else 80

    # Color support detection
    color = ColorTier.NONE
    if is_tty:
        term = os.environ.get('TERM', '')
        colorterm = os.environ.get('COLORTERM', '')
        no_color = 'NO_COLOR' in os.environ

        if no_color or term == 'dumb':
            color = ColorTier.NONE
        elif colorterm in ('truecolor', '24bit'):
            color = ColorTier.TRUE_COLOR
        elif '256color' in term:
            color = ColorTier.COLOR_256
        elif term:
            color = ColorTier.COLOR_16

    # Notebook detection
    is_notebook = False
    try:
        from IPython import get_ipython
        shell = get_ipython()
        if shell is not None:
            is_notebook = shell.__class__.__name__ == 'ZMQInteractiveShell'
    except (ImportError, NameError):
        pass

    return TerminalInfo(
        is_tty=is_tty,
        color_support=color,
        width=width,
        is_notebook=is_notebook,
    )
```
Source: Python `os.isatty` docs, `shutil.get_terminal_size` docs, IPython `get_ipython` pattern

### ANSI Renderer Core
```python
# Escape sequence constants
CURSOR_UP = '\033[{n}A'      # Move cursor up n lines
ERASE_LINE = '\033[2K'       # Erase entire current line
RESET = '\033[0m'            # Reset all attributes
CARRIAGE_RETURN = '\r'

def erase_previous(stream, height: int) -> None:
    """Erase previously rendered lines."""
    if height <= 0:
        return
    # Move to start of first previous line
    stream.write(CURSOR_UP.format(n=height))
    # Clear each line
    for i in range(height):
        stream.write(ERASE_LINE)
        if i < height - 1:
            stream.write('\n')
    # Return to start
    stream.write(CURSOR_UP.format(n=height - 1))
    stream.write(CARRIAGE_RETURN)
```
Source: ANSI escape code standard (ECMA-48), tqdm `_term_move_up` pattern

### Wall-Clock Frame Selection
```python
import time

def select_frame_index(
    frame_count: int,
    start_time: float,
    fps: float,
) -> int:
    """Select animation frame based on wall-clock elapsed time."""
    elapsed = time.monotonic() - start_time
    return int(elapsed * fps) % frame_count
```
Source: Standard game loop timing pattern, `time.monotonic` documentation

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `@dataclass` | `@dataclass(slots=True)` | Python 3.10 | ~20% faster attribute access, lower memory |
| `NamedTuple` for immutable data | `@dataclass(frozen=True)` | Python 3.7+ (mature by 3.10) | More flexible, supports `__post_init__`, default factories |
| `os.get_terminal_size()` | `shutil.get_terminal_size()` | Python 3.3 | Better fallback handling |
| `time.time()` for timing | `time.monotonic()` | Python 3.3 (standard by 3.10) | Immune to system clock adjustments |
| Custom `ioctl` for term size | `shutil.get_terminal_size()` | Python 3.3 | Cross-platform, handles edge cases |

**Deprecated/outdated:**
- `time.clock()`: Removed in Python 3.8. Use `time.monotonic()` or `time.perf_counter()`.
- Manual `struct.pack`/`fcntl.ioctl` for terminal size: Replaced by `shutil.get_terminal_size()`.

## Open Questions

1. **ANSI Erase Strategy: Per-Line vs Block Erase**
   - What we know: tqdm uses per-line `\033[2K` + cursor movement. Some renderers use `\033[J` (erase to end of screen).
   - What's unclear: Whether `\033[J` is safe in all target terminals (some may erase too much in multiplexed environments).
   - Recommendation: Use per-line erase (tqdm's approach) — safer, more predictable, well-tested in the wild.

2. **Synchronized Output (`\033[?2026h` / `\033[?2026l`)**
   - What we know: Modern terminals support synchronized output to reduce flicker. Wrapping render in sync markers prevents partial frame display.
   - What's unclear: Support matrix across terminals (xterm, iTerm2, Windows Terminal, tmux).
   - Recommendation: Defer to Phase 2 or later — nice optimization but not needed for foundation correctness.

3. **`NO_COLOR` Environment Variable Standard**
   - What we know: `NO_COLOR` (https://no-color.org/) is a growing standard — presence means disable color.
   - What's unclear: Whether `NYANBAR_DISABLE=1` should also suppress animation (just color or everything?).
   - Recommendation: `NO_COLOR` disables color only (text still animates). `NYANBAR_DISABLE=1` disables all animation (plain text bar). Handle both in terminal detection.

## Sources

### Primary (HIGH confidence)
- [Python `unicodedata` documentation](https://docs.python.org/3/library/unicodedata.html) — east_asian_width API
- [Python `dataclasses` documentation](https://docs.python.org/3/library/dataclasses.html) — frozen, slots, __post_init__
- [Python `time.monotonic` documentation](https://docs.python.org/3/library/time.html#time.monotonic) — monotonic clock
- [Python `shutil.get_terminal_size` documentation](https://docs.python.org/3/library/shutil.html#shutil.get_terminal_size) — terminal dimensions
- [ANSI Escape Codes Reference](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797) — comprehensive escape sequence list

### Secondary (MEDIUM confidence)
- [tqdm issue #803](https://github.com/tqdm/tqdm/issues/803) — east_asian_width usage pattern for display width
- [tqdm source code](https://github.com/tqdm/tqdm) — `_term_move_up`, `moveto()`, `clear()` patterns
- [IPython issue #9732](https://github.com/ipython/ipython/issues/9732) — notebook vs terminal detection

### Tertiary (LOW confidence)
- Game loop timing patterns — community consensus, not formally specified
- Synchronized output support matrix — varies by terminal, needs runtime testing

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib, well-documented, stable APIs
- Architecture: HIGH — patterns derived from tqdm source + Python best practices
- Pitfalls: HIGH — documented in tqdm issues, Python docs, and terminal rendering community
- Animation timing: HIGH — `time.monotonic()` is the established solution

**Research date:** 2026-02-25
**Valid until:** 2026-06-25 (stable stdlib APIs, 120-day validity)
