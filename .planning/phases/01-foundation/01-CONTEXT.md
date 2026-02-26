# Phase 1: Foundation - Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Pure primitives: Frame/Animation dataclasses, ANSI renderer, terminal detection, and animation engine modes. No NyanBar class, no tqdm-compatible API — those are Phase 2. This phase builds the testable foundation that everything else sits on.

**Critical architecture constraint:** nyanbar is standalone with zero dependencies. It does NOT import or depend on tqdm. It reimplements tqdm's user-facing API. The fallback for rendering errors is a plain built-in text bar, not tqdm.

</domain>

<decisions>
## Implementation Decisions

### Character Set & Art Style
- Each theme ships in multiple art-style variants using suffix naming: `cat_walk` (Unicode default), `cat_walk.ascii`, `cat_walk.emoji`
- Unicode is the default when user selects a base theme name (e.g., `theme='cat_walk'` → Unicode variant)
- If Unicode can't render in the current terminal, auto-downgrade silently to the `.ascii` variant
- Every theme must have an `.ascii` variant; `.emoji` variants only where natural (nyan, fish, rocket — not necessarily all)
- One theme file per theme containing all variants as separate Animation objects
- Theme-matched bar characters — each theme picks fill/empty chars that fit its aesthetic (e.g., `━━━╌╌╌` for cat, `~~~≋≋≋` for fish)
- Per-theme color palettes — each theme defines its own ANSI colors inline
- Keep sprites compact: max 4-5 chars wide, 3 lines tall
- Completion frames are nice-to-have — include where natural, don't force on every theme
- No terminal bell/beep — visual only
- `list_themes()` returns grouped listing: `{'cat_walk': ['unicode', 'ascii', 'emoji'], ...}`
- `theme='random'` picks a random built-in theme each time
- `python -m nyanbar demo` shows all themes with a sample progress run
- Animation/Frame dataclasses are the public custom theme API — document how to create custom themes

### Animation Timing Feel
- Default 12 FPS (configurable per theme)
- Walk mode: linear movement (position = progress × bar width), no easing
- Visual speed ceiling for rate-proportional effects: `visual_speed = min(rate / baseline, max_speed)` — prevents seizure-blur at high iteration rates, caps at "zoomies"
- Indeterminate mode (`total=None`):
  - **Wander mode**: sprite moves at speed proportional to current rate, wrapping at edges. Stall = stop, burst = sprint. Gives real rate information visually.
  - **Chase mode**: two sprites — cat chases mouse/yarn ball that moves randomly. Pure whimsy, zero information content.
  - Default: themes with Chase support default to Chase; otherwise fall back to Wander
- Physics-style bounce for cat_bounce theme: gravity drop, slow rise, slight squash at bottom
- Idle animation on stall: sprite switches to idle pose (cat sits, rocket idles) after several seconds of no updates. Signals "waiting" vs "broken"
- Sprite moves backward if progress goes backward (e.g., manual negative update). Could flip sprite direction.
- Completion frame at 100%: sprite transitions to 'done' pose at right edge
- Error during iteration: just clean up terminal, no error sprite
- Seamless resume after pause — no wake-up transition
- Multiple simultaneous bars: independent clocks, not synchronized

### Terminal Fallback Tiers
- Three color tiers: true color (24-bit) / 256 color / 16 color (basic ANSI). Themes adapt per tier.
- Non-TTY / piped output / TERM=dumb / width < 30 cols → plain built-in text bar (tqdm-style format: ` 45%|█████████████░░░░░░░░░░░| 45/100 [00:05<00:06, 8.2it/s]`)
- Environment variable support: `NYANBAR_THEME=nyan`, `NYANBAR_DISABLE=1` for CI/scripts
- Configuration via `nyanbar.config(animation='cat_walk', fps=12, fallback='text', color='auto', stats=True)` — full control
- Per-bar kwargs do NOT extend tqdm's API — all customization via `nyanbar.config()` or env vars
- Zero modification to `tqdm()` calls — users only change the import line and optionally add `nyanbar.config()` at top

### Drop-in Compatibility Contract
- nyanbar reimplements tqdm's user-facing API from scratch, zero dependencies
- Full API surface: `__iter__`, `__enter__`/`__exit__`, `update()`, `close()`, `set_description()`, `set_postfix()`, `set_postfix_str()`, `write()`
- All display kwargs: `desc=`, `unit=`, `unit_scale=`, `leave=`, `disable=`, `file=`, `ncols=`, `mininterval=`, `position=`
- `total=None` for indeterminate mode, `position=` for nested bars
- Unknown tqdm kwargs: silently accepted, never raises
- Fully independent from tqdm — both can be installed, zero conflict, no monkey-patching
- Removal story: swap import back to `from tqdm import tqdm`, remove `nyanbar.config()` lines, done. No leftover state, no generated files.

### Renderer Output Contract
- Stats placement: adaptive — right of animation for single-line themes, below for multi-line
- Stats format: match tqdm's exact format string
- Terminal resize: re-check width only if `dynamic_ncols=True` (match tqdm behavior)
- `write()` method: clear animation, print message, redraw animation below

### Claude's Discretion
- Exact ANSI escape sequence implementation details
- Internal renderer architecture (pure function vs class)
- `disp_len()` implementation for Unicode width measurement
- Performance optimization details (pre-computation, caching)
- Exact physics curve for cat_bounce
- Chase mode movement algorithm for the mouse/yarn ball

</decisions>

<specifics>
## Specific Ideas

- User's ideal usage pattern:
  ```python
  # set once in your project
  import nyanbar
  nyanbar.config(animation="cat")

  # every bar is cute, no extra kwargs
  from nyanbar import tqdm
  for x in tqdm(range(100)):
      ...
  ```
- "We want to only disrupt a few lines at the top of a file and nothing else, being very easy to remove"
- Wander mode gives visual rate information even without knowing total — stall = cat stops, burst = cat sprints
- Chase mode is "pure whimsy, zero information content, maximum delight"

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-foundation*
*Context gathered: 2026-02-25*
