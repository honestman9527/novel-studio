---
name: ns
description: "NS 小说创作插件总入口。用于路由和管理单本小说项目：当前文件夹就是这部小说根目录，唯一记忆目录固定为 novel-studio/，新项目正文默认放在 content/volumes/、content/extras/ 等通用发布/展示友好的目录中，旧项目可兼容 volumes/、extras/；当用户不知道该用哪个技能、请求含糊、混合多个写作动作，或要初始化/接入项目、拆分创作阶段、协调 YAML/Markdown 记忆、调研、架构、新开卷与番外起草、下一章续写、轻改、重写、简介、插画提示词流程时，优先使用本入口并根据需求判断应转入哪个 NS 子技能。"
---

# NS

作为小说创作套件的总入口，先判断阶段，再调用合适的子 skill。默认心智模型是：当前文件夹就是一部小说；`novel-studio/` 是唯一记忆目录；新项目正文写在 `content/volumes/`、`content/extras/` 等通用发布/展示友好的正文目录里；旧项目已有 `volumes/`、`extras/` 时兼容，不强制搬迁。

当用户不知道该用哪个技能、只说“帮我继续弄”“优化一下”“写点后续”“整理一下资料”这类含糊请求，或一次请求里同时包含记忆、调研、写作、改写、简介、插画提示词等动作时，先使用本 skill 分诊。分诊时不要停在建议层：直接判断主任务、必要时拆分顺序，并点名接下来应使用的子 skill。用户已经明确要写正文、查资料、搭设定或生成插画提示词时，可以直接使用对应子 skill。

## 子 Skill 路由

| 需求 | 使用 |
| --- | --- |
| 初始化空项目、接入已有正文、创建通用正文结构 | `$ns-init` |
| 写前发散、题材选择、卖点收束 | `$ns-brainstorm` |
| 建立或更新 YAML 长期记忆、本地项目结构 | `$ns-memory` |
| 搭主框架、世界观、人物、系统、无限流副本、大纲 | `$ns-architect` |
| 查找网络素材、考据、案例、资料来源 | `$ns-research` |
| 新开卷、新番外、独立短篇、序章、尾声、特殊篇初稿 | `$ns-draft` |
| 接上一章、写下一章、接着已有章节或片段继续写 | `$ns-continue` |
| 小改、轻改、润色、局部扩写/压缩 | `$ns-rewrite-light` |
| 大改、重写、重构章节或剧情 | `$ns-rewrite-heavy` |
| 简介、梗概、标签、宣传文案 | `$ns-blurb` |
| 生成角色、场景、封面、分镜插画提示词 | `$ns-illustration` |

## 模糊请求判断

- “不知道用什么”“帮我看看下一步”：先读 `novel-studio/` 的现有状态，再选择最缺的一环。
- “初始化项目”“接入旧小说”“整理正文结构”：用 `$ns-init`。
- “继续写”“接着写”“写下一章”：已有正文片段、上一章结尾或当前卷线性推进时用 `$ns-continue`。
- “新开卷”“写番外”“写序章/尾声”“开一个独立短篇”：不直接承接上一章结尾时用 `$ns-draft`。
- “改一下”“优化一下”：不改变事实、结构和人物选择时用 `$ns-rewrite-light`；会改变剧情、场景顺序、结局方向或设定时用 `$ns-rewrite-heavy`。
- “查点素材”“找参考”：需要来源、事实、最新信息或可追溯素材时用 `$ns-research`。
- “简介/卖点/标签/投稿梗概/封面文案”：用 `$ns-blurb`，对外内容输出到根目录 `brief.md`，内部梗概写入 `novel-studio/notes/synopsis.md`。
- “封面图/角色图/场景图/分镜提示词”：用 `$ns-illustration`，输出到根目录 `visuals/`。

## 默认工作流

1. 定位小说根目录：如果用户给了路径，使用该路径；否则使用当前工作目录。
2. 空项目或旧项目接入：用 `$ns-init` 创建 `content/`、`novel-studio/`、根目录 `brief.md`、`visuals/`、`media/`，并复制 `novel-studio/tools/word_count.py`。
3. 读取或创建 `novel-studio/`，优先直接编辑 YAML/Markdown，不把脚本当主流程。
4. 有想法但未成型：用 `$ns-brainstorm`，结果写入 `novel-studio/plan.yaml`、`novel-studio/memory.yaml` 或 `novel-studio/notes/*.md`。
5. 写正文前：用 `$ns-architect` 补齐 `project.yaml`、`plan.yaml`、`memory.yaml`、`continuity.yaml`、`style.yaml`、`publish.yaml`。
6. 需要事实、风俗、职业、地理、历史、科技或视觉参考：用 `$ns-research`，写入 `research.yaml` 和 `logs/research-log.md`。
7. 新开卷、番外、独立短篇、序章、尾声或特殊篇：用 `$ns-draft`，正文写到 `content/volumes/volume-001/ch001.md`、`content/volumes/volume-002/ch020.md` 或 `content/extras/extra-001.md`。
8. 写下一章、接上一章或续写已有文本：用 `$ns-continue`。
9. 修改旧文本：不改事实的小改用 `$ns-rewrite-light`；改剧情、结构、人物选择的大改用 `$ns-rewrite-heavy`。
10. 写完章节后：先补章节内 `章末回写`，再人工更新 `index.yaml`、`continuity.yaml`、`memory.yaml`、`finish.yaml`。
11. 需要视觉资产：用 `$ns-illustration`，生成内容放入根目录 `visuals/`，图片文件放 `media/`。
12. 需要简介/梗概/标签：用 `$ns-blurb`，对外内容写入根目录 `brief.md`，内部梗概写入 `novel-studio/notes/synopsis.md`。

## 项目结构

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
      characters.md
      world.md
      timeline.md
      glossary.md
      style.md
      synopsis.md
      open-threads.md
    logs/
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

## 章节硬约束

- 章节必须在 `content/volumes/` 或 `content/extras/` 里；旧项目可继续使用已存在的 `volumes/`、`extras/`，但不能散放根目录。
- 每章必须有 YAML frontmatter、`## 写作目标`、`## 正文`、`## 章末回写`。
- 只有 `## 正文` 是可发布文本；目标和回写是创作工作区段。
- `章末回写` 用 YAML 块记录摘要、人物变化、世界变化、时间线事件、伏笔、待收束线索和下一入口。

## 字数硬约束

- 用户给出明确字数、字数区间或“至少/不低于/不少于”要求时，字数是验收条件，不是参考建议。
- 不能凭感觉声称“约 X 字”“已达到 X 字”。只有经过机器统计或等价精确计数后，才能报告实际字数。
- 章节文件以 `novel-studio/tools/word_count.py <chapter-file>` 或 `$ns-draft` 的 `scripts/chapter_audit.py <chapter-file>` 输出的“有效字数”为准；未运行统计时必须说明“未核验”，不能虚报。
- 如果统计结果不足，继续补写到达标；若上下文或篇幅限制导致无法达标，明确说明差额和下一段应从哪里接。

## 长短篇选择

- 短篇：新项目使用 `content/volumes/volume-001/story.md`，记忆仍放 `novel-studio/`。
- 中篇/长篇/连载：新项目使用 `content/volumes/volume-*`，每卷维护阶段目标和章节计划。
- 番外/间章：新项目写入 `content/extras/`，并在 `index.yaml.extras` 登记。
- 系统文：在 `memory.yaml.genre.system` 维护系统规则、面板字段、成长曲线、任务/奖励和限制。
- 无限流：在 `memory.yaml.genre.infinite_flow` 维护空间规则、副本库、通关条件、道具、队友关系和现实线。

## 网络素材

当用户明确要求“查资料、找素材、参考真实案例、联网、最新、现实依据”时，使用浏览/搜索能力，并记录来源链接。不要搬运受版权保护的长文本；只提炼事实、结构灵感、风格观察和可改造素材。
