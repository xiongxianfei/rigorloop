# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/review-skill-family-consistency-parser-owned-finding-shape.md
Reviewed artifact: specs/review-skill-family-consistency-parser-owned-finding-shape.md
Review date: 2026-05-21
Status: changes-requested
Recording status: recorded

## Scope

Reviewed the draft feature spec for review-skill family consistency and parser-owned finding shape against the accepted proposal, adjacent asset specs, and the current review-artifact parser contract.

## Review inputs

- Spec: `specs/review-skill-family-consistency-parser-owned-finding-shape.md`
- Proposal: `docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md`
- Proposal review: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/reviews/proposal-review-r1.md`
- Skill contract: `specs/skill-contract.md`
- Adjacent asset specs: `specs/proposal-family-assets-progressive-disclosure.md`, `specs/spec-family-assets-progressive-disclosure.md`
- Parser contract inspected: `scripts/review_artifact_validation.py`

## Result

- Review status: changes-requested
- Material findings: RSF-SR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-log.md`
- Review resolution: `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/review-resolution.md`
- Open blockers: RSF-SR1
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: resolve RSF-SR1 before spec-review approval or downstream test planning
- Automatic downstream handoff: none; this review is isolated

## Material findings

### RSF-SR1

Finding ID: RSF-SR1
Severity: major
Location: `specs/review-skill-family-consistency-parser-owned-finding-shape.md` RSF-R20, RSF-R21, EC2, AC-RSF-010
Evidence: The spec requires representative invalid fills with non-enum `Severity:` values to fail `scripts/validate-review-artifacts.py --mode structure`. The current parser in `scripts/review_artifact_validation.py` only parses material findings from `Finding ID:` fields in `_parse_finding_records`; it does not require or validate `Severity:` values in detailed review records. Existing parser fixtures also use `Severity: major` as ordinary field text rather than enum-checked structure.
Required outcome: Align the spec with the actual validation contract. Either make non-enum severity rejection an explicit new validator behavior owned by this spec, or narrow the invalid-fill checks to failures the current review-artifact structure validator actually owns.
Safe resolution path: Revise RSF-R20, RSF-R21, EC2, and AC-RSF-010 to distinguish current parser-owned structure checks from any new severity-enum validation. If the intended behavior is to add severity-enum validation, add a requirement that explicitly changes validator behavior and names the accepted enum source per review skill. If no parser change is intended, remove non-enum `Severity:` from the structure-validation failure set and keep blank or renamed `Finding ID:` as parser-owned failure examples.

## Review dimensions

| Review dimension | Verdict | Notes |
|---|---|---|
| requirement clarity | concern | Most requirements are concrete, but RSF-R20/RSF-R21 overstate what the current structure validator owns for severity values. |
| normative language | concern | The non-enum severity `MUST fail` language is testable but currently conflicts with the stated no-parser-contract-change boundary. |
| completeness | pass | The spec covers scope, assets, parser conformance, result skeletons, generated output, rollback, follow-ons, and lifecycle evidence. |
| testability | block | RSF-R21 and AC-RSF-010 cannot pass against the current parser unless the implementation adds new severity-enum validation or the spec is narrowed. |
| examples | concern | E2 names non-enum severity as a validator failure without specifying whether that is existing parser behavior or new behavior. |
| compatibility | pass | Compatibility and migration preserve review behavior and generated-output boundaries. |
| observability | pass | Required evidence surfaces are visible and concrete. |
| security/privacy | pass | No secrets, private data, external services, or authorization behavior are introduced. |
| non-goals | pass | Non-goals correctly exclude parser accepted-label changes, references, scripts, partials, and deferred review skills. |
| acceptance criteria | concern | AC-RSF-010 inherits the severity-validation mismatch from RSF-R20/RSF-R21. |

## Scope preservation review

Pass. The spec preserves the accepted proposal scope: first-slice `code-review`, `proposal-review`, and `spec-review`; material-finding and result-skeleton assets; behavior preservation; parser-shaped defaults with validation backstop; no references, scripts, partials, parser-contract changes, or non-review expansion.

## Recommendation

Request spec revision for RSF-SR1. Do not start test-spec, architecture, plan, or implementation until the validator contract mismatch is resolved and the spec is re-reviewed.
