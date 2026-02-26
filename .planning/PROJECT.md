# nyanbar

## What This Is

nyanbar is a standalone, zero-dependency Python progress bar library that renders cute animated ASCII/Unicode sprite animations in the terminal. It implements the same user-facing API as tqdm (same kwargs, same iteration pattern) so it's a drop-in replacement, but it does not import or depend on tqdm. Users write `from nyanbar import tqdm` and get animated progress bars (walking cats, nyan cat with rainbow trails, swimming fish, launching rockets).

## Core Value

tqdm-compatible API with zero dependencies — `from nyanbar import tqdm` must accept the same kwargs and iteration patterns as tqdm, but nyanbar is a fully standalone implementation with no external dependencies.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Standalone progress bar implementing tqdm-compatible API (no tqdm dependency)
- [ ] Animation engine with Frame/Animation dataclasses and wall-clock frame timing
- [ ] ANSI renderer for cursor movement, color, and multi-line in-place redraw
- [ ] Theme registry with lazy loading and 5+ built-in themes (cat_walk, cat_bounce, nyan, fish, rocket)
- [ ] Terminal detection utilities (width, color support, TTY, notebook)
- [ ] Graceful fallback to plain built-in text bar in non-TTY/dumb terminals and piped output
- [ ] Stats display (percentage, rate, ETA) alongside animations
- [ ] Multi-line rendering for complex themes (cat_bounce, nyan, fish, rocket)
- [ ] Single-line mode for simple themes (cat_walk)
- [ ] Completion frames for themes (cat sits down, rocket in space)
- [ ] Public API: `tqdm`, `trange`, `set_theme`, `Animation`, `Frame`, `list_themes`, `get_theme`
- [ ] Test suite covering core compatibility, renderer, themes, and fallback behavior
- [ ] Package configuration via pyproject.toml (Python 3.10+, MIT license)

### Out of Scope

- Jupyter/notebook HTML rendering with CSS animations — stretch goal, v1 falls back to plain text bar
- Mobile app or GUI version — terminal-only
- Any runtime dependencies — nyanbar is zero-dependency
- External asset files for themes — all frames defined inline in Python
- tqdm as a dependency — nyanbar reimplements the API surface, does not import tqdm

## Context

- Standalone implementation — reimplements tqdm's user-facing API without importing tqdm
- NyanBar class implements `__iter__`, `__enter__`/`__exit__`, `update()`, `close()`, `set_description()`, `set_postfix()`, etc.
- Frame selection uses `time.monotonic()` wall-clock, not iteration count, to decouple animation from iteration rate
- Uses `mininterval` to prevent animation rendering from bottlenecking the wrapped iterator
- Multi-line themes require cursor-up ANSI sequences and height tracking (`_prev_height`)
- Nested bars (position > 0) should disable multi-line and fall back to single-line
- Terminal width from `shutil.get_terminal_size().columns` with rightmost column reserved
- Stats string width calculated first, remaining space goes to animation
- Minimum 30 columns required for animation, otherwise fall back to plain built-in text bar
- Each theme module is self-contained with a `THEME` module-level `Animation` variable
- Additional creative themes beyond the core 5 are encouraged (moon phases, rubber duck, etc.)
- Fallback for rendering errors or non-TTY is a plain built-in text progress bar (not tqdm)

## Constraints

- **Python version**: 3.10+ (use `X | Y` union syntax, not `Union`)
- **Dependencies**: Zero runtime dependencies; `pytest>=7.0` for dev
- **Performance**: Animation rendering must never bottleneck the wrapped iterator
- **Compatibility**: Implements tqdm's user-facing API (same kwargs, same patterns) without depending on tqdm
- **License**: MIT

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Standalone reimplementation over tqdm subclass | Zero dependencies, full control, no version coupling | — Pending |
| Wall-clock frame timing over iteration-based | Consistent animation speed regardless of iteration rate | — Pending |
| Lazy theme loading | Unused themes don't slow down import | — Pending |
| ANSI escape codes over curses | Simpler, more portable, works in more terminals | — Pending |
| Inline frame definitions | No external assets to manage, themes are self-contained Python | — Pending |

---
*Last updated: 2026-02-25 after initialization*
