---
name: ns-continue
description: "小说线性续写技能。用于从现有章节、片段、上一章结尾或当前卷计划继续往下写正文；新项目正文写入 content/volumes/ 或 content/extras/，旧项目兼容 volumes/、extras/。当用户说续写、接着写、继续上一章、写下一章、下一回、从这里往后写、承接某段剧情或沿当前卷推进时使用。新开卷、番外、独立短篇、序章、尾声走 ns-draft；大改走 ns-rewrite-heavy；小改走 ns-rewrite-light。"
---

# NS Continue

顺着已有文本或当前卷计划继续写。普通“下一章”默认用本 skill。

## 读取

- `novel-studio/project.yaml`
- `novel-studio/plan.yaml`
- `novel-studio/memory.yaml`
- `novel-studio/continuity.yaml`
- `novel-studio/publish.yaml`
- 当前章节、上一章结尾、当前卷计划

## 原则

- 承接上一段动作、情绪或信息，不跳场。
- 延续视角、语气、人物动机和场景状态。
- 每次至少推进一个变化：信息、关系、处境、选择、伏笔或代价。
- 不推翻已定设定；矛盾写入 `章末回写` 待确认。

## 输出

- 同章续写：追加到 `## 正文`。
- 下一章：创建 `content/volumes/volume-*/ch*.md`，旧项目沿用已登记目录。
- 写完更新 `章末回写`、`index.yaml`、`continuity.yaml`、`memory.yaml`。
- `finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。

## 字数

- 明确字数要求是硬验收。
- 落盘后用 `python novel-studio/tools/word_count.py <chapter-file>`；开发插件时可用 `python skills/ns-draft/scripts/chapter_audit.py <chapter-file>`。
- 未统计不能声称达标；不足就补写或报告差额和承接点。
