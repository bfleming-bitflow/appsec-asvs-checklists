from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from tools import checklist


@pytest.fixture(scope="session")
def reference() -> checklist.Reference:
    return checklist.load_reference()


@pytest.fixture(scope="session")
def schema() -> dict[str, Any]:
    return checklist.load_schema()


@pytest.fixture(scope="session")
def checklist_paths() -> list[Path]:
    paths = checklist.default_checklists()
    assert paths, "no checklist sources found under checklists/"
    return paths


@pytest.fixture()
def minimal_checklist() -> dict[str, Any]:
    """A small, valid document used as the base for negative tests."""
    data = {
        "schema_version": 1,
        "stack": {
            "id": "example",
            "name": "Example",
            "prefix": "EX",
            "scope": "Synthetic checklist used only by the test suite.",
        },
        "standards": {"asvs": "5.0.0", "api_top10": "2023"},
        "sections": [
            {
                "id": "authentication",
                "code": "AUTHN",
                "title": "Authentication",
                "items": [
                    {
                        "id": "EX-AUTHN-001",
                        "title": "Minimum password length",
                        "asvs": "V6.2.1",
                        "level": 1,
                        "api_top10": ["API2:2023"],
                        "summary": "Passwords must be at least eight characters long.",
                        "verification": "Submit a seven character password and expect a rejection.",
                        "evidence": "Request and response pair for the rejected password.",
                        "zap": [10010],
                    }
                ],
            }
        ],
    }
    return copy.deepcopy(data)
