# Code Review M3 R4: Compact semantic operation completeness

Review ID: code-review-m3-r4
Stage: code-review
Round: r4
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation and bounded CLI implementation against Design Review R9 and Delivery Review R6
Reviewed milestone: M3
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M3-CR3, CCSR-M3-CR4, CCSR-M3-CR5
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-M3-r4.md`, `review-log.md`, and `review-resolution.md`
- Open blockers: CCSR-M3-CR3, CCSR-M3-CR4, CCSR-M3-CR5
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CCSR-M3-CR3, CCSR-M3-CR4, CCSR-M3-CR5
- Recording status: recorded
- Recording blocker: none
- Review record: `reviews/code-review-M3-r4.md`
- Review log: `review-log.md`
- Review resolution: `review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M3-CR3, CCSR-M3-CR4, CCSR-M3-CR5
- Verify readiness: not-claimed

## Finding CCSR-M3-CR3

- Finding ID: CCSR-M3-CR3
- Severity: major
- Location: `packages/rigorloop/dist/lib/compact-operations.js:84`, `packages/rigorloop/dist/lib/compact-operations.js:102`, `packages/rigorloop/dist/lib/compact-operations.js:110`, `packages/rigorloop/dist/lib/compact-operations.js:181`, `packages/rigorloop/dist/lib/compact-operations.js:194`, and `packages/rigorloop/dist/lib/compact-operations.js:228`
- Evidence: `resolve-finding` replaces the whole target review but verifies only that the selected finding disappeared, so another open finding can disappear without a disposition. `upsert-decision` and evidence replacement similarly delete every coordinator reference owned by the same stable file before adding the candidate contents, without proving that unselected current decisions or evidence entries remain. The focused suite directly proves finding non-loss only for `replace-review`, not these sibling operations.
- Required outcome: Every stable-file mutation must preserve all unselected open findings, decisions, and evidence entries byte-consistently, or require an operation-specific valid disposition/removal for each omitted entry.
- Safe resolution path: Add failing multi-entry tests for each operation, compare candidate content with the prior current set before replacing references, reject omissions with stable non-loss errors, then rerun focused and package validation.
- needs-decision rationale: none; SR-06 and SR-10 through SR-15 already require non-loss.

## Finding CCSR-M3-CR4

- Finding ID: CCSR-M3-CR4
- Severity: major
- Location: `packages/rigorloop/dist/lib/compact-eligibility.js:22`, `packages/rigorloop/dist/lib/compact-eligibility.js:73`, and `packages/rigorloop/dist/lib/compact-operations.js:151`
- Evidence: The operation matrix implements only a generic main-chain `NEXT_STAGE` edge and shallow target checks. It omits the reviewed conditional Code Review and review-resolution edges; allows an existing artifact registration to change stable kind, role, path, or owner; does not bind review subjects to their target/package identities; and permits `record-verify` without proving a current approved final Code Review, no required remaining work, exact report evidence selection, and directly observed report subjects. Passing current tests does not exercise the full fourteen-operation stage/target matrix required by TG-09 through TG-13.
- Required outcome: Encode every approved operation predicate over exact stage, active work, target, current identities, findings, remaining work, review outcome, and evidence; reject every unapproved edge or stable-registration mutation; and directly test the positive and negative partitions.
- Safe resolution path: Add table-driven matrix and end-to-end tests first, implement the exact predicates and stable target derivations in the pure evaluator, and keep semantic choices in request content rather than inventing them in the CLI.
- needs-decision rationale: none; the Design R9 operation eligibility matrix fixes the required outcomes.

## Finding CCSR-M3-CR5

- Finding ID: CCSR-M3-CR5
- Severity: major
- Location: `packages/rigorloop/dist/lib/compact-operations.js:42`, `packages/rigorloop/dist/lib/compact-operations.js:305`, and `packages/rigorloop/dist/lib/compact-cli.js`
- Evidence: The evaluator proves that `expected_files` equals the adapter-supplied map and now requires referenced evidence subjects, but it does not derive and compare the only allowed input-path set. A request may add an unrelated repository path to `expected_files`; the adapter reads it and the evaluator accepts it as an input even though it is neither authoritative, affected, nor a declared evidence subject. This violates SR-26's missing/extra fail-closed rule and enlarges the supposedly bounded transaction surface.
- Required outcome: Derive the exact allowed expected-file set from the current authoritative set, operation target paths, and declared observed evidence subjects, and reject both omissions and extras before semantic evaluation.
- Safe resolution path: Add explicit extra-path, missing-subject, new-target-absence, and transient-source tests; derive the expected path set in the pure evaluator; keep content source bytes separately identity-bound and non-authoritative.
- needs-decision rationale: none; SR-22, SR-25, and SR-26 already define this boundary.

## Checklist

| Area | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Three evaluator boundaries remain weaker than SR-06, SR-10–SR-15, and SR-22–SR-26. |
| Test coverage | block | The 13-test named M3 suite does not partition all fourteen operations or sibling non-loss paths. |
| Edge cases | block | Multi-entry stable files, conditional stage edges, extra expected paths, and final Verify prerequisites are not closed. |
| Error handling | concern | Existing fail-closed schema and transaction errors are sound, but semantic omission paths can yield a valid wrong candidate. |
| Architecture boundaries | concern | The pure evaluator and adapter separation is correct; exact derived coordination remains incomplete. |
| Compatibility | pass | Legacy compact writes and migration reject and historical readers remain available. |
| Security/privacy | pass | No caller authentication claim, secret output, Git, PR, network, or diagnostic-log dependency was introduced. |
| Derived artifact currency | pass | Runtime schemas, JSON Schema, help, README, and focused tests agree on fourteen operations and the withheld writer. |
| Unrelated changes | pass | Changes remain within M3 plus the narrow legacy resolution parser regression. |
| Validation evidence | concern | Named checks pass, but they do not prove the missing semantic partitions. |

## Handoff

M3 remains under review. Route CCSR-M3-CR3, CCSR-M3-CR4, and CCSR-M3-CR5 to implementation through review-resolution, then perform a fresh holistic M3 rereview. No milestone, branch, Verify, or PR readiness is claimed.
