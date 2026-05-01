---
name: ns-canon
description: "小说 canon 记忆维护技能。用于更新单本 NS 项目的已定事实、计划、连续性、正文索引、风格摘要、来源边界、视觉索引、notes/*.md 和 records/*.md。当用户要求记住设定、保存资料、更新大纲/进度、处理章末笔记、修正连续性、整理 notes/records、拆分过长文件或接手旧小说记忆时使用。agent 项目约束写入走 ns-guidance。"
---

# NS Canon

只维护项目记忆、事实和进度；不写新正文，不主动造设定。

读取 [memory-schema.md](references/memory-schema.md) 判断 agent 约束、记忆和主要产物的关系；需要决定具体写入文件时读 [file-roles.md](references/file-roles.md)；新建卷、章节、notes 或 records 时读 [content-templates.md](assets/templates/content-templates.md)。

## 文件职责

- agent 约束文件：只读，写入转 `$ns-guidance`。
- `novel-studio/`：结构化记忆、notes、records 和工具。
- 创作产物：正文、brief、visuals、media；位置见 `file-roles.md`。

## 写入边界

- 不写 agent 约束文件；工作流、协作边界和写入禁区转 `$ns-guidance`。
- YAML/frontmatter 保持短小；长说明进 notes，进度/过程/检查点进 records。
- 不复制同一信息；只在其它文件保留摘要、状态或路径。

## YAML/Markdown 协作

- 先定唯一来源：结构化事实归 YAML，正文和长说明归 Markdown，frontmatter 只做连接层。
- `index.yaml.entries` 应能从章节 frontmatter 和审计字数重建。
- 卷 `_index.md` 维护人读简介和目录；`plan.yaml` 维护计划。
- 章节笔记可辅助回写 canon，但不是必填。

## 同步顺序

- 新建/移动章节：章节 Markdown + frontmatter -> `index.yaml` -> 卷 `_index.md`。
- 改正文/章末笔记：审计字数 -> 更新 frontmatter -> `index.yaml`、`continuity.yaml`、`memory.yaml`。
- 改规模/卷计划：`plan.yaml` -> 必要的卷 `_index.md` 说明。
- 改 notes/records：YAML 只留摘要和路径。

## 规则

- 新事实只写一个主 YAML 字段；不确定内容写到 loose/open questions。
- “以后 agent 都要/不要/这个文件别碰/写进 AGENTS 或 CLAUDE”转 `$ns-guidance`。
- `finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。
- 修改 notes 后同步必要 YAML 摘要，避免分叉。

## 工具

- 结构体检：`python skills/ns-canon/scripts/schema_doctor.py <novel-root>`。
- 连续性检查：`python skills/ns-canon/scripts/continuity_check.py <novel-root>`。
- 需要机器读结果时加 `--json`；需要把未收束线索作为失败条件时，连续性检查加 `--strict`。
