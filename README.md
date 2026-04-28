# Novel Studio

Novel Studio 是一个面向 Claude Code 的小说创作插件仓库。插件名是 `ns`，技能统一以 `NS` 作为识别前缀，适合长篇、短篇、连载、系统文、无限流、悬疑、言情、奇幻、科幻、历史和现实题材。

这个仓库只管理 Novel Studio 一个插件。个人插件市场路由仓库是 `honestman9527/my-skills`，它会指向这个独立插件仓库。

## Claude Code 在线安装

推荐从个人插件市场安装：

```powershell
claude plugin marketplace add honestman9527/my-skills
claude plugin install ns@my-skills
```

也可以直接把本仓库作为 marketplace 添加：

```powershell
claude plugin marketplace add honestman9527/novel-studio
claude plugin install ns@novel-studio
```

在 Claude Code 交互界面中也可以使用：

```text
/plugin marketplace add honestman9527/my-skills
/plugin install ns@my-skills
/reload-plugins
```

## 本地开发加载

```powershell
claude --plugin-dir D:\projects\novel-studio
```

安装后可用的技能入口：

```text
/ns:ns
/ns:ns-brainstorm
/ns:ns-memory
/ns:ns-architect
/ns:ns-research
/ns:ns-draft
/ns:ns-illustration
```

## 技能分工

- `ns`: 总入口、流程路由和项目管理。
- `ns-brainstorm`: 写作前脑暴，收束题材、卖点、主角和开篇钩子。
- `ns-memory`: 初始化、读取和回写本地长期记忆。
- `ns-architect`: 撰写世界观、人物、势力、规则、大纲和章节纲。
- `ns-research`: 联网查找素材、考据、视觉参考并记录来源。
- `ns-draft`: 正文写作、续写、改写、润色、章节检查和完稿收尾。
- `ns-illustration`: 生成封面、角色、场景、道具和分镜插画提示词。

## 多小说工作区

推荐一个工作区管理多本小说，每本小说一个文件夹：

```text
novel-workspace/
  00-workspace/
    index.md
    shared-source-log.md
  novels/
    book-a/
      00-meta/
      01-brainstorm/
      02-bible/
      03-outline/
      04-drafts/
      05-revisions/
      06-art/
      07-finish/
    book-b/
```

初始化多小说工作区：

```powershell
python skills/ns-memory/scripts/init_novel_project.py ./novel-workspace --novel book-a --title "第一本小说" --mode long --genre system --genre infinite-flow
```

初始化单本小说根目录：

```powershell
python skills/ns-memory/scripts/init_novel_project.py ./book-a --single-novel --title "第一本小说" --mode long
```

章节完成后追加回写：

```powershell
python skills/ns-memory/scripts/apply_chapter_backwrite.py ./novel-workspace ./novel-workspace/novels/book-a/04-drafts/volumes/volume-001/chapters/ch001.md --novel book-a --chapter-id ch001 --title "第001章"
```

## 仓库结构

```text
novel-studio/
  .claude-plugin/
    plugin.json        # Claude Code 插件 manifest
    marketplace.json   # 允许本仓库也作为 marketplace 安装
  assets/
  skills/
    ns/
    ns-brainstorm/
    ns-memory/
    ns-architect/
    ns-research/
    ns-draft/
    ns-illustration/
```
