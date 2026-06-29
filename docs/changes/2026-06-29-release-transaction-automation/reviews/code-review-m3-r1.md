# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: M3 R1
Reviewer: Codex code-review skill
Target: M3 commit `1c494c68`
Reviewed artifact: M3 commit `1c494c68`
Reviewed milestone: M3. `prepare-release` pending artifact generation
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M3-F1
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m3-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: material finding requires review-resolution before M4
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: CR-RTA-M3-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m3-r1
- Reviewed milestone: M3. `prepare-release` pending artifact generation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CR-RTA-M3-F1
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `1c494c68`.
- Review surface: `scripts/release_transaction.py`, `scripts/prepare-release.py`, `scripts/test-release-transaction.py`, active plan M3 state, change metadata, and recorded validation evidence.
- Tracked governing branch state: approved proposal, approved spec, approved architecture/ADR, approved test spec, active plan, change metadata, closed M1, closed M2, and M3 implementation are tracked at `1c494c68`.
- Governing spec: `specs/release-transaction-automation.md` requirements `R8`-`R17`, `R43`, `R44`; acceptance criteria `AC2`-`AC5`, `AC18`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T005` through `RTA-T010`.
- Plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M3.
- Validation evidence inspected: M3 plan validation notes for `python scripts/test-release-transaction.py`, `python scripts/prepare-release.py --help`, Python compilation, selector manual-routing result, change metadata validation, lifecycle explicit-path validation, review artifact validation, and whitespace validation.
- Validation spot checks run during review: `python scripts/test-release-transaction.py`, `python scripts/prepare-release.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py`, `git diff --check --`, and a temporary-repository mutation proof for invalid pending evidence.

## Diff Summary

M3 adds a fixture-safe `prepare-release` implementation and CLI wrapper. The generator reads the active routine release profile, plans package metadata, package README examples, bundled release metadata, pending `release.yaml`, release notes generated regions, pending `npm-publication.md`, adapter artifact report placeholders, and current-version fixture data. The tests cover idempotency, exact touched paths, release-note narrative preservation, historical release evidence immutability, check mode, CLI check mode, and no external action reporting.

## Findings

### CR-RTA-M3-F1: Pending evidence validation can accept malformed target evidence

Finding ID: CR-RTA-M3-F1
Severity: major
Status: open
Location: `scripts/release_transaction.py:260`
Evidence: The approved spec requires pending evidence to use placeholders only where pre-publication validation explicitly permits them at `specs/release-transaction-automation.md:97`, and the approved test spec requires a negative unpermitted-placeholder proof at `specs/release-transaction-automation.test.md:403` and invalid pending evidence rejection at `specs/release-transaction-automation.test.md:438` through `specs/release-transaction-automation.test.md:444`. M3 adds `validate_pending_release_artifacts`, but the npm evidence check searches for required fragments across the whole file at `scripts/release_transaction.py:260` through `scripts/release_transaction.py:275`; it does not bind those checks to each target row or parse the generated YAML block. During review, a temporary generated fixture was mutated so the first target's YAML and table result changed from `pending-publication` to `published`; `validate_pending_release_artifacts("v0.3.5", root=<tmp>)` still returned `[]` because other targets still contained the required `result: "pending-publication"` fragment. The M3 tests only assert the generated happy path at `scripts/test-release-transaction.py:397` through `scripts/test-release-transaction.py:405`; they do not include the required negative pending-evidence fixture.
Required outcome: Add direct M3 proof that invalid pending evidence fails pre-publication validation, and strengthen the validator enough that target-specific malformed pending values cannot pass because another target contains a valid fragment.
Safe resolution path: Add pending evidence negative fixtures or temporary-repository mutations for at least an unpermitted result value and the `npx -y` command shape; parse or structurally inspect the generated pending YAML/table by target instead of relying on global substring presence; assert diagnostics name the invalid pending evidence field or target; rerun `python scripts/test-release-transaction.py`, M3 lifecycle validation, and return M3 to code review.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | CR-RTA-M3-F1 shows `R17` is not enforced by the current pre-publication validation helper. |
| Test coverage | block | The happy-path generated evidence test passes, but the approved negative pending-evidence proof from `RTA-T006` and `RTA-T010` is absent. |
| Edge cases | block | A malformed target result can pass if another target still contains the expected result fragment. |
| Error handling | concern | Pending evidence diagnostics are fragment-based and not target-specific enough for invalid placeholder failures. |
| Architecture boundaries | pass | M3 keeps release generation local and does not introduce preflight, closeout, CI, publication, or full-gate behavior. |
| Compatibility | pass | Historical release evidence is preserved in the fixture, and no generated test logic is introduced. |
| Security/privacy | pass | No secrets, credentials, network calls, publication actions, tags, pushes, or live registry reads appear in the reviewed code. |
| Derived artifact currency | pass-with-findings | Generated pending artifacts are deterministic, but invalid pending evidence can currently evade the M3 validation helper. |
| Unrelated changes | pass | The reviewed M3 diff is scoped to `prepare-release` generation, tests, and lifecycle evidence. |
| Validation evidence | concern | Focused tests pass, but they do not include the required invalid pending-evidence proof. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

The review did not attempt to fix or rerun the implementation after recording the finding. M4-M6 remain unimplemented and unreviewed. The selector still has known manual-routing behavior for release transaction scripts, which is separate from the M3 blocker.

## Validation

- `python scripts/test-release-transaction.py` passed during review: 28 tests.
- `python scripts/prepare-release.py --help` passed.
- `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py` passed.
- `git diff --check --` passed.
- Temporary mutation proof: changing one generated target's pending result to `published` still produced `[]` from `validate_pending_release_artifacts`, confirming CR-RTA-M3-F1.

## Recommended Next Stage

Enter `review-resolution` for `CR-RTA-M3-F1`, apply the targeted M3 pending-evidence validation and negative proof fixes, rerun M3 validation, return M3 to `review-requested`, and rerun `code-review M3`.
