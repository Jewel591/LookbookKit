import SwiftUI

struct LookbookFormStyle: FormStyle {
    func makeBody(configuration: Configuration) -> some View {
        LookbookStyledForm(configuration: configuration)
    }
}

private struct LookbookStyledForm: View {
    let configuration: FormStyleConfiguration
    @Environment(\.lookbook) private var look
    @Environment(\.lookbookSurface) private var surface

    var body: some View {
        Form(configuration)
            .formStyle(.grouped)
            .modifier(LookbookCanvasModifier(look: look, surface: surface))
    }
}

struct LookbookCanvasModifier: ViewModifier {
    let look: Look
    let surface: LookbookSurface

    func body(content: Content) -> some View {
        content
            .scrollContentBackground(.hidden)
            .background {
                look.canvas(for: surface)
                    .ignoresSafeArea()
            }
    }
}
