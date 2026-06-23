# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: working tree diff for M3. Representative Output and Preservation Evidence
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`, `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, `docs/plan.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Open blockers: none
- Next stage: implement M4
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M3. Representative Output and Preservation Evidence
- Milestone closeout: closed
- Remaining implementation milestones: M4
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: working tree diff for M3 representative output proof, cold-read proof, behavior-preservation evidence, selector evidence-class registration, regression assertions, and lifecycle state updates.
- Tracked governing branch state: approved spec `specs/project-map.md`, active test spec `specs/project-map.test.md`, active plan `docs/plans/2026-06-23-evidence-bound-incremental-project-map.md`, and M3 validation evidence recorded in the active plan and change metadata.
- Governing artifacts: M3 milestone in the active plan; `specs/project-map.md` R78-R84 plus downstream reliance R72-R77; `specs/project-map.test.md` T12-T17 and T21.
- Validation evidence: `python scripts/test-skill-validator.py -k project_map`, `python scripts/test-skill-validator.py`, `python scripts/test-select-validation.py ValidationSelectionTests.test_registered_change_evidence_patterns_and_exact_names_match_once`, change metadata validation, artifact lifecycle validation, selected CI, and whitespace validation recorded in the active plan and change metadata.
- Implementation files reviewed: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md`, `docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md`, `scripts/test-skill-validator.py`, `scripts/validation_selection.py`, and `scripts/test-select-validation.py`.

## Diff summary

M3 adds concise representative project-map excerpts covering metadata, dirty baselines, root and area maps, parent-map registration, overlap ownership, observed/inferred/unknown labels, configured-versus-executed commands, runtime and data-flow evidence types, future-intent handling, stale-map handling, wrong-at-baseline correction notes, and placeholder removal.

It adds a cold-read proof for a small repository, a monorepo or multi-service fixture, and an intentionally stale map. The behavior-preservation file now links the M3 proof artifacts and still avoids generated-adapter, verification, branch-readiness, PR-readiness, or final-closeout claims.

The validator regression suite now asserts the representative proof files contain the drift-prone M3 evidence. The selector registers `cold-read-proof.md` and `representative-project-map-outputs.md` as `project-map-output-proof` evidence so selected CI routes them through lifecycle validation instead of leaving manual-routing debt.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `representative-project-map-outputs.md` lines 20-178 covers the representative output set required by R78-R80 without adding a full artifact validator. `cold-read-proof.md` lines 18-99 covers R84's small, multi-service, and stale-map cases. |
| Test coverage | pass | `scripts/test-skill-validator.py` lines 3813-3909 asserts representative output, cold-read proof, and behavior-preservation evidence. `scripts/test-select-validation.py` lines 870-883 covers the registered proof filenames. |
| Edge cases | pass | Direct proof covers dirty baselines, inspected uncommitted paths, configured commands without success claims, executed command exit code, future intent not represented as deployed, stale paths, and wrong-at-baseline correction notes in `representative-project-map-outputs.md` lines 24-32, 50-52, 93-99, and 149-172. |
| Error handling | pass | The selector evidence class in `scripts/validation_selection.py` lines 377-384 routes deterministic project-map proof files through `artifact_lifecycle.validate`, resolving the manual-routing failure observed during implementation. |
| Architecture boundaries | pass | M3 touches representative evidence, tests, selector routing, and lifecycle state only. It does not change runtime code, generated adapter output, architecture docs, existing project maps, or the canonical `project-map` skill behavior. |
| Compatibility | pass | The proof artifacts are labeled as representative fixture excerpts, not current repository claims, at `representative-project-map-outputs.md` line 9. Existing project maps remain unmigrated, and generated adapter inclusion remains assigned to M4. |
| Security/privacy | pass | The excerpts use fictional fixture paths and no secrets. The external-boundary example records missing provider credentials as unknown rather than exposing or inventing runtime secrets. |
| Derived artifact currency | pass | M3 does not change generated assets. Selected CI ran `skills.generation_regression`; M4 still owns generated adapter inclusion proof. |
| Unrelated changes | pass | The M3 review surface is scoped to representative evidence, regression assertions, selector registration needed by the new evidence files, and lifecycle handoff state. |
| Validation evidence | pass | The active plan records M3 validation: project-map subset passed 14 tests, full skill-validator passed 228 tests, selector targeted test passed, artifact lifecycle and change metadata validation passed, selected CI passed 7 checks, and whitespace validation passed. |

## No-finding rationale

The implementation satisfies M3's proof boundary. The representative output artifact covers the named output-shape and evidence-class cases without becoming a full produced-map validator. The cold-read proof covers each required repository shape with no deferral. The regression assertions are narrow string checks over the M3 proof files, and selector registration closes the deterministic evidence-routing gap discovered during implementation.

## Residual risks

M4 still needs generated local skill and adapter inclusion proof. This review does not claim generated adapter inclusion, final verification, branch readiness, PR readiness, or final lifecycle closeout.

## Handoff

Reviewed milestone: M3. Representative Output and Preservation Evidence
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Remaining implementation milestones: M4
Next stage: implement M4
Final closeout readiness: not ready; M4, explain-change, verify, and PR handoff have not completed.

Do not claim branch readiness, PR readiness, verification, final lifecycle closeout, or full generated adapter inclusion from this review.
