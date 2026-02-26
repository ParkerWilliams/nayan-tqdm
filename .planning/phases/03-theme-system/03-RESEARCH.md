# Phase 3: Theme System - Research

**Researched:** 2026-02-25
**Domain:** Theme registry with lazy loading, 5 built-in animated themes, terminal capability detection tiers, completion frames, and color degradation
**Confidence:** HIGH

## Summary

Phase 3 adds the theme system to nyanbar: a registry that maps theme names to `Animation` objects, 5 built-in themes (cat_walk, cat_bounce, nyan, fish, rocket), a 3-tier rendering system (emoji > unicode > ASCII), and integration with the existing `NyanBar` class from Phase 2.

The existing architecture is well-prepared for this. `Animation` and `Frame` dataclasses from Phase 1 already support `completion_frame`, multiple animation modes (WALK, CYCLE, FILL), and wall-clock frame selection. `NyanBar` from Phase 2 already has an `_animation` attribute (currently `None`) and a working animation thread that renders via `render_animation()` from `engine.py`. The main work is: (1) build the registry, (2) define the 5 theme animations with 3 rendering tiers each, (3) wire registry lookups into `NyanBar.__init__`, and (4) add terminal capability-based tier selection.

**Primary recommendation:** Build the registry as a simple module-level dict with lazy-loading factory functions. Define each theme in its own submodule under `nyanbar/themes/`. Wire the registry into `NyanBar` via the existing `_animation` attribute. Add a `render_level` parameter to `NyanBar` and detection logic to `terminal.py` for auto-selecting the rendering tier.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Theme Visual Design
- Each theme must have 3 rendering tiers: emoji (best), unicode (middle), ASCII (fallback)
- Auto-detect terminal capability and select the highest supported tier
- Classic Nyan Cat style for the nyan theme -- rainbow trail, pop-tart body, starfield background, faithful to the original meme
- Each theme integrates the progress bar differently (mixed approach): e.g., cat walks across, rocket launches vertically above bar
- Animation speed is fixed FPS, independent of progress rate

#### Completion Frames
- Completion frames are optional per theme -- only added where they make sense for the art
- If a theme defines a completion frame, it displays at 100%; otherwise the animation just stops on the last frame
- Stats line (percentage, rate, time) persists after completion -- no summary replacement
- When leave=True, the completion frame (if defined) stays on screen

#### Color Degradation
- The 3-tier rendering system (emoji/unicode/ASCII) handles degradation naturally
- Terminal capability auto-detection by default (TERM, COLORTERM, locale sniffing)
- User override available via `render_level='ascii'|'unicode'|'emoji'` kwarg to force a specific tier
- ASCII-tier theme art is still attempted on dumb terminals (TERM=dumb) -- not collapsed to plain text fallback
- Nyan cat rainbow trail uses patterned stripes (different ASCII characters per stripe: =, ~, -, .) when color is unavailable

#### Registry Behavior
- Default theme is `nyan` (the namesake of the library)
- Invalid theme names fall back to the default theme with a warning (not an exception)
- `register_theme(name, animation)` API available for users to add custom themes
- `set_theme()` affects only future bars -- currently running bars keep their assigned theme
- `list_themes()` returns all registered theme names (built-in + custom)
- `get_theme(name)` returns the Animation object for a given theme name

### Claude's Discretion
- Exact ASCII/unicode/emoji art for each theme character
- Animation frame count and FPS per theme
- Multi-line layout dimensions per theme
- Auto-detection logic details (which env vars, what thresholds)
- Whether piped output uses ASCII-tier or plain fallback (safe choice)
</user_constraints>

## Existing Architecture Analysis

### What Phase 1 and 2 Already Provide

**models.py:**
- `Frame(lines: tuple[str, ...])` -- frozen dataclass, auto-computes `display_width` and `height`
- `Animation(name, frames, fps=12.0, mode=AnimationMode.WALK, completion_frame=None)` -- frozen dataclass
- `AnimationMode.WALK` (sprite moves with progress), `CYCLE` (stays in place, cycles frames), `FILL` (tiles pattern)

**engine.py:**
- `render_animation(animation, progress, width, elapsed) -> list[str]` -- handles completion frame at 100%, frame selection by elapsed time, all three modes
- `select_frame_index(frame_count, elapsed, fps)` -- wall-clock frame cycling
- `walk_position()`, `cycle_position()`, `fill_pattern()` -- mode-specific positioning

**renderer.py:**
- `render_frame(lines, prev_height, stream) -> int` -- erases previous frame, writes new lines, returns new height
- `erase_lines(stream, count)` -- cursor-up + erase for multi-line cleanup
- `ensure_reset(line)` -- appends ANSI reset if line has color codes

**terminal.py:**
- `ColorTier` enum: NONE, COLOR_16, COLOR_256, TRUE_COLOR
- `TerminalInfo(is_tty, color_support, width, is_notebook)` -- frozen dataclass
- `detect_terminal(stream)` -- detects TTY, color support, width, notebook

**core.py (NyanBar):**
- `self._animation = None` -- already present, waiting for theme system
- `self._terminal = detect_terminal(self.file)` -- terminal info already captured
- `_start_animation_thread()` -- checks `self._animation is not None` before starting
- `_render_animation_frame()` -- calls `render_animation()` from engine.py
- `_render_final()` -- handles completion frame rendering at close time
- `self._use_fallback` -- already computed from terminal detection

**fallback.py:**
- `should_use_fallback(info, disable, position)` -- returns True for non-TTY, TERM=dumb, width<30, position>0

### Integration Points for Phase 3

1. **Registry -> NyanBar.__init__:** When NyanBar is constructed, look up the theme name and set `self._animation` to the resolved `Animation` object.

2. **Tier selection -> Theme factories:** Each theme module exports a factory function that takes a `RenderTier` (emoji/unicode/ascii) and returns an `Animation`. The tier is determined from `TerminalInfo.color_support` and optional user override.

3. **Public API -> __init__.py:** `set_theme`, `list_themes`, `get_theme`, `register_theme` are module-level functions in the registry, re-exported from `__init__.py`.

4. **NyanBar kwarg:** Add `theme=` and `render_level=` kwargs to NyanBar constructor.

## Architecture Decisions

### Registry Design

A module-level dict mapping `str -> Callable[RenderTier] -> Animation` (lazy factory). Built-in themes register on import. Custom themes register via `register_theme()`.

```python
# nyanbar/registry.py
_themes: dict[str, Callable[[str], Animation]] = {}
_default_theme: str = "nyan"

def register_theme(name: str, factory: Callable[[str], Animation]) -> None: ...
def get_theme(name: str, tier: str = "emoji") -> Animation: ...
def list_themes() -> list[str]: ...
def set_theme(name: str) -> None: ...
```

Why lazy factories instead of pre-built Animation objects:
- Each theme has 3 tiers (emoji, unicode, ascii) = 15 Animation objects if eager
- Users typically use 1 theme at 1 tier
- Lazy: only build the Animation you actually need

### Rendering Tier Detection

Map `ColorTier` from terminal.py to render tier:

| ColorTier | Default Render Tier | Reason |
|-----------|-------------------|--------|
| TRUE_COLOR | emoji | Full unicode + color support implied |
| COLOR_256 | emoji | Most modern terminals with 256color support emoji |
| COLOR_16 | unicode | Basic color, emoji may not render well |
| NONE | ascii | No color, safe ASCII only |

Also check locale for UTF-8 support (emoji/unicode need UTF-8 encoding):
- `LANG`, `LC_ALL`, `LC_CTYPE` environment variables
- If none contain "UTF-8" or "utf-8", downgrade to ascii tier even if color available

User override via `render_level='ascii'|'unicode'|'emoji'` bypasses auto-detection.

### Theme Module Structure

```
nyanbar/
  themes/
    __init__.py       # imports and registers all built-in themes
    _cat_walk.py      # cat_walk theme factory
    _cat_bounce.py    # cat_bounce theme factory
    _nyan.py          # nyan theme factory
    _fish.py          # fish theme factory
    _rocket.py        # rocket theme factory
  registry.py         # theme registry (get/set/list/register)
```

Each theme module defines a factory function:
```python
def create(tier: str) -> Animation:
    if tier == "emoji":
        return _create_emoji()
    elif tier == "unicode":
        return _create_unicode()
    else:
        return _create_ascii()
```

### Theme Design Specifications

#### cat_walk (THEME-04)
- **Mode:** WALK (sprite moves left-to-right with progress)
- **Lines:** 1 (single-line)
- **Frames:** 2 walking frames (legs alternating)
- **FPS:** 4 (slow walk cadence)
- **Completion:** Cat sitting (optional)
- **Emoji tier:** Cat emoji with paw variants
- **Unicode tier:** Cat face with body characters
- **ASCII tier:** Simple text cat like `=^.^=`

#### cat_bounce (THEME-05)
- **Mode:** WALK (cat moves with progress, bounces vertically)
- **Lines:** 2 (cat on top row, bar-like ground on bottom)
- **Frames:** 4 bounce frames (up/down positions)
- **FPS:** 6 (bouncy rhythm)
- **Completion:** Cat sitting on ground
- **Emoji tier:** Cat emoji bouncing
- **Unicode tier:** Cat with box-drawing ground
- **ASCII tier:** Text cat with dash ground

#### nyan (THEME-06)
- **Mode:** WALK (nyan cat moves with progress)
- **Lines:** 3 (starfield top, cat + rainbow middle, starfield bottom)
- **Frames:** 4 (rainbow trail cycling, star twinkling)
- **FPS:** 8 (smooth animation)
- **Completion:** Cat at far right, full rainbow trail
- **Key:** Rainbow trail uses ANSI color codes for colored stripes, patterned characters (=, ~, -, .) for ASCII tier
- **Emoji tier:** Pop-tart cat emoji, colored rainbow, star emoji
- **Unicode tier:** Box-drawing cat, colored bars, unicode stars
- **ASCII tier:** Text cat, patterned stripes (=~-.), asterisks for stars

#### fish (THEME-07)
- **Mode:** WALK (fish swims with progress)
- **Lines:** 3 (sky/air top, water surface middle, fish + underwater bottom)
- **Frames:** 3 (tail wiggle animation)
- **FPS:** 6
- **Completion:** Fish at surface, splash
- **Emoji tier:** Fish emoji, wave emoji, bubble emoji
- **Unicode tier:** Unicode fish, tilde waves, circle bubbles
- **ASCII tier:** `><>` fish, `~` waves, `o` bubbles

#### rocket (THEME-08)
- **Mode:** CYCLE (rocket stays in place, progress shown by flame/altitude)
- **Lines:** 4 (rocket top, body, flame, ground/launch pad)
- **Frames:** 3 (flame flicker animation)
- **FPS:** 8
- **Completion:** Rocket at top (in space), stars around it
- **Emoji tier:** Rocket emoji, fire emoji, star emoji
- **Unicode tier:** Triangle rocket, block flame, dot stars
- **ASCII tier:** `/\` rocket, `*` flame, `.` stars

### NyanBar Integration

In `NyanBar.__init__`, after terminal detection and fallback decision:

```python
# Theme resolution (Phase 3)
if not self._use_fallback:
    tier = _resolve_render_tier(self._terminal, render_level)
    theme_name = theme or _get_default_theme()
    self._animation = _get_theme_animation(theme_name, tier)
```

Where `_resolve_render_tier` maps `TerminalInfo.color_support` to "emoji"/"unicode"/"ascii" with optional user override, and `_get_theme_animation` calls the registry.

### Fallback Behavior Notes

Per CONTEXT.md: "ASCII-tier theme art is still attempted on dumb terminals (TERM=dumb) -- not collapsed to plain text fallback."

This means the current `should_use_fallback()` logic needs adjustment:
- Currently: `TERM=dumb` -> `ColorTier.NONE` -> `should_use_fallback = True` (no animation)
- Phase 3: `TERM=dumb` should still allow ASCII-tier animation if TTY is true

The adjustment: `should_use_fallback` should only be True for truly non-interactive outputs (non-TTY, piped). For TTY with `ColorTier.NONE` (dumb terminal), we still render animation but at ASCII tier.

Also need to update for narrow terminals: width < 30 still falls back to plain text.

### Warning on Invalid Theme

Per CONTEXT.md: "Invalid theme names fall back to the default theme with a warning (not an exception)."

Use `warnings.warn()` with a `UserWarning`:
```python
import warnings
warnings.warn(f"Unknown theme '{name}', using default '{_default_theme}'", UserWarning, stacklevel=2)
```

## Requirement Mapping

| Requirement | Component | Notes |
|-------------|-----------|-------|
| THEME-01 | registry.py | Lazy loading via factory functions |
| THEME-02 | registry.py | `get_theme()`, `list_themes()` |
| THEME-03 | registry.py + core.py | `set_theme()` global, `theme=` kwarg |
| THEME-04 | themes/_cat_walk.py | Single-line WALK mode |
| THEME-05 | themes/_cat_bounce.py | 2-line WALK mode with bounce |
| THEME-06 | themes/_nyan.py | 3-line WALK mode, rainbow trail |
| THEME-07 | themes/_fish.py | 3-line WALK mode, water level |
| THEME-08 | themes/_rocket.py | 4-line CYCLE mode, flame |
| THEME-09 | All theme modules | `completion_frame` on Animation |
| THEME-10 | registry.py + terminal.py | 3-tier system + auto-detection |

## Risk Assessment

1. **Multi-line rendering bugs:** The `render_frame()` and `erase_lines()` from Phase 1 handle multi-line correctly, but the interaction with the animation thread needs care. The `_prev_height` tracking in `_render_animation_frame()` already handles variable heights. Risk: LOW.

2. **Emoji display width:** Some terminals render emoji at unexpected widths (1 vs 2 columns). The `disp_len()` function from Phase 1 handles East Asian Width correctly, but emoji widths vary by terminal. Mitigation: use well-known single-codepoint emoji that are consistently 2 columns wide. Risk: MEDIUM.

3. **ASCII art alignment:** Multi-line ASCII art must have consistent display widths across all lines in a frame. If lines have different widths, `render_frame()` will misalign. Mitigation: pad all lines to the same width within each Frame. Risk: LOW (just be careful in art definition).

4. **Fallback logic change:** Adjusting `should_use_fallback()` to allow ASCII-tier animation on dumb terminals (per CONTEXT.md) requires updating existing tests. Risk: LOW (surgical change).

## RESEARCH COMPLETE
