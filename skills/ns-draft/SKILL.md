---
name: ns-draft
description: "小说正文写作技能。用于写短篇、长篇、连载章节、系统文升级剧情、无限流副本剧情、开篇、续写、重写、扩写、压缩、润色、去 AI 味、章节检查和完稿收尾；当用户要求写正文、写第几章、继续写、改写、润色、补剧情、写结局、生成简介或整理完稿资料时使用。"
---

# NS Draft

写可读正文，而不是只讲该怎么写。当前文件夹就是小说根目录；记忆读取 `novel-studio/*.yaml`；正文写入 `volumes/` 或 `extras/`，不能散放根目录。

## 写前读取

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/continuity.yaml`
5. `novel-studio/style.yaml`
6. 上一章、当前卷计划或用户提供的续写文本

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

## 完稿功能

完稿后更新 `novel-studio/finish.yaml`：

- `blurb`：读者向简介。
- `synopsis_short`：300-800 字短梗概。
- `synopsis_long`：完整剧情梗概。
- `chapter_summaries`：章节摘要。
- `cast_list`：人物表。
- `sequel_hooks`：番外、续作或修订方向。
