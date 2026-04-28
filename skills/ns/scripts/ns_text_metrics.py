#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Shared text metrics for NS chapter scripts."""

from __future__ import annotations

import re


CJK_CHAR_PATTERN = re.compile(
    "[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff"
    "\U00020000-\U0002ebef]"
)
LATIN_OR_NUMBER_PATTERN = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,:/-]\d+)*")
PLACEHOLDER_PATTERNS = [
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("待补", re.compile(r"(待补|待完善|待续写|待扩写)")),
    ("在这里写", re.compile(r"(在这里写|此处写|这里补)")),
    ("略", re.compile(r"([\[【(（]\s*略\s*[\]】)）]|此处略|下略|略写)")),
]
PLACEHOLDER_LINE_PATTERN = re.compile(
    r"^[\[【(（]?\s*(TODO|待补|待完善|待续写|待扩写|在这里写|此处写|这里补|略|此处略|下略|略写)\s*[\]】)）]?$",
    re.IGNORECASE,
)


def story_text(text: str) -> str:
    """Return countable story text after removing Markdown and placeholder-only lines."""
    text = text.replace("\ufeff", "")
    text = re.sub(r"\A\s*---\s*\n[\s\S]*?\n---\s*", "", text)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^#{1,6}\s+", stripped):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            continue
        if re.match(r"^[-:| ]{3,}$", stripped):
            continue
        if re.match(r"^[-*+]\s+\[[ xX]\]\s+", stripped):
            continue
        if PLACEHOLDER_LINE_PATTERN.match(stripped):
            continue
        stripped = re.sub(r"^>\s*", "", stripped)
        lines.append(stripped)
    return "\n".join(lines)


def effective_word_metrics(text: str) -> dict[str, int]:
    plain = story_text(text)
    cjk_count = len(CJK_CHAR_PATTERN.findall(plain))
    latin_or_number_count = len(LATIN_OR_NUMBER_PATTERN.findall(plain))
    visible_count = len(re.sub(r"\s+", "", plain))
    return {
        "effective": cjk_count + latin_or_number_count,
        "cjk": cjk_count,
        "latin_or_number": latin_or_number_count,
        "visible": visible_count,
    }


def effective_word_count(text: str) -> int:
    return effective_word_metrics(text)["effective"]


def placeholder_markers(text: str) -> list[str]:
    markers = []
    for label, pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            markers.append(label)
    return markers
