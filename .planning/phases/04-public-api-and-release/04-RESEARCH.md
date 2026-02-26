# Phase 4: Public API and Release - Research

**Researched:** 2026-02-25
**Domain:** Python packaging, type stubs, test organization, PyPI publishing
**Confidence:** HIGH

## Summary

Phase 4 packages the existing nyanbar library for public release. The codebase is fully functional: all imports already work (`from nyanbar import tqdm, trange, set_theme, Animation, Frame, list_themes, get_theme`), `py.typed` exists, 452 tests pass in 0.66s, and all 5 themes render correctly. What's missing: `pyproject.toml`, mypy strict compliance, a reorganized test suite matching the required domain structure, and a README worthy of PyPI.

The project uses Python 3.14.2 in a `.venv` virtual environment. Zero runtime dependencies. Dev dependencies are currently just pytest 9.0.2. No pyproject.toml or build system exists yet.

**Primary recommendation:** Create pyproject.toml with hatchling build backend, fix any mypy --strict issues, reorganize tests into the 4 domain files specified by CONTEXT.md, write a compelling README, and verify the full pipeline (`build` + `pip install` from wheel).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- License: MIT
- Starting version: 1.0.0
- Minimum Python: 3.10+
- Author: Parker Williams (from git config)
- Homepage: https://github.com/ParkerWilliams/nayan-tqdm
- Build backend: hatchling
- README tone: Fun and playful -- matches the nyan cat spirit, emoji welcome, personality
- Hero content: Lead with GIF/screenshot of themes in action (visual wow factor first)
- Code examples: 5+ examples covering drop-in replacement, theme selection, trange, context manager, manual update, set_description, leave behavior
- Theme gallery: Visual section showing all 5 themes with ASCII/screenshot previews so users can pick a theme
- Manual publish: build locally with `python -m build`, upload with `twine`
- TestPyPI first: upload to test.pypi.org, verify `pip install` works, then publish to real PyPI
- Git tag: create `v1.0.0` tag after successful PyPI publish
- Test organization: by domain -- test_tqdm_compat.py, test_renderer.py, test_themes.py, test_fallbacks.py
- Style: plain pytest test_* functions with fixtures (no classes)
- Existing tests: reorganize Phase 1-3 tests into the new domain-based structure
- Dev dependencies: optional group in pyproject.toml -- `pip install nyanbar[dev]` installs pytest + mypy

### Claude's Discretion
- Exact pyproject.toml classifiers and keywords
- README badge selection and layout
- pytest fixture design and shared conftest patterns
- GIF/screenshot creation tooling (or placeholder approach)
- Exact test count and granularity within each domain file

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| API-01 | __init__.py exports tqdm, trange, set_theme, Animation, Frame, list_themes, get_theme | Already works. Verified with `from nyanbar import tqdm, trange, set_theme, Animation, Frame, list_themes, get_theme` -- all resolve. |
| API-02 | py.typed marker file present for PEP 561 type checking support | File exists at `nyanbar/py.typed` (empty marker). Need mypy --strict to pass. |
| API-03 | pyproject.toml configured with correct metadata, dependencies, and build system | No pyproject.toml exists. Need hatchling backend, MIT license, Python >=3.10 classifiers. |
| TEST-01 | Test suite covers tqdm API compatibility (all standard kwargs work) | Existing test_core.py covers constructor, iteration, update, close, context manager, desc/postfix. Needs reorganization into test_tqdm_compat.py with pytest functions (no classes). |
| TEST-02 | Test suite covers ANSI renderer output correctness | Existing test_renderer.py covers erase_lines, render_frame, ensure_reset, has_unclosed_ansi. Needs reorganization. |
| TEST-03 | Test suite covers each theme renders without error at 0%, 25%, 50%, 75%, 100% | Existing test_themes_{cat,nyan,fish,rocket}.py all parametrize over 5 progress levels x 3 tiers. Needs consolidation into test_themes.py. |
| TEST-04 | Test suite covers fallback behavior in non-TTY, dumb terminal, and narrow terminal | Existing test_fallback.py covers non-TTY, dumb terminal, narrow terminal, disabled, nested bar. Needs reorganization into test_fallbacks.py. |
| TEST-05 | All tests complete in under 2 seconds each | Current suite: 452 tests pass in 0.66s total. Well within budget. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| hatchling | latest | PEP 517 build backend | User decision. Modern, fast, good defaults for pure-Python packages |
| build | latest | PEP 517 frontend (`python -m build`) | Standard way to build sdist + wheel |
| twine | latest | Upload to PyPI/TestPyPI | Standard upload tool, validates packages before upload |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | >=9.0 | Test runner | Already installed (9.0.2). Dev dependency. |
| mypy | >=1.13 | Static type checking | Dev dependency for `--strict` checking. Need to install. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| hatchling | setuptools | Locked decision: user chose hatchling |
| twine | `hatch publish` | twine is more widely documented, user chose twine explicitly |

**Installation (dev):**
```bash
pip install hatchling build twine mypy pytest
```

## Architecture Patterns

### pyproject.toml Structure
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "nyanbar"
version = "1.0.0"
description = "Animated progress bars with nyan cat and friends"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
authors = [{ name = "Parker Williams" }]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    "Typing :: Typed",
]
keywords = ["progress", "bar", "tqdm", "nyan", "cat", "animation", "terminal"]

[project.urls]
Homepage = "https://github.com/ParkerWilliams/nayan-tqdm"
Repository = "https://github.com/ParkerWilliams/nayan-tqdm"

[project.optional-dependencies]
dev = ["pytest>=9.0", "mypy>=1.13"]
```

### Test Reorganization Pattern

Current tests (16 files, class-based) need consolidation into 4 domain files with plain functions:

| New File | Absorbs From | Tests |
|----------|-------------|-------|
| test_tqdm_compat.py | test_core.py, test_integration.py, test_thread.py | tqdm API kwargs, iteration, update, close, context manager, desc/postfix, trange, disable, nested, thread safety |
| test_renderer.py | test_renderer.py, test_utils.py | ANSI renderer output, erase_lines, render_frame, ensure_reset, disp_len, strip_ansi |
| test_themes.py | test_themes_cat.py, test_themes_nyan.py, test_themes_fish.py, test_themes_rocket.py, test_registry.py | All 5 themes x 5 progress points x 3 tiers, registry operations, set_theme, list_themes, get_theme |
| test_fallbacks.py | test_fallback.py, test_terminal.py | Non-TTY, dumb terminal, narrow terminal, disabled, nested bar, terminal detection |

### mypy --strict Compliance

Key areas to verify/fix for `--strict`:
- All functions need return type annotations
- All parameters need type annotations
- No untyped imports (the `from IPython import get_ipython` in terminal.py has `# type: ignore[import-untyped]` already)
- Generics must use explicit type parameters
- `Optional` usage should be checked

Known potential issues:
- `NyanBar.__init__` uses `**kwargs: Any` -- acceptable under strict
- `trange` signature uses `*args: object, **kwargs: object` -- may need adjustment
- `from __future__ import annotations` used consistently -- good for forward refs

### README Structure

```
# nyanbar

[Badges: PyPI version, Python versions, License, Typed]

[Hero GIF/screenshot placeholder]

One-line description

## Quick Start
## Themes Gallery
## API Reference (brief)
## Installation
## Examples (5+ as specified)
## Contributing (brief)
## License
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Package building | Custom setup.py | `python -m build` | PEP 517 standard, handles sdist + wheel correctly |
| PyPI upload | curl/manual HTTP | twine | Validates package integrity, handles auth, TestPyPI support |
| Type checking | Manual annotation review | mypy --strict | Catches actual type errors, PEP 561 compliance |
| Test organization | Manual file moves | Write new files, import existing test logic | Cleaner than trying to merge files; fixtures can be shared via conftest.py |

## Common Pitfalls

### Pitfall 1: Missing package data in wheel
**What goes wrong:** py.typed and theme files not included in built wheel
**Why it happens:** hatchling may not include non-Python files by default
**How to avoid:** Verify wheel contents after build: `unzip -l dist/*.whl | grep py.typed`
**Warning signs:** mypy can't find nyanbar types after pip install

### Pitfall 2: Import path issues after install
**What goes wrong:** `from nyanbar import tqdm` works in development (sys.path includes project root) but fails after pip install from wheel
**Why it happens:** Package not correctly structured for distribution
**How to avoid:** Test with `pip install dist/*.whl` in a clean venv, then verify imports
**Warning signs:** ImportError only in installed context

### Pitfall 3: mypy --strict failures on existing code
**What goes wrong:** Code that runs fine fails mypy --strict due to missing annotations, untyped imports, or `Any` leaking
**Why it happens:** --strict enables many checks beyond default
**How to avoid:** Run mypy early, fix issues incrementally. Common fixes: add return types, annotate closures, use explicit generics
**Warning signs:** Multiple error categories (no-untyped-def, no-any-return, etc.)

### Pitfall 4: Test reorganization breaks coverage
**What goes wrong:** Consolidating tests loses some edge cases or creates import conflicts
**Why it happens:** Copy-paste errors, shared fixtures not properly scoped
**How to avoid:** Run test count before and after; compare coverage; parametrize shared patterns
**Warning signs:** Fewer tests after reorganization than before

### Pitfall 5: README looks bad on PyPI
**What goes wrong:** Markdown renders differently on PyPI vs GitHub
**Why it happens:** PyPI uses a subset of markdown; some GitHub-specific features don't render
**How to avoid:** Use standard markdown, avoid GitHub-only features (admonitions, HTML tags may be stripped). Keep it simple.
**Warning signs:** HTML tags in markdown, complex table layouts

## Code Examples

### pyproject.toml with hatchling
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Building and uploading
```bash
# Build
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ nyanbar

# Upload to real PyPI
twine upload dist/*
```

### Test reorganization — pytest functions with fixtures
```python
# conftest.py
import io
import pytest
from unittest.mock import patch
from nyanbar.terminal import TerminalInfo, ColorTier

@pytest.fixture
def tty_terminal():
    return TerminalInfo(is_tty=True, color_support=ColorTier.COLOR_256, width=80, is_notebook=False)

@pytest.fixture
def non_tty_terminal():
    return TerminalInfo(is_tty=False, color_support=ColorTier.NONE, width=80, is_notebook=False)

@pytest.fixture
def output_stream():
    return io.StringIO()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| setup.py + setuptools | pyproject.toml + hatchling | PEP 517/518 (2019+) | Declarative config, no setup.py needed |
| MANIFEST.in for package data | Hatchling auto-includes py.typed | hatchling default behavior | Less boilerplate |
| Optional type annotations | PEP 561 py.typed + mypy --strict | Mature since mypy 1.0+ | Full type safety for users |

## Open Questions

1. **GIF/screenshot for README hero**
   - What we know: User wants visual wow factor with themes in action
   - What's unclear: No tooling for capturing terminal GIFs (asciinema, terminalizer, VHS)
   - Recommendation: Use ASCII art placeholders in README with `<!-- TODO: replace with GIF -->` comments. Can be created manually later. The README should still be compelling with code examples and theme previews in text.

2. **Python 3.14 compatibility**
   - What we know: The venv uses Python 3.14.2. All code works.
   - What's unclear: mypy may not fully support Python 3.14 yet (it's very new)
   - Recommendation: Set `requires-python = ">=3.10"` in pyproject.toml. If mypy has issues with 3.14, test with `--python-version 3.13` flag.

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection: All source files in nyanbar/, tests/, verified import behavior, ran test suite
- Python Packaging User Guide (pypa.io): pyproject.toml structure, hatchling backend, build + twine workflow
- PEP 561: py.typed marker file specification

### Secondary (MEDIUM confidence)
- Hatchling documentation: Default package data inclusion behavior
- mypy documentation: --strict flag behavior and common fixes

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - well-established Python packaging tools, user decisions locked
- Architecture: HIGH - existing codebase fully inspected, clear reorganization path
- Pitfalls: HIGH - common Python packaging issues, well-documented

**Research date:** 2026-02-25
**Valid until:** 2026-03-25 (stable domain, 30-day validity)
