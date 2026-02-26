---
phase: quick-3
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - nyanbar/themes/_pac_man.py       # DELETE
  - nyanbar/themes/_fire.py
  - nyanbar/themes/_heartbeat.py
  - nyanbar/themes/_wizard.py
  - nyanbar/themes/_rocket.py
  - nyanbar/themes/_train.py          # NEW
  - nyanbar/themes/_garden.py         # NEW
  - nyanbar/themes/_lightning.py      # NEW
  - nyanbar/themes/_candy.py          # NEW
  - nyanbar/themes/_aurora.py         # NEW
  - nyanbar/themes/_coffee.py         # NEW
  - nyanbar/themes/__init__.py
  - tests/test_themes.py
  - demo.py
autonomous: true
requirements: []

must_haves:
  truths:
    - "pac_man theme is completely removed -- not in registry, tests, or imports"
    - "fire theme has decoration lines (smoke/flame above and below bar)"
    - "heartbeat theme fill uses heart unicode characters (small/large alternating)"
    - "heartbeat theme has decoration (heartbeat/pulse line)"
    - "wizard theme has more fill variety (10+ symbols) and decoration lines"
    - "rocket theme has decoration (stars/exhaust particles above and below)"
    - "6 new themes exist: train, garden, lightning, candy, aurora, coffee"
    - "At least 3 of the 6 new themes have decoration lines"
    - "All 23 themes pass ALL_THEMES parametrized tests across all 3 tiers"
    - "demo.py shows all 23 themes without indeterminate section"
  artifacts:
    - path: "nyanbar/themes/__init__.py"
      provides: "Theme registration imports -- 23 themes, no pac_man"
    - path: "tests/test_themes.py"
      provides: "ALL_THEMES list with 23 entries, no pac_man, no pac_man-specific test"
    - path: "demo.py"
      provides: "Demo iterating all themes dynamically, no indeterminate section"
  key_links:
    - from: "nyanbar/themes/__init__.py"
      to: "each _theme.py module"
      via: "import triggering register_theme side effect"
      pattern: "from . import _"
    - from: "tests/test_themes.py"
      to: "ALL_THEMES list"
      via: "parametrize over every theme name"
      pattern: "ALL_THEMES"
---

<objective>
Cut pac_man, polish fire/heartbeat/wizard/rocket to nyan-quality (add decoration lines), and create 6 distinctive new themes. Result: 23 themes total, all passing tests.

Purpose: Elevate the theme library from mostly-flat themes to a collection where many have nyan-level visual richness (bar_fill + sprite + decoration).
Output: 23 working themes, updated tests, updated demo.
</objective>

<execution_context>
@/Users/prwilliams/.claude/get-shit-done/workflows/execute-plan.md
@/Users/prwilliams/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@nyanbar/themes/_nyan.py (gold standard pattern -- decoration, completion_decoration, rainbow fill)
@nyanbar/themes/__init__.py (current 18 theme imports)
@nyanbar/models.py (Animation model -- decoration/completion_decoration fields)
@nyanbar/engine.py (render_themed_bar -- handles decoration lines above/below)
@tests/test_themes.py (ALL_THEMES list, parametrized tests, pac_man-specific test)
@demo.py (current demo with indeterminate section to remove)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Cut pac_man and rework fire/heartbeat/wizard/rocket with decorations</name>
  <files>
    nyanbar/themes/_pac_man.py
    nyanbar/themes/_fire.py
    nyanbar/themes/_heartbeat.py
    nyanbar/themes/_wizard.py
    nyanbar/themes/_rocket.py
    nyanbar/themes/__init__.py
  </files>
  <action>
**Delete pac_man:**
- Delete `nyanbar/themes/_pac_man.py` entirely.
- Remove `from . import _pac_man  # noqa: F401` from `nyanbar/themes/__init__.py`.

**Rework fire (add smoke/flame decoration):**
Rewrite `nyanbar/themes/_fire.py`:
- emoji fill: Use a more dynamic 6-char cycle mixing red/orange/yellow ANSI blocks AND flame-like unicode chars. Example cycle: red full-block, yellow full-block, red dark-shade, orange full-block, yellow dark-shade, red full-block. The key is making it feel like flickering flame, not just static colored bars.
- Add `decoration` with 2 alternating Frame objects. Each Frame has 2 lines (above/below). Above line: scattered flame/smoke particles like `~` and `.` and small flame chars in red/yellow ANSI, spaced irregularly. Below line: similar ember/ash particles. These should alternate between frames to create flickering effect.
- Add `completion_decoration` with a dense celebratory pattern.
- Keep fire emoji sprite for emoji tier, ^v^ / /v\ kaomoji for unicode, ^ for ascii.
- ASCII tier: use `#` fill, simple `.` and `~` decoration (no ANSI).
- Unicode tier: same fill as emoji, kaomoji sprites, `~` and `.` decoration (no ANSI).

**Rework heartbeat (heart-character fill + pulse decoration):**
Rewrite `nyanbar/themes/_heartbeat.py`:
- emoji fill: Cycle of heart-related 1-display-col characters in pink/red ANSI. Use hearts of varying visual weight: `♡` (U+2661, 1 col), `♥` (U+2665, 1 col) in alternating magenta/red ANSI colors. Example 6-char cycle: mag-heart-suit, red-heart-suit, mag-white-heart, red-heart-suit, mag-heart-suit, red-white-heart. The fill itself should visually read as "hearts" not "colored blocks."
- IMPORTANT: Each fill char MUST be 1 display col. Test with `disp_len()`. Stick to `♡` (U+2661) and `♥` (U+2665) which are reliably 1 col. Do NOT use emoji hearts like U+2764 FE0F (which can be 2 cols).
- Add `decoration` with 2 alternating Frames. Above: a heartbeat/pulse line like `  ~  ^  ~     ^  ~  ^     ~` alternating with a shifted version. Below: scattered small hearts `♡` spaced out. Creates a pulse-monitor line above.
- Add `completion_decoration` with dense heart pattern.
- emoji sprite: `♥` (1 col) alternating frames (both same for consistent width). Completion: sparkling heart emoji.
- unicode: Same fill, `<3` sprite alternating, `<3!` completion.
- ascii: Fill of alternating `<` and `3` chars (reads as partial hearts), `<3` sprite, `<3!` completion, simple `-` and `^` decoration.

**Rework wizard (more fill variety + magical decoration):**
Rewrite `nyanbar/themes/_wizard.py`:
- emoji fill: Expand to 10+ colorful magical symbols. Add more to existing set: keep the 6 (star, asterisk, diamond, hollow-star, snowflake, comet) and add 4+ more like `\u2721` (Star of David, 1 col), `\u2740` (floral, check width!), `\u2302` (house/hat, 1 col -- whimsical), `\u2234` (therefore dots, 1 col). Use magenta/cyan/blue/yellow ANSI colors. EVERY char must be verified 1 display col.
- Add `decoration` with 2+ alternating Frames. Above: floating sparkles `\u2726`, `\u2605`, `\u00b7` spaced irregularly like "   \u2726       \u2605           \u00b7       \u2726". Below: same concept, different positions. Alternate between frames for twinkling effect.
- Add `completion_decoration` with dense magical sparkle pattern.
- Keep wizard emoji sprite (U+1F9D9). Keep completion U+1F9D9 + sparkles.
- Unicode: same fill, `*>` / `~>` sprites, sparkle decoration using `*` and `.`.
- ASCII: expanded ASCII fill (`*~+.^~*+.~`), same sprites, `*` and `.` decoration.

**Rework rocket (space decoration + dynamic exhaust):**
Rewrite `nyanbar/themes/_rocket.py`:
- emoji fill: More dynamic exhaust trail. Use 6-char cycle: red full-block, yellow full-block, orange half-block, red dark-shade, yellow full-block, red full-block. Mix in `\u2591` (light shade) and `\u2592` (medium shade) for exhaust texture.
- Add `decoration` with 2 alternating Frames. Above: stars and space debris `\u2605  \u00b7       \u2726        \u00b7  \u2605`. Below: exhaust particles `\u2022    \u00b7        \u2022   \u00b7`. Alternate for parallax-like starfield effect.
- Add `completion_decoration` with dense star celebration pattern.
- Keep rocket emoji sprite (U+1F680). Completion: rocket + star.
- Unicode: same fill, `|=>` / `]=>` sprites, `*` and `.` decoration.
- ASCII: `~` and `=` fill, `=>` sprite, `*` and `.` decoration.

**Decoration pattern guidelines (applies to all 4 reworks):**
- Each decoration Frame must have exactly 2 lines: `lines[0]` = above bar, `lines[1]` = below bar.
- Decoration strings can be any length; the engine pads them to ncols. Keep them around 50-60 chars with scattered symbols.
- Use 2 alternating decoration frames (like nyan) to create twinkling/animation.
- completion_decoration is a single Frame (not a tuple).
- ASCII tier decorations should use only ASCII chars (`.`, `*`, `~`, `^`, etc.).
- Unicode tier: can use unicode symbols but NO ANSI color codes.
- Emoji tier: can use unicode symbols WITH ANSI color codes.

**Validation:** After writing each theme file:
- Run `.venv/bin/python -c "from nyanbar.themes._fire import _create; a = _create('emoji'); print(a.decoration is not None, len(a.bar_fill))"` (adapt per theme) to sanity-check.
  </action>
  <verify>
```bash
# Confirm pac_man deleted
test ! -f nyanbar/themes/_pac_man.py && echo "pac_man deleted"

# Confirm __init__.py has no pac_man
! grep -q pac_man nyanbar/themes/__init__.py && echo "pac_man removed from init"

# Confirm all 4 reworked themes have decoration
.venv/bin/python -c "
from nyanbar.registry import get_theme
for name in ('fire', 'heartbeat', 'wizard', 'rocket'):
    a = get_theme(name, 'emoji')
    assert a.decoration is not None, f'{name} missing decoration'
    assert a.completion_decoration is not None, f'{name} missing completion_decoration'
    assert len(a.bar_fill) >= 3, f'{name} bar_fill too short'
    print(f'{name}: OK (decoration={len(a.decoration)} frames, fill={len(a.bar_fill)} chars)')
"

# Verify heartbeat fill uses heart chars (not generic blocks)
.venv/bin/python -c "
from nyanbar.registry import get_theme
a = get_theme('heartbeat', 'emoji')
fill_str = ''.join(c.replace('\033[35m','').replace('\033[31m','').replace('\033[0m','') for c in a.bar_fill)
assert '\u2665' in fill_str or '\u2661' in fill_str, f'heartbeat fill has no hearts: {a.bar_fill}'
print('heartbeat fill uses hearts: OK')
"

# Verify wizard has 10+ fill chars
.venv/bin/python -c "
from nyanbar.registry import get_theme
a = get_theme('wizard', 'emoji')
assert len(a.bar_fill) >= 10, f'wizard fill only {len(a.bar_fill)} chars'
print(f'wizard fill: {len(a.bar_fill)} chars OK')
"
```
  </verify>
  <done>pac_man deleted. fire/heartbeat/wizard/rocket each have decoration (2 alternating frames), completion_decoration, and enriched bar_fill. heartbeat uses heart unicode chars. wizard has 10+ magical symbols.</done>
</task>

<task type="auto">
  <name>Task 2: Create 6 new themes -- train, garden, lightning, candy, aurora, coffee</name>
  <files>
    nyanbar/themes/_train.py
    nyanbar/themes/_garden.py
    nyanbar/themes/_lightning.py
    nyanbar/themes/_candy.py
    nyanbar/themes/_aurora.py
    nyanbar/themes/_coffee.py
    nyanbar/themes/__init__.py
  </files>
  <action>
Create 6 new theme files following the exact pattern of existing themes (see _nyan.py as gold standard). Each theme MUST have:
- 3-tier factory: `_create(tier) -> Animation` dispatching to `_emoji()`, `_unicode()`, `_ascii()`
- `bar_fill`: tuple of 1-display-col strings (MUST verify each char is 1 col -- no emoji in fill)
- `frames`: tuple of 2+ Frame objects (single-line sprites), consistent display_width across frames
- `completion_frame`: Frame shown at 100%
- `register_theme("name", _create)` at module bottom
- At least 3 of the 6 should have `decoration` and `completion_decoration`

**1. train (`_train.py`) -- WITH decoration:**
- Concept: Steam engine chugging along railroad tracks, steam billowing.
- emoji fill: Brown/gray ANSI blocks for railroad ties/tracks. 6-char cycle mixing `\u2588` (full block) in dark ANSI colors (brown=`\033[33m` darker, gray=`\033[90m`).
- emoji sprite: train emoji `\U0001f682` (locomotive, 2 cols). Both frames same. Completion: `\U0001f682\u2605` (train + star).
- decoration: Steam puffs above (`.` `\u00b0` `\u2022` scattered), track texture below (`=` `-` `+`). 2 alternating frames.
- completion_decoration: Arrival celebration pattern.
- unicode: Same fill, `[TTT]` / `[===]` sprite (5 cols each), `[TTT]*` completion. `.` and `o` steam decoration.
- ascii: `=` and `-` fill, `[TTT]` sprite, `[TTT]*` completion. `.` and `o` decoration.

**2. garden (`_garden.py`) -- WITH decoration:**
- Concept: Growing garden with flowers and leaves filling the bar.
- emoji fill: Green/yellow/magenta ANSI symbols. Use leaf/plant 1-col chars: `\u2766` (floral heart, 1 col), `\u2740` -- VERIFY WIDTH, if not 1 col use `\u273f` or stick to `*` in green. Safer: use `\u2022` (bullet) in green, `\u2605` in yellow, `\u2666` in magenta. 6-char cycle alternating greens and flower colors.
- emoji sprite: sunflower emoji `\U0001f33b` (2 cols). Completion: `\U0001f33b\u2728`.
- decoration: Butterflies/petals above, grass/soil below. Use `.` `\u00b7` `~` scattered. 2 alternating frames.
- completion_decoration: Blooming garden pattern.
- unicode: Green ANSI symbols, `@` / `*` sprite (flower shapes), `@!` completion. `.` `~` decoration.
- ascii: `*` `.` `~` `o` fill, `@` sprite, `@!` completion. `.` `~` decoration.

**3. lightning (`_lightning.py`) -- WITH decoration:**
- Concept: Electric bolt charging across the bar.
- emoji fill: Blue/cyan/white ANSI blocks creating electric crackle. 6-char cycle: cyan full-block, blue full-block, white full-block, cyan dark-shade, blue full-block, white dark-shade.
- emoji sprite: lightning bolt `\u26a1` (1 col -- verify! If 2 cols, use `\u2607` or text-art). Completion: `\u26a1\u2605`.
- IMPORTANT: Verify `\u26a1` display width. If it's 2 cols in your testing, use the text-art `/>` for emoji tier too, or find a 1-col alternative.
- decoration: Electric sparks above (`\u00b7` `.` `\u2022` in cyan/white ANSI scattered), ground strike below. 2 alternating frames for crackling effect.
- completion_decoration: Dense electric pattern.
- unicode: Same fill, `/>` / `/>` sprite, `/>!` completion. `.` `*` decoration.
- ascii: `#` `=` fill, `/>` sprite, `/>!` completion. `.` `*` decoration.

**4. candy (`_candy.py`) -- no decoration (simple sweet theme):**
- Concept: Colorful candy trail.
- emoji fill: Pink/cyan/yellow/green ANSI symbols. Use `\u2022` (bullet), `\u2666` (diamond), `\u25cf` (circle, 1 col -- verify!) in candy colors. 6-char cycle.
- emoji sprite: candy emoji `\U0001f36c` (2 cols). Completion: `\U0001f36c\u2605`.
- NO decoration (keep it simple -- not every theme needs it).
- unicode: Same fill, `(o)` / `{o}` sprite, `(o)!` completion.
- ascii: `o` `.` `*` fill, `(o)` sprite, `(o)!` completion.

**5. aurora (`_aurora.py`) -- WITH decoration:**
- Concept: Northern lights shimmering across the sky.
- emoji fill: Green/cyan/magenta/blue ANSI blocks for aurora color waves. 8-char cycle using full blocks `\u2588` in green, cyan, blue, magenta ANSI, creating a sweeping color gradient.
- emoji sprite: star emoji `\u2b50` (1 col -- verify! if 2 cols use `\u2605` which is reliably 1 col). Safest: use `\u2605` in bright white ANSI.
- decoration: Shimmering light wisps above (`\u2605` `.` `\u00b7` `\u2726` scattered in green/cyan ANSI). Dark sky dots below (`\u00b7` `.`). 2 alternating frames for shimmer.
- completion_decoration: Full aurora display.
- unicode: Same fill, `*` sprite, `*!` completion. `.` `*` decoration.
- ascii: `#` `=` `~` fill, `*` sprite, `*!` completion. `.` `~` decoration.

**6. coffee (`_coffee.py`) -- no decoration (cozy simple theme):**
- Concept: Coffee brewing, warm brown tones.
- emoji fill: Brown/dark-yellow ANSI blocks. Use `\u2588` in `\033[33m` (yellow/brown) and `\033[90m` (dark gray). 4-char cycle for espresso crema look.
- emoji sprite: coffee emoji `\u2615` (1 col -- verify! widely supported, should be 1 col. If 2 cols, use text-art). Completion: `\u2615\u2605`.
- NO decoration (simple cozy theme).
- unicode: Same fill, `c[_]` sprite (4 cols, both frames), `c[_]*` completion.
- ascii: `#` fill, `c[_]` sprite, `c[_]*` completion.

**CRITICAL width constraints:**
- Every `bar_fill` char MUST be 1 display col (per `build_themed_fill` contract). Test each with `disp_len()`.
- All frames within a theme MUST have identical `display_width`. Both sprite frames must use same-width strings.
- Emoji that are 2 display cols (like `\U0001f682`, `\U0001f33b`, `\U0001f36c`) are fine for SPRITES only, not for fill chars.
- After creating each file, validate with:
  ```python
  .venv/bin/python -c "
  from nyanbar.utils import disp_len
  from nyanbar.themes._THEMENAME import _create
  a = _create('emoji')
  for c in a.bar_fill:
      assert disp_len(c) == 1, f'fill char {repr(c)} is {disp_len(c)} cols'
  widths = {f.display_width for f in a.frames}
  assert len(widths) == 1, f'inconsistent frame widths: {widths}'
  print('OK')
  "
  ```

**Add imports to `__init__.py`:**
After ALL 6 files created, add these imports to `nyanbar/themes/__init__.py` (which should already have pac_man removed from Task 1):
```python
from . import _train         # noqa: F401
from . import _garden        # noqa: F401
from . import _lightning     # noqa: F401
from . import _candy         # noqa: F401
from . import _aurora        # noqa: F401
from . import _coffee        # noqa: F401
```
Keep alphabetical order in the imports list.
  </action>
  <verify>
```bash
# Verify all 6 new themes register and have required fields
.venv/bin/python -c "
from nyanbar.registry import get_theme, list_themes
from nyanbar.utils import disp_len
new_themes = ('train', 'garden', 'lightning', 'candy', 'aurora', 'coffee')
all_t = list_themes()
print(f'Total themes: {len(all_t)}')
assert len(all_t) == 23, f'Expected 23, got {len(all_t)}: {all_t}'
for name in new_themes:
    assert name in all_t, f'{name} not registered'
    for tier in ('emoji', 'unicode', 'ascii'):
        a = get_theme(name, tier)
        assert a.bar_fill is not None, f'{name}/{tier} missing bar_fill'
        assert a.frame_count >= 2, f'{name}/{tier} needs 2+ frames'
        assert a.completion_frame is not None, f'{name}/{tier} missing completion_frame'
        # Verify fill char widths
        for c in a.bar_fill:
            w = disp_len(c)
            assert w == 1, f'{name}/{tier} fill char {repr(c)} width={w}'
        # Verify frame width consistency
        widths = {f.display_width for f in a.frames}
        assert len(widths) == 1, f'{name}/{tier} inconsistent widths: {widths}'
    print(f'{name}: OK (all 3 tiers)')

# Verify decoration on themes that should have it
for name in ('train', 'garden', 'lightning', 'aurora'):
    a = get_theme(name, 'emoji')
    assert a.decoration is not None, f'{name} should have decoration'
    assert a.completion_decoration is not None, f'{name} should have completion_decoration'
    print(f'{name}: decoration OK')
print('All 6 new themes validated.')
"
```
  </verify>
  <done>6 new themes created (train, garden, lightning, candy, aurora, coffee). All register successfully, have bar_fill with 1-col chars, consistent frame widths, completion frames, and at least 4 have decoration. Total theme count is 23.</done>
</task>

<task type="auto">
  <name>Task 3: Update tests and demo, run full validation</name>
  <files>
    tests/test_themes.py
    demo.py
  </files>
  <action>
**Update tests/test_themes.py:**

1. Replace the `ALL_THEMES` list (line 27-31) with the new 23-theme list. Remove `"pac_man"`, add `"aurora"`, `"candy"`, `"coffee"`, `"garden"`, `"lightning"`, `"train"`. Keep alphabetical order:
```python
ALL_THEMES = [
    "aurora", "candy", "coffee", "construction", "deal_with_it", "disco",
    "finger_guns", "fire", "garden", "heartbeat", "lenny", "lightning",
    "mario", "matrix", "nyan", "ocean", "rocket", "shrug", "snake",
    "table_flip", "train", "wizard", "zen",
]
```

2. Delete `test_pac_man_completion_has_ghost` (around line 215-219).

3. Add new theme-specific completion tests for the 6 new themes:
```python
def test_train_completion_has_star() -> None:
    anim = get_theme("train", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star

def test_garden_completion_has_sparkles() -> None:
    anim = get_theme("garden", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2728" in comp  # sparkles

def test_lightning_completion_has_star() -> None:
    anim = get_theme("lightning", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star

def test_candy_completion_has_star() -> None:
    anim = get_theme("candy", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star

def test_aurora_completion_has_star() -> None:
    anim = get_theme("aurora", "emoji")
    assert anim.completion_frame is not None

def test_coffee_completion_has_star() -> None:
    anim = get_theme("coffee", "emoji")
    assert anim.completion_frame is not None
    comp = anim.completion_frame.lines[0]
    assert "\u2605" in comp  # star
```
Adjust the assertions to match whatever completion sprites you actually used in Task 2. The key is that each new theme has a specific completion test.

4. Add decoration tests for the 4 reworked themes (fire, heartbeat, wizard, rocket) -- similar to `test_nyan_has_decoration`:
```python
@pytest.mark.parametrize("theme", ["fire", "heartbeat", "wizard", "rocket"])
@pytest.mark.parametrize("tier", TIERS)
def test_reworked_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None
```

5. Add decoration tests for the new decorated themes:
```python
@pytest.mark.parametrize("theme", ["train", "garden", "lightning", "aurora"])
@pytest.mark.parametrize("tier", TIERS)
def test_new_decorated_themes_have_decoration(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    assert anim.decoration is not None
    assert anim.completion_decoration is not None
```

6. Add a test that all decorated themes render 3 lines:
```python
DECORATED_THEMES = [
    "aurora", "fire", "garden", "heartbeat", "lightning", "nyan",
    "rocket", "train", "wizard",
]

@pytest.mark.parametrize("theme", DECORATED_THEMES)
@pytest.mark.parametrize("tier", TIERS)
def test_decorated_themes_render_3_lines(theme: str, tier: str) -> None:
    anim = get_theme(theme, tier)
    stats_left = format_stats_left(50, 100)
    stats_right = format_stats_right(50, 100, 5.0, 10.0)
    lines = render_themed_bar(anim, 0.5, WIDTH, 0.0, stats_left, stats_right)
    assert len(lines) == 3, f"{theme}/{tier} should render 3 lines, got {len(lines)}"
```

**Update demo.py:**
Remove the entire indeterminate section (lines 17-32). Keep the dynamic theme iteration. The file should be:
```python
"""Visual demo of all nyanbar themes."""
import time
from nyanbar import tqdm
from nyanbar.registry import list_themes

THEMES = list_themes()
N = 80
DELAY = 0.02

for theme in THEMES:
    print(f"\n  === {theme} ===\n")
    for _ in tqdm(range(N), theme=theme):
        time.sleep(DELAY)
    time.sleep(0.5)

print()
```

**Run full test suite:**
```bash
.venv/bin/python -m pytest tests/ -x -q
```
All tests must pass. If any fail, debug and fix the offending theme file(s).

**Run mypy:**
```bash
.venv/bin/python -m mypy nyanbar/ --strict
```
Must pass with no errors.
  </action>
  <verify>
```bash
# Full test suite
.venv/bin/python -m pytest tests/ -x -q

# Type checking
.venv/bin/python -m mypy nyanbar/ --strict

# Verify theme count
.venv/bin/python -c "from nyanbar.registry import list_themes; t = list_themes(); print(f'{len(t)} themes: {t}'); assert len(t) == 23"

# Verify pac_man is completely gone
! grep -rq pac_man nyanbar/ tests/ demo.py && echo "pac_man completely removed"

# Quick smoke test of demo (non-visual, just confirm no crash)
timeout 5 .venv/bin/python -c "
from nyanbar.registry import list_themes, get_theme
from nyanbar.engine import render_themed_bar
from nyanbar.formatters import format_stats_left, format_stats_right
for name in list_themes():
    for tier in ('emoji', 'unicode', 'ascii'):
        a = get_theme(name, tier)
        sl = format_stats_left(50, 100)
        sr = format_stats_right(50, 100, 5.0, 10.0)
        lines = render_themed_bar(a, 0.5, 80, 0.0, sl, sr)
        assert len(lines) >= 1
print('All 23 themes render successfully across all tiers.')
" || echo "FAILED"
```
  </verify>
  <done>ALL_THEMES has 23 entries. pac_man test removed. 6 new completion tests added. Decoration tests for reworked + new themes pass. Demo has no indeterminate section. Full pytest passes. mypy --strict passes. All 23 themes render across all 3 tiers without errors.</done>
</task>

</tasks>

<verification>
1. `test ! -f nyanbar/themes/_pac_man.py` -- pac_man file deleted
2. `.venv/bin/python -m pytest tests/ -x -q` -- all tests pass
3. `.venv/bin/python -m mypy nyanbar/ --strict` -- no type errors
4. `.venv/bin/python -c "from nyanbar.registry import list_themes; assert len(list_themes()) == 23"` -- 23 themes
5. `! grep -rq pac_man nyanbar/ tests/ demo.py` -- pac_man fully removed
6. `.venv/bin/python -c "from nyanbar.registry import get_theme; [get_theme(n,'emoji') for n in ('fire','heartbeat','wizard','rocket') if get_theme(n,'emoji').decoration is None]"` -- reworked themes have decoration
</verification>

<success_criteria>
- 23 themes total (17 existing minus pac_man + 6 new)
- fire, heartbeat, wizard, rocket all have decoration + completion_decoration
- heartbeat fill uses heart unicode characters, not generic colored blocks
- wizard has 10+ fill characters for variety
- 6 new themes (train, garden, lightning, candy, aurora, coffee) work across all 3 tiers
- At least 4 new themes have decoration (train, garden, lightning, aurora)
- All bar_fill chars are 1 display col
- All frame widths consistent within each theme
- pytest passes, mypy --strict passes
- demo.py iterates all themes dynamically, no indeterminate section
</success_criteria>

<output>
After completion, create `.planning/quick/3-cut-pacman-rework-fire-heartbeat-wizard-/3-SUMMARY.md`
</output>
