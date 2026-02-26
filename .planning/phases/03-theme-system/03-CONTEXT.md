# Phase 3: Theme System - Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Theme registry with lazy loading, 5 built-in animated themes (cat_walk, cat_bounce, nyan, fish, rocket), multi-line rendering support, and completion frames. Users select themes by name via `set_theme()` or `theme=` kwarg and see correct animations from 0% through 100%.

</domain>

<decisions>
## Implementation Decisions

### Theme Visual Design
- Each theme must have 3 rendering tiers: emoji (best), unicode (middle), ASCII (fallback)
- Auto-detect terminal capability and select the highest supported tier
- Classic Nyan Cat style for the nyan theme — rainbow trail, pop-tart body, starfield background, faithful to the original meme
- Each theme integrates the progress bar differently (mixed approach): e.g., cat walks across, rocket launches vertically above bar — whatever fits the theme
- Animation speed is fixed FPS, independent of progress rate — smooth and consistent

### Completion Frames
- Completion frames are optional per theme — only added where they make sense for the art
- If a theme defines a completion frame, it displays at 100%; otherwise the animation just stops on the last frame
- Stats line (percentage, rate, time) persists after completion — no summary replacement
- When leave=True, the completion frame (if defined) stays on screen

### Color Degradation
- The 3-tier rendering system (emoji/unicode/ASCII) handles degradation naturally
- Terminal capability auto-detection by default (TERM, COLORTERM, locale sniffing)
- User override available via `render_level='ascii'|'unicode'|'emoji'` kwarg to force a specific tier
- ASCII-tier theme art is still attempted on dumb terminals (TERM=dumb) — not collapsed to plain text fallback
- Nyan cat rainbow trail uses patterned stripes (different ASCII characters per stripe: =, ~, -, .) when color is unavailable, keeping the layered visual

### Registry Behavior
- Default theme is `nyan` (the namesake of the library)
- Invalid theme names fall back to the default theme with a warning (not an exception)
- `register_theme(name, animation)` API available for users to add custom themes
- `set_theme()` affects only future bars — currently running bars keep their assigned theme
- `list_themes()` returns all registered theme names (built-in + custom)
- `get_theme(name)` returns the Animation object for a given theme name

### Claude's Discretion
- Exact ASCII/unicode/emoji art for each theme character
- Animation frame count and FPS per theme
- Multi-line layout dimensions per theme
- Auto-detection logic details (which env vars, what thresholds)
- Whether piped output uses ASCII-tier or plain fallback (safe choice)

</decisions>

<specifics>
## Specific Ideas

- Nyan cat should be faithful to the original meme — rainbow trail, pop-tart body cat, starfield
- Rainbow trail without color should use distinct patterns per stripe (=, ~, -, .) so it's still visually layered
- The 3-tier system is the core degradation strategy — emoji > unicode > ASCII, detected automatically with user override

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-theme-system*
*Context gathered: 2026-02-25*
