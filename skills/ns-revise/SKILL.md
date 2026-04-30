---
name: ns-revise
description: "小说正文修订技能。用于修改已有章节或片段：润色、小改、对白优化、节奏调整、扩写/压缩、去 AI 味、重写场景、调整 POV 或结构改；区分轻改与结构改，并按影响同步章末笔记、continuity.yaml、memory.yaml、plan.yaml、notes/*.md 和 logs/revision.md。"
---

# NS Revise

只改已有文本；新写走 `$ns-write`。

## 读取

- 待改章节或片段。
- `project.yaml`
- `plan.yaml`
- `NOVEL.md`（存在时读取；不要自行创建或修改）
- `memory.yaml`
- `continuity.yaml`
- `style.yaml`

## 模式

- `light`：润色、压缩、扩写、对白、画面和节奏；不改事件结果或长期设定。
- `structural`：重写场景、改变冲突、调整 POV、改开头结尾或按新大纲重构；同步记忆和连续性。

## 流程

1. 明确保留项、修改目标和修订范围。
2. 轻改可直接改；结构改先给替换方案或场景顺序。
3. 只替换目标片段或目标章节。
4. 更新 `updated_at`、必要的 `word_count` 和 `index.yaml`。
5. 结构改再同步 `plan.yaml`、`continuity.yaml`、`memory.yaml`、必要 notes 和 `logs/revision.md`。
6. 新全局规则交给 `$ns-canon`，经同意再写 `NOVEL.md`。

## Notes

修订过程写 logs；长人物/时间线变化写 notes。YAML 和 frontmatter 只留结果摘要、索引和路径。

## 同步顺序

1. 改 Markdown。
2. 统计字数，更新 frontmatter。
3. 轻改同步 `index.yaml`；结构改同步相关 YAML/notes/logs。

## 字数

有字数或比例要求时，落盘后用 `novel-studio/tools/word_count.py` 或 `skills/ns-write/scripts/chapter_audit.py` 统计。未统计不能把估算当实际字数。
