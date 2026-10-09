# Contributing

Contributions that correct, clarify or extend the checklists are welcome. This document describes
what a change needs before it can be merged.

## Ground rules

- Every item maps to a real ASVS 5.0.0 requirement at its official level. Check the identifier
  and level against the official ASVS text, not against secondary sources; ASVS 4.0.3 identifiers
  differ.
- Verification steps must be specific to the framework: name the API, configuration key,
  middleware or package, and state the versions where behaviour differs.
- Claims about default behaviour must be verifiable in framework source or official
  documentation. Include the reference in the pull request description.
- Keep summaries as paraphrases. Do not copy ASVS requirement text into the checklists.
- Evidence must never require collecting secrets or personal data.

## Adding or changing an item

1. Edit the stack file in `checklists/`. Append new items to the end of their section with the
   next unused sequence number; never reuse a retired identifier.
2. If you reference a new ZAP rule, add it to `reference/zap-alerts.yml` after confirming its
   identifier and name at `https://www.zaproxy.org/docs/alerts/<id>/`.
3. Run `make render` and commit the regenerated files in `docs/checklists/`.
4. Run `make check`.
5. Add an entry to `CHANGELOG.md` under "Unreleased".

## Adding a stack

Create `checklists/<stack-id>.yml` with a unique stack `id` and `prefix`, reuse the existing
section identifiers and codes where they apply, and cover at least the core requirements listed
in `tests/test_checklists.py::test_stacks_cover_the_same_core_requirements`. Add the stack to the
tables in `README.md`.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(laravel): ...`,
`fix(node): ...`, `docs: ...`, `build: ...`, `test: ...`. Reference item identifiers in the body
when a change affects specific items.

## Licensing of contributions

By contributing, you agree that checklist content is licensed under CC BY-SA 4.0 and code under
the MIT License, as described in `README.md`.
