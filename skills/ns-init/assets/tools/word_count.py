#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Count effective novel text in Markdown chapters.

Default behavior counts only the `## 正文` section when it exists. This keeps
writing goals, notes, and chapter backwrite blocks out of the reported number.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CJK_CHAR_PATTERN = re.compile(
    "[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff"
    "\U00020000-\U0002ebef]"
)
LATIN_OR_NUMBER_PATTERN = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,:/-]\d+)*")
PLACEHOLDER_PATTERNS = [
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("待补", re.compile(r"(待补|待完善|待续写|待扩写)")),
    ("在这里写", re.compile(r"(在这里写|此处写|这里补)")),
    ("略", re.compile(r"([\[【(（]\s*略\s*[\]】)）]|此处略|下略|略写)")),
]
PLACEHOLDER_LINE_PATTERN = re.compile(
    r"^[\[【(（]?\s*(TODO|待补|待完善|待续写|待扩写|在这里写|此处写|这里补|略|此处略|下略|略写)\s*[\]】)）]?$",
    re.IGNORECASE,
)


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A\s*---\s*\n[\s\S]*?\n---\s*", "", text.replace("\ufeff", ""))


def extract_body_section(text: str) -> str:
    """Return content below `## 正文` until the next level-2 heading."""
    text = strip_frontmatter(text)
    match = re.search(r"(?m)^##\s*正文\s*$", text)
    if not match:
        return text
    rest = text[match.end() :]
    next_heading = re.search(r"(?m)^##\s+", rest)
    return rest[: next_heading.start()] if next_heading else rest


def countable_text(text: str, include_all: bool = False) -> str:
    text = strip_frontmatter(text) if include_all else extract_body_section(text)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)

    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^#{1,6}\s+", stripped):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            continue
        if re.match(r"^[-:| ]{3,}$", stripped):
            continue
        if re.match(r"^[-*+]\s+\[[ xX]\]\s+", stripped):
            continue
        if PLACEHOLDER_LINE_PATTERN.match(stripped):
            continue
        stripped = re.sub(r"^>\s*", "", stripped)
        lines.append(stripped)
    return "\n".join(lines)


def metrics_for_text(text: str, include_all: bool = False) -> dict[str, int]:
    plain = countable_text(text, include_all=include_all)
    cjk_count = len(CJK_CHAR_PATTERN.findall(plain))
    latin_or_number_count = len(LATIN_OR_NUMBER_PATTERN.findall(plain))
    visible_count = len(re.sub(r"\s+", "", plain))
    return {
        "effective": cjk_count + latin_or_number_count,
        "cjk": cjk_count,
        "latin_or_number": latin_or_number_count,
        "visible": visible_count,
    }


def placeholder_markers(text: str) -> list[str]:
    return [label for label, pattern in PLACEHOLDER_PATTERNS if pattern.search(text)]


def status_for(count: int, minimum: int | None, maximum: int | None) -> tuple[str, str]:
    if minimum is not None and count < minimum:
        return "偏少", f"还差 {minimum - count} 字"
    if maximum is not None and count > maximum:
        return "偏长", f"超出 {count - maximum} 字"
    return "达标", ""


def iter_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in {".md", ".markdown"}))
    return sorted(dict.fromkeys(files))


def audit_file(path: Path, minimum: int | None, maximum: int | None, include_all: bool) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    metrics = metrics_for_text(text, include_all=include_all)
    status, detail = status_for(metrics["effective"], minimum, maximum)
    return {
        "file": str(path),
        "status": status,
        "detail": detail,
        "metrics": metrics,
        "placeholders": placeholder_markers(text),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="统计小说 Markdown 正文有效字数。")
    parser.add_argument("paths", nargs="+", help="章节文件或目录，可传多个。")
    parser.add_argument("--min", type=int, default=None, help="最低有效字数。")
    parser.add_argument("--max", type=int, default=None, help="最高有效字数。")
    parser.add_argument("--include-all", action="store_true", help="统计整个 Markdown，而不是只统计 ## 正文。")
    parser.add_argument("--json", action="store_true", help="输出 JSON。")
    args = parser.parse_args()

    files = iter_markdown_files([Path(p) for p in args.paths])
    results = [audit_file(path, args.min, args.max, args.include_all) for path in files]
    total = sum(int(item["metrics"]["effective"]) for item in results)
    payload = {
        "counting_scope": "all_markdown" if args.include_all else "body_section",
        "total_effective": total,
        "files": results,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("未找到 Markdown 文件。")
        return 0

    for item in results:
        metrics = item["metrics"]
        print(f"{item['file']}: {metrics['effective']} 字，{item['status']}" + (f"（{item['detail']}）" if item["detail"] else ""))
        if item["placeholders"]:
            print(f"  疑似占位: {', '.join(item['placeholders'])}")
    print(f"合计有效字数: {total}")
    print("统计口径: 默认只统计 `## 正文`，排除 frontmatter、标题、表格、代码块、待办项、纯占位行、空白和标点。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
