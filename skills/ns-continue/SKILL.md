---
name: ns-continue
description: "小说续写技能。用于从现有章节、片段、上一章结尾或 novel-studio/ 计划继续往下写正文；当用户说续写、接着写、继续上一章、写下一章、从这里往后写、承接某段剧情时使用。只负责延续正文和章末回写，不做大幅重构或全章改写；大改走 ns-rewrite-heavy，小改润色走 ns-rewrite-light，新章从零起草走 ns-draft。"
---

# NS Continue

负责顺着既有文本继续写，不重置方向。正文必须写在 `volumes/` 或 `extras/` 内，遵守章节结构契约。

## 写前读取

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/continuity.yaml`
5. 当前章节文件和上一章结尾

## 续写原则

- 延续已有视角、语气、场景状态和人物动机。
- 先承接上一段最后的动作、情绪或信息，不突兀跳场。
- 每次续写至少推进一个变化：信息、关系、处境、选择、伏笔或代价。
- 不擅自推翻已定设定；发现矛盾时在 `章末回写` 标记待确认。

## 字数与续写量

- 用户给出明确字数、字数区间或“至少/不低于/不少于”时，字数是硬性验收条件。
- 续写到文件后，使用 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>` 统计有效字数；只报告机器统计结果，不虚报估算。
- 如果只在对话中交付片段且没有落盘，必须说明字数未经过章节审计；有强字数要求时应优先落盘再统计。
- 未达标时继续补写；无法在本轮补足时，写明当前有效字数、目标字数、差额和下一段承接点。

## 输出结构

如果继续同一章，追加到该章 `## 正文` 下；如果开下一章，创建新的卷目录章节文件，并包含：

- YAML frontmatter
- `## 写作目标`
- `## 正文`
- `## 章末回写`

写完后更新本章 `章末回写`，再人工同步 `novel-studio/index.yaml`、`novel-studio/continuity.yaml`、`novel-studio/finish.yaml`。
