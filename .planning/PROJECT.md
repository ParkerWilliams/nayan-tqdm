# nyanbar

## What This Is

nyanbar is a drop-in replacement for Python's `tqdm` progress bar library that renders cute animated ASCII/Unicode sprite animations in the terminal. Users swap `from tqdm import tqdm` to `from nyanbar import tqdm` and get animated progress bars (walking cats, nyan cat with rainbow trails, swimming fish, launching rockets) while preserving full tqdm API compatibility.

## Core Value

Drop-in tqdm compatibility — `from nyanbar import tqdm` must work everywhere `from tqdm import tqdm` works, with zero behavior changes beyond the visual output.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Drop-in tqdm replacement via subclassing (`NyanBar(tqdm)`)
- [ ] Animation engine with Frame/Animation dataclasses and wall-clock frame timing
- [ ] ANSI renderer for cursor movement, color, and multi-line in-place redraw
- [ ] Theme registry with lazy loading and 5+ built-in themes (cat_walk, cat_bounce, nyan, fish, rocket)
- [ ] Terminal detection utilities (width, color support, TTY, notebook)
- [ ] Graceful fallback to standard tqdm in non-TTY/dumb terminals and piped output
- [ ] Stats display (percentage, rate, ETA) alongside animations
- [ ] Multi-line rendering for complex themes (cat_bounce, nyan, fish, rocket)
- [ ] Single-line mode for simple themes (cat_walk)
- [ ] Completion frames for themes (cat sits down, rocket in space)
- [ ] Public API: `tqdm`, `trange`, `set_theme`, `Animation`, `Frame`, `list_themes`, `get_theme`
- [ ] Test suite covering core compatibility, renderer, themes, and fallback behavior
- [ ] Package configuration via pyproject.toml (Python 3.10+, MIT license)

### Out of Scope

- Jupyter/notebook HTML rendering with CSS animations — stretch goal, v1 falls back to tqdm.notebook
- Mobile app or GUI version — terminal-only
- Runtime dependencies beyond tqdm — zero extra deps for base package
- External asset files for themes — all frames defined inline in Python

## Context

- Subclasses `tqdm.tqdm` directly, overriding `display()` method
- Frame selection uses `time.monotonic()` wall-clock, not iteration count, to decouple animation from iteration rate
- Uses `mininterval` to prevent animation rendering from bottlenecking the wrapped iterator
- Multi-line themes require cursor-up ANSI sequences and height tracking (`_prev_height`)
- Nested bars (position > 0) should disable multi-line and fall back to single-line
- Terminal width from `shutil.get_terminal_size().columns` with rightmost column reserved
- Stats string width calculated first, remaining space goes to animation
- Minimum 30 columns required for animation, otherwise fall back to plain tqdm
- Each theme module is self-contained with a `THEME` module-level `Animation` variable
- Additional creative themes beyond the core 5 are encouraged (moon phases, rubber duck, etc.)

## Constraints

- **Python version**: 3.10+ (use `X | Y` union syntax, not `Union`)
- **Dependencies**: Only `tqdm>=4.60` at runtime; `pytest>=7.0` and `rich` for dev
- **Performance**: Animation rendering must never bottleneck the wrapped iterator
- **Compatibility**: All tqdm kwargs must be preserved and functional
- **License**: MIT

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Subclass tqdm rather than wrap it | True drop-in compatibility, inherit all features | — Pending |
| Wall-clock frame timing over iteration-based | Consistent animation speed regardless of iteration rate | — Pending |
| Lazy theme loading | Unused themes don't slow down import | — Pending |
| ANSI escape codes over curses | Simpler, more portable, works in more terminals | — Pending |
| Inline frame definitions | No external assets to manage, themes are self-contained Python | — Pending |

---
*Last updated: 2026-02-25 after initialization*
