---
phase: 04-public-api-and-release
plan: 02
status: complete
started: 2026-02-25
completed: 2026-02-25
---

# Plan 04-02: Test reorganization into 4 domain files

## What was built
- Reorganized 14 test files into 4 domain-based test files + shared conftest.py
- Converted all class-based tests to plain pytest `test_*` functions with fixtures
- Test count increased from 452 to 456 (all pass in 0.53s)

## File mapping

| New file | Absorbed from |
|----------|---------------|
| `tests/conftest.py` | New shared fixtures + context managers |
| `tests/test_tqdm_compat.py` | test_core, test_integration, test_thread, test_formatters |
| `tests/test_renderer.py` | test_renderer, test_utils, test_engine |
| `tests/test_themes.py` | test_themes_cat, test_themes_nyan, test_themes_fish, test_themes_rocket, test_registry, test_models |
| `tests/test_fallbacks.py` | test_fallback, test_terminal |

## Key changes
- `conftest.py` provides: tty_terminal, non_tty_terminal, dumb_terminal, narrow_terminal, output_stream, mock_tty, mock_non_tty fixtures, plus utf8_locale/no_utf8_locale context managers
- All test classes eliminated -- every test is a plain `test_*` function
- test_themes.py uses `@pytest.mark.parametrize` over ALL_THEMES x TIERS x PROGRESS_LEVELS
- 14 old test files deleted after verification

## Verification
- 456 tests pass in 0.53s (was 452 in 0.66s)
- `grep -n "^class " tests/test_*.py` returns nothing (no classes)
- Only 4 test files + conftest.py remain
- mypy --strict still passes

## Key files
- **created**: `tests/conftest.py`, `tests/test_tqdm_compat.py`, `tests/test_themes.py`, `tests/test_fallbacks.py`
- **modified**: `tests/test_renderer.py` (rewritten to absorb test_utils + test_engine)
- **deleted**: 14 old test files

## Self-Check: PASSED
- [x] Only 4 test files + conftest.py exist
- [x] All tests are plain functions (no classes)
- [x] Test count 456 >= original 452
- [x] All tests pass in < 2 seconds
- [x] Coverage: tqdm API, renderer, 5 themes x 5 progress x 3 tiers, 3 fallback conditions, terminal detection
