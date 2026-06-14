#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def find_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return index

    return -1


def validate_file(path):
    errors = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError as exc:
        return [f"{path}: invalid UTF-8: {exc}"]

    end = find_frontmatter(lines)
    if end is None:
        return errors
    if end == -1:
        return [f"{path}:1:1: frontmatter starts with --- but has no closing ---"]

    frontmatter = "".join(lines[1:end])
    try:
        data = yaml.safe_load(frontmatter) if frontmatter.strip() else {}
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        if mark is not None:
            line = mark.line + 2
            column = mark.column + 1
            message = getattr(exc, "problem", None) or str(exc)
            return [f"{path}:{line}:{column}: invalid YAML frontmatter: {message}"]
        return [f"{path}: invalid YAML frontmatter: {exc}"]

    if data is not None and not isinstance(data, dict):
        errors.append(f"{path}:1:1: frontmatter must be a YAML mapping")

    return errors


def markdown_files(root):
    if root.is_file():
        if root.suffix == ".md":
            yield root
        return

    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            yield path


def main():
    parser = argparse.ArgumentParser(description="Validate YAML frontmatter in Markdown files.")
    parser.add_argument("paths", nargs="*", type=Path, default=[Path("docs")], help="Files or directories to validate.")
    args = parser.parse_args()

    errors = []
    for root in args.paths:
        for path in markdown_files(root):
            errors.extend(validate_file(path))

    if errors:
        print("Frontmatter validation failed:", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Frontmatter validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
