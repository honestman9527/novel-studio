---
name: ns-revise
description: "小说正文修订技能。用于修改已有章节或片段：润色、小改、对白优化、节奏调整、局部扩写/压缩、去 AI 味、重写场景、调整 POV、重构章节顺序或按新方案大改剧情；负责区分轻改与结构改，并在影响事实或连续性时同步可选章末笔记、continuity.yaml、memory.yaml、plan.yaml 和 logs/revision.md。"
---

# NS Revise

只修改已有文本。新写下一章走 `$ns-write`。

## 读取

- 待改章节或片段。
- `project.yaml`
- `plan.yaml`
- `memory.yaml`
- `continuity.yaml`
- `style.yaml`

## 模式

- `light`：润色、压缩、扩写、对白、画面感、语病和节奏；不改变事件结果、人物选择、世界规则或长期设定。
- `structural`：重写场景、改变冲突、调整 POV、改开头结尾、按新大纲重构章节；必须同步记忆和连续性。

## 流程

1. 明确保留什么、改变什么、修订解决什么问题。
2. 轻改可直接给改后文本；结构改先给场景顺序或替换方案。
3. 落盘时只替换目标片段或目标章节。
4. 事实变化同步到 canon；若章节已有 `## 章末笔记`，用普通 Markdown 补一条修订备注，并更新 frontmatter 的 `updated_at` 和必要的 `word_count`。
5. 结构改同步 `plan.yaml`、`continuity.yaml`、`memory.yaml`、`index.yaml` 和 `logs/revision.md`。

## 字数

有字数或比例要求时，落盘后用 `novel-studio/tools/word_count.py` 或 `skills/ns-write/scripts/chapter_audit.py` 统计。未统计不能把估算当实际字数。
