---
name: ns-blurb
description: "小说简介、卖点文案和梗概生成技能。用于生成或改写书名卖点、读者向简介、短简介、平台简介、标签、章节摘要、投稿梗概、完稿梗概和宣传文案；当用户要求写简介、文案、梗概、标签、卖点、作品介绍、封面文案或完稿资料时使用。对外简介、标签、pitch、封面文案写入根目录 brief.md；内部长梗概、投稿梗概、完稿梗概写入 novel-studio/notes/synopsis.md。"
---

# NS Blurb

写简介和宣传/交付文案。

## 读取

- `novel-studio/project.yaml`
- `novel-studio/plan.yaml`
- `novel-studio/memory.yaml`
- `novel-studio/finish.yaml`
- `novel-studio/notes/synopsis.md`
- 已完成章节摘要或用户梗概

## 输出

- `brief.md`：读者简介、标签、卖点、Pitch、封面文案。
- `novel-studio/notes/synopsis.md`：内部短梗概、长梗概、投稿梗概、完稿梗概。
- `finish.yaml`：只记路径、状态、更新时间，不复制正文。

## 规则

- 读者简介抓欲望、代价、反差、主冲突，不剧透终局。
- 投稿/完稿梗概可以剧透。
- 不堆设定名词。
- 有字数/字符数要求时必须精确计数；不能用估算冒充。
