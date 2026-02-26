# Architecture Research

**Domain:** Animated terminal progress bar library (tqdm subclass)
**Researched:** 2026-02-25
**Confidence:** HIGH — derived from reading tqdm source directly (`tqdm==4.67.x`) and from PROJECT.md design decisions

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         Public API Layer                          │
│  tqdm (alias)  |  trange  |  set_theme  |  list_themes           │
│  Animation     |  Frame   |  get_theme                           │
└───────────────────────────────┬──────────────────────────────────┘
                                │ subclass / delegation
┌───────────────────────────────▼──────────────────────────────────┐
│                        NyanBar Core                               │
│  Subclasses tqdm.tqdm — overrides display()                      │
│  Drives animation clock (time.monotonic)                         │
│  Selects current frame, invokes ANSI renderer                    │
│  Falls back to super().display() when disabled                   │
└──────┬──────────────────┬────────────────────┬───────────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌──────────────┐  ┌───────────────┐  ┌────────────────────────────┐
│ Theme        │  │ Animation     │  │ Terminal Detection         │
│ Registry     │  │ Engine        │  │ Utilities                  │
│              │  │               │  │                            │
│ Lazy-loads   │  │ Frame/Anim    │  │ TTY check, width, color    │
│ theme mods   │  │ dataclasses   │  │ depth, notebook detect     │
│ by name      │  │ Wall-clock    │  │ Returns: enabled | mode    │
│ THEME var    │  │ frame select  │  │                            │
└──────────────┘  └───────────────┘  └────────────────────────────┘
       │                  │
       │ Animation obj     │ frame index
       ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ANSI Renderer                             │
│  Builds output string: cursor-up + animation frame + stats      │
│  Handles single-line vs multi-line height (_prev_height)        │
│  Writes to fp (stderr by default) via sp() or direct write      │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Theme Modules                              │
│  nyanbar/themes/cat_walk.py   THEME = Animation(...)            │
│  nyanbar/themes/cat_bounce.py THEME = Animation(...)            │
│  nyanbar/themes/nyan.py       THEME = Animation(...)            │
│  nyanbar/themes/fish.py       THEME = Animation(...)            │
│  nyanbar/themes/rocket.py     THEME = Animation(...)            │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| NyanBar (core) | Iterator protocol, update loop, display() hook, fallback logic | `nyanbar/core.py` — `class NyanBar(tqdm)` |
| Animation Engine | `Frame` and `Animation` dataclasses; wall-clock frame index calculation | `nyanbar/animation.py` — dataclasses + `current_frame(t)` |
| ANSI Renderer | Build final output string; cursor movement; multi-line erase; color codes | `nyanbar/renderer.py` — `render(frame, stats, width, height)` |
| Theme Registry | Map name → `Animation`; lazy import of theme modules; built-in registration | `nyanbar/themes/__init__.py` — dict + `importlib` |
| Theme Modules | Self-contained `Animation` definitions with all frames inline | `nyanbar/themes/<name>.py` — `THEME = Animation(...)` |
| Terminal Detection | TTY, color depth, terminal width, notebook detection, dumb terminal | `nyanbar/terminal.py` — pure functions, no side effects |
| Public API | Re-export `tqdm`, `trange`, `set_theme`, etc. from single namespace | `nyanbar/__init__.py` |

---

## Recommended Project Structure

```
nyanbar/
├── __init__.py          # Public API: re-exports tqdm, trange, set_theme,
│                        # list_themes, get_theme, Animation, Frame
├── core.py              # NyanBar(tqdm) — overrides display(), holds
│                        # animation state (_frame_t0, _prev_height, _theme)
├── animation.py         # Frame and Animation dataclasses;
│                        # current_frame(animation, t) pure function
├── renderer.py          # render(frame, stats_str, width, prev_height) → str
│                        # ANSI escape sequences, multi-line erase, color
├── terminal.py          # is_tty(fp), color_support(fp), terminal_width(),
│                        # is_notebook() — pure detection functions
└── themes/
    ├── __init__.py      # Theme registry: {name: Animation | module_path}
    │                    # lazy_load(name) → Animation
    ├── cat_walk.py      # THEME = Animation(...)   single-line, 4–8 frames
    ├── cat_bounce.py    # THEME = Animation(...)   multi-line
    ├── nyan.py          # THEME = Animation(...)   multi-line, rainbow trail
    ├── fish.py          # THEME = Animation(...)   multi-line
    └── rocket.py        # THEME = Animation(...)   multi-line, completion frame

tests/
├── test_core.py         # tqdm API compatibility, fallback activation
├── test_animation.py    # Frame/Animation dataclasses, frame selection
├── test_renderer.py     # Output string correctness, ANSI codes, widths
├── test_terminal.py     # Detection utility mocking
└── test_themes.py       # All themes load, frame counts, completion frames

pyproject.toml
```

### Structure Rationale

- **core.py:** Keeps the tqdm subclass isolated. Only file that touches tqdm internals. Easier to test the override boundary.
- **animation.py:** Pure dataclasses with no I/O. Can be tested without a terminal. Frame timing logic is a pure function of `time.monotonic()` minus the epoch stored at bar open.
- **renderer.py:** Isolated string construction. Accepts primitives (frame string, stats string, int width, int prev_height), returns a string. Zero side effects — easiest to unit test.
- **terminal.py:** Pure detection functions. All accept a file object or return system values. Mockable without patching global state.
- **themes/:** Self-contained modules. The registry lazy-imports them on first use so importing `nyanbar` itself has near-zero overhead even with many themes installed.

---

## Architectural Patterns

### Pattern 1: Subclass + `display()` Override

**What:** `NyanBar` extends `tqdm.tqdm` and overrides exactly one method: `display()`. tqdm calls `display()` whenever the bar needs to render (from `refresh()`, `update()`, `close()`). NyanBar intercepts that call to substitute animated output. All other tqdm machinery (iterator protocol, `__init__` kwargs, EMA rate smoothing, position management, lock, `TMonitor`) is inherited unchanged.

**When to use:** Anytime you want drop-in compatibility without re-implementing tqdm internals.

**Trade-offs:** Must stay compatible with tqdm's `display()` signature (`msg=None, pos=None`). tqdm may call `display(msg='', pos=pos)` to clear — must handle that sentinel.

**Example:**
```python
class NyanBar(tqdm):
    def display(self, msg=None, pos=None):
        # Fallback: tqdm clears bar with msg=''
        if msg == '':
            return super().display(msg=msg, pos=pos)

        if self.disable or not self._tty:
            return super().display(msg=msg, pos=pos)

        frame = current_frame(self._animation, time.monotonic() - self._frame_t0)
        stats = self._build_stats_str()          # delegates to tqdm format_dict
        output = render(frame, stats, self._width, self._prev_height)
        self._prev_height = frame.height
        self.fp.write(output)
        self.fp.flush()
        return True
```

### Pattern 2: Wall-Clock Frame Selection (Pure Function)

**What:** Frame index is derived from elapsed wall-clock seconds, not iteration count. `current_frame(animation, elapsed)` computes `frame_index = int(elapsed / animation.frame_duration) % len(animation.frames)`. This means animation speed is constant regardless of how fast the loop runs.

**When to use:** Always for animated bars — iteration-based frame selection causes animations to freeze on slow loops and strobe on fast ones.

**Trade-offs:** Frame advances even when the loop is paused (e.g., waiting on I/O). This is intentional — the cat keeps walking even when waiting for a network call, which is the right UX.

**Example:**
```python
from dataclasses import dataclass

@dataclass
class Frame:
    lines: list[str]    # each string is one terminal row
    duration: float     # seconds this frame should display

@dataclass
class Animation:
    frames: list[Frame]
    completion_frame: Frame | None = None  # shown when n == total

def current_frame(animation: Animation, elapsed: float) -> Frame:
    total_duration = sum(f.duration for f in animation.frames)
    t = elapsed % total_duration
    acc = 0.0
    for frame in animation.frames:
        acc += frame.duration
        if t < acc:
            return frame
    return animation.frames[-1]
```

### Pattern 3: Lazy Theme Registry

**What:** The registry stores `{name: str | Animation}`. Initially values are the module path string. On first access, the registry imports the module, reads `THEME`, caches the `Animation` object, and returns it. Subsequent accesses hit the cache.

**When to use:** When you want fast imports even with many themes available. Users who only use `cat_walk` should not pay the import cost of `nyan.py`.

**Trade-offs:** First access per theme has a small `importlib` overhead. Acceptable since it happens once per program run, before the loop starts.

**Example:**
```python
import importlib

_REGISTRY: dict[str, str | Animation] = {
    "cat_walk":   "nyanbar.themes.cat_walk",
    "cat_bounce": "nyanbar.themes.cat_bounce",
    "nyan":       "nyanbar.themes.nyan",
    "fish":       "nyanbar.themes.fish",
    "rocket":     "nyanbar.themes.rocket",
}

def get_theme(name: str) -> Animation:
    entry = _REGISTRY[name]
    if isinstance(entry, str):
        mod = importlib.import_module(entry)
        _REGISTRY[name] = mod.THEME
    return _REGISTRY[name]
```

### Pattern 4: Multi-Line Erase via Cursor-Up

**What:** Multi-line themes occupy N terminal rows. On each render, the renderer emits `\x1b[A` (cursor up) repeated `prev_height - 1` times, then `\r`, then the new frame lines joined by `\n`. This overwrites the previous output in place without scrolling.

**When to use:** Any theme where `len(frame.lines) > 1`. Single-line themes use the simpler `\r` + overwrite pattern (same as stock tqdm).

**Trade-offs:** Requires tracking previous rendered height (`_prev_height`) in NyanBar state. If height changes between frames (e.g., completion frame is different size), must erase old height before writing new height.

**Example:**
```python
def render(frame: Frame, stats: str, width: int, prev_height: int) -> str:
    erase = ('\x1b[A' * (prev_height - 1) + '\r') if prev_height > 1 else '\r'
    lines = _layout(frame, stats, width)   # fit frame + stats into width columns
    return erase + '\n'.join(lines)
```

---

## Data Flow

### Iteration Flow (happy path)

```
User code: for item in NyanBar(iterable):
    │
    ▼
NyanBar.__iter__()           [inherited from tqdm]
    │  yields item to user code
    │  after each yield: checks miniters + mininterval throttle
    │
    ▼ (when throttle allows)
NyanBar.update(n)            [inherited from tqdm]
    │  increments self.n, updates EMA rate
    │
    ▼
NyanBar.refresh()            [inherited from tqdm]
    │
    ▼
NyanBar.display()            [OVERRIDDEN — entry point for animation]
    │
    ├──► terminal.is_tty() + terminal.terminal_width()
    │         → if not TTY or width < 30: super().display() and return
    │
    ├──► themes.get_theme(self._theme_name)
    │         → Animation object (lazy-loaded once)
    │
    ├──► animation.current_frame(anim, time.monotonic() - self._frame_t0)
    │         → Frame object
    │
    ├──► self._build_stats_str()   [uses tqdm format_dict + format_meter]
    │         → "42% 3.1it/s ETA 0:00:12"
    │
    ├──► renderer.render(frame, stats, width, self._prev_height)
    │         → final ANSI string ready to write
    │
    └──► self.fp.write(output); self.fp.flush()
         self._prev_height = frame.height
```

### Completion Flow

```
NyanBar.close()              [inherited from tqdm]
    │  calls display() one final time with pos=0
    ▼
NyanBar.display()
    │  detects self.n == self.total
    ├──► animation.completion_frame if present, else last regular frame
    ├──► renderer.render(completion_frame, final_stats, width, prev_height)
    └──► self.fp.write(output + '\n')   [tqdm handles the newline via close()]
```

### Fallback Flow

```
NyanBar.display()
    │
    ├── terminal.is_tty() → False       (piped, CI, redirected)
    │   OR
    ├── terminal.terminal_width() < 30  (too narrow)
    │   OR
    ├── self.disable == True            (set by user or non-TTY __init__)
    │
    └──► super().display(msg, pos)      [stock tqdm output, zero animation overhead]
```

### Theme Load Flow (one-time per theme)

```
NyanBar.__init__()
    │  self._theme_name = current_theme or default
    │  (does NOT load Animation yet)
    │
    ▼ (first display() call)
themes.get_theme(name)
    │  registry[name] is str → importlib.import_module(path)
    │  → mod.THEME  (Animation object defined inline in theme file)
    │  → cache in registry[name]
    └──► return Animation
```

---

## Anti-Patterns

### Anti-Pattern 1: Wrapping tqdm Instead of Subclassing

**What people do:** Create a `NyanBar` class that holds a `tqdm` instance as `self._bar` and delegates all method calls.

**Why it's wrong:** `isinstance(bar, tqdm)` checks fail. Context manager (`with NyanBar(...) as t`) semantics diverge. tqdm's position management (`_instances`, `_get_free_pos`) is never invoked, so nested bars break. External code that checks `bar.n`, `bar.total`, `bar.format_dict` must be duplicated. Every new tqdm feature requires manual wrapper updates.

**Do this instead:** `class NyanBar(tqdm): ...` — override only `display()`. Inherit everything else.

### Anti-Pattern 2: Iteration-Based Frame Advance

**What people do:** Advance the animation frame each time `update()` is called (`self._frame_idx = (self._frame_idx + 1) % len(frames)`).

**Why it's wrong:** Animation speed couples to iteration rate. A fast loop (100k items/s) causes strobing; a slow loop (1 item/s) causes near-freezing. The animation looks broken in both cases.

**Do this instead:** `current_frame(animation, time.monotonic() - self._frame_t0)` — wall-clock elapsed determines the frame. Speed is constant regardless of iteration rate.

### Anti-Pattern 3: Rendering on Every Iteration

**What people do:** Call the renderer unconditionally inside `update()` or `__iter__`.

**Why it's wrong:** ANSI writes + string construction are not free. A loop at 1M items/s would spend more time rendering than iterating. tqdm's `mininterval` throttle (default 100ms) exists precisely to prevent this.

**Do this instead:** Override `display()` only. tqdm's `update()` and `__iter__` machinery call `display()` only when the throttle allows, automatically. NyanBar gets rate limiting for free.

### Anti-Pattern 4: Global Mutable Theme State

**What people do:** Store the active theme in a module-level global variable that `set_theme()` mutates, then read it inside `display()`.

**Why it's wrong:** Not thread-safe when multiple bars run concurrently. Per-bar themes become impossible. `set_theme()` called between bar creation and first iteration produces surprising results.

**Do this instead:** Store `self._theme_name` on each `NyanBar` instance during `__init__`. `set_theme()` updates a module-level default that `__init__` reads at construction time — not at render time. Each bar captures its theme at creation.

### Anti-Pattern 5: Loading All Themes at Import Time

**What people do:** `from nyanbar.themes.cat_walk import THEME; from nyanbar.themes.nyan import THEME; ...` at the top of `themes/__init__.py`.

**Why it's wrong:** Every `from nyanbar import tqdm` pays the import cost of all themes. Themes with many frames (nyan's rainbow trail) can be large. Users who never change from the default theme pay for themes they never use.

**Do this instead:** Lazy registry — store module paths as strings, import on first `get_theme()` call per theme name.

---

## Component Boundaries (what talks to what)

| From | To | Via | Notes |
|------|----|-----|-------|
| NyanBar.display() | animation.current_frame() | direct call | passes elapsed float, receives Frame |
| NyanBar.display() | themes.get_theme() | direct call | passes name str, receives Animation |
| NyanBar.display() | terminal.is_tty() | direct call | passes self.fp, receives bool |
| NyanBar.display() | terminal.terminal_width() | direct call | no args, receives int |
| NyanBar.display() | renderer.render() | direct call | passes Frame + stats str + ints |
| NyanBar.display() | super().display() | inherited method | fallback path only |
| NyanBar._build_stats_str() | self.format_dict | tqdm property | uses tqdm's computed stats dict |
| themes.get_theme() | theme module | importlib | one-time lazy import per theme |
| theme module | animation.Animation / Frame | dataclass instantiation | THEME defined inline |

**Key boundary rule:** The renderer knows nothing about tqdm, NyanBar, or themes. It takes only primitives (strings and ints) and returns a string. This makes it trivially testable without a real terminal or tqdm instance.

---

## Suggested Build Order (dependency-based)

Build in this order because each layer depends only on what's below it:

```
1. animation.py          No dependencies except stdlib dataclasses.
                         Define Frame, Animation, current_frame().
                         Test: pure unit tests, no terminal needed.

2. terminal.py           No dependencies. Pure detection functions.
                         Test: mock sys.stdout.isatty, shutil.get_terminal_size.

3. renderer.py           Depends on: animation.Frame (type only).
                         Test: construct Frame objects, assert output strings.

4. themes/cat_walk.py    Depends on: animation.Frame, animation.Animation.
   (one theme first)     Single-line theme — simplest case, validates dataclasses.
                         Test: THEME loads, frame count correct, no syntax errors.

5. core.py (NyanBar)     Depends on: animation, terminal, renderer, themes.
                         Start with single-line mode + fallback only.
                         Test: tqdm API compat, fallback activation, no crash.

6. themes/ (remaining)   Depends on: animation.Frame, animation.Animation.
                         Add cat_bounce, nyan, fish, rocket one at a time.
                         Test: each theme renders without error.

7. core.py multi-line    Depends on: multi-line themes existing, renderer.
                         Add _prev_height tracking and cursor-up erase logic.
                         Test: multi-line themes render in-place correctly.

8. themes/__init__.py    Depends on: all theme modules.
   (registry)            Finalize lazy loading, set_theme(), list_themes().
                         Test: lazy load doesn't import at module import time.

9. nyanbar/__init__.py   Depends on: everything above.
   (public API)          Wire up tqdm/trange aliases, re-export Animation/Frame.
                         Test: `from nyanbar import tqdm` works as drop-in.
```

**Rationale for this order:**
- Steps 1–3 are pure/testable with no terminal or tqdm dependency — build confidence early.
- Step 4 (one theme) validates the dataclass design before committing to more frames.
- Step 5 (core with single-line only) gets the tqdm compatibility boundary right before adding rendering complexity.
- Multi-line (step 7) is the hardest rendering problem; deferring it means core compatibility is proven before tackling cursor gymnastics.
- The registry and public API are glue — they go last when all pieces are proven.

---

## Scaling Considerations

This library has no server-side scaling dimension — it runs in a single terminal process. "Scaling" here means:

| Concern | Approach |
|---------|----------|
| Many frames per theme | Frames are in-memory Python lists; no I/O. 100+ frames are fine. |
| Many concurrent bars (nested) | tqdm's position management + lock already handles this. NyanBar inherits it. Disable multi-line for `position > 0` bars — multi-line + nested = cursor chaos. |
| Fast iteration loops (>100k/s) | tqdm's `mininterval` throttle (default 0.1s) caps render rate at ~10Hz regardless. NyanBar adds no overhead to the hot loop. |
| Very wide terminals | Calculate stats width first; give remainder to animation. Cap animation width at a reasonable maximum (e.g., 40 cols) to avoid stretched sprites. |
| Themes with many lines | Reserve terminal rows: check `nrows` (terminal height) before writing multi-line. tqdm already tracks `nrows`. |

---

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| NyanBar ↔ tqdm | Subclass inheritance | Only `display()` overridden; all other methods inherited |
| NyanBar ↔ renderer | Direct function call | Renderer is stateless; NyanBar holds `_prev_height` |
| NyanBar ↔ themes | Registry function call | Lazy; NyanBar stores only theme name, not Animation |
| NyanBar ↔ terminal | Direct function calls | Called once per display(); results not cached (width can change) |
| theme modules ↔ animation | Import / instantiation | Modules reference animation.Frame and animation.Animation |

### External Integration (tqdm compatibility surface)

| tqdm Mechanism | NyanBar handling |
|----------------|-----------------|
| `display(msg=None, pos=None)` | Overridden — animation render or fallback |
| `display(msg='', pos=pos)` | Pass to super() — tqdm uses this to clear bars |
| `format_dict` property | Read via `self.format_dict` to build stats string |
| `_lock`, position management | Fully inherited — no changes |
| `disable=True` path | Inherited `__init__` sets `self.disable`; `display()` checks it first |
| `bar_format` kwarg | Unused by NyanBar when animating; respected on fallback path |
| `trange` | Re-exported as `lambda *a, **kw: NyanBar(range(*a), **kw)` |

---

## Sources

- tqdm source read directly: `/tmp/tqdm_env/lib/python3.14/site-packages/tqdm/std.py` (1524 lines), `utils.py`, `_monitor.py` — confidence HIGH
- tqdm `display()` docstring explicitly states: *"Consider overloading this function when inheriting"* — confirms the subclass+override pattern is the intended extension point — confidence HIGH
- PROJECT.md design decisions (subclass approach, wall-clock timing, ANSI over curses, lazy themes, inline frames) — confidence HIGH (these are project constraints, not ecosystem patterns)

---
*Architecture research for: animated terminal progress bar library (nyanbar / tqdm subclass)*
*Researched: 2026-02-25*
