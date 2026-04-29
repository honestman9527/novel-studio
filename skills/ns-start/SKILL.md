---
name: ns-start
description: "Novel Studio 项目启动技能。用于把空文件夹初始化为单本小说项目，或把已有 Markdown 正文接入 NS；创建 content/、novel-studio/、brief.md、visuals/、media/、基础 YAML/Markdown 记忆和 novel-studio/tools/word_count.py。当用户要求初始化、接入旧项目、整理目录、迁移到 NS 或准备本地小说工作区时使用。"
---

# NS Start

只负责项目骨架和接入，不写正文，不脑暴设定。

## 创建结构

```text
NOVEL.md
content/volumes/volume-001/_index.md
content/volumes/volume-001/ch001.md
content/extras/
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
  logs/
  tools/word_count.py
brief.md
visuals/
media/
```

## 流程

1. 判断空项目、已有 NS 项目、已有 Markdown 正文或混合旧结构。
2. 创建缺失目录和基础文件；已有文件不覆盖，除非用户要求。
3. 复制本 skill 的 `assets/tools/word_count.py` 到 `novel-studio/tools/word_count.py`。
4. 复制本 skill 的 `assets/templates/NOVEL.md` 到根目录 `NOVEL.md`，已有文件不覆盖。
5. 扫描已有 `.md`，只把正文条目登记到 `index.yaml.entries`；不批量改正文。

## 模板要求

- 卷 `_index.md` 必须包含 YAML frontmatter、`# 第一卷`、`## 卷简介`、`## 卷承诺`、`## 本卷主要人物`、`## 章节目录`。
- `## 卷末笔记` 可选。
- 章节文件必须包含 YAML frontmatter、`# 第001章 章节标题`、`## 写作目标`、`## 正文`。
- `## 章末笔记` 可选；需要时用普通 Markdown 列表写本章概要、未收束、已解决、下一章钩子和修订备注。
- 章节 frontmatter 至少写 `id`、`type`、`chapter_number`、`title`、`display_title`、`volume_id`、`volume_number`、`volume_title`、`weight`、`status`、`created_at`、`updated_at`、`word_target`。
- `NOVEL.md` 生成初始全局约束模板，留给用户填写。
- 时间用 ISO 8601 字符串，优先带时区，例如 `2026-04-29T20:30:00+08:00`。
- 完整模板见 `$ns-canon` 的 `memory-schema.md`；本 skill 只创建骨架，不编造卷简介和正文。

## 分工

- `project.yaml` 管项目身份、类型、受众、承诺、禁区。
- `plan.yaml.scale` 管预计卷数、主线章数、番外数、总字数、单章字数区间和限制强度。
- `plan.yaml.volumes[]` 管每卷计划章节数、章节范围、目标字数和状态。
- `plan.yaml.extras[]` 管番外目的、预计字数和状态。
- `NOVEL.md` 管全局约束：必须遵守、不要写/不要改、风格偏好、内容边界、结构偏好和待确认。
- `publish.yaml` 管正文根目录、排序、过滤和媒体目录。
- `index.yaml` 只管正文条目路径、状态、字数和排序。
- `_index.md` 是卷的人读入口；章节 frontmatter 是机器可读入口。
- `brief.md` 是对外展示；`notes/*.md` 是长文记忆；`logs/*.md` 是过程记录。
