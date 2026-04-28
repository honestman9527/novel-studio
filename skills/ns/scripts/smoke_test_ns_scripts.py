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
        workspace = root / "workspace"
        chapter = root / "ch001.md"
        chapter.write_text("# 第一章 测试\n这是AI-17计划。她说：“三天后再见。”\n", encoding="utf-8")

        run_script(str(INIT_SCRIPT), str(workspace), "--novel", "test-book", "--title", "测试书", "--mode", "long")
        project = workspace / "novels/test-book"

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

        progress = (project / "00-meta/progress.md").read_text(encoding="utf-8")
        summary = (project / "07-finish/chapter-summary.md").read_text(encoding="utf-8")
        timeline = (project / "02-bible/timeline.md").read_text(encoding="utf-8")
        revision = (project / "05-revisions/revision-log.md").read_text(encoding="utf-8")

        assert progress.count("最近章节：ch001") == 1, progress
        assert summary.count("| ch001 测试章 |") == 1, summary
        assert timeline.count("| ch001 |") == 1, timeline
        assert revision.count("| ch001 |") == 1, revision

        audit = run_script(str(AUDIT_SCRIPT), str(chapter), "--min", "10", "--max", "20", "--json")
        audit_data = json.loads(audit.stdout)
        assert audit_data["status"] == "达标", audit_data
        assert audit_data["metrics"]["effective"] == 13, audit_data

        short_workspace = root / "short-workspace"
        run_script(
            str(INIT_SCRIPT),
            str(short_workspace),
            "--novel",
            "short-book",
            "--title",
            "短篇",
            "--mode",
            "short",
            "--minimal-short",
        )
        short_project = short_workspace / "novels/short-book"
        assert (short_project / "04-drafts/short/story.md").exists()
        assert (short_project / "00-meta/project.md").exists()
        assert not (short_project / "00-meta/progress.md").exists()
        assert not (short_project / "03-outline/chapter-outline.md").exists()

        for _ in range(2):
            run_script(
                str(SOURCE_LOG_SCRIPT),
                str(workspace),
                "--novel",
                "test-book",
                "--topic",
                "测试主题",
                "--source",
                "测试来源",
                "--url",
                "https://example.com/source",
                "--material",
                "可用素材",
                "--position",
                "02-bible/world.md",
            )
        source_log = (project / "00-meta/source-log.md").read_text(encoding="utf-8")
        assert source_log.count("https://example.com/source") == 1, source_log

        for prompt in ["第一次提示词", "第二次提示词"]:
            run_script(
                str(ART_PROMPT_SCRIPT),
                str(workspace),
                "--novel",
                "test-book",
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
        prompts = (project / "06-art/prompts.md").read_text(encoding="utf-8")
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
