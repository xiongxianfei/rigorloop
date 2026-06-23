# Repository-Wide Resource Audit

## Status

Implementation evidence for M6.

## Scope

This audit covers the current canonical published skills under `skills/` after:

- M2 canonical resource-map and bounded legacy-reference validation;
- M3 architecture resource normalization;
- M4 generated and archive mapped-resource parity;
- M5 locally packed clean-install mapped-resource parity.

The audit intentionally inspects canonical authored skills only. It does not
modify generated adapter output, installed target trees, historical archives, or
runtime fallback behavior.

## Audit command

```bash
python scripts/validate-skills.py
```

Result:

```text
validated 23 skill files under /home/xiongxianfei/data/20260419-rigorloop/skills
```

The repository does not need a separate audit-mode flag for M6 because the
current canonical validator already reports resource-integrity findings as hard
validation failures with path-specific diagnostics. M6 uses that hard validator
as the audit proof, then records the repository-wide result here before
continuing enforcement.

## Current skill inventory

| Skill | Packaged resources? | Resource-integrity result |
| --- | ---: | --- |
| architecture | yes | clean |
| architecture-review | no | clean |
| bugfix | no | clean |
| ci-maintenance | yes | clean |
| code-review | yes | clean |
| constitution | no | clean |
| explain-change | no | clean |
| explore | no | clean |
| implement | no | clean |
| learn | no | clean |
| plan | yes | clean |
| plan-review | no | clean |
| pr | no | clean |
| project-map | no | clean |
| proposal | yes | clean |
| proposal-review | yes | clean |
| research | no | clean |
| spec | yes | clean |
| spec-review | yes | clean |
| test-spec | yes | clean |
| verify | no | clean |
| vision | no | clean |
| workflow | no | clean |

## Packaged-resource inventory

| Skill | Resource |
| --- | --- |
| architecture | `assets/adr-skeleton.md` |
| architecture | `assets/architecture-skeleton.md` |
| architecture | `assets/diagram-styles.mmd` |
| ci-maintenance | `assets/github-workflow-skeleton.yml` |
| ci-maintenance | `references/risk-to-check-map.md` |
| code-review | `assets/material-finding.md` |
| code-review | `assets/review-result-skeleton.md` |
| plan | `assets/current-handoff-summary.md` |
| plan | `assets/decision-log-row.md` |
| plan | `assets/milestone.md` |
| plan | `assets/plan-skeleton.md` |
| proposal | `assets/proposal-skeleton.md` |
| proposal-review | `assets/material-finding.md` |
| proposal-review | `assets/review-result-skeleton.md` |
| spec | `assets/spec-skeleton.md` |
| spec-review | `assets/material-finding.md` |
| spec-review | `assets/review-result-skeleton.md` |
| test-spec | `assets/coverage-map-row.md` |
| test-spec | `assets/test-case.md` |
| test-spec | `assets/test-spec-skeleton.md` |

All packaged resources are under approved `assets/` or `references/` classes.
No current canonical skill ships `templates/` as a packaged skill-local resource
class.

## Drift findings

| Finding class | Result | Disposition |
| --- | --- | --- |
| Missing `Resource map` for packaged resources | none found | clean |
| Mapped resource missing from canonical skill source | none found | clean |
| Mapped resource outside skill root | none found | clean |
| Mapped resource verb/class mismatch | none found | clean |
| Unmapped legacy skill-local resource-loading reference | none found | clean |
| Temporary migration exception still required | none | clean |
| Unrelated repository-wide resource drift | none found | clean |

## Enforcement decision

Repository-wide hard enforcement can remain enabled for current skills.

Rationale:

- the audit of all 23 canonical published skills is clean;
- architecture drift was resolved in M3 and the former `templates/...`
  architecture instruction now fails validation in `scripts/test-skill-validator.py`;
- new or changed skills are covered by the same validator and regression
  fixtures for mapped-resource validation and unmapped legacy-resource lint;
- no unresolved drift requires deferral or a temporary exception.

This decision does not claim final branch readiness or PR readiness. It only
closes the M6 audit/enforcement decision for code review.

## Validation evidence

M6 validation commands:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `bash scripts/ci.sh --mode explicit --path <each current skills/*/SKILL.md> --path scripts/skill_validation.py --path scripts/test-skill-validator.py`

The original plan shorthand used `--path skills`, but the v1 selector only
classifies concrete canonical skill files. The supported classified-path command
was used for the M6 CI proof.

Additional lifecycle commands are recorded in the active plan and change
metadata.
