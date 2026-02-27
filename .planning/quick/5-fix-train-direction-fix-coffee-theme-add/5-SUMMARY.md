---
phase: quick-5
plan: 01
subsystem: themes
tags: [themes, kaomoji, fix, decoration, train, coffee, cat]
dependency_graph:
  requires: []
  provides: [train-text-art-sprite, coffee-real-emoji, cat_smug-theme, cat_sleepy-theme, cat_play-theme]
  affects: [nyanbar/themes, tests/test_themes.py, tests/test_tqdm_compat.py]
tech_stack:
  added: []
  patterns: [3-tier-theme, kaomoji-sprite, ANSI-color, decoration-frame]
key_files:
  modified:
    - nyanbar/themes/_train.py
    - nyanbar/themes/_coffee.py
    - nyanbar/themes/__init__.py
    - tests/test_themes.py
    - tests/test_tqdm_compat.py
  created:
    - nyanbar/themes/_cat_smug.py
    - nyanbar/themes/_cat_sleepy.py
    - nyanbar/themes/_cat_play.py
decisions:
  - "Train emoji tier uses ANSI yellow [==>] text-art (5 cols) since all train emoji face left in Unicode"
  - "Coffee emoji tier uses real U+2615 (2 cols) with steam/bean fill -- prior text-art was workaround, now corrected"
  - "cat_smug/cat_sleepy use 7-col kaomoji; cat_play uses 8-col batting sprites for energetic visual"
  - "cat_play completion frame (7 cols) differs from sprite frame (8 cols) -- engine handles independently at 100%"
metrics:
  duration: ~8 min
  completed: 2026-02-26
  tasks_completed: 2
  files_modified: 5
  files_created: 3
---

# Quick Task 5 Summary: Fix Train Direction, Fix Coffee Theme, Add 3 Cat Kaomoji Themes

**One-liner:** ANSI yellow `[==>]` text-art replaces left-facing train emoji; real U+2615 coffee emoji with steam/bean decoration; three kaomoji cat themes (cat_smug 2fps, cat_sleepy 1.5fps, cat_play 5fps) bring total to 29 themes.

## What Was Built

### Task 1: Fix train and coffee themes

**Train (`_train.py`):**
- Replaced left-facing U+1F682 locomotive emoji with ANSI yellow `[==>]` text-art sprite (5 display cols)
- Both sprite frames identical (`[==>]`) -- animation comes from alternating track decoration
- Completion: `[==>]★` (6 cols)
- Unicode and ASCII tiers unchanged (`[TTT]`/`[===]`) -- already correct

**Coffee (`_coffee.py`):**
- Emoji tier now uses real `☕` (U+2615, 2 display cols) as sprite instead of text-art `c[_]`
- Fill replaced: brown blocks → steam/bean alternating 1-col chars (white bullets, brown diamonds, middle dots)
- Added steam-above/bean-below decoration to all 3 tiers (emoji, unicode, ascii)
- Unicode tier uses ANSI-colored `c[_]` (4 cols) with same steam/bean fill and decoration
- ASCII tier uses plain `c[_]` with `~` and `.` steam wisps fill and plain decoration

**Tests:** Added `test_coffee_has_decoration` (parametrized across tiers), `test_coffee_emoji_sprite_is_real_emoji`, added `"coffee"` to `DECORATED_THEMES`.

### Task 2: Add cat_smug, cat_sleepy, cat_play kaomoji themes

**cat_smug (`_cat_smug.py`):**
- Sprite: `(=^.^=)` / `(=^w^=)` alternating (7 cols each), magenta ANSI color
- Completion: `(=^♥^=)` using U+2665 heart suit (7 cols, red ANSI)
- Fill: magenta/yellow/cyan bullet and middle-dot mix (4 chars, all 1 col)
- Decoration: `><>` fish and `·` dots above, `. ~ .` purr wisps below
- fps: 2.0 (slow smug stroll)

**cat_sleepy (`_cat_sleepy.py`):**
- Sprite: `(-._.-)`  / `(u._.u)` alternating (7 cols each), blue ANSI color
- Completion: `(-.♥.-)` using U+2665 heart suit (7 cols, red ANSI)
- Fill: blue/magenta/cyan pastel bullets and dots (4 chars, all 1 col)
- Decoration: `z` and `.` floating above (sleep), `. ~ .` dreamy clouds below
- fps: 1.5 (very slow, drowsy pace)

**cat_play (`_cat_play.py`):**
- Sprite: `(=^.^=)~` / `~(=^.^=)` alternating (8 cols each), green ANSI color
- Completion: `(=^♥^=)` using U+2665 heart suit (7 cols, green ANSI)
- Fill: red/green/yellow bullets and diamonds (6 chars, all 1 col)
- Decoration: `o` and `*` bouncing toys above, `~` and `.` scuff marks below
- fps: 5.0 (fast, energetic!)

**Registration:** All 3 added to `__init__.py` in alphabetical position (cat_play, cat_sleepy, cat_smug between cat_mouse and cat_yarn).

**Tests:** Added all 3 to `ALL_THEMES` and `DECORATED_THEMES`. Added `test_cat_smug/sleepy/play_completion_has_heart` tests. Updated `test_list_themes_returns_all_twenty_nine` in `test_tqdm_compat.py` (auto-fixed: test was checking for 26 themes by name, needed to reflect new 29 total).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated test_tqdm_compat.py theme count test**
- **Found during:** Task 2 full suite run
- **Issue:** `test_list_themes_returns_all_twenty_six` checked for exact list of 26 theme names; adding 3 themes caused assertion failure
- **Fix:** Renamed test to `test_list_themes_returns_all_twenty_nine` and updated expected theme list to include cat_play, cat_sleepy, cat_smug
- **Files modified:** tests/test_tqdm_compat.py
- **Commit:** 7a32057

## Verification Results

All success criteria confirmed:

- Train emoji tier: ANSI yellow `[==>]` text-art (5 cols), no U+1F682 emoji codepoint
- Coffee emoji tier: real U+2615 coffee emoji, steam/bean fill (all 1 col), decoration present (3-line output)
- Frame width consistency verified for all new themes:
  - cat_smug: 7/7/7 cols across emoji/unicode/ascii
  - cat_sleepy: 7/7/7 cols across emoji/unicode/ascii
  - cat_play: 8/8/8 cols across emoji/unicode/ascii
- All bar_fill chars 1 display col
- 29 themes total in registry
- 1659 tests pass (up from 1322)
- mypy --strict: no issues in 40 source files

## Commits

| Hash | Message |
|------|---------|
| 1d5f4ce | fix(quick-5): train text-art sprite + coffee real emoji with decoration |
| 7a32057 | feat(quick-5): add cat_smug, cat_sleepy, cat_play kaomoji themes (29 total) |

## Self-Check: PASSED
