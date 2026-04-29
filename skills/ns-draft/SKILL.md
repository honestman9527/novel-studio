---
name: ns-draft
description: "小说新写作单元起草技能。用于新开卷、番外、独立短篇、序章、尾声、结局初稿、特殊篇、系统文新阶段或无限流新副本；新项目正文写入 content/volumes/ 或 content/extras/，旧项目兼容 volumes/、extras/。当用户要从大纲或目标开一个不直接承接上一章的新单元时使用。普通下一章走 ns-continue；轻改走 ns-rewrite-light；大改走 ns-rewrite-heavy；简介走 ns-blurb。"
---

# NS Draft

写新写作单元的正文初稿。

## 读取

- `novel-studio/project.yaml`
- `novel-studio/plan.yaml`
- `novel-studio/memory.yaml`
- `novel-studio/continuity.yaml`
- `novel-studio/style.yaml`
- `novel-studio/publish.yaml`
- 用户给的新卷/番外/短篇/特殊篇目标

## 输出

- 正文写入 `content/volumes/` 或 `content/extras/`；旧项目沿用已登记目录。
- 章节保留 frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。
- 写完后更新 `index.yaml`、`continuity.yaml`、`memory.yaml`；`finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。

## 写法

- 先定新单元功能：新卷开局、番外补完、短篇闭环、序章钩子、尾声收束、新阶段或新副本。
- 写 4-8 个场景拍点，再直接写正文。
- 少解释，多用行动、对白、环境反馈和选择。

## 字数

- 明确字数要求是硬验收。
- 落盘后用 `python novel-studio/tools/word_count.py <chapter-file>`；开发插件时可用 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>`。
- 未统计不能声称达标；不足就补写或报告差额和承接点。
