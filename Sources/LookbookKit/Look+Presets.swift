import SwiftUI

public extension Look {
    /// Product looks that a host can switch with `.lookbook(_:)`.
    static let presets: [Look] = [.systemGrouped, .cursor, .grok]

    /// System grouped surface. Default environment value.
    static let systemGrouped = Look(
        id: "systemGrouped",
        pageBackground: Color(light: (242, 242, 247), dark: (28, 28, 30)),
        sectionHeaderFont: .subheadline.weight(.regular),
        symbolWeight: .regular,
        symbolScale: .large
    )

    /// Cursor Mobile canvases: page `#F7F7F7` / `#141414`, sheet `#FCFCFC` / `#191919`.
    /// In-page chips are not a kit color; Cursor is effectively 0-shadow.
    /// Titles stay `.inline` — no Large Title / `.inlineLarge` jump.
    static let cursor = Look(
        id: "cursor",
        pageBackground: Color(light: (247, 247, 247), dark: (20, 20, 20)),
        sheetBackground: Color(light: (252, 252, 252), dark: (25, 25, 25)),
        sectionHeaderFont: .subheadline.weight(.semibold),
        symbolWeight: .semibold,
        symbolScale: .large,
        toolbarTitleDisplayMode: .inline
    )

    /// Grok settings sheet: slightly brighter than system grouped gray.
    static let grok = Look(
        id: "grok",
        pageBackground: Color(light: (245, 245, 245), dark: (32, 32, 34)),
        sectionHeaderFont: .subheadline.weight(.semibold),
        symbolWeight: .semibold,
        symbolScale: .large
    )

    /// Old name for ``grok``.
    static let groupedBright = grok
}
