"""Rendering is deterministic, complete and in sync with the committed output."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools import checklist


@pytest.mark.parametrize("path", checklist.default_checklists(), ids=lambda p: p.stem)
def test_render_contains_every_item(path: Path, reference: checklist.Reference) -> None:
    data = checklist.load_yaml(path)
    output = checklist.render_markdown(data, reference)
    for section in data["sections"]:
        assert f"## {section['title']}" in output
        for item in section["items"]:
            assert f"### {item['id']} {item['title']}" in output
            assert f"{item['asvs']} (L{item['level']})" in output


@pytest.mark.parametrize("path", checklist.default_checklists(), ids=lambda p: p.stem)
def test_render_is_deterministic(path: Path, reference: checklist.Reference) -> None:
    data = checklist.load_yaml(path)
    assert checklist.render_markdown(data, reference) == checklist.render_markdown(data, reference)


@pytest.mark.parametrize("path", checklist.default_checklists(), ids=lambda p: p.stem)
def test_level_filter(path: Path, reference: checklist.Reference) -> None:
    data = checklist.load_yaml(path)
    output = checklist.render_markdown(data, reference, max_level=1)
    for section in data["sections"]:
        for item in section["items"]:
            heading = f"### {item['id']} {item['title']}"
            assert (heading in output) == (item["level"] == 1), item["id"]


def test_minimal_render_layout(minimal_checklist, reference: checklist.Reference) -> None:
    output = checklist.render_markdown(minimal_checklist, reference)
    assert output.startswith("# Example verification checklist\n")
    assert "| EX-AUTHN-001 |" not in output  # summary rows link to the item
    assert "[EX-AUTHN-001](#ex-authn-001-minimum-password-length)" in output
    assert "V6.2.1 (L1), V6 Authentication / V6.2 Password Security" in output
    assert "API2:2023 Broken Authentication" in output
    assert "[10010 Cookie No HttpOnly Flag](https://www.zaproxy.org/docs/alerts/10010/)" in output
    assert output.endswith("\n") and not output.endswith("\n\n")


def test_committed_output_is_up_to_date() -> None:
    stale = checklist.render_files(
        checklist.default_checklists(), checklist.OUTPUT_DIR, max_levels=[1, 3], check=True
    )
    assert stale == [], "run 'python tools/checklist.py render' and commit the result"


def test_check_mode_detects_stale_output(tmp_path: Path) -> None:
    paths = checklist.default_checklists()
    checklist.render_files(paths, tmp_path, max_levels=[3], check=False)
    target = next(tmp_path.glob("*.md"))
    target.write_text(target.read_text(encoding="utf-8") + "edited\n", encoding="utf-8")
    stale = checklist.render_files(paths, tmp_path, max_levels=[3], check=True)
    assert str(target) in stale


def test_coverage_lists_every_primary_requirement(reference: checklist.Reference) -> None:
    documents = [checklist.load_yaml(path) for path in checklist.default_checklists()]
    output = checklist.render_coverage(documents, reference)
    for document in documents:
        for section in document["sections"]:
            for item in section["items"]:
                assert item["asvs"] in output, item["id"]
