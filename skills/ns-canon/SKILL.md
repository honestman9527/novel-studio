---
name: ns-canon
description: "小说 canon 记忆维护技能。用于更新单本 NS 项目的已定事实、计划、连续性、正文索引、风格摘要、来源边界、视觉索引和 notes/*.md。当用户要求记住设定、保存资料、更新大纲/进度、处理章末笔记、修正连续性、整理 notes、拆分过长文件或接手旧小说记忆时使用。全局指导写入走 ns-guidance。"
---

# NS Canon

只维护指导、事实和进度；不写新正文，不主动造设定。

读取 [memory-schema.md](references/memory-schema.md) 获取结构规则；需要判断 YAML/Markdown 文件职责时读取 [file-roles.md](references/file-roles.md)；新建卷、章节或 notes 时读取 [content-templates.md](assets/templates/content-templates.md)。

## 文件职责

- YAML：项目身份、计划、人物/世界摘要、连续性、索引、来源、发布、完稿和视觉索引。
- Markdown：正文、卷简介、章末笔记、brief、visuals、logs、notes 长说明。
- 根指导文件：只读；写入转 `$ns-guidance`。

## 写入边界

- 不写根指导文件；全局规则、禁区和长期偏好转 `$ns-guidance`。
- YAML/frontmatter/根指导文件保持短小；长说明拆到按主题命名的 notes。
- 单个 notes 文件只承载一个主题。

## YAML/Markdown 协作

- 先定唯一来源：结构化事实归 YAML，正文和长说明归 Markdown，frontmatter 只做连接层。
- `index.yaml.entries` 应能从章节 frontmatter 和审计字数重建。
- 卷 `_index.md` 维护人读简介和目录；`plan.yaml` 维护计划。
- 章节笔记可辅助回写 canon，但不是必填。

## 同步顺序

- 新建/移动章节：章节 Markdown + frontmatter -> `index.yaml` -> 卷 `_index.md`。
- 改正文/章末笔记：审计字数 -> 更新 frontmatter -> `index.yaml`、`continuity.yaml`、`memory.yaml`。
- 改规模/卷计划：`plan.yaml` -> 必要的卷 `_index.md` 说明。
- 改 notes：YAML 只留摘要和路径。

## 规则

- 新事实只写一个主 YAML 字段；不确定内容写到 loose/open questions。
- “以后都要/不要再写/不能改/保持味道”先判断是否全局指导；是则转 `$ns-guidance`。
- `finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。
- 修改 notes 后同步必要 YAML 摘要，避免分叉。

## 工具

- 结构体检：`python skills/ns-canon/scripts/schema_doctor.py <novel-root>`。
- 连续性检查：`python skills/ns-canon/scripts/continuity_check.py <novel-root>`。
- 需要机器读结果时加 `--json`；需要把未收束线索作为失败条件时，连续性检查加 `--strict`。
