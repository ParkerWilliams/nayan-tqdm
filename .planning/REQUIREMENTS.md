# Requirements: nyanbar

**Defined:** 2026-02-25
**Core Value:** tqdm-compatible API with zero dependencies — standalone reimplementation of tqdm's user-facing API

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Foundation

- [ ] **FOUND-01**: Frame and Animation dataclasses define sprite data with frozen immutability
- [ ] **FOUND-02**: Animation.render() returns correct frame lines for given progress, width, and elapsed time
- [ ] **FOUND-03**: Frame width uses terminal display width (custom disp_len), not Python len()
- [ ] **FOUND-04**: Terminal detection identifies TTY, color support, terminal width, and notebook environments
- [ ] **FOUND-05**: ANSI renderer produces correct cursor-up, clear-line, and color reset escape sequences
- [ ] **FOUND-06**: Renderer handles multi-line frame erase with correct prev_height tracking
- [ ] **FOUND-07**: All ANSI color sequences are properly closed with reset codes

### Core Compatibility

- [ ] **CORE-01**: NyanBar implements tqdm-compatible API (total, desc, unit, disable, file, etc.) with zero dependencies
- [ ] **CORE-02**: `from nyanbar import tqdm` works as a drop-in replacement for `from tqdm import tqdm`
- [ ] **CORE-03**: `trange(n)` shorthand works identically to `tqdm(range(n))`
- [ ] **CORE-04**: NyanBar implements __iter__, __enter__/__exit__, update(), close(), set_description(), set_postfix()
- [ ] **CORE-05**: Non-TTY and piped output falls back to plain built-in text bar with no ANSI sequences
- [ ] **CORE-06**: Dumb terminal (TERM=dumb) falls back to plain built-in text bar
- [ ] **CORE-07**: Terminal width < 30 columns falls back to plain built-in text bar
- [ ] **CORE-08**: Stats display (percentage, rate, ETA) renders alongside animation
- [ ] **CORE-09**: leave=True preserves final animation frame; leave=False cleans up all lines
- [ ] **CORE-10**: Nested bars (position > 0) disable multi-line and use single-line fallback
- [ ] **CORE-11**: Exception during iteration cleans up terminal state correctly
- [ ] **CORE-12**: Thread safety via threading.Lock for concurrent access

### Themes

- [ ] **THEME-01**: Theme registry supports lazy loading of theme modules
- [ ] **THEME-02**: get_theme(), list_themes() API for theme discovery
- [ ] **THEME-03**: set_theme() sets global default theme; theme= kwarg sets per-instance theme
- [ ] **THEME-04**: cat_walk theme renders single-line cat walking across bar with progress
- [ ] **THEME-05**: cat_bounce theme renders 2-line cat bouncing above filled bar
- [ ] **THEME-06**: nyan theme renders 3-line nyan cat with rainbow trail and twinkling stars
- [ ] **THEME-07**: fish theme renders 3-line swimming fish with rising water level
- [ ] **THEME-08**: rocket theme renders 4-line rocket launching with flame animation
- [ ] **THEME-09**: Themes define completion frames (cat sits, rocket in space, etc.)
- [ ] **THEME-10**: Color themes gracefully degrade on non-color terminals

### Animation Engine

- [ ] **ANIM-01**: Frame selection uses wall-clock time (time.monotonic), not iteration count
- [ ] **ANIM-02**: Animation FPS is configurable per theme
- [ ] **ANIM-03**: Walk mode positions sprite based on progress percentage
- [ ] **ANIM-04**: Cycle mode keeps sprite in place and cycles animation frames
- [ ] **ANIM-05**: Fill mode fills the bar area with animation

### Public API

- [ ] **API-01**: __init__.py exports tqdm, trange, set_theme, Animation, Frame, list_themes, get_theme
- [ ] **API-02**: py.typed marker file present for PEP 561 type checking support
- [ ] **API-03**: pyproject.toml configured with correct metadata, dependencies, and build system

### Testing

- [ ] **TEST-01**: Test suite covers tqdm API compatibility (all standard kwargs work)
- [ ] **TEST-02**: Test suite covers ANSI renderer output correctness
- [ ] **TEST-03**: Test suite covers each theme renders without error at 0%, 25%, 50%, 75%, 100%
- [ ] **TEST-04**: Test suite covers fallback behavior in non-TTY, dumb terminal, and narrow terminal
- [ ] **TEST-05**: All tests complete in under 2 seconds each

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Notebook Support

- **NOTE-01**: Jupyter notebook rendering uses HTML/CSS animations instead of ANSI
- **NOTE-02**: Auto-detection of notebook environment switches rendering mode

### Platform

- **PLAT-01**: Windows colorama integration for cmd.exe ANSI support
- **PLAT-02**: asyncio native support

### Ecosystem

- **ECO-01**: Plugin/theme discovery protocol for community themes
- **ECO-02**: Theme marketplace or registry for sharing custom themes

### Additional Themes

- **XTHM-01**: Moon phases theme (🌑 to 🌕)
- **XTHM-02**: Rubber duck bobbing in rising water theme
- **XTHM-03**: Additional creative community-inspired themes

## Out of Scope

| Feature | Reason |
|---------|--------|
| Jupyter HTML/CSS rendering | Separate rendering model, high complexity; v1 falls back to plain text bar |
| Rich library integration | Fundamentally incompatible output model (Rich owns the console) |
| curses-based rendering | Windows-incompatible, overkill for the use case |
| External asset files for themes | Breaks packaging simplicity; all frames defined inline in Python |
| Any runtime dependencies | nyanbar is zero-dependency by design |
| tqdm as a dependency | Standalone reimplementation, no import of tqdm |
| Mobile/GUI version | Terminal-only library |
| Config files for default themes | set_theme() at script top is sufficient |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Pending |
| FOUND-03 | Phase 1 | Pending |
| FOUND-04 | Phase 1 | Pending |
| FOUND-05 | Phase 1 | Pending |
| FOUND-06 | Phase 1 | Pending |
| FOUND-07 | Phase 1 | Pending |
| ANIM-01 | Phase 1 | Pending |
| ANIM-02 | Phase 1 | Pending |
| ANIM-03 | Phase 1 | Pending |
| ANIM-04 | Phase 1 | Pending |
| ANIM-05 | Phase 1 | Pending |
| CORE-01 | Phase 2 | Pending |
| CORE-02 | Phase 2 | Pending |
| CORE-03 | Phase 2 | Pending |
| CORE-04 | Phase 2 | Pending |
| CORE-05 | Phase 2 | Pending |
| CORE-06 | Phase 2 | Pending |
| CORE-07 | Phase 2 | Pending |
| CORE-08 | Phase 2 | Pending |
| CORE-09 | Phase 2 | Pending |
| CORE-10 | Phase 2 | Pending |
| CORE-11 | Phase 2 | Pending |
| CORE-12 | Phase 2 | Pending |
| THEME-01 | Phase 3 | Pending |
| THEME-02 | Phase 3 | Pending |
| THEME-03 | Phase 3 | Pending |
| THEME-04 | Phase 3 | Pending |
| THEME-05 | Phase 3 | Pending |
| THEME-06 | Phase 3 | Pending |
| THEME-07 | Phase 3 | Pending |
| THEME-08 | Phase 3 | Pending |
| THEME-09 | Phase 3 | Pending |
| THEME-10 | Phase 3 | Pending |
| API-01 | Phase 4 | Pending |
| API-02 | Phase 4 | Pending |
| API-03 | Phase 4 | Pending |
| TEST-01 | Phase 4 | Pending |
| TEST-02 | Phase 4 | Pending |
| TEST-03 | Phase 4 | Pending |
| TEST-04 | Phase 4 | Pending |
| TEST-05 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 42 total
- Mapped to phases: 42
- Unmapped: 0

---
*Requirements defined: 2026-02-25*
*Last updated: 2026-02-25 after roadmap creation*
