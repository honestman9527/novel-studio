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
- `plan.yaml`：全书规模、卷、章节、番外、下一步。
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

## YAML 和 Markdown 协作

- YAML 文件保存项目级事实、索引、计划和连续性。
- Markdown 文件保存作者可读内容：卷说明、章节目标、正文、可选章末笔记和长文笔记。
- Markdown frontmatter 是两者的桥，只放身份、排序、时间、状态和可检索标签；不要把长梗概、正文摘要或大段设定塞进 frontmatter。
- `index.yaml.entries` 同步章节 frontmatter 的 `id`、`volume_id`、`chapter_number`、`title`、`path`、`status`、`word_count`、`created_at`、`updated_at`。
- 章节 `## 章末笔记` 是可选的普通 Markdown 记录；用于写概要、未收束线索、下一章钩子和修订备注，不要求 YAML。

## 规模规划

`plan.yaml` 是总章数、卷数和番外计划的唯一来源。规模字段是写作计划，不是硬锁；是否严格执行由 `limits_are` 决定。

```yaml
scale:
  target_volumes: 3
  target_main_chapters: 90
  target_extras: 5
  target_total_words: 300000
  chapter_word_target: "3000-5000"
  limits_are: soft
volumes:
  - id: volume-001
    title: "第一卷"
    planned_chapters: 30
    chapter_range:
      start: ch001
      end: ch030
    word_target: 100000
    status: drafting
extras:
  - id: extra-001
    title: "番外标题"
    purpose: "补人物关系"
    planned_words: 5000
    status: planned
```

- `target_volumes`：预计卷数。
- `target_main_chapters`：预计主线章节数，不含番外。
- `target_extras`：预计番外篇数。
- `target_total_words`：全书目标字数。
- `chapter_word_target`：默认单章字数区间；章节 frontmatter 可覆盖。
- `limits_are`：`soft` 表示计划可调整；`hard` 表示用户明确要求不要突破。
- `volumes[].planned_chapters` 的合计应接近 `target_main_chapters`。
- `extras[]` 只登记计划和功能，正文仍写入 `content/extras/`。

## 卷文件结构

每卷用 `_index.md` 做卷首页，既是人读简介，也是章节目录入口。

```markdown
---
id: volume-001
type: volume
volume_number: 1
title: "第一卷"
subtitle: ""
display_title: "第一卷"
status: planning
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
word_target: ""
chapter_range:
  start: ch001
  end:
---

# 第一卷

## 卷简介

## 卷承诺

## 本卷主要人物

## 章节目录

| 章节 | 标题 | 状态 | 功能 | 字数 |
| --- | --- | --- | --- | --- |

## 卷末笔记
```

## 章节结构

章节必须有 frontmatter、H1、`## 写作目标`、`## 正文`。`## 章末笔记` 可选；发布或导出只取 `## 正文`。

````markdown
---
id: ch001
type: main
chapter_number: 1
title: "章节标题"
display_title: "第001章 章节标题"
volume_id: volume-001
volume_number: 1
volume_title: "第一卷"
weight: 1
status: draft
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
word_target: "3000-5000"
word_count:
  effective:
  counted_at:
pov:
timeline:
location:
tags: []
memory_read:
  - novel-studio/project.yaml
  - novel-studio/plan.yaml
  - novel-studio/memory.yaml
  - novel-studio/continuity.yaml
  - novel-studio/style.yaml
memory_write:
  - novel-studio/index.yaml
  - novel-studio/continuity.yaml
  - novel-studio/memory.yaml
---

# 第001章 章节标题

## 写作目标

- 本章功能：
- 必须推进：
- 避免：

## 正文

## 章末笔记

- 本章概要：
- 记忆更新：
- 未收束：
- 已解决：
- 下一章钩子：
- 修订备注：
````

## 去重规则

- `publish.yaml.site.content_root` 是正文根目录唯一来源。
- `index.yaml` 只存正文条目。
- 卷 `_index.md` 存卷简介和章节目录，不替代 `plan.yaml` 的计划；`## 卷末笔记` 可选。
- `finish.yaml` 不参与日常章节回写。
- `art.yaml` 不存完整提示词。
- YAML 是事实源；Markdown 是长文说明或展示面板。
