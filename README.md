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
  visuals/
    cover-prompts.md
    image-prompts.md
  briefs/
    blurb.md
    synopsis-short.md
```

当前文件夹就是这部小说的根目录；`novel-studio/` 是唯一记忆目录；正文必须放在 `volumes/`、`extras/` 等目录中。

不知道该用哪个技能时，直接使用 `ns`。入口会根据请求判断应转入记忆、架构、调研、起草、续写、轻改、重写、简介或插画提示词技能。

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
/ns:ns-continue
/ns:ns-rewrite-light
/ns:ns-rewrite-heavy
/ns:ns-blurb
/ns:ns-illustration
```

## 技能分工

- `ns`：总入口、流程路由和阶段协作；不知道用哪个技能时先用它分诊。
- `ns-brainstorm`：写作前脑暴，收束题材、卖点、主角和开篇钩子。
- `ns-memory`：维护 `novel-studio/` YAML 长期记忆。
- `ns-architect`：撰写世界观、人物、势力、规则、大纲、卷纲、章节纲和连续性资料。
- `ns-research`：联网查找素材、考据、视觉参考并记录来源；创作素材优先从小说素材站、写作站、网文资料和类型小说相关网站提炼，事实考据再用官方/学术/专业来源核验。
- `ns-draft`：起草新章节、新番外和新正文初稿。
- `ns-continue`：顺着已有章节或片段续写。
- `ns-rewrite-light`：轻改、小改、润色、局部扩写或压缩。
- `ns-rewrite-heavy`：大改、重写、重构章节或剧情。
- `ns-blurb`：生成简介、梗概、标签、pitch 和宣传文案，输出到 `briefs/`。
- `ns-illustration`：生成封面、角色、场景、道具和分镜插画提示词，输出到 `visuals/`。

## 章节结构

章节必须放在卷或番外目录中，例如 `volumes/volume-001/ch001.md`。每章必须包含 YAML frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。发布正文时只取 `## 正文`。

用户给出明确字数、字数区间或“不少于/不低于”要求时，必须用章节审计脚本或等价精确计数核验后再报告实际字数，不能虚报估算。

## 常用命令

日常写作直接编辑 YAML/Markdown。脚本只保留章节审计和开发烟测。

章节有效字数和占位检查：

```powershell
python D:\projects\novel-studio\skills\ns-draft\scripts\chapter_audit.py .\volumes\volume-001\ch001.md
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
    ns-continue/
    ns-rewrite-light/
    ns-rewrite-heavy/
    ns-blurb/
    ns-illustration/
```
