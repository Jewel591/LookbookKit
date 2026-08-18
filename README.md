# LookbookKit

Optional beta look presets for SwiftUI. Not a component library, and not a required house kit.

Hosts opt in when they want a page or sheet to match a reference app. APIs may still change. There is no playbook lint that checks whether an app adopted this package.

Host pages keep writing native `Form`, `Section`, `Label`, and `Image`. The kit only injects surface tokens through `lookbook*` modifiers.

## Requirements

- iOS 18+ / macOS 15+
- Swift 6

## Installation

Add the package with an automatic compatible version range (`Up to Next Major Version` in Xcode, `from:` in `Package.swift`):

```
https://github.com/Jewel591/LookbookKit
```

## Choose a look

Call `.lookbook(_:)` once at the scene root. Switching products is this one line.

```swift
import LookbookKit
import SwiftUI

WindowGroup {
    HomeView()
        .lookbook(.cursor)
}
```

Every canvas then declares a role. Pages and sheets use the same modifier:

```swift
ScrollView { … }
    .lookbookSurface(.page)

.sheet {
    SettingsView()
        .lookbookSurface(.sheet)
}
```

Previews or a sheet that must choose the look itself can pass the role at the same call:

```swift
SettingsView()
    .lookbook(.cursor, surface: .sheet)
```

Do not copy product hex values into views. Prefer `Form` over `List` when the look should own the page background.

## Modifiers

| Modifier | Required? | Where | What it does |
|---|---|---|---|
| `.lookbook(_:)` | Yes, once | Scene root | Sets the product look, grouped `FormStyle`, and environment |
| `.lookbookSurface(.page)` | Yes, on pages | Page `ScrollView` / `Form` / detail canvas | Paints the page canvas from the current look |
| `.lookbookSurface(.sheet)` | Yes, on sheets | Presented sheet content | Paints the sheet canvas and presentation background |
| `.lookbookSectionHeader()` | Optional | `Section` header `Text` | Header font and secondary color from the look |
| `.lookbookSymbol()` | Optional | `Label` / `Image` | Symbol weight and scale from the look |
| `.lookbookToolbarBackground()` | Optional | A view that owns the nav bar | Matches the toolbar to the current page or sheet canvas |

Typical form:

```swift
Form {
    Section {
        Label("Haptics", systemImage: "hand.tap")
            .lookbookSymbol()
    } header: {
        Text("App")
            .lookbookSectionHeader()
    }
}
.lookbookSurface(.page)
.lookbookToolbarBackground()
```

There are no kit wrappers for `Form`, `List`, `Section`, or rows. If a modifier is not in this table, it does not exist; do not invent product-named ones such as `.lookbookCursorChrome()`.

## Looks

| Look | Page | Sheet | Type |
|---|---|---|---|
| `.cursor` | `#F7F7F7` / `#141414` | `#FCFCFC` / `#191919` | Semibold headers and symbols |
| `.grok` | `#F5F5F5` / `#202022` | Same as page | Semibold headers and symbols |
| `.systemGrouped` | `#F2F2F7` / `#1C1C1E` | Same as page | Regular headers and symbols |

`.groupedBright` is the old name for `.grok`. `Look.presets` is the switchable list.

A new reference app is a new preset that fills every token on `Look`. A new visual axis is a new property on `Look`, filled for every existing preset.

In-page chips are not a look token. Cursor Mobile uses essentially no drop shadow, so do not add chip colors or shadow axes to the kit.

## Inventory

Every injection site uses the `lookbook` prefix:

```sh
rg -n --type swift '\.lookbook(Surface|SectionHeader|Symbol|ToolbarBackground)?\('
```

To find canvases that may still need `.lookbookSurface`, and drop-shadow sites that fight a Cursor look:

```sh
python3 scripts/lookbook-surface-candidates.py /path/to/HostApp
python3 scripts/lookbook-shadow-candidates.py /path/to/HostApp
```

Both scripts print candidates only. They cannot prove a line is a page versus a chip, or that a shadow is decorative, and they are not a hard gate. `.lookbook(.cursor)` does not turn off shadows in the subtree.

Only Ivens can keep a shadow. After he confirms a specific site, put a reason on the same line or the line above. The shadow scan still prints it, under Exempted:

```swift
// lookbook-shadow-exempt: lift the badge off a photo
Image(photo)
    .shadow(radius: 8)
```
