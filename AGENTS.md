# LookbookKit

Personal SwiftUI look presets for matching a reference app's surface details.

- Do not wrap `Form`, `List`, `Section`, or rows into kit components.
- Host pages keep writing native SwiftUI.
- Public API names all start with `lookbook` so every injection site is one search.
- Choose the product look in one place with `.lookbook(_:)`. Page and sheet canvases declare a role with `.lookbookSurface(.page)` or `.lookbookSurface(.sheet)`. Other call sites only read the environment.
- Scan for missed canvases with `scripts/lookbook-surface-candidates.py`; it reports candidates, not a hard gate.
- Preset names at `.lookbook(_:)` may be product names (`.cursor`, `.grok`). Do not copy product hex values into host views.
- A new reference app is a new `Look` preset that fills every token. A new visual axis is a new property on `Look` with a value for every existing preset.
- Do not use UIAppearance or private list decoration views.
