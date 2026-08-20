#!/usr/bin/env python3
"""Print drop-shadow call sites in a host app. Not a hard gate.

`.lookbook(.cursor)` cannot turn off shadows in the subtree. Agents use this
scan to find `.shadow(` and layer-shadow assignments so a Cursor look can
stay effectively 0-shadow.

A hit on the same line or the previous line with
`// lookbook-shadow-exempt: <reason>` is still printed, under Exempted.
An empty reason does not exempt. Agents must not add that comment
until Ivens confirms the specific site.

Usage:
    python3 scripts/lookbook-shadow-candidates.py /path/to/HostApp
"""

from __future__ import annotations

import argparse
import re
import sys
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
}

SWIFTUI_SHADOW = re.compile(r"\.shadow\s*\(")
LAYER_SHADOW = re.compile(
    r"\blayer\.shadow(?:Color|Offset|Radius|Opacity|Path)\b"
    r"|\.shadow(?:Color|Offset|Radius|Opacity|Path)\s*="
)
NSSHADOW = re.compile(r"\bNSShadow\b")
EXEMPT = re.compile(r"lookbook-shadow-exempt:\s*(.+)$")
EXEMPT_COMMENT = re.compile(
    r"\s*(?://|/\*)\s*lookbook-shadow-exempt:\s*.+?(?:\*/)?\s*$"
)


def iter_swift_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.swift"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def is_shadow_line(line: str) -> bool:
    return bool(
        SWIFTUI_SHADOW.search(line)
        or LAYER_SHADOW.search(line)
        or NSSHADOW.search(line)
    )


def exemption_reason(line: str) -> str | None:
    match = EXEMPT.search(line)
    if match is None:
        return None
    reason = match.group(1).strip().removesuffix("*/").strip()
    return reason or None


def reason_for_hit(lines: list[str], index: int) -> str | None:
    current = exemption_reason(lines[index])
    if current is not None:
        return current
    if index == 0:
        return None
    previous = lines[index - 1]
    if is_shadow_line(previous):
        return None
    return exemption_reason(previous)


def collect(root: Path) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "swiftui": [],
        "layer": [],
        "nsshadow": [],
        "exempted": [],
    }
    for path in iter_swift_files(root):
        rel = path
        try:
            rel = path.relative_to(root)
        except ValueError:
            pass
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not is_shadow_line(line):
                continue
            source = EXEMPT_COMMENT.sub("", line).strip()
            loc = f"{rel}:{index + 1}:{source}"
            reason = reason_for_hit(lines, index)
            if reason is not None:
                buckets["exempted"].append(f"{loc}  [exempt: {reason}]")
                continue
            if SWIFTUI_SHADOW.search(line):
                buckets["swiftui"].append(loc)
            if LAYER_SHADOW.search(line):
                buckets["layer"].append(loc)
            if NSSHADOW.search(line):
                buckets["nsshadow"].append(loc)
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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List drop-shadow call sites. Not a hard gate."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Host app directory to scan (default: current directory)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    buckets = collect(root)
    open_count = (
        len(buckets["swiftui"]) + len(buckets["layer"]) + len(buckets["nsshadow"])
    )
    print(f"Scan root: {root}")
    print(
        f"Shadow candidates: {open_count} open, "
        f"{len(buckets['exempted'])} exempted"
    )
    print("Candidates only — review by hand. Not a hard gate.")
    print()
    print_bucket("SwiftUI .shadow(", buckets["swiftui"])
    print_bucket("CALayer / UIView shadow properties", buckets["layer"])
    print_bucket("NSShadow", buckets["nsshadow"])
    print_bucket("Exempted (lookbook-shadow-exempt)", buckets["exempted"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
