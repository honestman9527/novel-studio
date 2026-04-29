# Memory Schema

当前文件夹就是小说根目录。`novel-studio/` 是唯一记忆目录；新正文放 `content/volumes/`、`content/extras/`。旧项目已有 `volumes/`、`extras/` 时兼容，并在 `index.yaml` 登记。

## 目录

```text
novel-studio/
  project.yaml
  plan.yaml
  memory.yaml
  continuity.yaml
  index.yaml
  style.yaml
  research.yaml
  art.yaml
  finish.yaml
  publish.yaml
  notes/
    characters.md
    world.md
    timeline.md
    glossary.md
    style.md
    synopsis.md
    open-threads.md
  logs/
  tools/word_count.py
content/
  volumes/volume-001/_index.md
  volumes/volume-001/ch001.md
  extras/
brief.md
visuals/
media/
```

## YAML 职责

- `project.yaml`：项目身份、类型、受众、承诺、禁区。
- `plan.yaml`：卷、章节、番外、下一步。
- `memory.yaml`：人物、世界、关系、名词、道具、伏笔、类型模块。
- `continuity.yaml`：当前状态、事件、未收束线、改写影响。
- `index.yaml`：正文条目路径、状态、字数、排序；不写 `content_root`。
- `style.yaml`：文风、禁忌、章节结构契约。
- `research.yaml`：来源、待查问题、事实边界。
- `publish.yaml`：正文根目录唯一来源、排序、slug、封面、过滤规则。
- `finish.yaml`：完稿状态、里程碑、输出索引；不存正文。
- `art.yaml`：视觉一致性、提示词文件、媒体文件；不存完整提示词。

## Markdown 职责

- `brief.md`：对外简介、标签、卖点、pitch、封面文案。
- `notes/characters.md`：人物长说明。
- `notes/world.md`：世界观长说明。
- `notes/timeline.md`：时间线长说明。
- `notes/glossary.md`：术语表。
- `notes/style.md`：文风样例。
- `notes/synopsis.md`：内部梗概、投稿梗概、完稿梗概。
- `notes/open-threads.md`：伏笔和待确认问题。
- `visuals/*.md`：完整提示词。
- `media/`：实际图片素材。

## 章节结构

章节必须有 frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。发布或导出只取 `## 正文`。

```markdown
---
id: ch001
type: main
volume: volume-001
weight: 1
title: "第001章"
status: draft
word_target: "3000-5000"
memory_read:
  - novel-studio/project.yaml
  - novel-studio/plan.yaml
  - novel-studio/memory.yaml
  - novel-studio/continuity.yaml
memory_write:
  - novel-studio/index.yaml
  - novel-studio/continuity.yaml
---

# 第001章

## 写作目标

## 正文

## 章末回写
```

## 去重规则

- `publish.yaml.site.content_root` 是正文根目录唯一来源。
- `index.yaml` 只存正文条目。
- `finish.yaml` 不参与日常章节回写。
- `art.yaml` 不存完整提示词。
- YAML 是事实源；Markdown 是长文说明或展示面板。
