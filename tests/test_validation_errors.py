"""Negative tests: invalid documents must be rejected with a useful message."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from tools import checklist


def _errors(data: Any, schema: dict[str, Any], reference: checklist.Reference) -> list[str]:
    return checklist.validate_data(data, schema, reference)


def _item(data: dict[str, Any]) -> dict[str, Any]:
    return data["sections"][0]["items"][0]


def test_minimal_document_is_valid(minimal_checklist, schema, reference) -> None:
    assert _errors(minimal_checklist, schema, reference) == []


@pytest.mark.parametrize("field", ["id", "title", "asvs", "level", "summary", "verification", "evidence"])
def test_missing_required_field(minimal_checklist, schema, reference, field) -> None:
    del _item(minimal_checklist)[field]
    errors = _errors(minimal_checklist, schema, reference)
    assert any(f"'{field}' is a required property" in error for error in errors)


def test_unknown_field_rejected(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["notes"] = "free text"
    assert any("Additional properties" in e for e in _errors(minimal_checklist, schema, reference))


@pytest.mark.parametrize("bad_id", ["6.2.1", "V6.2", "v6.2.1", "V6.2.1.1", "V0.1.1", "ASVS-V6.2.1"])
def test_malformed_asvs_id(minimal_checklist, schema, reference, bad_id) -> None:
    _item(minimal_checklist)["asvs"] = bad_id
    assert any("asvs" in e for e in _errors(minimal_checklist, schema, reference))


def test_nonexistent_asvs_requirement(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["asvs"] = "V6.2.99"
    errors = _errors(minimal_checklist, schema, reference)
    assert errors == ["EX-AUTHN-001: V6.2.99 is not an ASVS 5.0.0 requirement"]


def test_asvs_4_identifier_is_not_accepted(minimal_checklist, schema, reference) -> None:
    # V1.14.6 belongs to ASVS 4.0.3 (V1.14 Configuration Architecture); chapter V1 of
    # ASVS 5.0.0 only has sections V1.1 to V1.5.
    _item(minimal_checklist)["asvs"] = "V1.14.6"
    errors = _errors(minimal_checklist, schema, reference)
    assert errors == ["EX-AUTHN-001: V1.14.6 is not an ASVS 5.0.0 requirement"]


def test_level_mismatch(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["level"] = 2
    errors = _errors(minimal_checklist, schema, reference)
    assert errors == ["EX-AUTHN-001: level 2 does not match ASVS 5.0.0 level 1 for V6.2.1"]


def test_level_out_of_range(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["level"] = 4
    assert any("level" in e for e in _errors(minimal_checklist, schema, reference))


def test_duplicate_item_id(minimal_checklist, schema, reference) -> None:
    items = minimal_checklist["sections"][0]["items"]
    clone = dict(items[0], title="Another distinct title")
    items.append(clone)
    assert "duplicate item id: EX-AUTHN-001" in _errors(minimal_checklist, schema, reference)


def test_duplicate_title(minimal_checklist, schema, reference) -> None:
    items = minimal_checklist["sections"][0]["items"]
    items.append(dict(items[0], id="EX-AUTHN-002"))
    assert any(e.startswith("duplicate item title") for e in _errors(minimal_checklist, schema, reference))


def test_item_prefix_must_match_stack_and_section(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["id"] = "EX-SESS-001"
    errors = _errors(minimal_checklist, schema, reference)
    assert errors == ["EX-SESS-001: identifier must start with 'EX-AUTHN-'"]


@pytest.mark.parametrize("risk", ["API11:2023", "API1:2019", "A01:2021"])
def test_invalid_api_top10_reference(minimal_checklist, schema, reference, risk) -> None:
    _item(minimal_checklist)["api_top10"] = [risk]
    assert _errors(minimal_checklist, schema, reference)


def test_unlisted_zap_alert(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["zap"] = [99999]
    errors = _errors(minimal_checklist, schema, reference)
    assert errors == ["EX-AUTHN-001: ZAP alert 99999 is not listed in reference/zap-alerts.yml"]


def test_related_asvs_must_exist_and_differ(minimal_checklist, schema, reference) -> None:
    _item(minimal_checklist)["related_asvs"] = ["V6.2.1", "V99.1.1"]
    errors = _errors(minimal_checklist, schema, reference)
    assert "EX-AUTHN-001: related_asvs repeats the primary requirement" in errors
    assert "EX-AUTHN-001: related V99.1.1 is not an ASVS 5.0.0 requirement" in errors


def test_wrong_standard_version(minimal_checklist, schema, reference) -> None:
    minimal_checklist["standards"]["asvs"] = "4.0.3"
    assert _errors(minimal_checklist, schema, reference)


def test_duplicate_stack_across_files(tmp_path: Path, minimal_checklist) -> None:
    for name in ("a.yml", "b.yml"):
        (tmp_path / name).write_text(yaml.safe_dump(minimal_checklist), encoding="utf-8")
    with pytest.raises(checklist.ValidationError) as excinfo:
        checklist.validate_files(sorted(tmp_path.glob("*.yml")))
    assert "duplicate stack id across files: example" in excinfo.value.errors


def test_cli_validate_reports_errors(tmp_path: Path, minimal_checklist, capsys) -> None:
    _item(minimal_checklist)["asvs"] = "V6.2.99"
    path = tmp_path / "example.yml"
    path.write_text(yaml.safe_dump(minimal_checklist), encoding="utf-8")
    assert checklist.main(["validate", str(path)]) == 1
    assert "V6.2.99 is not an ASVS 5.0.0 requirement" in capsys.readouterr().err
