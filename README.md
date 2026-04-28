# Novel Studio

Novel Studio 是一个面向 Claude Code 的小说创作插件仓库。插件名是 `ns`，技能统一以 `NS` 作为识别前缀，适合长篇、短篇、连载、系统文、无限流、悬疑、言情、奇幻、科幻、历史和现实题材。

这个仓库只管理 Novel Studio 一个插件。个人插件市场路由仓库是 `honestman9527/my-marketplace`，它会指向这个独立插件仓库。

仓库同时提供 Claude Code 和 Codex 两套插件生态入口：

- Claude Code：`.claude-plugin/plugin.json` 和 `.claude-plugin/marketplace.json`
- Codex：`.codex-plugin/plugin.json`

## Claude Code 在线安装

推荐从个人插件市场安装：

```powershell
claude plugin marketplace add honestman9527/my-marketplace
claude plugin install ns@my-marketplace
```

也可以直接把本仓库作为 marketplace 添加：

```powershell
claude plugin marketplace add honestman9527/novel-studio
claude plugin install ns@novel-studio
```

在 Claude Code 交互界面中也可以使用：

```text
/plugin marketplace add honestman9527/my-marketplace
/plugin install ns@my-marketplace
/reload-plugins
```

## 本地开发加载

```powershell
claude --plugin-dir D:\projects\novel-studio
```

## Codex 插件生态

Codex 插件 manifest 位于：

```text
.codex-plugin/plugin.json
```

它声明了插件名 `ns`、技能目录 `./skills/`、展示信息和 `assets/` 下的图标资源。维护 Codex 入口时优先保持这些字段和 Claude manifest 的基础元信息一致：`name`、`version`、`description`、`author`、`homepage`、`repository`、`license` 和 `keywords`。

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
- `ns-brainstorm`: 写作前脑暴，收束题材、卖点、主角和开篇钩子，并可写入脑暴记录。
- `ns-memory`: 初始化、读取和回写本地长期记忆，支持短篇最小结构。
- `ns-architect`: 撰写世界观、人物、势力、规则、大纲和章节纲。
- `ns-research`: 联网查找素材、考据、视觉参考并记录来源，默认按 URL 去重。
- `ns-draft`: 正文写作、续写、改写、润色、章节检查、有效字数审计和完稿收尾。
- `ns-illustration`: 生成封面、角色、场景、道具和分镜插画提示词，并可写入 `06-art/prompts.md`。

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

初始化一次性短篇最小结构：

```powershell
python skills/ns-memory/scripts/init_novel_project.py ./novel-workspace --novel short-a --title "短篇 A" --mode short --minimal-short
```

## 常用辅助脚本

章节有效字数和占位检查：

```powershell
python skills/ns-draft/scripts/chapter_audit.py ./novel-workspace/novels/book-a/04-drafts/volumes/volume-001/chapters/ch001.md
```

素材来源记录，默认按 URL 去重：

```powershell
python skills/ns-research/scripts/append_source_log.py ./novel-workspace --novel book-a --topic "清代驿站" --source "示例来源" --url "https://example.com/source" --material "可转化素材" --position "02-bible/realism.md"
```

插画提示词写入，默认按“类型 + 标题 + 目标模型”替换旧记录：

```powershell
python skills/ns-illustration/scripts/append_art_prompt.py ./novel-workspace --novel book-a --type character --title "主角立绘" --target-model "通用中文" --prompt "黑发青年，旧风衣，站在雨夜街口" --negative "文字，水印" --stable "黑发，灰眼，旧风衣" --variable "表情、光线和背景"
```

开发自检：

```powershell
python skills/ns/scripts/smoke_test_ns_scripts.py
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
      scripts/
    ns-brainstorm/
    ns-memory/
      scripts/
    ns-architect/
    ns-research/
      scripts/
    ns-draft/
      scripts/
    ns-illustration/
      scripts/
```
