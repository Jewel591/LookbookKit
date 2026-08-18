# LookbookKit

Optional beta SwiftUI look presets for matching a reference app's surface details.

This is not a house default. Hosts opt in. Do not add a playbook lint that requires adoption.

- Do not wrap `Form`, `List`, `Section`, or rows into kit components.
- Host pages keep writing native SwiftUI.
- Public API names all start with `lookbook` so every injection site is one search.
- Choose the product look in one place with `.lookbook(_:)`. Page and sheet canvases declare a role with `.lookbookSurface(.page)` or `.lookbookSurface(.sheet)`. Other call sites only read the environment.
- Scan for missed canvases with `scripts/lookbook-surface-candidates.py`, and for drop shadows with `scripts/lookbook-shadow-candidates.py`. Both report candidates, not a hard gate. `.lookbook(.cursor)` cannot disable subtree shadows; do not add a `.lookbookElevation()` wrapper. Agents run the shadow scan and remove open hits by default. ⛔ Do not write `lookbook-shadow-exempt` without Ivens confirming that specific site must keep a shadow. After he confirms, put `// lookbook-shadow-exempt: <reason>` on the same line or the previous line — the script still prints it, under Exempted. An empty reason does not exempt.
- Preset names at `.lookbook(_:)` may be product names (`.cursor`, `.grok`). Do not copy product hex values into host views.
- Canvases are page and sheet only. In-page chips are not a token; use host white or a system fill. Do not add chip hex or shadow properties. Cursor Mobile is effectively 0-shadow — elevation is page gray against white.
- A new reference app is a new `Look` preset that fills every token. A new visual axis is a new property on `Look` with a value for every existing preset.
- Do not use UIAppearance or private list decoration views.
