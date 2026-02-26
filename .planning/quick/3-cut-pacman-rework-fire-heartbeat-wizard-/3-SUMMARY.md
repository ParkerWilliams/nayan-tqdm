---
phase: quick-3
plan: 01
subsystem: themes
tags: [themes, decoration, animation, unicode]
key-files:
  created:
    - nyanbar/themes/_train.py
    - nyanbar/themes/_garden.py
    - nyanbar/themes/_lightning.py
    - nyanbar/themes/_candy.py
    - nyanbar/themes/_aurora.py
    - nyanbar/themes/_coffee.py
  modified:
    - nyanbar/themes/_fire.py
    - nyanbar/themes/_heartbeat.py
    - nyanbar/themes/_wizard.py
    - nyanbar/themes/_rocket.py
    - nyanbar/themes/__init__.py
    - tests/test_themes.py
    - tests/test_tqdm_compat.py
    - demo.py
  deleted:
    - nyanbar/themes/_pac_man.py
decisions:
  - "U+26A1 (lightning bolt) is 2 display cols -- use U+2607 (lightning symbol) for emoji sprite"
  - "U+2615 (coffee cup emoji) is 2 display cols -- use text-art c[_] sprite for all tiers"
  - "U+2764 (heavy heart) is 1 col but U+1F496 (sparkling heart emoji) is 2 -- completion uses heart + sparkles"
  - "heartbeat sprite uses U+2665 (heart suit, 1 col) with ANSI colors to maintain consistent 1-col width across frames"
metrics:
  duration: ~15 min
  completed: "2026-02-26"
  tasks: 3
  files: 14
---

# Quick Task 3: Cut pac_man, Rework 4 Themes, Add 6 New Themes Summary

**One-liner:** Deleted pac_man, added nyan-quality decoration to fire/heartbeat/wizard/rocket, and created 6 new themes (train, garden, lightning, candy, aurora, coffee) bringing the total to 23 themes across 3 render tiers.

## What Was Built

### Theme Changes

**Deleted:**
- `_pac_man.py` -- removed from file system and `__init__.py` imports

**Reworked with decoration (2 alternating frames above+below bar):**
- `_fire.py`: 6-char flickering flame fill (red/yellow ANSI blocks + shades) + smoke/flame particle decoration
- `_heartbeat.py`: Heart-unicode fill (U+2665/U+2661 in magenta/red ANSI) + heartbeat pulse line + scattered hearts decoration
- `_wizard.py`: Expanded to 10 magical symbols (star, asterisk, diamond, hollow-star, snowflake, comet, star-of-david, therefore, house, 4-point-star) + twinkling sparkle decoration
- `_rocket.py`: Dynamic exhaust fill (full blocks + shade chars) + starfield/parallax decoration

**New themes (6):**
- `_train.py`: Railroad track fill + steam/track decoration (WITH decoration)
- `_garden.py`: Floral symbol fill + petal/grass decoration (WITH decoration)
- `_lightning.py`: Electric crackle fill + spark decoration (WITH decoration, uses U+2607 not U+26A1)
- `_candy.py`: Candy-colored shapes fill, no decoration (simple sweet theme)
- `_aurora.py`: 8-char aurora color wave fill + shimmer decoration (WITH decoration)
- `_coffee.py`: Brown espresso blocks fill, text-art c[_] sprite, no decoration

### Test Coverage Added

- Updated ALL_THEMES to 23 entries, removed pac_man, added 6 new themes
- Deleted `test_pac_man_completion_has_ghost`
- Added 6 new theme completion tests
- Added parametrized decoration tests for 4 reworked themes (fire/heartbeat/wizard/rocket x 3 tiers = 12 tests)
- Added parametrized decoration tests for 4 new decorated themes (train/garden/lightning/aurora x 3 tiers = 12 tests)
- Added `test_decorated_themes_render_3_lines` for all 9 decorated themes x 3 tiers = 27 tests
- Fixed stale `test_list_themes_returns_all_eighteen` -> `test_list_themes_returns_all_twenty_three`

### Demo Updated

Removed the indeterminate section (lines 17-32). Demo now iterates all themes dynamically via `list_themes()` with no hardcoded theme list.

## Verification Results

- `test ! -f nyanbar/themes/_pac_man.py`: PASS
- `pytest tests/ -x -q`: 1355 passed, 0 failed
- `mypy nyanbar/ --strict`: Success: no issues found in 34 source files
- `len(list_themes()) == 23`: PASS
- All 23 themes render across all 3 tiers without errors
- All bar_fill chars verified 1 display col via disp_len()
- All decoration frames have exactly 2 lines (above/below bar)
- All sprite frames within themes have consistent display_width

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Stale theme-count test in test_tqdm_compat.py**
- **Found during:** Task 3 (pytest run)
- **Issue:** `test_list_themes_returns_all_eighteen` still expected 18 themes with pac_man
- **Fix:** Renamed to `test_list_themes_returns_all_twenty_three`, updated expected list to 23 themes
- **Files modified:** `tests/test_tqdm_compat.py`
- **Commit:** 2029726

## Commits

| Hash | Message |
|------|---------|
| 4ac7499 | feat(quick-3): cut pac_man, rework fire/heartbeat/wizard/rocket with decoration |
| 8c528fb | feat(quick-3): create 6 new themes (train, garden, lightning, candy, aurora, coffee) |
| 2029726 | feat(quick-3): update tests and demo for 23 themes, remove pac_man |

## Self-Check: PASSED

All 6 new theme files present. _pac_man.py deleted. All 3 task commits verified (4ac7499, 8c528fb, 2029726). 1355 tests pass. mypy --strict clean.
