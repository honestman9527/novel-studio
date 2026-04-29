---
name: ns-init
description: "NS 小说项目初始化与接入技能。用于把空文件夹初始化为一部小说项目，或把已有 Markdown 小说接入 Novel Studio；创建 content/ 正文结构、novel-studio/ YAML/Markdown 记忆、根目录 brief.md、visuals/、media/，并把字数检测脚本复制到 novel-studio/tools/。当用户要求初始化、接入旧项目、整理目录、迁移到 NS、准备发布/展示正文目录或生成基础记忆文件时使用。"
---

# NS Init

当前文件夹就是小说根目录。只创建结构、模板和工具，不写正文。

## 结构

```text
content/
  volumes/volume-001/_index.md
  volumes/volume-001/ch001.md
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
  tools/word_count.py
brief.md
visuals/
media/
```

- `content/`：正文；`_index.md` 是卷简介。
- `novel-studio/`：唯一记忆目录。
- `brief.md`：对外简介。
- `visuals/`：提示词。
- `media/`：图片素材。

旧项目已有 `volumes/`、`extras/` 时不强制搬迁，只在 `index.yaml` 登记。

## 流程

1. 判断空项目、已有 NS 项目、已有 Markdown 正文或混合旧结构。
2. 创建缺失目录和文件。
3. 复制 `assets/tools/word_count.py` 到 `novel-studio/tools/word_count.py`；目标已存在时不覆盖，除非用户要求。
4. 扫描已有 `.md`，写入 `index.yaml.entries`；不批量改正文。

## 最小 YAML

- `project.yaml`：书名、slug、状态、类型、受众、承诺、禁区。不要写 `content_root`。
- `publish.yaml`：唯一记录 `site.content_root`、卷目录、番外目录、媒体目录、排序和过滤规则。
- `index.yaml`：只记录正文条目路径、状态、字数、排序；不写 `content_root`。
- `finish.yaml`：只记录完稿状态、里程碑、输出文件索引。
- `art.yaml`：只记录视觉一致性和文件索引；完整提示词写 `visuals/*.md`。

## Markdown

- `brief.md`：`# 作品简介`，含读者简介、标签、卖点、Pitch、封面文案。
- `notes/*.md`：长文记忆，不编造占位内容。
- `logs/*.md`：修订和调研日志。
