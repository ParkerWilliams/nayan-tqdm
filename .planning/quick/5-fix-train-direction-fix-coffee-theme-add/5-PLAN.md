---
phase: quick-5
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - nyanbar/themes/_train.py
  - nyanbar/themes/_coffee.py
  - nyanbar/themes/_cat_smug.py
  - nyanbar/themes/_cat_sleepy.py
  - nyanbar/themes/_cat_play.py
  - nyanbar/themes/__init__.py
  - tests/test_themes.py
autonomous: true
requirements: [QUICK-5]

must_haves:
  truths:
    - "Train theme sprite clearly suggests rightward motion via text-art locomotive with ANSI yellow color"
    - "Coffee theme emoji tier uses actual U+2615 coffee emoji (2 cols) as sprite, not text-art"
    - "Coffee theme fill uses steam-related 1-col chars, not brown blocks"
    - "Coffee theme has steam/bean decoration (3-line output)"
    - "cat_smug theme uses (=^.^=) 7-col kaomoji with cozy fill and paw/fish trail"
    - "cat_sleepy theme uses (-._.-)  7-col kaomoji with slow fps and pastel fill"
    - "cat_play theme uses playful alternating kaomoji with yarn/toy fill"
    - "All 3 new cat themes registered and appear in ALL_THEMES"
    - "All frames within each theme have identical display_width"
    - "All bar_fill chars are 1 display col each"
  artifacts:
    - path: "nyanbar/themes/_train.py"
      provides: "Fixed train theme with text-art rightward locomotive"
      contains: "==>"
    - path: "nyanbar/themes/_coffee.py"
      provides: "Fixed coffee theme with real emoji and steam fill/decoration"
      contains: "\\u2615"
    - path: "nyanbar/themes/_cat_smug.py"
      provides: "Smug cat kaomoji theme"
      contains: "(=^.^=)"
    - path: "nyanbar/themes/_cat_sleepy.py"
      provides: "Sleepy cat kaomoji theme"
      contains: "(-._.-)'"
    - path: "nyanbar/themes/_cat_play.py"
      provides: "Playful cat kaomoji theme"
      contains: "(=^.^=)"
    - path: "nyanbar/themes/__init__.py"
      provides: "Import registration for all 3 new themes"
    - path: "tests/test_themes.py"
      provides: "Updated ALL_THEMES list + completion tests for new themes"
  key_links:
    - from: "nyanbar/themes/_cat_smug.py"
      to: "nyanbar/themes/__init__.py"
      via: "import triggers register_theme"
      pattern: "from . import _cat_smug"
    - from: "nyanbar/themes/_cat_sleepy.py"
      to: "nyanbar/themes/__init__.py"
      via: "import triggers register_theme"
      pattern: "from . import _cat_sleepy"
    - from: "nyanbar/themes/_cat_play.py"
      to: "nyanbar/themes/__init__.py"
      via: "import triggers register_theme"
      pattern: "from . import _cat_play"
    - from: "tests/test_themes.py"
      to: "ALL_THEMES list"
      via: "parametrized test coverage"
      pattern: "cat_smug.*cat_sleepy.*cat_play"
---

<objective>
Fix train direction (text-art rightward locomotive), rework coffee theme (real emoji + steam fill + decoration), and add 3 unicode cat kaomoji themes (cat_smug, cat_sleepy, cat_play).

Purpose: Train emoji faces left in Unicode (structural limitation) -- replace with ANSI-colored text-art sprite pointing right. Coffee was using text-art instead of the actual coffee emoji and had a thematically disconnected brown-block fill. The 3 new cat kaomoji themes add charm distinct from the existing nyan/cat_yarn/cat_mouse chase themes.

Output: 5 theme files (2 modified, 3 new), updated __init__.py, updated tests. 29 themes total.
</objective>

<execution_context>
@/Users/prwilliams/.claude/get-shit-done/workflows/execute-plan.md
@/Users/prwilliams/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@nyanbar/themes/_nyan.py (gold standard: 3-tier pattern, decoration, ANSI colors, bar_fill)
@nyanbar/themes/_train.py (current train -- emoji faces left, needs text-art fix)
@nyanbar/themes/_coffee.py (current coffee -- uses c[_] text-art, brown blocks, no decoration)
@nyanbar/themes/_cat_yarn.py (reference: chase theme with kaomoji-style sprites)
@nyanbar/models.py (Animation, Frame, AnimationMode dataclasses)
@nyanbar/engine.py (render_themed_bar -- bar_fill cycling, decoration above/below)
@nyanbar/themes/__init__.py (import registration)
@tests/test_themes.py (ALL_THEMES, DECORATED_THEMES, completion tests pattern)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Fix train and coffee themes</name>
  <files>
    nyanbar/themes/_train.py
    nyanbar/themes/_coffee.py
    tests/test_themes.py
  </files>
  <action>
**Train (_train.py) -- Replace emoji locomotive with text-art rightward sprite:**

- Emoji tier: Replace U+1F682 locomotive emoji with ANSI yellow text-art sprites.
  - Frame A: `f"{_YEL}==>{_RST}"` (3 display cols) -- simple rightward train
  - Frame B: `f"{_YEL}=>{_RST} "` (3 display cols) -- piston motion variant (note trailing space to keep 3 cols)
  - Wait -- 3 cols is too small visually. Better: `f"{_YEL}[==>]{_RST}"` (5 cols, same as unicode tier's `[TTT]`)
  - Frame A: `f"{_YEL}[==>]{_RST}"` (5 cols)
  - Frame B: `f"{_YEL}[==>{_RST}{_DRK}]{_RST}"` -- Actually keep it simple, both frames same width.
  - Frame A: `f"{_YEL}[==>]{_RST}"` (5 display cols)
  - Frame B: `f"{_YEL}[=>>{_RST}{_DRK}]{_RST}"` -- no, just use clean text art:
  - Frame A: `f"{_YEL}[==>{_RST}]"` (5 display cols)
  - Frame B: `f"{_YEL}[==>]{_RST}"` (5 display cols) -- both identical is fine, the animation comes from decoration
  - Completion: `f"{_YEL}[==>]{_RST}\u2605"` (6 cols) -- train + star
- Unicode tier: Keep existing `[TTT]`/`[===]` sprites (already fine, text-art facing right).
- ASCII tier: Keep existing `[TTT]` sprites (already fine).
- Add `_YEL = "\033[33m"` color constant.
- Keep all existing decoration (steam above, track below) -- it already works great.
- Verify: All emoji tier Frame display_widths are 5 (matching unicode tier).

**Coffee (_coffee.py) -- Use real emoji + steam fill + decoration:**

- Emoji tier:
  - Sprite: Use actual `\u2615` (2 display cols) for both frames. Completion: `\u2615\u2605` (3 cols, coffee + star).
  - Fill: Replace brown blocks with steam-themed 1-col chars using ANSI colors:
    ```python
    fill = (
        f"{_WHT}\u2022{_RST}",   # white bullet (steam wisp)
        f"{_BRN}\u25c6{_RST}",   # brown diamond (coffee bean)
        f"{_WHT}\u00b7{_RST}",   # white middle dot (steam)
        f"{_BRN}\u2022{_RST}",   # brown bullet (bean)
        f"{_WHT}\u25c6{_RST}",   # white diamond (steam)
        f"{_BRN}\u00b7{_RST}",   # brown middle dot (bean)
    )
    ```
    All 1 display col each. Alternates white steam wisps with brown coffee beans.
  - Add `_WHT = "\033[37m"` color constant.
  - Add decoration -- steam rising above, coffee bean pattern below:
    ```python
    dec_a = Frame(lines=(
        "  ~    \u00b0       ~         \u00b0   ~",
        "  \u2022 \u00b7 \u2022   \u00b7 \u2022   \u00b7 \u2022   \u00b7 \u2022",
    ))
    dec_b = Frame(lines=(
        "     \u00b0  ~        \u00b0  ~  \u00b0    ~",
        "  \u00b7 \u2022 \u00b7   \u2022 \u00b7   \u2022 \u00b7   \u2022 \u00b7",
    ))
    ```
    Use `~` and `\u00b0` (degree sign) for steam wisps above. Use `\u2022` (bullet) and `\u00b7` (middle dot) for coffee bean pattern below.
  - Completion decoration: steam settled, beans lined up.
  - Set `fps=3.0` (keep existing, gentle pace).

- Unicode tier:
  - Sprite: `f"{_BRN}c[_]{_RST}"` (4 cols with ANSI color). Completion: `f"{_BRN}c[_]{_RST}*"` (5 cols).
  - Same steam/bean fill as emoji tier (same ANSI-colored 1-col chars).
  - Same decoration pattern as emoji tier.

- ASCII tier:
  - Sprite: `"c[_]"` (4 cols, plain). Completion: `"c[_]*"` (5 cols).
  - Fill: `("~", ".", "~", ".")` -- steam wisps pattern, 1 col each.
  - Decoration: plain `~` and `.` steam wisps above, `. o` bean pattern below.

**Tests (test_themes.py):**

- Update `test_train_completion_has_star` -- still checks for `\u2605` in completion, should still pass.
- Add `test_coffee_has_decoration` parametrized across all 3 tiers: asserts `anim.decoration is not None` and `anim.completion_decoration is not None`.
- Add `"coffee"` to the `DECORATED_THEMES` list (so it gets the 3-line rendering test).
- Update `test_coffee_completion_has_star` -- still checks for `\u2605`, should still pass since emoji tier completion is `\u2615\u2605`.
  </action>
  <verify>
`.venv/bin/python -m pytest tests/test_themes.py -x -q` -- all existing tests pass plus new coffee decoration tests.
`.venv/bin/python -c "from nyanbar.registry import get_theme; from nyanbar.utils import disp_len; a=get_theme('train','emoji'); print([f.display_width for f in a.frames]); print(disp_len(a.frames[0].lines[0]))"` -- frame widths are [5, 5].
`.venv/bin/python -c "from nyanbar.registry import get_theme; a=get_theme('coffee','emoji'); print(a.frames[0].lines[0]); print(a.decoration is not None)"` -- shows coffee emoji, True.
  </verify>
  <done>
Train emoji tier uses yellow ANSI text-art `[==>]` (5 cols) rightward sprite instead of left-facing locomotive emoji. Coffee emoji tier uses real U+2615 coffee emoji sprite, steam/bean alternating fill, and has steam-above/bean-below decoration. All 26 existing themes still pass all tests. Coffee now appears in DECORATED_THEMES with 3-line rendering.
  </done>
</task>

<task type="auto">
  <name>Task 2: Add cat_smug, cat_sleepy, cat_play kaomoji themes</name>
  <files>
    nyanbar/themes/_cat_smug.py
    nyanbar/themes/_cat_sleepy.py
    nyanbar/themes/_cat_play.py
    nyanbar/themes/__init__.py
    tests/test_themes.py
  </files>
  <action>
Create 3 new kaomoji cat themes. Each follows the _nyan.py 3-tier pattern. Since these are pure unicode/text-art kaomoji, the emoji and unicode tiers share ANSI-colored sprites while ascii tier is plain. All sprites within a theme MUST have identical display_width.

**cat_smug (_cat_smug.py):**
- Concept: A smug cat strolling confidently, leaving paw prints and fish behind.
- Emoji tier:
  - Sprites (7 cols each): `f"{_MAG}(=^.^=){_RST}"` and `f"{_MAG}(=^w^=){_RST}"` (smug alternating expressions)
  - Completion: `f"{_MAG}(=^\u2764^=){_RST}"` -- heart-nose, verify display_width (should be 7: `(`, `=`, `^`, heart 1 col, `^`, `=`, `)` -- WAIT: `\u2764` is heavy black heart, check eaw. Use `\u2665` (heart suit, 1 col guaranteed) instead: `f"{_RED}(=^\u2665^=){_RST}"` (7 cols).
  - Fill: Cozy warm colors -- `f"{_MAG}\u2022{_RST}"` (magenta bullet), `f"{_YEL}\u00b7{_RST}"` (yellow dot), `f"{_CYN}\u2022{_RST}"` (cyan bullet), `f"{_MAG}\u00b7{_RST}"` -- paw-print-like dots.
  - Decoration: Fish and paw prints above, purr pattern below.
    - Above: scattered `><>` fish shapes and `\u00b7` dots
    - Below: `. ~ .` purr wisps
  - fps: 2.0 (slow, smug pace)
- Unicode tier: Same sprites but with ANSI color. Same fill and decoration.
- ASCII tier: `(=^.^=)` and `(=^w^=)` plain (7 cols). Fill: `(".", "~", ".", "~")`. Completion: `(=^w^=)` (same 7 cols). Decoration: plain dots and tildes.
- Colors: `_MAG`, `_YEL`, `_CYN`, `_RED`, `_RST`.

**cat_sleepy (_cat_sleepy.py):**
- Concept: A drowsy cat, dreamy pastel fill, slow lazy pace.
- Emoji tier:
  - Sprites (7 cols each): `f"{_BLU}(-._.-)  {_RST}"` -- WAIT, that adds spaces making it 9. Keep sprite exactly 7 cols: `f"{_BLU}(-._.-)  {_RST}"` NO. The sprite is `(-._.-)` which is already 7 cols. Both frames 7 cols.
  - Frame A: `f"{_BLU}(-._.-)  {_RST}"` -- NO. Just `f"{_BLU}(-._.-)  {_RST}"`. Stop. The SPRITE is the string inside Frame(lines=(...,)). It must be exactly 7 cols.
  - Frame A: `f"{_BLU}(-._.-){_RST} "` -- that's 8 cols (7 + space). No.
  - Frame A: `f"{_BLU}(-._.-)  {_RST}"` is 9 cols. WRONG.
  - Correct: Frame A: `f"{_BLU}(-._.-)  {_RST}"` -- STOP. `(-._.-)` = 7 cols already. No padding needed.
  - Frame A: `f"{_BLU}(-._.-)  {_RST}"` = `(` `-` `.` `_` `.` `-` `)` = 7 cols. ANSI codes don't count. Good.
  - WAIT I keep writing extra spaces. Let me be precise:
  - Frame A: `f"{_BLU}(-._.-)  {_RST}"` has `(-._.-)  ` = 9 printable chars. BAD.
  - Frame A: `f"{_BLU}(-._.-){_RST}"` = 7 display cols. CORRECT.
  - Frame B: `f"{_BLU}(u._.u){_RST}"` = 7 display cols. Drowsy variant.
  - Completion: `f"{_BLU}(-.\u2665.-){_RST}"` -- `(` `-` `.` heart(1) `.` `-` `)` = 7 cols. Dreaming of love.
  - Fill: Pastel dreamy -- `f"{_BLU}\u2022{_RST}"` (blue dot), `f"{_MAG}\u00b7{_RST}"` (magenta dot), `f"{_CYN}\u2022{_RST}"` (cyan dot), `f"{_BLU}\u00b7{_RST}"` (blue dot) -- soft, dreamy feel.
  - Decoration: `z` letters floating above (sleep), soft dots below.
    - Above: scattered `z` and `.` for sleeping wisps
    - Below: `. ~ .` dreamy clouds
  - fps: 1.5 (SLOW, drowsy pace -- this is a sleepy cat!)
- Unicode tier: Same ANSI-colored sprites, same fill, same decoration.
- ASCII tier: `(-._.-)` and `(u._.u)` plain (7 cols). Fill: `(".", "-", ".", "-")`. Completion: `(-._!-)` (7 cols, wake-up moment). Decoration: plain `z` and `.`.

**cat_play (_cat_play.py):**
- Concept: A playful cat batting at toys, energetic alternation.
- Emoji tier:
  - Need equal-width frames. `(=^.^=)~` is 8 cols, `~(=^.^=)` is 8 cols. Good -- bat left, bat right.
  - Frame A: `f"{_GRN}(=^.^=)~{_RST}"` (8 display cols) -- batting right
  - Frame B: `f"{_GRN}~(=^.^=){_RST}"` (8 display cols) -- batting left
  - Completion: `f"{_GRN}(=^\u2665^=){_RST}"` (7 cols) -- happy, relaxed after play. Actually completion_frame width doesn't need to match frame width (engine handles it separately at 100%).
  - Fill: Toy/yarn colors -- `f"{_RED}\u2022{_RST}"` (red dot), `f"{_GRN}\u25c6{_RST}"` (green diamond), `f"{_YEL}\u2022{_RST}"` (yellow dot), `f"{_RED}\u25c6{_RST}"` (red diamond), `f"{_GRN}\u2022{_RST}"` (green dot), `f"{_YEL}\u25c6{_RST}"` (yellow diamond) -- colorful toys.
  - Decoration: Bouncing toys above, paw scuffs below.
    - Above: `o` and `*` scattered (bouncing toys/balls)
    - Below: `~` and `.` (scuff marks, playful energy)
  - fps: 5.0 (FAST, energetic play!)
- Unicode tier: Same ANSI-colored sprites and fill. Same decoration.
- ASCII tier: `(=^.^=)~` and `~(=^.^=)` plain (8 cols). Fill: `("*", "~", "*", "~")`. Completion: `(=^o^=)` (7 cols). Decoration: plain `o`, `*`, `~`.

**__init__.py:**
Add 3 imports in alphabetical position:
```python
from . import _cat_play     # noqa: F401
from . import _cat_sleepy   # noqa: F401
from . import _cat_smug     # noqa: F401
```
Insert after `_cat_mouse` and before `_cat_yarn` (alphabetical order: cat_mouse, cat_play, cat_sleepy, cat_smug, cat_yarn).

**tests/test_themes.py:**
- Add `"cat_play"`, `"cat_sleepy"`, `"cat_smug"` to `ALL_THEMES` list (alphabetical).
- Add all 3 to `DECORATED_THEMES` list (alphabetical).
- Add completion-specific tests:
  ```python
  def test_cat_smug_completion_has_heart() -> None:
      anim = get_theme("cat_smug", "emoji")
      assert anim.completion_frame is not None
      comp = anim.completion_frame.lines[0]
      assert "\u2665" in comp  # heart suit

  def test_cat_sleepy_completion_has_heart() -> None:
      anim = get_theme("cat_sleepy", "emoji")
      assert anim.completion_frame is not None
      comp = anim.completion_frame.lines[0]
      assert "\u2665" in comp  # heart suit

  def test_cat_play_completion_has_heart() -> None:
      anim = get_theme("cat_play", "emoji")
      assert anim.completion_frame is not None
      comp = anim.completion_frame.lines[0]
      assert "\u2665" in comp  # heart suit
  ```
  </action>
  <verify>
`.venv/bin/python -m pytest tests/test_themes.py -x -q` -- all tests pass (should be ~1500+ with 29 themes x 3 tiers x 5 progress levels + specific tests).
`.venv/bin/python -c "from nyanbar.registry import list_themes; t=list_themes(); print(len(t), t)"` -- 29 themes, includes cat_play, cat_sleepy, cat_smug.
`.venv/bin/python -c "
from nyanbar.registry import get_theme
from nyanbar.utils import disp_len
for name in ['cat_smug', 'cat_sleepy', 'cat_play']:
    for tier in ['emoji', 'unicode', 'ascii']:
        a = get_theme(name, tier)
        widths = [f.display_width for f in a.frames]
        fills = [disp_len(c) for c in a.bar_fill]
        print(f'{name}/{tier}: frame_widths={widths}, fill_widths={fills}, dec={a.decoration is not None}')
        assert len(set(widths)) == 1, f'{name}/{tier} inconsistent frame widths: {widths}'
        assert all(w == 1 for w in fills), f'{name}/{tier} fill char not 1 col: {fills}'
        assert a.decoration is not None, f'{name}/{tier} missing decoration'
print('ALL OK')
"` -- all frame widths consistent, all fill chars 1 col, all have decoration.
  </verify>
  <done>
Three new cat kaomoji themes registered and fully tested: cat_smug (smug stroll, 2fps), cat_sleepy (drowsy drift, 1.5fps), cat_play (energetic batting, 5fps). Each has 3 tiers (emoji/unicode with ANSI color, ascii plain), consistent frame widths, 1-col fill chars, and steam/paw/toy decoration. ALL_THEMES and DECORATED_THEMES updated. 29 themes total. All tests pass including completion-specific tests.
  </done>
</task>

</tasks>

<verification>
1. `cd /Users/prwilliams/Repos/nayan-tqdm && .venv/bin/python -m pytest tests/test_themes.py -x -q` -- all tests pass
2. `cd /Users/prwilliams/Repos/nayan-tqdm && .venv/bin/python -m pytest tests/ -x -q` -- full suite passes
3. `cd /Users/prwilliams/Repos/nayan-tqdm && .venv/bin/python -m mypy nyanbar/ --strict` -- no type errors
4. Verify 29 themes registered: `.venv/bin/python -c "from nyanbar.registry import list_themes; print(len(list_themes()))"`
5. Verify train emoji sprite is text-art (no emoji codepoints in U+1F600-1FFFF range)
6. Verify coffee emoji sprite contains U+2615
7. Verify all new themes have consistent frame widths and 1-col fill chars
</verification>

<success_criteria>
- Train emoji tier uses ANSI yellow `[==>]` text-art sprite (rightward), not left-facing U+1F682 emoji
- Coffee emoji tier uses real U+2615 coffee emoji as sprite, steam/bean fill, has decoration (3-line output)
- cat_smug, cat_sleepy, cat_play themes created with 3 tiers each, all with decoration
- All frame widths consistent within each theme/tier
- All bar_fill chars are 1 display col
- 29 themes total, all tests pass, mypy --strict passes
</success_criteria>

<output>
After completion, create `.planning/quick/5-fix-train-direction-fix-coffee-theme-add/5-SUMMARY.md`
</output>
