# Verify Report: Retire the Standalone Test-Spec Stage

Verification ID: verify-r1
Stage: verify
Verifier: Codex verify
Verification date: 2026-08-31
Status: not-ready
PR readiness: not claimed

## Result

- Skill: verify
- Status: blocked
- Artifacts changed: this verify report and the verify-report pointer in `change.yaml`
- Open blockers: `RTS-VRF1`
- Next stage: Workflow must route a boundary-projection implementation correction, followed by Code Review, refreshed explanation, and Verify
- Validation: CMD-02 through CMD-16 passed; the authoritative direct PR graph failed Gate A boundary proof structure
- Readiness: not-ready

## Scope and verdict

This governed-final run assessed change `2026-08-31-retire-standalone-test-spec-stage` on branch `proposal/retire-standalone-test-spec-stage` against exact base `origin/main@7ff73122f72a863bc0ea2619988ef90b84005b1c` and workflow-handoff subject `9986a8d784e40140a2c4c3f6c1b8acbbae01d162`.

Verdict: `not-ready`.

The accepted proposal, approved Design Review `design-review-r2`, approved Delivery Review `delivery-review-r3`, five closed implementation milestones, final holistic Code Review `code-review-final-r1`, closed review resolution, and current explanation are coherent. Every change-specific M6 command from CMD-02 through CMD-16 passed, including 12-check broad smoke. Branch readiness is nevertheless blocked because the current direct PR graph detects stale boundary-first generated governance: the activation snapshot still expects two projections under the removed `skills/test-spec` package and its stored projection identity no longer matches the canonical resource graph.

Verify records this failure but does not repair it, reopen a milestone, alter review authority, or route lifecycle state. Hosted CI was not observed.

## Verification basis

```yaml
verification_basis:
  repository_identity: xiongxianfei/rigorloop
  remote_identity: https://github.com/xiongxianfei/rigorloop
  base_branch: origin/main
  base_revision: 7ff73122f72a863bc0ea2619988ef90b84005b1c
  merge_base_revision: 7ff73122f72a863bc0ea2619988ef90b84005b1c
  head_branch: proposal/retire-standalone-test-spec-stage
  verified_subject_revision: 9986a8d784e40140a2c4c3f6c1b8acbbae01d162
```

The final reviewed implementation subject is `28fbc5be6aa720082635136f6eab19cb5baaca55`, the final-review recording revision is `09cdc5312795e2ab5792141d27a7f7ef9f11cb85`, the explanation revision is `1b6dff3f061f82aad4c5662c1f32f8f048a452ec`, and the Workflow verify-handoff revision is the verified subject above.

## Blocking finding

### RTS-VRF1 — Boundary-first activation projection is stale

Result: block

Evidence: `bash scripts/ci.sh --mode pr --base 7ff73122f72a863bc0ea2619988ef90b84005b1c --head 9986a8d784e40140a2c4c3f6c1b8acbbae01d162` failed Gate A when `python scripts/validate-boundary-first.py --check` reported:

- `BFR-PROJECTION-MISSING` for `skills/test-spec/references/boundary-first-method-v1.md`;
- `BFR-PROJECTION-MISSING` for `skills/test-spec/references/boundary-first-proof-v1.md`;
- `BFR-PROJECTION-HASH` for the projection identity stored in `specs/boundary-first-activation.yaml`.

Impact: the canonical v2 skill inventory has correctly removed `skills/test-spec`, but the active boundary-first projection snapshot still requires resources under that removed package. Generated-governance currency is therefore inconsistent across the exact branch, violating RTS-R18, RTS-R19, RTS-R23, RTS-AC10, TS-012, TS-013, TG-FINAL-03, and the direct PR acceptance contract.

Owner and safe next action: Workflow should route this to a bounded implementation correction that regenerates or updates the boundary-first resource ownership and activation projection from canonical sources, proves the retired consumer is absent, and reruns `python scripts/validate-boundary-first.py --check`, the affected projection tests, direct PR validation, Code Review, Explain Change refresh, and Verify. Verify does not perform that correction automatically.

## Verification dimensions

| Dimension | Result | Evidence |
| --- | --- | --- |
| Requirements and proof map | concern | TG-FINAL-03 is not closed because one active generated-governance projection is stale; other mapped M6 proof passed. |
| Test validity | pass | Named suites executed nonzero test counts; package tests passed 310 with two intentional historical skips. |
| Architecture coherence | pass | Explicit v2 plus frozen manifest behavior remains consistent with the approved ADR and architecture. |
| Artifact lifecycle state | pass | The governed record is current at Verify, M1-M5 are closed, and M6 remains an open lifecycle-closeout milestone. |
| Review closeout | pass | Closeout validation reports 17 reviews, 10 resolved findings, 17 log entries, and no open finding. |
| Explanation currency | pass | `explain-change.md` binds the exact reviewed S → R → E tail and returns control to Workflow. |
| Change-specific validation | pass | CMD-02 through CMD-16 completed successfully, including 12 broad-smoke checks. |
| Generated-output currency | block | Boundary-first activation still names removed test-spec projections and carries a stale projection identity. |
| Direct PR graph | block | Gate A boundary proof structure failed at the exact verified subject. |
| Branch integration | pass | `git diff --check` passed and merge-tree produced conflict-free tree `aa6553f2491fbfdc4c39a69ae1375c9f37f28592`. |
| Hosted CI | unknown | No current hosted run was observed; no hosted-CI success is claimed. |
| Local worktree | concern | Existing untracked `packages/rigorloop/node_modules/` remains untouched and is unrelated baseline state. |

## Commands actually run

| Command or group | Result |
| --- | --- |
| `npm test --prefix packages/rigorloop` | passed: 312 total, 310 passed, two intentional historical skips |
| `python scripts/test-change-metadata-validator.py` | passed: 82 tests |
| `python scripts/test-artifact-lifecycle-validator.py` | passed |
| `python scripts/test-workflow-automation.py && python scripts/test-workflow-automation-policy.py && python scripts/test-workflow-automation-state.py` | passed |
| `python scripts/test-review-artifact-validator.py` | passed |
| `python scripts/test-skill-validator.py` | passed: 378 tests |
| `python scripts/test-build-skills.py && python scripts/build-skills.py --check` | passed: 8 tests and generated-skill check |
| `python scripts/test-adapter-distribution.py` | passed: 154 tests |
| `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` | passed with zero errors and 48 existing line-wrap warnings |
| `python scripts/test-lifecycle-cli-conformance.py` | passed: invalid=6, protected=10 |
| `python scripts/test-governed-lifecycle-cli-validator.py` | passed: 8 tests |
| `python scripts/validate-skills.py skills/spec/SKILL.md skills/plan/SKILL.md skills/delivery-review/SKILL.md skills/workflow/SKILL.md` | passed for all four named skills |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-31-retire-standalone-test-spec-stage` | passed: 17 reviews and 10 resolved findings |
| `python scripts/validate-change-metadata.py docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml` | passed |
| `bash scripts/ci.sh --mode broad-smoke` | passed: 12 checks in 733 seconds |
| `bash scripts/ci.sh --mode pr --base 7ff73122f72a863bc0ea2619988ef90b84005b1c --head 9986a8d784e40140a2c4c3f6c1b8acbbae01d162` | failed: Gate A boundary proof structure; three projection issues |
| `python scripts/select-validation.py --mode pr --base origin/main --head HEAD` | blocked in the legacy selector compatibility surface; current `docs/workflows.md` explicitly excludes this selector from the direct PR gate, so this is recorded as a non-authoritative concern rather than the readiness blocker |
| `git diff --check origin/main...HEAD` | passed |
| `git merge-tree --write-tree origin/main HEAD` | passed: tree `aa6553f2491fbfdc4c39a69ae1375c9f37f28592` |

## CI status, drift, and claim limits

- Local broad smoke passed, but the local direct PR graph failed. The branch cannot be called ready by averaging those results.
- Hosted CI was not queried or observed.
- This report does not claim `branch-ready`, PR-body readiness, PR-open readiness, release, publication, deployment, merge completion, lifecycle completion, or M6 closeout.
- The failed direct PR gate invalidates final readiness but does not by itself invalidate the already-recorded implementation reviews; the correction owner and subsequent Code Review must decide the exact refreshed review basis.

## Readiness

Verdict: `not-ready`.

The permitted handoff is back to Workflow for a bounded boundary-projection implementation correction. PR is not the next stage while `RTS-VRF1` remains open.
