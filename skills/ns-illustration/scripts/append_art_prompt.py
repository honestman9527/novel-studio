#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Append or replace an illustration prompt in an NS project art prompt file."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


PROMPTS_HEADER = "# 插画提示词\n\n"
MEMORY_DIR = "novel-studio"
PROMPT_TYPE_LABELS = {
    "character": "角色立绘",
    "cover": "封面",
    "chapter": "章节插图",
    "storyboard": "分镜",
    "prop": "道具",
    "map": "地图",
    "mood": "气氛图",
    "visual-bible": "视觉圣经",
    "other": "其他",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "untitled"


def resolve_memory_root(project_dir: str) -> Path:
    return Path(project_dir).resolve() / MEMORY_DIR


def clean_inline(value: str) -> str:
    value = " ".join(value.strip().split())
    return value or "无"


def clean_code_block(value: str) -> str:
    return value.strip().replace("```", "'''") or "无"


def ensure_prompts_file(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PROMPTS_HEADER, encoding="utf-8")


def remove_section(text: str, heading: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    result = []
    removed = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.rstrip("\r\n") == heading:
            end = index + 1
            while end < len(lines) and not lines[end].startswith("## "):
                end += 1
            removed += 1
            index = end
            continue
        result.append(line)
        index += 1
    return "".join(result), removed


def build_section(
    *,
    date: str,
    prompt_type: str,
    title: str,
    target_model: str,
    prompt: str,
    negative: str,
    stable: str,
    variable: str,
    chapter: str,
    notes: str,
) -> str:
    label = PROMPT_TYPE_LABELS[prompt_type]
    heading = section_heading(prompt_type, title, target_model)
    parts = [
        heading,
        "",
        f"- 日期：{clean_inline(date)}",
        f"- 类型：{label}",
        f"- 目标模型：{clean_inline(target_model)}",
        f"- 关联章节：{clean_inline(chapter)}",
        f"- 稳定要素：{clean_inline(stable)}",
        f"- 可变要素：{clean_inline(variable)}",
        f"- 备注：{clean_inline(notes)}",
        "",
        "### 正向提示词",
        "",
        "```text",
        clean_code_block(prompt),
        "```",
        "",
        "### 负面提示词",
        "",
        "```text",
        clean_code_block(negative),
        "```",
        "",
    ]
    return "\n".join(parts)


def section_heading(prompt_type: str, title: str, target_model: str) -> str:
    label = PROMPT_TYPE_LABELS[prompt_type]
    return f"## {label}: {clean_inline(title)} [{clean_inline(target_model)}]"


def append_art_prompt(
    project_dir: Path,
    *,
    date: str,
    prompt_type: str,
    title: str,
    target_model: str,
    prompt: str,
    negative: str,
    stable: str,
    variable: str,
    chapter: str,
    notes: str,
    append_duplicate: bool,
) -> tuple[Path, int]:
    path = project_dir / "logs/art-prompts.md"
    ensure_prompts_file(path)
    text = path.read_text(encoding="utf-8")
    heading = section_heading(prompt_type, title, target_model)
    removed = 0
    if not append_duplicate:
        text, removed = remove_section(text, heading)
    section = build_section(
        date=date,
        prompt_type=prompt_type,
        title=title,
        target_model=target_model,
        prompt=prompt,
        negative=negative,
        stable=stable,
        variable=variable,
        chapter=chapter,
        notes=notes,
    )
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + section, encoding="utf-8")
    return path, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="追加或替换一条 NS 插画提示词记录。")
    parser.add_argument("project_dir", help="小说根目录；默认写入 novel-studio/logs/art-prompts.md")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--type", choices=sorted(PROMPT_TYPE_LABELS), default="other", help="提示词类型")
    parser.add_argument("--title", required=True, help="角色、场景、封面或分镜标题")
    parser.add_argument("--target-model", default="通用中文", help="目标模型或提示词格式")
    parser.add_argument("--prompt", required=True, help="正向提示词")
    parser.add_argument("--negative", default="", help="负面提示词")
    parser.add_argument("--stable", default="", help="稳定复用要素")
    parser.add_argument("--variable", default="", help="可变要素")
    parser.add_argument("--chapter", default="", help="关联章节或位置")
    parser.add_argument("--notes", default="", help="备注")
    parser.add_argument("--append-duplicate", action="store_true", help="保留同类型、标题和目标模型的旧记录")
    args = parser.parse_args()

    root = resolve_memory_root(args.project_dir)

    path, removed = append_art_prompt(
        root,
        date=args.date,
        prompt_type=args.type,
        title=args.title,
        target_model=args.target_model,
        prompt=args.prompt,
        negative=args.negative,
        stable=args.stable,
        variable=args.variable,
        chapter=args.chapter,
        notes=args.notes,
        append_duplicate=args.append_duplicate,
    )
    if removed:
        print(f"已替换插画提示词: {path}")
    else:
        print(f"已追加插画提示词: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
