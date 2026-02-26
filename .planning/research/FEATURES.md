# Feature Research

**Domain:** Animated terminal progress bar library (Python)
**Researched:** 2026-02-25
**Confidence:** MEDIUM — Web access unavailable; findings based on training knowledge of tqdm, alive-progress, rich.progress, enlighten, progressbar2, halo, yaspin, and click. Core tqdm API is HIGH confidence (well-documented, stable API). Animation and differentiation claims are MEDIUM confidence (synthesized from ecosystem knowledge through ~mid-2025).

---

## Competitive Landscape Overview

| Library | Stars (approx) | Focus | Drop-in tqdm? |
|---------|----------------|-------|---------------|
| tqdm | ~29k | De-facto standard, minimal visuals | Self |
| alive-progress | ~5k | Animated bars, spinners, rich visuals | No |
| rich.progress | ~50k (rich) | Full-featured, opinionated styling | No |
| enlighten | ~1k | Multi-bar, persistent headers | No |
| progressbar2 | ~800 | Configurable widgets | No |
| halo | ~3k | Spinner-only (indeterminate) | No |
| yaspin | ~1k | Spinner-only (indeterminate) | No |
| tqdm (notebook) | bundled | Jupyter HTML widget | Partial |

**Key finding:** No library is simultaneously a tqdm drop-in AND provides character-sprite animation. nyanbar occupies a genuinely empty position: the only animated-theme library that works by `s/tqdm/nyanbar/` in the import line.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or broken.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Wrap any iterable | Core tqdm idiom — `for x in tqdm(iterable)` must work | LOW | Inherited free from `tqdm.tqdm` superclass |
| `trange(n)` shorthand | Used in virtually every tqdm codebase | LOW | One-liner wrapping `tqdm(range(n))` |
| `desc=` label | Users always name their bars | LOW | Inherited; must render in stats line |
| `total=` parameter | Required for percentage and ETA | LOW | Inherited; animation uses this for progress fraction |
| Percentage display | Universally expected in any progress UI | LOW | Must be visible alongside animation |
| Rate display (it/s) | Users care about throughput | LOW | Inherited stats rendering |
| ETA display | Users need to know "when will this finish?" | LOW | Inherited; must not be obscured by animation |
| Non-TTY graceful fallback | Scripts run in CI, cron, pipes — must not break | LOW | `isatty()` check, delegate to `super().display()` |
| CTRL+C safety | Interrupted bar must not corrupt terminal | MEDIUM | `try/finally` or context manager close; must call `self.close()` |
| Context manager (`with tqdm(...) as t`) | Idiomatic Python resource management | LOW | Inherited from tqdm |
| Manual `update(n)` | Used when you can't wrap an iterable | LOW | Inherited |
| `set_postfix()` / `set_description()` | Runtime mutation — very common | LOW | Inherited; must not crash animation |
| Nested bars (`position=`) | Multiple simultaneous bars | HIGH | tqdm handles positioning; multi-line themes must degrade to single-line when nested |
| Unicode/ASCII fallback | SSH sessions, Windows cmd.exe, TERM=dumb | MEDIUM | Detect `supports_unicode()`, swap sprite characters |
| Terminal width adaptation | Bars must fit; don't overflow lines | MEDIUM | `shutil.get_terminal_size()`, minimum-width fallback |
| Thread safety | Data pipelines run bars from multiple threads | MEDIUM | tqdm's lock mechanism should be inherited; verify display() override is safe |

### Differentiators (Competitive Advantage)

Features that set nyanbar apart. Not expected from a tqdm replacement, but create delight and adoption.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Character sprite animation (sprites move with progress) | Core differentiator — nobody else does this as tqdm drop-in | HIGH | Walk-mode: sprite x-position = `progress * bar_width`; needs wall-clock frame cycling decoupled from iteration rate |
| Wall-clock frame timing (FPS-based) | Animation looks smooth regardless of iteration speed (fast or slow loops) | MEDIUM | `int(elapsed * fps) % len(frames)` — must not bottleneck iterator |
| Theme system with registry | Users can install additional themes; extensible | MEDIUM | Lazy loading per theme module; `THEME` module-level variable pattern |
| Completion frames ("done" animations) | Reward signal — cat sits, rocket disappears, fish swim away | MEDIUM | Triggered in `close()`; makes the bar feel alive end-to-end |
| Multi-line animation modes | Enables visually rich themes (nyan rainbow, rocket trajectory) | HIGH | Requires cursor-up ANSI sequences, `_prev_height` tracking; must not conflict with tqdm's own cursor management |
| ANSI color in animations (rainbow trail, fire) | Visual richness; no other tqdm-compatible bar does this | MEDIUM | Color support detection; graceful ASCII-color fallback |
| Animation mode variety (walk, cycle, fill) | Enables diverse theme types without per-theme rendering logic | MEDIUM | `mode` field on `Animation`; render() method dispatches by mode |
| Named theme selection (`set_theme()`, `theme=` kwarg) | Users pick personality, not just colors | LOW | String name → lazy import; global default + per-instance override |
| `trange()` with animation | Animated range shorthand — very common usage pattern | LOW | Simple: `NyanBar(range(n), **kwargs)` |
| User-defined custom themes | Power users contribute themes; community extensions | MEDIUM | Public `Animation` + `Frame` dataclasses; documented protocol |
| `list_themes()` API | Discoverability — users explore without reading docs | LOW | Returns `list[str]` from registry |
| Minimum-width enforcement (< 30 cols fallback) | Prevents visual corruption on narrow terminals | LOW | Width check in `display()`, delegate to super if too narrow |
| ASCII sprite fallback (unicode detection) | Works on Windows cmd, basic SSH | MEDIUM | Each theme needs ASCII variant frames; detection via `supports_unicode()` |
| Per-theme `fps` setting | Fast themes (spinner) vs slow themes (cat walk) feel right | LOW | `fps: float` on `Animation` dataclass |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems — explicitly out of scope.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Jupyter HTML/CSS animation rendering | Notebooks are popular; native HTML looks great | Complex secondary rendering path; tqdm.notebook already handles notebooks; v1 scope creep — HTML canvas/CSS animation is a separate engineering problem | Fallback to `tqdm.notebook` in notebook environment; v2 stretch goal |
| Rich library integration (panels, tables, layout) | Rich has beautiful output | Rich changes the output model entirely (console object, Live context); fundamentally incompatible with tqdm's stderr line model; creates a hard dependency | Themes can use ANSI color codes directly; Rich is optional dev dep only |
| GUI progress window (tkinter/Qt) | Some users want desktop popups | Far outside terminal library scope; adds heavy dependencies; breaks headless environments | Terminal-only; document this explicitly |
| Sound/audio feedback | Fun for some users | Platform-dependent, hard to make optional, annoying in shared environments | No audio; animation is the engagement layer |
| Progress persistence (save/resume) | Long jobs that restart | Requires external state storage; complex; not tqdm's model | Let callers manage state; tqdm doesn't do this either |
| Async/await native progress | asyncio is popular | tqdm has `tqdm.asyncio`; wrapping it is complex and not in drop-in scope | Inherit `tqdm.asyncio` behavior; don't implement independently |
| Real-time downloads with transfer speed widget | Popular feature request | Already in tqdm as `unit_scale=True, unit='B'`; just inherit it | Use tqdm kwargs passthrough — it already works |
| Per-iteration callback hooks | "Call my function every N iterations" | Breaks tqdm's iterator protocol; users use `update()` and postfix already | Document `set_postfix()` and `update()` patterns instead |
| Plugin marketplace / PyPI theme discovery | npm-style ecosystem | Over-engineering for v1; requires protocol standards, versioning, metadata | Define theme authoring protocol; let community publish themes naturally |
| Configfile-based default theme | `~/.nyanbarrc` or similar | Adds complexity, OS-specific paths, validation; not standard for Python libs | `set_theme()` call at top of script is sufficient; document the pattern |

---

## Feature Dependencies

```
[tqdm drop-in compatibility (subclass)]
    └──required by──> [All features] (everything inherits from this)

[Terminal detection (TTY, width, unicode, color)]
    └──required by──> [Non-TTY fallback]
    └──required by──> [Unicode/ASCII sprite switching]
    └──required by──> [ANSI color in animations]
    └──required by──> [Minimum-width enforcement]
    └──required by──> [Multi-line rendering]

[Frame/Animation dataclasses]
    └──required by──> [Theme system / registry]
    └──required by──> [Wall-clock frame timing]
    └──required by──> [Animation mode dispatch (walk/cycle/fill)]

[Theme system / registry]
    └──required by──> [Named theme selection (set_theme, theme= kwarg)]
    └──required by──> [list_themes() API]
    └──required by──> [User-defined custom themes]
    └──required by──> [All built-in themes (cat_walk, nyan, fish, rocket)]

[ANSIRenderer (cursor movement, color, multi-line redraw)]
    └──required by──> [Multi-line animation modes]
    └──required by──> [ANSI color in animations]
    └──required by──> [Completion frames]

[Single-line animation (cat_walk)]
    └──enables──> [Multi-line animation (cat_bounce, nyan, fish, rocket)]
    (Single-line is simpler; validate the display() override works here first)

[Multi-line rendering]
    └──conflicts──> [Nested bars (position > 0)]
    (Resolution: disable multi-line when position > 0, fall back to single-line)

[Unicode detection]
    └──enhances──> [All sprite themes]
    (Themes provide ASCII fallback frames; detection selects which set to use)

[Completion frames]
    └──requires──> [close() override]
    └──requires──> [Theme defines completion_frame field]
```

### Dependency Notes

- **All features require tqdm subclass:** The subclass approach is load-bearing. If dropped (e.g., switched to a wrapper), the entire drop-in compatibility story breaks and half the features become manual reimplementations.
- **Multi-line conflicts with nested bars:** tqdm uses `position=` to stack multiple bars by printing to specific terminal lines. Multi-line animation breaks this model. Detection and fallback must happen in `display()`.
- **Terminal detection gates multiple features:** It's a shared utility that must be implemented early (Phase 1). Getting it wrong causes cascading failures (broken output in CI, incorrect fallbacks).
- **Theme system enables extensibility:** It's a medium-complexity feature but it unlocks user-defined themes, `set_theme()`, and `list_themes()`. Implement before the 5 built-in themes.
- **Wall-clock timing is independent of iteration rate:** This is the key insight that makes animation smooth — do not couple frame index to `self.n` (iteration count), or fast loops will spin through all frames instantly and slow loops will freeze.

---

## MVP Definition

### Launch With (v1)

Minimum viable product to validate that animated tqdm replacement is a real thing people want.

- [ ] **Drop-in tqdm subclass** — `from nyanbar import tqdm` works everywhere `from tqdm import tqdm` works; this is the entire value proposition
- [ ] **Non-TTY / dumb terminal fallback** — must not break CI pipelines; this is the #1 trust issue for any tqdm replacement
- [ ] **`cat_walk` theme (single-line)** — simplest animation; validates the display() override approach before building complex multi-line themes
- [ ] **Wall-clock frame timing** — without this, animation either freezes (slow loops) or blurs (fast loops); non-negotiable for animation quality
- [ ] **Terminal width adaptation + minimum-width fallback** — prevents line-wrapping and visual corruption
- [ ] **Stats display (%, rate, ETA)** — users rely on these; animation must not hide them
- [ ] **Unicode/ASCII sprite fallback** — SSH sessions and Windows cmd must not get garbled characters
- [ ] **`trange()` shorthand** — used in too many codebases to omit
- [ ] **Thread safety** — data pipelines need this; inheriting tqdm's locks should be sufficient, but must verify display() override doesn't break it
- [ ] **One multi-line theme (`nyan`)** — validates the multi-line rendering stack; reveals `_prev_height` bugs before adding more themes
- [ ] **Test suite** — compatibility tests, renderer tests, fallback tests; without this, each new theme risks breaking the API

### Add After Validation (v1.x)

Features to add once core is proven working.

- [ ] **Remaining built-in themes (cat_bounce, fish, rocket)** — trigger: positive reception to cat_walk and nyan; each new theme is a marketing moment
- [ ] **Completion frames** — trigger: user feedback that bars feel "abrupt" when they stop
- [ ] **ANSI color in animations (nyan rainbow, rocket fire)** — trigger: confirmed the ASCII fallback path works correctly
- [ ] **`set_theme()` global default** — trigger: users asking "how do I make cat my default permanently?"
- [ ] **User-defined custom theme documentation** — trigger: anyone asks "can I make my own theme?"
- [ ] **Additional creative themes (moon, duck, etc.)** — trigger: community enthusiasm; low-cost wins

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **Jupyter HTML/CSS animation rendering** — defer: separate rendering model, high complexity; fallback to `tqdm.notebook` is acceptable for v1
- [ ] **Plugin/theme discovery protocol** — defer: only matters if there are third-party theme authors, which requires community first
- [ ] **`asyncio` integration beyond inheritance** — defer: `tqdm.asyncio` handles this; only needed if users report gaps

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Drop-in tqdm subclass | HIGH | LOW | P1 |
| Non-TTY fallback | HIGH | LOW | P1 |
| cat_walk (single-line animation) | HIGH | MEDIUM | P1 |
| Wall-clock frame timing | HIGH | LOW | P1 |
| Stats display (%, rate, ETA) | HIGH | LOW | P1 |
| Terminal width adaptation | HIGH | LOW | P1 |
| Unicode/ASCII fallback | HIGH | MEDIUM | P1 |
| trange() | HIGH | LOW | P1 |
| Thread safety | HIGH | LOW | P1 |
| nyan theme (multi-line, color) | HIGH | HIGH | P1 |
| Test suite | HIGH | MEDIUM | P1 |
| cat_bounce theme | MEDIUM | MEDIUM | P2 |
| fish theme | MEDIUM | MEDIUM | P2 |
| rocket theme | MEDIUM | HIGH | P2 |
| Completion frames | MEDIUM | MEDIUM | P2 |
| set_theme() global | MEDIUM | LOW | P2 |
| list_themes() API | LOW | LOW | P2 |
| User-defined custom themes | MEDIUM | LOW | P2 |
| Moon phases theme | LOW | LOW | P3 |
| Rubber duck theme | LOW | LOW | P3 |
| Jupyter HTML rendering | LOW | HIGH | P3 |
| asyncio native support | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | tqdm | alive-progress | rich.progress | nyanbar (planned) |
|---------|------|----------------|---------------|-------------------|
| Drop-in `from x import tqdm` | Self | No | No | Yes (core value) |
| Character sprite animation | No | Partial (spinners, bar styles) | No | Yes (walking sprites) |
| Wall-clock frame timing | No | Yes | Yes | Yes |
| Multi-line animation | No | No | Yes (panels) | Yes (select themes) |
| ANSI color in bar | No | Yes | Yes | Yes (select themes) |
| Completion animation | No | Yes | No | Yes (per theme) |
| Theme/style registry | No | Yes (styles) | Yes (columns) | Yes (Animation registry) |
| Non-TTY fallback | Yes | Yes | Yes | Yes (delegate to tqdm) |
| Nested bars | Yes | Partial | Yes | Partial (single-line only when nested) |
| Jupyter support | Yes (tqdm.notebook) | No | Yes | Fallback to tqdm.notebook |
| Zero extra deps | Yes | No (requires alive-progress) | No (requires rich) | Yes (only tqdm) |
| Custom bar format | Yes (`bar_format=`) | No | Yes (columns) | Via custom Animation |
| Spinner (indeterminate) | No | Yes | Yes | Could be a theme (cycle mode) |

**Key competitive insight:** alive-progress has the best animation and visual richness but requires users to rewrite their tqdm code. rich.progress is the most powerful but is a complete UI framework, not a drop-in. nyanbar's angle is "you don't change anything except the import, and it becomes fun." That's a unique position no competitor occupies.

---

## Sources

- tqdm documentation and source: training knowledge (HIGH confidence for stable API, verified against PROJECT.md which uses tqdm internals correctly)
- alive-progress: training knowledge through mid-2025 (MEDIUM confidence)
- rich.progress: training knowledge through mid-2025 (MEDIUM confidence)
- enlighten, progressbar2, halo, yaspin: training knowledge (MEDIUM confidence for feature presence, LOW confidence for current version specifics)
- Project context: `/Users/prwilliams/Repos/nayan-tqdm/.planning/PROJECT.md` and `/Users/prwilliams/Repos/nayan-tqdm/nayan-tqdm.md` (HIGH confidence — primary source)

**Note:** Web access was unavailable during this research session. Competitor download statistics, GitHub stars, and version-specific feature additions after mid-2025 are unverified. The feature categorization (table stakes vs. differentiators) is based on what users experience across these libraries and is unlikely to have changed materially. The tqdm API (inherited features) should be verified against the installed tqdm version (`tqdm>=4.60`) before implementation.

---
*Feature research for: Animated terminal progress bar library (Python — nyanbar)*
*Researched: 2026-02-25*
