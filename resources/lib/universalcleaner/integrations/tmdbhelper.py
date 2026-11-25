# -*- coding: utf-8 -*-
from .. import kodi_api
from ..models import Step
from .base import Integration


class TmdbHelperIntegration(Integration):
    """TMDb Helper (verified against plugin.video.themoviedb.helper 6.22.7).

    TMDb Helper has no "clear cache" command. Its only official cache action
    is clean_image_cache, which trims the image cache down to the size limit
    chosen in its settings. It does nothing when that limit is Unlimited.
    Its database cache is maintained by TMDb Helper itself on a schedule, so
    it is NOT touched here.

    After the script finishes TMDb Helper re-opens its own settings window
    (it expects to be started from a settings button), so after_clean closes
    that window again on a best-effort basis.
    """

    addon_id = "plugin.video.themoviedb.helper"
    name = "TMDb Helper"
    summary = "Image cache only (trimmed to your size limit)"
    run_order = 90  # last: it opens its own dialogs

    def steps(self):
        return [Step("Trim image cache",
                     "RunScript(plugin.video.themoviedb.helper,clean_image_cache)")]

    def check_ready(self, addon):
        try:
            size = addon.getSettingInt("image_cache_size")
        except Exception:
            return None  # cannot read it; let TMDb Helper decide
        if size == 0:
            return ("TMDb Helper's image cache limit is set to Unlimited, so its "
                    "cleaner does nothing. Set a size limit in TMDb Helper "
                    "settings first.")
        return None

    def after_clean(self):
        kodi_api.sleep(1000)
        if kodi_api.condition("Window.IsActive(addonsettings)"):
            kodi_api.run_builtin("Dialog.Close(addonsettings)", wait=False)
