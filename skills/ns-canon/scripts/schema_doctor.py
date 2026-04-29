#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Check Novel Studio project structure, chapter metadata, and index coverage."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SHARED_SCRIPT_DIR = Path(__file__).resolve().parents[2] / "ns" / "scripts"
if str(SHARED_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPT_DIR))

from ns_text_metrics import effective_word_metrics


REQUIRED_PROJECT_FILES = [
    "project.yaml",
    "plan.yaml",
    "memory.yaml",
    "continuity.yaml",
    "index.yaml",
    "style.yaml",
    "research.yaml",
    "art.yaml",
    "finish.yaml",
    "publish.yaml",
]
REQUIRED_VOLUME_FIELDS = ["id", "type", "volume_number", "title", "status", "created_at", "updated_at"]
REQUIRED_VOLUME_SECTIONS = ["卷简介", "卷承诺", "本卷主要人物", "章节目录"]
REQUIRED_CHAPTER_FIELDS = [
    "id",
    "type",
    "chapter_number",
    "title",
    "display_title",
    "volume_id",
    "volume_number",
    "volume_title",
    "weight",
    "status",
    "created_at",
    "updated_at",
]
REQUIRED_CHAPTER_SECTIONS = ["写作目标", "正文"]


@dataclass
class Issue:
    severity: str
    file: str
    message: str


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    text = text.replace("\ufeff", "")
    match = re.match(r"\A---\s*\n(?P<yaml>[\s\S]*?)\n---\s*\n?", text)
    if not match:
        return {}, text
    return parse_simple_yaml(match.group("yaml")), text[match.end() :]


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Small YAML subset parser for NS frontmatter and index path checks."""
    raw_lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for idx, raw in enumerate(raw_lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            item = parse_scalar(line[2:])
            if isinstance(parent, list):
                parent.append(item)
            continue

        if ":" not in line or not isinstance(parent, dict):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            parent[key] = parse_scalar(value)
        else:
            next_line = ""
            for following in raw_lines[idx + 1 :]:
                if following.strip() and not following.lstrip().startswith("#"):
                    next_line = following
                    break
            next_indent = len(next_line) - len(next_line.lstrip(" ")) if next_line else indent
            is_list = bool(next_line.strip().startswith("- ") and next_indent > indent)
            parent[key] = [] if is_list else {}
            stack.append((indent, parent[key]))
    return root


def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)}


def first_h1(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def chapter_files(root: Path) -> list[Path]:
    content = root / "content"
    files = []
    if content.exists():
        files.extend(p for p in content.rglob("*.md") if p.name != "_index.md")
    return sorted(files)


def volume_files(root: Path) -> list[Path]:
    content = root / "content"
    return sorted(content.rglob("_index.md")) if content.exists() else []


def index_paths(root: Path) -> set[str]:
    index = root / "novel-studio" / "index.yaml"
    if not index.exists():
        return set()
    text = index.read_text(encoding="utf-8")
    return {m.group(1).replace("\\", "/") for m in re.finditer(r"(?m)^\s*path:\s*[\"']?([^\"'\n]+)", text)}


def check_project(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    ns_dir = root / "novel-studio"
    content_dir = root / "content"
    if not ns_dir.exists():
        issues.append(Issue("error", "novel-studio/", "missing novel-studio directory"))
    if not content_dir.exists():
        issues.append(Issue("error", "content/", "missing content directory"))
    for name in REQUIRED_PROJECT_FILES:
        path = ns_dir / name
        if not path.exists():
            issues.append(Issue("warning", rel(path, root), "missing recommended project YAML file"))
    return issues


def check_volume(path: Path, root: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    if not meta:
        issues.append(Issue("error", rel(path, root), "missing YAML frontmatter"))
    for field in REQUIRED_VOLUME_FIELDS:
        if field not in meta or meta.get(field) in {"", None}:
            issues.append(Issue("error", rel(path, root), f"missing frontmatter field: {field}"))
    found = headings(body)
    for section in REQUIRED_VOLUME_SECTIONS:
        if section not in found:
            issues.append(Issue("warning", rel(path, root), f"missing section: ## {section}"))
    return issues


def check_chapter(path: Path, root: Path, indexed: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    path_rel = rel(path, root)
    if not meta:
        issues.append(Issue("error", path_rel, "missing YAML frontmatter"))
    for field in REQUIRED_CHAPTER_FIELDS:
        if field not in meta or meta.get(field) in {"", None}:
            issues.append(Issue("error", path_rel, f"missing frontmatter field: {field}"))

    title = str(meta.get("display_title", "")).strip()
    h1 = first_h1(body)
    if title and h1 and title != h1:
        issues.append(Issue("warning", path_rel, f"H1 does not match display_title: {h1!r} != {title!r}"))
    if not h1:
        issues.append(Issue("error", path_rel, "missing H1 chapter title"))

    found = headings(body)
    for section in REQUIRED_CHAPTER_SECTIONS:
        if section not in found:
            issues.append(Issue("error", path_rel, f"missing section: ## {section}"))

    if indexed and path_rel not in indexed:
        issues.append(Issue("warning", path_rel, "chapter is not listed in novel-studio/index.yaml entries"))

    metrics = effective_word_metrics(text)
    word_count = meta.get("word_count")
    effective = word_count.get("effective") if isinstance(word_count, dict) else None
    if effective not in {"", None}:
        try:
            if int(effective) != metrics["effective"]:
                issues.append(Issue("warning", path_rel, f"frontmatter word_count.effective is {effective}, audited {metrics['effective']}"))
        except (TypeError, ValueError):
            issues.append(Issue("warning", path_rel, "frontmatter word_count.effective is not numeric"))
    return issues


def payload(issues: list[Issue]) -> dict[str, Any]:
    return {
        "ok": not any(issue.severity == "error" for issue in issues),
        "errors": sum(1 for issue in issues if issue.severity == "error"),
        "warnings": sum(1 for issue in issues if issue.severity == "warning"),
        "issues": [issue.__dict__ for issue in issues],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 Novel Studio 项目结构、卷/章节 frontmatter 和 index 覆盖。")
    parser.add_argument("root", nargs="?", default=".", help="小说项目根目录。")
    parser.add_argument("--json", action="store_true", help="输出 JSON。")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues = check_project(root)
    indexed = index_paths(root)
    for path in volume_files(root):
        issues.extend(check_volume(path, root))
    for path in chapter_files(root):
        issues.extend(check_chapter(path, root, indexed))

    data = payload(issues)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"Schema doctor: {'OK' if data['ok'] else 'FAILED'} ({data['errors']} errors, {data['warnings']} warnings)")
        for issue in issues:
            print(f"[{issue.severity}] {issue.file}: {issue.message}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
