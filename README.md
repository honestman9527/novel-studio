# Novel Studio

Novel Studio 是一个面向 Claude Code Marketplace 和 Agent Skills 生态的小说创作仓库。插件名是 `ns`，技能统一以 `NS` 作为识别前缀，适合长篇、短篇、连载、系统文、无限流、悬疑、言情、奇幻、科幻、历史和现实题材。

仓库只保留 Claude Code marketplace 插件入口；其它支持 Agent Skills 的工具通过 `npx skills` 按需安装技能：

- Claude Code marketplace：`.claude-plugin/plugin.json` 和 `.claude-plugin/marketplace.json`
- Codex / Cursor / Gemini CLI / OpenCode 等：`npx skills add honestman9527/novel-studio`

## 核心模型

Novel Studio 只保留新版单本小说目录模型：

```text
my-novel/
  AGENTS.md / CLAUDE.md  # agent 项目约束
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
    records/
    tools/
      word_count.py
  content/
    volumes/
      volume-001/
        _index.md
        ch001.md
        ch002.md
    extras/
      extra-001.md
  visuals/
    cover-prompts.md
    image-prompts.md
  brief.md
  media/
    covers/
    illustrations/
```

当前文件夹就是这部小说的根目录；`novel-studio/` 是唯一记忆目录；新项目正文默认放在 `content/volumes/`、`content/extras/`。旧项目已有 `volumes/`、`extras/` 时可沿用。

`AGENTS.md` 或 `CLAUDE.md` 只保存 agent 在本项目里的执行约束，例如工作流、写入边界、协作偏好和禁区；不保存小说记忆、剧情进度、设定库或资料摘录。`novel-studio/*.yaml` 保存当前结构化记忆和索引；`novel-studio/notes/*.md` 保存长说明；`novel-studio/records/*.md` 保存进度、检查点、迁移、调研和修订过程记录；`content/`、`brief.md`、`visuals/` 和 `media/` 是主要创作产物。详细位置和同步关系见 `ns-canon` 的 `memory-schema.md` / `file-roles.md`。

不知道该用哪个技能时，直接使用 `ns`。入口会根据请求判断应转入启动、创意、框架、agent 约束、canon 记忆、调研、写作、修订、文案或视觉提示词技能。

## Claude Code 在线安装

推荐从插件市场安装：

```powershell
claude plugin marketplace add honestman9527/dream-marketplace
claude plugin install ns@dream-marketplace
```

在 Claude Code 交互界面中也可以使用：

```text
/plugin marketplace add honestman9527/dream-marketplace
/plugin install ns@dream-marketplace
/reload-plugins
```

## 本地开发加载

```powershell
claude --plugin-dir D:\projects\novel-studio
```

## 其它 Agent 安装

[`npx skills`](https://github.com/vercel-labs/skills) 是开放技能生态的 CLI 工具。除 Claude Code marketplace 外，其它支持 Agent Skills 的编码助手统一使用它安装，并在交互提示中按需选择技能。

```bash
npx skills add honestman9527/novel-studio
```

交互式提示会让你：

1. 选择要安装的技能（按需选择即可）
2. 选择目标 Agent（Codex / Cursor / Gemini CLI / OpenCode …）
3. 选择安装范围：**项目级**（仅当前仓库）或 **全局级**（所有项目）

安装完成后，技能文件会被放入对应 Agent 的技能目录（如 `.claude/skills/`、`.codex/skills/` 等），Agent 下次启动即可识别。

常用管理命令：

```bash
npx skills list              # 查看已安装技能
npx skills check             # 检查可用更新
npx skills update            # 更新所有技能到最新版本
npx skills remove <技能名>    # 移除指定技能
```

> **提示：** 更多技能可在 [skills.sh](https://skills.sh/) 浏览和发现。

### 安装后可用的技能入口

```text
/ns:ns
/ns:ns-start
/ns:ns-ideate
/ns:ns-build
/ns:ns-guidance
/ns:ns-canon
/ns:ns-research
/ns:ns-write
/ns:ns-revise
/ns:ns-pitch
/ns:ns-visual
```

## 技能分工

- `ns`：总入口，按目标产物路由到最小可用子技能。
- `ns-start`：初始化空项目或接入已有正文项目，只创建结构、基础记忆和 `novel-studio/tools/word_count.py`。
- `ns-ideate`：创意发散与收束，只产出题材方向、卖点、主角欲望和开篇钩子。
- `ns-build`：搭建故事圣经，只负责世界观、人物、类型规则、大纲、卷纲、章节计划和必要的长文 notes。
- `ns-guidance`：维护 `AGENTS.md` 或 `CLAUDE.md`，只记录 agent 项目约束和协作边界。
- `ns-canon`：维护 `novel-studio/` canon 记忆、notes、records、已定事实、连续性、索引和进度。
- `ns-research`：联网查找素材、考据、视觉参考并记录来源；创作素材优先从小说素材站、写作站、网文资料和类型小说相关网站提炼，事实考据再用官方/学术/专业来源核验。
- `ns-write`：写新的正文内容，统一负责下一章、续写、新开卷、番外、序章、尾声和独立短篇。
- `ns-revise`：修订已有正文，统一负责润色、小改、扩写、压缩、重写和结构改。
- `ns-pitch`：生成简介、标签、pitch 和宣传文案到根目录 `brief.md`，内部梗概写入 `novel-studio/notes/synopsis.md`。
- `ns-visual`：生成封面、角色、场景、道具和分镜插画提示词，输出到 `visuals/`。

## 卷和章节结构

章节必须放在卷或番外目录中，新项目路径例如 `content/volumes/volume-001/ch001.md`、`content/extras/extra-001.md`。每卷用 `_index.md` 维护卷简介、卷承诺、主要人物和章节目录；`## 卷末笔记` 可选。

每章必须包含 YAML frontmatter、H1、`## 写作目标`、`## 正文`。frontmatter 只记录 `id`、`type`、`chapter_number`、`title`、`volume_id`、`status`、`created_at`、`updated_at`、`word_target` 和 `word_count`；发布正文时只取 `## 正文`。`## 章末笔记` 是可选普通 Markdown，不要求 YAML。

全书规模只写在 `novel-studio/plan.yaml`：`scale.target_volumes`、`scale.target_main_chapters`、`scale.target_extras`、`scale.target_total_words`、`scale.chapter_word_target` 和 `scale.limits_are`。每卷用 `volumes[].planned_chapters` 和 `chapter_range` 记录计划章节数；番外用 `extras[]` 记录目的、预计字数和状态。

用户给出明确字数、字数区间或“不少于/不低于”要求时，必须用章节审计脚本或等价精确计数核验后再报告实际字数，不能虚报估算。

## 常用命令

日常写作直接编辑 YAML/Markdown。脚本只保留章节审计和开发烟测。

初始化后的项目优先使用本地工具检查章节有效字数：

```powershell
python .\novel-studio\tools\word_count.py .\content\volumes --json
```

开发插件自身时也可以直接运行内置审计脚本：

```powershell
python D:\projects\novel-studio\skills\ns-write\scripts\chapter_audit.py .\content\volumes\volume-001\ch001.md
```

结构体检、连续性检查和正文导出：

```powershell
python D:\projects\novel-studio\skills\ns-canon\scripts\schema_doctor.py .
python D:\projects\novel-studio\skills\ns-canon\scripts\continuity_check.py .
python D:\projects\novel-studio\skills\ns-write\scripts\export_text.py . -o export\novel.md
```

开发自检：

```powershell
python skills/ns/scripts/smoke_test_ns_scripts.py
```

## 仓库结构

```text
novel-studio/
  .claude-plugin/
  assets/
  skills/
    ns/
    ns-start/
    ns-ideate/
    ns-build/
    ns-guidance/
    ns-canon/
    ns-research/
    ns-write/
    ns-revise/
    ns-pitch/
    ns-visual/
```
