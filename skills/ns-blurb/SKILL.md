---
name: ns-blurb
description: "小说简介、卖点文案和梗概生成技能。用于生成或改写书名卖点、读者向简介、短简介、平台简介、标签、章节摘要、投稿梗概、完稿梗概和宣传文案；当用户要求写简介、文案、梗概、标签、卖点、作品介绍、封面文案或完稿资料时使用。对外简介、标签、pitch 和封面文案写入项目根目录 brief.md；内部长梗概、投稿梗概和完稿梗概写入 novel-studio/notes/synopsis.md。"
---

# NS Blurb

负责简介和宣传/交付文案。对外展示内容集中放在项目根目录 `brief.md`；内部长梗概和交付资料放在 `novel-studio/notes/synopsis.md`；`novel-studio/finish.yaml` 只记录索引或摘要。

## 输入

1. `novel-studio/project.yaml`
2. `novel-studio/plan.yaml`
3. `novel-studio/memory.yaml`
4. `novel-studio/finish.yaml`
5. `novel-studio/notes/synopsis.md`
6. 已完成章节摘要或用户提供的剧情梗概

## 输出位置

```text
brief.md
novel-studio/
  notes/
    synopsis.md
```

`brief.md` 建议结构：

```markdown
# 作品简介

## 读者简介

## 标签

## 卖点

## Pitch

## 封面文案
```

## 文案类型

- 读者向简介：抓卖点、情绪承诺和主冲突，不剧透核心反转。
- 短梗概：300-800 字，适合投稿或内部复盘；内部版本写入 `novel-studio/notes/synopsis.md`。
- 长梗概：完整剧情链，包含结局，写入 `novel-studio/notes/synopsis.md`。
- 平台标签：题材、情绪、主角关系、核心爽点。
- 封面文案：一句话钩子、短句卖点、封底介绍。

## 约束

- 简介不堆设定名词，优先主角欲望、代价、反差和读者期待。
- 投稿梗概可以剧透；读者简介不要剧透终局。
- 输出后在 `novel-studio/finish.yaml` 记录 `brief.md` 和 `novel-studio/notes/synopsis.md` 的路径。
- 用户要求简介、梗概、pitch 或标签在指定字数/字符数内时，必须精确计数后再报告；不能用“约 X 字”冒充结果。
- 中文简介按实际中日韩文字和英文/数字连续串计数；如平台要求“字符数”而不是“字数”，按平台口径记录在文件中。
- 若计数超出限制，继续压缩；若低于“至少/不少于”要求，继续补足。
