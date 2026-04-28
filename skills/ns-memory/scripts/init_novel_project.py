#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Initialize a local NS workspace or a single novel memory folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BASE_FILES: dict[str, str] = {
    "00-meta/project.md": "# 项目概览\n\n- 书名：\n- 类型：\n- 篇幅模式：\n- 视角：\n- 目标读者：\n- 核心卖点：\n- 主角：\n- 核心冲突：\n- 当前阶段：\n",
    "00-meta/writing-contract.md": "# 创作契约\n\n## 风格\n\n\n## 禁忌\n\n\n## 必须保留\n\n\n## 更新规则\n\n- 新事实写入长期记忆。\n- 不确定内容写入 open-questions。\n",
    "00-meta/progress.md": "# 进度\n\n- 当前章节：\n- 已完成：\n- 下一步：\n- 待回写：\n",
    "00-meta/source-log.md": "# 素材来源\n\n| 日期 | 主题 | 来源 | 链接 | 可用素材 | 写作位置 |\n| --- | --- | --- | --- | --- | --- |\n",
    "01-brainstorm/premise-lab.md": "# 脑洞实验室\n\n## 原始想法\n\n\n## 可选方向\n\n\n## 已选择方向\n\n",
    "01-brainstorm/options.md": "# 备选方案\n\n| 方案 | 卖点 | 风险 | 状态 |\n| --- | --- | --- | --- |\n",
    "01-brainstorm/open-questions.md": "# 待确认问题\n\n- \n",
    "02-bible/genre-contract.md": "# 类型契约\n\n- 类型：\n- 读者期待：\n- 爽点/情绪承诺：\n- 不写什么：\n",
    "02-bible/world.md": "# 世界观\n\n## 核心规则\n\n\n## 限制与代价\n\n\n## 重要地点\n\n| 地点 | 功能 | 危险/规则 | 首次出现 |\n| --- | --- | --- | --- |\n",
    "02-bible/characters.md": "# 人物档案\n\n| 姓名 | 身份 | 目标 | 恐惧 | 秘密 | 当前状态 | 弧光 |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    "02-bible/relationships.md": "# 人物关系\n\n| A | B | 关系 | 张力 | 变化 |\n| --- | --- | --- | --- | --- |\n",
    "02-bible/factions.md": "# 势力组织\n\n| 名称 | 目标 | 资源 | 对主角态度 |\n| --- | --- | --- | --- |\n",
    "02-bible/locations.md": "# 地点\n\n| 地点 | 氛围 | 功能 | 关联事件 |\n| --- | --- | --- | --- |\n",
    "02-bible/timeline.md": "# 时间线\n\n| 顺序 | 时间 | 章节 | 事件 | 影响 |\n| --- | --- | --- | --- | --- |\n",
    "02-bible/glossary.md": "# 名词表\n\n| 名词 | 类型 | 标准写法 | 含义 | 首次出现 |\n| --- | --- | --- | --- | --- |\n",
    "02-bible/artifacts.md": "# 道具与能力\n\n| 名称 | 类型 | 功能 | 限制 | 持有人 |\n| --- | --- | --- | --- | --- |\n",
    "02-bible/foreshadowing.md": "# 伏笔追踪\n\n| 伏笔 | 埋设位置 | 表面含义 | 真实含义 | 兑现计划 | 状态 |\n| --- | --- | --- | --- | --- | --- |\n",
    "03-outline/structure.md": "# 故事结构\n\n## 一句话故事\n\n\n## 阶段结构\n\n| 阶段 | 目标 | 转折 | 代价 |\n| --- | --- | --- | --- |\n",
    "03-outline/volume-outline.md": "# 卷纲\n\n| 卷 | 主题 | 起点 | 终点 | 核心反转 |\n| --- | --- | --- | --- | --- |\n",
    "03-outline/chapter-outline.md": "# 章节纲\n\n| 章节 | 标题 | 功能 | 冲突 | 钩子 | 状态 |\n| --- | --- | --- | --- | --- | --- |\n",
    "05-revisions/revision-log.md": "# 修改记录\n\n| 日期 | 范围 | 原因 | 影响 |\n| --- | --- | --- | --- |\n",
    "06-art/visual-bible.md": "# 视觉圣经\n\n- 总体画风：\n- 色彩：\n- 角色一致性：\n- 场景关键词：\n",
    "06-art/prompts.md": "# 插画提示词\n\n",
    "07-finish/blurb.md": "# 小说简介\n\n",
    "07-finish/synopsis-short.md": "# 短梗概\n\n",
    "07-finish/synopsis-long.md": "# 长梗概\n\n",
    "07-finish/chapter-summary.md": "# 章节摘要\n\n| 章节 | 摘要 | 关键变化 |\n| --- | --- | --- |\n",
    "07-finish/cast-list.md": "# 人物表\n\n",
    "07-finish/sequel-hooks.md": "# 番外与续作方向\n\n",
}

MINIMAL_SHORT_FILES = [
    "00-meta/project.md",
    "02-bible/characters.md",
    "03-outline/structure.md",
    "07-finish/blurb.md",
]

WORKSPACE_FILES: dict[str, str] = {
    "00-workspace/index.md": "# NS 工作区索引\n\n| 小说 | 标题 | 模式 | 类型 | 状态 | 最近更新 | 路径 |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    "00-workspace/shared-source-log.md": "# 共享素材来源\n\n| 日期 | 主题 | 来源 | 链接 | 可复用方向 |\n| --- | --- | --- | --- | --- |\n",
}

GENRE_FILES: dict[str, dict[str, str]] = {
    "system": {
        "02-bible/system.md": "# 系统设定\n\n- 系统来源：\n- 绑定条件：\n- 面板字段：\n- 任务类型：\n- 奖励类型：\n- 惩罚/限制：\n- 升级曲线：\n- 系统不可做的事：\n"
    },
    "infinite-flow": {
        "02-bible/infinite-flow.md": "# 无限流规则\n\n- 空间/主神规则：\n- 进入条件：\n- 队伍机制：\n- 通关条件：\n- 死亡/失败后果：\n- 现实线影响：\n",
        "02-bible/instances.md": "# 副本库\n\n| 副本 | 类型 | 规则 | 关键 NPC | 通关条件 | 奖励 | 伏笔 |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    },
    "mystery": {
        "02-bible/mystery.md": "# 悬疑设定\n\n- 核心谜面：\n- 真相：\n- 证据链：\n- 误导链：\n- 嫌疑人动机：\n- 公平线索：\n"
    },
    "romance": {
        "02-bible/romance.md": "# 情感线设定\n\n- 关系类型：\n- 初始距离：\n- 吸引力来源：\n- 亲密推进节点：\n- 外部阻力：\n- 信任破裂点：\n- 结局承诺：\n"
    },
    "fantasy": {
        "02-bible/power-system.md": "# 力量体系\n\n- 力量来源：\n- 等级/境界：\n- 修炼方式：\n- 资源：\n- 代价：\n- 禁忌：\n- 战斗限制：\n"
    },
    "xianxia": {
        "02-bible/power-system.md": "# 力量体系\n\n- 力量来源：\n- 等级/境界：\n- 修炼方式：\n- 资源：\n- 代价：\n- 禁忌：\n- 门派/势力：\n- 地图层级：\n"
    },
    "scifi": {
        "02-bible/scifi.md": "# 科幻设定\n\n- 核心技术：\n- 技术限制：\n- 社会后果：\n- 伦理冲突：\n- 阵营分歧：\n- 关键设施/设备：\n- 失控风险：\n"
    },
    "realism": {
        "02-bible/realism.md": "# 现实/历史考据\n\n- 时代背景：\n- 地点与路线：\n- 职业细节：\n- 社会规则：\n- 语言边界：\n- 关键事实：\n- 待查问题：\n"
    },
    "game": {
        "02-bible/game.md": "# 游戏/电竞设定\n\n- 游戏类型：\n- 核心规则：\n- 职业/角色/卡组：\n- 版本环境：\n- 比赛制度：\n- 对手风格：\n- 成长目标：\n"
    },
    "apocalypse": {
        "02-bible/apocalypse.md": "# 末世/灾变设定\n\n- 灾变来源：\n- 生存资源：\n- 安全区规则：\n- 威胁类型：\n- 组织秩序：\n- 道德困境：\n- 迁徙路线：\n"
    },
    "urban": {
        "02-bible/urban.md": "# 都市/职场设定\n\n- 行业：\n- 职位/阶层：\n- 利益结构：\n- 人脉关系：\n- 城市地点：\n- 金钱压力：\n- 职业风险：\n"
    },
    "journey": {
        "02-bible/journey.md": "# 公路/旅行设定\n\n- 路线：\n- 每站主题：\n- 交通方式：\n- 旅伴关系：\n- 地方风俗：\n- 消耗与风险：\n"
    },
    "ensemble": {
        "02-bible/ensemble.md": "# 单元剧/群像设定\n\n- 核心场域：\n- 常驻人物：\n- 单元主题：\n- 单元事件模板：\n- 长线主线：\n- 群像关系变化：\n"
    },
}


def write_file(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "untitled"


def append_workspace_index(workspace: Path, novel_slug: str, title: str, mode: str, genres: list[str]) -> None:
    index = workspace / "00-workspace/index.md"
    existing = index.read_text(encoding="utf-8") if index.exists() else WORKSPACE_FILES["00-workspace/index.md"]
    row_prefix = f"| {novel_slug} |"
    if row_prefix in existing:
        return
    genre_text = ", ".join(genres) if genres else "通用"
    row = f"| {novel_slug} | {title or novel_slug} | {mode} | {genre_text} | 初始化 |  | novels/{novel_slug} |\n"
    with index.open("a", encoding="utf-8") as handle:
        handle.write(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 NS 小说工作区或单本小说长期记忆文件夹。")
    parser.add_argument("workspace_dir")
    parser.add_argument("--novel", help="小说文件夹 slug；不提供时使用 --title 自动生成，或在 --single-novel 模式下直接使用目标目录")
    parser.add_argument("--title", default="", help="小说标题")
    parser.add_argument("--mode", choices=["short", "novella", "long", "serial"], default="long")
    parser.add_argument("--genre", action="append", default=[])
    parser.add_argument("--single-novel", action="store_true", help="把 workspace_dir 当作单本小说根目录，不创建 novels/<slug>")
    parser.add_argument("--minimal-short", action="store_true", help="仅在 --mode short 时创建短篇最小结构")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.minimal_short and args.mode != "short":
        parser.error("--minimal-short 只能和 --mode short 一起使用")

    workspace = Path(args.workspace_dir).resolve()
    novel_slug = slugify(args.novel or args.title)
    if args.single_novel:
        root = workspace
    else:
        for relative, content in WORKSPACE_FILES.items():
            write_file(workspace / relative, content, args.overwrite)
        root = workspace / "novels" / novel_slug

    if args.minimal_short:
        files = {relative: BASE_FILES[relative] for relative in MINIMAL_SHORT_FILES}
    else:
        files = dict(BASE_FILES)
    for genre in args.genre:
        files.update(GENRE_FILES.get(genre, {}))

    if args.mode == "short":
        files["04-drafts/short/story.md"] = "# 正文\n\n"
    else:
        files["04-drafts/volumes/volume-001/chapters/ch001.md"] = "# 第001章\n\n## 写作目标\n\n\n## 正文\n\n"

    for relative, content in files.items():
        write_file(root / relative, content, args.overwrite)

    if not args.single_novel:
        append_workspace_index(workspace, novel_slug, args.title, args.mode, args.genre)

    print(f"已初始化小说记忆: {root}")
    if not args.single_novel:
        print(f"工作区: {workspace}")
        print(f"小说 slug: {novel_slug}")
    print(f"篇幅模式: {args.mode}")
    print(f"类型模块: {', '.join(args.genre) if args.genre else '通用'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
