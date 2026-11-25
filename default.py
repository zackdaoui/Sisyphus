# -*- coding: utf-8 -*-
"""Entry point for Kodi Universal Cleaner (Program add-ons)."""
import os
import sys

_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'lib')
if _LIB not in sys.path:
    sys.path.insert(0, _LIB)

from universalcleaner import ui  # noqa: E402

if __name__ == '__main__':
    ui.run()
