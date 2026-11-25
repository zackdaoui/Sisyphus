# -*- coding: utf-8 -*-
from ..models import Step
from .base import Integration

BASE = "RunPlugin(plugin://plugin.video.pov/?mode=clear_cache&cache=%s)"


class PovIntegration(Integration):
    """POV (verified against plugin.video.pov 6.11.03).

    Uses POV's own route mode=clear_cache&cache=<type>. POV shows its own
    "Are you sure?" prompt for each type, and Kodi does not tell us if the
    user pressed No, so a declined prompt still looks like "command sent".

    Deliberately NOT used:
      * clear_all_cache and the trakt / mdblist types: they wipe the cached
        Trakt watched status and progress tables (POV re-downloads them,
        but this cleaner promises never to touch watched status).
      * internal_scrapers (debrid cloud lists), imdb, tmdblist: left out of
        V1 to avoid even more confirmation prompts.
    """

    addon_id = "plugin.video.pov"
    name = "POV"
    summary = "Scraper results, metadata and list caches"
    run_order = 20

    def steps(self):
        return [
            Step("Scraper results cache", BASE % "external_scrapers"),
            Step("Metadata cache", BASE % "meta"),
            Step("Lists cache", BASE % "list"),
        ]
