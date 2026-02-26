---
phase: quick-2
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - nyanbar/themes/_construction.py
  - nyanbar/themes/_pac_man.py
  - nyanbar/themes/_wizard.py
  - nyanbar/themes/_disco.py
  - demo.py
  - tests/test_themes.py
autonomous: true
requirements: []

must_haves:
  truths:
    - "construction theme tells a visual story (bulldozer pushing earth, not generic hazard stripes)"
    - "pac_man theme uses wedge-shaped text characters, not yellow/orange circle emoji"
    - "wizard trail is made of colorful magical symbols, not purple ANSI gradient blocks"
    - "disco fill is visually distinct from nyan rainbow (different characters, not same 6-color blocks)"
    - "demo.py shows total=None (indeterminate) usage alongside existing theme demos"
  artifacts:
    - path: "nyanbar/themes/_construction.py"
      provides: "Reworked construction theme with earth-moving narrative"
      contains: "register_theme"
    - path: "nyanbar/themes/_pac_man.py"
      provides: "Reworked pac_man theme with text-art wedge sprite"
      contains: "register_theme"
    - path: "nyanbar/themes/_wizard.py"
      provides: "Reworked wizard theme with magical symbol trail"
      contains: "register_theme"
    - path: "nyanbar/themes/_disco.py"
      provides: "Reworked disco theme distinct from nyan"
      contains: "register_theme"
    - path: "demo.py"
      provides: "Demo with indeterminate mode examples"
      contains: "total=None"
  key_links:
    - from: "nyanbar/themes/_construction.py"
      to: "nyanbar/registry.py"
      via: "register_theme call"
      pattern: "register_theme"
    - from: "tests/test_themes.py"
      to: "nyanbar/themes/*.py"
      via: "parametrized theme tests"
      pattern: "ALL_THEMES"
---

<objective>
Rework four themes (construction, pac_man, wizard, disco) to fix user feedback issues,
and add indeterminate mode (total=None) examples to demo.py.

Purpose: The current construction/pac_man/wizard/disco themes are either generic, visually
wrong, or carbon copies of nyan. Each needs a distinct visual identity that tells a story.
The demo should also showcase total=None (indeterminate) usage.

Output: Four reworked theme files, updated tests, and enhanced demo.py
</objective>

<execution_context>
@/Users/prwilliams/.claude/get-shit-done/workflows/execute-plan.md
@/Users/prwilliams/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@nyanbar/themes/_nyan.py (reference: rainbow fill pattern to NOT duplicate in disco)
@nyanbar/themes/_construction.py (rework target)
@nyanbar/themes/_pac_man.py (rework target)
@nyanbar/themes/_wizard.py (rework target)
@nyanbar/themes/_disco.py (rework target)
@nyanbar/models.py (Animation, AnimationMode, Frame)
@nyanbar/engine.py (build_themed_fill: bar_fill chars assumed 1 display col each)
@nyanbar/utils.py (disp_len for display width measurement)
@tests/test_themes.py (existing theme tests - update completion assertions)
@demo.py (add indeterminate examples)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Rework all four themes</name>
  <files>
    nyanbar/themes/_construction.py
    nyanbar/themes/_pac_man.py
    nyanbar/themes/_wizard.py
    nyanbar/themes/_disco.py
  </files>
  <action>
Rework each theme file following these specifications. All bar_fill characters MUST be
1 display column each (verified via disp_len). All frames must be single-line. Each theme
needs 2+ animation frames, a completion_frame, and bar_fill. Keep the existing 3-tier
structure (emoji/unicode/ascii) and register_theme pattern.

**construction -- "Bulldozer building a road"**
Story: A bulldozer pushes along, leaving a paved road behind it.
- emoji tier:
  - bar_fill: Alternating brown/yellow ANSI-colored block characters to look like
    laid bricks/pavement. Use `\u2588` (full block) with colors: `\033[33m` (yellow/brown)
    and `\033[90m` (dark gray) alternating -- gives a "paved road" look.
    Tuple: `(f"{YEL}\u2588{RST}", f"{GRAY}\u2588{RST}", f"{YEL}\u2588{RST}", f"{GRAY}\u2588{RST}")`
  - sprite frames: Two frames alternating between construction vehicles:
    Frame 1: `\U0001f6a7` (construction sign, 2 cols)
    Frame 2: `\U0001f6a7` (same, for consistent width)
    Actually -- use the tractor `\U0001f69c` (tractor emoji). Verify its disp_len is 2.
    If tractor doesn't render well, fall back to `\U0001f6a7`. Both frames same emoji
    for consistent width.
    NO WAIT -- the user said the current construction sign "doesn't convey anything."
    Use `\U0001f3d7` (building construction emoji, the crane) as sprite. Check disp_len.
    If it's 2 cols, use it. Both frames: same emoji for consistent display_width.
  - completion_frame: `\U0001f3e0` (house emoji -- "building complete!")
  - No decoration.
- unicode tier:
  - bar_fill: Same ANSI-colored blocks as emoji tier
  - sprite frames: `[=]` and `[-]` (bulldozer-ish)
  - completion_frame: `[OK]`
- ascii tier:
  - bar_fill: `("=", "-")` alternating
  - sprite frames: `[=]` and `[-]`
  - completion_frame: `[OK]`
- fps: 3.0, mode: WALK

**pac_man -- "Pac-Man eating dots with text-art wedge"**
User feedback: yellow/orange circles are "just a dot, not pac man." Use text-art approach.
- emoji tier:
  - bar_fill: `("\u00b7",)` (middle dot -- the pellets) -- 1 display col, confirmed
  - sprite frames: Use ANSI yellow-colored text characters for the Pac-Man wedge shape.
    Frame 1 (mouth open): `f"{YEL}C{RST}"` -- the classic C shape looks like open Pac-Man
    Frame 2 (mouth closed): `f"{YEL}O{RST}"` -- closed mouth (was just a dot before!)
    WAIT -- but then sprite display_width might vary if we use emoji-width chars.
    Actually `C` and `O` are both 1 display col. But the fill is also 1 col dots.
    The key insight: colored `C`/`O` on a dot trail IS the classic Pac-Man look.
    Actually even better: Frame 1 (open): `f"{YEL}<{RST}"` and Frame 2 (closed): `f"{YEL}-{RST}"`
    The `<` is the iconic Pac-Man wedge shape! Both are 1 display col.
  - completion_frame: `\U0001f47b` (ghost emoji -- already there, keep it)
  - No decoration.
- unicode tier:
  - bar_fill: `("\u00b7",)` (middle dot)
  - sprite frames: `<` (open) and `-` (closed) -- no ANSI coloring
  - completion_frame: `(^o^)` (ghost-ish face)
- ascii tier:
  - bar_fill: `(".",)`
  - sprite frames: `<` (open) and `-` (closed)
  - completion_frame: `O` (ghost)
- fps: 6.0 (faster for Pac-Man munching feel), mode: WALK

IMPORTANT: Since sprite width changes from 1 col (normal frames `<`/`-`) to 2 cols
(completion `\U0001f47b` ghost emoji), that's OK because completion_frame is rendered
separately at 100% and doesn't need consistent width with animation frames.

**wizard -- "Wizard leaving magical symbol trail"**
User feedback: "the path behind wizard doesn't make sense, what about leaving behind all
the various 'wizardy' emoji? stars, crystal balls, cats, sparkles etc"
Since bar_fill chars must be 1 display col, actual emoji (2-col) cannot be used directly.
Use ANSI-colored magical unicode symbols that are each 1 display col:
- emoji tier:
  - bar_fill: A diverse tuple of ANSI-colored magical symbols, each 1 display col:
    ```python
    fill = (
        f"{MAG}\u2605{RST}",   # ★ magenta star
        f"{CYN}\u2733{RST}",   # ✳ cyan sparkle
        f"{BLU}\u2666{RST}",   # ♦ blue diamond
        f"{MAG}\u2606{RST}",   # ☆ magenta hollow star
        f"{CYN}\u2744{RST}",   # ❄ cyan snowflake
        f"{BLU}\u2604{RST}",   # ☄ blue comet
    )
    ```
    This creates a colorful, varied magical trail that cycles through different symbols.
  - sprite: `\U0001f9d9` (wizard emoji, 2 cols) for both frames
  - completion_frame: `\U0001f9d9\u2728` (wizard + sparkles)
  - No decoration.
- unicode tier:
  - bar_fill: Same ANSI-colored symbols as emoji tier
  - sprite frames: `*>` and `~>` (existing, these are fine)
  - completion_frame: `*>*`
- ascii tier:
  - bar_fill: `("*", "~", "+", ".", "*", "~")` -- variety of magical-ish ASCII chars
  - sprite frames: `*>` and `~>`
  - completion_frame: `*>*`
- fps: 3.0, mode: WALK

**disco -- "Glittery disco dance floor, NOT rainbow blocks"**
User feedback: "carbon copy of nyan." The fill must be visually distinct.
Nyan uses solid `\u2588` blocks in 6 rainbow ANSI colors.
Disco should use different CHARACTER SHAPES with different COLOR choices:
- emoji tier:
  - bar_fill: Alternating sparkle/diamond unicode shapes (NOT solid blocks) with
    magenta/cyan/white ANSI colors for a disco-ball glitter effect:
    ```python
    fill = (
        f"{MAG}\u2733{RST}",   # ✳ magenta eight-spoked asterisk
        f"{CYN}\u2666{RST}",   # ♦ cyan diamond
        f"{WHT}\u2605{RST}",   # ★ white/bright star
        f"{MAG}\u2022{RST}",   # • magenta bullet
        f"{CYN}\u2733{RST}",   # ✳ cyan eight-spoked asterisk
        f"{WHT}\u2666{RST}",   # ♦ white diamond
    )
    ```
    Use `\033[97m` for bright white (WHT), `\033[35m` for magenta, `\033[36m` for cyan.
    This creates a sparkling glitter pattern vs nyan's smooth rainbow.
  - sprite frames: `\U0001faa9` (mirror ball emoji) if available (disp_len 2).
    If mirror ball has issues, use `\U0001f483` (dancer emoji, disp_len 2).
    Verify disp_len of `\U0001faa9`. Use same emoji for both frames (consistent width).
  - completion_frame: `\U0001faa9\U0001f3b5` (mirror ball + music note) or
    `\U0001f483\U0001f3b5` (dancer + music note)
  - No decoration.
- unicode tier:
  - bar_fill: Same ANSI-colored sparkle characters as emoji tier
  - sprite frames: `(o)` and `(O)` (disco ball pulsing)
  - completion_frame: `(O)!`
- ascii tier:
  - bar_fill: `("*", ".", "+", ".", "*", ".")` -- glittery ASCII pattern
  - sprite frames: `(o)` and `(O)`
  - completion_frame: `(O)!`
- fps: 6.0 (faster for disco energy), mode: WALK

**For ALL themes, after writing, verify with:**
```python
from nyanbar.utils import disp_len
# For each theme, for each tier, verify:
# 1. All bar_fill chars are 1 display col
# 2. All animation frames have consistent display_width
# 3. Sprite frames are single-line (height == 1)
```
  </action>
  <verify>
Run: `.venv/bin/python -c "from nyanbar.utils import disp_len; from nyanbar.registry import get_theme; import nyanbar.themes; [print(f'{t} {tier}: fill_widths={[disp_len(c) for c in get_theme(t, tier).bar_fill]}, frame_widths={[f.display_width for f in get_theme(t, tier).frames]}') for t in ('construction','pac_man','wizard','disco') for tier in ('emoji','unicode','ascii')]"`
All bar_fill chars should show width 1. All frame_widths within a theme+tier should be identical.
  </verify>
  <done>
All four themes reworked: construction has earth/paving fill with construction crane sprite;
pac_man has dot fill with yellow `<`/`-` text-art wedge; wizard has colorful magical symbol
trail (stars, diamonds, snowflakes); disco has sparkle/diamond glitter pattern distinct from
nyan's solid rainbow blocks. All bar_fill chars are 1 display col. All frame widths consistent.
  </done>
</task>

<task type="auto">
  <name>Task 2: Update tests and demo for reworked themes + indeterminate mode</name>
  <files>
    tests/test_themes.py
    demo.py
  </files>
  <action>
**tests/test_themes.py updates:**
Update theme-specific completion tests that reference the old completion chars:

1. `test_pac_man_completion_has_ghost` -- Keep as-is if ghost emoji `\U0001f47b` is still
   the completion frame (it should be).

2. `test_construction_completion_has_ok` -- Currently checks for "OK" in ascii tier.
   If construction ascii completion is still `[OK]`, keep. If changed to something else
   (e.g., a house symbol), update the assertion.

3. `test_wizard_completion_has_star` -- Currently checks for `\u2605` in emoji tier.
   If wizard completion still contains star (it does via `\u2728` sparkles), update to
   check for `\u2728` (sparkles) since new completion is `\U0001f9d9\u2728`.

4. `test_disco_completion_has_note` -- Currently checks for `\U0001f3b5`. If disco
   completion still has music note, keep as-is.

The parametrized tests (test_theme_is_animation, test_theme_has_bar_fill, etc.) should
all pass automatically since the theme structure is preserved.

Run the full test suite to verify nothing breaks.

**demo.py updates:**
Add a section after the existing theme loop that demonstrates `total=None` (indeterminate)
mode. Since WANDER and CHASE AnimationModes do not exist yet, show the current behavior
with clear labeling:

```python
# After existing theme loop:
print("\n  === Indeterminate Mode (total=None) ===\n")
print("  Note: Shows current behavior with total=None.\n")

import time
from nyanbar import tqdm as nyanbar_tqdm

# Show 2-3 themes in indeterminate mode using manual update()
for theme in ["nyan", "wizard", "disco"]:
    print(f"\n  --- {theme} (total=None) ---\n")
    bar = nyanbar_tqdm(total=None, theme=theme, desc=theme)
    for i in range(60):
        time.sleep(0.03)
        bar.update(1)
    bar.close()
    time.sleep(0.3)

print()
```

Keep the existing determinate theme loop intact. The new indeterminate section comes after.
  </action>
  <verify>
Run: `.venv/bin/pytest tests/test_themes.py -v --tb=short` -- all tests pass.
Run: `.venv/bin/python -c "from nyanbar.registry import get_theme; import nyanbar.themes; [get_theme(t, tier) for t in ('construction','pac_man','wizard','disco') for tier in ('emoji','unicode','ascii')]"` -- no errors.
  </verify>
  <done>
Tests updated to match new completion frames. All parametrized theme tests pass.
demo.py has both the existing determinate theme showcase AND a new indeterminate mode
section showing total=None behavior with a few select themes.
  </done>
</task>

</tasks>

<verification>
1. `.venv/bin/pytest tests/ -v --tb=short` -- all tests pass
2. `.venv/bin/python -m mypy nyanbar/ --strict` -- no type errors
3. Visual spot-check: `.venv/bin/python demo.py` -- themes render distinctly,
   indeterminate section runs without errors
4. Verify disco fill is NOT the same as nyan: compare bar_fill tuples manually
</verification>

<success_criteria>
- construction theme has a paving/building narrative, not generic hazard stripes
- pac_man uses text-art wedge `<` character, not yellow/orange circle emoji
- wizard trail is colorful magical symbols (stars, diamonds, snowflakes), not purple blocks
- disco fill uses sparkle/diamond chars in magenta/cyan/white, not same 6-color solid blocks as nyan
- demo.py shows total=None indeterminate mode examples
- All existing tests pass, no type errors
</success_criteria>

<output>
After completion, create `.planning/quick/2-rework-construction-pac-man-wizard-disco/2-SUMMARY.md`
</output>
