---
name: ns-write
description: "小说正文写作技能。用于写新正文：下一章、续写、新开卷、番外、短篇、序章、尾声、结局初稿、系统文新阶段或无限流新副本；负责创建/追加章节、保持结构、字数审计，并回写 index.yaml、continuity.yaml、memory.yaml 和必要 notes 摘要。"
---

# NS Write

只写新正文；改旧文走 `$ns-revise`，文案走 `$ns-pitch`。

## 读取

- `project.yaml`
- `plan.yaml`
- 根指导文件（存在时读取；不要自行创建或修改）
- `memory.yaml`
- `continuity.yaml`
- `style.yaml`
- `publish.yaml`
- 当前章节、上一章结尾或用户给定片段

## 模式

- `continue`：承接上一章或片段，不跳场，至少推进一个变化。
- `new-unit`：新开卷、番外、序章、尾声或独立短篇，先定单元功能。
- `append`：同章续写，只追加到 `## 正文`。

## 输出

- 新章节写入 `content/volumes/` 或 `content/extras/`；旧项目沿用已登记目录。
- 写主线/番外前看 `plan.yaml`；硬限制只在用户同意后突破。
- 章节保留 frontmatter、H1、`## 写作目标`、`## 正文`；章末笔记按需使用。
- frontmatter 只写身份、归属、状态、时间、目标字数和统计字数。
- 写完更新 `index.yaml`、`continuity.yaml`、`memory.yaml` 和卷 `_index.md`；长说明只留 notes 路径。
- 新全局偏好或禁忌交给 `$ns-guidance`。

## 同步顺序

1. 写 Markdown/frontmatter。
2. 统计字数，更新 `word_count`、`updated_at`。
3. 同步 `index.yaml`、卷 `_index.md`、`continuity.yaml`、`memory.yaml`。

## 章末笔记

`## 章末笔记` 可选，用普通 Markdown；模板见 [chapter-note.md](assets/templates/chapter-note.md)。

## 字数

有明确字数要求时，落盘后统计：

```powershell
python novel-studio/tools/word_count.py <chapter-file>
```

开发插件自身时可用：

```powershell
python skills/ns-write/scripts/chapter_audit.py <chapter-file>
```

统计后写入 frontmatter；未统计不声称达标。

## 导出

发布或投稿稿只导出 `## 正文`：

```powershell
python skills/ns-write/scripts/export_text.py <novel-root> -o export/novel.md
```

默认保留卷标题和章节标题；只要纯正文时加 `--no-titles`。
