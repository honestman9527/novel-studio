#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Quickly audit a drafted chapter for effective story length and placeholders."""

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


def main() -> int:
    parser = argparse.ArgumentParser(description="检查章节字数和明显占位内容。")
    parser.add_argument("chapter")
    parser.add_argument("--min", type=int, default=2500)
    parser.add_argument("--max", type=int, default=5000)
    parser.add_argument("--json", action="store_true", help="以 JSON 输出统计结果，便于脚本集成。")
    args = parser.parse_args()

    path = Path(args.chapter)
    text = path.read_text(encoding="utf-8")
    metrics = effective_word_metrics(text)
    count = metrics["effective"]
    markers = placeholder_markers(text)
    status, detail = count_status(count, args.min, args.max)

    if args.json:
        print(
            json.dumps(
                {
                    "file": str(path),
                    "status": status,
                    "detail": detail,
                    "target": {"min": args.min, "max": args.max},
                    "metrics": metrics,
                    "placeholders": markers,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return 0

    print(f"文件: {path}")
    print(f"有效字数: {count}")
    print(f"统计明细: 中日韩文字 {metrics['cjk']}，英文/数字词 {metrics['latin_or_number']}，非空可见字符 {metrics['visible']}")
    print("统计口径: 排除 Markdown 标题、表格、代码块、待办项和纯占位行；不计空白和标点。")
    print(f"目标范围: {args.min}-{args.max}")
    if markers:
        print(f"疑似占位: {', '.join(markers)}")
    print(f"字数: {status}" + (f"（{detail}）" if detail else ""))
    if status == "偏少":
        print("建议: 扩写场景推进、冲突反应、人物选择和后果余波。")
    elif status == "偏长":
        print("建议: 精简重复解释、弱相关背景和过长心理旁白。")
    else:
        print("建议: 保持当前篇幅，重点复核动机、节奏和结尾钩子。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
