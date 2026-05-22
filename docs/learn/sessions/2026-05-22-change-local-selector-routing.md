# Learn Session: Change-Local Selector Routing

## Frame

- Date: 2026-05-22
- Status: session-recorded; durable lesson routed to topic guidance
- Trigger: contributor explicitly invoked `learn` after final verify reported `manual-routing-required` for deterministic change-local evidence files and noted this kind of selector error has happened several times.
- Trigger type: explicit contributor observation after verification blocker.
- Scope: root cause of repeated `changed change-local-unsupported path has no deterministic v1 selector check` failures; why prior lifecycle stages did not catch them; best practices for future change-local evidence artifacts.
- Session path: `docs/learn/sessions/2026-05-22-change-local-selector-routing.md`

## Evidence Reviewed

- Current verify blocker for `2026-05-22-broad-smoke-and-fixture-suite-output-compaction`:
  - `bash scripts/ci.sh --mode local --jobs 1` blocked with selector status `blocked`.
  - Blocking code: `manual-routing-required`.
  - Affected paths include `script-output-layer-audit.md`, broad-smoke command identity files, and change-metadata-validator selected-test identity files under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/`.
- `scripts/validation_selection.py`:
  - unknown changed paths produce `changed path is not classified by the v1 selector`;
  - unsupported change-local categories can produce `changed <category> path has no deterministic v1 selector check`;
  - recognized change-local lifecycle artifacts route to `artifact_lifecycle.validate`.
- `scripts/test-select-validation.py`:
  - existing tests enumerate supported change-local lifecycle filenames, including prior evidence names such as `script-output-audit.md` and `selected-tests-baseline.txt`.
- `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`:
  - M2 already recorded that local CI reported `manual-routing-required` for unsupported evidence files and worked around it with selected explicit CI plus manual patch hygiene.
- Prior similar incidents:
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/verify-report.md` records a final-verify selector gap for `baseline.md` and `generated-output-proof.md`.
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/explain-change.md` records PR CI initially blocking on deterministic change-local evidence files such as `adapter-packaging.md`, `historical-coverage.md`, and `token-cost.md`.
  - `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md` records an adjacent hosted CI selector incident for new artifact classes and release metadata.
- Prior learn topics:
  - `docs/learn/topics/evidence-preserving-compaction.md`
  - `docs/learn/topics/script-output-optimization.md`

## Exclusions

- This learn session does not itself fix selector routing.
- This session does not claim verify, branch readiness, PR readiness, hosted CI status, or lifecycle closeout.
- This session does not replace the required selector code/test fix for the current blocker.

## Prior Learnings Reviewed

- `docs/learn/topics/evidence-preserving-compaction.md` is relevant because it says compact evidence must keep preservation mechanisms explicit and testable.
- `docs/learn/topics/script-output-optimization.md` is relevant to the active change, but it covers output layers rather than CI selector routing for new evidence files.
- `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md` captures the adjacent pattern that new artifact classes need selector classification and CI command shape designed together.

## Observations

### O1: The recurring failure is caused by a closed selector taxonomy meeting open-ended change-local evidence names

The workflow allows changes to create useful, change-specific evidence files under `docs/changes/<change-id>/`. The v1 validation selector, however, is intentionally deterministic and allowlist-like: a changed path must map to a known category and check set. When a new evidence filename is created without adding selector classification and regression coverage, local or PR CI cannot infer the safe check and blocks with `manual-routing-required`.

This is a taxonomy mismatch, not a failure of artifact lifecycle validation itself. The affected files are valid evidence surfaces, but the selector does not yet know that they are change-local lifecycle artifacts.

### O2: Earlier stages often validate the artifacts explicitly, so they do not exercise the full changed-path selector contract

Proposal, spec, plan, implementation, and code-review stages commonly run explicit validation commands over known paths, such as `validate-artifact-lifecycle.py --mode explicit-paths ...` or `bash scripts/ci.sh --mode explicit --path ...`. Those commands prove the artifact content is valid, but they can bypass the local/PR selector's changed-path classification.

That is why a change can pass milestone validation and review, then fail at verify or hosted PR CI: verify is the first stage that runs the selector against the complete changed-path set instead of the hand-picked supported paths.

### O3: The active plan recorded the unsupported-path gap but treated it as a milestone workaround, not a selector-maintenance blocker

M2 recorded that `bash scripts/ci.sh --mode local --jobs 1` reported `manual-routing-required` for unsupported evidence files. It then used selected explicit CI over supported paths plus manual patch hygiene. That was enough for a milestone-local proof, but it left the branch-level local/PR selector route unresolved.

The lesson is that a `manual-routing-required` result for deterministic in-repo evidence is not merely a validation inconvenience. Before final verify or PR, it is CI-maintenance work.

### O4: Similar incidents show the pattern is repeated, not isolated

Prior changes recorded the same shape:

- new deterministic change-local proof artifacts were valid lifecycle surfaces;
- selected or explicit validation could prove them in isolation;
- local/PR selector routing blocked until `scripts/validation_selection.py` and `scripts/test-select-validation.py` learned those filenames or patterns.

The repeated failures show that the missing practice is not a single filename rule. It is an artifact-introduction rule: adding a new change-local evidence class must include its deterministic selector route.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | Topic guidance; current selector fix remains separate CI-maintenance | Contributor explicit `learn` request and repeated evidence | The pattern generalizes across multiple changes: open-ended evidence filenames need deterministic selector routing. |
| O2 | durable-lesson | durable-lesson | Topic guidance | Contributor explicit `learn` request and validation evidence | Explains why prior stage-local validation can pass while branch-level selector readiness fails. |
| O3 | process-follow-up | process-follow-up | Current active change selector fix | Current verify blocker | The active change needs code/test maintenance, not only documentation. |
| O4 | durable-lesson | durable-lesson | Topic guidance | Contributor statement that this happened several times plus prior recorded incidents | Repetition justifies durable guidance rather than a one-off note. |

Contributor confirmation status: confirmed for learn capture and guidance by explicit contributor `learn` invocation and repeated-pattern statement.

## Routing Results

- Session record created: `docs/learn/sessions/2026-05-22-change-local-selector-routing.md`.
- Durable topic guidance added: `docs/learn/topics/ci-selector-routing.md`.
- Current selector code/test fix remains owned by the active CI-maintenance work for `2026-05-22-broad-smoke-and-fixture-suite-output-compaction`.
- No workflow spec, ADR, or skill behavior change is made by this learn session.

## Root Cause

The root cause is that RigorLoop has two different extensibility models:

```text
change-local evidence:
  open-ended, change-specific filenames are allowed when they are useful proof

validation selector:
  deterministic, closed routing table from changed path to required checks
```

The repeated failure happens when a change adds a new proof artifact name but does not also teach the selector how that artifact is validated. The artifact may be lifecycle-valid, review-useful, and correctly listed in `change.yaml`, but local/PR CI still blocks because it cannot deterministically choose a check from the path alone.

## Why Earlier Stages Did Not Catch It

Earlier stages usually checked content validity, not full diff routing:

- implementation and review ran explicit lifecycle and metadata commands over known files;
- selected explicit CI used `--path` lists that often avoided unsupported evidence files;
- code review focused on whether the evidence proved the milestone contract;
- the active plan even recorded a local selector block in M2 but allowed a milestone workaround;
- final verify is where the complete changed-path set is expected to pass local/PR selector routing.

So the missing gate was not "did the evidence file validate?" It was "does every changed evidence file have a deterministic local/PR selector route?"

## Best Practices

1. Treat every new change-local evidence filename as a selector-surface addition.

If a change creates `docs/changes/<change-id>/<new-proof-name>`, decide immediately whether it is:

- a known lifecycle artifact routed to `artifact_lifecycle.validate`;
- a review artifact routed to review validation;
- a generated or release artifact with its own check;
- unsupported by design, with an explicit reason that blocks branch readiness until manually handled.

2. Add selector regression coverage when adding a new evidence class.

The fix should usually touch both:

- `scripts/validation_selection.py`;
- `scripts/test-select-validation.py`.

Do not rely only on `validate-artifact-lifecycle.py --mode explicit-paths`; that proves content validity, not changed-path routing.

3. Prefer bounded filename patterns over one-off filenames when the evidence class is recurring.

For example, identity evidence such as baseline/post-milestone command or test lists should use a documented pattern that the selector can route safely, rather than adding a new exact filename for every milestone.

4. Make `manual-routing-required` a final-readiness blocker for deterministic in-repo evidence.

It can be acceptable as an intermediate milestone limitation if recorded, but before final verify or PR it should trigger CI-maintenance unless the path is intentionally unsupported and the plan records an approved manual route.

5. During plan or test-spec, include a selector-routing row for new artifact classes.

A practical question to add to implementation planning:

```text
Will this change introduce any new docs/changes/<change-id>/ filenames?
If yes, what deterministic selector category and regression test will route them?
```

## Follow-Ups

- Current active change: fix selector routing for broad-smoke command identity files, producer selected-test identity files, and `script-output-layer-audit.md`.
- Potential later workflow improvement: add an explicit selector-routing checklist item to planning or test-spec guidance for newly named change-local evidence classes.
