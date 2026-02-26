# Phase 2: Core Integration - Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Standalone NyanBar class with tqdm-compatible API, single-line rendering, stats display, all fallback paths, and terminal cleanup. Users can `from nyanbar import tqdm` and get an animated progress bar — zero dependencies, no tqdm import.

Wander/Chase indeterminate animation modes are deferred to Phase 3 (themes). For Phase 2, `total=None` uses tqdm-style text output only (count + rate + elapsed, no animation bar).

</domain>

<decisions>
## Implementation Decisions

### Stats Display Format
- Match tqdm's exact format string: `  0%|          | 0/100 [00:00<?, ?it/s]`
- Stats appear on the same line as the animation, to the right
- Rate/ETA use exponential moving average (EMA) smoothing with `smoothing=0.3` default — stable, not jumpy
- `set_description()` and `set_postfix()` match tqdm behavior exactly: desc= prefix, postfix appends key=value pairs
- `unit_scale=True` auto-formats with SI suffixes (k, M, G, T)
- `total=None` (indeterminate): no bar, just count + rate + elapsed like tqdm: `1000it [00:05, 200it/s]`

### Plain Text Fallback
- tqdm-style text bar: `50%|#####     | 50/100 [00:05<00:05, 10it/s]`
- Uses `\r` carriage return to overwrite in-place when terminal supports it; falls through to newlines only when truly piped
- Triggers silently — no warning or stderr notice when falling back
- Fallback conditions (from Phase 1 context): non-TTY, piped output, TERM=dumb, terminal width < 30 columns

### tqdm API Surface
- Full instance API: `__iter__`, `__enter__`/`__exit__`, `update()`, `close()`, `set_description()`, `set_postfix()`, `set_postfix_str()`, `write()`
- `tqdm.write()` class/static method supported (clears bar, prints, redraws)
- `tqdm.pandas()` NOT supported — out of scope
- `bar_format=` silently accepted but ignored (no format string parser)
- Unknown kwargs silently accepted via `**kwargs` — maximum compatibility, scripts just work
- All display kwargs honored: `desc=`, `unit=`, `unit_scale=`, `leave=`, `disable=`, `file=`, `ncols=`, `mininterval=`, `position=`
- `trange(n)` works identically to `tqdm(range(n))`

### Refresh Throttling
- Match tqdm's mininterval/maxinterval system: `mininterval=0.1s` (10Hz cap), `maxinterval=10s` (force redraw if stalled)
- Dynamic miniters with auto-tuning — critical for tight loops (millions of iterations/sec) to avoid write overhead
- Animation frame rate decoupled from stats refresh rate
- Background daemon thread for animation ticks at theme FPS (e.g., 12Hz)
- **Thread simplicity constraint:** daemon thread ONLY ticks frame counter and calls render. All state updates (n, rate, etc.) happen in main thread with a lock. No thread pools, no async, no queues.
- Thread dies automatically via daemon flag if main thread crashes

### Claude's Discretion
- Internal NyanBar class architecture (method decomposition, private helpers)
- Exact miniters auto-tuning algorithm
- Lock granularity for thread safety
- How animation thread lifecycle integrates with `__enter__`/`__exit__`
- Stats string formatting implementation details

</decisions>

<specifics>
## Specific Ideas

- From Phase 1 context: "We want to only disrupt a few lines at the top of a file and nothing else, being very easy to remove"
- Usage pattern: `import nyanbar; nyanbar.config(animation="cat")` at top, then `from nyanbar import tqdm` everywhere
- `from nyanbar import tqdm; list(tqdm(range(100)))` must work as the simplest case
- Removal story: swap import back to `from tqdm import tqdm`, remove `nyanbar.config()` lines, done

</specifics>

<deferred>
## Deferred Ideas

- Wander mode (rate-proportional sprite movement for `total=None`) — Phase 3
- Chase mode (two sprites, cat chases mouse/yarn ball for `total=None`) — Phase 3
- Frustrated worker emoji / table flip Easter eggs (e.g., `(╯°□°)╯︵ ┻━┻`, `ಠ_ಠ`, `(ง'̀-'́)ง`) — future phase or theme personality
- `tqdm.pandas()` integration — out of scope for v1

</deferred>

---

*Phase: 02-core-integration*
*Context gathered: 2026-02-25*
