#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Collect unresolved threads from optional chapter notes and continuity.yaml."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ThreadItem:
    text: str
    source: str
    kind: str


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def note_block(text: str) -> str:
    match = re.search(r"(?ms)^##\s*章末笔记\s*$([\s\S]*?)(?=^##\s+|\Z)", text)
    if not match:
        return ""
    return match.group(1)


def scalar_or_list_values(text: str, keys: set[str]) -> list[str]:
    values: list[str] = []
    current_key = ""
    current_indent = 0
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" in line and not line.startswith("- "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_indent = indent
            if current_key in keys and value.strip():
                values.append(value.strip().strip('"').strip("'"))
            continue
        if line.startswith("- ") and current_key in keys and indent > current_indent:
            value = line[2:].strip().strip('"').strip("'")
            if value:
                values.append(value)
    return values


def markdown_note_values(text: str, labels: set[str]) -> list[str]:
    values: list[str] = []
    current_label = ""
    normalized = {label.rstrip("：:") for label in labels}

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        heading = re.match(r"^#{3,6}\s+(.+?)\s*$", line)
        if heading:
            label = heading.group(1).strip().rstrip("：:")
            current_label = label if label in normalized else ""
            continue
        item = re.match(r"^[-*+]\s+(.+)$", line)
        if not item:
            continue
        body = item.group(1).strip()
        label_match = re.match(r"^([^：:]{2,12})[：:]\s*(.*)$", body)
        if label_match:
            label = label_match.group(1).strip().rstrip("：:")
            value = label_match.group(2).strip()
            if label in normalized and value:
                values.append(value)
            current_label = label if label in normalized else ""
        elif current_label:
            values.append(body)
    return values


def chapter_files(root: Path) -> list[Path]:
    content = root / "content"
    if not content.exists():
        return []
    return sorted(p for p in content.rglob("*.md") if p.name != "_index.md")


def collect(root: Path) -> dict[str, Any]:
    opened: list[ThreadItem] = []
    resolved: list[ThreadItem] = []
    hooks: list[ThreadItem] = []

    for path in chapter_files(root):
        text = path.read_text(encoding="utf-8")
        block = note_block(text)
        source = rel(path, root)
        if not block:
            continue
        for item in markdown_note_values(block, {"未收束", "未解决", "待确认", "悬念"}):
            opened.append(ThreadItem(item, source, "chapter_open_thread"))
        for item in markdown_note_values(block, {"已解决", "已收束"}):
            resolved.append(ThreadItem(item, source, "chapter_resolved_thread"))
        for item in markdown_note_values(block, {"下一章钩子", "下章钩子", "下章"}):
            hooks.append(ThreadItem(item, source, "next_hook"))

    continuity = root / "novel-studio" / "continuity.yaml"
    if continuity.exists():
        text = continuity.read_text(encoding="utf-8")
        for item in scalar_or_list_values(text, {"loose_threads", "open_threads", "unresolved_threads"}):
            opened.append(ThreadItem(item, rel(continuity, root), "continuity_thread"))
        for item in scalar_or_list_values(text, {"resolved_threads"}):
            resolved.append(ThreadItem(item, rel(continuity, root), "continuity_resolved_thread"))

    resolved_text = {item.text for item in resolved}
    unresolved = [item for item in opened if item.text not in resolved_text]
    return {
        "ok": not unresolved,
        "unresolved": [item.__dict__ for item in unresolved],
        "resolved": [item.__dict__ for item in resolved],
        "next_hooks": [item.__dict__ for item in hooks],
        "counts": {
            "unresolved": len(unresolved),
            "resolved": len(resolved),
            "next_hooks": len(hooks),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="汇总可选章末笔记和 continuity.yaml 中的未收束线索。")
    parser.add_argument("root", nargs="?", default=".", help="小说项目根目录。")
    parser.add_argument("--json", action="store_true", help="输出 JSON。")
    parser.add_argument("--strict", action="store_true", help="存在未收束线索时返回非零。")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data = collect(root)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        counts = data["counts"]
        print(f"Continuity: {counts['unresolved']} unresolved, {counts['next_hooks']} hooks")
        for item in data["unresolved"]:
            print(f"[open] {item['source']}: {item['text']}")
        for item in data["next_hooks"]:
            print(f"[hook] {item['source']}: {item['text']}")
    return 1 if args.strict and not data["ok"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
