# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- CI and `make test` now enforce at least 80% line coverage on `tools/`.

## [0.1.0] - 2026-10-09

### Added

- Laravel checklist with 56 items and Node.js (Express and NestJS) checklist with 57 items,
  covering authentication, session management, access control, tokens, input validation and
  output encoding, and API configuration.
- Mapping to OWASP ASVS 5.0.0 requirement identifiers and levels, OWASP API Security Top 10 2023
  risks, and ZAP scan rule identifiers where applicable.
- JSON Schema for checklist sources and `tools/checklist.py` for validation, Markdown rendering
  (all levels and L1-only), coverage matrix generation and ASVS reference import.
- Vendored ASVS 5.0.0 requirement identifiers and levels for offline validation.
- Test suite and GitHub Actions workflow running lint, validation, tests and a rendered output
  check.

[Unreleased]: https://github.com/bfleming-bitflow/appsec-asvs-checklists/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/bfleming-bitflow/appsec-asvs-checklists/releases/tag/v0.1.0
