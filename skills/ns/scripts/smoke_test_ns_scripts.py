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
AUDIT_SCRIPT = REPO_ROOT / "skills/ns-draft/scripts/chapter_audit.py"


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
        chapter.parent.mkdir(parents=True)
        chapter.write_text("# 第一章 测试\n\n## 写作目标\n\n- 本章功能：测试\n\n## 正文\n\n这是AI-17计划。她说：“三天后再见。”\n\n## 章末回写\n\n```yaml\nsummary: 测试\n```\n", encoding="utf-8")

        audit = run_script(str(AUDIT_SCRIPT), str(chapter), "--min", "10", "--max", "20", "--json")
        audit_data = json.loads(audit.stdout)
        assert audit_data["status"] == "达标", audit_data
        assert audit_data["metrics"]["effective"] == 19, audit_data


def main() -> int:
    assert_shared_metrics()
    assert_scripts()
    print("Smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
