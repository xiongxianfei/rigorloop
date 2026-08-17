# M1 Preservation Inventories

## Result

- Milestone: M1
- Status: implementation-complete; code review required
- Canonical learn package changed: no
- Rule ledger: `learn-rule-disposition.yaml`
- Literal ledger: `learn-literal-compatibility.yaml`
- Scenario and caller fixture: `fixtures/learn-simplification-scenarios.yaml`
- Baseline: `evidence/profile-size-baseline.md`
- Architecture trigger result: none present; M2 may be considered only after clean M1 code review

## Closed inventories

The rule ledger assigns 28 behavior clusters to the universal skill, the conditional session reference, destination owners, change-local evidence, or existing validation. The literal ledger classifies 24 compatibility-sensitive operations, paths, phase names, classifications, route values, and resource verbs. Unknown rule owners, rule dispositions, literal classes, literal dispositions, operations, classifications, confirmation values, completion kinds, and settlements have explicit failing fixtures.

The caller inventory binds both supported operations and repository trigger guidance to exact current paths and identifying phrases and finds no assessment-only caller. Six legacy artifact-model surfaces retain mandatory owner-produced results while replacing direct learn destination writes with a stable route and exact backlink. Twenty-eight deterministic scenarios cover operation, trigger closeout, unique paths, interruption, retry, evidence, confirmation, topics, stable routes, owner results, history, resources, authority, compact results, and architecture escalation.

## R46 architecture gate

The required behavior is implementable with ordinary Markdown sessions, one conditional skill reference, deterministic unique paths, fail-closed interruption, and explicit route backlinks. M1 found no need for transaction-grade phase recovery, a new persistent route or session schema owner, polling or coordination, external integration, or new cross-owner mutation authority.

If implementation later requires any listed trigger, work stops before canonical mutation and returns to architecture assessment. The canonical `skills/learn/` package remained byte-identical during M1.

## Baseline

The flat canonical skill contains 1,712 Unicode whitespace-separated words and 12,375 UTF-8 bytes after LF normalization, with SHA-256 `ce64e3aa8d13dee458b7491078050feab86e0b0f1f36d452eec1497561184b0f`. LR0 and LR1 share this baseline.

## Validation

- `python scripts/test-skill-validator.py LearnSkillSimplificationLedgerTests` — passed; five tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-16-learn-skill-simplification/change.yaml` — passed.
- `git diff --check` — passed.

## Unaffected surfaces

- `skills/learn/SKILL.md`: unchanged in M1 because canonical mutation belongs to M2.
- `specs/learn-artifact-model.md` and its test spec: unchanged in M1 because prospective writer alignment belongs to M2.
- Generated and installed packages: unchanged because canonical package generation belongs to M2 and parity proof to M3.

## Handoff

M1 is ready for independent code review. This evidence does not claim clean review, milestone closeout, M2 authorization, verification, or branch readiness.
