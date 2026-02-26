# nyanbar

[![PyPI version](https://img.shields.io/pypi/v/nyanbar)](https://pypi.org/project/nyanbar/)
[![Python versions](https://img.shields.io/pypi/pyversions/nyanbar)](https://pypi.org/project/nyanbar/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Typed](https://img.shields.io/badge/typed-PEP%20561-brightgreen.svg)](https://peps.python.org/pep-0561/)

**Animated progress bars with nyan cat and friends.**
A drop-in replacement for [tqdm](https://github.com/tqdm/tqdm) with zero dependencies and cute animated themes.

<!-- TODO: Add terminal recording GIF here showing nyan cat progress bar in action -->

Your progress bars don't have to be boring. Replace one import and watch a cat walk across your terminal.

## Installation

```bash
pip install nyanbar
```

Zero dependencies. Python 3.10+. That's it.

## Quick Start

```python
from nyanbar import tqdm

for item in tqdm(range(1000)):
    pass  # your work here
```

That's literally all you need to change. If you're already using tqdm, swap the import and you're done.

## Themes

nyanbar ships with 5 built-in animated themes. Each theme has 3 rendering tiers (emoji, unicode, ascii) that are automatically selected based on your terminal's capabilities.

### `cat_walk` (default: nyan)

A cat walking across the progress bar. Single line, clean and simple.

```
=^.^=                                                        50%|00:05<00:05
```

### `cat_bounce`

A cat bouncing above the bar. Two lines of fun.

```
=^.^=
-----                                                        50%|00:05<00:05
```

### `nyan`

The classic nyan cat with a rainbow trail and twinkling stars. Three lines of pure joy.

```
 * ~~~~  *
~~~~~~=^.^=                                                  50%|00:05<00:05
* ~~~~  *
```

### `fish`

A fish swimming through rising water. Three lines of aquatic adventure.

```
   o
~~~~~~~~                                                     50%|00:05<00:05
 ><>
```

### `rocket`

A rocket launching with animated flames. Four lines of liftoff.

```
  /\
  ||
  **                                                         50%|00:05<00:05
======
```

Select a theme by name:

```python
for item in tqdm(range(1000), theme="rocket"):
    pass
```

## Examples

### Drop-in tqdm replacement

```python
# Before (tqdm)
from tqdm import tqdm

# After (nyanbar) -- same API, animated cats
from nyanbar import tqdm
```

### Choose a theme

```python
from nyanbar import tqdm

for item in tqdm(range(1000), theme="fish"):
    pass
```

### trange shorthand

```python
from nyanbar import trange

for i in trange(100):
    pass
```

### Context manager

```python
from nyanbar import tqdm

with tqdm(total=100) as bar:
    for batch in data_loader:
        process(batch)
        bar.update(10)
```

### Manual update and close

```python
from nyanbar import tqdm

bar = tqdm(total=500)
for chunk in download_chunks():
    save(chunk)
    bar.update(len(chunk))
bar.close()
```

### Description and postfix

```python
from nyanbar import tqdm

bar = tqdm(range(100))
for epoch in bar:
    loss = train(epoch)
    bar.set_description(f"Epoch {epoch}")
    bar.set_postfix(loss=f"{loss:.4f}")
```

### Leave behavior

```python
from nyanbar import tqdm

# Bar disappears when done
for item in tqdm(range(100), leave=False):
    pass

# Bar stays visible (default)
for item in tqdm(range(100), leave=True):
    pass
```

### Set a global theme

```python
from nyanbar import set_theme, tqdm

set_theme("rocket")

# All bars now use the rocket theme
for item in tqdm(range(100)):
    pass
```

### Force a render level

```python
from nyanbar import tqdm

# Force ASCII rendering even in a fancy terminal
for item in tqdm(range(100), render_level="ascii"):
    pass
```

## API Reference

### Progress bars

| Name | Description |
|------|-------------|
| `tqdm(iterable, **kwargs)` | Wrap an iterable with an animated progress bar |
| `trange(n, **kwargs)` | Shorthand for `tqdm(range(n), **kwargs)` |
| `NyanBar` | The progress bar class (also aliased as `tqdm`) |

### Key parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `total` | `len(iterable)` | Total number of iterations |
| `desc` | `None` | Description prefix |
| `theme` | `"nyan"` | Animation theme name |
| `render_level` | auto-detected | Force `"emoji"`, `"unicode"`, or `"ascii"` |
| `leave` | `True` | Keep the bar visible after completion |
| `disable` | `False` | Disable the progress bar entirely |
| `unit` | `"it"` | Unit label for rate display |
| `unit_scale` | `False` | Format counts with SI suffixes (k, M, G, ...) |
| `miniters` | `1` | Minimum iterations between display updates |
| `mininterval` | `0.1` | Minimum seconds between display updates |
| `position` | `0` | Bar position (nested bars use `> 0`) |
| `postfix` | `None` | Dict of extra stats to display |

### Theme management

| Name | Description |
|------|-------------|
| `set_theme(name)` | Set the default theme for all new bars |
| `list_themes()` | Return sorted list of available theme names |
| `get_theme(name, tier)` | Get a theme's `Animation` object for a specific tier |

### Models

| Name | Description |
|------|-------------|
| `Animation` | Frozen dataclass holding frames, FPS, mode, and completion frame |
| `Frame` | Frozen dataclass holding line strings with computed display width |
| `AnimationMode` | Enum: `WALK`, `CYCLE`, `FILL` |

## Typed

nyanbar is fully typed and ships with a `py.typed` marker ([PEP 561](https://peps.python.org/pep-0561/)). It passes `mypy --strict` with zero errors. Your IDE will thank you.

## Graceful Fallback

nyanbar automatically falls back to a plain text progress bar (no ANSI escapes) when:

- Output is piped (non-TTY)
- Terminal is too narrow (< 30 columns)
- The bar is explicitly disabled

No crashes, no garbled output. It just works.

## Requirements

- **Python**: 3.10+
- **Dependencies**: None (zero runtime dependencies)
- **Platforms**: macOS, Linux, Windows (any terminal that supports ANSI escape codes)

## License

[MIT](LICENSE)
