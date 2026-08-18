import SwiftUI

/// Page vs sheet canvas. Call sites declare a role; they do not name a product.
public enum LookbookSurface: Sendable, Equatable {
    case page
    case sheet
}

/// A named bag of surface tokens shared by every product look.
///
/// Add a property here only when a new visual axis appears, and fill it for
/// every existing preset (use the page canvas or the system value as default).
/// Add a product by creating another static preset that fills every property.
/// In-page chips and drop shadows are not axes: Cursor elevates with page gray
/// against white and uses essentially no shadow.
public struct Look: Sendable {
    public var id: String
    public var pageBackground: Color
    public var sheetBackground: Color
    public var sectionHeaderFont: Font
    public var symbolWeight: Font.Weight
    public var symbolScale: Image.Scale

    public init(
        id: String,
        pageBackground: Color,
        sheetBackground: Color? = nil,
        sectionHeaderFont: Font,
        symbolWeight: Font.Weight,
        symbolScale: Image.Scale
    ) {
        self.id = id
        self.pageBackground = pageBackground
        self.sheetBackground = sheetBackground ?? pageBackground
        self.sectionHeaderFont = sectionHeaderFont
        self.symbolWeight = symbolWeight
        self.symbolScale = symbolScale
    }

    public func canvas(for surface: LookbookSurface) -> Color {
        switch surface {
        case .page:
            pageBackground
        case .sheet:
            sheetBackground
        }
    }
}

extension Look: Equatable {
    public static func == (lhs: Look, rhs: Look) -> Bool {
        lhs.id == rhs.id
    }
}

extension EnvironmentValues {
    @Entry public var lookbook: Look = .systemGrouped
    @Entry public var lookbookSurface: LookbookSurface = .page
}

extension Color {
    init(light: (Int, Int, Int), dark: (Int, Int, Int)) {
        #if os(macOS)
        self.init(nsColor: NSColor(name: nil) { appearance in
            let usesDark = appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            let rgb = usesDark ? dark : light
            return NSColor(
                srgbRed: CGFloat(rgb.0) / 255,
                green: CGFloat(rgb.1) / 255,
                blue: CGFloat(rgb.2) / 255,
                alpha: 1
            )
        })
        #else
        self.init(uiColor: UIColor { traits in
            let rgb = traits.userInterfaceStyle == .dark ? dark : light
            return UIColor(
                red: CGFloat(rgb.0) / 255,
                green: CGFloat(rgb.1) / 255,
                blue: CGFloat(rgb.2) / 255,
                alpha: 1
            )
        })
        #endif
    }
}
