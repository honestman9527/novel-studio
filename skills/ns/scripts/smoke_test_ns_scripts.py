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
AUDIT_SCRIPT = REPO_ROOT / "skills/ns-write/scripts/chapter_audit.py"
SCHEMA_DOCTOR_SCRIPT = REPO_ROOT / "skills/ns-canon/scripts/schema_doctor.py"
CONTINUITY_CHECK_SCRIPT = REPO_ROOT / "skills/ns-canon/scripts/continuity_check.py"
EXPORT_SCRIPT = REPO_ROOT / "skills/ns-write/scripts/export_text.py"


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
## 写作目标
这段不应该计入正文。
## 正文
这是AI-17计划。她说：“三天后再见。”
| 备注 | 不应计入 |
| --- | --- |
- [ ] 待办项不应计入
（略）
## 章末笔记
summary: 不应该计入
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
        ns_dir = project / "novel-studio"
        volume_dir = project / "content/volumes/volume-001"
        chapter = volume_dir / "ch001.md"
        volume_index = volume_dir / "_index.md"
        ns_dir.mkdir(parents=True)
        chapter.parent.mkdir(parents=True)

        for name in [
            "project.yaml",
            "memory.yaml",
            "continuity.yaml",
            "style.yaml",
            "research.yaml",
            "art.yaml",
            "finish.yaml",
            "publish.yaml",
        ]:
            (ns_dir / name).write_text("{}\n", encoding="utf-8")
        (ns_dir / "plan.yaml").write_text(
            "scale:\n"
            "  target_volumes: 1\n"
            "  target_main_chapters: 1\n"
            "  target_extras: 0\n"
            "  target_total_words: 13\n"
            "  chapter_word_target: 10-20\n"
            "  limits_are: soft\n"
            "volumes:\n"
            "  - id: volume-001\n"
            "    title: 第一卷\n"
            "    planned_chapters: 1\n"
            "    chapter_range:\n"
            "      start: ch001\n"
            "      end: ch001\n"
            "    word_target: 13\n"
            "    status: drafting\n"
            "extras: []\n",
            encoding="utf-8",
        )
        (ns_dir / "index.yaml").write_text(
            "entries:\n"
            "  - id: ch001\n"
            "    path: content/volumes/volume-001/ch001.md\n"
            "    status: draft\n",
            encoding="utf-8",
        )
        (project / "NOVEL.md").write_text(
            "# NOVEL\n\n"
            "## 必须遵守\n\n"
            "- 保持测试章结构。\n\n"
            "## 不要写/不要改\n\n"
            "- 不要改测试人物。\n",
            encoding="utf-8",
        )
        volume_index.write_text(
            "---\n"
            "id: volume-001\n"
            "type: volume\n"
            "volume_number: 1\n"
            "title: 第一卷\n"
            "display_title: 第一卷\n"
            "status: drafting\n"
            "created_at: 2026-04-29T00:00:00+08:00\n"
            "updated_at: 2026-04-29T00:00:00+08:00\n"
            "---\n\n"
            "# 第一卷\n\n"
            "## 卷简介\n\n测试卷。\n\n"
            "## 卷承诺\n\n测试承诺。\n\n"
            "## 本卷主要人物\n\n- 她\n\n"
            "## 章节目录\n\n| 章节 | 标题 | 状态 | 功能 | 字数 |\n| --- | --- | --- | --- | --- |\n\n"
            "## 卷末笔记\n",
            encoding="utf-8",
        )
        chapter.write_text(
            "---\n"
            "id: ch001\n"
            "type: main\n"
            "chapter_number: 1\n"
            "title: 测试\n"
            "display_title: 第001章 测试\n"
            "volume_id: volume-001\n"
            "volume_number: 1\n"
            "volume_title: 第一卷\n"
            "weight: 1\n"
            "status: draft\n"
            "created_at: 2026-04-29T00:00:00+08:00\n"
            "updated_at: 2026-04-29T00:00:00+08:00\n"
            "word_target: 10-20\n"
            "word_count:\n"
            "  effective: 13\n"
            "  counted_at: 2026-04-29T00:00:00+08:00\n"
            "---\n\n"
            "# 第001章 测试\n\n"
            "## 写作目标\n\n- 本章功能：测试\n\n"
            "## 正文\n\n这是AI-17计划。她说：“三天后再见。”\n\n"
            "## 章末笔记\n\n"
            "- 本章概要：测试。\n"
            "- 未收束：门后的声音来源\n"
            "- 下一章钩子：她将在门后发现新线索\n",
            encoding="utf-8",
        )

        audit = run_script(str(AUDIT_SCRIPT), str(chapter), "--min", "10", "--max", "20", "--json")
        audit_data = json.loads(audit.stdout)
        assert audit_data["total_effective"] == 13, audit_data
        assert audit_data["files"][0]["status"] == "达标", audit_data
        assert audit_data["files"][0]["metrics"]["effective"] == 13, audit_data

        doctor = run_script(str(SCHEMA_DOCTOR_SCRIPT), str(project), "--json")
        doctor_data = json.loads(doctor.stdout)
        assert doctor_data["ok"] is True, doctor_data

        continuity = run_script(str(CONTINUITY_CHECK_SCRIPT), str(project), "--json")
        continuity_data = json.loads(continuity.stdout)
        assert continuity_data["counts"]["unresolved"] == 1, continuity_data
        assert continuity_data["counts"]["next_hooks"] == 1, continuity_data

        export_path = project / "export/novel.md"
        run_script(str(EXPORT_SCRIPT), str(project), "-o", str(export_path))
        exported = export_path.read_text(encoding="utf-8")
        assert "这是AI-17计划" in exported, exported
        assert "写作目标" not in exported, exported
        assert "summary" not in exported, exported


def main() -> int:
    assert_shared_metrics()
    assert_scripts()
    print("Smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
