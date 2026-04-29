#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Smoke-test NS helper scripts and shared metrics."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from ns_text_metrics import effective_word_metrics, placeholder_markers


REPO_ROOT = Path(__file__).resolve().parents[3]
INIT_SCRIPT = REPO_ROOT / "skills/ns-memory/scripts/init_novel_project.py"
BACKWRITE_SCRIPT = REPO_ROOT / "skills/ns-memory/scripts/apply_chapter_backwrite.py"
AUDIT_SCRIPT = REPO_ROOT / "skills/ns-draft/scripts/chapter_audit.py"
SOURCE_LOG_SCRIPT = REPO_ROOT / "skills/ns-research/scripts/append_source_log.py"
ART_PROMPT_SCRIPT = REPO_ROOT / "skills/ns-illustration/scripts/append_art_prompt.py"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-X", "utf8", *args],
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )


def assert_shared_metrics() -> None:
    sample = """---
title: 测试章
---
# 第一章 测试
这是AI-17计划。她说：“三天后再见。”
| 备注 | 不应计入 |
| --- | --- |
- [ ] 待办项不应计入
（略）
"""
    metrics = effective_word_metrics(sample)
    assert metrics["effective"] == 13, metrics
    assert metrics["cjk"] == 11, metrics
    assert metrics["latin_or_number"] == 2, metrics
    assert placeholder_markers(sample) == ["略"]


def assert_scripts() -> None:
    with tempfile.TemporaryDirectory(prefix="ns-smoke-") as tmp:
        root = Path(tmp)
        project = root / "test-book"
        chapter = project / "volumes/volume-001/ch001.md"

        run_script(str(INIT_SCRIPT), str(project), "--title", "测试书", "--mode", "long")
        chapter.write_text("# 第一章 测试\n\n## 写作目标\n\n- 本章功能：测试\n\n## 正文\n\n这是AI-17计划。她说：“三天后再见。”\n\n## 章末回写\n\n```yaml\nsummary: 测试\n```\n", encoding="utf-8")
        memory = project / "novel-studio"

        for _ in range(2):
            run_script(
                str(BACKWRITE_SCRIPT),
                str(project),
                str(chapter),
                "--chapter-id",
                "ch001",
                "--title",
                "测试章",
            )

        project_yaml = (memory / "project.yaml").read_text(encoding="utf-8")
        index_yaml = (memory / "index.yaml").read_text(encoding="utf-8")
        backwrite = (memory / "logs/auto-backwrite.md").read_text(encoding="utf-8")

        assert 'title: "测试书"' in project_yaml, project_yaml
        assert 'path: "volumes/volume-001/ch001.md"' in index_yaml, index_yaml
        assert backwrite.count("ch001 测试章") == 2, backwrite
        assert "write_back_targets" in backwrite, backwrite

        audit = run_script(str(AUDIT_SCRIPT), str(chapter), "--min", "10", "--max", "20", "--json")
        audit_data = json.loads(audit.stdout)
        assert audit_data["status"] == "达标", audit_data
        assert audit_data["metrics"]["effective"] == 19, audit_data

        short_project = root / "short-book"
        run_script(
            str(INIT_SCRIPT),
            str(short_project),
            "--title",
            "短篇",
            "--mode",
            "short",
        )
        short_memory = short_project / "novel-studio"
        assert (short_project / "volumes/volume-001/story.md").exists()
        assert (short_memory / "project.yaml").exists()
        assert (short_memory / "plan.yaml").exists()
        assert (short_project / "extras").is_dir()

        for _ in range(2):
            run_script(
                str(SOURCE_LOG_SCRIPT),
                str(project),
                "--topic",
                "测试主题",
                "--source",
                "测试来源",
                "--url",
                "https://example.com/source",
                "--material",
                "可用素材",
                "--position",
                "novel-studio/memory.yaml",
            )
        source_log = (memory / "logs/research-log.md").read_text(encoding="utf-8")
        assert source_log.count("https://example.com/source") == 1, source_log

        for prompt in ["第一次提示词", "第二次提示词"]:
            run_script(
                str(ART_PROMPT_SCRIPT),
                str(project),
                "--type",
                "character",
                "--title",
                "主角立绘",
                "--target-model",
                "通用中文",
                "--prompt",
                prompt,
                "--negative",
                "文字，水印",
                "--stable",
                "黑发，灰眼，旧风衣",
                "--variable",
                "表情和背景随章节变化",
                "--chapter",
                "ch001",
            )
        prompts = (memory / "logs/art-prompts.md").read_text(encoding="utf-8")
        assert prompts.count("## 角色立绘: 主角立绘 [通用中文]") == 1, prompts
        assert "第一次提示词" not in prompts, prompts
        assert "第二次提示词" in prompts, prompts


def main() -> int:
    assert_shared_metrics()
    assert_scripts()
    print("Smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
