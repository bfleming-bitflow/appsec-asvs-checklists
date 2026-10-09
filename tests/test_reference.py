"""Sanity checks on the vendored reference data."""

from __future__ import annotations

import re

from tools import checklist

ASVS_ID = re.compile(r"^V[1-9][0-9]?\.[1-9][0-9]?\.[1-9][0-9]?$")


def test_asvs_reference_has_all_requirements(reference: checklist.Reference) -> None:
    # ASVS 5.0.0 defines 345 requirements across 17 chapters.
    assert len(reference.asvs) == 345
    assert {req.chapter_id for req in reference.asvs.values()} == {f"V{n}" for n in range(1, 18)}


def test_asvs_reference_ids_and_levels(reference: checklist.Reference) -> None:
    for req_id, requirement in reference.asvs.items():
        assert ASVS_ID.match(req_id), req_id
        assert requirement.level in (1, 2, 3), req_id
        assert req_id.startswith(requirement.section_id + "."), req_id
        assert requirement.section_id.startswith(requirement.chapter_id + "."), req_id


def test_api_top10_reference(reference: checklist.Reference) -> None:
    assert list(reference.api_top10) == [f"API{n}:2023" for n in range(1, 11)]


def test_zap_reference_is_unique_and_named(reference: checklist.Reference) -> None:
    raw = checklist.load_yaml(checklist.ZAP_PATH)["alerts"]
    ids = [alert["id"] for alert in raw]
    assert len(ids) == len(set(ids))
    assert all(name.strip() for name in reference.zap.values())
