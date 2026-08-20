# LookbookKit

Optional beta SwiftUI look presets for matching a reference app's surface details.

This is not a house default. Hosts opt in. Do not add a playbook lint that requires adoption.

- Do not wrap `Form`, `List`, `Section`, or rows into kit components.
- Host pages keep writing native SwiftUI.
- Public API names all start with `lookbook` so every injection site is one search.
- Choose the product look in one place with `.lookbook(_:)`. Page and sheet canvases declare a role with `.lookbookSurface(.page)` or `.lookbookSurface(.sheet)`. Other call sites only read the environment. The canvas applies `toolbarTitleDisplayMode` from the look (`.cursor` is `.inline`). Hosts should not also set `.toolbarTitleDisplayMode` / `.navigationBarTitleDisplayMode` — that override fights the look. Title scale is this axis, not a type ramp or `.lookbookTitle()`.
- Scan for missed canvases with `scripts/lookbook-surface-candidates.py`, drop shadows with `scripts/lookbook-shadow-candidates.py`, and page-title slots with `scripts/lookbook-title-candidates.py`. All three report candidates, not a hard gate. `.lookbook(.cursor)` cannot disable subtree shadows or move a painted body title into `.navigationTitle`; do not add a `.lookbookElevation()` or `.lookbookTitle()` wrapper. Agents run the shadow scan and remove open hits by default. Title-slot hits are reviewed one by one: missing `.navigationTitle` on a page-sized view, an in-content `.title` / `.title2` / `.largeTitle` competing with the nav title, or a host `.toolbarTitleDisplayMode` override. ⛔ Do not write `lookbook-shadow-exempt` or `lookbook-title-exempt` without Ivens confirming that specific site. After he confirms, put `// lookbook-*-exempt: <reason>` on the same line or the previous line — the script still prints it, under Exempted. An empty reason does not exempt.
- Preset names at `.lookbook(_:)` may be product names (`.cursor`, `.grok`). Do not copy product hex values into host views.
- Canvases are page and sheet only. In-page chips are not a token; use host white or a system fill. Do not add chip hex, shadow properties, or a type ramp. Cursor Mobile is effectively 0-shadow — elevation is page gray against white — and it never jumps to Large Title.
- A new reference app is a new `Look` preset that fills every token. A new visual axis is a new property on `Look` with a value for every existing preset.
- Do not use UIAppearance or private list decoration views.
