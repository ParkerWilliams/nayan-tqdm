# Pitfalls Research

**Domain:** Animated terminal progress bar library (tqdm subclass, Python)
**Researched:** 2026-02-25
**Confidence:** HIGH (tqdm source code read directly from installed package; pitfalls derived from internal mechanics, not training data alone)

---

## Critical Pitfalls

### Pitfall 1: Forgetting the `display(msg='', pos=pos)` Contract in `close()`

**What goes wrong:**
When the user's iteration ends (normally or via exception), tqdm calls `close()`, which calls `display()` with `msg=''` (to erase) or `display(pos=0)` (to leave the final state). If `NyanBar.display()` ignores the `msg` argument and always renders animation, the final-state behavior is broken: bars that should disappear (leave=False) will leave animation artifacts; bars that should display a final summary will show an animation frame instead of the completion state.

**Why it happens:**
Developers focus on the happy-path "render animation" case and write `display()` to unconditionally call the animation renderer. They don't check `msg is None` (normal update) vs `msg == ''` (clear/erase) vs `msg` is a non-empty string (custom message).

**How to avoid:**
Override `display()` with explicit message-contract handling:
```python
def display(self, msg=None, pos=None):
    if msg == '':
        # tqdm wants to erase the bar (leave=False) — clear all animation lines
        self._clear_animation_lines()
        return super().display(msg=msg, pos=pos)
    if msg is not None:
        # Custom message passed — render it as plain text, not animation
        return super().display(msg=msg, pos=pos)
    # msg is None — normal animation update path
    self._render_animation(pos=pos)
```

**Warning signs:**
- `leave=False` bars leave residual animation lines after iteration ends
- Exception handling leaves dangling ANSI escape sequences in the terminal
- The completion frame never shows — it's being overwritten by a plain `close()` render
- Test with `with NyanBar(..., leave=False) as t: pass` and check the terminal is clean

**Phase to address:** Phase implementing `core.py` (NyanBar class). Must be validated in `test_compat.py` with `leave=True` and `leave=False` cases before any multi-line work begins.

---

### Pitfall 2: Multi-line Height Mismatch Corrupts Terminal State

**What goes wrong:**
Multi-line animations (nyan, fish, rocket) track `_prev_height` to know how many lines to move the cursor up before overwriting. If `_prev_height` is ever wrong — even by 1 — every subsequent render prints to the wrong row. Over time, output "drifts" upward or downward, corrupting both the bar and anything printed to stdout/stderr below it.

**Why it happens:**
Height can become inconsistent in four places: (1) first render (prev_height=0, need to emit newlines not cursor-up), (2) theme switch at runtime changes line count, (3) terminal resize changes effective line count, (4) fallback path (when terminal is too narrow) emits 1 line but prev_height was set for 3. Any one of these paths diverging from the tracking variable causes permanent corruption.

**How to avoid:**
- Initialize `_prev_height = 0` in `NyanBar.__init__()`, not lazily
- In `ANSIRenderer.render_frame()`, always derive the actual height from `len(lines)` after rendering, and return it so the caller can update `_prev_height` atomically
- On fallback activation (narrow terminal, non-TTY), explicitly reset `_prev_height = 0`
- On theme switch (if supported), reset `_prev_height = 0`
- Test the first render path separately: it must emit `\n * (height - 1)` downward, not `\033[{n}A` upward (nothing to move up from on first render)

**Warning signs:**
- Output that slowly "climbs" or "descends" the terminal over many iterations
- A second bar appearing at a different vertical offset than expected
- The stats line and animation lines de-sync (stats on row 5, animation on row 3)
- Terminal looks correct at 50% but corrupted at completion

**Phase to address:** Phase implementing `renderer.py` (ANSIRenderer). All multi-line cursor math must be in a single `render_frame()` method so it cannot be duplicated or drift independently. Do not track height in `core.py` AND `renderer.py` simultaneously.

---

### Pitfall 3: Not Guarding Against the `position > 0` (Nested Bar) Case

**What goes wrong:**
tqdm's nested bar support uses `self.pos` to indicate vertical offset. The `display()` method calls `self.moveto(pos)`, which writes `\n * pos` then `\033[A * pos` to reposition the cursor. When NyanBar then emits its own cursor-up sequences for multi-line animation, the two cursor movements conflict. The result is bars that overwrite each other, or a bar that moves to the wrong row and permanently corrupts the nested layout.

**Why it happens:**
tqdm's `moveto()` assumes the bar is a single line. Adding multi-line rendering on top of `moveto()` creates double-cursor-movement: tqdm moves down to the bar's position, NyanBar moves up to overwrite previous animation lines, and the net cursor position after display() returns is wrong.

**How to avoid:**
In `NyanBar.display()`, check `abs(self.pos) > 0` and disable multi-line mode for nested bars:
```python
def display(self, msg=None, pos=None):
    if abs(self.pos) > 0:
        # Nested bar: disable multi-line to avoid cursor conflict with tqdm's moveto()
        return self._render_single_line(pos=pos)
    ...
```
The project CLAUDE.md already notes this. Enforce it as a property (`self._multiline_allowed`) set during `__init__` and re-checked each call to `display()`.

**Warning signs:**
- `tqdm.trange(outer, desc='outer')` with `NyanBar(inner, desc='inner')` produces garbled output
- The inner bar overwrites the outer bar
- Passing `position=1` to a NyanBar leaves a permanent extra blank line

**Phase to address:** Phase implementing `core.py`. Add a `test_compat.py` test that runs two simultaneous NyanBar instances (one nested) before adding any multi-line theme.

---

### Pitfall 4: Unicode Width Miscalculation Breaks Column Arithmetic

**What goes wrong:**
Sprite frames containing wide Unicode characters (emoji: `🚀`, `🔥`, `✨`; CJK characters; box-drawing ligatures) occupy 2 terminal columns per character but count as 1 in Python's `len()`. If column arithmetic uses `len(line)` instead of terminal-display-width, the animation overflows the terminal, wraps to a second line mid-frame, and destroys the multi-line height tracking.

**Why it happens:**
Python's built-in `len()` counts Unicode code points. Terminal emulators measure display columns using East Asian Width rules (W/F = 2 cols, everything else = 1 col). The mismatch is invisible in testing until a sprite uses a wide character.

**How to avoid:**
Use tqdm's own `disp_len()` from `tqdm.utils` for all terminal-width calculations:
```python
from tqdm.utils import disp_len
# disp_len strips ANSI codes then measures East Asian Width per character
available_cols = terminal_width - disp_len(stats_str)
```
For the `Frame.width` field (auto-calculated), compute it using `disp_len(line)` not `len(line)`. Apply the same logic to sprite positioning math.

**Warning signs:**
- Rocket or nyan theme wraps to an extra line on terminals with emoji support
- Line-width assertions in `test_themes.py` pass (using `len()`) but visual output overflows
- Cat sprite jumps to row 2 mid-animation on terminals with wide-char rendering

**Phase to address:** Phase implementing `themes/base.py` (Frame dataclass). The `Frame.width` auto-calculation must use `disp_len()` from the start. If this is added to `base.py` after themes are already written, every theme's frame widths need re-verification.

---

### Pitfall 5: ANSI Color Codes Left Open After Fallback or Close

**What goes wrong:**
ANSI color sequences must be closed with a reset (`\033[0m`). If the animation code adds color (e.g., rainbow trail for nyan theme) but the reset is lost — because an exception interrupted rendering, or the fallback path cleared lines without resetting, or `\r\033[K` (clear line) is emitted before the reset — the terminal stays in colored mode. Everything printed after the bar (stdout from user code, subsequent print statements, shell prompts) inherits the last color.

**Why it happens:**
ANSI clear-line (`\033[K`) erases the visible characters but does not reset SGR (Select Graphic Rendition) attributes. Developers assume clearing the line resets state; it does not. The color state is tied to the terminal's attribute registers, not the visible characters.

**How to avoid:**
- Always emit `\033[0m` as the last character of any colored line before `\r` or `\n`
- Use tqdm's `disp_trim()` from `tqdm.utils` when truncating colored strings — it appends `\033[0m` if ANSI sequences are present and truncation cut through them
- In `_clear_animation_lines()`, emit `\033[0m` before each `\r\033[K` sequence
- Add a test that captures stderr output after bar close and asserts it contains no open ANSI sequences (regex: `\033\[` with no following `\033\[0m`)

**Warning signs:**
- Shell prompt turns rainbow-colored after a nyan bar completes
- Test output from pytest is colored unexpectedly after a test uses NyanBar
- Piped output (`python script.py 2>&1 | cat`) contains raw ANSI sequences that bleed past the bar's last line

**Phase to address:** Phase implementing `renderer.py`. Add a reset-sequence checker to `test_renderer.py`. Must be addressed before nyan/fish/rocket themes since those are the first to use color.

---

### Pitfall 6: Rendering Performance Bottlenecking the Wrapped Iterator

**What goes wrong:**
The animation renderer is called on every `display()` invocation. If rendering is expensive — character-by-character string construction, repeated `shutil.get_terminal_size()` calls, per-frame regex operations, or synchronous `fp.flush()` calls — it adds latency to every iteration of the user's loop. For tight loops (millions of iterations), this can reduce throughput by 10x or more.

**Why it happens:**
Developers build themes by constructing strings character-by-character in Python (e.g., placing a sprite at position `int(progress * width)` via string concatenation in a loop). This is O(width) per render. Combined with `mininterval=0.1` default, this runs 10 times per second — fine individually, catastrophic under profiling.

**How to avoid:**
- Pre-compute all frame strings at theme load time. Frames that vary only by progress position should precompute the sprite-left-of-cursor and sprite-right-of-cursor padding as a lookup table indexed by integer position (0..width). Recompute only on terminal resize.
- Cache `shutil.get_terminal_size()` results; re-read only when `dynamic_ncols=True`
- Use `''.join([...])` not `s += char` for string building
- Never call `fp.flush()` more frequently than tqdm itself would (tqdm flushes inside `sp()`)
- Benchmark: `python -m cProfile -s cumtime` a tight loop of 100k iterations with NyanBar and assert rendering does not appear in top-5 cumulative time

**Warning signs:**
- Users report their script is "much slower" with nyanbar than tqdm
- `time.monotonic()` measurements inside `display()` show render time > 1ms
- Theme render function appears in cProfile output

**Phase to address:** Phase implementing animation themes (cat_walk first, then multi-line). Establish a render-time budget (<0.5ms per `display()` call) before implementing subsequent themes.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Use `len(line)` instead of `disp_len(line)` for width | Simpler code, no tqdm import in base.py | Every emoji-containing theme overflows terminal; width math is wrong for all wide chars | Never — use `disp_len()` from day one |
| Track `_prev_height` in both `core.py` and `renderer.py` | Feels natural at each layer | Two sources of truth drift apart; cursor corruption is intermittent and hard to reproduce | Never — single source in renderer |
| Skip `msg=''` / `msg=None` distinction in `display()` | Simpler override | `leave=False` bars corrupt terminal; tqdm's own `close()` logic is broken | Never for any shipped code |
| Hardcode `animation.fps = 8` inside `display()` | One less attribute access | Can't tune per-theme without code change; fish theme looks wrong at 8fps | Acceptable as MVP default if `Animation.fps` is still the public knob |
| Always call `shutil.get_terminal_size()` per render | Always current width | 10x slower per render on Linux (syscall) | Only for `dynamic_ncols=True` path |
| Skip completion frame in MVP | Fewer theme states to test | Cat never sits down; rocket never reaches space; feels unfinished at 100% | Acceptable to defer rocket/nyan completion frames; cat_walk completion is easy, do it |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| tqdm's `status_printer()` / `self.sp` | Calling `self.sp(line)` for each of N animation lines separately | `self.sp` is a single-line printer that tracks `last_len` to pad with spaces. For multi-line, write directly to `self.fp` using the pre-assembled escape sequence string |
| tqdm's `moveto()` | Calling `super().moveto(pos)` then emitting cursor-up for multi-line | `moveto()` assumes single-line. For multi-line, replace the entire cursor movement with a single compound escape sequence: cursor-up N + overwrite N lines |
| tqdm's `_lock` (TqdmDefaultWriteLock) | Writing to `self.fp` outside the lock | tqdm uses a per-class lock for thread safety. Multi-line output across multiple `fp.write()` calls is not atomic unless done inside `with self._lock:` |
| tqdm's `disable=True` early-exit | Not calling `super().__init__()` before checking disable | tqdm's `__init__` sets `self.disable` late; accessing animation attributes before `super().__init__()` completes will AttributeError |
| Python's `print()` during a NyanBar | `print()` writes to stdout; NyanBar writes to stderr — interleaved output corrupts layout | Document that users must use `tqdm.write()` (the class method) instead of `print()`. This is standard tqdm behavior, but warn explicitly in README |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Rebuilding full frame string on every `display()` call | `display()` takes >1ms; profiler shows string ops dominating | Pre-compute position-indexed frame table at `__init__` time; recompute only on resize | Any tight loop (>10k iterations/sec) |
| `shutil.get_terminal_size()` on every render | 2-3x slower on Linux; noticeable on macOS | Cache width at init; only refresh if `dynamic_ncols=True` | Always visible in profiler; becomes user-visible at >1k renders/sec |
| Calling `self.fp.flush()` explicitly | Doubles I/O syscalls | Trust tqdm's `sp()` to flush; only add explicit flush if the bar is not updating live | Any terminal with buffered I/O (common in CI) |
| Per-character star-twinkle computation (nyan theme) | Nyan render is 5x slower than cat_walk | Pre-compute star positions per frame in `Animation.frames`; don't compute at render time | Noticeable when nyan bar is used in a tight data processing loop |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Animation continues at 100% after iteration ends | Confusing — bar looks stuck; user doesn't know if the loop finished | Render the completion frame (cat sits, rocket in space) synchronously in `close()`, then let tqdm print the final `\n` |
| Stats line (ETA, rate) disappears in multi-line mode | Users lose the information they care most about (how fast, how long left) | Always reserve the bottom line for stats; animation occupies lines above it |
| No fallback when terminal is < 30 columns | Bar renders as garbage; lines overflow and wrap | Check width at every `display()` call; if below threshold, call `super().display()` immediately |
| Animation flickers noticeably at fast iteration rates | Looks broken; users think there's a bug | Respect `mininterval` (tqdm default 0.1s = max 10 fps); don't bypass tqdm's rate limiting |
| Theme set globally affects all NyanBar instances in process | User sets cat theme for one loop; all subsequent bars in libraries also use cat | `set_theme()` should set the per-instance default, not a process-global; use `_default_theme` as a fallback, not as a forced override |

---

## "Looks Done But Isn't" Checklist

- [ ] **leave=False**: Verify `NyanBar(..., leave=False)` leaves a clean terminal with no dangling escape sequences — not just that the bar disappears visually
- [ ] **Exception in loop body**: Wrap iteration in `try/finally` and raise an exception mid-loop. Verify `close()` is called, the terminal is clean, and subsequent `print()` statements appear at the correct position
- [ ] **Nested bars**: Run two NyanBar instances simultaneously (`position=0` and `position=1`) and verify neither overwrites the other
- [ ] **Piped output**: Run `python script.py 2>&1 | head -5` and verify the output is clean plain-text (no ANSI) and the process terminates (no hang waiting for terminal input that never comes)
- [ ] **No total**: `NyanBar(iterable)` where `len(iterable)` raises `TypeError` — verify animation still renders (in percentage-unknown mode) without crashing
- [ ] **Terminal resize mid-run**: Resize the terminal window while an animation is running. Verify the bar re-adapts and does not leave stale wide lines
- [ ] **Completion frame**: Verify that 100% progress actually triggers the completion frame, not just the last walk-cycle frame
- [ ] **ANSI color reset**: After any colored theme completes, `echo "test"` in the shell should appear in the default terminal color, not the last animation color

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| `_prev_height` tracking diverged, terminal corrupted | LOW | Add a `reset_cursor()` method that emits enough `\n` characters to scroll past corruption, then resets `_prev_height = 0`. Expose as `NyanBar.reset_display()`. |
| Color left open (terminal turned rainbow) | LOW | Add a `NyanBar.cleanup()` classmethod that emits `\033[0m\n` to stderr. Document that users can call it if they ctrl-C mid-animation. |
| Performance bottleneck discovered post-implementation | MEDIUM | Refactor `Animation.render()` to accept pre-indexed frame table. This is backward-compatible (the method signature doesn't change) but requires rewriting per-theme render logic. |
| Multi-line / nested conflict discovered after all themes are built | HIGH | Requires adding `_multiline_allowed` flag and two code paths in `display()`. All multi-line themes need single-line fallback frames added. Test suite needs nested-bar tests for every multi-line theme. |
| Unicode width miscalculation in `Frame.width` | MEDIUM | Rewrite `Frame.width` to use `disp_len()`. All existing themes need their explicit `width` values (if hardcoded) updated. Tests catch this if they check `disp_len(line) <= width` not `len(line) <= width`. |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| `display(msg='')` contract broken | Phase: Implement `core.py` | `test_compat.py`: `leave=True`, `leave=False`, exception-during-iteration test cases |
| Multi-line height mismatch | Phase: Implement `renderer.py` | `test_renderer.py`: first-render, N-line render, resize, and fallback path each verify `_prev_height` matches actual output line count |
| Nested bar cursor conflict | Phase: Implement `core.py` | `test_compat.py`: simultaneous NyanBar with `position=0` and `position=1` |
| Unicode width miscalculation | Phase: Implement `themes/base.py` | `test_themes.py`: assert `disp_len(line) <= frame.width` for every line in every frame of every theme |
| ANSI color left open | Phase: Implement `renderer.py` and color themes | `test_renderer.py`: regex-assert no open ANSI sequences remain after `render_frame()` completion |
| Rendering performance bottleneck | Phase: Implement `cat_walk.py` (first theme) | Benchmark test: 10k renders of cat_walk complete in <5 seconds total; no single render >0.5ms |
| `status_printer` / `sp` misuse | Phase: Implement `core.py` | `test_renderer.py`: verify all multi-line output uses `fp.write()` directly, not `sp()` for individual lines |

---

## Sources

- tqdm source code read directly: `/Users/prwilliams/Repos/GraphVerse/.venv/lib/python3.9/site-packages/tqdm/std.py` and `utils.py`
- tqdm `display()` method signature and `msg=None` vs `msg=''` contract: `std.py` lines 1464-1498
- tqdm `close()` multi-path logic (leave=True vs leave=False): `std.py` lines 1265-1308
- tqdm `moveto()` single-line cursor assumption: `std.py` lines 1441-1444
- tqdm `DisableOnWriteError` and `isatty()` disable path: `std.py` lines 973-974
- East Asian Width / `disp_len()` implementation: `utils.py` lines 374-383
- `disp_trim()` ANSI-reset-on-truncation: `utils.py` lines 386-399
- `_term_move_up()` Windows vs. Unix difference: `utils.py` line 371
- Project architecture and constraints: `/Users/prwilliams/Repos/nayan-tqdm/nayan-tqdm.md`

---
*Pitfalls research for: animated terminal progress bar library (nyanbar, tqdm subclass)*
*Researched: 2026-02-25*
