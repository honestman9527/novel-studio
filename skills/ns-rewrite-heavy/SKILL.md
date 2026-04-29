---
name: ns-rewrite-heavy
description: "小说重写和大改技能。用于大幅改写章节、重构场景顺序、改变剧情方案、重设人物选择、改 POV、改冲突、重写开头或结尾、把旧章节按新大纲重写；当用户说大改、重写、推翻这一章、按新方案改、结构不行、剧情要换、重构章节时使用。小范围润色和不改事实的局部优化走 ns-rewrite-light。"
---

# NS Rewrite Heavy

负责改变故事结构或剧情事实的大改。大改必须同步考虑记忆和连续性，不只替换文本。

## 写前读取

1. 待改章节或片段。
2. `novel-studio/project.yaml`
3. `novel-studio/plan.yaml`
4. `novel-studio/memory.yaml`
5. `novel-studio/continuity.yaml`
6. `novel-studio/style.yaml`

## 大改流程

1. 先列出改动意图：要保留什么、推翻什么、新版本解决什么问题。
2. 给出新章节功能和场景顺序。
3. 重写 `## 正文`，必要时同步改 `## 写作目标`。
4. 在 `## 章末回写` 明确列出对人物、世界、时间线、伏笔和待收束线索的影响。
5. 人工更新 `plan.yaml`、`continuity.yaml`、`memory.yaml`、`index.yaml` 和 `logs/revision.md`。

## 约束

- 不默默吞掉旧伏笔；被废弃的线索写进 `continuity.yaml.revision_notes`。
- 不让重写后的章节和前后章节断裂；必要时列出需要一起回修的文件。
- 不把旧稿全部删除为摘要；保留用户要求保留的台词、场景或设定。
- 用户要求指定字数、字数区间或“不少于/不低于”时，必须重写后运行 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>` 统计有效字数；未统计不能声称达标。
- 重写后不足目标字数时继续补写，或明确当前有效字数、目标字数、差额和下一段承接点。

## 输出

先给重写方案，再给可替换正文。用户要求直接改文件时，按章节结构落盘。
