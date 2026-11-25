# Contributing

Thanks for helping. The one rule: **an integration may only call the target
add-on's own official cleaning command.** No deleting folders or files, no
touching settings, databases, logins or watched status.

## Adding an add-on
1. Read the target add-on's source. Find how its own "clear cache" button works
   (usually a `RunPlugin(...)` or `RunScript(...)` in its `settings.xml`).
   If you cannot verify what it does, do not add it.
2. Create `resources/lib/universalcleaner/integrations/<name>.py` with an
   `Integration` subclass: `addon_id`, `name`, `summary`, `run_order`, `steps()`
   and, if needed, `check_ready(addon)` (return a reason string if it cannot
   run now). In the docstring, record the add-on version you verified and what
   you deliberately did NOT use, and why.
3. Add it to `ALL_INTEGRATIONS` in `integrations/__init__.py`.
4. Add tests in `tests/` (exact commands, readiness checks, failure handling).
5. Update the table in `README.md` and `CHANGELOG.md`.

## Tests
```
pip install pytest
python -m pytest tests
```
Tests use small Kodi stubs in `tests/stubs`. They check our logic only; real
cleaning must be tested on a Kodi device, and please say so in your pull request.

## Style
Python 3 (Kodi 19+), clear names, small functions, log what is run.
