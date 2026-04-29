#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optional helper: append chapter-derived notes to the NS auto-backwrite log."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


MEMORY_DIR = "novel-studio"
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
    plain = re.sub(r"\s+", "", "".join(lines))
    return plain[:limit] + ("..." if len(plain) > limit else "")


def unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def memory_root(project_dir: str) -> Path:
    root = Path(project_dir).resolve()
    return root / MEMORY_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="可选：根据章节文本生成自动回写候选，追加到 novel-studio/logs/auto-backwrite.md。")
    parser.add_argument("project_dir", help="小说根目录")
    parser.add_argument("chapter_file", help="章节 Markdown 文件")
    parser.add_argument("--chapter-id", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    chapter_path = Path(args.chapter_file).resolve()
    text = chapter_path.read_text(encoding="utf-8")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    chapter_id = args.chapter_id or chapter_path.stem
    title = args.title or chapter_path.stem
    summary = args.summary or compact_summary(text)
    times = unique(TIME_PATTERN.findall(text))
    foreshadow_hits = unique(FORESHADOW_PATTERN.findall(text))
    word_count = effective_word_count(text)

    content = (
        f"\n## {now} {chapter_id} {title}\n\n"
        f"- path: `{chapter_path}`\n"
        f"- effective_words: {word_count}\n"
        f"- summary: {summary}\n"
        f"- time_markers: {', '.join(times) if times else '未明示'}\n"
        f"- foreshadowing_candidates: {', '.join(foreshadow_hits) if foreshadow_hits else '无'}\n"
        "- write_back_targets:\n"
        "  - novel-studio/index.yaml\n"
        "  - novel-studio/continuity.yaml\n"
        "  - novel-studio/memory.yaml\n"
        "  - novel-studio/finish.yaml\n"
        "- human_review: 人物状态、世界规则、伏笔状态和下一章入口必须人工复核后再写入 YAML。\n"
    )

    output = memory_root(args.project_dir) / "logs" / "auto-backwrite.md"
    if args.dry_run:
        print(content)
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists():
        output.write_text("# 自动回写候选\n\n", encoding="utf-8")
    with output.open("a", encoding="utf-8") as handle:
        handle.write(content)
    print(f"已追加自动回写候选: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
