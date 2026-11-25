# -*- coding: utf-8 -*-
import socket

from ..models import Step
from .base import Integration

BASE = "RunPlugin(plugin://plugin.video.elementum/cmd/cache/%s)"


class ElementumIntegration(Integration):
    """Elementum (verified against plugin.video.elementum 0.1.119).

    Elementum lists these actions in its own Settings > Cache section.
    The Python plugin forwards them to the Elementum background service
    (ElementumD), so the service must be running.

    Deliberately NOT used: clear_trakt, compact_cache and every
    cmd/database/* action. Those are implemented inside the compiled
    service, so what they delete cannot be verified from the add-on code.
    """

    addon_id = "plugin.video.elementum"
    name = "Elementum"
    summary = "Cache + TMDB cache"
    run_order = 10

    def steps(self):
        return [
            Step("Clear the cache", BASE % "clear_cache"),
            Step("Clear TMDB cache", BASE % "clear_tmdb"),
        ]

    def check_ready(self, addon):
        host = addon.getSetting("remote_host") or "127.0.0.1"
        port = addon.getSetting("remote_port") or "65220"
        try:
            sock = socket.create_connection((host, int(port)), timeout=3)
            sock.close()
        except Exception:
            return ("Elementum's background service is not reachable at %s:%s. "
                    "Open Elementum once so it starts, then try again." % (host, port))
        return None
