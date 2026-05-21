# Spec Review R1 - Script Output Optimization

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/script-output-optimization.md
Reviewed artifact: specs/script-output-optimization.md
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Review inputs

- Spec: `specs/script-output-optimization.md`
- Accepted proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Proposal review approval: `docs/changes/2026-05-21-script-output-optimization/reviews/proposal-review-r2.md`
- Prior CI wrapper contract: `specs/test-and-ci-speed-optimization.md`
- Prior CI wrapper test spec: `specs/test-and-ci-speed-optimization.test.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SRO-SR1, SRO-SR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-21-script-output-optimization/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-21-script-output-optimization/review-log.md`
- Review resolution: `docs/changes/2026-05-21-script-output-optimization/review-resolution.md`
- Open blockers: SRO-SR1, SRO-SR2
- Immediate next stage: spec revision

## Findings

### SRO-SR1 - Combined `--verbose` and `--quiet` behavior is left to implementation

Finding ID: SRO-SR1
Severity: major
Location: `specs/script-output-optimization.md` `Error and boundary behavior`
Evidence: The spec says, "`--verbose` and `--quiet` used together must be rejected with an actionable usage error or resolved by a documented precedence rule before implementation begins." This permits two incompatible behaviors and does not name the owner or artifact that chooses between them.
Required outcome: The spec must define one observable behavior for `--verbose` and `--quiet` used together before test-spec or implementation relies on it.
Safe resolution path: Add a requirement such as: "`scripts/test-select-validation.py` MUST reject combined `--verbose` and `--quiet` with a nonzero usage error that names both conflicting flags and does not run the test suite." Then add a matching edge case and acceptance criterion.

### SRO-SR2 - Quiet success wording weakens the "prints nothing" contract

Finding ID: SRO-SR2
Severity: major
Location: `specs/script-output-optimization.md` Example E4, R12, AC5
Evidence: Example E4 says stdout and stderr contain "no nonessential success output," and R12 says quiet-mode success prints "no nonessential success output." The accepted proposal and AC5 require `--quiet` success to print no success output. "Nonessential" leaves room for implementation to emit a success summary or other success text and still claim it is essential.
Required outcome: Quiet-mode success must have a single testable output contract.
Safe resolution path: Replace the vague wording with: "`--quiet` success MUST write no output to stdout or stderr." Update Example E4 and AC5 to use the same wording. If the project wants warnings or usage diagnostics to remain possible, limit that exception to non-success outcomes.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most requirements are precise, but combined verbosity flags and quiet success output need single observable contracts. |
| normative language | concern | Normative language is generally strong; R12's "nonessential" wording is too subjective. |
| completeness | concern | Normal, failure, zero-test, rerun, JSON, and CI-wrapper behavior are covered; conflicting flag behavior is incomplete. |
| testability | concern | Test-spec cannot deterministically test combined `--verbose`/`--quiet` behavior until the spec chooses one outcome. |
| examples | concern | Examples are useful, but E4 inherits the quiet-success ambiguity. |
| compatibility | pass | The spec preserves CI wrapper modes, check coverage, selected checks, and existing `--verbose` wrapper behavior. |
| observability | pass | Summary lines, failure details, behavior-preservation matrix, and CI output evidence are observable. |
| security/privacy | pass | The spec prevents new secrets, machine-local path expansion, and unnecessary environment dumps. |
| non-goals | pass | Non-goals preserve validation logic, generated output, JSON deferral, and helper-library deferral. |
| acceptance criteria | concern | AC5 should match the stricter no-output quiet-success contract, and an AC for combined flag rejection is missing. |

## Eventual test-spec readiness

not-ready

## Stop condition

Resolve SRO-SR1 and SRO-SR2 in the spec, then rerun spec-review before architecture, plan, test-spec, or implementation relies on the spec.

## Scope preservation review

Pass.

The spec preserves the accepted proposal scope: first-slice script-output audit, `scripts/test-select-validation.py` output shaping, `scripts/ci.sh` only if needed, no validation selection changes, reliable-only rerun commands, ASCII status words, zero-test safety, and JSON deferral.

## Recommendation

Request spec revision. Do not start test-spec, planning, or implementation until combined verbosity flags and quiet-success output are specified as single testable contracts.
