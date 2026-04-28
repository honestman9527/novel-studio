---
name: ns-memory
description: "小说长期记忆与本地资料库技能。用于创建、读取、更新 NS 小说工作区；一个工作区可管理多本小说，每本小说一个文件夹，让长篇、短篇、连载、系统文、无限流等项目在多轮对话和多次写作中保持人物、世界观、时间线、伏笔、素材来源、章节进度和完稿资料一致；当用户要求建立项目、记住设定、保存资料、继续之前的小说、更新大纲或本地记忆时使用。"
---

# NS Memory

用本地文件夹作为长期记忆。默认一个工作区可管理多本小说，每本小说一个独立文件夹。

## 初始化

可运行脚本创建目录和模板：

```bash
python scripts/init_novel_project.py <workspace-dir> --novel my-book --title "我的小说" --mode long --genre system
```

`--mode` 可选 `short`、`novella`、`long`、`serial`。`--genre` 可多次填写，如 `--genre system --genre infinite-flow`。

如果用户明确只想建单本小说根目录，可加 `--single-novel`。

## 工作区结构

```text
<workspace-dir>/
  00-workspace/
    index.md
    shared-source-log.md
  novels/
    <novel-slug>/
      00-meta/
      01-brainstorm/
      02-bible/
      03-outline/
      04-drafts/
      05-revisions/
      06-art/
      07-finish/
```

工作区级文件只做多本小说索引和共享素材；单本小说资料必须写入 `novels/<novel-slug>/`。

## 记忆结构

读取 [memory-schema.md](references/memory-schema.md) 获取完整目录说明。单本小说核心目录：

- `00-meta/`：项目概览、创作契约、进度、素材来源。
- `01-brainstorm/`：脑暴记录、方向取舍、废案。
- `02-bible/`：世界观、人物、势力、系统、无限流、副本、时间线、名词表、伏笔。
- `03-outline/`：全书结构、卷纲、章节纲。
- `04-drafts/`：正文草稿。
- `05-revisions/`：修改记录和版本说明。
- `06-art/`：视觉设定和插画提示词。
- `07-finish/`：简介、梗概、章节摘要、完稿总结。

## 更新协议

1. 写作前读取 `00-meta/project.md`、`00-meta/progress.md` 和当前任务相关资料。
2. 新增事实只写入一个主文件，其他位置用引用或摘要。
3. 写完章节后更新：进度、时间线、人物状态、事件与伏笔、名词表、素材来源、章节摘要。
4. 不确定的内容写入 `01-brainstorm/open-questions.md`，不要混入已确定设定。
5. 改动已出场设定时，记录兼容解释或列出需要回修的章节。

## 章节后自动回写

写完章节后可运行：

```bash
python scripts/apply_chapter_backwrite.py <workspace-dir>/novels/my-book <chapter-file> --chapter-id ch001 --title 第001章
```

脚本会追加更新 `00-meta/progress.md`、`07-finish/chapter-summary.md`、`02-bible/timeline.md`、`02-bible/foreshadowing.md` 和 `05-revisions/revision-log.md`。它只做机械辅助；人物状态、系统奖励、副本结果和重大设定仍要人工复核后写入对应 bible 文件。
