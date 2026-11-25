# -*- coding: utf-8 -*-
"""Thin wrapper around Kodi APIs so the rest of the code stays testable."""
import xbmc
import xbmcaddon

ADDON_ID = "script.kodi.universal.cleaner"
TITLE = "Kodi Universal Cleaner"


def log(message, level=None):
    if level is None:
        level = xbmc.LOGINFO
    xbmc.log("[%s] %s" % (ADDON_ID, message), level)


def run_builtin(command, wait=True):
    """Run a Kodi built-in (RunPlugin / RunScript). Blocks until it finishes."""
    log("Running built-in: %s" % command)
    xbmc.executebuiltin(command, wait)


def get_addon(addon_id):
    """Return the xbmcaddon.Addon for an installed + enabled add-on, else None."""
    try:
        return xbmcaddon.Addon(addon_id)
    except Exception:  # not installed, disabled or broken
        return None


def sleep(ms):
    xbmc.sleep(ms)


def condition(expression):
    return xbmc.getCondVisibility(expression)
