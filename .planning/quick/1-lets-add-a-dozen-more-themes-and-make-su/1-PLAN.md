---
phase: quick
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - nyanbar/themes/_mario.py
  - nyanbar/themes/_pac_man.py
  - nyanbar/themes/_snake.py
  - nyanbar/themes/_rocket.py
  - nyanbar/themes/_fire.py
  - nyanbar/themes/_ocean.py
  - nyanbar/themes/_matrix.py
  - nyanbar/themes/_heartbeat.py
  - nyanbar/themes/_disco.py
  - nyanbar/themes/_zen.py
  - nyanbar/themes/_construction.py
  - nyanbar/themes/_wizard.py
  - nyanbar/themes/__init__.py
  - tests/test_themes.py
  - demo.py
autonomous: true
requirements: []

must_haves:
  truths:
    - "12 new themes are registered and usable via theme= parameter"
    - "All 18 themes render correctly at all 3 tiers (emoji, unicode, ascii)"
    - "All 18 themes pass the existing parametrized test suite"
    - "demo.py shows every registered theme"
  artifacts:
    - path: "nyanbar/themes/_mario.py"
      provides: "mario theme"
    - path: "nyanbar/themes/_pac_man.py"
      provides: "pac_man theme"
    - path: "nyanbar/themes/_snake.py"
      provides: "snake theme"
    - path: "nyanbar/themes/_rocket.py"
      provides: "rocket theme"
    - path: "nyanbar/themes/_fire.py"
      provides: "fire theme"
    - path: "nyanbar/themes/_ocean.py"
      provides: "ocean theme"
    - path: "nyanbar/themes/_matrix.py"
      provides: "matrix theme"
    - path: "nyanbar/themes/_heartbeat.py"
      provides: "heartbeat theme"
    - path: "nyanbar/themes/_disco.py"
      provides: "disco theme"
    - path: "nyanbar/themes/_zen.py"
      provides: "zen theme"
    - path: "nyanbar/themes/_construction.py"
      provides: "construction theme"
    - path: "nyanbar/themes/_wizard.py"
      provides: "wizard theme"
    - path: "nyanbar/themes/__init__.py"
      provides: "registration of all 18 themes"
    - path: "tests/test_themes.py"
      provides: "ALL_THEMES list covering all 18 themes"
    - path: "demo.py"
      provides: "demo covering all 18 themes"
  key_links:
    - from: "nyanbar/themes/__init__.py"
      to: "each new _*.py theme module"
      via: "from . import _name"
      pattern: "from \\. import"
    - from: "tests/test_themes.py"
      to: "nyanbar/registry"
      via: "ALL_THEMES parametrize list"
      pattern: "ALL_THEMES"
---

<objective>
Add 12 new themes to nyanbar and update the demo to showcase all of them.

Purpose: Expand theme variety from 6 to 18. Make the library more fun and appealing with diverse visual styles.
Output: 12 new theme modules, updated registry imports, updated tests, updated demo.
</objective>

<execution_context>
@/Users/prwilliams/.claude/get-shit-done/workflows/execute-plan.md
@/Users/prwilliams/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@nyanbar/themes/_nyan.py (reference theme with rainbow fill + decoration)
@nyanbar/themes/_deal_with_it.py (simple theme pattern)
@nyanbar/themes/_shrug.py (simple theme pattern)
@nyanbar/themes/__init__.py (registration imports)
@nyanbar/models.py (Animation, AnimationMode, Frame)
@nyanbar/registry.py (register_theme API)
@tests/test_themes.py (parametrized theme tests)
@demo.py (current demo)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create 12 new theme modules</name>
  <files>
    nyanbar/themes/_mario.py
    nyanbar/themes/_pac_man.py
    nyanbar/themes/_snake.py
    nyanbar/themes/_rocket.py
    nyanbar/themes/_fire.py
    nyanbar/themes/_ocean.py
    nyanbar/themes/_matrix.py
    nyanbar/themes/_heartbeat.py
    nyanbar/themes/_disco.py
    nyanbar/themes/_zen.py
    nyanbar/themes/_construction.py
    nyanbar/themes/_wizard.py
    nyanbar/themes/__init__.py
  </files>
  <action>
Create 12 new theme files following the exact pattern from existing themes. Each file MUST:
- Import `from __future__ import annotations`
- Import `Animation, AnimationMode, Frame` from `..models` and `register_theme` from `..registry`
- Set `__all__: list[str] = []`
- Define `_create(tier: str) -> Animation` dispatching to `_emoji()`, `_unicode()`, `_ascii()`
- Each tier function returns an `Animation` with: `name` matching the registered name, `frames` tuple of at least 2 `Frame` objects (all same display_width, all single-line/height=1), `fps` (2.0-4.0), `mode=AnimationMode.WALK`, `completion_frame` (non-None), `bar_fill` (non-None tuple of strings)
- Call `register_theme("name", _create)` at module level
- Include docstring with rendering tiers

CRITICAL constraints (from test suite):
- All frames in `frames` tuple MUST have identical `display_width` (test_theme_frame_widths_consistent)
- All frames MUST be height=1 / single-line (test_theme_single_line_sprites)
- `bar_fill` MUST be non-None (test_all_themes_use_bar_fill)
- `completion_frame` MUST be non-None (test_theme_has_completion_frame)
- At least 2 frames (test_theme_has_frames checks frame_count >= 2)
- fps > 0 (test_theme_fps_positive)
- The completion frame sprite text must appear in the rendered bar output at 100% (test_themed_bar_completion_renders checks `comp.lines[0] in full_output`)

Theme specifications (name -> emoji sprite / fill / completion concept):

1. **mario** -- Super Mario mushroom running. emoji: mushroom emoji, fill: brick-colored blocks, completion: star emoji. ascii: ">o>" / "#" / "*o*"

2. **pac_man** -- Pac-Man eating dots. emoji: pac-man open/closed mouth alternating, fill: dots (middle dot char), completion: ghost emoji. ascii: "C" / "." / "O"

3. **snake** -- Snake slithering. emoji: snake emoji head, fill: green-colored blocks, completion: snake + apple. ascii: "~>" / "=" / "~>@"

4. **rocket** -- Rocket with flame trail. emoji: rocket emoji, fill: flame-colored gradient (red/orange/yellow ANSI), completion: rocket + star. ascii: "=>" / "~" / "=>*"

5. **fire** -- Fire spreading. emoji: fire emoji, fill: red/orange ANSI-colored blocks, completion: fire + sparkles. ascii: "^" / "#" / "^*^"

6. **ocean** -- Wave surfing. emoji: wave/surfer emoji, fill: blue-colored gradient blocks (ANSI blue/cyan), completion: sun emoji. ascii: "~^~" / "~" / "\\o/"

7. **matrix** -- Digital rain. emoji: binary digits as fill (0/1), fill: green ANSI "0"/"1", completion: green "DONE". ascii: ">" / "01" / ">>>"

8. **heartbeat** -- Heart pulse. emoji: heart emoji alternating sizes, fill: pink ANSI blocks, completion: sparkling heart. ascii: "<3" / "~" / "<3!"

9. **disco** -- Disco ball. emoji: mirror ball / sparkle alternating, fill: cycling ANSI colors (red/yellow/green/cyan/blue/magenta), completion: disco ball + music note. ascii: "*" / "=" / "*!*"

10. **zen** -- Calm meditation. emoji: lotus emoji, fill: light shade blocks, completion: lotus + sparkle. ascii: "@" / "." / "@*"

11. **construction** -- Under construction. emoji: construction/hard hat, fill: yellow/black hazard pattern (ANSI yellow block / ANSI black block alternating), completion: check mark emoji. ascii: "!" / "#-" / "[OK]"

12. **wizard** -- Magic wizard. emoji: wizard/wand emoji, fill: purple ANSI sparkle pattern, completion: wizard + star. ascii: "*>" / "~" / "*>*"

For ANSI-colored fills (rocket, fire, ocean, matrix, heartbeat, disco, construction, wizard), use the same ANSI escape pattern as nyan theme: `f"\033[{code}m\u2588\033[0m"` for colored blocks, or `f"\033[{code}m{char}\033[0m"` for colored characters. Color codes: 31=red, 32=green, 33=yellow, 34=blue, 35=magenta, 36=cyan.

For emoji tier: use actual Unicode emoji where possible (e.g., mushroom U+1F344, rocket U+1F680, fire U+1F525, wave U+1F30A, heart U+2764, lotus U+1FAB7 or use a simpler flower). For unicode tier: use the same Unicode/ANSI as emoji but with text kaomoji instead of emoji. For ascii tier: use only printable ASCII characters and no ANSI codes.

After creating all 12 files, update `nyanbar/themes/__init__.py` to import all 12 new modules (add `from . import _name  # noqa: F401` for each).

Run `.venv/bin/python -c "from nyanbar.registry import list_themes; print(list_themes())"` to verify all 18 themes register.
  </action>
  <verify>`.venv/bin/python -c "from nyanbar.registry import list_themes; t = list_themes(); print(t); assert len(t) == 18"` prints 18 themes and does not error.</verify>
  <done>12 new theme modules exist, all register correctly, `list_themes()` returns 18 entries.</done>
</task>

<task type="auto">
  <name>Task 2: Update tests and demo to cover all 18 themes</name>
  <files>
    tests/test_themes.py
    demo.py
  </files>
  <action>
Update `tests/test_themes.py`:
- Change the `ALL_THEMES` list at the top to include all 18 theme names in sorted order:
  ```python
  ALL_THEMES = [
      "construction", "deal_with_it", "disco", "finger_guns", "fire",
      "heartbeat", "lenny", "mario", "matrix", "nyan", "ocean",
      "pac_man", "rocket", "shrug", "snake", "table_flip", "wizard", "zen",
  ]
  ```
- Add theme-specific completion tests for each new theme (following the pattern of existing tests like `test_table_flip_completion_has_table`). Each test should verify the completion_frame contains a distinguishing character. For example:
  - `test_mario_completion_has_star`: check for star character
  - `test_pac_man_completion_has_ghost_or_indicator`: check for distinguishing char
  - `test_snake_completion_has_apple_or_indicator`: check for distinguishing char
  - `test_rocket_completion_has_star`: check for star
  - `test_fire_completion_has_sparkle`: check for distinguishing char
  - `test_ocean_completion`: check for distinguishing char
  - `test_matrix_completion`: check for "DONE" or distinguishing char
  - `test_heartbeat_completion`: check for "!" or distinguishing char
  - `test_disco_completion`: check for note or distinguishing char
  - `test_zen_completion`: check for sparkle or distinguishing char
  - `test_construction_completion`: check for check mark or distinguishing char
  - `test_wizard_completion`: check for star or distinguishing char

The exact character checked must match what you actually put in the theme's completion_frame. Write the test AFTER the theme so you know the exact content.

Update `demo.py`:
- Change the `THEMES` list to use `list_themes()` from the registry so it always covers every registered theme automatically:
  ```python
  from nyanbar.registry import list_themes
  THEMES = list_themes()
  ```
- Keep the same loop structure but reduce `DELAY` to `0.02` and `N` to `80` so the full demo doesn't take forever with 18 themes.

Run the full test suite: `.venv/bin/python -m pytest tests/test_themes.py -v`
  </action>
  <verify>`.venv/bin/python -m pytest tests/test_themes.py -v` -- all tests pass, including the parametrized tests for all 18 themes across 3 tiers and 5 progress levels.</verify>
  <done>ALL_THEMES contains 18 entries, all parametrized tests pass (18 themes x 3 tiers x 5 levels = 270 render tests plus per-theme completion tests), demo.py dynamically lists all themes.</done>
</task>

</tasks>

<verification>
1. `.venv/bin/python -c "from nyanbar.registry import list_themes; t = list_themes(); print(len(t), t); assert len(t) == 18"` -- 18 themes registered
2. `.venv/bin/python -m pytest tests/test_themes.py -v` -- all tests pass
3. `.venv/bin/python -m pytest tests/ -v` -- full test suite passes (no regressions)
4. `.venv/bin/python -m mypy nyanbar/themes/ --strict` -- type checking passes
5. `.venv/bin/python demo.py` -- visual confirmation all 18 themes render (optional human check)
</verification>

<success_criteria>
- 18 total themes registered (6 existing + 12 new)
- All parametrized tests pass across all themes, tiers, and progress levels
- mypy --strict passes on all theme modules
- demo.py covers every registered theme
- No regressions in existing test suite
</success_criteria>

<output>
After completion, create `.planning/quick/1-lets-add-a-dozen-more-themes-and-make-su/1-SUMMARY.md`
</output>
