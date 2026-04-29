---
name: ns
description: "NS 小说创作插件总入口。用于路由和管理单本小说项目：当前文件夹就是小说根目录，novel-studio/ 是唯一记忆目录，新正文默认放 content/volumes/、content/extras/，旧项目兼容 volumes/、extras/。当用户不知道用哪个技能、请求含糊、混合多个写作动作，或要初始化/接入项目、拆分阶段、协调记忆、调研、架构、起草、续写、改写、简介、插画提示词时使用。"
---

# NS

先判断阶段，再转入子 skill。不要停在建议层。

## 路由

| 需求 | 使用 |
| --- | --- |
| 初始化空项目、接入已有正文、整理目录 | `$ns-init` |
| 写前发散、题材、卖点 | `$ns-brainstorm` |
| 维护记忆、计划、连续性 | `$ns-memory` |
| 世界观、人物、大纲、卷纲 | `$ns-architect` |
| 素材、考据、来源 | `$ns-research` |
| 新开卷、番外、序章、尾声、独立短篇 | `$ns-draft` |
| 接上一章、写下一章、续写片段 | `$ns-continue` |
| 小改、润色、局部扩写/压缩 | `$ns-rewrite-light` |
| 大改、重写、剧情重构 | `$ns-rewrite-heavy` |
| 简介、标签、pitch、梗概 | `$ns-blurb` |
| 封面、角色、场景、分镜提示词 | `$ns-illustration` |

## 模糊判断

- “继续写/下一章”：`$ns-continue`。
- “新开卷/番外/序章/尾声/独立短篇”：`$ns-draft`。
- “改一下”：不改事实用 `$ns-rewrite-light`；改剧情结构用 `$ns-rewrite-heavy`。
- “简介/卖点/标签”：`$ns-blurb`，对外写 `brief.md`，内部梗概写 `novel-studio/notes/synopsis.md`。
- “封面图/角色图提示词”：`$ns-illustration`，提示词写 `visuals/`。

## 结构

```text
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
  tools/word_count.py
content/
  volumes/volume-001/_index.md
  volumes/volume-001/ch001.md
  extras/
brief.md
visuals/
media/
```

## 硬约束

- 章节放 `content/volumes/` 或 `content/extras/`；旧项目可沿用已登记的 `volumes/`、`extras/`。
- 每章包含 YAML frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。
- 发布正文只取 `## 正文`。
- 字数必须用 `novel-studio/tools/word_count.py` 或 `skills/ns-draft/scripts/chapter_audit.py` 统计；未统计不能声称达标。
- 写完章节更新 `index.yaml`、`continuity.yaml`、`memory.yaml`；`finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。
