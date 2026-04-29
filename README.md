# Novel Studio

Novel Studio 是一个面向 Claude Code 和 Codex 的小说创作插件仓库。插件名是 `ns`，技能统一以 `NS` 作为识别前缀，适合长篇、短篇、连载、系统文、无限流、悬疑、言情、奇幻、科幻、历史和现实题材。

仓库同时提供 Claude Code 和 Codex 两套插件生态入口：

- Claude Code：`.claude-plugin/plugin.json` 和 `.claude-plugin/marketplace.json`
- Codex：`.codex-plugin/plugin.json`

## 核心模型

Novel Studio 只保留新版单本小说目录模型：

```text
my-novel/
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
    logs/
  volumes/
    volume-001/
      ch001.md
      ch002.md
  extras/
    extra-001.md
```

当前文件夹就是这部小说的根目录；`novel-studio/` 是唯一记忆目录；正文必须放在 `volumes/`、`extras/` 等目录中。

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

## Codex 插件生态

Codex 插件 manifest 位于：

```text
.codex-plugin/plugin.json
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

- `ns`：总入口、流程路由和阶段协作。
- `ns-brainstorm`：写作前脑暴，收束题材、卖点、主角和开篇钩子。
- `ns-memory`：维护 `novel-studio/` YAML 长期记忆。
- `ns-architect`：撰写世界观、人物、势力、规则、大纲、卷纲、章节纲和连续性资料。
- `ns-research`：联网查找素材、考据、视觉参考并记录来源。
- `ns-draft`：正文写作、续写、改写、润色、章节检查和完稿收尾。
- `ns-illustration`：生成封面、角色、场景、道具和分镜插画提示词。

## 章节结构

章节必须放在卷或番外目录中，例如 `volumes/volume-001/ch001.md`。每章必须包含 YAML frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。发布正文时只取 `## 正文`。

## 常用命令

日常写作优先直接编辑 YAML/Markdown；脚本只作为可选辅助。

初始化当前目录为一部小说：

```powershell
python D:\projects\novel-studio\skills\ns-memory\scripts\init_novel_project.py . --title "第一本小说" --mode long --genre system --genre infinite-flow
```

章节有效字数和占位检查：

```powershell
python D:\projects\novel-studio\skills\ns-draft\scripts\chapter_audit.py .\volumes\volume-001\ch001.md
```

生成自动回写候选：

```powershell
python D:\projects\novel-studio\skills\ns-memory\scripts\apply_chapter_backwrite.py . .\volumes\volume-001\ch001.md --chapter-id ch001 --title "第001章"
```

素材来源日志：

```powershell
python D:\projects\novel-studio\skills\ns-research\scripts\append_source_log.py . --topic "清代驿站" --source "示例来源" --url "https://example.com/source" --material "可转化素材" --position "novel-studio/research.yaml"
```

插画提示词日志：

```powershell
python D:\projects\novel-studio\skills\ns-illustration\scripts\append_art_prompt.py . --type character --title "主角立绘" --target-model "通用中文" --prompt "黑发青年，旧风衣，站在雨夜街口" --negative "文字，水印" --stable "黑发，灰眼，旧风衣" --variable "表情、光线和背景"
```

开发自检：

```powershell
python skills/ns/scripts/smoke_test_ns_scripts.py
```

## 仓库结构

```text
novel-studio/
  .claude-plugin/
  .codex-plugin/
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
