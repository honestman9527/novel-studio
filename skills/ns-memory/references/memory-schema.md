# Memory Schema

当前文件夹就是一部小说的项目根目录。只保留新版结构：`novel-studio/` 是唯一记忆目录；正文必须放进卷、番外等正文目录，不直接散落在根目录。

## 项目结构

```text
{novel-root}/
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
      revision.md
      research-log.md
  volumes/
    volume-001/
      ch001.md
      ch002.md
  extras/
    extra-001.md
  visuals/
    cover-prompts.md
    image-prompts.md
    character-prompts.md
    storyboard-prompts.md
    style-bible.yaml
  briefs/
    blurb.md
    synopsis-short.md
    synopsis-long.md
    tags.md
    pitch.md
```

- `novel-studio/`：长期记忆、计划、约束、索引、资料和日志。
- `volumes/volume-*/`：正文章节。每卷一个目录，章节只放在卷目录里。
- `extras/`：番外、间章、附录、设定短篇等非主线正文。
- `visuals/`：图片、封面、角色、场景、分镜提示词和视觉输出稿。
- `briefs/`：简介、梗概、标签、投稿 pitch 和宣传文案。
- 只使用上面的目录约定。

## YAML 职责

- `project.yaml`：书名、项目代号、篇幅、类型、受众、核心承诺和禁区。
- `plan.yaml`：当前入口、卷计划、章节计划、番外计划、下一步。
- `memory.yaml`：世界观、人物、关系、势力、名词、道具、伏笔和类型模块。
- `continuity.yaml`：当前状态、事件台账、未收束线索、改写影响。
- `index.yaml`：正文文件索引，记录每个章节/番外路径、状态、有效字数。
- `style.yaml`：文风、禁忌、必须保留、章节结构契约。
- `research.yaml`：资料来源、待查问题、事实边界。
- `art.yaml`：视觉记忆索引；具体提示词正文放 `visuals/`。
- `finish.yaml`：完稿资料索引；具体简介和梗概正文放 `briefs/`。

## 章节文件结构

每个章节必须使用 YAML frontmatter，并保留三个固定一级工作区段。发布或导出正文时只取 `## 正文` 下的内容。

````markdown
---
id: ch001
type: main
volume: volume-001
title: "第001章"
status: draft
pov: ""
timeline: ""
word_target: "3000-5000"
memory_read:
  - novel-studio/project.yaml
  - novel-studio/plan.yaml
  - novel-studio/memory.yaml
  - novel-studio/continuity.yaml
memory_write:
  - novel-studio/index.yaml
  - novel-studio/continuity.yaml
  - novel-studio/finish.yaml
---

# 第001章

## 写作目标

- 本章功能：
- 主要冲突：
- 出场人物：
- 承接内容：
- 本章变化：
- 结尾钩子：

## 正文

这里写可发布正文。

## 章末回写

```yaml
summary: ""
character_updates: []
world_updates: []
timeline_events: []
foreshadowing: []
loose_threads: []
next_entry: ""
```
````

## 回写协议

1. 写作前读取 `project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`style.yaml`。
2. 写作时只把真正正文写入 `## 正文`，不要把长期设定混入正文段落。
3. 写完一章先填写本章 `章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`、`finish.yaml`。
4. 新事实只写入一个主 YAML 字段，其他文件引用路径或摘要。
5. 不确定内容写入 `continuity.yaml.loose_threads` 或 `research.yaml.open_questions`。
6. 改写旧章节时，更新 `continuity.yaml.revision_notes` 和 `logs/revision.md`。

## 类型模块位置

类型化资料统一收进 `memory.yaml.genre`：

- `system`：系统规则、面板、任务、奖励、限制和成长曲线。
- `infinite_flow`：空间规则、通关条件、惩罚、现实线和副本库。
- `mystery`：谜面、证据链、误导链和公平线索。
- `romance`：关系推进、信任变化和情感选择代价。
- `power_system`：奇幻、仙侠、玄幻的力量体系和代价。
- `scifi`：科技规则、社会后果和失控风险。
- `realism`：历史/现实题材的考据边界和待查事实。
- `game`：游戏或电竞规则、版本环境和比赛制度。
- `apocalypse`：末世资源、秩序和生存风险。
- `urban`：都市/职场行业规则、利益结构和现实压力。
- `journey`：旅行路线、站点主题和关系变化。
- `ensemble`：单元剧/群像的常驻人物、单元模板和长线变化。

## 生成内容位置

- 图片、封面、角色、场景、分镜提示词：写入 `visuals/`。
- 简介、梗概、标签、pitch、封面文案：写入 `briefs/`。
- `novel-studio/art.yaml` 和 `novel-studio/finish.yaml` 只保留索引、状态和摘要，不存放长篇生成正文。

## 工具原则

日常写作优先直接编辑 Markdown 和 YAML。只保留章节审计这类检查工具；初始化、回写、素材记录、提示词记录都用 Markdown/YAML 约束完成。
