---
phase: quick-4
plan: 01
subsystem: themes
tags: [themes, chase, animation, decoration]
dependency_graph:
  requires: []
  provides: [cat_yarn-theme, cat_mouse-theme, duck_bread-theme]
  affects: [theme-registry, test-suite]
tech_stack:
  added: []
  patterns: [compound-chase-sprite, two-frame-animation, 3-tier-theme]
key_files:
  created:
    - nyanbar/themes/_cat_yarn.py
    - nyanbar/themes/_cat_mouse.py
    - nyanbar/themes/_duck_bread.py
  modified:
    - nyanbar/themes/__init__.py
    - tests/test_themes.py
    - tests/test_tqdm_compat.py
decisions:
  - "Chase mechanic uses compound sprite: Frame A = chaser+space+target, Frame B = chaser+target+space, both equal display_width"
  - "duck_bread completion uses star (U+2605) not bread emoji for clean completion marker matching test assertion"
metrics:
  duration: ~10 min
  completed: 2026-02-26
  tasks_completed: 2
  files_created: 3
  files_modified: 3
---

# Quick Task 4: Add cat_yarn, cat_mouse, duck_bread Chase Themes

**One-liner:** Three chase-motif themes where a compound chaser+target sprite animates across ANSI-colored fills, with 2-line decoration above and below the bar.

## What Was Built

Added 3 new chase-themed progress bar animations to expand the theme library with a "pursuit" motif. Each theme features a compound sprite that alternates between two frames to simulate chasing behavior.

### Chase Mechanic

The chase effect is implemented via a two-frame sprite where:
- Frame A: `chaser + space + target` (gap shows active pursuit)
- Frame B: `chaser + target + space` (no gap shows momentary catch, trailing space preserves display_width)

Both frames must have identical `display_width` — verified by Frame's `__post_init__` which calls `disp_len()`.

### Themes Created

**cat_yarn** (`_cat_yarn.py`):
- Emoji: Cat U+1F431 chases yarn U+1F9F6, magenta/yellow/red bullet+diamond fill, heart-eyes completion U+1F63B
- Unicode: `>^.^ o` / `>^.^o ` sprites (6 cols), colored fill, dot/tilde decoration
- ASCII: Same text sprites, tilde/dash fill, dot/tilde decoration

**cat_mouse** (`_cat_mouse.py`):
- Emoji: Cat U+1F431 chases mouse U+1F42D, yellow/white/grey paw-print fill, smirking cat completion U+1F63C
- Unicode: `>^.^ @` / `>^.^@ ` sprites (6 cols), colored fill, dot/comma decoration
- ASCII: Same text sprites, dot/comma fill, dot/comma decoration

**duck_bread** (`_duck_bread.py`):
- Emoji: Duck U+1F986 chases bread U+1F35E, cyan/yellow/blue water fill, star completion U+2605
- Unicode: `=< o` / `=<o ` sprites (4 cols), colored fill, tilde/dot decoration
- ASCII: Same text sprites, tilde/dot fill, tilde/dot decoration

### Registry and Tests

- `nyanbar/themes/__init__.py`: Added 3 new imports in alphabetical position
- `tests/test_themes.py`: ALL_THEMES updated to 26, DECORATED_THEMES includes all 3 chase themes, new parametrized `test_chase_themes_have_decoration` test, 3 completion-specific tests added
- `tests/test_tqdm_compat.py`: Updated `test_list_themes_returns_all_twenty_six` (was `twenty_three`)

## Verification

All constraints verified:
- Every `bar_fill` char: exactly 1 display col (ANSI codes are 0 cols, unicode bullets/tildes/diamonds are 1 col)
- All frames within a tier: identical `display_width`
- Decoration frames: exactly 2 lines each
- `list_themes()` returns exactly 26 themes
- Full test suite: 1508 tests pass

## Commits

| Task | Description | Commit | Files |
|------|-------------|--------|-------|
| 1 | Create 3 chase theme files | 4afb0f8 | `_cat_yarn.py`, `_cat_mouse.py`, `_duck_bread.py` |
| 2 | Register themes and update tests | 6bea5de | `__init__.py`, `test_themes.py`, `test_tqdm_compat.py` |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated test_tqdm_compat.py theme count test**
- **Found during:** Task 2 verification (full test suite run)
- **Issue:** `test_list_themes_returns_all_twenty_three` had hardcoded list of 23 themes that didn't include the 3 new chase themes
- **Fix:** Renamed to `test_list_themes_returns_all_twenty_six` and updated the expected list to 26 themes
- **Files modified:** `tests/test_tqdm_compat.py`
- **Commit:** 6bea5de

## Self-Check: PASSED

- FOUND: nyanbar/themes/_cat_yarn.py
- FOUND: nyanbar/themes/_cat_mouse.py
- FOUND: nyanbar/themes/_duck_bread.py
- FOUND: commit 4afb0f8 (task 1)
- FOUND: commit 6bea5de (task 2)
