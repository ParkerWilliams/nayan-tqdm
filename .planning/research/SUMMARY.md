# Project Research Summary

**Project:** nyanbar — animated terminal progress bar library (tqdm subclass)
**Domain:** Python terminal library / animated CLI tooling
**Researched:** 2026-02-25
**Confidence:** HIGH

## Executive Summary

nyanbar is a Python library that subclasses `tqdm.tqdm` to produce character-sprite animated progress bars while remaining a drop-in replacement: users change only their import line. Research confirms this is a genuinely unoccupied competitive position — alive-progress has better animation but requires rewriting tqdm code; rich.progress is a full UI framework; no existing library offers both sprite animation AND `from nyanbar import tqdm` compatibility. The recommended approach is a clean 6-module src-layout package (`core.py`, `animation.py`, `renderer.py`, `terminal.py`, `themes/`) managed with hatch, using only `tqdm>=4.60` as a runtime dependency. All animation, timing, and ANSI rendering is implemented with stdlib only.

The architecture is well-defined and dependency-ordered. The single extension point is `display()`, which tqdm's own documentation identifies as the intended override point for subclasses. Animation frames advance on wall-clock time (`time.monotonic()`), not iteration count — this is the key design decision that makes animation smooth at both fast and slow iteration rates. The build order flows from pure/testable primitives outward to the tqdm integration boundary, which is the right approach for validating each layer independently before tackling cursor-movement complexity.

The dominant risks are all terminal rendering problems: corrupted multi-line cursor state, ANSI color sequences left open after close, and the `display(msg='')` erase contract being ignored. These are not speculative — they are derived from reading tqdm's source directly and are each diagnosable with targeted tests. Addressing them in the correct phase (before building multi-line themes) eliminates the recovery cost, which PITFALLS.md rates as HIGH if discovered after all themes are built. Performance is a secondary risk: string construction and terminal-size syscalls in the hot render path must be pre-computed at init time.

---

## Key Findings

### Recommended Stack

The stack is minimal by design: `tqdm>=4.60` is the only runtime dependency, and all other capabilities come from Python stdlib. hatch manages the project lifecycle (environments, testing, building, publishing) via `pyproject.toml`. The dev toolchain is ruff (lint + format), mypy with `--strict`, pytest with pytest-mock and pytest-cov, and pre-commit. Python 3.10+ is required and correct — it's the oldest version still receiving security updates, and 3.10 syntax (`X | Y` union types, `match` statements) is used throughout.

See `.planning/research/STACK.md` for full version table and `pyproject.toml` template.

**Core technologies:**
- Python 3.10+: runtime — `X | Y` syntax, `match`, dataclasses; 3.10 is minimum viable security baseline
- tqdm >=4.60: base class — `display()` is the documented subclass override point; `format_dict` exposes all stats
- stdlib `time.monotonic()`: frame timing — immune to clock adjustments; decouples animation speed from iteration rate
- stdlib `shutil.get_terminal_size()`: width detection — cross-platform, no external dep
- stdlib `dataclasses` (`@dataclass(frozen=True)`): `Frame` and `Animation` value objects — zero deps, idiomatic
- hatch + hatchling: project management — replaces pip/venv/build/twine; PyPA-recommended for new libraries
- ruff: lint and format — replaces flake8+isort+black; single tool, 10-100x faster
- mypy `--strict`: type checking — essential for a library's public API surface

**What not to use:** curses (Windows-incompatible, overkill), threading.Timer (race conditions with tqdm's lock), asyncio animation loops (adds complexity tqdm doesn't need), setup.py (legacy), external asset files (breaks packaging).

### Expected Features

The competitive insight from FEATURES.md is direct: nyanbar occupies the only empty position in the Python progress bar landscape — the intersection of "animated character sprites" and "tqdm drop-in compatibility." No other library holds both.

See `.planning/research/FEATURES.md` for full feature matrix and competitor table.

**Must have (table stakes):**
- Drop-in tqdm subclass (`from nyanbar import tqdm` works everywhere) — the entire value proposition
- Non-TTY / dumb terminal fallback — #1 trust issue; must not break CI pipelines
- `trange(n)` shorthand — used in virtually every tqdm codebase
- Wall-clock frame timing — without this, animation freezes on slow loops and strobes on fast ones
- Stats display (%, rate, ETA) — users rely on these; animation must not hide them
- Terminal width adaptation + minimum-width fallback (< 30 cols) — prevents line overflow and visual corruption
- Unicode/ASCII sprite fallback — SSH and Windows cmd must not get garbled characters
- Thread safety — inherited from tqdm locks; must verify `display()` override does not break it
- Test suite — compatibility, renderer, and fallback tests before any theme expansion

**Should have (competitive differentiators):**
- Character sprite animation with walk mode — nobody else does this as a tqdm drop-in
- `cat_walk` theme (single-line) — validates the display() override before multi-line complexity
- `nyan` theme (multi-line, rainbow) — validates multi-line rendering stack
- Completion frames — reward signal when progress hits 100%
- Named theme selection (`theme=` kwarg, `set_theme()`)
- Remaining built-in themes: `cat_bounce`, `fish`, `rocket`
- `list_themes()` API — discoverability without reading docs
- User-defined custom theme documentation

**Defer (v2+):**
- Jupyter HTML/CSS animation rendering — separate rendering model, high complexity
- Plugin/theme discovery protocol — only matters after community exists
- asyncio native support beyond tqdm.asyncio inheritance
- Windows colorama integration — macOS/Linux are v1 primary targets

### Architecture Approach

The architecture is a clean 6-module layered design where each layer has zero knowledge of the layers above it. `NyanBar` subclasses `tqdm` and overrides only `display()`. It delegates to `animation.current_frame()` for timing, `themes.get_theme()` for lazy-loaded theme data, `terminal.*` for environment detection, and `renderer.render()` for ANSI string construction. The renderer is a pure function that accepts only primitives and returns a string — it knows nothing about tqdm, NyanBar, or themes. This makes it trivially testable without a real terminal.

See `.planning/research/ARCHITECTURE.md` for full component diagram, data flow, and build order.

**Major components:**
1. `NyanBar` (`core.py`) — tqdm subclass; overrides `display()`; holds `_frame_t0`, `_prev_height`, `_theme_name`
2. `Animation` / `Frame` (`animation.py`) — frozen dataclasses; `current_frame(animation, elapsed)` pure function
3. ANSI Renderer (`renderer.py`) — pure `render(frame, stats, width, prev_height) -> str`; cursor-up erase for multi-line
4. Terminal Detection (`terminal.py`) — pure functions: `is_tty()`, `terminal_width()`, `color_support()`, `is_notebook()`
5. Theme Registry (`themes/__init__.py`) — lazy registry: `{name: module_path_str | Animation}`, loads on first access
6. Theme Modules (`themes/<name>.py`) — self-contained `THEME = Animation(...)` with inline frame definitions

**Key architectural rules:**
- Never track `_prev_height` in two places — single source of truth in renderer return value
- Renderer receives only primitives; returns only a string; no side effects
- Theme modules are loaded lazily — importing `nyanbar` does not pay the cost of all themes
- `set_theme()` sets a per-instance default captured at `__init__`; not a process-global at render time

### Critical Pitfalls

See `.planning/research/PITFALLS.md` for full detail, phase mapping, and recovery costs.

1. **`display(msg='', pos=pos)` contract ignored** — tqdm calls `display()` with `msg=''` to erase bars (`leave=False`). If NyanBar always renders animation, `leave=False` bars leave residual lines and exception handling corrupts the terminal. Prevention: explicit `msg is None` / `msg == ''` / `msg is not None` dispatch at the top of `display()`. Verify in `test_compat.py` with `leave=True`, `leave=False`, and exception-during-iteration cases. Recovery cost if skipped: LOW, but must be fixed before any public release.

2. **Multi-line height mismatch corrupts terminal state** — `_prev_height` must be authoritative and single-sourced. If height diverges by even 1 line (first render, theme switch, terminal resize, fallback activation), every subsequent render prints to the wrong row and the output drifts permanently. Prevention: initialize `_prev_height = 0` at `__init__`; derive actual height from renderer return value, not from a separate count; reset to 0 on any fallback activation. Address in `renderer.py` phase, before writing multi-line themes. Recovery cost if skipped: MEDIUM.

3. **Nested bar cursor conflict** — tqdm's `moveto()` assumes single-line bars. NyanBar's multi-line cursor-up sequences conflict with tqdm's own cursor movement when `self.pos > 0`. Result: bars overwrite each other. Prevention: check `abs(self.pos) > 0` in `display()` and disable multi-line mode for nested bars. Address in `core.py` phase; test with two simultaneous NyanBar instances before building any multi-line theme. Recovery cost if skipped: HIGH.

4. **ANSI color sequences left open** — `\r\033[K` (clear line) erases visible characters but does not reset SGR color attributes. If any colored render path fails to emit `\033[0m` before the line terminator, the shell prompt inherits the animation color. Prevention: always end colored lines with `\033[0m`; use `tqdm.utils.disp_trim()` when truncating colored strings; add a regex test that asserts no open ANSI sequences remain after `render_frame()`. Address in `renderer.py` phase, before color themes. Recovery cost if skipped: LOW (easy fix, embarrassing bug).

5. **Unicode width miscalculation** — `len(line)` returns code points; terminal emulators measure East Asian Width (emoji and CJK = 2 columns). Mixing these breaks column arithmetic and causes wide-character sprites to overflow the terminal, corrupting multi-line height tracking. Prevention: use `tqdm.utils.disp_len()` everywhere width is measured; set `Frame.width` using `disp_len()` not `len()`. Address in `animation.py` / `themes/base.py` from day one — retrofitting this is MEDIUM cost and requires re-verifying every theme. Recovery cost if skipped: MEDIUM.

6. **Rendering performance bottleneck** — string construction per `display()` call at fast iteration rates (>10k/s, rendered 10x/sec by tqdm's default `mininterval`) adds measurable latency. Prevention: pre-compute position-indexed frame strings at init time; cache `shutil.get_terminal_size()` except when `dynamic_ncols=True`; use `''.join([...])` not `+=`. Establish a <0.5ms per-render budget with the first theme (`cat_walk`). Recovery cost if discovered late: MEDIUM.

---

## Implications for Roadmap

Based on research, the architecture's build order and pitfall-to-phase mapping both point to the same phase structure. Build from pure/testable primitives outward to the tqdm integration boundary, then expand animation complexity one layer at a time.

### Phase 1: Foundation — Pure Primitives and Project Scaffold

**Rationale:** `animation.py`, `terminal.py`, and `renderer.py` have no tqdm dependency and can be unit-tested without a real terminal. Building and testing them first establishes confidence in the core data model before touching tqdm internals. This also resolves the Unicode width pitfall (Pitfall 5) and ANSI color pitfall (Pitfall 4) at the lowest-cost moment.

**Delivers:** Working `Frame`/`Animation` dataclasses, `current_frame()` pure function, terminal detection utilities, pure ANSI renderer with correct multi-line erase math, full test coverage for each.

**Addresses:** Drop-in subclass prerequisites, terminal width adaptation, Unicode/ASCII fallback detection logic, ANSI color correctness.

**Avoids:** Pitfall 4 (ANSI color open), Pitfall 5 (Unicode width miscalculation) — both must be addressed in this phase.

**Stack:** Python 3.10, stdlib only, pytest + pytest-mock, ruff, mypy `--strict`, hatch project scaffold.

**Research flag:** Standard patterns — no additional research needed. Architecture doc provides exact code examples.

### Phase 2: Core tqdm Integration (Single-Line, cat_walk Theme)

**Rationale:** `core.py` is the most integration-sensitive component — it touches tqdm internals and must get the `display()` contract right. Starting with single-line-only mode (cat_walk theme) constrains the cursor-movement surface area to just `\r`, eliminating multi-line complexity while validating the full animation pipeline end-to-end.

**Delivers:** `NyanBar` class, `trange()` shorthand, `cat_walk` theme, non-TTY fallback, `leave=True`/`leave=False` correct behavior, thread safety verification, first real animated progress bar.

**Addresses:** Drop-in compatibility, non-TTY fallback, stats display (%, rate, ETA), trange() shorthand, thread safety, minimum-width fallback.

**Avoids:** Pitfall 1 (`display(msg='')` contract) — must be validated here with `leave=True`, `leave=False`, and exception-during-iteration tests. Pitfall 3 (nested bar cursor conflict) — add `abs(self.pos) > 0` guard and test with two simultaneous bars.

**Stack:** tqdm 4.67.x, `time.monotonic()`, `shutil.get_terminal_size()`, `os.isatty()`.

**Research flag:** Standard patterns — tqdm source read directly; override contract is documented. No additional research needed.

### Phase 3: Theme Registry and Multi-Line Rendering

**Rationale:** Multi-line animation (nyan, fish, rocket) is the hardest rendering problem — cursor-up erase, `_prev_height` tracking, and conflict with tqdm's `moveto()` all converge here. Building the lazy registry first separates theme infrastructure from rendering complexity. The nyan theme validates multi-line rendering before committing to additional multi-line themes.

**Delivers:** Lazy theme registry (`get_theme()`, `set_theme()`, `list_themes()`), multi-line ANSI erase logic in renderer, `nyan` theme (multi-line, rainbow trail), `_prev_height` tracking with single-source-of-truth pattern, user-facing theme selection via `theme=` kwarg.

**Addresses:** Theme system with registry, named theme selection, multi-line animation mode, ANSI color in animations, nyan as the flagship differentiator theme.

**Avoids:** Pitfall 2 (multi-line height mismatch) — renderer must return actual height; NyanBar must reset on fallback; first-render path uses `\n` downward not cursor-up. Pitfall 3 (nested bar, reinforced) — `abs(self.pos) > 0` forces single-line fallback for multi-line themes.

**Stack:** `importlib.import_module()` for lazy registry, `tqdm.utils.disp_len()` and `disp_trim()` for width and color safety.

**Research flag:** May need shallow research during planning on `_prev_height` first-render edge cases if any ambiguity surfaces. The PITFALLS.md doc is thorough but the first-render vs. subsequent-render split is subtle.

### Phase 4: Remaining Themes and Completion Frames

**Rationale:** Once multi-line rendering is proven with nyan, the remaining themes (cat_bounce, fish, rocket) are straightforward `Animation` data definitions. Completion frames are a per-theme addition (cat sits down, rocket reaches space). This phase is primarily content creation — the infrastructure is already built.

**Delivers:** `cat_bounce`, `fish`, `rocket` themes, completion frame support in `close()`, `list_themes()` finalized, user-defined custom theme documentation.

**Addresses:** Remaining built-in themes (P2 from FEATURES.md), completion frames (reward signal at 100%), extensibility documentation for community themes.

**Avoids:** Pitfall 6 (rendering performance) — establish <0.5ms render budget per theme; pre-compute position-indexed frame tables for walk-mode themes.

**Stack:** No new dependencies. `tqdm.utils.disp_len()` for all frame width validation in tests.

**Research flag:** Standard patterns — no research needed. Each theme is a self-contained `THEME = Animation(...)` data definition.

### Phase 5: Public API Finalization and Release

**Rationale:** The public API surface (`nyanbar/__init__.py` re-exports, pyproject.toml metadata, README, PyPI publish) is the final integration step. This phase wires everything together under a single import namespace and runs the full "looks done but isn't" checklist from PITFALLS.md before publishing.

**Delivers:** `from nyanbar import tqdm, trange, Animation, Frame, set_theme, list_themes` all work from one import. pyproject.toml finalized, README with usage examples, PyPI publication via `hatch publish`, CI pipeline (GitHub Actions, `hatch run test-cov`).

**Addresses:** All P1 and P2 features complete. "Looks done but isn't" checklist: `leave=False` clean terminal, exception-in-loop clean terminal, nested bars, piped output (no ANSI leakage), no-total mode, terminal resize mid-run, completion frame trigger, ANSI color reset verified.

**Avoids:** All residual pitfalls from checklist — this phase is the final validation gate.

**Stack:** hatch build + hatch publish, GitHub Actions CI, `FORCE_COLOR=1` in CI to test ANSI paths.

**Research flag:** Standard patterns. PyPI publishing with hatch is well-documented.

### Phase Ordering Rationale

- **Primitives before integration (Phases 1-2):** `animation.py` and `renderer.py` have no tqdm dependency. Testing them first means the tqdm override boundary is the only unknown when Phase 2 begins.
- **Single-line before multi-line (Phase 2 before Phase 3):** The `display()` contract (`msg=None` vs `msg=''`) and the nested-bar guard must be proven correct on the simpler single-line case before adding cursor-up complexity.
- **One multi-line theme before five (Phase 3 uses nyan):** nyan exercises the full multi-line stack (cursor-up erase, color, `_prev_height`, rainbow trail). Proving it works before building cat_bounce/fish/rocket means the registry and renderer are stable for the remaining themes.
- **Content before release (Phase 4 before 5):** All themes and completion frames ship before the public API is finalized, so the v1 release is complete rather than a preview.
- **This order directly avoids the highest-cost pitfalls:** Multi-line/nested conflict (HIGH recovery cost) is addressed in Phase 2 before multi-line themes exist. Unicode width and color bugs (MEDIUM cost) are addressed in Phase 1 before any frame data is written.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** The `_prev_height` first-render edge case (must emit `\n * (height-1)` downward on first render, not cursor-up) is subtle. If planning reveals ambiguity about how tqdm's own `moveto()` handles position=0 on first render, a targeted `/gsd:research-phase` on that specific interaction is warranted.

Phases with standard patterns (can skip research-phase):
- **Phase 1:** Pure stdlib code with no external integration; well-documented patterns.
- **Phase 2:** tqdm override contract is documented in tqdm's own source and confirmed by ARCHITECTURE.md.
- **Phase 4:** Theme content creation; no new infrastructure.
- **Phase 5:** hatch publish and GitHub Actions are well-documented.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | tqdm source read directly; all version numbers confirmed via `pip index versions` on 2026-02-25; stdlib APIs confirmed available since Python 3.3/3.7; PyPA hatch recommendation is MEDIUM (could not verify current PyPA page, but hatch is de facto standard) |
| Features | MEDIUM | tqdm API is HIGH confidence (stable, well-documented). Competitor feature claims (alive-progress, rich.progress stars, feature presence) are MEDIUM — derived from training knowledge through mid-2025, web access unavailable. Core feature categorization (table stakes vs. differentiators) is unlikely to have changed materially. |
| Architecture | HIGH | tqdm source read directly; `display()` override is the documented extension point; all component boundaries and data flows derived from reading `std.py` lines 1265-1524 and `utils.py`. Pattern examples in ARCHITECTURE.md are verified against actual tqdm internals. |
| Pitfalls | HIGH | All 6 critical pitfalls derived from reading tqdm source code directly (`std.py` and `utils.py`); specific line numbers cited. Not training-data speculation — each pitfall traces to a specific tqdm behavior: `close()` erase contract, `moveto()` single-line assumption, `disp_len()` in `utils.py`, `_lock` usage. |

**Overall confidence:** HIGH

### Gaps to Address

- **Competitor star counts and recent features:** Web access was unavailable. alive-progress, rich.progress, and enlighten feature sets are accurate as of mid-2025 but could have added tqdm-compatible interfaces since then. Validation: a quick manual check before launch to confirm nyanbar's positioning claim ("only animated tqdm drop-in") still holds.
- **Windows support scope:** Colorama integration for Windows cmd.exe ANSI is deferred to v2. If early users are primarily on Windows, this prioritization should be revisited after initial feedback.
- **`tqdm.asyncio` inheritance behavior:** Not validated against tqdm source. If users report gaps with async code, this needs investigation. Acceptable to defer; standard tqdm behavior should be inherited.
- **pyproject.toml `hatchling` version pin:** The `pyproject.toml` template in STACK.md uses `hatchling==1.29.0` in `[build-system].requires`. This should be validated as the current stable version before release (or use `>=1.29` to avoid unnecessary pin tightness).

---

## Sources

### Primary (HIGH confidence)
- tqdm 4.67.x source code (`std.py`, `utils.py`) — read directly from installed package; `display()` contract, `close()` behavior, `moveto()`, `disp_len()`, `_lock`
- `/Users/prwilliams/Repos/nayan-tqdm/nayan-tqdm.md` — project constraints (ANSI vs. curses, inline frames, zero runtime deps, wall-clock timing)
- Python stdlib documentation — `shutil.get_terminal_size()`, `time.monotonic()`, `dataclasses` — confirmed Python 3.10+ availability
- PyPI version data (`pip index versions`, 2026-02-25) — all pinned versions confirmed current

### Secondary (MEDIUM confidence)
- Training knowledge (through mid-2025): alive-progress, rich.progress, enlighten, progressbar2, halo, yaspin — feature presence and competitive positioning
- Python Packaging Authority hatch recommendation — de facto standard; specific PyPA page not directly verified

### Tertiary (LOW confidence)
- Competitor GitHub star counts — approximations from training data; not verified against live GitHub

---
*Research completed: 2026-02-25*
*Ready for roadmap: yes*
