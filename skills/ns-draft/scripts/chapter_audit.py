#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Quickly audit a drafted chapter for length and common placeholders."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def chinese_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main() -> int:
    parser = argparse.ArgumentParser(description="检查章节字数和明显占位内容。")
    parser.add_argument("chapter")
    parser.add_argument("--min", type=int, default=2500)
    parser.add_argument("--max", type=int, default=5000)
    args = parser.parse_args()

    path = Path(args.chapter)
    text = path.read_text(encoding="utf-8")
    count = chinese_chars(text)
    markers = [item for item in ["T" + "ODO", "待补", "在这里写", "略"] if item in text]

    print(f"文件: {path}")
    print(f"中文字符数: {count}")
    print(f"目标范围: {args.min}-{args.max}")
    if markers:
        print(f"疑似占位: {', '.join(markers)}")
    if count < args.min:
        print("建议: 扩写场景推进、冲突反应、人物选择和后果余波。")
    elif count > args.max:
        print("建议: 精简重复解释、弱相关背景和过长心理旁白。")
    else:
        print("字数: 达标")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
