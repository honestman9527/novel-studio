---
name: ns-draft
description: "小说新写作单元起草技能。用于新开卷、开新番外、写独立短篇、序章、尾声、结局初稿、特殊篇、系统文新阶段或无限流新副本的正文初稿；新项目正文写入 content/volumes/ 或 content/extras/，旧项目兼容 volumes/、extras/；当用户要求从大纲或写作目标开一个不直接承接上一章结尾的新单元时使用。普通下一章、接上一章、沿当前卷线性推进走 ns-continue；小改润色走 ns-rewrite-light；大改重写走 ns-rewrite-heavy；简介梗概走 ns-blurb。"
---

# NS Draft

写新写作单元的正文初稿，而不是只讲该怎么写。当前文件夹就是小说根目录；记忆读取 `novel-studio/*.yaml` 和必要的 `novel-studio/notes/*.md`；新项目正文写入 `content/volumes/` 或 `content/extras/`，不能散放根目录。旧项目已有 `volumes/`、`extras/` 时兼容。

## 写前读取

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/continuity.yaml`
5. `novel-studio/style.yaml`
6. `novel-studio/publish.yaml`
7. 新卷计划、番外目标、独立短篇目标、特殊篇目标或用户提供的起草要求

## 章节文件结构

每章必须保留：

1. YAML frontmatter：`id`、`type`、`volume`、`title`、`status`、`pov`、`timeline`、`word_target`、`memory_read`、`memory_write`。
2. `## 写作目标`：本章功能、主要冲突、出场人物、承接内容、本章变化、结尾钩子。
3. `## 正文`：唯一可发布正文。
4. `## 章末回写`：YAML 块，记录 `summary`、`character_updates`、`world_updates`、`timeline_events`、`foreshadowing`、`loose_threads`、`next_entry`。

## 正文流程

1. 确认新写作单元功能：新卷开局、番外补完、独立短篇闭环、序章钩子、尾声收束、系统新阶段或副本入口。
2. 写 4-8 个场景拍点：开场抓手、中段阻力、选择代价、反转、结尾钩子。
3. 直接写 `## 正文`。减少解释性旁白，多用行动、对白、环境反馈和选择。
4. 写完后补 `## 章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`；只有分卷完成、全书完稿或交付物变化时才更新 `finish.yaml`。
5. 需要机器统计时优先运行 `novel-studio/tools/word_count.py <chapter-file>`；开发插件自身时可运行 `scripts/chapter_audit.py <chapter-file>`；不把脚本输出直接当最终记忆。

## 字数策略

- 短篇：1000-12000 字，结构完整，结尾有余味。
- 中篇：按场景交付，保证每章有阶段推进。
- 长篇/连载：默认每章 2500-5000 中文字，用户另有要求则服从。
- 章节过长时先交付完整片段，并明确下一段从哪里接。
- 字数复核以 `novel-studio/tools/word_count.py` 或 `scripts/chapter_audit.py` 的“有效字数”为准：默认只统计 `## 正文`，排除 frontmatter、Markdown 标题、表格、代码块、待办项和纯占位行；中日韩文字按单字计，英文/数字按词或连续串计，不把空白和标点算入正文。
- 用户给出明确字数、字数区间或“至少/不低于/不少于”时，必须把它当硬性验收条件；未统计前不能说已经达标。
- 不能用估算字数冒充实际字数。章节落盘后优先运行 `python novel-studio/tools/word_count.py <chapter-file>`；开发插件自身时可运行 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>`，用输出的有效字数报告结果。
- 如果有效字数不足，继续补写正文直到达标；如果本轮无法补足，明确写出当前有效字数、目标字数、差额和下一段承接点。

## 边界

- 只负责新开卷、新番外、独立短篇、序章、尾声、特殊篇等新写作单元初稿。
- 普通“下一章”、接续上一章结尾、沿当前卷线性推进时转 `$ns-continue`。
- 需要接续既有段落时转 `$ns-continue`。
- 需要小范围润色时转 `$ns-rewrite-light`。
- 需要重构剧情或章节时转 `$ns-rewrite-heavy`。
- 需要简介、梗概、标签或宣传文案时转 `$ns-blurb`。
