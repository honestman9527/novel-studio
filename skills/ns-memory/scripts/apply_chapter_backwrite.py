#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Append chapter-derived updates into a NS project memory folder."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


TIME_PATTERN = re.compile(
    r"(清晨|早上|上午|中午|下午|傍晚|黄昏|夜里|深夜|凌晨|次日|当天|当晚|"
    r"三天后|数日后|一周后|一个月后|第[一二三四五六七八九十百\d]+天)"
)
FORESHADOW_PATTERN = re.compile(r"(伏笔|线索|秘密|疑点|预感|异样|暗示|真相|隐约|不对劲|钥匙|信物|梦境|旧照片)")

SHARED_SCRIPT_DIR = Path(__file__).resolve().parents[2] / "ns" / "scripts"
if str(SHARED_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPT_DIR))

from ns_text_metrics import effective_word_count


def strip_markdown(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"\A\s*---\s*\n[\s\S]*?\n---\s*", "", text)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def compact_summary(text: str, limit: int = 180) -> str:
    plain = strip_markdown(text)
    lines = [line.strip() for line in plain.splitlines() if line.strip()]
    if lines and re.match(r"^第[一二三四五六七八九十百\d]+章", lines[0]):
        lines = lines[1:]
    plain = "".join(lines)
    plain = re.sub(r"\s+", "", plain)
    return plain[:limit] + ("..." if len(plain) > limit else "")


def unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "untitled"


def append(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"\n--- {path} ---\n{content.rstrip()}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content)


def ensure_file(path: Path, header: str, dry_run: bool) -> None:
    if dry_run or path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header, encoding="utf-8")


def remove_sections_with_marker(text: str, heading_token: str, marker: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    result = []
    removed = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("## ") and heading_token in line:
            end = index + 1
            while end < len(lines) and not lines[end].startswith("## "):
                end += 1
            block = "".join(lines[index:end])
            if marker in block:
                removed += 1
                index = end
                continue
        result.append(line)
        index += 1
    return "".join(result), removed


def remove_lines_with_markers(text: str, markers: list[str]) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    kept = []
    removed = 0
    for line in lines:
        if any(marker in line for marker in markers):
            removed += 1
            continue
        kept.append(line)
    return "".join(kept), removed


def update_text_file(path: Path, content: str, dry_run: bool, label: str) -> None:
    if dry_run:
        print(f"\n--- {path} ---\n{label}")
        return
    path.write_text(content, encoding="utf-8")


def remove_existing_chapter_entries(root: Path, chapter_id: str, dry_run: bool) -> None:
    progress_path = root / "00-meta/progress.md"
    if progress_path.exists():
        text = progress_path.read_text(encoding="utf-8")
        updated, removed = remove_sections_with_marker(text, "自动回写", f"最近章节：{chapter_id}")
        if removed:
            update_text_file(progress_path, updated, dry_run, f"将移除 {removed} 个 {chapter_id} 自动回写进度块。")

    summary_path = root / "07-finish/chapter-summary.md"
    if summary_path.exists():
        text = summary_path.read_text(encoding="utf-8")
        updated, removed = remove_lines_with_markers(text, [f"| {chapter_id} ", f"| {chapter_id} |"])
        if removed:
            update_text_file(summary_path, updated, dry_run, f"将移除 {removed} 行 {chapter_id} 章节摘要。")

    timeline_path = root / "02-bible/timeline.md"
    if timeline_path.exists():
        text = timeline_path.read_text(encoding="utf-8")
        updated, removed = remove_lines_with_markers(text, [f"| {chapter_id} |"])
        if removed:
            update_text_file(timeline_path, updated, dry_run, f"将移除 {removed} 行 {chapter_id} 时间线。")

    foreshadowing_path = root / "02-bible/foreshadowing.md"
    if foreshadowing_path.exists():
        text = foreshadowing_path.read_text(encoding="utf-8")
        updated, removed = remove_sections_with_marker(text, "自动发现候选", f"## {chapter_id} 自动发现候选")
        if removed:
            update_text_file(foreshadowing_path, updated, dry_run, f"将移除 {removed} 个 {chapter_id} 伏笔候选块。")

    revision_path = root / "05-revisions/revision-log.md"
    if revision_path.exists():
        text = revision_path.read_text(encoding="utf-8")
        updated, removed = remove_lines_with_markers(text, [f"| {chapter_id} |"])
        if removed:
            update_text_file(revision_path, updated, dry_run, f"将移除 {removed} 行 {chapter_id} 修改记录。")


def main() -> int:
    parser = argparse.ArgumentParser(description="根据章节文本追加回写小说长期记忆。")
    parser.add_argument("project_dir")
    parser.add_argument("chapter_file")
    parser.add_argument("--novel", help="如果 project_dir 是 NS 工作区，则指定 novels/<novel> 作为回写目标")
    parser.add_argument("--chapter-id", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--append-duplicate", action="store_true", help="保留旧行为：不清理同 chapter-id 的既有自动回写记录。")
    args = parser.parse_args()

    root = Path(args.project_dir).resolve()
    if args.novel:
        root = root / "novels" / slugify(args.novel)
    chapter_path = Path(args.chapter_file).resolve()
    text = chapter_path.read_text(encoding="utf-8")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    chapter_id = args.chapter_id or chapter_path.stem
    title = args.title or chapter_path.stem
    summary = args.summary or compact_summary(text)
    times = unique(TIME_PATTERN.findall(text))
    foreshadow_hits = unique(FORESHADOW_PATTERN.findall(text))
    word_count = effective_word_count(text)

    if not args.append_duplicate:
        remove_existing_chapter_entries(root, chapter_id, args.dry_run)

    ensure_file(root / "00-meta/progress.md", "# 进度\n\n", args.dry_run)
    ensure_file(
        root / "07-finish/chapter-summary.md",
        "# 章节摘要\n\n| 章节 | 摘要 | 关键变化 |\n| --- | --- | --- |\n",
        args.dry_run,
    )
    ensure_file(
        root / "02-bible/timeline.md",
        "# 时间线\n\n| 顺序 | 时间 | 章节 | 事件 | 影响 |\n| --- | --- | --- | --- | --- |\n",
        args.dry_run,
    )
    ensure_file(
        root / "02-bible/foreshadowing.md",
        "# 伏笔追踪\n\n| 伏笔 | 埋设位置 | 表面含义 | 真实含义 | 兑现计划 | 状态 |\n| --- | --- | --- | --- | --- | --- |\n",
        args.dry_run,
    )
    ensure_file(
        root / "05-revisions/revision-log.md",
        "# 修改记录\n\n| 日期 | 范围 | 原因 | 影响 |\n| --- | --- | --- | --- |\n",
        args.dry_run,
    )

    append(
        root / "00-meta/progress.md",
        f"\n## {now} 自动回写\n\n- 最近章节：{chapter_id} {title}\n- 有效字数：{word_count}\n- 摘要：{summary}\n- 待人工复核：人物状态、系统/副本结果、伏笔状态、名词表。\n",
        args.dry_run,
    )
    append(root / "07-finish/chapter-summary.md", f"| {chapter_id} {title} | {summary} | 待人工补充 |\n", args.dry_run)

    if times:
        for marker in times:
            append(root / "02-bible/timeline.md", f"| 待排序 | {marker} | {chapter_id} | {summary} | 待人工确认 |\n", args.dry_run)
    else:
        append(root / "02-bible/timeline.md", f"| 待排序 | 未明示 | {chapter_id} | {summary} | 待人工确认 |\n", args.dry_run)

    if foreshadow_hits:
        append(root / "02-bible/foreshadowing.md", f"\n## {chapter_id} 自动发现候选\n\n", args.dry_run)
        for hit in foreshadow_hits:
            append(root / "02-bible/foreshadowing.md", f"- `{hit}`：章节中出现，请人工判断是否为伏笔或误导。\n", args.dry_run)

    append(root / "05-revisions/revision-log.md", f"| {now} | {chapter_id} | 章节完成后自动回写 | 追加进度、摘要、时间线和伏笔候选 |\n", args.dry_run)

    print(f"已处理章节回写: {chapter_id} {title}")
    if args.dry_run:
        print("dry-run 模式未写入文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
