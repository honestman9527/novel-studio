---
name: ns-write
description: "小说正文写作技能。用于写新的正文内容：下一章、续写片段、新开卷、番外、独立短篇、序章、尾声、结局初稿、系统文新阶段或无限流新副本；负责创建或追加章节、保持章节结构、按字数要求审计，并在写完后回写 index.yaml、continuity.yaml、memory.yaml 和必要的 notes 摘要。"
---

# NS Write

只写新的正文内容。修改旧文本走 `$ns-revise`，简介文案走 `$ns-pitch`。

## 读取

- `project.yaml`
- `plan.yaml`
- `NOVEL.md`（存在时读取；不要自行创建或修改）
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
- 写主线章节前检查 `plan.yaml.scale` 和对应 `volumes[].planned_chapters`；`limits_are: hard` 时不要超出目标章数，除非用户明确同意。
- 写番外前检查 `plan.yaml.extras[]`；计划外番外先登记目的、预计字数和状态。
- 每章保留 frontmatter、H1、`## 写作目标`、`## 正文`。
- 新建章节 frontmatter 只写必要索引：`id`、`type`、`chapter_number`、`title`、`volume_id`、`status`、`created_at`、`updated_at`、`word_target`、`word_count`。
- H1 用 `# 第001章 章节标题`，由 `chapter_number` 和 `title` 生成。
- 写完后直接更新 `index.yaml`、`continuity.yaml`、`memory.yaml`；如果用户希望保留回顾，可追加普通 Markdown 的 `## 章末笔记`。
- 若写完后的记忆更新太长，YAML 只写摘要和路径，长说明交给 `$ns-canon` 写入或拆分 `notes/*.md`。
- 不要把新产生的偏好或禁忌顺手写进 `NOVEL.md`；需要全局约束时让 `$ns-canon` 在用户同意后处理。
- 所属卷的 `_index.md` 同步章节目录行；新开卷时补 `## 卷简介` 和 `## 卷承诺`。
- `finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。

## 同步顺序

1. 写入章节 Markdown 和 frontmatter。
2. 统计有效字数并更新 frontmatter 的 `word_count` 与 `updated_at`。
3. 同步 `index.yaml.entries` 和卷 `_index.md` 目录。
4. 把已发生事实写入 `continuity.yaml`、`memory.yaml`；长说明只写 notes 路径。

## 章末笔记

`## 章末笔记` 是可选区块，只用普通 Markdown。需要时按下面写，不需要就省略：

```markdown
## 章末笔记

- 本章概要：
- 记忆更新：
- 未收束：
- 已解决：
- 下一章钩子：
- 修订备注：
```

不要在笔记里写未来剧情正文；未确认内容只写成“未收束”或“下一章钩子”。

## 字数

明确字数要求是硬验收。落盘后用：

```powershell
python novel-studio/tools/word_count.py <chapter-file>
```

开发插件自身时可用：

```powershell
python skills/ns-write/scripts/chapter_audit.py <chapter-file>
```

统计后把有效字数和统计时间写入 frontmatter 的 `word_count`。未统计不能声称达标；不足就补写或报告差额和承接点。

## 导出

发布或投稿稿只导出 `## 正文`：

```powershell
python skills/ns-write/scripts/export_text.py <novel-root> -o export/novel.md
```

默认保留卷标题和章节标题；只要纯正文时加 `--no-titles`。
