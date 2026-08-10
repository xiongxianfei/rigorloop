# Code-Review Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/code-review-skill-simplification.test.md`
Review date: 2026-08-10
Status: changes-requested
Material findings: CRSIM-TSR1, CRSIM-TSR2, CRSIM-TSR3, CRSIM-TSR4
Review status: changes-requested
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: CRSIM-TSR1, CRSIM-TSR2, CRSIM-TSR3, CRSIM-TSR4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-code-review-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-10-code-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-code-review-skill-simplification/review-resolution.md#test-spec-review-r1`
- Open blockers: CRSIM-TSR1, CRSIM-TSR2, CRSIM-TSR3, CRSIM-TSR4
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: requested automation target reached with material test-spec findings open

## Findings

## Finding CRSIM-TSR1

Finding ID: CRSIM-TSR1
Severity: major
Location: `specs/code-review-skill-simplification.test.md`, CMD1 and T1
Evidence: CMD1 checks the valid ledger for unknown values, but it handles the negative fixture only with `assert invalid["disposition"] not in allowed`. The invalid record never enters the same validation function or produces a fail-closed result. T1 therefore claims that the unknown fixture is rejected before consistency without executing that path.
Required outcome: One shared validation function must process valid and invalid records, return or raise the explicit unknown-value failure before required-field and destination consistency, and make the negative fixture test fail if that ordering regresses.
Safe resolution path: Keep the proof change-local and standard-library-only, but define one inline `validate_rule` or `validate_ledger` function, assert the valid ledger has no errors, and assert the invalid fixture's first error is the named unknown-disposition error. Do not add a validator file.
needs-decision rationale: none

## Finding CRSIM-TSR2

Finding ID: CRSIM-TSR2
Severity: major
Location: `specs/code-review-skill-simplification.test.md`, R11-R14 coverage, PRF-012, T11, Validation commands, and M1/M3 proof rows
Evidence: T11 depends on unspecified “change-local measurement commands” while its only Command ID is CMD1, which measures nothing. The command ledger has no owner for lines, words, estimated tokens, conditional-reference size, total package size, cluster count, inline-template count, or mapped-resource count. R14 and AC7 are marked covered without executable or exact manual proof.
Required outcome: Add stable command IDs and exact safe commands for the required before/after measurements, including the existing deterministic token estimator and repository-local line, word, package, cluster, template, and resource counts; bind their evidence to M1 and M3.
Safe resolution path: Reuse `scripts/measure-skill-tokens.py` for token estimates and exact read-only shell or standard-library commands for the other counts. Classify them as existing/configured or planned change-local evidence, define failure behavior, and update T11, PRF-012, and milestone rows.
needs-decision rationale: none

## Finding CRSIM-TSR3

Finding ID: CRSIM-TSR3
Severity: major
Location: `specs/code-review-skill-simplification.test.md`, T13, T15, and Manual procedure MP1
Evidence: Test-case `Level` is a closed enum of `unit`, `integration`, `e2e`, `smoke`, or `manual`, but T13 and T15 use `migration`, which is valid only in coverage maps. MP1 lists steps but does not explicitly name its required environment, owning stage, pass condition, or failure condition as required by the review contract.
Required outcome: Use allowed test-case levels while retaining migration coverage-map classification, and make MP1 a stable procedure with rationale, environment, owner, evidence path, exact steps, pass condition, and failure condition.
Safe resolution path: Change T13 and T15 to `integration` or `e2e` as appropriate; add a structured MP1 header before its numbered steps and keep semantic judgment limited to the approved R17 checklist.
needs-decision rationale: none

## Finding CRSIM-TSR4

Finding ID: CRSIM-TSR4
Severity: major
Location: `specs/code-review-skill-simplification.test.md`, CMD6
Evidence: CMD6 chains temporary-directory creation, adapter generation, and validation with semicolons. A generation failure does not stop validation immediately, the command returns only the final process status, and the temporary directory is never cleaned. That conflicts with its claimed failure behavior and the fixture isolation requirement.
Required outcome: The combined command must fail fast on directory, generation, or validation failure and clean only its validated temporary directory on every exit.
Safe resolution path: Use a bounded `bash -eu -o pipefail -c` command, create the directory with `mktemp -d`, validate it is non-empty and under the system temporary root before installing a cleanup trap, then run build and validation sequentially. Alternatively use a repository test owner that already provides equivalent cleanup and direct `code-review` selection.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | No test invents product behavior. |
| Requirement coverage | block | R9 ordering and R14 measurement claims are not directly proved. |
| Example coverage | pass | E1-E7 map to stable cases. |
| Negative and boundary coverage | concern | The unknown fixture is declared but not exercised through the same path. |
| Proof-level adequacy | concern | Two test-case levels are outside the closed vocabulary. |
| Milestone mapping | concern | M1/M3 measurement evidence lacks command ownership. |
| Command validity | block | CMD1 overclaims negative proof; CMD6 does not fail fast or clean up. |
| Fixture and data design | block | CMD6 leaves temporary output and can continue after failure. |
| Manual-proof boundary | block | MP1 lacks required ownership, environment, and pass/fail fields. |
| Observability | concern | Measurement and negative-ordering failures lack exact command diagnostics. |
| Determinism and isolation | concern | Most proof is deterministic; CMD6 cleanup and propagation need correction. |
| Scope and non-goals | pass | No agent-runtime or new validator family is proposed. |
| Execution economics | pass | Focused M1/M2 checks precede full M3 package proof. |
| Traceability | concern | Structural mapping is complete but four evidence links overclaim adequacy. |
| Implementation handoff | block | Implementation would need to invent proof details. |

The proof map is close, but implementation is not authorized until all four findings are revised and rereviewed.
