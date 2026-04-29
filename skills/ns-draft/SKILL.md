---
name: ns-draft
description: "小说新正文起草技能。用于从大纲或写作目标起草新章节、新短篇、新番外、开篇、结局初稿、系统文升级剧情或无限流副本剧情；当用户要求写新的一章、起草正文、写开篇、按章节纲写正文、从零写某个番外时使用。续写既有文本走 ns-continue；小改润色走 ns-rewrite-light；大改重写走 ns-rewrite-heavy；简介梗概走 ns-blurb。"
---

# NS Draft

写新正文初稿，而不是只讲该怎么写。当前文件夹就是小说根目录；记忆读取 `novel-studio/*.yaml`；正文写入 `volumes/` 或 `extras/`，不能散放根目录。

## 写前读取

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/continuity.yaml`
5. `novel-studio/style.yaml`
6. 当前卷计划、章节目标或用户提供的起草要求

## 章节文件结构

每章必须保留：

1. YAML frontmatter：`id`、`type`、`volume`、`title`、`status`、`pov`、`timeline`、`word_target`、`memory_read`、`memory_write`。
2. `## 写作目标`：本章功能、主要冲突、出场人物、承接内容、本章变化、结尾钩子。
3. `## 正文`：唯一可发布正文。
4. `## 章末回写`：YAML 块，记录 `summary`、`character_updates`、`world_updates`、`timeline_events`、`foreshadowing`、`loose_threads`、`next_entry`。

## 正文流程

1. 确认本章功能：推进主线、升级关系、揭示信息、兑现伏笔、制造选择、完成副本/任务节点。
2. 写 4-8 个场景拍点：开场抓手、中段阻力、选择代价、反转、结尾钩子。
3. 直接写 `## 正文`。减少解释性旁白，多用行动、对白、环境反馈和选择。
4. 写完后补 `## 章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`、`finish.yaml`。
5. 需要机器统计时再运行 `scripts/chapter_audit.py <chapter-file>`；不把脚本输出直接当最终记忆。

## 字数策略

- 短篇：1000-12000 字，结构完整，结尾有余味。
- 中篇：按场景交付，保证每章有阶段推进。
- 长篇/连载：默认每章 2500-5000 中文字，用户另有要求则服从。
- 章节过长时先交付完整片段，并明确下一段从哪里接。
- 字数复核以 `scripts/chapter_audit.py` 的“有效字数”为准：排除 Markdown 标题、表格、代码块、待办项和纯占位行；中日韩文字按单字计，英文/数字按词或连续串计，不把空白和标点算入正文。
- 用户给出明确字数、字数区间或“至少/不低于/不少于”时，必须把它当硬性验收条件；未统计前不能说已经达标。
- 不能用估算字数冒充实际字数。章节落盘后运行 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>`，用输出的有效字数报告结果。
- 如果有效字数不足，继续补写正文直到达标；如果本轮无法补足，明确写出当前有效字数、目标字数、差额和下一段承接点。

## 边界

- 只负责新正文初稿。
- 需要接续既有段落时转 `$ns-continue`。
- 需要小范围润色时转 `$ns-rewrite-light`。
- 需要重构剧情或章节时转 `$ns-rewrite-heavy`。
- 需要简介、梗概、标签或宣传文案时转 `$ns-blurb`。
