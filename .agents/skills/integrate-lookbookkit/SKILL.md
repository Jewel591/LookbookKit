---
name: integrate-lookbookkit
description: 在任何 Apple App 里实现、迁移或排查「按参考 App 对齐页面/Sheet 画布、分组表单表面、符号与 section header」时必须先加载：一律接 LookbookKit（Jewel591/LookbookKit），⛔ 不包 Form/List/Section/行，⛔ 不手写产品 hex，⛔ 不用 UIAppearance。覆盖标准接线、公开 SPM 版本范围、画布角色声明与候选扫描。
---

# LookbookKit 接入 skill

（本文件是 skill 正身；各机器 `~/.agents/skills/integrate-lookbookkit/` 只放指向这里的壳。）

全线 Apple App 的 look preset 唯一正身是 **[Jewel591/LookbookKit](https://github.com/Jewel591/LookbookKit)**
（本地 checkout：`~/Documents/DevProjects/LookbookKit`）。
范围裁决与不变式读 kit 仓库 `AGENTS.md`，用法读 `README.md`——本文件不复制正文。

## 何时触发

- 要把某页对齐 Cursor / Grok 等参考 App 的页面或 sheet 画布
- 宿主里出现 `lookbook` 前缀、产品 hex 背景、或手写 grouped 表单表面
- 排查 Form 背景盖不住、sheet 和页面同色、或导航栏与画布脱节

## 硬性规则

1. ⛔ 不把 `Form`、`List`、`Section` 或行包成 kit 组件。宿主页面继续写原生 SwiftUI。
2. 产品只在一处选择：scene 根 `.lookbook(_:)`。其他调用点只读 environment。
3. 每个画布自己声明角色：页面 `.lookbookSurface(.page)`，sheet `.lookbookSurface(.sheet)`。
4. 公开 API 一律 `lookbook` 前缀。⛔ 不要发明 `.lookbookCursorChrome()` 这类产品名修饰器。
5. 依赖必须是公开 GitHub + 自动兼容版本范围：
   `https://github.com/Jewel591/LookbookKit`，`from:` / Xcode *Up to Next Major Version*。
   ⛔ 不用 `exact`、`branch`、`revision`，也不要本地 path 进产品 main。
6. ⛔ 不要把产品 hex 抄进宿主视图。新参考 App = 新 `Look` preset；新视觉轴 = `Look` 上新属性并填齐所有 preset。
7. ⛔ 不用 UIAppearance，也不碰私有 list decoration view。
8. `scripts/lookbook-surface-candidates.py` 只报候选，不是硬闸；漏画布仍要人看。

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
