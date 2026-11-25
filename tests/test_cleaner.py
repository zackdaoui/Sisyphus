import socket
import threading

import xbmc
import xbmcgui

from conftest import install
from universalcleaner import runner, scanner, ui
from universalcleaner.integrations import ALL_INTEGRATIONS
from universalcleaner.integrations.base import Integration
from universalcleaner.models import Step, SupportedAddon

ELE, POV, TMDB = ("plugin.video.elementum", "plugin.video.pov",
                  "plugin.video.themoviedb.helper")


def by_id(addon_id):
    return next(i for i in ALL_INTEGRATIONS if i.addon_id == addon_id)


def listening_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    return s, s.getsockname()[1]


# ---- scanner -------------------------------------------------------------
def test_scan_only_lists_installed_supported_addons():
    install(POV, "POV")
    install("plugin.video.unsupported")
    found = scanner.scan()
    assert [f.integration.addon_id for f in found] == [POV]


def test_scan_empty_when_nothing_supported():
    assert scanner.scan() == []


def test_scan_order_is_stable():
    for a in (TMDB, POV, ELE):
        install(a)
    assert [f.integration.addon_id for f in scanner.scan()] == [ELE, POV, TMDB]


# ---- exact commands (safety) ----------------------------------------------
def test_elementum_commands_are_only_cache_commands():
    cmds = [s.command for s in by_id(ELE).steps()]
    assert cmds == [
        "RunPlugin(plugin://plugin.video.elementum/cmd/cache/clear_cache)",
        "RunPlugin(plugin://plugin.video.elementum/cmd/cache/clear_tmdb)",
    ]


def test_pov_never_touches_trakt_or_clear_all():
    cmds = [s.command for s in by_id(POV).steps()]
    assert len(cmds) == 3
    joined = " ".join(cmds)
    assert "trakt" not in joined and "mdblist" not in joined
    assert "clear_all_cache" not in joined
    assert all(c.startswith("RunPlugin(plugin://plugin.video.pov/?mode=clear_cache&cache=")
               for c in cmds)


def test_tmdbhelper_uses_only_image_cache_script():
    assert [s.command for s in by_id(TMDB).steps()] == [
        "RunScript(plugin.video.themoviedb.helper,clean_image_cache)"]


# ---- readiness ----------------------------------------------------------
def test_elementum_fails_when_service_unreachable():
    s, port = listening_port()
    s.close()  # nothing listening now
    install(ELE, remote_host="127.0.0.1", remote_port=port)
    r = runner.clean_one(SupportedAddon(by_id(ELE), "Elementum", "", "1"))
    assert not r.ok and "not reachable" in r.error
    assert xbmc.BUILTINS == []


def test_elementum_runs_when_service_reachable():
    s, port = listening_port()
    t = threading.Thread(target=lambda: s.accept(), daemon=True)
    t.start()
    install(ELE, remote_host="127.0.0.1", remote_port=port)
    r = runner.clean_one(SupportedAddon(by_id(ELE), "Elementum", "", "1"))
    t.join(timeout=2)
    s.close()
    assert r.ok and r.ops_ok == 2 and len(xbmc.BUILTINS) == 2


def test_tmdbhelper_unlimited_size_is_reported_not_run():
    install(TMDB, image_cache_size=0)
    r = runner.clean_one(SupportedAddon(by_id(TMDB), "TMDb Helper", "", "1"))
    assert not r.ok and "Unlimited" in r.error and xbmc.BUILTINS == []


def test_tmdbhelper_runs_and_closes_reopened_settings():
    install(TMDB, image_cache_size=128)
    xbmc.CONDITIONS["Window.IsActive(addonsettings)"] = True
    r = runner.clean_one(SupportedAddon(by_id(TMDB), "TMDb Helper", "", "1"))
    assert r.ok
    cmds = [c for c, _ in xbmc.BUILTINS]
    assert cmds[0].startswith("RunScript(") and cmds[-1] == "Dialog.Close(addonsettings)"


def test_missing_addon_at_clean_time_is_a_failure():
    r = runner.clean_one(SupportedAddon(by_id(POV), "POV", "", "1"))
    assert not r.ok and "no longer installed" in r.error


# ---- independence of failures ------------------------------------------
class Boom(Integration):
    addon_id, name, run_order = "boom", "Boom", 1

    def steps(self):
        raise RuntimeError("kaboom")


def test_one_failure_does_not_stop_others():
    install("boom")
    install(POV)
    sel = [SupportedAddon(Boom(), "Boom", "", "1"),
           SupportedAddon(by_id(POV), "POV", "", "1")]
    results = runner.clean_selected(sel)
    assert [r.ok for r in results] == [False, True]
    assert "kaboom" in results[0].error
    assert len(xbmc.BUILTINS) == 3


def test_step_failure_is_recorded_and_remaining_steps_run(monkeypatch):
    install(POV)
    calls = []

    def fake(cmd, wait=True):
        calls.append(cmd)
        if "cache=meta" in cmd:
            raise RuntimeError("nope")

    monkeypatch.setattr("universalcleaner.integrations.base.run_builtin", fake)
    r = runner.clean_one(SupportedAddon(by_id(POV), "POV", "", "1"))
    assert len(calls) == 3 and r.ops_ok == 2 and r.ops_failed == 1 and not r.ok


# ---- results text ------------------------------------------------------
def test_format_results_counts_and_no_storage_claims():
    install(POV)
    r1 = runner.clean_one(SupportedAddon(by_id(POV), "POV", "", "1"))
    r2 = runner.clean_one(SupportedAddon(by_id(ELE), "Elementum", "", "1"))
    text = runner.format_results([r1, r2])
    assert "Add-ons cleaned: 1" in text and "Add-ons failed: 1" in text
    assert "Operations successful: 3" in text and "Operations failed: 1" in text
    assert "MB" not in text and "GB" not in text


# ---- UI flow -----------------------------------------------------------
def test_ui_no_supported_addons_message():
    ui.run()
    assert xbmcgui.CALLS[0][0] == "ok" and "No supported add-ons" in xbmcgui.CALLS[0][1]


def test_ui_select_all_clean_confirm_results():
    install(POV, "POV")
    install(TMDB, "TMDb Helper", image_cache_size=128)
    # items: 0 select all, 1 deselect, 2 POV, 3 TMDb, 4 Clean
    xbmcgui.SCRIPT["select"] = [0, 4]
    ui.run()
    kinds = [c[0] for c in xbmcgui.CALLS]
    assert "yesno" in kinds and kinds[-1] == "textviewer"
    shown = [c[1] for c in xbmcgui.CALLS if c[0] == "select"][-1]
    assert shown[2].startswith("[X]") and shown[3].startswith("[X]")
    assert len(xbmc.BUILTINS) == 4  # 3 POV + 1 TMDb (+ Dialog.Close not needed)


def test_ui_cancel_at_confirmation_cleans_nothing():
    install(POV, "POV")
    xbmcgui.SCRIPT["select"] = [2, 3, -1]  # toggle POV, Clean, back out
    xbmcgui.SCRIPT["yesno"] = [False]
    ui.run()
    assert xbmc.BUILTINS == []


def test_ui_clean_with_nothing_selected_does_not_run():
    install(POV, "POV")
    xbmcgui.SCRIPT["select"] = [3, -1]
    ui.run()
    assert xbmc.BUILTINS == [] and xbmcgui.CALLS[1][0] == "ok"


def test_ui_deselect_all():
    install(POV, "POV")
    xbmcgui.SCRIPT["select"] = [0, 1, -1]
    ui.run()
    last_select = [c[1] for c in xbmcgui.CALLS if c[0] == "select"][-1]
    assert last_select[2].startswith("[  ]")
