---
name: ns-start
description: "Novel Studio 项目启动技能。用于初始化空文件夹或接入已有 Markdown 正文；创建 content/、novel-studio/、brief.md、visuals/、media/、基础 YAML/Markdown 和记数字数工具。当用户要求初始化、迁移、接入旧项目或整理小说工作区时使用。"
---

# NS Start

只建骨架和接入旧文，不写正文，不脑暴设定；agent 约束基础模块交给 `$ns-guidance`。

## 创建结构

```text
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
  records/
  tools/word_count.py
brief.md
visuals/
media/
```

## 流程

1. 判断空项目、已有 NS 项目、旧 Markdown 或混合结构。
2. 创建缺失目录和基础文件；不覆盖已有文件，除非用户要求。
3. 复制 `assets/tools/word_count.py` 到 `novel-studio/tools/word_count.py`。
4. 扫描已有 `.md`，只登记正文到 `index.yaml.entries`。
5. 如果需要 agent 项目约束，转 `$ns-guidance` 写入 `AGENTS.md` 或 `CLAUDE.md`；初始化时可生成基础模块。

## 模板要求

- 卷 `_index.md`：frontmatter、H1、卷简介、卷承诺、主要人物、章节目录；卷末笔记可选。
- 章节：frontmatter、H1、`## 写作目标`、`## 正文`；章末笔记可选。
- frontmatter 只写身份、归属、状态、时间、字数等索引字段。
- 时间用 ISO 8601，优先带时区。

## 分工

- YAML 管结构化事实、计划、索引和发布配置。
- Markdown 管正文、卷简介、简介文案、notes 和 records。
- agent 约束文件由 `$ns-guidance` 维护；本 skill 不直接维护。
