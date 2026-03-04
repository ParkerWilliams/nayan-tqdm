"""Theme registry for nayan_tqdm.

Maps theme names to lazy factory functions that produce :class:`Animation`
objects at a specific rendering tier (``"emoji"``, ``"unicode"``, ``"ascii"``).
"""
from __future__ import annotations

import os
import warnings
from typing import Callable

from .models import Animation
from .terminal import ColorTier, TerminalInfo

__all__ = [
    "register_theme",
    "get_theme",
    "list_themes",
    "set_theme",
    "get_default_theme",
    "resolve_render_tier",
]

# Type alias: factory takes a tier string and returns an Animation.
ThemeFactory = Callable[[str], Animation]

# ── Registry state (module-level) ────────────────────

_themes: dict[str, ThemeFactory] = {}
_cache: dict[tuple[str, str], Animation] = {}
_default_theme: str = "nyan"


# ── Public API ───────────────────────────────────────


def register_theme(name: str, factory: ThemeFactory) -> None:
    """Register a theme factory.  Overwrites any existing entry for *name*.

    Parameters
    ----------
    name:
        Theme identifier (e.g. ``"nyan"``, ``"cat_walk"``).
    factory:
        Callable that accepts a tier string (``"emoji"``/``"unicode"``/``"ascii"``)
        and returns an :class:`Animation`.
    """
    _themes[name] = factory
    # Invalidate cached entries for this theme
    keys_to_remove = [k for k in _cache if k[0] == name]
    for k in keys_to_remove:
        del _cache[k]


def get_theme(name: str, tier: str = "emoji") -> Animation:
    """Get the :class:`Animation` for theme *name* at rendering *tier*.

    Lazily calls the factory on first access and caches the result.
    Unknown names emit a :class:`UserWarning` and fall back to the
    default theme.

    Parameters
    ----------
    name:
        Theme name to look up.
    tier:
        Rendering tier: ``"emoji"``, ``"unicode"``, or ``"ascii"``.
    """
    if name not in _themes:
        warnings.warn(
            f"Unknown theme '{name}', using default '{_default_theme}'",
            UserWarning,
            stacklevel=2,
        )
        name = _default_theme

    key = (name, tier)
    if key not in _cache:
        _cache[key] = _themes[name](tier)
    return _cache[key]


def list_themes() -> list[str]:
    """Return a sorted list of all registered theme names."""
    return sorted(_themes.keys())


def set_theme(name: str) -> None:
    """Set the global default theme for future bars.

    If *name* is not a registered theme, emits a :class:`UserWarning`
    and leaves the default unchanged.
    """
    global _default_theme
    if name not in _themes:
        warnings.warn(
            f"Unknown theme '{name}', keeping default '{_default_theme}'",
            UserWarning,
            stacklevel=2,
        )
        return
    _default_theme = name


def get_default_theme() -> str:
    """Return the current default theme name."""
    return _default_theme


def resolve_render_tier(
    info: TerminalInfo,
    render_level: str | None = None,
) -> str:
    """Determine the rendering tier for the given terminal.

    Parameters
    ----------
    info:
        Terminal capabilities snapshot.
    render_level:
        User override: ``"emoji"``, ``"unicode"``, or ``"ascii"``.
        Bypasses auto-detection when provided.

    Returns
    -------
    str
        One of ``"emoji"``, ``"unicode"``, ``"ascii"``.
    """
    if render_level is not None:
        return render_level

    # UTF-8 locale required for emoji and unicode tiers
    if not _check_utf8_locale():
        return "ascii"

    if info.color_support >= ColorTier.COLOR_256:
        return "emoji"
    elif info.color_support >= ColorTier.COLOR_16:
        return "unicode"
    else:
        return "ascii"


# ── Internal helpers ─────────────────────────────────


def _check_utf8_locale() -> bool:
    """Return ``True`` if locale environment indicates UTF-8 support."""
    for var in ("LC_ALL", "LC_CTYPE", "LANG"):
        val = os.environ.get(var, "")
        if "utf-8" in val.lower() or "utf8" in val.lower():
            return True
    return False


def _clear_cache() -> None:
    """Clear the animation cache.  Used by tests."""
    _cache.clear()
