# M1 preservation inventories

## Result

- Milestone: M1
- Status: implementation-complete; review required
- Canonical skill packages changed: no
- Rule ledger: `pr-rule-disposition.yaml`
- Literal ledger: `pr-literal-compatibility.yaml`
- Verification-basis ledger: `verify-basis-disposition.yaml`
- Scenario fixtures: `fixtures/pr-simplification-scenarios.json`
- Baseline: `evidence/profile-size-baseline.md`

## Ownership decision

The inventories assign universal intent, external-operation safety, remote classification, hosted-CI truthfulness, stops, claims, and results to `skills/pr/SKILL.md`; governed lifecycle aggregation to the conditional reference; normalized branch-readiness basis production to `verify`; and repeated PR-body structure to the asset. Legacy prose- or command-only verification evidence is classified as preparation-only.

## Validation

The standard-library validator checks non-empty unique ledgers, closed dispositions, all seven verification-basis fields, every closed-vocabulary unknown fixture, all required scenario families, operation-result consistency, and the exact LF-normalized baseline identity.

Observed on 2026-08-16:

- `python docs/changes/2026-08-16-pr-skill-simplification/fixtures/validate-pr-simplification.py` — passed; validated 24 rules, 25 literals, seven basis fields, and 18 scenarios.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-pr-skill-simplification/change.yaml` — passed.
- `git diff --check` — passed.
