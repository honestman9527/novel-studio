---
name: ns-illustration
description: "小说插画提示词生成技能。用于为小说角色、场景、封面、章节插图、分镜、道具、地图和气氛图生成可复用的中文或英文 AI 绘图提示词；当用户要求插画提示词、角色立绘、封面 prompt、场景图、分镜图、视觉设定、画风统一或从小说正文提取画面时使用。"
---

# NS Illustration

从小说记忆或正文中提取视觉信息，生成稳定、可复用、可迭代的插画提示词。生成内容写入项目根目录的 `visuals/`；`novel-studio/art.yaml` 只记录视觉索引和稳定设定。

## 输入优先级

1. 读取 `novel-studio/art.yaml` 的统一画风。
2. 读取 `novel-studio/memory.yaml` 中的人物、地点、道具。
3. 读取当前章节 `## 正文`。
4. 没有视觉设定时，先生成 2-3 个风格方向供用户选择。

## 提示词结构

读取 [prompt-patterns.md](references/prompt-patterns.md) 后输出：

- 主体：人物/地点/事件。
- 关键特征：年龄、服饰、姿态、表情、道具、关系。
- 场景：时间、天气、光线、空间、氛围。
- 构图：镜头、景别、焦点、动势。
- 风格：画风、媒介、色彩、精细度。
- 负面提示：不需要的元素、错手、文字、水印、风格偏差。

## 目标格式

- 未指定：默认输出“通用中文提示词”和“通用英文提示词”各一版。
- 指定 Midjourney、SDXL/Stable Diffusion、自然语言图像模型或只要中文/英文时，按 `prompt-patterns.md` 的目标模型分支输出。
- 用户需要同一角色/场景多次复用时，额外输出“稳定要素”和“可变要素”，方便后续迭代。

## 落盘

```text
visuals/
  cover-prompts.md
  image-prompts.md
  character-prompts.md
  storyboard-prompts.md
  style-bible.yaml
```

视觉风格、角色稳定要素和常用场景可同步摘要到 `novel-studio/art.yaml`。长提示词、模型参数、负面词和迭代记录必须写入 `visuals/`。

默认直接人工编辑 YAML/Markdown，不使用脚本记录提示词。

默认只生成提示词；用户明确要求生成图片时，再调用图像生成能力。
