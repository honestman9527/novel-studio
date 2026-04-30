#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Export publishable Novel Studio text by collecting only `## 正文` sections."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


SHARED_SCRIPT_DIR = Path(__file__).resolve().parents[2] / "ns" / "scripts"
if str(SHARED_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPT_DIR))

from ns_text_metrics import body_section


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---\s*\n(?P<yaml>[\s\S]*?)\n---\s*\n?", text.replace("\ufeff", ""))
    if not match:
        return {}, text
    return parse_simple_yaml(match.group("yaml")), text[match.end() :]


def parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith(" "):
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        value = value.strip().strip('"').strip("'")
        if value.isdigit():
            data[key.strip()] = int(value)
        else:
            data[key.strip()] = value
    return data


def h1(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def title_from_index(path: Path) -> str:
    index = path / "_index.md"
    if not index.exists():
        return path.name
    meta, body = split_frontmatter(index.read_text(encoding="utf-8"))
    return str(h1(body) or meta.get("title") or path.name)


def chapter_files(root: Path) -> list[Path]:
    content = root / "content"
    if not content.exists():
        return []
    files = [p for p in content.rglob("*.md") if p.name != "_index.md"]

    def key(path: Path) -> tuple[str, int, str]:
        meta, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        volume = str(meta.get("volume_id") or path.parent.name)
        order = meta.get("chapter_number") or 999999
        try:
            order = int(order)
        except (TypeError, ValueError):
            order = 999999
        return (volume, order, path.as_posix())

    return sorted(files, key=key)


def render(root: Path, fmt: str, include_titles: bool) -> str:
    chunks: list[str] = []
    current_volume = ""
    for path in chapter_files(root):
        text = path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(text)
        volume_id = str(meta.get("volume_id") or path.parent.name)
        if include_titles and volume_id != current_volume:
            current_volume = volume_id
            volume_label = title_from_index(path.parent)
            chunks.append(f"## {volume_label}" if fmt == "markdown" else volume_label)
        title = str(h1(body) or meta.get("title") or path.stem)
        story = body_section(text).strip()
        if include_titles:
            chunks.append(f"### {title}" if fmt == "markdown" else title)
        chunks.append(story)
    separator = "\n\n" if fmt == "markdown" else "\n\n"
    return separator.join(chunk for chunk in chunks if chunk.strip()) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="导出只包含 `## 正文` 的发布稿。")
    parser.add_argument("root", nargs="?", default=".", help="小说项目根目录。")
    parser.add_argument("-o", "--output", help="输出文件；不传则打印到 stdout。")
    parser.add_argument("--format", choices=["markdown", "txt"], default="markdown")
    parser.add_argument("--no-titles", action="store_true", help="不输出卷标题和章节标题。")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = render(root, args.format, not args.no_titles)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(f"Exported {path}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
