"""Validation of the checklist sources shipped in checklists/."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from tools import checklist

ITEM_ID = re.compile(r"^[A-Z]{2,6}-[A-Z]{2,6}-[0-9]{3}$")
ASVS_ID = re.compile(r"^V[1-9][0-9]?\.[1-9][0-9]?\.[1-9][0-9]?$")
REQUIRED_FIELDS = ("id", "title", "asvs", "level", "summary", "verification", "evidence")


def _items(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for section in data["sections"] for item in section["items"]]


@pytest.fixture(scope="module", params=checklist.default_checklists(), ids=lambda p: p.stem)
def source(request: pytest.FixtureRequest) -> tuple[Path, dict[str, Any]]:
    path: Path = request.param
    return path, checklist.load_yaml(path)


def test_file_name_matches_stack_id(source: tuple[Path, dict[str, Any]]) -> None:
    path, data = source
    assert path.stem == data["stack"]["id"]


def test_schema_valid(source: tuple[Path, dict[str, Any]], schema: dict[str, Any]) -> None:
    _, data = source
    assert checklist.schema_errors(data, schema) == []


def test_semantically_valid(source: tuple[Path, dict[str, Any]], reference: checklist.Reference) -> None:
    _, data = source
    assert checklist.semantic_errors(data, reference) == []


def test_required_fields_present_and_non_empty(source: tuple[Path, dict[str, Any]]) -> None:
    _, data = source
    for item in _items(data):
        for field in REQUIRED_FIELDS:
            value = item.get(field)
            assert value not in (None, ""), f"{item.get('id')}: missing {field}"
            if isinstance(value, str):
                assert value.strip(), f"{item['id']}: blank {field}"


def test_identifier_formats(source: tuple[Path, dict[str, Any]]) -> None:
    _, data = source
    for item in _items(data):
        assert ITEM_ID.match(item["id"]), item["id"]
        assert ASVS_ID.match(item["asvs"]), item["id"]
        for related in item.get("related_asvs", []):
            assert ASVS_ID.match(related), item["id"]


def test_no_duplicate_item_ids(source: tuple[Path, dict[str, Any]]) -> None:
    _, data = source
    ids = [item["id"] for item in _items(data)]
    assert len(ids) == len(set(ids))


def test_item_ids_increase_within_section(source: tuple[Path, dict[str, Any]]) -> None:
    # Retired identifiers are never reused, so gaps are allowed but order is not.
    _, data = source
    for section in data["sections"]:
        numbers = [int(item["id"].rsplit("-", 1)[1]) for item in section["items"]]
        assert numbers == sorted(set(numbers)), section["id"]


def test_levels_match_official_asvs(
    source: tuple[Path, dict[str, Any]], reference: checklist.Reference
) -> None:
    _, data = source
    for item in _items(data):
        assert item["level"] == reference.asvs[item["asvs"]].level, item["id"]


def test_no_placeholder_text(source: tuple[Path, dict[str, Any]]) -> None:
    path, _ = source
    text = path.read_text(encoding="utf-8").lower()
    for marker in ("lorem", "todo", "tbd", "fixme", "xxx"):
        assert marker not in text, f"{path.name} contains '{marker}'"


def test_stacks_cover_the_same_core_requirements(checklist_paths: list[Path]) -> None:
    """Both stacks should verify the same core controls so results are comparable."""
    core = {"V6.2.1", "V6.3.1", "V7.2.4", "V7.4.1", "V8.2.1", "V8.2.2", "V8.2.3", "V1.2.4", "V3.4.2"}
    for path in checklist_paths:
        covered = {item["asvs"] for item in _items(checklist.load_yaml(path))}
        assert core <= covered, f"{path.name} misses {sorted(core - covered)}"


def test_validate_files_accepts_shipped_sources(checklist_paths: list[Path]) -> None:
    checklist.validate_files(checklist_paths)


def test_readme_totals_match_sources(checklist_paths: list[Path]) -> None:
    readme = (checklist.ROOT / "README.md").read_text(encoding="utf-8")
    totals = [len(_items(checklist.load_yaml(path))) for path in checklist_paths]
    row = next(line for line in readme.splitlines() if line.startswith("| Total |"))
    stated = [int(cell) for cell in row.strip("|").split("|")[2:] if cell.strip()]
    assert sorted(stated) == sorted(totals)
