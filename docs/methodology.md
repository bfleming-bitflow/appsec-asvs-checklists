# Mapping methodology

This document explains how checklist items are selected, mapped and maintained.

## Unit of mapping

Each checklist item maps to exactly one primary ASVS 5.0.0 requirement (`asvs`). The item's
`level` is the minimum ASVS level of that requirement and must match the official value; this is
enforced by `tools/checklist.py validate` against `reference/asvs-5.0.0-requirements.csv`.

`related_asvs` lists requirements that the same verification steps also produce evidence for,
typically the documentation requirement that defines the policy being tested (for example
V6.1.1 for V6.3.1). A related requirement is not considered verified by the item on its own.

A requirement may appear in more than one item when it needs distinct verification steps, but
the shipped checklists currently use each primary requirement once per stack.

## Item selection

Requirements were selected when all of the following hold:

1. The requirement applies to a typical Laravel or Node.js web application or API. Requirements
   specific to other technologies (JNDI, LaTeX, memory-unsafe code, WebRTC) are out of scope.
2. The framework provides a specific mechanism, default or common pitfall that changes how the
   requirement is verified. Requirements whose verification is identical in every stack and
   purely procedural (most documentation requirements) are referenced as related requirements
   rather than as separate items.
3. A reviewer can produce concrete evidence: configuration, code location, request and response
   pairs, or test results.

## API Security Top 10 mapping

`api_top10` lists OWASP API Security Top 10 2023 risks that a failure of the item would
contribute to. The mapping is many-to-many and indicative. It is meant to help teams that report
against the API Top 10 locate relevant checks; it is not an official OWASP crosswalk.

## ZAP alert references

`zap` lists ZAP scan rules whose alerts are relevant evidence for the item. A ZAP rule is
only listed when its alert directly concerns the property being verified, for example
`10011 Cookie Without Secure Flag` for the session cookie Secure attribute. Absence of a ZAP alert
is never sufficient evidence that a requirement is met. Every referenced rule identifier is
listed, with its name, in `reference/zap-alerts.yml`.

## Writing guidance

- Summaries paraphrase the requirement. They do not reproduce the ASVS text, which remains
  authoritative and should be read before recording a result.
- Verification steps name real framework APIs, configuration keys, middleware or packages, and
  state version constraints where behaviour differs between versions.
- Default behaviour is described only when it was confirmed in framework source or official
  documentation. Where behaviour depends on a third-party package, the package is named.
- Evidence describes what a reviewer should keep, never secrets or personal data.

## Versioning

- Item identifiers (`LAR-AUTHN-001`) are stable. Removed items are not renumbered; their
  identifier is retired and noted in the changelog.
- The checklist content follows semantic versioning: a new minor version adds items or stacks,
  a new major version changes the schema or the ASVS version.
- When OWASP publishes ASVS errata, `reference/` is regenerated with
  `tools/checklist.py import-asvs` and validation flags any affected item.
