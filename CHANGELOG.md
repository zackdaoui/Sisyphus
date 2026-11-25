# Changelog

## 1.0.0
- First release.
- Scans installed add-ons and lists the supported ones with icon and name.
- Tick boxes, Select all, Deselect all, Clean Selected, confirmation dialog and results screen.
- Integrations (each verified against the add-on's own code):
  - Elementum 0.1.119: "Clear the cache" and "Clear TMDB cache".
  - POV 6.11.03: scraper results, metadata and lists caches.
  - TMDb Helper 6.22.7: image cache only (trimmed to the add-on's own size limit).
- Each add-on is cleaned independently; one failure never stops the others.
- No storage figures are shown (they cannot be measured reliably).
