# M1 Preservation Inventories

## Result

- Milestone: M1
- Status: implementation-complete; code review required
- Canonical vision package changed: no
- Rule ledger: `vision-rule-disposition.yaml`
- Literal ledger: `vision-literal-compatibility.yaml`
- Scenario fixture: `fixtures/vision-simplification-scenarios.yaml`
- Baseline: `evidence/profile-size-baseline.md`
- Architecture trigger result: none present; M2 may be considered only after clean M1 code review

## Closed inventories

The rule ledger assigns 32 behavior clusters to the universal skill, strategic reference, README reference, two structural assets, change-local evidence, or existing validation. The literal ledger classifies 32 compatibility-sensitive paths, markers, operations, classifications, assemblies, actions, results, verbs, headings, and obsolete phrases. Unknown rule owners, rule dispositions, literal classes, literal dispositions, and every one of the 11 new or changed closed vocabularies have explicit failing fixtures.

The fixture defines all six loaded assemblies as three primary and three secondary skip profiles. Thirty-four deterministic scenarios cover operations, state routing, assembly selection, late strategic loading, authority, markers, positioning, independent assets, manifests, source-first ordering, retry, resource loss, compatibility, measurement, and architecture escalation.

## Architecture gate

The required behavior remains implementable with conditional Markdown resources, structural assets, ordinary change-local Markdown authoring evidence, and deterministic repository validators. M1 found no need for a new persisted multi-file transaction schema, classification-state owner, executable README synchronizer, generated-content owner, or independent policy owner.

If implementation later requires any listed trigger, work stops before canonical package mutation and returns to architecture assessment. The canonical `skills/vision/` package remained byte-identical during M1.

## Baseline

The flat canonical skill contains 2,268 Unicode whitespace-separated words and 15,845 UTF-8 bytes after LF normalization, with SHA-256 `627a26b862d04acb001470ba0ef64138071a80e8dd67b2eccf47a41770dcb229`. VA0, VA0S, VA1, VA1S, VA2, and VA2S share this baseline.

## Validation

- `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureLedgerTests` — passed; five tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml` — passed.
- `git diff --check` — passed.

## Unaffected surfaces

- `skills/vision/SKILL.md`: unchanged in M1 because canonical mutation belongs to M2.
- `specs/vision-skill.md`: unchanged because the focused approved spec supplements its behavior without altering the consolidated contract.
- `VISION.md`, `docs/vision/strategic-positioning.md`, and README vision front-matter: unchanged because project strategy is outside this package refactor.
- Generated, archived, release-candidate, and installed packages: unchanged because canonical generation belongs to M2 and parity proof to M3.

## Handoff

M1 is ready for independent code review. This evidence does not claim clean review, milestone closeout, M2 authorization, verification, or branch readiness.
