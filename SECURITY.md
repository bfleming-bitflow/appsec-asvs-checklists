# Security policy

## Scope

This repository contains documentation and a small Python tool that processes local YAML files.
It does not run as a service and handles no credentials or user data.

Reports are welcome for:

- vulnerabilities in `tools/checklist.py` or the CI workflow (for example unsafe YAML loading or
  workflow injection);
- checklist guidance that is technically wrong in a way that would lead a reviewer to accept an
  insecure implementation.

Vulnerabilities in Laravel, Node.js, Express, NestJS or third-party packages should be reported
to those projects directly.

## Reporting

Use GitHub private vulnerability reporting ("Report a vulnerability" under the Security tab) so
that the report is not public. Include the affected file and item identifier, the expected and
actual behaviour, and references that support the correction.

Incorrect guidance that is not exploitable can be reported as a regular issue.

## Response

Reports are acknowledged within five business days. Confirmed issues are fixed in the next
release and recorded in `CHANGELOG.md`, with credit if the reporter wishes.
