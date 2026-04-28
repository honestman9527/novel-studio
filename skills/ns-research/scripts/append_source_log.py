#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Append a sourced research note to an NS project source log."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


SOURCE_LOG_HEADER = (
    "# 素材来源\n\n"
    "| 日期 | 主题 | 来源 | 链接 | 可用素材 | 写作位置 |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "untitled"


def table_cell(value: str) -> str:
    value = " ".join(value.strip().split())
    value = value.replace("|", "\\|")
    return value or "待补"


def ensure_source_log(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SOURCE_LOG_HEADER, encoding="utf-8")


def append_source(
    project_dir: Path,
    *,
    date: str,
    topic: str,
    source: str,
    url: str,
    material: str,
    position: str,
    allow_duplicate: bool,
) -> bool:
    path = project_dir / "00-meta/source-log.md"
    ensure_source_log(path)
    text = path.read_text(encoding="utf-8")
    if url and not allow_duplicate and url in text:
        return False
    row = (
        f"| {table_cell(date)} | {table_cell(topic)} | {table_cell(source)} | "
        f"{table_cell(url)} | {table_cell(material)} | {table_cell(position)} |\n"
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(row)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="追加一条 NS 小说素材来源记录。")
    parser.add_argument("project_dir", help="单本小说根目录，或带 --novel 的 NS 工作区目录")
    parser.add_argument("--novel", help="如果 project_dir 是 NS 工作区，则指定 novels/<novel> 作为写入目标")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--topic", required=True, help="调研主题")
    parser.add_argument("--source", required=True, help="来源标题或站点")
    parser.add_argument("--url", required=True, help="来源链接")
    parser.add_argument("--material", required=True, help="可转化为小说素材的要点")
    parser.add_argument("--position", default="待定", help="计划用于哪一部分")
    parser.add_argument("--allow-duplicate", action="store_true", help="允许同一 URL 重复写入")
    args = parser.parse_args()

    root = Path(args.project_dir).resolve()
    if args.novel:
        root = root / "novels" / slugify(args.novel)

    appended = append_source(
        root,
        date=args.date,
        topic=args.topic,
        source=args.source,
        url=args.url,
        material=args.material,
        position=args.position,
        allow_duplicate=args.allow_duplicate,
    )
    path = root / "00-meta/source-log.md"
    if appended:
        print(f"已追加素材来源: {path}")
    else:
        print(f"已跳过重复来源: {args.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
