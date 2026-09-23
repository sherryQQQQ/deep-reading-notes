#!/usr/bin/env python3
"""Render a Markdown note from a compact JSON payload without overwriting files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path


ALLOWED_TYPES = {"source", "literature", "concept", "claim", "question", "evergreen"}
ALLOWED_STATUS = {"inbox", "reading", "processed", "revisit"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", normalized, flags=re.UNICODE)
    slug = re.sub(r"[-_]{2,}", "-", slug).strip("-_")
    return slug[:64] or "note"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_string(v) for v in values) + "]"


def load_payload(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object")
    for field in ("title", "note_type", "body"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Missing non-empty string field: {field}")
    if data["note_type"] not in ALLOWED_TYPES:
        raise ValueError(f"note_type must be one of: {', '.join(sorted(ALLOWED_TYPES))}")
    status = data.get("status", "processed")
    if status not in ALLOWED_STATUS:
        raise ValueError(f"status must be one of: {', '.join(sorted(ALLOWED_STATUS))}")
    for field in ("locators", "tags"):
        value = data.get(field, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field} must be a list of strings")
    return data


def render(data: dict, note_id: str, created: str) -> str:
    lines = [
        "---",
        f"id: {yaml_string(note_id)}",
        f"title: {yaml_string(data['title'].strip())}",
        f"note_type: {yaml_string(data['note_type'])}",
    ]
    if data.get("source_id"):
        lines.append(f"source_id: {yaml_string(str(data['source_id']))}")
    if data.get("locators"):
        lines.append(f"locators: {yaml_list(data['locators'])}")
    if data.get("tags"):
        lines.append(f"tags: {yaml_list(data['tags'])}")
    lines.extend(
        [
            f"status: {yaml_string(data.get('status', 'processed'))}",
            f"created: {yaml_string(created)}",
            "---",
            "",
            data["body"].strip(),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON payload")
    parser.add_argument("--output-dir", required=True, type=Path, help="Note directory")
    parser.add_argument("--id", help="Optional stable note id")
    args = parser.parse_args()

    data = load_payload(args.input)
    created = str(data.get("created") or dt.date.today().isoformat())
    note_id = args.id or f"{created.replace('-', '')}-{slugify(data['title'])}"
    filename = f"{note_id}.md"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / filename
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing note: {output}")
    output.write_text(render(data, note_id, created), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
