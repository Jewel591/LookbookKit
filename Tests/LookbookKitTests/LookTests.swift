import Testing
@testable import LookbookKit

@Test
func productPresetsAreDistinct() {
    #expect(Look.cursor != .grok)
    #expect(Look.cursor != .systemGrouped)
    #expect(Look.grok != .systemGrouped)
    #expect(Look.groupedBright == .grok)
    #expect(Look.cursor.id == "cursor")
    #expect(Look.grok.id == "grok")
    #expect(Look.systemGrouped.id == "systemGrouped")
}

@Test
func presetsListIsTheSwitchableSet() {
    #expect(Look.presets == [.systemGrouped, .cursor, .grok])
}

@Test
func grokUsesHeavierTypeAndSymbolsThanSystemGrouped() {
    #expect(Look.grok.symbolWeight == .semibold)
    #expect(Look.systemGrouped.symbolWeight == .regular)
    #expect(Look.grok.symbolScale == .large)
}

@Test
func cursorKeepsToolbarTitlesInline() {
    #expect(Look.cursor.toolbarTitleDisplayMode == .inline)
    #expect(Look.systemGrouped.toolbarTitleDisplayMode == .automatic)
    #expect(Look.grok.toolbarTitleDisplayMode == .automatic)
}

@Test
func looksCompareByIdentityOnly() {
    let copy = Look(
        id: Look.cursor.id,
        pageBackground: Look.systemGrouped.pageBackground,
        sheetBackground: Look.systemGrouped.sheetBackground,
        sectionHeaderFont: Look.systemGrouped.sectionHeaderFont,
        symbolWeight: .regular,
        symbolScale: .small
    )
    #expect(copy == .cursor)
}

@Test
func omittedSheetBackgroundMatchesPage() {
    let look = Look(
        id: "singleCanvas",
        pageBackground: Look.systemGrouped.pageBackground,
        sectionHeaderFont: Look.systemGrouped.sectionHeaderFont,
        symbolWeight: .regular,
        symbolScale: .large
    )
    #expect(look.canvas(for: .page) == look.pageBackground)
    #expect(look.canvas(for: .sheet) == look.pageBackground)
}
