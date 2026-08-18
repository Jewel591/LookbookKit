#!/usr/bin/env python3
"""Print candidate sites that may need `.lookbookSurface`. Not a hard gate.

Usage:
    python3 scripts/lookbook-surface-candidates.py /path/to/HostApp
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".build",
    "DerivedData",
    "Pods",
    "build",
}

PRESENTATION = re.compile(
    r"\.(sheet|fullScreenCover|popover)\s*\("
)
CANVAS_PAINT = re.compile(
    r"\.lookbookSurface\s*\(|\.lookbook\s*\("
)
LEFTOVER_GROUND = re.compile(
    r"Theme\.ground|systemGroupedBackground"
)
CHIP_OR_DECORATION = re.compile(
    r"in:\s*Capsule|in:\s*Circle|in:\s*RoundedRectangle|\.fill\(Theme\.ground|stroke(?:Border)?\(.*Theme\.ground|static let ground"
)


def iter_swift_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.swift"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def collect(root: Path) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "presentations": [],
        "leftover_grounds": [],
        "lookbook_surfaces": [],
    }
    for path in iter_swift_files(root):
        rel = path
        try:
            rel = path.relative_to(root)
        except ValueError:
            pass
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            loc = f"{rel}:{index}:{stripped}"
            if PRESENTATION.search(line):
                buckets["presentations"].append(loc)
            if CANVAS_PAINT.search(line):
                buckets["lookbook_surfaces"].append(loc)
            if LEFTOVER_GROUND.search(line) and not CHIP_OR_DECORATION.search(line):
                buckets["leftover_grounds"].append(loc)
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
        description="List candidate Lookbook canvas sites. Not a hard gate."
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
    print(f"Scan root: {root}")
    print("Candidates only — review by hand. Chip/card Theme.ground hits are skipped.")
    print()
    print_bucket("Presentations (.sheet / .fullScreenCover / .popover)", buckets["presentations"])
    print_bucket("Leftover full-bleed grounds (Theme.ground / systemGroupedBackground)", buckets["leftover_grounds"])
    print_bucket("Existing lookbook canvas paints", buckets["lookbook_surfaces"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
