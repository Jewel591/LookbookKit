import SwiftUI

public extension View {
    /// Chooses the product look for this hierarchy.
    ///
    /// Call once at the scene root. Canvases still declare
    /// ``lookbookSurface(_:)`` because child navigation stacks are opaque.
    /// Pass `surface:` when a preview or sheet must choose the look itself.
    func lookbook(_ look: Look, surface: LookbookSurface = .page) -> some View {
        self
            .environment(\.lookbook, look)
            .environment(\.lookbookSurface, surface)
            .formStyle(LookbookFormStyle())
            .modifier(LookbookCanvasModifier(look: look, surface: surface))
            .presentationBackground(look.canvas(for: surface))
    }

    /// Declares page vs sheet and paints that canvas from the current look.
    func lookbookSurface(_ surface: LookbookSurface) -> some View {
        modifier(LookbookSurfaceFromEnvironment(surface: surface))
    }

    func lookbookSectionHeader() -> some View {
        modifier(LookbookSectionHeaderModifier())
    }

    func lookbookSymbol() -> some View {
        modifier(LookbookSymbolModifier())
    }

    func lookbookToolbarBackground() -> some View {
        modifier(LookbookToolbarBackgroundModifier())
    }
}

private struct LookbookSurfaceFromEnvironment: ViewModifier {
    @Environment(\.lookbook) private var look
    let surface: LookbookSurface

    func body(content: Content) -> some View {
        content
            .environment(\.lookbookSurface, surface)
            .modifier(LookbookCanvasModifier(look: look, surface: surface))
            .presentationBackground(look.canvas(for: surface))
    }
}

private struct LookbookSectionHeaderModifier: ViewModifier {
    @Environment(\.lookbook) private var look

    func body(content: Content) -> some View {
        content
            .font(look.sectionHeaderFont)
            .foregroundStyle(.secondary)
            .textCase(nil)
    }
}

private struct LookbookSymbolModifier: ViewModifier {
    @Environment(\.lookbook) private var look

    func body(content: Content) -> some View {
        content
            .imageScale(look.symbolScale)
            .fontWeight(look.symbolWeight)
    }
}

private struct LookbookToolbarBackgroundModifier: ViewModifier {
    @Environment(\.lookbook) private var look
    @Environment(\.lookbookSurface) private var surface

    func body(content: Content) -> some View {
        let canvas = look.canvas(for: surface)
        #if os(iOS)
        content
            .toolbarBackground(canvas, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
        #else
        content
            .toolbarBackground(canvas, for: .windowToolbar)
        #endif
    }
}
