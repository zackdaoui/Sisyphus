# -*- coding: utf-8 -*-
from .kodi_api import get_addon, log
from .models import AddonResult


def clean_one(supported):
    """Clean a single add-on. Never raises."""
    integ = supported.integration
    result = AddonResult(addon_id=integ.addon_id, name=supported.name)
    try:
        addon = get_addon(integ.addon_id)
        if addon is None:
            result.error = "Add-on is no longer installed or enabled."
            return result
        reason = integ.check_ready(addon)
        if reason:
            result.error = reason
            return result
        result.steps = integ.clean()
    except Exception as exc:
        log("Unexpected error cleaning %s: %s" % (integ.addon_id, exc))
        result.error = "Unexpected error: %s" % exc
    return result


def clean_selected(selected, progress=None):
    """Clean each selected add-on independently. progress(i, total, name) is optional."""
    results = []
    ordered = sorted(selected, key=lambda s: s.integration.run_order)
    for i, supported in enumerate(ordered):
        if progress:
            progress(i, len(ordered), supported.name)
        results.append(clean_one(supported))
    return results


def format_results(results):
    ok = [r for r in results if r.ok]
    bad = [r for r in results if not r.ok]
    ops_ok = sum(r.ops_ok for r in results)
    ops_bad = sum(r.ops_failed for r in results)
    lines = [
        "Add-ons cleaned: %d    Add-ons failed: %d" % (len(ok), len(bad)),
        "Operations successful: %d    Operations failed: %d" % (ops_ok, ops_bad),
        "",
    ]
    for r in results:
        lines.append("[B]%s: %s[/B]" % (r.name, "DONE" if r.ok else "FAILED"))
        if r.error:
            lines.append("   Reason: %s" % r.error)
        for s in r.steps:
            lines.append("   %s %s%s" % ("OK  " if s.ok else "FAIL", s.label,
                                         "" if s.ok else " - " + s.detail))
        lines.append("")
    lines.append("Note: Kodi does not report what another add-on actually "
                 "removed. DONE means the add-on's own cleaning command was "
                 "run without error. No storage figures are shown because "
                 "they cannot be measured reliably.")
    return "\n".join(lines)
