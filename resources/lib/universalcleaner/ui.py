# -*- coding: utf-8 -*-
"""Kodi dialogs for Kodi Universal Cleaner (native dialogs, remote-friendly)."""
import xbmcgui

from . import runner, scanner
from .kodi_api import TITLE, log

SELECT_ALL = 0
DESELECT_ALL = 1
FIRST_ADDON = 2


def _build_items(supported, selected):
    items = [
        xbmcgui.ListItem(label="Select all"),
        xbmcgui.ListItem(label="Deselect all"),
    ]
    for entry in supported:
        mark = "[X]" if entry.integration.addon_id in selected else "[  ]"
        item = xbmcgui.ListItem(label="%s  %s" % (mark, entry.name),
                                label2=entry.integration.summary)
        item.setArt({"icon": entry.icon, "thumb": entry.icon})
        items.append(item)
    items.append(xbmcgui.ListItem(
        label="[B]Clean Selected (%d)[/B]" % len(selected)))
    return items


def _confirm(chosen):
    lines = ["You are about to clean:", ""]
    for entry in chosen:
        lines.append("- %s: %s" % (entry.name, entry.integration.summary))
    lines += ["", "Only these add-ons will be touched. Some add-ons show "
              "their own confirmation first."]
    return xbmcgui.Dialog().yesno(TITLE, "\n".join(lines),
                                  nolabel="Cancel", yeslabel="Clean")


def _run_with_progress(chosen):
    progress = xbmcgui.DialogProgress()
    progress.create(TITLE, "Starting...")

    def update(i, total, name):
        progress.update(int(i * 100 / max(total, 1)), "Cleaning %s..." % name)

    try:
        return runner.clean_selected(chosen, progress=update)
    finally:
        progress.close()


def run():
    dialog = xbmcgui.Dialog()
    try:
        supported = scanner.scan()
    except Exception as exc:
        log("Scan failed: %s" % exc)
        dialog.ok(TITLE, "Could not scan your add-ons.\n\n%s" % exc)
        return

    if not supported:
        dialog.ok(TITLE,
                  "No supported add-ons are installed.\n\n"
                  "Supported: Elementum, POV, TMDb Helper.")
        return

    selected = set()
    cursor = 0
    while True:
        index = dialog.select(TITLE, _build_items(supported, selected),
                              preselect=cursor, useDetails=True)
        if index < 0:
            return
        cursor = index
        clean_index = FIRST_ADDON + len(supported)
        if index == SELECT_ALL:
            selected = {s.integration.addon_id for s in supported}
        elif index == DESELECT_ALL:
            selected = set()
        elif index == clean_index:
            chosen = [s for s in supported if s.integration.addon_id in selected]
            if not chosen:
                dialog.ok(TITLE, "Tick at least one add-on first.")
                continue
            if not _confirm(chosen):
                continue
            results = _run_with_progress(chosen)
            dialog.textviewer(TITLE + " - Results", runner.format_results(results))
            return
        else:
            addon_id = supported[index - FIRST_ADDON].integration.addon_id
            selected.symmetric_difference_update({addon_id})
