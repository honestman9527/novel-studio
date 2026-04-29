---
name: ns-memory
description: "小说长期记忆与本地资料库技能。用于创建、读取、更新单本 NS 小说项目：当前文件夹就是这部小说根目录，唯一记忆目录固定为 novel-studio/，正文放在 volumes/、extras/ 等卷和番外目录中；通过 YAML 文件维护项目约束、计划、记忆、连续性、正文索引、资料来源、视觉设定和完稿资料；当用户要求建立项目、记住设定、保存资料、继续之前的小说、更新大纲、维护计划或本地记忆时使用。"
---

# NS Memory

只使用新版结构：当前文件夹是一部小说，`novel-studio/` 是唯一记忆目录，正文放入 `volumes/`、`extras/` 等目录。

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
    logs/
  volumes/
    volume-001/
      ch001.md
  extras/
  visuals/
  briefs/
```

## 初始化原则

直接创建和编辑 YAML/Markdown，不使用脚本初始化。新项目至少创建 `novel-studio/project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`index.yaml`、`style.yaml`，以及 `volumes/volume-001/`、`extras/`、`visuals/`、`briefs/`。

## 记忆结构

读取 [memory-schema.md](references/memory-schema.md) 获取完整说明。核心文件：

- `novel-studio/project.yaml`：项目身份、类型、承诺、禁区。
- `novel-studio/plan.yaml`：卷、章节、番外和下一步计划。
- `novel-studio/memory.yaml`：人物、世界、关系、名词、伏笔和类型模块。
- `novel-studio/continuity.yaml`：当前状态、事件台账、待收束线索和改写影响。
- `novel-studio/index.yaml`：正文文件索引。
- `novel-studio/style.yaml`：文风和章节结构契约。
- `novel-studio/research.yaml`：资料来源、待查问题和事实边界。
- `novel-studio/art.yaml`：视觉记忆索引；提示词正文放 `visuals/`。
- `novel-studio/finish.yaml`：完稿资料索引；简介和梗概正文放 `briefs/`。

## 章节约束

章节文件必须放在卷或番外目录中，例如 `volumes/volume-001/ch001.md`、`extras/extra-001.md`。每章必须包含：

1. YAML frontmatter：`id`、`type`、`volume`、`title`、`status`、`pov`、`timeline`、`word_target`、`memory_read`、`memory_write`。
2. `## 写作目标`：本章功能、冲突、出场人物、承接内容、变化、钩子。
3. `## 正文`：唯一可发布正文区域。
4. `## 章末回写`：用 YAML 块记录摘要、人物变化、世界变化、时间线事件、伏笔、待收束线索、下一入口。

## 更新协议

1. 写作前读取 `project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`style.yaml`。
2. 写完章节后，先补本章 `章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`、`finish.yaml`。
3. 新事实只写入一个主 YAML 字段，避免多处散记。
4. 不确定内容写入 `continuity.yaml.loose_threads` 或 `research.yaml.open_questions`。
5. 改写旧章节时，更新 `continuity.yaml.revision_notes` 和 `novel-studio/logs/revision.md`。
6. 图片、封面、角色、场景、分镜提示词写入 `visuals/`。
7. 简介、梗概、标签、pitch、封面文案写入 `briefs/`。
