---
name: ns-memory
description: "小说长期记忆与本地资料库技能。用于读取、更新单本 NS 小说项目的 YAML 与 Markdown 记忆：当前文件夹就是这部小说根目录，唯一记忆目录固定为 novel-studio/，新项目正文默认放在 content/volumes/、content/extras/，旧项目可兼容 volumes/、extras/；通过 YAML 文件维护项目约束、计划、记忆、连续性、正文索引、发布配置、资料来源、视觉设定和完稿资料，通过 novel-studio/notes/*.md 维护便于人查看的长笔记，根目录 brief.md 维护对外简介。当用户要求记住设定、保存资料、继续之前的小说、更新大纲、维护计划或本地记忆时使用。初始化空项目或接入旧项目走 ns-init。"
---

# NS Memory

只使用新版结构：当前文件夹是一部小说，`novel-studio/` 是唯一记忆目录。新项目正文放入 `content/volumes/`、`content/extras/`；旧项目已有 `volumes/`、`extras/` 时兼容，并在 `index.yaml` 登记。

## 默认结构

```text
<novel-root>/
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
    tools/
  content/
    volumes/
      volume-001/
        _index.md
        ch001.md
    extras/
  visuals/
  brief.md
  media/
```

## 初始化原则

初始化空项目、接入旧项目、创建 `content/` 结构和复制 `novel-studio/tools/word_count.py` 时使用 `$ns-init`。本 skill 只负责初始化后的记忆维护。

## 记忆结构

读取 [memory-schema.md](references/memory-schema.md) 获取完整说明。核心文件：

- `novel-studio/project.yaml`：项目身份、类型、承诺、禁区。
- `novel-studio/plan.yaml`：卷、章节、番外和下一步计划。
- `novel-studio/memory.yaml`：人物、世界、关系、名词、伏笔和类型模块。
- `novel-studio/continuity.yaml`：当前状态、事件台账、待收束线索和改写影响。
- `novel-studio/index.yaml`：正文文件索引，记录章节/番外路径、状态、字数和排序；不保存正文根目录。
- `novel-studio/style.yaml`：文风和章节结构契约。
- `novel-studio/research.yaml`：资料来源、待查问题和事实边界。
- `novel-studio/art.yaml`：视觉一致性索引；完整提示词正文放 `visuals/`，实际图片放 `media/`。
- `novel-studio/finish.yaml`：完稿状态索引；只记录状态、里程碑、交付物路径和检查结果。
- `novel-studio/publish.yaml`：发布/展示配置，是正文根目录的唯一来源，记录排序、slug、封面和导出规则。
- `novel-studio/notes/*.md`：人物、世界、时间线、术语、文风和未收束线索等便于人查看的长笔记。

## 章节约束

章节文件必须放在卷或番外目录中，例如 `content/volumes/volume-001/ch001.md`、`content/extras/extra-001.md`。旧项目已有 `volumes/volume-001/ch001.md`、`extras/extra-001.md` 时可以继续维护。每章必须包含：

1. YAML frontmatter：`id`、`type`、`volume`、`title`、`status`、`pov`、`timeline`、`word_target`、`memory_read`、`memory_write`。
2. `## 写作目标`：本章功能、冲突、出场人物、承接内容、变化、钩子。
3. `## 正文`：唯一可发布正文区域。
4. `## 章末回写`：用 YAML 块记录摘要、人物变化、世界变化、时间线事件、伏笔、待收束线索、下一入口。

## 更新协议

1. 写作前读取 `project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`style.yaml`。
2. 写完章节后，先补本章 `章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`；只有分卷完成、全书完稿或交付物变化时才更新 `finish.yaml`。
3. 新事实只写入一个主 YAML 字段，避免多处散记。
4. 不确定内容写入 `continuity.yaml.loose_threads` 或 `research.yaml.open_questions`。
5. 改写旧章节时，更新 `continuity.yaml.revision_notes` 和 `novel-studio/logs/revision.md`。
6. 图片、封面、角色、场景、分镜提示词写入 `visuals/`。
7. 对外简介、标签、pitch、封面文案写入根目录 `brief.md`；内部梗概写入 `novel-studio/notes/synopsis.md`。
8. 发布渠道需要的实际图片、封面、插图文件写入 `media/`。

## 去重规则

- `publish.yaml` 管正文根目录；`index.yaml` 只存条目路径，不再重复 `content_root`。
- `finish.yaml` 不存简介、梗概或章节摘要正文，只存状态和输出索引。
- `art.yaml` 不存完整提示词，只存视觉稳定要素和文件索引。
