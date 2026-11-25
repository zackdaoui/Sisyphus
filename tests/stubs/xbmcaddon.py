INSTALLED = {}  # addon_id -> dict(name, icon, version, settings)


class Addon(object):
    def __init__(self, addon_id):
        if addon_id not in INSTALLED:
            raise RuntimeError("Unknown addon id '%s'." % addon_id)
        self._d = INSTALLED[addon_id]

    def getAddonInfo(self, key):
        return self._d.get(key, "")

    def getSetting(self, key):
        return str(self._d.get("settings", {}).get(key, ""))

    def getSettingInt(self, key):
        return int(self._d["settings"][key])
