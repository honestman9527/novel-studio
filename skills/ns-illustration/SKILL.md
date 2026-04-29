---
name: ns-illustration
description: "小说插画提示词生成技能。用于为小说角色、场景、封面、章节插图、分镜、道具、地图和气氛图生成可复用中文或英文 AI 绘图提示词；当用户要求插画提示词、角色立绘、封面 prompt、场景图、分镜图、视觉设定、画风统一或从小说正文提取画面时使用。"
---

# NS Illustration

生成可复用插画提示词。提示词写 `visuals/`，图片写 `media/`，`art.yaml` 只存视觉一致性和文件索引。

## 读取

- `novel-studio/art.yaml`
- `novel-studio/memory.yaml`
- 当前章节 `## 正文`
- 需要模型格式时读取 [prompt-patterns.md](references/prompt-patterns.md)

## 输出

- 默认给中文和英文提示词。
- 指定 Midjourney、SDXL 或其他模型时按目标格式写。
- 复用角色/场景时列出稳定要素和可变要素。
- 长提示词、负面词、参数、迭代记录写 `visuals/*.md`。
- 视觉稳定要素、提示词文件、媒体文件路径摘要到 `novel-studio/art.yaml`。

默认只生成提示词；用户明确要求生成图片时再调用图像生成能力。
