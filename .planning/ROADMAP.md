# Roadmap: nyanbar

## Overview

nyanbar is a standalone, zero-dependency progress bar library built in four phases. Phase 1 establishes the data model, animation engine, ANSI renderer, and terminal detection as pure primitives. Phase 2 implements the core NyanBar class with tqdm-compatible API (without importing tqdm), single-line rendering, stats, and all fallback paths. Phase 3 adds the theme registry and all built-in themes with multi-line rendering support. Phase 4 wires the public API, finalizes the package, and ships to PyPI.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation** - Pure primitives: Frame/Animation dataclasses, ANSI renderer, terminal detection (2026-02-25)
- [x] **Phase 2: Core Integration** - Standalone NyanBar class with tqdm-compatible API, single-line rendering, all fallbacks (2026-02-25)
- [x] **Phase 3: Theme System** - Lazy registry, multi-line rendering, all 5 built-in themes and completion frames (2026-02-25)
- [x] **Phase 4: Public API and Release** - __init__.py exports, pyproject.toml, test suite, PyPI publish (2026-02-25)

## Phase Details

### Phase 1: Foundation
**Goal**: Pure primitives (dataclasses, renderer, terminal detection, animation engine) are tested and correct
**Depends on**: Nothing (first phase)
**Requirements**: FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05, FOUND-06, FOUND-07, ANIM-01, ANIM-02, ANIM-03, ANIM-04, ANIM-05
**Success Criteria** (what must be TRUE):
  1. A Frame and Animation value can be constructed and its fields accessed; Animation.render() returns the correct frame lines for given progress, width, and elapsed time
  2. Frame width measurement uses disp_len() so emoji and CJK characters count as 2 columns, not 1
  3. Terminal detection correctly identifies TTY vs. non-TTY, color support, terminal width, and notebook environments when called with mocked os.isatty() and TERM values
  4. The ANSI renderer produces valid cursor-up and clear-line sequences for multi-line frames; no color sequence is left open after any render call
  5. Wall-clock frame selection advances animation frames based on time.monotonic() elapsed time at the configured FPS, independent of iteration count
**Plans**: 5 plans
- [x] 01-01-PLAN.md — Display width and ANSI stripping utilities (TDD)
- [x] 01-02-PLAN.md — Terminal capability detection (TDD)
- [x] 01-03-PLAN.md — Frame and Animation data model (TDD)
- [x] 01-04-PLAN.md — ANSI frame renderer (TDD)
- [x] 01-05-PLAN.md — Animation engine (TDD)

### Phase 2: Core Integration
**Goal**: Users can run `from nyanbar import tqdm` and see an animated progress bar with correct stats, fallbacks, and terminal cleanup — zero dependencies
**Depends on**: Phase 1
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, CORE-06, CORE-07, CORE-08, CORE-09, CORE-10, CORE-11, CORE-12
**Success Criteria** (what must be TRUE):
  1. `from nyanbar import tqdm; list(tqdm(range(100)))` runs without error and displays an animated single-line progress bar with percentage, rate, and ETA — no tqdm import occurs
  2. `trange(10)` works identically to `tqdm(range(10))` — same output, same kwargs accepted
  3. Non-TTY, piped output, dumb terminal (TERM=dumb), and terminal width < 30 columns all fall back silently to a plain built-in text bar with no ANSI sequences emitted
  4. `leave=True` keeps the final bar on screen; `leave=False` cleans up all lines with no residual output; an exception raised inside the loop leaves the terminal in a clean state
  5. Two simultaneous NyanBar instances (nested bars) render without overwriting each other — nested bars use single-line fallback
**Plans**: 4 plans
- [x] 02-01-PLAN.md — Stats formatting utilities: EMA, SI format, interval format, meter string (TDD)
- [x] 02-02-PLAN.md — Fallback rendering: decision logic and plain text bar (TDD)
- [x] 02-03-PLAN.md — NyanBar class core with tqdm-compatible API and public aliases
- [x] 02-04-PLAN.md — Animation thread, refresh throttle, leave/cleanup, thread safety (TDD)

### Phase 3: Theme System
**Goal**: Users can select any of 5 built-in themes by name and see correct multi-line animations through 100% completion
**Depends on**: Phase 2
**Requirements**: THEME-01, THEME-02, THEME-03, THEME-04, THEME-05, THEME-06, THEME-07, THEME-08, THEME-09, THEME-10
**Success Criteria** (what must be TRUE):
  1. `set_theme('nyan')` and `tqdm(..., theme='cat_walk')` both work; `list_themes()` returns all 5 built-in theme names; `get_theme('fish')` returns the Animation object
  2. Each theme (cat_walk, cat_bounce, nyan, fish, rocket) renders without error at 0%, 25%, 50%, 75%, and 100% progress
  3. Multi-line themes (cat_bounce, nyan, fish, rocket) use cursor-up erase correctly — no duplicate lines, no drifting rows between renders
  4. At 100% completion each theme displays its completion frame (cat sits, rocket reaches space) rather than a mid-animation frame
  5. Color themes display correctly on color-capable terminals and degrade gracefully (no garbled characters, no open ANSI sequences) on non-color terminals
**Plans**: 5 plans
- [x] 03-01-PLAN.md — Registry, render tier resolution, fallback adjustment (TDD)
- [x] 03-02-PLAN.md — cat_walk and cat_bounce themes (TDD)
- [x] 03-03-PLAN.md — nyan theme (TDD)
- [x] 03-04-PLAN.md — fish and rocket themes (TDD)
- [x] 03-05-PLAN.md — NyanBar integration, public API wiring, integration tests (TDD)

### Phase 4: Public API and Release
**Goal**: `pip install nyanbar` works and `from nyanbar import tqdm` is a complete, zero-dependency, typed, tested drop-in replacement ready for public use
**Depends on**: Phase 3
**Requirements**: API-01, API-02, API-03, TEST-01, TEST-02, TEST-03, TEST-04, TEST-05
**Success Criteria** (what must be TRUE):
  1. `from nyanbar import tqdm, trange, set_theme, Animation, Frame, list_themes, get_theme` all resolve without ImportError
  2. mypy --strict passes on the entire nyanbar package with py.typed present
  3. `pytest` passes all tests in under 2 seconds each; coverage includes tqdm compatibility, renderer output, all 5 themes at 5 progress points, and all 3 fallback conditions
  4. `pip install nyanbar` from PyPI installs successfully on Python 3.10+ with zero runtime dependencies
**Plans**: 4 plans
- [x] 04-01-PLAN.md — pyproject.toml + mypy --strict compliance
- [x] 04-02-PLAN.md — Test reorganization into 4 domain files
- [x] 04-03-PLAN.md — README + LICENSE
- [x] 04-04-PLAN.md — Build verification + clean install + publish checkpoint

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 5/5 | Complete | 2026-02-25 |
| 2. Core Integration | 4/4 | Complete | 2026-02-25 |
| 3. Theme System | 5/5 | Complete | 2026-02-25 |
| 4. Public API and Release | 4/4 | Complete | 2026-02-25 |
