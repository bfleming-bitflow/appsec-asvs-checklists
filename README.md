# appsec-asvs-checklists

Verification checklists for Laravel and Node.js (Express and NestJS) applications, mapped to
[OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0) and the
[OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).

Each item ties one ASVS requirement to the framework mechanisms that implement it, the pitfalls
that commonly break it, and the evidence a reviewer should collect. The checklists are
maintained as YAML, validated against a JSON Schema and the official ASVS requirement list, and
rendered to Markdown.

## Contents

| Checklist | All levels | Level 1 only |
| --- | --- | --- |
| Laravel (11 and later) | [laravel.md](docs/checklists/laravel.md) | [laravel-l1.md](docs/checklists/laravel-l1.md) |
| Node.js (Express 4/5, NestJS 10 and later) | [node.md](docs/checklists/node.md) | [node-l1.md](docs/checklists/node-l1.md) |

The [coverage matrix](docs/checklists/coverage.md) shows which ASVS requirements each checklist
references.

## Scope and coverage

Version 0.1.0 focuses on the areas where framework-specific guidance adds the most value:

| Area | ASVS chapters | Laravel items | Node.js items |
| --- | --- | --- | --- |
| Authentication | V6, V11.4, V16.3 | 11 | 11 |
| Session management | V3.3, V7 | 10 | 11 |
| Access control | V8, V15.3, V16.3 | 8 | 8 |
| Tokens | V7.2, V9 | 5 | 5 |
| Input validation and output encoding | V1, V2, V15.3 | 13 | 13 |
| API and web service configuration | V2.4, V3.4, V4, V13.4, V15.3, V16.5 | 9 | 9 |
| Total | | 56 | 57 |

Not covered in this version: file handling (V5), OAuth and OIDC flows (V10), cryptography beyond
password storage (V11), secure communication (V12), most of configuration and data protection
(V13, V14), browser security headers other than CORS (V3.4), and WebRTC (V17). A checklist built
from this repository is therefore not a full ASVS assessment.

## Using the checklists

### In a security review

1. Choose the target level. Most internet-facing applications should aim for L2; use the L1
   checklist for an initial pass or for low-risk internal applications.
2. Work through the rendered checklist. For each item, read the official requirement text,
   follow the verification steps, and record the evidence described.
3. Record results per item identifier (for example `LAR-SESS-001: pass`, with evidence links) so
   that later reviews can be compared.

### In pull requests

Reference item identifiers in pull request descriptions or review comments when a change touches
a covered control, for example "Adds absolute session timeout (LAR-SESS-007, ASVS V7.3.2)". For
recurring reviews, copy the relevant section of the L1 checklist into the pull request template
of the reviewed repository.

### As data

The YAML sources are stable and machine-readable. They can be imported into a tracker or a
spreadsheet, or filtered by level, ASVS chapter or API Top 10 risk.

```sh
python tools/checklist.py render --max-level 2 --output-dir /tmp/checklists
```

## Repository layout

```text
checklists/          YAML sources, one file per stack (source of truth)
schema/              JSON Schema for the YAML sources
reference/           ASVS 5.0.0 requirement IDs and levels, API Top 10 2023, ZAP alert IDs
tools/checklist.py   validation, rendering and reference import
docs/checklists/     rendered Markdown (generated, committed)
docs/methodology.md  how items are selected and mapped
tests/               pytest suite
```

## Item format

```yaml
- id: LAR-SESS-001                 # <stack>-<section>-<sequence>, stable
  title: Session identifier is regenerated on authentication
  asvs: V7.2.4                     # ASVS 5.0.0 requirement, must exist
  level: 1                         # must match the official ASVS level
  related_asvs: [V7.1.1]           # optional
  api_top10: [API2:2023]           # optional
  zap: [40013]                     # optional, ZAP scan rule IDs
  summary: Paraphrase of the requirement.
  verification: Framework-specific steps.
  evidence: What to record.
```

The [mapping methodology](docs/methodology.md) describes how requirements are selected, how
levels and related requirements are used, and when a ZAP rule is referenced.

## Validation

`tools/checklist.py validate` enforces:

- conformance to `schema/checklist.schema.json` (required fields, identifier formats, no unknown
  fields);
- every `asvs` and `related_asvs` value exists in ASVS 5.0.0, and `level` matches the official
  level;
- API Top 10 identifiers exist in the 2023 edition, and ZAP rule identifiers are listed in
  `reference/zap-alerts.yml`;
- item identifiers match their stack and section, with no duplicate identifiers or titles.

## Development

Requires Python 3.11 or later.

```sh
make venv     # create .venv and install pinned development dependencies
make check    # ruff, yamllint, validation, tests, rendered output check
make render   # regenerate docs/checklists after editing checklists/*.yml
```

The same checks run in GitHub Actions on every push and pull request
([.github/workflows/ci.yml](.github/workflows/ci.yml)).

## Limitations

- The checklists support a manual review. They do not replace reading the ASVS, threat modelling
  or testing.
- Framework guidance reflects the versions named in each checklist's scope. Behaviour of
  third-party packages changes; confirm against the version in use.
- API Top 10 and ZAP references are indicative, not official crosswalks.
- Requirement summaries are paraphrases; the ASVS text is authoritative.

## Licensing

This repository uses two licenses:

| Material | License |
| --- | --- |
| Checklist content: `checklists/`, `docs/`, and `reference/` data files | [CC BY-SA 4.0](LICENSE-CONTENT) |
| Code: `tools/`, `tests/`, `schema/`, build and CI configuration | [MIT](LICENSE) |

The checklist content paraphrases and references OWASP ASVS 5.0.0 and the OWASP API Security
Top 10, both published by the OWASP Foundation under CC BY-SA 4.0. Distributing the content under
the same license keeps derived material compatible with the upstream terms. The tooling contains
no OWASP material and is MIT-licensed so it can be reused independently. See
[reference/README.md](reference/README.md) for attribution.

OWASP, ASVS and ZAP names are used to identify the referenced projects; this repository is not
affiliated with or endorsed by the OWASP Foundation or the ZAP project.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security issues in the tooling: see
[SECURITY.md](SECURITY.md).
