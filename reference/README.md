# Reference data

The files in this directory are used by `tools/checklist.py` to validate the
checklists. They are reference data, not checklist content.

| File | Content | Upstream source |
| --- | --- | --- |
| `asvs-5.0.0-requirements.csv` | Requirement identifier, minimum level, chapter and section names for all 345 requirements of ASVS 5.0.0. Requirement text is intentionally omitted. | `5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv` at tag `v5.0.0_release` of [OWASP/ASVS](https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0) |
| `api-security-top10-2023.yml` | Risk identifiers and names of the OWASP API Security Top 10, 2023 edition. | [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) |
| `zap-alerts.yml` | ZAP scan rule identifiers referenced by checklist items. | [ZAP alert details](https://www.zaproxy.org/docs/alerts/) |

## Attribution and license

`asvs-5.0.0-requirements.csv` is derived from the OWASP Application Security
Verification Standard 5.0.0, copyright the OWASP Foundation, and is
redistributed under the
[Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
license, which is the license of the upstream standard.

The OWASP API Security Top 10 is published by the OWASP Foundation under
CC BY-SA 4.0. Only risk identifiers and names are reproduced here.

## Updating

To refresh the ASVS reference after an upstream errata release, regenerate the
CSV from the official CSV export and run `make check`. Any checklist item whose
requirement was renumbered or whose level changed will fail validation.

```sh
python tools/checklist.py import-asvs path/to/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv
```
