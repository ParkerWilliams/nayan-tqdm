"""Shared fixtures for nayan_tqdm test suite."""
from __future__ import annotations

import io
import os
from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

from nayan_tqdm.terminal import TerminalInfo, ColorTier


@pytest.fixture
def tty_terminal() -> TerminalInfo:
    """Standard TTY terminal with 256-color support."""
    return TerminalInfo(
        is_tty=True,
        color_support=ColorTier.COLOR_256,
        width=80,
        is_notebook=False,
    )


@pytest.fixture
def non_tty_terminal() -> TerminalInfo:
    """Non-TTY (piped output) terminal."""
    return TerminalInfo(
        is_tty=False,
        color_support=ColorTier.NONE,
        width=80,
        is_notebook=False,
    )


@pytest.fixture
def dumb_terminal() -> TerminalInfo:
    """Dumb TTY terminal (TERM=dumb, no color)."""
    return TerminalInfo(
        is_tty=True,
        color_support=ColorTier.NONE,
        width=80,
        is_notebook=False,
    )


@pytest.fixture
def narrow_terminal() -> TerminalInfo:
    """Narrow TTY terminal (width < 30)."""
    return TerminalInfo(
        is_tty=True,
        color_support=ColorTier.COLOR_256,
        width=25,
        is_notebook=False,
    )


@pytest.fixture
def output_stream() -> io.StringIO:
    """StringIO output stream for capturing bar output."""
    return io.StringIO()


@pytest.fixture
def mock_tty() -> Generator[TerminalInfo, None, None]:
    """Mock a TTY with COLOR_256 and UTF-8 locale for NyanBar tests."""
    info = TerminalInfo(
        is_tty=True, color_support=ColorTier.COLOR_256,
        width=80, is_notebook=False,
    )
    with patch("nayan_tqdm.core.detect_terminal", return_value=info):
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8", "LC_ALL": "", "LC_CTYPE": ""}):
            yield info


@pytest.fixture
def mock_non_tty() -> Generator[TerminalInfo, None, None]:
    """Mock a non-TTY (piped output) for NyanBar tests."""
    info = TerminalInfo(
        is_tty=False, color_support=ColorTier.NONE,
        width=80, is_notebook=False,
    )
    with patch("nayan_tqdm.core.detect_terminal", return_value=info):
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}):
            yield info


@contextmanager
def utf8_locale() -> Generator[None, None, None]:
    """Context manager that sets UTF-8 locale environment."""
    with patch.dict(os.environ, {"LANG": "en_US.UTF-8", "LC_ALL": "", "LC_CTYPE": ""}):
        yield


@contextmanager
def no_utf8_locale() -> Generator[None, None, None]:
    """Context manager that ensures no UTF-8 in locale environment."""
    env = {k: v for k, v in os.environ.items() if k not in ("LANG", "LC_ALL", "LC_CTYPE")}
    env["LANG"] = "C"
    env["LC_ALL"] = ""
    env["LC_CTYPE"] = ""
    with patch.dict(os.environ, env, clear=True):
        yield
