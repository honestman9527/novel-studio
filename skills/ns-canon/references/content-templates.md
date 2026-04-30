# Content Templates

需要创建新项目、卷或章节时读取本文件；只维护模板，不解释职责。

## NOVEL.md

只在用户同意创建或修改 `NOVEL.md` 时使用。

````markdown
# NOVEL

## 必须遵守

## 不要写/不要改

## 风格偏好

## 内容边界

## 结构偏好

## 待确认
````

## Volume Index

````markdown
---
id: volume-001
type: volume
volume_number: 1
title: "第一卷"
status: planning
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
---

# 第一卷

## 卷简介

## 卷承诺

## 本卷主要人物

## 章节目录

| 章节 | 标题 | 状态 | 功能 | 字数 |
| --- | --- | --- | --- | --- |

## 卷末笔记
````

## Chapter

````markdown
---
id: ch001
type: main
chapter_number: 1
title: "章节标题"
volume_id: volume-001
status: draft
created_at: "2026-04-29T00:00:00+08:00"
updated_at: "2026-04-29T00:00:00+08:00"
word_target: "3000-5000"
word_count:
  effective:
  counted_at:
---

# 第001章 章节标题

## 写作目标

- 本章功能：
- 必须推进：
- 避免：

## 正文

## 章末笔记

- 本章概要：
- 记忆更新：
- 未收束：
- 已解决：
- 下一章钩子：
- 修订备注：
````

## Note

按主题创建，例如 `notes/people.md`、`notes/world.md`、`notes/timeline.md`、`notes/synopsis.md`。不要把多个主题堆进一个过长文件。

````markdown
# 主题名称

## 摘要

## 细节

## 待确认
````
