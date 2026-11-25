# -*- coding: utf-8 -*-
from .integrations import ALL_INTEGRATIONS
from .kodi_api import get_addon, log
from .models import SupportedAddon


def scan(integrations=None):
    """Return SupportedAddon entries for supported add-ons that are installed and enabled."""
    found = []
    for integ in sorted(integrations if integrations is not None else ALL_INTEGRATIONS,
                        key=lambda i: i.run_order):
        addon = get_addon(integ.addon_id)
        if addon is None:
            log("Not installed/enabled: %s" % integ.addon_id)
            continue
        found.append(SupportedAddon(
            integration=integ,
            name=addon.getAddonInfo("name") or integ.name,
            icon=addon.getAddonInfo("icon"),
            version=addon.getAddonInfo("version"),
        ))
    return found
