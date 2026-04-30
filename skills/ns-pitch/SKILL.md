---
name: ns-pitch
description: "小说文案与梗概技能。用于生成或改写书名卖点、读者简介、短简介、平台简介、标签、pitch、封面文案、章节摘要、投稿/完稿梗概和宣传文案；对外写 brief.md，内部梗概写 notes/synopsis*.md。当用户要求改简介、改梗概、改 synopsis notes 或准备投稿文案时使用。"
---

# NS Pitch

只写介绍、卖点和梗概，不改正文和设定事实。

## 读取

- `project.yaml`
- `plan.yaml`
- 根指导文件（存在时读取；不要自行创建或修改）
- `memory.yaml`
- `finish.yaml`
- `notes/synopsis.md`
- 已完成章节摘要或用户梗概

## 输出

- `brief.md`：读者简介、标签、卖点、Pitch、封面文案。
- `notes/synopsis*.md`：内部梗概；过长时按用途拆分。
- `finish.yaml`：只记路径、状态、更新时间，不复制正文。

## 规则

- 读者简介抓欲望、代价、反差和主冲突；投稿/完稿梗概可以剧透。
- 不堆设定名词，不夸不存在的内容。
- 有字数/字符数要求时精确计数。
- 新全局指导交给 `$ns-guidance`。
