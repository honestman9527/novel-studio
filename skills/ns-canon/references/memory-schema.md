# Memory Schema

当前文件夹就是小说根目录。`novel-studio/` 是唯一结构化记忆目录；新正文放 `content/volumes/`、`content/extras/`。文件模板见 [content-templates.md](content-templates.md)。

## 目录

```text
NOVEL.md  # 用户同意后创建/维护
novel-studio/
  project.yaml
  plan.yaml
  memory.yaml
  continuity.yaml
  index.yaml
  style.yaml
  research.yaml
  art.yaml
  finish.yaml
  publish.yaml
  notes/
  logs/
  tools/word_count.py
content/
  volumes/volume-001/_index.md
  volumes/volume-001/ch001.md
  extras/
brief.md
visuals/
media/
```

## 职责

- `NOVEL.md`：根目录全局约束，记录必须遵守、不要写/不要改、风格偏好、内容边界、结构偏好和待确认；创建和修改需要用户同意。
- `project.yaml`：项目身份、类型、受众、承诺、禁区。
- `plan.yaml`：全书规模、卷、章节、番外、下一步。
- `memory.yaml`：人物、世界、关系、名词、道具、伏笔、类型模块。
- `continuity.yaml`：当前状态、事件、未收束线、改写影响。
- `index.yaml`：正文条目路径、状态、字数、排序；不写 `content_root`。
- `style.yaml`：文风、禁忌、章节结构契约。
- `research.yaml`：来源、待查问题、事实边界。
- `publish.yaml`：正文根目录唯一来源、排序、slug、封面、过滤规则。
- `finish.yaml`：完稿状态、里程碑、输出索引；不存正文。
- `art.yaml`：视觉一致性、提示词文件、媒体文件；不存完整提示词。
- `notes/*.md`：人物、世界、时间线、术语、风格样例、梗概和待确认问题的长说明。
- `brief.md`：对外简介、标签、卖点、pitch、封面文案。
- `visuals/*.md`：完整提示词；`media/` 存实际图片素材。

## 协作规则

- 先判断唯一来源：结构化事实归 YAML，正文和长说明归 Markdown，frontmatter 只做连接层。
- YAML 管结构化事实；`NOVEL.md` 管全局约束；其它 Markdown 管长说明或展示。
- `NOVEL.md` 可以读取；写入前必须确认用户已同意。没有同意时，把建议作为待确认项报告，不偷偷落盘。
- Markdown frontmatter 只放身份、归属、时间、状态和字数；不要放长梗概、正文摘要、大段设定或执行过程。
- `index.yaml.entries` 同步章节 frontmatter 的 `id`、`volume_id`、`chapter_number`、`title`、`path`、`status`、`word_count`、`created_at`、`updated_at`。
- `publish.yaml.site.content_root` 是正文根目录唯一来源。
- 卷 `_index.md` 存卷简介和章节目录，不替代 `plan.yaml` 的计划。
- `NOVEL.md` 只存全局约束，不复制设定库和大纲。
- `finish.yaml` 只在分卷完成、全书完稿或交付物变化时更新。

## 同步顺序

- 新建或移动章节：先写章节 Markdown 和 frontmatter，再同步 `index.yaml`，最后更新卷 `_index.md` 目录。
- 修改正文或章末笔记：先审计字数和更新时间，再同步 `index.yaml`、`continuity.yaml`、`memory.yaml`。
- 修改卷计划或全书规模：先改 `plan.yaml`，再同步卷 `_index.md` 的目录说明，不把计划长文复制进卷文件。
- 修改 notes 长文：保留 YAML 摘要和 notes 路径；不要把 notes 全文回灌进 YAML。
- 修改 `publish.yaml.site.content_root` 后，检查 `index.yaml.entries[].path` 是否仍位于正文根目录下。

## 文件体量

- YAML 和 frontmatter 只保存索引、状态、短摘要和指向长文档的路径。
- `NOVEL.md` 只保存全局约束，不保存设定库、剧情大纲、资料摘录或聊天记录。
- `notes/*.md` 是长文记忆的默认位置；单个 notes 文件只处理一个主题，过长或混入多个主题时拆分。
- `logs/*.md` 记录过程，长日志按日期或任务拆分。
- 正文章节可以按创作目标变长；不要为了文件体量把一个章节正文拆到 notes。

## 规模规划

`plan.yaml` 是总章数、卷数和番外计划的唯一来源。

- `scale.target_volumes`：预计卷数。
- `scale.target_main_chapters`：预计主线章节数，不含番外。
- `scale.target_extras`：预计番外篇数。
- `scale.target_total_words`：全书目标字数。
- `scale.chapter_word_target`：默认单章字数区间；章节 frontmatter 可覆盖。
- `scale.limits_are`：`soft` 表示计划可调整；`hard` 表示用户明确要求不要突破。
- `volumes[].planned_chapters` 的合计应接近 `scale.target_main_chapters`。
- `volumes[].chapter_range` 记录计划章节范围。
- `extras[]` 只登记计划和功能，正文写入 `content/extras/`。

## 文件结构

- 卷 `_index.md` 必须有 frontmatter、H1、`## 卷简介`、`## 卷承诺`、`## 本卷主要人物`、`## 章节目录`；`## 卷末笔记` 可选。
- 章节必须有 frontmatter、H1、`## 写作目标`、`## 正文`；`## 章末笔记` 可选。
- 发布或导出只取章节 `## 正文`。

卷 frontmatter 只写必要索引：

```yaml
id: volume-001
type: volume
volume_number: 1
title: "第一卷"
status: planning
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
```

章节 frontmatter 只写必要索引：

```yaml
id: ch001
type: main
chapter_number: 1
title: "章节标题"
volume_id: volume-001
status: draft
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
word_target: "3000-5000"
word_count:
  effective:
  counted_at:
```

`pov`、`timeline`、`location`、`tags` 写入 `## 写作目标` 或 `## 章末笔记`；`display_title`、`volume_number`、`volume_title`、`weight`、`memory_read`、`memory_write` 不进章节头部。

卷的 `subtitle`、`display_title`、`word_target`、`chapter_range` 不进卷头部；卷计划写 `plan.yaml.volumes[]`，卷简介和承诺写 `_index.md` 正文。
