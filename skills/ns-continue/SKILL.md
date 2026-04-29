---
name: ns-continue
description: "小说线性续写技能。用于从现有章节、片段、上一章结尾或当前卷计划继续往下写正文；新项目正文写入 content/volumes/ 或 content/extras/，旧项目兼容 volumes/、extras/；当用户说续写、接着写、继续上一章、写下一章、下一回、从这里往后写、承接某段剧情、沿当前卷推进时使用。只负责延续正文和章末回写，不做大幅重构或全章改写；新开卷、番外、独立短篇、序章、尾声或不直接承接上一章的新单元走 ns-draft；大改走 ns-rewrite-heavy，小改润色走 ns-rewrite-light。"
---

# NS Continue

负责顺着既有文本或当前卷计划继续写，不重置方向。普通“下一章”默认属于本 skill；新项目正文必须写在 `content/volumes/` 或 `content/extras/` 内，旧项目兼容已有 `volumes/`、`extras/`，遵守章节结构契约。

## 写前读取

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/continuity.yaml`
5. `novel-studio/publish.yaml`
6. 当前章节文件、上一章结尾、当前卷计划和下一章目标

## 续写原则

- 延续已有视角、语气、场景状态和人物动机。
- 先承接上一段最后的动作、情绪或信息，不突兀跳场。
- 写下一章时，承接上一章结尾和当前卷目标，不把它当成新卷开篇。
- 每次续写至少推进一个变化：信息、关系、处境、选择、伏笔或代价。
- 不擅自推翻已定设定；发现矛盾时在 `章末回写` 标记待确认。

## 字数与续写量

- 用户给出明确字数、字数区间或“至少/不低于/不少于”时，字数是硬性验收条件。
- 续写到文件后，优先使用 `python novel-studio/tools/word_count.py <chapter-file>` 统计有效字数；开发插件自身时可使用 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>`；只报告机器统计结果，不虚报估算。
- 如果只在对话中交付片段且没有落盘，必须说明字数未经过章节审计；有强字数要求时应优先落盘再统计。
- 未达标时继续补写；无法在本轮补足时，写明当前有效字数、目标字数、差额和下一段承接点。

## 输出结构

如果继续同一章，追加到该章 `## 正文` 下；如果开下一章，优先创建 `content/volumes/volume-*/ch*.md`，旧项目沿用已登记的卷目录，并包含：

- YAML frontmatter
- `## 写作目标`
- `## 正文`
- `## 章末回写`

写完后更新本章 `章末回写`，再人工同步 `novel-studio/index.yaml`、`novel-studio/continuity.yaml`、`novel-studio/memory.yaml`；只有分卷完成、全书完稿或交付物变化时才更新 `novel-studio/finish.yaml`。

## 边界

- 普通下一章、下一回、接上一章结尾、沿当前卷推进：继续使用本 skill。
- 新开卷、番外、独立短篇、序章、尾声、特殊篇或新副本入口：转 `$ns-draft`。
- 需要改变既有剧情事实、章节结构或人物选择：转 `$ns-rewrite-heavy`。
