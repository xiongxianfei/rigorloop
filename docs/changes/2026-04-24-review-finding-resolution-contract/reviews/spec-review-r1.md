# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: `specs/review-finding-resolution-contract.md`
Status: changes-requested

## Scope

This is the first-pass spec review record for the updated review finding resolution contract. Treat this file as append-only review history; record decisions and fixes in `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`.

## Summary

Verdict: changes-requested.

The spec captures the intended first-pass review timing and re-review rule, but three contract points still require guessing before architecture, test-spec, or implementation can safely proceed.

## Findings

### SR1: Final closeout state is still ambiguous

Finding ID: SR1

Severity: major

Evidence: `R6f` says a final disposition value alone is not final closeout when closeout status is `open` or required records are missing. `R6g` then allows closeout status `closed` or "an explicitly allowed deferred final state," but the spec does not define the allowed closeout status vocabulary or what a deferred final state is.

Required outcome: The spec must define the exact closeout status values and the conditions under which each final disposition satisfies closeout.

Suggested resolution: Replace `R6g` with wording such as: "Before `verify`, `explain-change`, or `pr`, every material finding MUST have `Closeout status: closed` and a final disposition. `deferred` is closed only when `R7b` is satisfied. `partially-accepted` is closed only when `R7c` and `R7d` are satisfied. `needs-decision` and `Closeout status: open` always block."

### SR2: Late repair behavior contradicts first-pass timing unless reconstructed records are defined

Finding ID: SR2

Severity: major

Evidence: `R2m` requires the first-pass detailed review file before any review-driven fix is made. The error behavior later says that if fixes begin before the first-pass record exists, the workflow state can be repaired by recording the first-pass review before continuing. Without a reconstructed-record rule, contributors can create a late record that appears to satisfy the before-fix timing requirement.

Required outcome: The spec must define whether late repair is allowed and, if allowed, how it is labeled and constrained.

Suggested resolution: Add a rule such as: "If a first-pass review record was missed before fixes began, contributors MUST create a reconstructed first-pass review record from the original review output before any further review-driven fixes, mark it as reconstructed after fixes began, and preserve the original review evidence. If the original review output cannot be reconstructed, the workflow MUST stop for authorized owner decision."

### SR3: The review-log parseable form remains undefined

Finding ID: SR3

Severity: major

Evidence: `R3f` requires `review-log.md` to use a parseable Review ID entry, and edge case 18 says prose mentions do not count unless they use the documented parseable form. The spec does not document the minimum accepted form.

Required outcome: The spec must define the contributor-visible ledger entry shape well enough that tests and architecture can validate exact-once Review ID references without guessing.

Suggested resolution: Add a v1 rule such as: "For v1, each review-log ledger entry MUST contain exactly one `Review ID: <id>` line. Incidental prose mentions of Review IDs MUST NOT count as ledger references. Table-based ledger forms are out of scope unless a later approved change adds them."

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | concern | `SR1`, `SR2`, and `SR3` have multiple valid interpretations. |
| Normative language | pass | The spec uses normative language consistently. |
| Completeness | concern | Late repair and final closeout semantics need completion. |
| Testability | concern | Closeout and review-log tests would need to infer missing exact values. |
| Examples | pass | New examples cover the intended timing behavior. |
| Compatibility | pass | Historical artifact migration and generated adapters are covered. |
| Observability | pass | Validator and review artifact visibility are defined. |
| Security/privacy | pass | Secret and network boundaries are covered. |
| Non-goals | pass | Semantic review-quality automation remains excluded. |
| Acceptance criteria | concern | Acceptance depends on closeout and ledger semantics that need tightening. |

## Readiness

Immediate next repository stage: `spec`.

Eventual `test-spec` readiness: not-ready.

Stop condition: revise `specs/review-finding-resolution-contract.md` to address `SR1`, `SR2`, and `SR3`, then rerun `spec-review`.
