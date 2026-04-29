---
name: ns-init
description: "NS 小说项目初始化与接入技能。用于把空文件夹初始化为一部小说项目，或把已经写过正文的文件夹接入 Novel Studio；创建通用发布/展示友好的 content/ 正文结构、novel-studio/ YAML 与 Markdown 记忆、根目录 brief.md、visuals/、media/，并把基础字数检测脚本复制到 novel-studio/tools/。当用户要求初始化项目、接入旧项目、整理目录结构、迁移到 NS、为小说网站或其他发布渠道准备正文目录、生成基础记忆文件时使用。"
---

# NS Init

负责初始化或接入一部小说项目。当前文件夹就是小说根目录；不要在根目录下再创建同名小说文件夹。初始化只创建结构、模板和工具，不替用户写正文。

## 目标结构

新项目默认使用通用发布/展示友好的结构：

```text
<novel-root>/
  content/
    volumes/
      volume-001/
        _index.md
        ch001.md
    extras/
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
      characters.md
      world.md
      timeline.md
      glossary.md
      style.md
      synopsis.md
      open-threads.md
    logs/
      revision.md
      research-log.md
    tools/
      word_count.py
  brief.md
  visuals/
  media/
    covers/
    illustrations/
```

- `content/`：可发布正文，适配小说网站、静态生成器、导出脚本或人工整理；章节 Markdown 必须有 YAML frontmatter。
- `content/volumes/volume-*/_index.md`：卷索引和卷简介，可写本卷标题、卷简介、阶段目标和封面信息。
- `novel-studio/`：唯一记忆目录，放 YAML 事实库、Markdown 人类可读笔记、日志和本地工具。
- `brief.md`：根目录对外简介展示文件，集中放读者简介、标签、卖点、pitch 和封面文案。
- `visuals/`：封面、角色、场景、分镜等提示词稿。
- `media/`：真实图片、封面和插图素材。

已有项目如果已经使用 `volumes/`、`extras/`，不要强制移动；在 `novel-studio/index.yaml` 登记现有路径，并建议后续新正文写入 `content/`。

## 初始化流程

1. 判断项目状态：空项目、已有 NS 结构、已有 Markdown 正文、混合旧结构。
2. 创建缺失目录：`content/volumes/volume-001/`、`content/extras/`、`novel-studio/notes/`、`novel-studio/logs/`、`novel-studio/tools/`、`visuals/`、`media/covers/`、`media/illustrations/`。
3. 创建缺失 YAML：`project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`index.yaml`、`style.yaml`、`research.yaml`、`art.yaml`、`finish.yaml`、`publish.yaml`。
4. 创建缺失 Markdown：根目录 `brief.md`、`content/volumes/volume-001/_index.md`、`notes/characters.md`、`notes/world.md`、`notes/timeline.md`、`notes/glossary.md`、`notes/style.md`、`notes/synopsis.md`、`notes/open-threads.md`、`logs/revision.md`、`logs/research-log.md`。
5. 复制 `assets/tools/word_count.py` 到项目的 `novel-studio/tools/word_count.py`；如果目标已存在，先读目标，除非用户要求覆盖，否则只提示可更新。
6. 如果已有章节文件，扫描 Markdown 文件，登记到 `index.yaml.entries`，不要改写正文。
7. 写入 `publish.yaml`，记录发布/展示需要的书名、slug、正文根目录、默认排序、输出目标和封面路径。

## 模板原则

- YAML 存结构化事实，Markdown 存长说明和便于人读的笔记。
- 初始化模板宁可留空字段，也不要编造书名、人物或设定。
- 章节 frontmatter 面向小说网站、导出脚本和写作工作流同时可用：`title`、`date`、`draft`、`type`、`volume`、`weight`、`word_target`、`status`、`pov`、`timeline`。
- 只把可发布正文放在 `## 正文`；`## 写作目标` 和 `## 章末回写` 是工作区段，发布或导出时可过滤。

## 最小文件骨架

`project.yaml` 至少包含：

```yaml
title: ""
slug: ""
status: planning
language: zh-CN
primary_genres: []
audience: ""
promise: ""
boundaries: []
```

不要在 `project.yaml` 里维护正文根目录；正文根目录只写在 `publish.yaml.site.content_root`。

`publish.yaml` 至少包含：

```yaml
site:
  generator: generic
  content_root: content
  volumes_dir: content/volumes
  extras_dir: content/extras
  media_dir: media
  cover: media/covers/cover.jpg
chapter:
  body_heading: "正文"
  hide_work_sections: true
  sort_by: weight
```

`index.yaml` 至少包含：

```yaml
entries: []
extras: []
legacy_paths: []
```

`index.yaml` 不再保存 `content_root`；正文根目录只以 `publish.yaml.site.content_root` 为准。`index.yaml.entries[*].path` 使用相对项目根目录的路径，例如 `content/volumes/volume-001/ch001.md`。

`finish.yaml` 至少包含：

```yaml
status: drafting
milestones: []
outputs:
  public_brief: brief.md
  internal_synopsis: novel-studio/notes/synopsis.md
```

`finish.yaml` 只记录完稿状态、里程碑和输出文件索引，不存放简介、梗概、章节摘要等正文内容。

`art.yaml` 至少包含：

```yaml
style_profile: ""
visual_consistency:
  characters: []
  locations: []
  recurring_props: []
prompt_files: []
media_files: []
```

`art.yaml` 只记录视觉一致性和文件索引；完整提示词写入 `visuals/*.md`，实际图片写入 `media/`。

`notes/*.md` 可以用一级标题加空段落初始化，例如 `# 人物笔记`、`# 世界笔记`，不要写虚构内容占位。
`brief.md` 可以初始化为 `# 作品简介`，下设 `## 读者简介`、`## 标签`、`## 卖点`、`## Pitch`、`## 封面文案`。

## 接入旧项目

- 先保留用户已有目录和文件名。
- 识别根目录下的 `.md`、`volumes/**/*.md`、`extras/**/*.md`、`content/**/*.md`，把路径写入 `index.yaml`。
- 没有 frontmatter 的旧章节，先在 `index.yaml` 记录，不批量改写正文；需要时再逐章补 frontmatter。
- 旧项目有图片或封面时，建议搬到 `media/`；提示词放到 `visuals/`，简介和封面文案集中写入根目录 `brief.md`。

## 验证

初始化后运行：

```powershell
python .\novel-studio\tools\word_count.py .\content\volumes --json
```

没有章节时，脚本可以没有结果；只要 `novel-studio/tools/word_count.py` 可执行即可。
