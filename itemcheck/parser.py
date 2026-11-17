"""Parse items written in a small Markdown format.

    ---
    id: EX-001
    domain: Internal Medicine
    ---
    ## Stem
    A 58-year-old man ...
    ## Lead-in
    Which of the following is the most likely diagnosis?
    ## Options
    A. Option text
    B. Option text
    ## Key
    B

Several items can live in one file, separated by a line with ``===``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

OPTION_RE = re.compile(r"^\s*([A-Z])[\.\)]\s+(.*\S)\s*$")


@dataclass
class Item:
    id: str
    stem: str
    lead_in: str
    options: dict[str, str]
    key: str
    meta: dict[str, str] = field(default_factory=dict)
    source: str = ""


def _sections(text: str) -> dict[str, str]:
    parts = re.split(r"^##\s+(.+?)\s*$", text, flags=re.M)
    return {parts[i].strip().lower(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def parse_item(text: str, source: str = "") -> Item:
    meta = {}
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    sec = _sections(text)
    options = {}
    for line in sec.get("options", "").splitlines():
        om = OPTION_RE.match(line)
        if om:
            options[om.group(1)] = om.group(2)
    return Item(
        id=meta.get("id", "item"),
        stem=sec.get("stem", ""),
        lead_in=sec.get("lead-in", sec.get("lead in", "")),
        options=options,
        key=sec.get("key", "").strip()[:1].upper(),
        meta=meta,
        source=source,
    )


def parse_file(path: str | Path) -> list[Item]:
    text = Path(path).read_text(encoding="utf-8")
    chunks = [c for c in re.split(r"^===\s*$", text, flags=re.M) if c.strip()]
    return [parse_item(c, str(path)) for c in chunks]
