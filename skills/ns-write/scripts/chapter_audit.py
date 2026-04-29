#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Quickly audit drafted chapters for effective story length and placeholders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SHARED_SCRIPT_DIR = Path(__file__).resolve().parents[2] / "ns" / "scripts"
if str(SHARED_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPT_DIR))

from ns_text_metrics import effective_word_metrics, placeholder_markers


def count_status(count: int, minimum: int, maximum: int) -> tuple[str, str]:
    if minimum <= count <= maximum:
        return "达标", ""
    if count < minimum:
        gap = minimum - count
        return "偏少", f"还差约 {gap} 字。"
    gap = count - maximum
    return "偏长", f"超出约 {gap} 字。"


def iter_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in {".md", ".markdown"}))
    return sorted(dict.fromkeys(files))


def audit_file(path: Path, minimum: int, maximum: int, include_all: bool) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    metrics = effective_word_metrics(text, include_all=include_all)
    count = metrics["effective"]
    markers = placeholder_markers(text)
    status, detail = count_status(count, minimum, maximum)
    return {
        "file": str(path),
        "status": status,
        "detail": detail,
        "target": {"min": minimum, "max": maximum},
        "metrics": metrics,
        "placeholders": markers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查章节字数和明显占位内容。")
    parser.add_argument("paths", nargs="+", help="章节文件或目录，可传多个。")
    parser.add_argument("--min", type=int, default=2500)
    parser.add_argument("--max", type=int, default=5000)
    parser.add_argument("--include-all", action="store_true", help="统计整个 Markdown，而不是只统计 ## 正文。")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出统计结果，便于脚本集成。")
    args = parser.parse_args()

    files = iter_markdown_files([Path(p) for p in args.paths])
    results = [audit_file(path, args.min, args.max, args.include_all) for path in files]
    total = sum(int(item["metrics"]["effective"]) for item in results)

    if args.json:
        print(
            json.dumps(
                {
                    "counting_scope": "all_markdown" if args.include_all else "body_section",
                    "total_effective": total,
                    "files": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not results:
        print("未找到 Markdown 文件。")
        return 0

    for item in results:
        metrics = item["metrics"]
        print(f"文件: {item['file']}")
        print(f"有效字数: {metrics['effective']}")
        print(f"统计明细: 中日韩文字 {metrics['cjk']}，英文/数字词 {metrics['latin_or_number']}，非空可见字符 {metrics['visible']}")
        print("统计口径: 默认只统计 `## 正文`；排除 frontmatter、Markdown 标题、表格、代码块、待办项和纯占位行；不计空白和标点。")
        print(f"目标范围: {args.min}-{args.max}")
        if item["placeholders"]:
            print(f"疑似占位: {', '.join(item['placeholders'])}")
        print(f"字数: {item['status']}" + (f"（{item['detail']}）" if item["detail"] else ""))
        if item["status"] == "偏少":
            print("建议: 扩写场景推进、冲突反应、人物选择和后果余波。")
        elif item["status"] == "偏长":
            print("建议: 精简重复解释、弱相关背景和过长心理旁白。")
        else:
            print("建议: 保持当前篇幅，重点复核动机、节奏和结尾钩子。")
        print()
    print(f"合计有效字数: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
