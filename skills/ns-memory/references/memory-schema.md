# Memory Schema

本地工作区就是小说长期记忆仓库。一个工作区可以管理多本小说，每本小说一个文件夹。长篇、短篇、连载都使用同一套单本小说结构，只是文件数量不同。

## 工作区结构

```text
{workspace}/
  00-workspace/
    index.md
    shared-source-log.md
  novels/
    {novel-slug}/
      00-meta/
      01-brainstorm/
      02-bible/
      03-outline/
      04-drafts/
      05-revisions/
      06-art/
      07-finish/
```

- `00-workspace/index.md`：多本小说索引、最近活动和状态。
- `00-workspace/shared-source-log.md`：多个小说都可能复用的公共素材来源。
- `novels/{novel-slug}/`：单本小说所有长期记忆。

## 单本小说完整结构

```text
{workspace}/novels/{novel-slug}/
  00-meta/
    project.md
    writing-contract.md
    progress.md
    source-log.md
  01-brainstorm/
    premise-lab.md
    options.md
    open-questions.md
  02-bible/
    genre-contract.md
    world.md
    characters.md
    relationships.md
    factions.md
    locations.md
    timeline.md
    glossary.md
    artifacts.md
    foreshadowing.md
    system.md
    infinite-flow.md
    instances.md
    mystery.md
    romance.md
    power-system.md
    scifi.md
    realism.md
    game.md
    apocalypse.md
    urban.md
    journey.md
    ensemble.md
  03-outline/
    structure.md
    volume-outline.md
    chapter-outline.md
  04-drafts/
    short/
    volumes/
      volume-001/
        chapters/
  05-revisions/
    revision-log.md
  06-art/
    visual-bible.md
    prompts.md
  07-finish/
    blurb.md
    synopsis-short.md
    synopsis-long.md
    chapter-summary.md
    cast-list.md
    sequel-hooks.md
```

## 单本短篇最小结构

短篇可以只保留：

- `00-meta/project.md`
- `02-bible/characters.md`
- `03-outline/structure.md`
- `04-drafts/short/story.md`
- `07-finish/blurb.md`

## 核心文件职责

- `project.md`：书名、题材、篇幅、视角、受众、核心卖点。
- `writing-contract.md`：风格、禁忌、必须保留设定、更新规则。
- `progress.md`：当前章节、已完成阶段、下一步。
- `source-log.md`：网络素材和参考来源。
- `genre-contract.md`：类型承诺和读者期待。
- `characters.md`：人物目标、恐惧、秘密、弧光和当前状态。
- `foreshadowing.md`：伏笔的埋设、推进、兑现和废弃处理。
- `system.md`：系统文规则、面板、任务、奖励、限制和成长曲线。
- `infinite-flow.md`：无限流空间规则、通关条件、惩罚和现实线。
- `instances.md`：副本库、主题、规则、关键 NPC、奖励和伏笔。
- `mystery.md`：谜面、证据链、误导链和公平线索。
- `romance.md`：关系推进、信任变化和情感选择代价。
- `power-system.md`：奇幻、仙侠、玄幻的力量体系和代价。
- `scifi.md`：科技规则、社会后果和失控风险。
- `realism.md`：历史/现实题材的考据边界和待查事实。
- `game.md`：游戏或电竞规则、版本环境和比赛制度。
- `apocalypse.md`：末世资源、秩序和生存风险。
- `urban.md`：都市/职场行业规则、利益结构和现实压力。
- `journey.md`：旅行路线、站点主题和关系变化。
- `ensemble.md`：单元剧/群像的常驻人物、单元模板和长线变化。

## 回写时机

- 写完一章：更新 `progress.md`、`chapter-summary.md`、`timeline.md`、`characters.md`、`foreshadowing.md`。
- 新查资料：更新 `source-log.md` 和相关 bible 文件。
- 新增角色：更新 `characters.md`、`relationships.md`。
- 新副本/任务：更新 `instances.md` 或 `system.md`。
- 完稿：更新 `07-finish/` 全部文件。
