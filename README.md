# nayan-tqdm

[![PyPI version](https://img.shields.io/pypi/v/nayan-tqdm)](https://pypi.org/project/nayan-tqdm/)
[![Python versions](https://img.shields.io/pypi/pyversions/nayan-tqdm)](https://pypi.org/project/nayan-tqdm/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Typed](https://img.shields.io/badge/typed-PEP%20561-brightgreen.svg)](https://peps.python.org/pep-0561/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/nayan-tqdm?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/nayan-tqdm)

**Animated progress bars that spark joy.**
A drop-in [tqdm](https://github.com/tqdm/tqdm) replacement with 40 themes, zero dependencies, and full type safety.

Your progress bars don't have to be boring. Swap one import and get rainbow cats, fire-breathing dragons, surfing waves, and table flips.

## Installation

```bash
pip install nayan-tqdm
```

Zero dependencies. Python 3.10+. That's it.

## Quick Start

```python
# Before
from tqdm import tqdm

# After -- same API, way more fun
from nayan_tqdm import tqdm

for item in tqdm(range(1000)):
    pass
```

## Themes

nayan-tqdm ships with **40 built-in themes** across emoji, kaomoji, and meme categories. Each theme has 3 rendering tiers (emoji, unicode, ascii) automatically selected based on your terminal.

### Emoji Trail Themes

These themes fill the bar with emoji, leaving a colorful trail behind the sprite.

```
ocean:       50%|🌊🌊🌊🌊🌊🌊🌊🌊🏄                | 50/100 [00:05<00:05, 10.00it/s]
fire:        50%|🔥🔥🔥🔥🔥🔥🔥🔥🐉                | 50/100 [00:05<00:05, 10.00it/s]
bee:         50%|🌻🌸🌼🌷🌺🌻🌸🌼🐝                | 50/100 [00:05<00:05, 10.00it/s]
love:        50%|❤️💛💚💙💜❤️💛💚💘                | 50/100 [00:05<00:05, 10.00it/s]
music:       50%|🎵🎶🎵🎶🎵🎶🎵🎶🎸                | 50/100 [00:05<00:05, 10.00it/s]
snake:       50%|🟩🟩🟩🟩🟩🟩🟩🟩🐍                | 50/100 [00:05<00:05, 10.00it/s]
train:       50%|🚃🚃🚃🚃🚃🚃🚃🚃🚂                | 50/100 [00:05<00:05, 10.00it/s]
pasta:       50%|🍝🍝🍝🍝🍝🍝🍝👨‍🍳               | 50/100 [00:05<00:05, 10.00it/s]
```

### Cat Themes

Five feline variations, each with distinct personality.

```
cat_mouse:   50%|•·•·•·•·•·•·•·🐱🐭                | 50/100 [00:05<00:05, 10.00it/s]
cat_yarn:    50%|•◆•◆•◆•◆•◆•◆•🐱🧶                | 50/100 [00:05<00:05, 10.00it/s]
cat_play:    50%|🐾🐾🐾🐾🐾🐾🐾🐾🙀                | 50/100 [00:05<00:05, 10.00it/s]
cat_smug:    50%|🐟🐟🐟🍥🐟🐟🐟🍥😼                | 50/100 [00:05<00:05, 10.00it/s]
cat_sleepy:  50%|💤💤💤💤💤💤💤💤😿                | 50/100 [00:05<00:05, 10.00it/s]
```

### Decorated Themes

These have twinkling decorations above and below the bar.

```
  ✦       ★                    ✦                    ★
nyan:        50%|████████████████🐱                | 50/100 [00:05<00:05, 10.00it/s]
  ★    ✦              ★              ✦

  ★  ·       ✦        ·  ★       ✦    ·  ★
rocket:      50%|🔥💥🔥✨🔥🌟🔥💥🚀                | 50/100 [00:05<00:05, 10.00it/s]
  •    ·        •   ·        •    ·

  ✦       ★           ·       ✦       ★
wizard:      50%|★✳♦☆❄☄✡∴⌂✦★✳♦☆❄☄🧙                | 50/100 [00:05<00:05, 10.00it/s]
  ★    ·              ★              ✦
```

### Kaomoji & Meme Themes

Classic internet faces as progress bars.

```
table_flip:  50%|██████████████(°_°)               | 50/100 [00:05<00:05, 10.00it/s]
             100%|████████████████████████████(╯°□°)╯︵ ┻━┻|

finger_guns: 50%|✧✦✧☆✧✦✧☆✧✦✧☆✧(☞ﾟ∀ﾟ)☞              | 50/100 [00:05<00:05, 10.00it/s]
shrug:       50%|▓▓▓▓▓▓▓▓▓▓▓▓¯\_(ツ)_/¯            | 50/100 [00:05<00:05, 10.00it/s]
deal_with_it:50%|██████████████( •_•)              | 50/100 [00:05<00:05, 10.00it/s]
             100%|████████████████████████████████████████(⌐■_■)|

lenny:       50%|░▒▓█░▒▓█░▒▓█░( ͡° ͜ʖ ͡°)             | 50/100 [00:05<00:05, 10.00it/s]
uwu:         50%|♡♥♡♥♡♥♡♥♡♥♡♥♡(✿◠‿◠)               | 50/100 [00:05<00:05, 10.00it/s]
rage:        50%|███████████████(ಠ益ಠ)              | 50/100 [00:05<00:05, 10.00it/s]
flex:        50%|██████████████ᕙ(⇀‸↼‶)ᕗ            | 50/100 [00:05<00:05, 10.00it/s]
```

### All 40 Themes

> `bear` `bee` `cat_mouse` `cat_play` `cat_sleepy` `cat_smug` `cat_yarn` `construction` `cry` `deal_with_it` `disapproval` `disco` `double_flip` `finger_guns` `fire` `flex` `garden` `heartbeat` `hype` `lenny` `lightning` `love` `matrix` `music` `nyan` `ocean` `pasta` `rage` `rocket` `run` `shrug` `snake` `sparkles` `table_flip` `table_rage` `table_unflip` `train` `uwu` `wizard` `zen`

Pick one:

```python
for item in tqdm(range(1000), theme="ocean"):
    pass
```

## Usage

### trange shorthand

```python
from nayan_tqdm import trange

for i in trange(100):
    pass
```

### Context manager

```python
from nayan_tqdm import tqdm

with tqdm(total=100) as bar:
    for batch in data_loader:
        process(batch)
        bar.update(10)
```

### Manual update

```python
from nayan_tqdm import tqdm

bar = tqdm(total=500)
for chunk in download_chunks():
    save(chunk)
    bar.update(len(chunk))
bar.close()
```

### Description and postfix

```python
bar = tqdm(range(100))
for epoch in bar:
    loss = train(epoch)
    bar.set_description(f"Epoch {epoch}")
    bar.set_postfix(loss=f"{loss:.4f}")
```

### Set a global default theme

```python
from nayan_tqdm import set_theme, tqdm

set_theme("rocket")

# All bars now use the rocket theme
for item in tqdm(range(100)):
    pass
```

### Force a render level

```python
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

## Typed

Fully typed with a `py.typed` marker ([PEP 561](https://peps.python.org/pep-0561/)). Passes `mypy --strict` with zero errors.

## Graceful Fallback

nayan-tqdm automatically falls back to a plain text progress bar when output is piped, the terminal is too narrow, or the bar is disabled. No crashes, no garbled output.

## Requirements

- **Python**: 3.10+
- **Dependencies**: None
- **Platforms**: macOS, Linux, Windows

## License

[MIT](LICENSE)
