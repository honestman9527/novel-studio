# Memory Schema

当前文件夹就是小说根目录。NS 把内容分成三层：根指导、项目记忆、创作产物。具体文件职责见 [file-roles.md](file-roles.md)，创建模板见 [content-templates.md](../assets/templates/content-templates.md)。

## 目录

```text
AGENTS.md / CLAUDE.md  # 根指导文件
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
  logs/
  tools/word_count.py
content/
  volumes/volume-001/_index.md
  volumes/volume-001/ch001.md
  extras/
brief.md
visuals/
media/
```

## 三层关系

| 层 | 位置 | 作用 | 不放什么 |
| --- | --- | --- | --- |
| 根指导 | `AGENTS.md` / `CLAUDE.md` | 作者长期偏好、硬禁区、写法原则、待确认原则 | 人物档案、剧情大纲、资料摘录、章节进度 |
| 项目记忆 | `novel-studio/*.yaml`、`notes/*.md`、`logs/*.md` | 已定事实、计划、连续性、索引、来源、长说明和过程记录 | 可发布正文、对外宣传成稿、完整视觉提示词 |
| 创作产物 | `content/`、`brief.md`、`visuals/`、`media/` | 正文、番外、对外文案、视觉提示词和素材 | 结构化记忆的唯一来源 |

## 主要产物位置

| 产物 | 位置 | 记忆中的对应项 |
| --- | --- | --- |
| 主线章节 | `content/volumes/<volume>/ch*.md` | `index.yaml` 登记路径和字数；`continuity.yaml` / `memory.yaml` 记录影响 |
| 番外/序章/尾声/短篇 | `content/extras/*.md` | `plan.yaml.extras[]` 记计划；`index.yaml` 记条目 |
| 卷简介和章节目录 | `content/volumes/<volume>/_index.md` | `plan.yaml.volumes[]` 记计划；`index.yaml` 记章节事实 |
| 长人物/世界/时间线/梗概 | `novel-studio/notes/*.md` | YAML 只留摘要和 notes 路径 |
| 对外简介和 pitch | `brief.md` | `finish.yaml` 只记状态和路径；内部长梗概进 notes |
| 调研结论和来源 | `research.yaml`、`novel-studio/logs/*.md` | YAML 存结论和来源边界；logs 存过程 |
| 视觉提示词 | `visuals/*.md` | `art.yaml` 存稳定要素、媒体路径和索引 |
| 图片素材 | `media/` | `art.yaml` 存文件路径和用途 |
| 导出稿 | `export/*.md` 或用户指定路径 | `finish.yaml` 存交付物索引 |

## 唯一来源

- 根指导文件是行为原则来源；项目记忆是故事事实来源；创作产物是正文和展示稿来源。
- 同一事实只完整写在一个地方，其它文件只保留摘要、状态或路径。
- 根指导文件不复制设定、计划、进度和资料；这些内容写入 `novel-studio/`。
- YAML 不复制 notes 全文；只保留短摘要和指向 notes 的路径。
- `plan.yaml` 管计划，卷 `_index.md` 管人读简介和目录。
- `publish.yaml.site.content_root` 是正文根目录唯一来源；`index.yaml` 不重复保存发布根。
- `art.yaml` 管视觉索引，`visuals/*.md` 管完整提示词。
- `brief.md` 管对外文案，内部长梗概写 `notes/synopsis*.md`。

## 同步顺序

- 新建或移动章节：章节 Markdown + frontmatter -> `index.yaml` -> 卷 `_index.md`。
- 修改正文或章末笔记：审计字数和更新时间 -> `index.yaml` -> `continuity.yaml` / `memory.yaml`。
- 修改卷计划或全书规模：`plan.yaml` -> 必要的卷 `_index.md` 说明。
- 修改 notes 长文：只把摘要和路径同步回 YAML。
- 修改根指导：走 `$ns-guidance`，不要顺手改故事记忆。

## 文件体量

- YAML、frontmatter 和根指导文件只写短事实、短原则、状态和路径。
- 单个 notes 文件只处理一个主题；过长或混入多个主题时拆分。
- logs 按日期或任务拆分；不要代替 YAML 记录最终事实。
- 正文章节可以按创作目标变长；不要为了体量把正文拆到 notes。
