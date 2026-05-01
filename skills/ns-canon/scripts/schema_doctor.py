#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Check Novel Studio project structure, agent constraint files, chapter metadata, and index coverage."""

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
AGENT_CONSTRAINT_FILES = ["AGENTS.md", "CLAUDE.md"]
REQUIRED_VOLUME_FIELDS = ["id", "type", "volume_number", "title", "status", "created_at", "updated_at"]
REQUIRED_VOLUME_SECTIONS = ["卷简介", "卷承诺", "本卷主要人物", "章节目录"]
REQUIRED_CHAPTER_FIELDS = [
    "id",
    "type",
    "chapter_number",
    "title",
    "volume_id",
    "status",
    "created_at",
    "updated_at",
    "word_target",
    "word_count",
]
REQUIRED_CHAPTER_SECTIONS = ["写作目标", "正文"]
MAX_AGENT_CONSTRAINT_CHARS = 4000
MAX_MEMORY_YAML_CHARS = 8000
MAX_BRIEF_CHARS = 6000
MAX_NOTE_CHARS = 12000
MAX_RECORD_CHARS = 12000
MAX_VISUAL_CHARS = 12000
YAML_LENGTH_EXEMPTIONS = {"index.yaml"}


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
            item_text = line[2:].strip()
            if ": " in item_text:
                key, value = item_text.split(":", 1)
                item = {key.strip(): parse_scalar(value)}
                if isinstance(parent, list):
                    parent.append(item)
                    stack.append((indent, item))
                continue
            item = parse_scalar(item_text)
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
            has_children = bool(next_line and next_indent > indent)
            if has_children:
                is_list = next_line.strip().startswith("- ")
                parent[key] = [] if is_list else {}
                stack.append((indent, parent[key]))
            else:
                parent[key] = ""
    return root


def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)}


def first_h1(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def expected_chapter_h1(meta: dict[str, Any]) -> str:
    number = meta.get("chapter_number")
    title = str(meta.get("title", "")).strip()
    if not title or number in {"", None}:
        return ""
    try:
        number_text = f"{int(number):03d}"
    except (TypeError, ValueError):
        number_text = str(number)
    return f"第{number_text}章 {title}"


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
    return {entry["path"] for entry in index_entries(root) if isinstance(entry.get("path"), str)}


def index_entries(root: Path) -> list[dict[str, Any]]:
    index = root / "novel-studio" / "index.yaml"
    if not index.exists():
        return []
    text = index.read_text(encoding="utf-8")
    parsed = parse_simple_yaml(text)
    entries = parsed.get("entries")
    if isinstance(entries, list):
        return [entry for entry in entries if isinstance(entry, dict)]
    return [{"path": path.replace("\\", "/")} for path in re.findall(r"(?m)^\s*path:\s*[\"']?([^\"'\n]+)", text)]


def project_yaml(root: Path, name: str) -> dict[str, Any]:
    path = root / "novel-studio" / name
    if not path.exists():
        return {}
    return parse_simple_yaml(path.read_text(encoding="utf-8"))


def publish_content_root(root: Path) -> str:
    publish = project_yaml(root, "publish.yaml")
    site = publish.get("site")
    content_root = site.get("content_root") if isinstance(site, dict) else None
    return str(content_root).replace("\\", "/").strip("/") if content_root else ""


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


def agent_constraint_files(root: Path) -> list[Path]:
    return [root / name for name in AGENT_CONSTRAINT_FILES if (root / name).exists()]


def check_agent_constraints(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    files = agent_constraint_files(root)
    if len(files) > 1:
        names = ", ".join(rel(path, root) for path in files)
        issues.append(Issue("warning", ".", f"multiple agent constraint files exist; write to first by priority only: {names}"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        if len(text) > MAX_AGENT_CONSTRAINT_CHARS:
            issues.append(Issue("warning", rel(path, root), "agent constraint file should stay short; move story memory into novel-studio/"))
    return issues


def text_size(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return path.stat().st_size


def check_file_lengths(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    ns_dir = root / "novel-studio"
    if ns_dir.exists():
        for path in ns_dir.glob("*.yaml"):
            if path.name in YAML_LENGTH_EXEMPTIONS:
                continue
            if text_size(path) > MAX_MEMORY_YAML_CHARS:
                issues.append(Issue("warning", rel(path, root), "YAML is long; keep summaries here and move long detail into notes/"))

        notes_dir = ns_dir / "notes"
        if notes_dir.exists():
            for path in notes_dir.glob("*.md"):
                if text_size(path) > MAX_NOTE_CHARS:
                    issues.append(Issue("warning", rel(path, root), "notes file is long; split by topic"))

        records_dir = ns_dir / "records"
        if records_dir.exists():
            for path in records_dir.glob("*.md"):
                if text_size(path) > MAX_RECORD_CHARS:
                    issues.append(Issue("warning", rel(path, root), "record file is long; split by date or task"))

        legacy_logs_dir = ns_dir / "logs"
        if legacy_logs_dir.exists():
            issues.append(Issue("warning", rel(legacy_logs_dir, root), "legacy logs directory; move progress/process records into records/"))

    brief = root / "brief.md"
    if brief.exists() and text_size(brief) > MAX_BRIEF_CHARS:
        issues.append(Issue("warning", rel(brief, root), "brief.md is long; keep public copy concise and move detail into notes/"))

    visuals_dir = root / "visuals"
    if visuals_dir.exists():
        for path in visuals_dir.glob("*.md"):
            if text_size(path) > MAX_VISUAL_CHARS:
                issues.append(Issue("warning", rel(path, root), "visual prompt file is long; split by cover, character, scene, or chapter"))

    return issues


def check_index_alignment(root: Path, entries: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    content_root = publish_content_root(root)
    seen_paths: set[str] = set()

    for entry in entries:
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            issues.append(Issue("warning", "novel-studio/index.yaml", "index entry missing path"))
            continue

        path_text = raw_path.replace("\\", "/").strip()
        if path_text in seen_paths:
            issues.append(Issue("warning", "novel-studio/index.yaml", f"duplicate index path: {path_text}"))
        seen_paths.add(path_text)

        if content_root and not (path_text == content_root or path_text.startswith(f"{content_root}/")):
            issues.append(Issue("warning", "novel-studio/index.yaml", f"index path is outside publish.yaml site.content_root: {path_text}"))

        if not (root / path_text).exists():
            issues.append(Issue("warning", "novel-studio/index.yaml", f"indexed Markdown file does not exist: {path_text}"))

    return issues


def as_int(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def check_scale(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    plan = project_yaml(root, "plan.yaml")
    if not plan:
        return issues

    scale = plan.get("scale")
    volumes = plan.get("volumes")
    extras = plan.get("extras")
    if not isinstance(scale, dict):
        issues.append(Issue("warning", "novel-studio/plan.yaml", "missing plan.yaml scale block for target volumes/chapters/extras"))
        return issues

    target_volumes = as_int(scale.get("target_volumes"))
    target_chapters = as_int(scale.get("target_main_chapters"))
    target_extras = as_int(scale.get("target_extras"))

    if volumes is not None and not isinstance(volumes, list):
        issues.append(Issue("warning", "novel-studio/plan.yaml", "volumes should be a list"))
        volumes = []
    if extras is not None and not isinstance(extras, list):
        issues.append(Issue("warning", "novel-studio/plan.yaml", "extras should be a list"))
        extras = []

    volumes_list = volumes if isinstance(volumes, list) else []
    extras_list = extras if isinstance(extras, list) else []
    if target_volumes is not None and volumes_list and len(volumes_list) != target_volumes:
        issues.append(Issue("warning", "novel-studio/plan.yaml", f"scale.target_volumes is {target_volumes}, but volumes has {len(volumes_list)} items"))
    if target_extras is not None and extras_list and len(extras_list) != target_extras:
        issues.append(Issue("warning", "novel-studio/plan.yaml", f"scale.target_extras is {target_extras}, but extras has {len(extras_list)} items"))

    planned_chapters = 0
    for item in volumes_list:
        if not isinstance(item, dict):
            continue
        planned = as_int(item.get("planned_chapters"))
        if planned is not None:
            planned_chapters += planned
    if target_chapters is not None and planned_chapters and planned_chapters != target_chapters:
        issues.append(Issue("warning", "novel-studio/plan.yaml", f"scale.target_main_chapters is {target_chapters}, but volume planned_chapters total is {planned_chapters}"))

    chapters = chapter_files(root)
    main_chapters = [path for path in chapters if "/extras/" not in rel(path, root)]
    extra_chapters = [path for path in chapters if "/extras/" in rel(path, root)]
    if target_chapters is not None and len(main_chapters) > target_chapters:
        issues.append(Issue("warning", "content/", f"main chapter files exceed target_main_chapters: {len(main_chapters)} > {target_chapters}"))
    if target_extras is not None and len(extra_chapters) > target_extras:
        issues.append(Issue("warning", "content/extras/", f"extra files exceed target_extras: {len(extra_chapters)} > {target_extras}"))

    return issues


def check_volume(path: Path, root: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    if not meta:
        issues.append(Issue("error", rel(path, root), "missing YAML frontmatter"))
    for field in REQUIRED_VOLUME_FIELDS:
        value = meta.get(field)
        if field not in meta or value is None or value == "":
            issues.append(Issue("error", rel(path, root), f"missing frontmatter field: {field}"))
    found = headings(body)
    for section in REQUIRED_VOLUME_SECTIONS:
        if section not in found:
            issues.append(Issue("warning", rel(path, root), f"missing section: ## {section}"))
    return issues


def check_chapter(path: Path, root: Path, indexed: dict[str, dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    path_rel = rel(path, root)
    if not meta:
        issues.append(Issue("error", path_rel, "missing YAML frontmatter"))
    for field in REQUIRED_CHAPTER_FIELDS:
        value = meta.get(field)
        if field not in meta or value is None or value == "":
            issues.append(Issue("error", path_rel, f"missing frontmatter field: {field}"))

    h1 = first_h1(body)
    expected_h1 = expected_chapter_h1(meta)
    if expected_h1 and h1 and h1 != expected_h1:
        issues.append(Issue("warning", path_rel, f"H1 does not match chapter_number/title: {h1!r} != {expected_h1!r}"))
    if not h1:
        issues.append(Issue("error", path_rel, "missing H1 chapter title"))

    found = headings(body)
    for section in REQUIRED_CHAPTER_SECTIONS:
        if section not in found:
            issues.append(Issue("error", path_rel, f"missing section: ## {section}"))

    entry = indexed.get(path_rel)
    if indexed and entry is None:
        issues.append(Issue("warning", path_rel, "chapter is not listed in novel-studio/index.yaml entries"))
    elif entry is not None:
        for field in ["id", "volume_id", "chapter_number", "title", "status"]:
            if field in entry and field in meta and str(entry[field]) != str(meta[field]):
                issues.append(Issue("warning", path_rel, f"index.yaml {field} does not match chapter frontmatter"))

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
    issues.extend(check_agent_constraints(root))
    issues.extend(check_file_lengths(root))
    issues.extend(check_scale(root))
    entries = index_entries(root)
    issues.extend(check_index_alignment(root, entries))
    indexed = {entry["path"].replace("\\", "/"): entry for entry in entries if isinstance(entry.get("path"), str)}
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
