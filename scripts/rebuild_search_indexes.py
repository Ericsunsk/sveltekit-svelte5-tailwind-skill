#!/usr/bin/env python3
"""Rebuild index.jsonl, sections.jsonl, and index.meta.json for docs collections."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


COLLECTIONS = ("docs", "references")
SUMMARY_LIMIT = 240
HEADING_DEPTH = 2


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return compact(text)


def clip(text: str, limit: int = SUMMARY_LIMIT) -> str:
    text = compact(text)
    if len(text) <= limit:
        return text
    clipped = text[: limit - 1].rsplit(" ", 1)[0].strip()
    return f"{clipped}…"


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, 0

    data: dict[str, str] = {}
    for raw_line in lines[1:end]:
        line = raw_line.rstrip("\n")
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip().strip('"').strip("'")
        data[key] = value

    return data, end + 1


def collect_heading_offsets(lines: list[str], level: int = HEADING_DEPTH) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    fence = False
    prefix = "#" * level + " "

    for index, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if line.startswith(prefix):
            headings.append((index, line[len(prefix) :].strip()))

    return headings


def first_paragraph(lines: list[str]) -> str:
    fence = False
    paragraph: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            if paragraph:
                break
            continue
        if fence:
            continue
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith("#"):
            if paragraph:
                break
            continue
        if stripped.startswith(("<!--", "|")):
            continue
        if re.match(r"^[-*]\s", stripped) or re.match(r"^\d+\.\s", stripped):
            if paragraph:
                break
            continue
        paragraph.append(stripped)

    if paragraph:
        return clip(strip_markdown(" ".join(paragraph)))

    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped:
            return clip(strip_markdown(stripped))
    return ""


def build_entry(path: Path, relative_path: str) -> tuple[dict[str, str], dict[str, object]]:
    lines = path.read_text().splitlines(keepends=True)
    frontmatter, body_start = parse_frontmatter(lines)
    summary = frontmatter.get("summary") or first_paragraph(lines[body_start:])
    summary = clip(strip_markdown(summary))

    headings = collect_heading_offsets(lines)
    sections = []
    for idx, (offset, heading) in enumerate(headings):
        next_offset = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines) + 1
        limit = next_offset - offset
        section_body = lines[offset: next_offset - 1]
        section_summary = first_paragraph(section_body) or summary
        sections.append(
            {
                "heading": heading,
                "level": HEADING_DEPTH,
                "offset": offset,
                "limit": limit,
                "summary": section_summary,
            }
        )

    detailed_summary = summary
    if sections and sections[0]["summary"] != summary:
        detailed_summary = clip(f"{summary} {sections[0]['summary']}")

    index_entry = {
        "relative_path": relative_path,
        "summary": summary,
    }
    sections_entry = {
        "relative_path": relative_path,
        "detailed_summary": detailed_summary,
        "sections": sections,
    }
    return index_entry, sections_entry


def write_collection(root: Path, collection: str) -> None:
    collection_dir = root / collection
    if not collection_dir.exists():
        return

    files = sorted(
        path
        for path in collection_dir.glob("*.md")
        if path.name not in {"README.md"}
    )

    index_entries = []
    sections_entries = []
    for index, path in enumerate(files, start=1):
        relative_path = path.relative_to(collection_dir).as_posix()
        index_entry, sections_entry = build_entry(path, relative_path)
        index_entry["index"] = index
        sections_entry["index"] = index
        index_entries.append(index_entry)
        sections_entries.append(sections_entry)

    (collection_dir / "index.jsonl").write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in index_entries)
    )
    (collection_dir / "sections.jsonl").write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in sections_entries)
    )

    meta_path = collection_dir / "index.meta.json"
    distribution = "author-only"
    if meta_path.exists():
        try:
            distribution = json.loads(meta_path.read_text()).get("distribution", distribution)
        except json.JSONDecodeError:
            pass

    meta = {
        "indexed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "heading_depth": HEADING_DEPTH,
        "distribution": distribution,
        "file_count": len(files),
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    for collection in COLLECTIONS:
        write_collection(root, collection)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
