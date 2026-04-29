#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Optionally scaffold a single-novel NS project."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MEMORY_DIR = "novel-studio"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "untitled"


def yaml_list(values: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    if not values:
        return f"{prefix}[]"
    return "\n".join(f"{prefix}- {value}" for value in values)


def project_yaml(title: str, slug: str, mode: str, genres: list[str]) -> str:
    genres_block = yaml_list(genres, 2)
    return f"""title: "{title}"
slug: "{slug}"
mode: "{mode}"
genres:
{genres_block}
status: "planning"
logline: ""
audience: ""
pov: ""
core_promise: ""
do_not_write: []
"""


def plan_yaml(mode: str) -> str:
    return f"""mode: "{mode}"
current:
  path: "volumes/volume-001/ch001.md"
  id: "ch001"
  status: "draft"
volumes:
  - id: "volume-001"
    title: "第一卷"
    status: "planning"
    goal: ""
    chapters:
      - id: "ch001"
        path: "volumes/volume-001/ch001.md"
        title: "第001章"
        function: ""
        status: "draft"
extras: []
next_actions:
  - "补全项目设定"
  - "明确第一章写作目标"
"""


def memory_yaml() -> str:
    return """world:
  rules: []
  locations: []
characters: []
relationships: []
factions: []
glossary: []
artifacts: []
foreshadowing: []
genre:
  system: {}
  infinite_flow: {}
  mystery: {}
  romance: {}
  power_system: {}
  scifi: {}
  realism: {}
  game: {}
  apocalypse: {}
  urban: {}
  journey: {}
  ensemble: {}
"""


def continuity_yaml() -> str:
    return """current_state:
  story_time: ""
  active_location: ""
  pov: ""
  characters: []
event_ledger: []
loose_threads: []
revision_notes: []
"""


def index_yaml(chapter_path: str, chapter_id: str, title: str) -> str:
    return f"""main_text:
  - id: "{chapter_id}"
    path: "{chapter_path}"
    title: "{title}"
    type: "main"
    status: "draft"
    effective_words: null
extras: []
"""


def style_yaml() -> str:
    return """voice:
  prose: ""
  dialogue: ""
  pacing: ""
taboos: []
must_keep: []
chapter_contract:
  frontmatter_required:
    - id
    - type
    - volume
    - title
    - status
    - pov
    - timeline
    - word_target
  required_sections:
    - "写作目标"
    - "正文"
    - "章末回写"
  publishable_text_section: "正文"
"""


def research_yaml() -> str:
    return """sources: []
open_questions: []
fact_boundaries: []
"""


def art_yaml() -> str:
    return """visual_bible:
  style: ""
  palette: ""
  character_consistency: []
prompts: []
"""


def finish_yaml() -> str:
    return """blurb: ""
synopsis_short: ""
synopsis_long: ""
chapter_summaries: []
cast_list: []
sequel_hooks: []
"""


def chapter_template(chapter_id: str, title: str, volume: str = "volume-001") -> str:
    return f"""---
id: {chapter_id}
type: main
volume: {volume}
title: "{title}"
status: draft
pov: ""
timeline: ""
word_target: "3000-5000"
memory_read:
  - novel-studio/project.yaml
  - novel-studio/plan.yaml
  - novel-studio/memory.yaml
  - novel-studio/continuity.yaml
memory_write:
  - novel-studio/index.yaml
  - novel-studio/continuity.yaml
  - novel-studio/finish.yaml
---

# {title}

## 写作目标

- 本章功能：
- 主要冲突：
- 出场人物：
- 承接内容：
- 本章变化：
- 结尾钩子：

## 正文


## 章末回写

```yaml
summary: ""
character_updates: []
world_updates: []
timeline_events: []
foreshadowing: []
loose_threads: []
next_entry: ""
```
"""


def write_file(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="可选：为当前单本小说生成 novel-studio/ 记忆目录和卷目录正文模板。")
    parser.add_argument("project_dir", help="这部小说的根目录；通常传当前目录 .")
    parser.add_argument("--title", default="", help="小说标题")
    parser.add_argument("--slug", default="", help="项目代号，只写入 project.yaml")
    parser.add_argument("--mode", choices=["short", "novella", "long", "serial"], default="long")
    parser.add_argument("--genre", action="append", default=[])
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_dir).resolve()
    title = args.title or project_root.name
    slug = slugify(args.slug or title or project_root.name)
    memory_root = project_root / MEMORY_DIR

    chapter_id = "story" if args.mode == "short" else "ch001"
    chapter_title = "正文" if args.mode == "short" else "第001章"
    chapter_path = "volumes/volume-001/story.md" if args.mode == "short" else "volumes/volume-001/ch001.md"

    files = {
        "project.yaml": project_yaml(title, slug, args.mode, args.genre),
        "plan.yaml": plan_yaml(args.mode),
        "memory.yaml": memory_yaml(),
        "continuity.yaml": continuity_yaml(),
        "index.yaml": index_yaml(chapter_path, chapter_id, chapter_title),
        "style.yaml": style_yaml(),
        "research.yaml": research_yaml(),
        "art.yaml": art_yaml(),
        "finish.yaml": finish_yaml(),
        "logs/revision.md": "# 修改记录\n\n",
        "logs/research-log.md": "# 素材来源\n\n",
        "logs/art-prompts.md": "# 插画提示词\n\n",
        "logs/auto-backwrite.md": "# 自动回写候选\n\n",
    }

    for relative, content in files.items():
        write_file(memory_root / relative, content, args.overwrite)

    write_file(project_root / chapter_path, chapter_template(chapter_id, chapter_title), args.overwrite)
    (project_root / "extras").mkdir(parents=True, exist_ok=True)

    print(f"已初始化小说根目录: {project_root}")
    print(f"记忆目录: {memory_root}")
    print(f"正文入口: {project_root / chapter_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
