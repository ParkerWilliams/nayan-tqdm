# Stack Research

**Domain:** Python animated terminal progress bar library (tqdm subclass)
**Researched:** 2026-02-25
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.10+ | Runtime language | `X \| Y` union syntax, `match` statements, structural pattern matching — all available; 3.10 is the oldest version still receiving security updates as of 2025; project explicitly requires it |
| tqdm | >=4.60, current: 4.67.3 | Base class to subclass | `display()` is the documented override point (tqdm itself says "Consider overloading this function when inheriting"); `format_dict` property exposes all stats cleanly; `status_printer`, `moveto`, `sp` are stable internals; 4.60+ has all the APIs nyanbar needs |
| Python stdlib: `shutil` | stdlib | Terminal width detection | `shutil.get_terminal_size()` is the standard, cross-platform way to get terminal columns/rows — no external dep needed |
| Python stdlib: `time` | stdlib | Wall-clock frame timing | `time.monotonic()` is the correct call for elapsed time (immune to system clock adjustments); decouples animation from iteration rate |
| Python stdlib: `dataclasses` | stdlib | `Frame` and `Animation` data types | `@dataclass` with `frozen=True` is idiomatic for immutable data containers; zero external dependency; available since Python 3.7 |
| Python stdlib: `os`, `sys` | stdlib | TTY and pipe detection | `os.isatty(sys.stderr.fileno())` / `sys.stderr.isatty()` is the canonical way to detect pipe/redirect; tqdm itself checks this in `__init__` |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| rich | >=13.0, current: 14.3.3 | Dev-only: test output formatting, console inspection | Use in dev environment only (per PROJECT.md constraint); useful for debugging ANSI output and theme development; NOT a runtime dependency |
| colorama | 0.4.6 | Windows ANSI escape code compatibility | Only if Windows support is a priority; on Windows, ANSI escape codes require `colorama.init()` or Windows 10+ VT100 mode; skip for v1 since macOS/Linux are primary targets — assess after initial release |
| wcwidth | 0.6.0 | Accurate Unicode display width calculation | Only if multi-byte Unicode characters (CJK, emoji) are used in themes; stdlib `len()` gives byte count, not display width; necessary if themes include wide characters like `🐱` or `🐟` |

### Development Tools

| Tool | Version | Purpose | Notes |
|------|---------|---------|-------|
| hatch | 1.16.4 | Project management, build, environments, publish | Single tool replaces pip+venv+build+twine; `pyproject.toml`-native; PEP 517/518 compliant; recommended by Python Packaging Authority (PyPA) for new projects; use `hatch run test`, `hatch build`, `hatch publish` |
| hatchling | 1.29.0 | Build backend (used by hatch) | The build backend that processes `pyproject.toml`; automatically included when using hatch |
| pytest | >=9.0, current: 9.0.2 | Test framework | Industry standard; parametrize decorators make animation frame testing clean; fixture system handles TTY mocking well |
| pytest-cov | 7.0.0 | Coverage reporting | Integrates with pytest via `--cov` flag; works with `coverage.py` 7.x |
| pytest-mock | 3.15.1 | Mocking in tests | Provides `mocker` fixture; cleaner than `unittest.mock.patch` decorators; needed to mock `sys.stderr.isatty()`, `shutil.get_terminal_size()`, `time.monotonic()` |
| coverage | 7.13.4 | Coverage measurement backend | Used by pytest-cov; track which branches of fallback logic are covered |
| ruff | 0.15.2 | Linting and formatting | Single tool replaces flake8 + isort + black; 10-100x faster than each individually; enforces style without blocking development |
| mypy | 1.19.1 | Static type checking | Catches type errors in the `display()` override signature and `Animation`/`Frame` dataclass usage; `--strict` mode recommended for a library |
| pre-commit | 4.5.1 | Git hook automation | Runs ruff and mypy on commit; catches issues before CI |
| uv | 0.10.6 | Fast pip replacement (optional) | Rust-based resolver; 10-100x faster than pip for dependency resolution; can replace pip in CI; optional but strongly recommended for faster developer iteration |
| build | 1.4.0 | PEP 517 build frontend (fallback) | Alternative to `hatch build` if hatch is not used; invoke with `python -m build` |
| twine | 6.2.0 | PyPI publishing (fallback) | Alternative to `hatch publish` if hatch is not used; validates wheel before upload |

## Installation

```bash
# Install hatch (project manager — replaces pip/venv/build/twine)
pip install hatch

# Initialize project (hatch creates the venv automatically)
hatch env create

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Lint and format
hatch run lint:all

# Build distribution
hatch build

# Publish to PyPI
hatch publish
```

```toml
# pyproject.toml (hatch-based)
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "nyanbar"
version = "0.1.0"
description = "Animated ASCII progress bars — drop-in tqdm replacement"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    "tqdm>=4.60",
]

[project.optional-dependencies]
dev = [
    "pytest>=9.0",
    "pytest-cov>=7.0",
    "pytest-mock>=3.15",
    "coverage>=7.0",
    "ruff>=0.15",
    "mypy>=1.19",
    "pre-commit>=4.5",
    "rich>=13.0",
]

[tool.hatch.envs.default]
dependencies = [
    "pytest>=9.0",
    "pytest-cov>=7.0",
    "pytest-mock>=3.15",
    "rich>=13.0",
]

[tool.hatch.envs.default.scripts]
test = "pytest {args}"
test-cov = "pytest --cov=nyanbar --cov-report=term-missing {args}"

[tool.hatch.envs.lint]
dependencies = ["ruff>=0.15", "mypy>=1.19"]

[tool.hatch.envs.lint.scripts]
all = ["ruff check . --fix", "ruff format .", "mypy src/nyanbar"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
strict = true
python_version = "3.10"
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| hatch | poetry | poetry is still widely used and mature, but its lock file approach is better suited for applications than libraries; hatch is better for libraries because it uses pyproject.toml natively without a separate lock file at publish time |
| hatch | setuptools + setup.py | Never for new projects; setup.py is legacy; setuptools still works but requires more boilerplate; use only if maintaining an existing setup.py project |
| ruff | black + flake8 + isort | If your team already has black configured and can't change; ruff is a strict superset of black's formatting, so migration is one-time |
| pytest | unittest | unittest is stdlib but verbose; pytest's parametrize decorator is essential for testing dozens of animation frames with clean output |
| mypy | pyright | pyright (from Microsoft) is technically faster and better at some inference patterns; choose pyright if VSCode is the primary editor and team prefers it; mypy is more portable as a CI tool |
| hatchling | flit | flit is simpler but less flexible; hatchling handles src layout, dynamic versioning, and custom hooks better |
| ANSI escape codes (stdlib) | curses | curses provides more control but is not available on Windows and requires terminal initialization; ANSI escape codes work in all modern terminals including macOS Terminal, iTerm2, Windows Terminal, and most CI environments; PROJECT.md explicitly chose ANSI |
| colorama (optional) | blessed / urwid | blessed and urwid are full terminal UI frameworks; far too heavy for nyanbar's scope; nyanbar needs only cursor movement and basic color, not a full TUI toolkit |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `curses` | Not available on Windows; requires `initscr()` which takes over the terminal; overkill for progress bar rendering; PROJECT.md explicitly ruled it out | ANSI escape codes via `\r`, `\033[A` (cursor up), `\033[K` (erase line) — these are sufficient and portable to all non-dumb terminals |
| `blessed` / `urwid` / `rich` as runtime deps | Full TUI toolkits add weight (rich is 500KB+); violates PROJECT.md's "zero extra deps beyond tqdm" constraint | stdlib ANSI sequences; rich is fine as a dev-only tool |
| `poetry` lock files committed for a library | poetry's `poetry.lock` is for applications, not libraries; committing it for a library forces downstream users into exact versions | Use `pyproject.toml` version ranges with hatch; let users resolve their own environments |
| `asyncio`-based animation loops | Adds complexity and requires the user's code to be async-aware; tqdm itself is synchronous; nyanbar's animation advances on `display()` calls triggered by tqdm's `update()` → wall-clock comparison is simpler and correct | `time.monotonic()` comparison inside `display()`: if `monotonic() - last_frame_t >= frame_duration` → advance frame |
| `threading.Timer` for frame ticks | Race conditions with tqdm's own thread lock (`_lock`); tqdm is not fully thread-safe across all operations; frame timing in a background thread can corrupt terminal state | Frame advancement on `display()` calls using wall-clock elapsed time — no background thread needed |
| `setup.py` / `setup.cfg` | Legacy packaging; no active development; not supported by modern build frontends without compatibility shims | `pyproject.toml` with hatchling |
| External asset files (PNG sprites, JSON theme files) | Adds packaging complexity; requires `importlib.resources` or `pkg_resources`; breaks in some zip-imported packages | Inline frame definitions as Python string constants in each theme module — per PROJECT.md decision |
| Python < 3.10 | `X \| Y` union syntax, structural pattern matching, and `match` statements are 3.10+ features; supporting 3.8/3.9 adds dead-weight compatibility shims | Require `python_requires = ">=3.10"` in pyproject.toml |

## Stack Patterns by Variant

**If Windows support is needed (v2+):**
- Add `colorama>=0.4.6` as a runtime dependency
- Call `colorama.init()` in `NyanBar.__init__()` when `sys.platform == "win32"`
- Because Windows versions before 10 1511 do not support ANSI escape codes in cmd.exe; colorama translates ANSI to Win32 console calls

**If Jupyter/notebook support is added (stretch goal):**
- Use `tqdm.notebook.tqdm_notebook` as an additional base class option
- Render CSS animations via `IPython.display.HTML` instead of ANSI
- Because Jupyter kernels capture stdout/stderr and ANSI sequences do not render in the browser

**If CI is GitHub Actions:**
- Use `hatch run test-cov` in the CI step
- Use `uv pip install` instead of `pip install` for faster dependency installation in CI
- GitHub Actions runners support ANSI colors when `FORCE_COLOR=1` or `--color=yes` is set

**If multi-Python version testing is needed:**
- Use `hatch` matrix environments: `[[envs.test.matrix]] python = ["3.10", "3.11", "3.12", "3.13"]`
- Because hatch manages multiple Python interpreters natively without tox or nox

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| tqdm>=4.60 | Python 3.10+ | tqdm 4.60 introduced the stable `format_dict` property used for subclass stats access; versions before 4.60 have subtly different internals |
| pytest>=9.0 | Python 3.10+ | pytest 9.x dropped Python 3.8 support; 9.0+ is required for modern fixture behavior |
| pytest-cov 7.x | pytest 9.x | pytest-cov 7.0 updated to support pytest's new Coverage plugin API; 6.x may work but 7.x is the tested combination |
| ruff 0.15.x | Python 3.10 target | `target-version = "py310"` in ruff config tells it to allow 3.10+ syntax; important for `X \| Y` union types not being flagged |
| mypy 1.19.x | Python 3.10 stubs | `python_version = "3.10"` in mypy config; mypy ships its own typeshed; no separate stubs needed for stdlib |
| hatchling 1.29 | hatch 1.16.x | These are released together; pin to hatchling in `[build-system]` and install hatch as the CLI tool |

## Key stdlib APIs Used (No External Dependencies)

This section documents the stdlib APIs nyanbar depends on — confirmed available in Python 3.10+:

| API | Module | Purpose | Confirmed Available |
|-----|--------|---------|---------------------|
| `get_terminal_size()` | `shutil` | Returns `(columns, lines)` terminal size with fallback | Python 3.3+ (HIGH confidence — stdlib) |
| `monotonic()` | `time` | Monotonic clock for elapsed time measurement | Python 3.3+ (HIGH confidence — stdlib) |
| `@dataclass` | `dataclasses` | `Frame` and `Animation` value objects | Python 3.7+ (HIGH confidence — stdlib) |
| `isatty()` | `sys.stderr` / `os` | Detect pipe/redirect/non-TTY environments | Always available (HIGH confidence — stdlib) |
| `StringIO` | `io` | Capture rendered output in tests | Always available (HIGH confidence — stdlib) |

## Sources

- tqdm 4.67.3 wheel source (`tqdm/std.py`) — inspected `display()`, `__init__`, `format_dict`, `status_printer`, `moveto` — HIGH confidence (direct source inspection)
- PyPI version data via `pip index versions` — all version numbers confirmed current as of 2026-02-25 — HIGH confidence
- Python docs: `shutil.get_terminal_size`, `time.monotonic`, `dataclasses` — confirmed Python 3.10+ availability — HIGH confidence
- Python Packaging Authority (PyPA) recommendation for hatch — MEDIUM confidence (training data, could not verify current PyPA recommendation page due to tool restrictions, but hatch/hatchling are the de facto modern standard)
- PROJECT.md decisions table — informed ANSI vs curses choice, inline vs external assets, zero runtime deps constraint — HIGH confidence (primary source document)

---
*Stack research for: nyanbar — animated terminal progress bar library (tqdm subclass)*
*Researched: 2026-02-25*
