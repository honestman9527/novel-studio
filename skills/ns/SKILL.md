---
name: ns
description: "Novel Studio 小说插件总入口。用于给单本小说项目做路由和阶段协调：初始化项目、脑暴点子、搭建故事框架、维护 canon 记忆、调研素材、写新正文、修订旧文本、生成简介文案和视觉提示词。当用户不知道用哪个 skill、请求混合多个动作或需要从模糊需求推进到具体下一步时使用。"
---

# NS

判断用户真正要改的产物，再进入最小可用子 skill。不要在总入口重复执行子 skill 的细节。

## 路由

| 目标产物 | 使用 |
| --- | --- |
| 项目目录、初始 YAML、字数工具 | `$ns-start` |
| 故事方向、卖点、主角欲望、开篇钩子 | `$ns-ideate` |
| 世界观、人物、规则、大纲、卷纲 | `$ns-build` |
| 已定事实、进度、连续性、索引 | `$ns-canon` |
| 资料、考据、来源、视觉参考 | `$ns-research` |
| 新章节、续写、番外、序章、尾声 | `$ns-write` |
| 润色、压缩、扩写、重写、结构修订 | `$ns-revise` |
| 简介、标签、pitch、梗概、宣传文案 | `$ns-pitch` |
| 封面、角色、场景、分镜提示词 | `$ns-visual` |

## 模糊判断

- “继续写/下一章/接着这里”：`$ns-write`。
- “新开卷/番外/序章/尾声/独立短篇”：`$ns-write`。
- “改一下/润色/重写/结构不行”：`$ns-revise`，由它判断轻改或结构改。
- “记住/更新设定/整理进度”：`$ns-canon`。
- “简介/卖点/标签/投稿梗概”：`$ns-pitch`。
- “封面图/角色图/场景 prompt”：`$ns-visual`。

## 项目约束

- 当前文件夹就是小说根目录；`novel-studio/` 是唯一记忆目录。
- 新正文放 `content/volumes/` 或 `content/extras/`；旧项目可沿用已登记的 `volumes/`、`extras/`。
- 章节必须包含 frontmatter、H1、`## 写作目标`、`## 正文`；frontmatter 记录章节号、标题、所属卷、状态、创建/更新时间和字数信息。`## 章末笔记` 可选，且使用普通 Markdown。
- 发布正文只取 `## 正文`。
- 明确字数要求必须用 `novel-studio/tools/word_count.py` 或 `skills/ns-write/scripts/chapter_audit.py` 统计后再报告。
