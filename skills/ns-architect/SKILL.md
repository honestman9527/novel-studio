---
name: ns-architect
description: "小说主框架与背景资料构建技能。用于撰写小说必备资源，包括题材承诺、世界观、人物档案、人物关系、势力组织、地点、时间线、系统规则、无限流副本、道具、能力体系、名词表、伏笔表、全书大纲、卷纲和章节纲；适配短篇、长篇、系统文、无限流、悬疑、言情、奇幻、科幻、历史等类型。"
---

# NS Architect

把想法整理成可长期写作的结构资料。资料写入 `novel-studio/*.yaml`，正文只放在 `volumes/`、`extras/`。不要为完整而堆设定，只写会影响冲突、选择、节奏和读者期待的设定。

## 必备资源

1. `novel-studio/project.yaml`：题材、篇幅、视角、读者承诺、风格禁区。
2. `novel-studio/plan.yaml`：卷计划、章节计划、番外计划、下一步。
3. `novel-studio/memory.yaml`：人物、世界规则、地点、势力、名词、道具、伏笔。
4. `novel-studio/continuity.yaml`：当前状态、事件台账、待收束线索。
5. `novel-studio/style.yaml`：文风、章节结构契约、必须保留和禁忌。

## 类型模块

读取 [genre-modules.md](references/genre-modules.md) 后按类型补齐 `novel-studio/memory.yaml.genre`：

- 系统文：`genre.system`
- 无限流：`genre.infinite_flow`
- 悬疑：`genre.mystery`
- 言情：`genre.romance`
- 奇幻/仙侠/玄幻：`genre.power_system`
- 科幻：`genre.scifi`
- 历史/现实：`genre.realism`
- 游戏/电竞：`genre.game`
- 末世：`genre.apocalypse`
- 都市/职场：`genre.urban`
- 公路/旅行：`genre.journey`
- 单元剧/群像：`genre.ensemble`

## 结构策略

- 短篇：只规划单一核心变化，人物和世界观从简。
- 中篇：规划 3-5 个关键转折，保证每段都有不可逆变化。
- 长篇/连载：先做卷计划和最近章节计划，不把全书逐章写死。
- 番外：在 `plan.yaml.extras` 里登记功能，避免番外破坏主线连续性。
- 系统文/无限流：每个阶段都要有规则升级和限制，避免只有数值膨胀。

## 输出

优先写入 YAML 记忆文件。回复用户时只概述关键设定、已更新文件和下一步写作入口。
