# Prompt Patterns

## 通用模板

```text
{主体}，{关键外观}，{动作/情绪}，位于{场景}，{光线与氛围}，{构图与镜头}，{画风与媒介}，{质量词}

Negative prompt: {不要的元素}
```

## 目标模型分支

### 通用中文

适合用户直接复制到中文图像工具。使用自然中文短段落，保留完整主体、场景、构图和风格：

```text
正向提示词：{主体与关键特征}，{动作/情绪}，{场景与光线}，{构图与镜头}，{画风与媒介}，{质量与细节要求}
负面提示词：{不要的元素}
```

### 通用英文

适合英文提示词工具。用逗号分隔短语，顺序从主体到画面控制：

```text
Prompt: {subject}, {key features}, {action and mood}, {setting and lighting}, {composition and camera}, {art style and medium}, {quality details}
Negative prompt: {unwanted elements}
```

### Midjourney

把画面描述放在前面，参数放在末尾；不要写 `Negative prompt:` 标签，用 `--no` 表达排除项。只有用户要求时才加入具体比例或风格化参数。

```text
{subject}, {key features}, {action and mood}, {setting and lighting}, {composition}, {style} --no {unwanted elements}
```

### SDXL / Stable Diffusion

分成 positive 和 negative 两段。保留清晰 tag，但不要堆无关质量词；角色一致性信息放在 positive 前半段。

```text
Positive: {subject}, {key features}, {action and mood}, {setting and lighting}, {composition}, {style}, detailed
Negative: low quality, blurry, watermark, text, logo, extra fingers, deformed hands, bad anatomy, duplicate face, inconsistent costume
```

### 自然语言图像模型

使用完整指令句，减少 tag 堆叠，不使用权重、LoRA、采样器、步数等特定参数。重点讲清画面主体、构图、风格和必须避免的内容。

```text
请生成一张{画幅/用途}插画：画面中{主体与动作}，位于{场景}，整体呈现{情绪与风格}。构图应{镜头与焦点}，避免{不要的元素}。
```

## 角色立绘

强调稳定识别：

- 年龄段、体型、发型、眼神。
- 服饰轮廓、材质、主色和标志物。
- 常用道具、姿态、表情。
- 背景简洁，避免抢主体。

角色多次复用时拆成：

- 稳定要素：年龄段、发型、眼神、体型、服饰轮廓、标志物、主色。
- 可变要素：姿态、表情、光线、背景、镜头、章节情绪。

## 封面

强调类型卖点：

- 主角剪影或脸部焦点。
- 核心冲突的象征物。
- 标题留白位置。
- 高对比色块或明确光源。

## 章节插图

强调具体瞬间：

- 本章最不可逆的动作。
- 人物关系位置。
- 场景压力。
- 钩子物件或视觉线索。

## 分镜

每个镜头只写一个动作或信息点：

1. 远景建立场景。
2. 中景呈现冲突。
3. 近景呈现表情或道具。
4. 特写呈现线索。
5. 反打或背影制造悬念。

## 负面提示词

常用项：low quality, blurry, watermark, text, logo, extra fingers, deformed hands, bad anatomy, duplicate face, cropped head, inconsistent costume。
