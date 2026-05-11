#!/usr/bin/env python3
"""
Report Markdown translation coverage for the documentation tree.

Coverage is based on English Markdown source files under docs/en. A localized
page counts as present when the same relative Markdown path exists under the
target language directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def markdown_files(directory: Path) -> set[str]:
    if not directory.exists():
        return set()
    return {path.relative_to(directory).as_posix() for path in directory.rglob("*.md")}


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").strip()


def count_by_section(paths: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in paths:
        section = path.split("/", 1)[0]
        counts[section] = counts.get(section, 0) + 1
    return counts


def format_sections(counts: dict[str, int]) -> str:
    if not counts:
        return "-"
    return ", ".join(f"{name}:{counts[name]}" for name in sorted(counts))


def load_languages(docs_dir: Path) -> dict[str, dict]:
    languages_path = docs_dir / "languages.json"
    with languages_path.open(encoding="utf-8") as file:
        return json.load(file)["languages"]


def build_report(docs_dir: Path, source_lang: str, active_only: bool) -> tuple[list[str], list[dict]]:
    languages = load_languages(docs_dir)
    source_dir = docs_dir / source_lang
    source_files = sorted(markdown_files(source_dir))
    source_set = set(source_files)

    rows = []
    for code, metadata in languages.items():
        if code == source_lang:
            continue
        if active_only and not metadata.get("active", False):
            continue

        target_dir = docs_dir / code
        target_set = markdown_files(target_dir)
        present = sorted(source_set & target_set)
        missing = sorted(source_set - target_set)
        extra = sorted(target_set - source_set)

        exact_english = []
        empty_exact = []
        for path in present:
            source_text = normalized_text(source_dir / path)
            target_text = normalized_text(target_dir / path)
            if source_text == target_text:
                if source_text:
                    exact_english.append(path)
                else:
                    empty_exact.append(path)

        strict_translated = len(present) - len(exact_english)
        rows.append(
            {
                "code": code,
                "name": metadata.get("name", code),
                "active": metadata.get("active", False),
                "present": present,
                "missing": missing,
                "extra": extra,
                "exact_english": exact_english,
                "empty_exact": empty_exact,
                "translated_count": strict_translated,
                "present_count": len(present),
                "coverage": strict_translated / len(source_files) * 100 if source_files else 0,
                "present_coverage": len(present) / len(source_files) * 100 if source_files else 0,
            }
        )

    rows.sort(
        key=lambda row: (
            row["translated_count"],
            row["present_count"],
            -len(row["missing"]),
            row["code"],
        ),
        reverse=True,
    )
    return source_files, rows


def print_summary(source_files: list[str], rows: list[dict]) -> None:
    source_counts = count_by_section(source_files)
    print(f"English Markdown source pages: {len(source_files)} ({format_sections(source_counts)})")
    print()
    print(
        "Rank  Lang  Active  Translated  Present  Missing  Extra  "
        "Coverage  Present coverage  Sections present"
    )
    print("-" * 112)
    for index, row in enumerate(rows, start=1):
        sections = format_sections(count_by_section(row["present"]))
        print(
            f"{index:>4}  {row['code']:<4}  {str(row['active']):<6}  "
            f"{row['translated_count']:>10}/{len(source_files):<3}  "
            f"{row['present_count']:>7}  {len(row['missing']):>7}  {len(row['extra']):>5}  "
            f"{row['coverage']:>7.2f}%  {row['present_coverage']:>15.2f}%  {sections}"
        )
        if row["exact_english"]:
            print(f"      exact English copies: {', '.join(row['exact_english'])}")


def print_details(rows: list[dict]) -> None:
    for row in rows:
        print()
        print(f"[{row['code']}] {row['name']}")
        print(f"Existing source-matched translations ({len(row['present'])}):")
        for path in row["present"]:
            print(f"  {path}")
        print(f"Missing source pages ({len(row['missing'])}):")
        for path in row["missing"]:
            print(f"  {path}")
        print(f"Extra localized pages without English source ({len(row['extra'])}):")
        for path in row["extra"]:
            print(f"  {path}")
        if row["empty_exact"]:
            print(f"Empty exact matches ({len(row['empty_exact'])}):")
            for path in row["empty_exact"]:
                print(f"  {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report documentation translation coverage.")
    parser.add_argument("--docs-dir", default="docs", type=Path, help="Documentation root directory.")
    parser.add_argument("--source-lang", default="en", help="Source language directory.")
    parser.add_argument("--active-only", action="store_true", help="Only include active languages.")
    parser.add_argument("--details", action="store_true", help="Print exact existing, missing, and extra paths.")
    args = parser.parse_args()

    source_files, rows = build_report(args.docs_dir, args.source_lang, args.active_only)
    print_summary(source_files, rows)
    if args.details:
        print_details(rows)


if __name__ == "__main__":
    main()
