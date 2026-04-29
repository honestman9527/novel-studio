---
name: ns-memory
description: "小说长期记忆与本地资料库技能。用于读取、更新单本 NS 小说项目的 YAML/Markdown 记忆：novel-studio/ 是唯一记忆目录，新正文默认放 content/volumes/、content/extras/，旧项目兼容 volumes/、extras/。YAML 维护结构化事实、计划、连续性、索引、发布配置、资料和视觉索引；novel-studio/notes/*.md 维护长文笔记；brief.md 维护对外简介。当用户要求记住设定、保存资料、继续旧小说、更新大纲、维护计划或本地记忆时使用。初始化走 ns-init。"
---

# NS Memory

只维护记忆，不初始化项目；初始化用 `$ns-init`。

## 核心文件

读取 [memory-schema.md](references/memory-schema.md) 获取完整结构。

- `project.yaml`：项目身份。
- `plan.yaml`：卷、章节、番外、下一步。
- `memory.yaml`：人物、世界、关系、伏笔、类型模块。
- `continuity.yaml`：当前状态、事件、未收束线。
- `index.yaml`：正文索引；不写 `content_root`。
- `style.yaml`：文风和章节契约。
- `research.yaml`：来源和事实边界。
- `publish.yaml`：正文根目录和发布规则。
- `finish.yaml`：完稿状态和输出索引。
- `art.yaml`：视觉一致性和文件索引。
- `notes/*.md`：长文说明。

## 更新规则

- 写作前读 `project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`style.yaml`。
- 写完章节：先补 `章末回写`，再更新 `index.yaml`、`continuity.yaml`、`memory.yaml`。
- 只有分卷完成、全书完稿或交付物变化时更新 `finish.yaml`。
- 新事实只写一个主 YAML 字段。
- 不确定内容写入 `continuity.yaml.loose_threads` 或 `research.yaml.open_questions`。
- 改写旧章节时更新 `continuity.yaml.revision_notes` 和 `logs/revision.md`。

## 去重

- `publish.yaml` 管正文根目录。
- `index.yaml` 只存正文条目。
- `finish.yaml` 不存简介、梗概、章节摘要正文。
- `art.yaml` 不存完整提示词。
- YAML 是事实源；Markdown 是长文说明。
