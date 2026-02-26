"""Built-in themes for nyanbar.

Importing this package registers all built-in themes with the registry.
Theme modules are imported here to trigger their registration side effects.
"""
from . import _cat_walk    # noqa: F401
from . import _cat_bounce  # noqa: F401
from . import _nyan        # noqa: F401
from . import _fish        # noqa: F401
from . import _rocket      # noqa: F401
