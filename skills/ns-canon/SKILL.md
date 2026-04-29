---
name: ns-canon
description: "小说 canon 记忆维护技能。用于读取、更新单本 NS 项目的已定事实、计划、连续性、正文索引、风格约束、来源边界和视觉索引；维护 novel-studio/*.yaml 与 notes/*.md。当用户要求记住设定、保存资料、更新大纲、整理进度、处理章末笔记、修正连续性或接手旧小说记忆时使用。初始化走 ns-start。"
---

# NS Canon

只维护事实源和进度，不新写正文，不创造未要求的新设定。

读取 [memory-schema.md](references/memory-schema.md) 获取完整结构。

## 职责

- `project.yaml`：项目身份。
- `plan.yaml`：全书规模、卷、章节、番外、下一步。
- `memory.yaml`：人物、世界、关系、伏笔、类型模块。
- `continuity.yaml`：当前状态、事件、未收束线、修订影响。
- `index.yaml`：正文条目路径、状态、字数、排序。
- `style.yaml`：文风和章节契约。
- `research.yaml`：来源和事实边界。
- `publish.yaml`：正文根目录和发布规则。
- `finish.yaml`：完稿状态和输出索引。
- `art.yaml`：视觉一致性和文件索引。

## YAML/Markdown 协作

- 章节和卷的 Markdown frontmatter 是 YAML 记忆与正文文件的连接层。
- frontmatter 只放身份、排序、状态、时间、字数和标签；长说明写 Markdown 正文区或 `notes/*.md`。
- `index.yaml.entries` 必须能从章节 frontmatter 和审计字数重建。
- 卷 `_index.md` 维护卷简介、卷承诺和章节目录；`plan.yaml` 维护计划，不互相复制长文本。
- 章节 `## 章末笔记` 是可选 Markdown；没有章末笔记时，直接从正文和上下文更新 canon。
- 总卷数、总章数、番外数和总字数目标只写在 `plan.yaml.scale`。

## 规则

- 新事实只写一个主 YAML 字段，避免重复记录。
- 不确定内容写入 `continuity.yaml.loose_threads` 或 `research.yaml.open_questions`。
- 写完章节后，优先读可选的 `## 章末笔记`，再更新 `index.yaml`、`continuity.yaml`、`memory.yaml`。
- 只有分卷完成、全书完稿或交付物变化时更新 `finish.yaml`。
- YAML 是事实源；Markdown 是长文说明或展示面板。
- 调整规模时先改 `plan.yaml.scale` 和 `plan.yaml.volumes/extras`，再同步卷 `_index.md` 的目录说明。

## 工具

- 结构体检：`python skills/ns-canon/scripts/schema_doctor.py <novel-root>`。
- 连续性检查：`python skills/ns-canon/scripts/continuity_check.py <novel-root>`。
- 需要机器读结果时加 `--json`；需要把未收束线索作为失败条件时，连续性检查加 `--strict`。
