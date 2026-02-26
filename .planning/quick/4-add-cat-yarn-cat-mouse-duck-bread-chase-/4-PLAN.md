---
phase: quick-4
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - nyanbar/themes/_cat_yarn.py
  - nyanbar/themes/_cat_mouse.py
  - nyanbar/themes/_duck_bread.py
  - nyanbar/themes/__init__.py
  - tests/test_themes.py
autonomous: true
requirements: [QUICK-4]
must_haves:
  truths:
    - "cat_yarn theme renders at all 5 progress levels in all 3 tiers"
    - "cat_mouse theme renders at all 5 progress levels in all 3 tiers"
    - "duck_bread theme renders at all 5 progress levels in all 3 tiers"
    - "All 3 themes have decoration (3-line output)"
    - "All 3 themes pass the full existing test suite including ANSI integrity"
    - "ALL_THEMES list has 26 entries"
  artifacts:
    - path: "nyanbar/themes/_cat_yarn.py"
      provides: "Cat chasing yarn theme"
    - path: "nyanbar/themes/_cat_mouse.py"
      provides: "Cat chasing mouse theme"
    - path: "nyanbar/themes/_duck_bread.py"
      provides: "Duck chasing bread theme"
  key_links:
    - from: "nyanbar/themes/__init__.py"
      to: "nyanbar/themes/_cat_yarn.py"
      via: "import registration"
    - from: "nyanbar/themes/__init__.py"
      to: "nyanbar/themes/_cat_mouse.py"
      via: "import registration"
    - from: "nyanbar/themes/__init__.py"
      to: "nyanbar/themes/_duck_bread.py"
      via: "import registration"
    - from: "tests/test_themes.py"
      to: "ALL_THEMES"
      via: "list includes cat_mouse, cat_yarn, duck_bread"
---

<objective>
Add 3 chase-themed progress bars: cat_yarn, cat_mouse, duck_bread.

Purpose: Expand theme library with a "chase" motif -- compound two-character sprites where a chaser pursues a target across the bar, with thematic decoration.
Output: 3 new theme files, updated registry, updated tests (26 themes total).
</objective>

<execution_context>
@/Users/prwilliams/.claude/get-shit-done/workflows/execute-plan.md
@/Users/prwilliams/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@nyanbar/themes/_nyan.py (gold standard: decoration pattern, 3-tier structure, ANSI colors)
@nyanbar/themes/_rocket.py (good reference: compound sprite completion, fill variety)
@nyanbar/themes/_garden.py (good reference: thematic decoration, colored fill)
@nyanbar/models.py (Animation, Frame, AnimationMode)
@nyanbar/engine.py (render_themed_bar -- the bar line is: |fill|sprite|empty|)
@nyanbar/themes/__init__.py (import registration pattern)
@tests/test_themes.py (ALL_THEMES, DECORATED_THEMES, test patterns)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create 3 chase theme files</name>
  <files>
    nyanbar/themes/_cat_yarn.py
    nyanbar/themes/_cat_mouse.py
    nyanbar/themes/_duck_bread.py
  </files>
  <action>
Create 3 theme files following the exact pattern of `_nyan.py` (3-tier factory, `register_theme()` at module level, `__all__: list[str] = []`).

**Chase mechanic via compound sprites:**
The bar renders as `|fill|sprite|empty|`. To create a "chase" effect, the SPRITE itself is a compound of chaser+target. Two animation frames alternate:
- Frame A: `chaser + " " + target` (gap = actively chasing, disp_len=5)
- Frame B: `chaser + target + " "` (no gap = caught momentarily, trailing space keeps disp_len=5)
Both frames MUST be disp_len=5 for emoji tier. Verify this holds for all tiers.

**Theme 1: cat_yarn** (`_cat_yarn.py`)
- emoji tier:
  - bar_fill: yarn-colored trail -- mix of magenta/yellow/red ANSI-colored unicode chars (bullet, diamond) representing yarn strands. 6 elements, each 1 display col.
  - sprite frames: Frame A = `"\U0001f431 \U0001f9f6"` (cat space yarn, 5 cols), Frame B = `"\U0001f431\U0001f9f6 "` (cat yarn space, 5 cols)
  - completion_frame: `"\U0001f63b\U0001f9f6"` (heart-eyes cat + yarn, 4 cols -- cat caught it!)
  - decoration: 2 alternating frames, each with 2 lines (above bar, below bar). Above: scattered yarn balls using middle-dot and bullet in magenta/yellow. Below: paw prints using middle-dot and tilde in magenta. Use ANSI colors with RST.
  - completion_decoration: dense celebratory pattern of yarn balls
  - fps=3.0
- unicode tier:
  - bar_fill: same ANSI-colored chars as emoji (magenta/yellow unicode symbols)
  - sprite frames: `">^.^ o"` / `">^.^o "` (both 6 cols -- cat face chasing yarn ball)
  - completion_frame: `">^.^o!"` (7 cols -- caught with celebration)
  - decoration: scattered `.` and `~` above, `~` pattern below (no ANSI)
  - completion_decoration: dense `.` `~` pattern
- ascii tier:
  - bar_fill: `("~", "-", "~", "-")` representing yarn strands
  - sprite frames: `">^.^ o"` / `">^.^o "` (both 6 cols)
  - completion_frame: `">^.^o!"` (7 cols)
  - decoration: `.` and `~` pattern, no ANSI
  - completion_decoration: dense pattern

**Theme 2: cat_mouse** (`_cat_mouse.py`)
- emoji tier:
  - bar_fill: paw-print trail -- mix of yellow/white/brown ANSI-colored chars (bullet, dot, comma shapes). 6 elements, each 1 display col.
  - sprite frames: Frame A = `"\U0001f431 \U0001f42d"` (cat space mouse, 5 cols), Frame B = `"\U0001f431\U0001f42d "` (cat mouse space, 5 cols)
  - completion_frame: `"\U0001f63c\U0001f42d"` (smirking cat + mouse, 4 cols -- cat caught it!)
  - decoration: 2 alternating frames. Above: scattered cheese crumbs (yellow middle-dot, bullet). Below: mouse footprints (small dots, periods in white/grey ANSI).
  - completion_decoration: dense celebratory cheese pattern
  - fps=3.0
- unicode tier:
  - bar_fill: ANSI-colored paw prints (yellow/white)
  - sprite frames: `">^.^ @"` / `">^.^@ "` (both 6 cols -- cat face chasing mouse @)
  - completion_frame: `">^.^@!"` (7 cols)
  - decoration: `.` scattered above, `,` below
  - completion_decoration: dense pattern
- ascii tier:
  - bar_fill: `(".", ",", ".", ",")` -- tiny footprints
  - sprite frames: `">^.^ @"` / `">^.^@ "` (both 6 cols)
  - completion_frame: `">^.^@!"` (7 cols)
  - decoration: `.` and `,` pattern
  - completion_decoration: dense pattern

**Theme 3: duck_bread** (`_duck_bread.py`)
- emoji tier:
  - bar_fill: breadcrumb/water trail -- mix of cyan/yellow/blue ANSI-colored chars (tilde, bullet, middle-dot). 6 elements, each 1 display col.
  - sprite frames: Frame A = `"\U0001f986 \U0001f35e"` (duck space bread, 5 cols), Frame B = `"\U0001f986\U0001f35e "` (duck bread space, 5 cols)
  - completion_frame: `"\U0001f986\U0001f35e"` (duck + bread, 4 cols -- duck got it, could add star but keep it clean)
  - Actually, for test consistency, use: `"\U0001f986\u2605"` (duck + star, tests check for star in completion). Wait -- no, the test just checks the completion_frame exists and its lines[0] appears in the bar output. Let's use `"\U0001f986\U0001f35e"` (duck ate the bread). But we should add a recognizable completion marker. Use `"\U0001f986\u2605"` (duck + star) for consistency with other themes.
  - decoration: 2 alternating frames. Above: water ripples (cyan tilde, middle-dot). Below: breadcrumbs (yellow bullet, dot).
  - completion_decoration: dense water/celebration pattern
  - fps=3.0
- unicode tier:
  - bar_fill: ANSI-colored water ripples (cyan/blue)
  - sprite frames: `"=< o"` / `"=<o "` (both 4 cols -- duck face chasing bread crumb)
  - completion_frame: `"=<o!"` (4 cols)
  - decoration: `~` ripples above, `.` crumbs below
  - completion_decoration: dense pattern
- ascii tier:
  - bar_fill: `("~", ".", "~", ".")` -- water and crumbs
  - sprite frames: `"=< o"` / `"=<o "` (both 4 cols)
  - completion_frame: `"=<o!"` (4 cols)
  - decoration: `~` and `.` pattern
  - completion_decoration: dense pattern

**CRITICAL CONSTRAINTS:**
1. Every bar_fill char must be exactly 1 display col (use `disp_len()` mentally -- ANSI escape codes are 0 cols, unicode bullets/diamonds/tildes are 1 col each)
2. All frames within a tier must have identical `display_width` (the Frame dataclass auto-computes this from `disp_len(line)`)
3. Decoration frames must have exactly 2 lines (line[0] = above bar, line[1] = below bar)
4. Each tier's completion_frame must have 1 line
5. All sprites are single-line (height=1)
6. Use `from ..models import Animation, AnimationMode, Frame` and `from ..registry import register_theme`
7. End each file with `register_theme("theme_name", _create)`
  </action>
  <verify>
Run `.venv/bin/python -c "from nyanbar.themes import _cat_yarn, _cat_mouse, _duck_bread; print('imports OK')"` to confirm modules load.
Then run `.venv/bin/python -c "
from nyanbar.registry import get_theme
from nyanbar.utils import disp_len
for name in ['cat_yarn', 'cat_mouse', 'duck_bread']:
    for tier in ['emoji', 'unicode', 'ascii']:
        a = get_theme(name, tier)
        widths = {f.display_width for f in a.frames}
        assert len(widths) == 1, f'{name}/{tier}: inconsistent frame widths {widths}'
        assert a.bar_fill is not None, f'{name}/{tier}: no bar_fill'
        assert a.decoration is not None, f'{name}/{tier}: no decoration'
        assert a.completion_frame is not None, f'{name}/{tier}: no completion_frame'
        assert a.completion_decoration is not None, f'{name}/{tier}: no completion_decoration'
        for bf in a.bar_fill:
            assert disp_len(bf) == 1, f'{name}/{tier}: bar_fill char {bf!r} is {disp_len(bf)} cols'
        for dec in a.decoration:
            assert len(dec.lines) == 2, f'{name}/{tier}: decoration frame has {len(dec.lines)} lines, need 2'
print('All 3 chase themes validated OK')
"` to confirm all constraints hold.
  </verify>
  <done>3 theme files exist, all load without error, all have bar_fill + decoration + completion_frame + consistent frame widths across all 3 tiers.</done>
</task>

<task type="auto">
  <name>Task 2: Register themes and update tests</name>
  <files>
    nyanbar/themes/__init__.py
    tests/test_themes.py
  </files>
  <action>
**Update `nyanbar/themes/__init__.py`:**
Add 3 new imports in alphabetical position among the existing imports:
```python
from . import _cat_mouse     # noqa: F401
from . import _cat_yarn      # noqa: F401
from . import _duck_bread    # noqa: F401
```
These go after `_candy` and before `_coffee` (for cat_mouse, cat_yarn) and after `_disco` before `_deal_with_it` wait -- actually just insert them alphabetically:
- `_cat_mouse` goes between `_candy` and `_coffee`
- `_cat_yarn` goes between `_cat_mouse` and `_coffee`
- `_duck_bread` goes between `_disco` and `_deal_with_it`

Wait, current order: _aurora, _candy, _coffee, _construction, _deal_with_it, _disco...
Alphabetically: _cat_mouse < _cat_yarn < _coffee, and _deal_with_it < _disco < _duck_bread

So the new order is:
```
_aurora, _candy, _cat_mouse, _cat_yarn, _coffee, _construction, _deal_with_it, _disco, _duck_bread, _finger_guns, _fire, _garden, _heartbeat, _lenny, _lightning, _mario, _matrix, _nyan, _ocean, _rocket, _shrug, _snake, _table_flip, _train, _wizard, _zen
```

**Update `tests/test_themes.py`:**

1. Update `ALL_THEMES` list to include `"cat_mouse"`, `"cat_yarn"`, `"duck_bread"` in sorted position (26 total):
```python
ALL_THEMES = [
    "aurora", "candy", "cat_mouse", "cat_yarn", "coffee", "construction",
    "deal_with_it", "disco", "duck_bread", "finger_guns", "fire", "garden",
    "heartbeat", "lenny", "lightning", "mario", "matrix", "nyan", "ocean",
    "rocket", "shrug", "snake", "table_flip", "train", "wizard", "zen",
]
```

2. Add `"cat_mouse"`, `"cat_yarn"`, `"duck_bread"` to the `DECORATED_THEMES` list (in sorted position):
```python
DECORATED_THEMES = [
    "aurora", "cat_mouse", "cat_yarn", "duck_bread", "fire", "garden",
    "heartbeat", "lightning", "nyan", "rocket", "train", "wizard",
]
```

3. Add the parametrized decoration existence test for the new chase themes:
```python
@pytest.mark.parametrize("theme", ["cat_mouse", "cat_yarn", "duck_bread"])
@pytest.mark.parametrize("tier", TIERS)
def test_chase_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None
```

4. Add theme-specific completion tests for each chase theme (following the existing pattern):
```python
def test_cat_yarn_completion_has_heart_eyes() -> None:
    anim = get_theme("cat_yarn", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f63b" in comp  # heart-eyes cat


def test_cat_mouse_completion_has_smirking_cat() -> None:
    anim = get_theme("cat_mouse", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\U0001f63c" in comp  # smirking cat


def test_duck_bread_completion_has_star() -> None:
    anim = get_theme("duck_bread", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star
```
  </action>
  <verify>
Run `.venv/bin/pytest tests/test_themes.py -x -q` -- all tests must pass (should be ~1400+ tests with the 3 new themes adding ~90 parametrized cases).
Then run `.venv/bin/python -c "from nyanbar.registry import list_themes; t = list_themes(); print(f'{len(t)} themes: {t}')"` and confirm 26 themes listed.
  </verify>
  <done>ALL_THEMES has 26 entries, DECORATED_THEMES includes the 3 new chase themes, all parametrized tests pass, theme-specific completion tests pass, and `list_themes()` returns 26 themes.</done>
</task>

</tasks>

<verification>
1. `.venv/bin/pytest tests/ -x -q` -- full test suite passes
2. `.venv/bin/python -c "from nyanbar.registry import list_themes; assert len(list_themes()) == 26"`
3. `.venv/bin/python demo.py` -- visual confirmation that all 26 themes render (including 3 new chase themes)
4. `.venv/bin/python -c "from nyanbar.utils import disp_len; from nyanbar.registry import get_theme; [get_theme(t, 'emoji') for t in ['cat_yarn','cat_mouse','duck_bread']]"` -- no errors
</verification>

<success_criteria>
- 3 new theme files exist and register correctly
- All 3 themes have decoration (render 3 lines), bar_fill, completion_frame, completion_decoration across all tiers
- Frame widths consistent within each tier
- ALL_THEMES = 26, DECORATED_THEMES includes all 3 chase themes
- Full test suite passes (pytest exits 0)
- demo.py shows all 26 themes including the new chase themes
</success_criteria>

<output>
After completion, create `.planning/quick/4-add-cat-yarn-cat-mouse-duck-bread-chase-/4-SUMMARY.md`
</output>
