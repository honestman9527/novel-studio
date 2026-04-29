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
    publish.yaml
    notes/
    tools/
      word_count.py
    logs/
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

当前文件夹就是这部小说的根目录；`novel-studio/` 是唯一记忆目录；新项目正文默认放在 `content/volumes/`、`content/extras/` 等通用发布/展示友好的目录中。旧项目已有 `volumes/`、`extras/` 时可以兼容维护，不强制搬迁。

不知道该用哪个技能时，直接使用 `ns`。入口会根据请求判断应转入启动、创意、框架、canon 记忆、调研、写作、修订、文案或视觉提示词技能。

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

## 通过 npx skills 安装（跨平台通用）

[`npx skills`](https://github.com/vercel-labs/skills) 是开放技能生态的 CLI 工具，一条命令即可将本仓库的技能安装到 **Claude Code、Codex、Cursor、Gemini CLI、OpenCode** 等任意支持 Agent Skills 的编码助手中。

```bash
npx skills add honestman9527/novel-studio
```

交互式提示会让你：

1. 选择要安装的技能（可全选）
2. 选择目标 Agent（Claude Code / Codex / Cursor / Gemini CLI …）
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

---

## Codex CLI 安装

### 方式一：通过 Marketplace 安装（推荐）

```bash
codex plugin marketplace add honestman9527/novel-studio
codex /plugins            # 在插件目录中选择 ns 并安装
```

### 方式二：手动安装

1. 克隆仓库到本地：

   ```bash
   git clone https://github.com/honestman9527/novel-studio.git
   ```

2. 将插件放入 Codex 插件缓存目录：

   ```bash
   # Linux / macOS
   mkdir -p "$CODEX_HOME/plugins/cache/local/ns/1.1.0"
   cp -r novel-studio/* "$CODEX_HOME/plugins/cache/local/ns/1.1.0/"

   # Windows (PowerShell)
   $dest = "$env:USERPROFILE\.codex\plugins\cache\local\ns\1.1.0"
   New-Item -ItemType Directory -Force -Path $dest
   Copy-Item -Recurse novel-studio\* $dest
   ```

3. 在 `~/.codex/config.toml`（Windows 为 `%USERPROFILE%\.codex\config.toml`）中启用插件：

   ```toml
   [features]
   plugins = true

   [plugins."ns@local"]
   enabled = true
   ```

4. 重启 Codex CLI，运行 `codex /plugins` 确认 `ns` 已出现。

### 方式三：本地开发加载

如果你正在开发或调试插件，可以直接用 `--plugin-dir` 加载本地目录：

```bash
codex --plugin-dir /path/to/novel-studio
```

### 安装后可用的技能入口

```text
/ns:ns
/ns:ns-start
/ns:ns-ideate
/ns:ns-build
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
- `ns-build`：搭建故事圣经，只负责世界观、人物、类型规则、大纲、卷纲和章节计划。
- `ns-canon`：维护 `novel-studio/` canon 记忆，只处理已定事实、连续性、索引和进度。
- `ns-research`：联网查找素材、考据、视觉参考并记录来源；创作素材优先从小说素材站、写作站、网文资料和类型小说相关网站提炼，事实考据再用官方/学术/专业来源核验。
- `ns-write`：写新的正文内容，统一负责下一章、续写、新开卷、番外、序章、尾声和独立短篇。
- `ns-revise`：修订已有正文，统一负责润色、小改、扩写、压缩、重写和结构改。
- `ns-pitch`：生成简介、标签、pitch 和宣传文案到根目录 `brief.md`，内部梗概写入 `novel-studio/notes/synopsis.md`。
- `ns-visual`：生成封面、角色、场景、道具和分镜插画提示词，输出到 `visuals/`。

## 卷和章节结构

章节必须放在卷或番外目录中，新项目路径例如 `content/volumes/volume-001/ch001.md`、`content/extras/extra-001.md`。每卷用 `_index.md` 维护卷简介、卷承诺、主要人物和章节目录；`## 卷末笔记` 可选。

每章必须包含 YAML frontmatter、H1、`## 写作目标`、`## 正文`。frontmatter 记录 `chapter_number`、`title`、`display_title`、`volume_id`、`volume_title`、`created_at`、`updated_at`、`status` 和字数信息；发布正文时只取 `## 正文`。`## 章末笔记` 是可选普通 Markdown，不要求 YAML。

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
  .codex-plugin/
  assets/
  skills/
    ns/
    ns-start/
    ns-ideate/
    ns-build/
    ns-canon/
    ns-research/
    ns-write/
    ns-revise/
    ns-pitch/
    ns-visual/
```
