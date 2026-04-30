---
name: ns
description: "Novel Studio 总入口。用于单本小说项目的路由和阶段协调：初始化、脑暴、框架、根指导、canon/notes、调研、写作、修订、文案、视觉。当用户不知道用哪个 skill、请求混合动作、需要拆分过长文件，或要从模糊需求推进到下一步时使用。"
---

# NS

判断目标产物，转入最小可用子 skill。总入口只路由和排顺序。

## 总原则

- 根指导文件可读；写入全局指导走 `$ns-guidance`。
- YAML/frontmatter/根指导文件写短事实；长说明进 `novel-studio/notes/*.md`。
- SKILL.md 只放触发、职责和边界；细说明放 references，可复用模板放 assets/templates。
- 需要详细判断 YAML/Markdown 文件职责时，走 `$ns-canon` 并读取 `file-roles.md`。
- 改正文 Markdown 后同步 frontmatter、`index.yaml` 和 canon；改 YAML 后只同步必要 Markdown。
- 文件过长或职责不明时转 `$ns-canon` 整理。

## 路由

| 目标产物 | 使用 |
| --- | --- |
| 项目目录、初始 YAML、字数工具 | `$ns-start` |
| 刚开始写、基础询问、讨论想法、头脑风暴、故事方向、开篇钩子 | `$ns-ideate` |
| 世界观、人物、规则、大纲、卷纲 | `$ns-build` |
| 长期规则、禁区、风格偏好、全局指导 | `$ns-guidance` |
| 已定事实、进度、连续性、索引、notes | `$ns-canon` |
| 资料、考据、来源、视觉参考 | `$ns-research` |
| 新章节、续写、番外、序章、尾声 | `$ns-write` |
| 润色、压缩、扩写、重写、结构修订 | `$ns-revise` |
| 简介、标签、pitch、梗概、宣传文案 | `$ns-pitch` |
| 封面、角色、场景、分镜提示词 | `$ns-visual` |
| notes 长说明、人物档案、时间线、过长记忆拆分 | `$ns-canon` |

## 模糊判断

- “继续写/下一章/接着这里”：`$ns-write`。
- “新开卷/番外/序章/尾声/独立短篇”：`$ns-write`。
- “刚开始写/不知道怎么开始/聊想法/讨论一下/头脑风暴/还没想清楚”：`$ns-ideate`。
- “改一下/润色/重写/结构不行”：`$ns-revise`，由它判断轻改或结构改。
- “记住/更新设定/整理进度”：`$ns-canon`。
- “以后都要/不要再写/这个不能改/保持这种味道”：`$ns-guidance`。
- “改 notes/整理人物档案/这份太长拆一下”：`$ns-canon`。
- “简介/卖点/标签/投稿梗概”：`$ns-pitch`。
- “封面图/角色图/场景 prompt”：`$ns-visual`。

## 项目约束

- 当前文件夹是小说根目录；`novel-studio/` 是唯一记忆目录。
- 正文默认在 `content/volumes/` 和 `content/extras/`；旧项目可沿用已登记目录。
- 章节保留 frontmatter、H1、`## 写作目标`、`## 正文`；`## 章末笔记` 可选。
- 发布只取 `## 正文`；明确字数要求必须工具统计后再报告。
