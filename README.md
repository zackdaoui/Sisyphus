# Kodi Universal Cleaner

Clear the caches of your video add-ons from **one screen**, instead of opening
each add-on's settings.

It scans your installed add-ons, shows the ones it supports, and runs each
add-on's **own official cleaning command** for the ones you tick. It does not
delete files itself.

## Supported add-ons (V1.0)

| Add-on | Verified version | What gets cleaned | Not touched, and why |
|---|---|---|---|
| Elementum | 0.1.119 | "Clear the cache", "Clear TMDB cache" | Trakt cache, compact, all database actions: they run inside Elementum's compiled service, so what they delete can't be verified |
| POV | 6.11.03 | Scraper results, metadata and lists caches | "Clear all cache", Trakt and MDBList caches: they wipe cached watched status/progress |
| TMDb Helper | 6.22.7 | Image cache only, trimmed to the size limit in TMDb Helper's settings | Its database cache: TMDb Helper has no official way to clear it and maintains it itself |

Unsupported add-ons are never touched. Other versions probably work but were
not verified.

## Install
1. Download `script.kodi.universal.cleaner-1.0.0.zip` from the Releases page of https://github.com/zackdaoui/Sisyphus.
2. Kodi: Settings > Add-ons > Install from zip file (allow unknown sources if asked).
3. Open it from Add-ons > Program add-ons.

Requires Kodi 19 or newer (developed against Kodi 21 "Omega").

## Use
1. Open **Kodi Universal Cleaner**.
2. Select an add-on to tick it, or use **Select all** / **Deselect all**.
3. Choose **Clean Selected**, then confirm.
4. Read the results screen.

## How cleaning works
For every supported add-on the cleaner checks it is installed and ready, then
runs that add-on's own command with Kodi's `RunPlugin` / `RunScript`. Each
add-on is processed separately, so one failure never blocks the rest.

## Known limitations
- Kodi does not report what another add-on removed. "DONE" means the command ran
  without error. No storage figures are shown for the same reason.
- **POV** asks "Are you sure?" for each of its 3 caches. If you answer No, the
  results still show the command as sent.
- **Elementum** needs its background service running; if it isn't, the cleaner
  says so and does nothing for it.
- **TMDb Helper** does nothing if its image cache limit is Unlimited. It also
  re-opens its own settings window when finished; the cleaner closes it again on
  a best-effort basis.
- Screen text is English only in V1.0.

## Tests
`python -m pytest tests` (see CONTRIBUTING.md). The tests check the add-on's logic
with Kodi stubs. They do not run a real Kodi, so real cleaning has to be checked
on a device.

## Contributing / License
See CONTRIBUTING.md. Licensed under the MIT License (LICENSE.txt).
This project is not affiliated with Kodi or any supported add-on.
