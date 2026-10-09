"""Validate and render ASVS verification checklists.

The YAML files under ``checklists/`` are the single source of truth. This
module validates them against the JSON Schema and the reference data in
``reference/``, and renders them to Markdown under ``docs/checklists/``.

Usage:
    python tools/checklist.py validate [FILES...]
    python tools/checklist.py render [--check] [--max-level N] [--output-dir DIR] [FILES...]
    python tools/checklist.py import-asvs PATH_TO_OFFICIAL_CSV
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CHECKLIST_DIR = ROOT / "checklists"
OUTPUT_DIR = ROOT / "docs" / "checklists"
SCHEMA_PATH = ROOT / "schema" / "checklist.schema.json"
ASVS_PATH = ROOT / "reference" / "asvs-5.0.0-requirements.csv"
API_TOP10_PATH = ROOT / "reference" / "api-security-top10-2023.yml"
ZAP_PATH = ROOT / "reference" / "zap-alerts.yml"

ASVS_URL = "https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0"
API_TOP10_URL = "https://owasp.org/API-Security/editions/2023/en/0x11-t10/"
ZAP_ALERT_URL = "https://www.zaproxy.org/docs/alerts/{id}/"


@dataclass(frozen=True)
class AsvsRequirement:
    req_id: str
    level: int
    chapter_id: str
    chapter_name: str
    section_id: str
    section_name: str


@dataclass(frozen=True)
class Reference:
    asvs: dict[str, AsvsRequirement]
    api_top10: dict[str, str]
    zap: dict[int, str]


class ValidationError(Exception):
    """Raised when one or more checklist files fail validation."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_reference() -> Reference:
    with ASVS_PATH.open(encoding="utf-8", newline="") as handle:
        asvs = {
            row["req_id"]: AsvsRequirement(
                req_id=row["req_id"],
                level=int(row["level"]),
                chapter_id=row["chapter_id"],
                chapter_name=row["chapter_name"],
                section_id=row["section_id"],
                section_name=row["section_name"],
            )
            for row in csv.DictReader(handle)
        }
    api_top10 = {risk["id"]: risk["name"] for risk in load_yaml(API_TOP10_PATH)["risks"]}
    zap = {int(alert["id"]): alert["name"] for alert in load_yaml(ZAP_PATH)["alerts"]}
    return Reference(asvs=asvs, api_top10=api_top10, zap=zap)


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def default_checklists() -> list[Path]:
    return sorted(CHECKLIST_DIR.glob("*.yml"))


def schema_errors(data: Any, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema: {location}: {error.message}")
    return errors


def semantic_errors(data: dict[str, Any], reference: Reference) -> list[str]:
    """Checks that JSON Schema cannot express: cross-references and uniqueness."""
    errors: list[str] = []
    prefix = data["stack"]["prefix"]
    item_ids: Counter[str] = Counter()
    titles: Counter[str] = Counter()
    section_ids: Counter[str] = Counter()
    section_codes: Counter[str] = Counter()

    for section in data["sections"]:
        section_ids[section["id"]] += 1
        section_codes[section["code"]] += 1
        expected_prefix = f"{prefix}-{section['code']}-"
        for item in section["items"]:
            item_id = item["id"]
            item_ids[item_id] += 1
            titles[item["title"].casefold()] += 1

            if not item_id.startswith(expected_prefix):
                errors.append(f"{item_id}: identifier must start with '{expected_prefix}'")

            requirement = reference.asvs.get(item["asvs"])
            if requirement is None:
                errors.append(f"{item_id}: {item['asvs']} is not an ASVS 5.0.0 requirement")
            elif requirement.level != item["level"]:
                errors.append(
                    f"{item_id}: level {item['level']} does not match ASVS 5.0.0 "
                    f"level {requirement.level} for {item['asvs']}"
                )

            for related in item.get("related_asvs", []):
                if related not in reference.asvs:
                    errors.append(f"{item_id}: related {related} is not an ASVS 5.0.0 requirement")
                if related == item["asvs"]:
                    errors.append(f"{item_id}: related_asvs repeats the primary requirement")

            for risk in item.get("api_top10", []):
                if risk not in reference.api_top10:
                    errors.append(f"{item_id}: unknown API Security Top 10 risk {risk}")

            for alert in item.get("zap", []):
                if alert not in reference.zap:
                    errors.append(f"{item_id}: ZAP alert {alert} is not listed in reference/zap-alerts.yml")

    for counter, label in (
        (item_ids, "item id"),
        (titles, "item title"),
        (section_ids, "section id"),
        (section_codes, "section code"),
    ):
        errors.extend(f"duplicate {label}: {value}" for value, count in counter.items() if count > 1)
    return errors


def validate_data(data: Any, schema: dict[str, Any], reference: Reference) -> list[str]:
    errors = schema_errors(data, schema)
    if errors:
        # Semantic checks assume a structurally valid document.
        return errors
    return semantic_errors(data, reference)


def validate_files(paths: list[Path]) -> None:
    schema = load_schema()
    reference = load_reference()
    errors: list[str] = []
    stack_ids: Counter[str] = Counter()
    prefixes: Counter[str] = Counter()
    for path in paths:
        data = load_yaml(path)
        errors.extend(f"{path.name}: {message}" for message in validate_data(data, schema, reference))
        if isinstance(data, dict) and isinstance(data.get("stack"), dict):
            stack_ids[data["stack"].get("id")] += 1
            prefixes[data["stack"].get("prefix")] += 1
    errors.extend(f"duplicate stack id across files: {v}" for v, c in stack_ids.items() if c > 1)
    errors.extend(f"duplicate stack prefix across files: {v}" for v, c in prefixes.items() if c > 1)
    if errors:
        raise ValidationError(errors)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _block(text: str) -> str:
    return text.strip() + "\n"


def render_markdown(data: dict[str, Any], reference: Reference, max_level: int = 3) -> str:
    stack = data["stack"]
    source = f"checklists/{stack['id']}.yml"
    sections = []
    for section in data["sections"]:
        items = [item for item in section["items"] if item["level"] <= max_level]
        if items:
            sections.append((section, items))

    all_items = [item for _, items in sections for item in items]
    per_level = Counter(item["level"] for item in all_items)
    level_text = ", ".join(f"L{level}: {per_level.get(level, 0)}" for level in range(1, max_level + 1))
    scope_label = "all levels" if max_level == 3 else f"levels up to L{max_level}"

    out: list[str] = []
    out.append(f"# {stack['name']} verification checklist\n")
    out.append(f"<!-- Generated from {source} by tools/checklist.py. Do not edit by hand. -->\n")
    out.append(_block(stack["scope"]))
    out.append("| Property | Value |")
    out.append("| --- | --- |")
    out.append(f"| Standard | [OWASP ASVS 5.0.0]({ASVS_URL}) |")
    out.append(f"| API risks | [OWASP API Security Top 10 2023]({API_TOP10_URL}) |")
    out.append(f"| Scope | {scope_label} |")
    out.append(f"| Items | {len(all_items)} ({level_text}) |")
    out.append("")
    out.append(
        "Requirement summaries are paraphrased. The official ASVS text is authoritative; "
        "consult it before recording a result.\n"
    )

    out.append("## Contents\n")
    for section, items in sections:
        out.append(f"- [{section['title']}](#{_anchor(section['title'])}) ({len(items)})")
    out.append("")

    out.append("## Summary\n")
    out.append("| ID | Title | ASVS | Level | API Top 10 |")
    out.append("| --- | --- | --- | --- | --- |")
    for item in all_items:
        risks = ", ".join(item.get("api_top10", [])) or "-"
        out.append(
            f"| [{item['id']}](#{_anchor(item['id'] + ' ' + item['title'])}) | {_cell(item['title'])} "
            f"| {item['asvs']} | L{item['level']} | {risks} |"
        )
    out.append("")

    for section, items in sections:
        out.append(f"## {section['title']}\n")
        if section.get("intro"):
            out.append(_block(section["intro"]))
        for item in items:
            out.extend(_render_item(item, reference, stack["name"]))

    return "\n".join(out).rstrip() + "\n"


def _render_item(item: dict[str, Any], reference: Reference, stack_name: str) -> list[str]:
    requirement = reference.asvs[item["asvs"]]
    lines = [f"### {item['id']} {item['title']}\n"]
    lines.append("- [ ] Verified")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    lines.append(
        f"| ASVS 5.0.0 | {item['asvs']} (L{item['level']}), "
        f"{requirement.chapter_id} {requirement.chapter_name} / "
        f"{requirement.section_id} {requirement.section_name} |"
    )
    if item.get("related_asvs"):
        lines.append(f"| Related ASVS | {', '.join(item['related_asvs'])} |")
    if item.get("api_top10"):
        risks = ", ".join(f"{risk} {reference.api_top10[risk]}" for risk in item["api_top10"])
        lines.append(f"| API Top 10 | {risks} |")
    if item.get("zap"):
        alerts = ", ".join(
            f"[{alert} {reference.zap[alert]}]({ZAP_ALERT_URL.format(id=alert)})" for alert in item["zap"]
        )
        lines.append(f"| ZAP alerts | {alerts} |")
    lines.append("")
    lines.append(f"**Requirement summary.** {item['summary'].strip()}\n")
    lines.append(f"**How to verify in {stack_name}.**\n")
    lines.append(_block(item["verification"]))
    lines.append(f"**Evidence.** {item['evidence'].strip()}\n")
    return lines


def _anchor(text: str) -> str:
    """GitHub-compatible heading anchor."""
    keep = []
    for char in text.strip().lower():
        if char.isalnum() or char in "-_":
            keep.append(char)
        elif char == " ":
            keep.append("-")
    return "".join(keep)


def render_coverage(documents: list[dict[str, Any]], reference: Reference) -> str:
    """Matrix of ASVS sections touched by at least one checklist, per stack."""
    stacks = [(doc["stack"]["name"], _covered(doc)) for doc in documents]
    sections: dict[str, list[AsvsRequirement]] = {}
    for requirement in reference.asvs.values():
        sections.setdefault(requirement.section_id, []).append(requirement)
    touched = sorted(
        {reference.asvs[req].section_id for _, covered in stacks for req in covered},
        key=_section_key,
    )

    out = ["# ASVS 5.0.0 coverage\n"]
    out.append("<!-- Generated from checklists/*.yml by tools/checklist.py. Do not edit by hand. -->\n")
    out.append(
        "Requirements covered by at least one checklist item, either as the primary requirement "
        "or as a related requirement, grouped by ASVS section. Sections with no coverage are "
        "omitted.\n"
    )
    header = "| Section | Requirements | " + " | ".join(name for name, _ in stacks) + " |"
    out.append(header)
    out.append("| --- | --- | " + " | ".join("---" for _ in stacks) + " |")
    for section_id in touched:
        requirements = sections[section_id]
        name = requirements[0].section_name
        cells = []
        for _, covered in stacks:
            ids = [req.req_id for req in requirements if req.req_id in covered]
            cells.append(", ".join(ids) if ids else "-")
        out.append(f"| {section_id} {name} | {len(requirements)} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("| Stack | Items | ASVS requirements referenced |")
    out.append("| --- | --- | --- |")
    for doc, (name, covered) in zip(documents, stacks, strict=True):
        items = sum(len(section["items"]) for section in doc["sections"])
        out.append(f"| {name} | {items} | {len(covered)} |")
    return "\n".join(out) + "\n"


def _covered(document: dict[str, Any]) -> set[str]:
    covered: set[str] = set()
    for section in document["sections"]:
        for item in section["items"]:
            covered.add(item["asvs"])
            covered.update(item.get("related_asvs", []))
    return covered


def _section_key(section_id: str) -> tuple[int, ...]:
    return tuple(int(part) for part in section_id.lstrip("V").split("."))


def output_name(stack_id: str, max_level: int) -> str:
    return f"{stack_id}.md" if max_level == 3 else f"{stack_id}-l{max_level}.md"


def render_files(paths: list[Path], output_dir: Path, max_levels: list[int], check: bool) -> list[str]:
    """Render checklists. In check mode, return the list of stale outputs instead of writing."""
    reference = load_reference()
    documents = [load_yaml(path) for path in paths]
    outputs: list[tuple[Path, str]] = []
    for data in documents:
        for max_level in max_levels:
            target = output_dir / output_name(data["stack"]["id"], max_level)
            outputs.append((target, render_markdown(data, reference, max_level=max_level)))
    outputs.append((output_dir / "coverage.md", render_coverage(documents, reference)))

    stale: list[str] = []
    if not check:
        output_dir.mkdir(parents=True, exist_ok=True)
    for target, content in outputs:
        if check:
            current = target.read_text(encoding="utf-8") if target.exists() else None
            if current != content:
                stale.append(str(target.relative_to(ROOT) if target.is_relative_to(ROOT) else target))
        else:
            target.write_text(content, encoding="utf-8")
    return stale


def import_asvs(source: Path) -> int:
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with ASVS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["req_id", "level", "chapter_id", "chapter_name", "section_id", "section_name"])
        for row in rows:
            writer.writerow(
                [
                    row["req_id"],
                    row["L"],
                    row["chapter_id"],
                    row["chapter_name"],
                    row["section_id"],
                    row["section_name"],
                ]
            )
    return len(rows)


def _display(path: Path) -> str:
    resolved = path.resolve()
    return str(resolved.relative_to(ROOT)) if resolved.is_relative_to(ROOT) else str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="validate checklist sources")
    p_validate.add_argument("files", nargs="*", type=Path)

    p_render = sub.add_parser("render", help="render checklists to Markdown")
    p_render.add_argument("files", nargs="*", type=Path)
    p_render.add_argument("--check", action="store_true", help="fail if rendered output is stale")
    p_render.add_argument(
        "--max-level",
        type=int,
        choices=[1, 2, 3],
        action="append",
        help="render only items up to this level (repeatable; default: 1 and 3)",
    )
    p_render.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)

    p_import = sub.add_parser("import-asvs", help="regenerate the ASVS reference from the official CSV")
    p_import.add_argument("source", type=Path)

    args = parser.parse_args(argv)

    if args.command == "import-asvs":
        count = import_asvs(args.source)
        print(f"wrote {count} requirements to {ASVS_PATH.relative_to(ROOT)}")
        return 0

    files = args.files or default_checklists()
    if not files:
        print("no checklist files found", file=sys.stderr)
        return 1

    if args.command == "validate":
        try:
            validate_files(files)
        except ValidationError as exc:
            for message in exc.errors:
                print(message, file=sys.stderr)
            print(f"{len(exc.errors)} error(s)", file=sys.stderr)
            return 1
        print(f"{len(files)} checklist file(s) valid")
        return 0

    try:
        validate_files(files)
    except ValidationError as exc:
        for message in exc.errors:
            print(message, file=sys.stderr)
        return 1
    max_levels = sorted(set(args.max_level or [1, 3]))
    stale = render_files(files, args.output_dir, max_levels, check=args.check)
    if args.check:
        if stale:
            for target in stale:
                print(f"stale: {target}", file=sys.stderr)
            print("run 'python tools/checklist.py render' and commit the result", file=sys.stderr)
            return 1
        print("rendered output is up to date")
    else:
        print(f"rendered {len(files) * len(max_levels) + 1} file(s) to {_display(args.output_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
