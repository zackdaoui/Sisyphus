# -*- coding: utf-8 -*-
from ..kodi_api import log, run_builtin
from ..models import StepResult


class Integration(object):
    """Base class. One subclass per supported add-on.

    A subclass must only run commands that the target add-on itself provides
    for cleaning its cache. Never delete files directly.
    """

    addon_id = ""
    name = ""
    summary = ""      # short text shown under the name in the list
    run_order = 50    # lower runs first

    def steps(self):
        """Return the list of models.Step to run (official commands only)."""
        raise NotImplementedError

    def check_ready(self, addon):
        """Return None if the add-on can be cleaned now, else a reason string."""
        return None

    def after_clean(self):
        """Optional best-effort tidy-up after the steps ran."""

    def clean(self):
        results = []
        for step in self.steps():
            try:
                run_builtin(step.command, wait=True)
                results.append(StepResult(step.label, True, "Command sent"))
            except Exception as exc:  # keep going with remaining steps
                log("%s: step %r failed: %s" % (self.name, step.label, exc))
                results.append(StepResult(step.label, False, str(exc)))
        try:
            self.after_clean()
        except Exception as exc:
            log("%s: after_clean failed: %s" % (self.name, exc))
        return results
