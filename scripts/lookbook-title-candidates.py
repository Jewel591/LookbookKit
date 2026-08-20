#!/usr/bin/env python3
"""Print page-title slot candidates in a host app. Not a hard gate.

Injection can set Cursor's inline *mode*. It cannot move a painted
`Text(title).font(.title2)` into `.navigationTitle`. Agents use this
scan to find page-sized views that still keep the title in the body.

A hit on the same line or the previous line with
`// lookbook-title-exempt: <reason>` is still printed, under Exempted.
An empty reason does not exempt. Agents must not add that comment
until Ivens confirms the specific site.

Usage:
    python3 scripts/lookbook-title-candidates.py /path/to/HostApp
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".build",
    ".swiftpm",
    "DerivedData",
    "Pods",
    "build",
    "SourcePackages",
    "Carthage",
    "node_modules",
    "Tests",
    "UITests",
    "Fixtures",
}

VIEW_TYPE = re.compile(
    r"^(?P<indent>[ \t]*)(?:public |internal |private |fileprivate )*"
    r"(?:struct|class|actor)\s+(?P<name>\w+)\s*:"
    r"[^{]*\bView\b",
    re.MULTILINE,
)
NAV_TITLE = re.compile(r"\.(?:navigationTitle|navigationBarTitle)\s*\(")
MODE_OVERRIDE = re.compile(
    r"\.(?:toolbarTitleDisplayMode|navigationBarTitleDisplayMode)\s*\("
)
PAGE_SIGNAL = re.compile(
    r"\.lookbookSurface\s*\("
    r"|\.toolbar\s*(\(|\{)"
    r"|\.navigationDestination\s*\("
    r"|\.navigationTitle\s*\("
    r"|\.navigationBarTitle\s*\("
)
# Hero / page titles. title3 is left out — it is usually a section.
DISPLAY_TITLE = re.compile(
    r"\.(?:appFont|font)\s*\(\s*\.\s*(?:largeTitle|title2|title)\b"
    r"|\.font\s*\(\s*\.system\s*\(\s*\.\s*(?:largeTitle|title2|title)\b"
)
EXEMPT = re.compile(r"lookbook-title-exempt:\s*(.+)$")
EXEMPT_COMMENT = re.compile(
    r"\s*(?://|/\*)\s*lookbook-title-exempt:\s*.+?(?:\*/)?\s*$"
)
PREVIEW_NAME = re.compile(r"(Preview|Previews)$")


def iter_swift_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.swift"):
        if any(
            part in SKIP_DIR_NAMES or part.endswith("Tests")
            for part in path.parts
        ):
            continue
        files.append(path)
    return sorted(files)


def matching_brace_end(text: str, open_idx: int) -> int | None:
    if open_idx >= len(text) or text[open_idx] != "{":
        return None
    depth = 0
    for index in range(open_idx, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    return None


def line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def line_number(starts: list[int], offset: int) -> int:
    lo, hi = 0, len(starts)
    while lo < hi:
        mid = (lo + hi) // 2
        if starts[mid] <= offset:
            lo = mid + 1
        else:
            hi = mid
    return lo


def iter_view_types(text: str) -> list[tuple[str, int, int]]:
    types: list[tuple[str, int, int]] = []
    for match in VIEW_TYPE.finditer(text):
        name = match.group("name")
        if PREVIEW_NAME.search(name):
            continue
        brace = text.find("{", match.end() - 1)
        if brace < 0:
            continue
        end = matching_brace_end(text, brace)
        if end is None:
            continue
        types.append((name, match.start(), end))
    return types


def innermost(types: list[tuple[str, int, int]], offset: int) -> str | None:
    found: tuple[str, int] | None = None
    for name, start, end in types:
        if start <= offset < end:
            span = end - start
            if found is None or span < found[1]:
                found = (name, span)
    return None if found is None else found[0]


def exemption_reason(line: str) -> str | None:
    match = EXEMPT.search(line)
    if match is None:
        return None
    reason = match.group(1).strip().removesuffix("*/").strip()
    return reason or None


def reason_for_hit(lines: list[str], index: int, hit_re: re.Pattern[str]) -> str | None:
    current = exemption_reason(lines[index])
    if current is not None:
        return current
    looked = 0
    walk = index - 1
    while walk >= 0 and looked < 3:
        raw = lines[walk]
        if hit_re.search(raw):
            return None
        reason = exemption_reason(raw)
        if reason is not None:
            return reason
        if raw.strip():
            looked += 1
        walk -= 1
    return None


def collect(root: Path) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "missing_slot": [],
        "competing": [],
        "mode_override": [],
        "exempted": [],
    }
    for path in iter_swift_files(root):
        rel = path
        try:
            rel = path.relative_to(root)
        except ValueError:
            pass
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        starts = line_starts(text)
        types = iter_view_types(text)
        if not types:
            continue

        per_type: dict[str, dict[str, list[tuple[int, str]]]] = {}
        for name, start, end in types:
            per_type[name] = {
                "display": [],
                "nav": [],
                "mode": [],
                "page": [],
            }
            body = text[start:end]
            if PAGE_SIGNAL.search(body):
                per_type[name]["page"].append((line_number(starts, start), name))

        for match in DISPLAY_TITLE.finditer(text):
            name = innermost(types, match.start())
            if name is None:
                continue
            line = line_number(starts, match.start())
            per_type[name]["display"].append((line, lines[line - 1].strip()))
        for match in NAV_TITLE.finditer(text):
            name = innermost(types, match.start())
            if name is None:
                continue
            line = line_number(starts, match.start())
            per_type[name]["nav"].append((line, lines[line - 1].strip()))
        for match in MODE_OVERRIDE.finditer(text):
            name = innermost(types, match.start())
            if name is None:
                continue
            line = line_number(starts, match.start())
            per_type[name]["mode"].append((line, lines[line - 1].strip()))

        for name, bits in per_type.items():
            if not bits["page"]:
                continue
            loc_prefix = f"{rel}:{name}"
            for line, source in bits["display"]:
                reason = reason_for_hit(lines, line - 1, DISPLAY_TITLE)
                loc = f"{loc_prefix}:{line}:{source}"
                if reason is not None:
                    buckets["exempted"].append(f"{loc}  [exempt: {reason}]")
                    continue
                if bits["nav"]:
                    buckets["competing"].append(loc)
                else:
                    buckets["missing_slot"].append(loc)
            for line, source in bits["mode"]:
                reason = reason_for_hit(lines, line - 1, MODE_OVERRIDE)
                loc = f"{loc_prefix}:{line}:{source}"
                if reason is not None:
                    buckets["exempted"].append(f"{loc}  [exempt: {reason}]")
                    continue
                buckets["mode_override"].append(loc)
    return buckets


def print_bucket(title: str, rows: list[str]) -> None:
    print(f"## {title} ({len(rows)})")
    if not rows:
        print("(none)")
        print()
        return
    for row in rows:
        print(row)
    print()


def selftest() -> int:
    failed = 0
    total = 0

    def check(name: str, ok: bool) -> None:
        nonlocal failed, total
        total += 1
        failed += 0 if ok else 1
        print(f"  [{'ok' if ok else 'FAIL'}] {name}")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "Pocket.swift").write_text(
            """
import SwiftUI
struct PocketDetailView: View {
    var title = "Camera"
    var body: some View {
        ScrollView {
            Text(title)
                .appFont(.title2, .heavy)
        }
        .lookbookSurface(.page)
        .toolbar { ToolbarItem { Button("More") {} } }
    }
}
""",
            encoding="utf-8",
        )
        (root / "Library.swift").write_text(
            """
import SwiftUI
struct LibraryView: View {
    var body: some View {
        ScrollView {
            Text("This week")
                .appFont(.title3, .bold)
        }
        .lookbookSurface(.page)
        .navigationTitle("Library")
    }
}
""",
            encoding="utf-8",
        )
        (root / "Compete.swift").write_text(
            """
import SwiftUI
struct SettingsView: View {
    var body: some View {
        VStack {
            Text("Settings")
                .font(.title)
        }
        .lookbookSurface(.page)
        .navigationTitle("Settings")
    }
}
""",
            encoding="utf-8",
        )
        (root / "Override.swift").write_text(
            """
import SwiftUI
struct NewsView: View {
    var body: some View {
        Text("News")
            .lookbookSurface(.page)
            .navigationTitle("News")
            .toolbarTitleDisplayMode(.inlineLarge)
    }
}
""",
            encoding="utf-8",
        )
        (root / "Row.swift").write_text(
            """
import SwiftUI
struct AppRow: View {
    var body: some View {
        Text("Cursor")
            .appFont(.title2, .bold)
    }
}
""",
            encoding="utf-8",
        )
        (root / "Exempt.swift").write_text(
            """
import SwiftUI
struct MetaphorView: View {
    var body: some View {
        ScrollView {
            // lookbook-title-exempt: open-pocket hero under the sleeve
            Text("Inbox")
                .appFont(.title2, .heavy)
        }
        .lookbookSurface(.page)
    }
}
""",
            encoding="utf-8",
        )
        buckets = collect(root)
        missing = " ".join(buckets["missing_slot"])
        competing = " ".join(buckets["competing"])
        overrides = " ".join(buckets["mode_override"])
        exempted = " ".join(buckets["exempted"])
        check("页内 title2 且无 navigationTitle 报 missing-slot",
              "PocketDetailView" in missing and "title2" in missing)
        check("title3 不当作页标题", "LibraryView" not in missing)
        check("有 navigationTitle 的普通页不报 missing-slot",
              "LibraryView" not in missing)
        check("页内 title + navigationTitle 报 competing",
              "SettingsView" in competing)
        check("宿主 toolbarTitleDisplayMode 报 mode-override",
              "inlineLarge" in overrides)
        check("无页面信号的行标题不报", "AppRow" not in missing)
        check("带理由的豁免进 Exempted",
              "MetaphorView" in exempted and not any(
                  "MetaphorView" in row for row in buckets["missing_slot"]
              ))

    print(f"{'✓' if failed == 0 else '✗'} lookbook-title-candidates selftest: "
          f"{total - failed}/{total}")
    return 0 if failed == 0 else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List page-title slot candidates. Not a hard gate."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Host app directory to scan (default: current directory)",
    )
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    buckets = collect(root)
    open_count = (
        len(buckets["missing_slot"])
        + len(buckets["competing"])
        + len(buckets["mode_override"])
    )
    print(f"Scan root: {root}")
    print(
        f"Title-slot candidates: {open_count} open, "
        f"{len(buckets['exempted'])} exempted"
    )
    print("Candidates only — review by hand. Not a hard gate.")
    print()
    print_bucket(
        "In-content title, no .navigationTitle",
        buckets["missing_slot"],
    )
    print_bucket(
        "In-content title competing with .navigationTitle",
        buckets["competing"],
    )
    print_bucket(
        "Host title-display-mode override",
        buckets["mode_override"],
    )
    print_bucket("Exempted (lookbook-title-exempt)", buckets["exempted"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
