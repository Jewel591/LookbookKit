---
name: integrate-lookbookkit
description: 仅在宿主主动要按参考 App 对齐页面/Sheet 画布时加载。LookbookKit（Jewel591/LookbookKit）是可选 beta kit，不是全线必备配置，⛔ 不要为「是否接入」加 playbook lint。接入后：⛔ 不包 Form/List/Section/行，⛔ 不手写产品 hex，⛔ 不用 UIAppearance。
---

# LookbookKit 接入 skill

（本文件是 skill 正身；各机器 `~/.agents/skills/integrate-lookbookkit/` 只放指向这里的壳。）

**[Jewel591/LookbookKit](https://github.com/Jewel591/LookbookKit)** 是可选 beta
（本地 checkout：`~/Documents/DevProjects/LookbookKit`）。
不是 SupportKit / AppContextKit 那种全线必备能力。没决定对齐参考画布就不要接，也不要为此开装配闸。
范围裁决与不变式读 kit 仓库 `AGENTS.md`，用法读 `README.md`——本文件不复制正文。

## 何时触发

- 宿主**已经决定**要把某页对齐 Cursor / Grok 等参考 App 的页面或 sheet 画布
- 宿主里已经出现 `lookbook` 前缀，要改接线或排错
- 排查已接入后的 Form 背景、sheet 与页面同色、或导航栏与画布脱节

⛔ 不要因为「这是新 App」或「别的 kit 都接了」就自动接入。

## 硬性规则

1. 可选：未接入是合法状态。⛔ 不写 playbook lint 检查是否 `import LookbookKit` / 是否 `.lookbook(`。
2. 一旦接入，⛔ 不把 `Form`、`List`、`Section` 或行包成 kit 组件。宿主页面继续写原生 SwiftUI。
3. 产品只在一处选择：scene 根 `.lookbook(_:)`。其他调用点只读 environment。
4. 每个画布自己声明角色：页面 `.lookbookSurface(.page)`，sheet `.lookbookSurface(.sheet)`。
5. 公开 API 一律 `lookbook` 前缀。⛔ 不要发明 `.lookbookCursorChrome()` 这类产品名修饰器。
6. 依赖用公开 GitHub + 自动兼容版本范围：
   `https://github.com/Jewel591/LookbookKit`，`from:` / Xcode *Up to Next Major Version*。
   ⛔ 不用 `exact`、`branch`、`revision`。试验仓可用本地 path；产品 main 不要长期挂 path。
7. ⛔ 不要把产品 hex 抄进宿主视图。新参考 App = 新 `Look` preset；新视觉轴 = `Look` 上新属性并填齐所有 preset。
8. ⛔ 不用 UIAppearance，也不碰私有 list decoration view。
9. `scripts/lookbook-surface-candidates.py` 只报候选，不是硬闸。

## 标准接线

```swift
import LookbookKit
import SwiftUI

WindowGroup {
    HomeView()
        .lookbook(.cursor)
}

ScrollView { … }
    .lookbookSurface(.page)

.sheet {
    SettingsView()
        .lookbookSurface(.sheet)
}
```

可选：`Section` header 上 `.lookbookSectionHeader()`，`Label` / `Image` 上 `.lookbookSymbol()`，拥有导航栏的画布上 `.lookbookToolbarBackground()`。
