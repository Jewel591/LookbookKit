// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "LookbookKit",
    platforms: [
        .iOS(.v18),
        .macOS(.v15),
    ],
    products: [
        .library(name: "LookbookKit", targets: ["LookbookKit"]),
    ],
    targets: [
        .target(name: "LookbookKit"),
        .testTarget(
            name: "LookbookKitTests",
            dependencies: ["LookbookKit"]
        ),
    ],
    swiftLanguageModes: [.v6]
)
