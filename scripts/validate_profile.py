#!/usr/bin/env python3
"""Validate the profile repository's Markdown without third-party dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:")


def markdown_files(root: Path) -> list[Path]:
    files = []
    readme = root / "README.md"
    if readme.exists():
        files.append(readme)
    docs = root / "docs"
    if docs.exists():
        files.extend(sorted(path for path in docs.rglob("*.md") if path.is_file()))
    return files


def lines_outside_fences(text: str):
    fence: str | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield line_number, line


def local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if not target or target.startswith("#") or target.startswith(EXTERNAL_PREFIXES):
        return None

    # Remove an optional Markdown title after a whitespace separator.
    target = target.split(maxsplit=1)[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    target = unquote(target)
    return target or None


def validate_file(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path.relative_to(root)}: not valid UTF-8 ({exc})"]

    relative = path.relative_to(root)
    if "\x00" in text:
        errors.append(f"{relative}: contains a NUL byte")
    if text and not text.endswith("\n"):
        errors.append(f"{relative}: missing final newline")

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip(" \t"):
            errors.append(f"{relative}:{line_number}: trailing whitespace")

    for line_number, line in lines_outside_fences(text):
        for match in LINK_RE.finditer(line):
            target = local_link_target(match.group(1))
            if target is None:
                continue
            candidate = (root / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
            if not candidate.resolve().exists():
                errors.append(f"{relative}:{line_number}: missing local link target {target!r}")

    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    files = markdown_files(root)
    if not files:
        return ["no Markdown files found under README.md or docs/"]

    errors: list[str] = []
    for path in files:
        errors.extend(validate_file(path, root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()

    errors = validate(args.root)
    if errors:
        print("Profile documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Profile documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
