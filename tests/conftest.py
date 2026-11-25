import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "stubs"))
sys.path.insert(0, os.path.join(HERE, "..", "resources", "lib"))

import pytest  # noqa: E402
import xbmc, xbmcaddon, xbmcgui  # noqa: E402,F401


@pytest.fixture(autouse=True)
def reset():
    xbmc.LOG.clear()
    xbmc.BUILTINS.clear()
    xbmc.CONDITIONS.clear()
    xbmcaddon.INSTALLED.clear()
    xbmcgui.CALLS.clear()
    xbmcgui.SCRIPT["select"] = []
    xbmcgui.SCRIPT["yesno"] = [True]
    yield


def install(addon_id, name=None, **settings):
    xbmcaddon.INSTALLED[addon_id] = {
        "name": name or addon_id, "icon": "icon.png", "version": "1.0",
        "settings": settings,
    }
