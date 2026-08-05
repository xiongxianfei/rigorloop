# Specification Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: independent Codex spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.md`
Target revision: `e756a6d67263ef7e7df42ae288f1090fcf77476a`
Status: changes-requested
Material findings: BFA-SR3-001, BFA-SR3-002
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: workflow-owned after recording and resolution

## Result

- Skill: spec-review
- Review status: changes-requested
- Recording status: recorded
- Recording blocker: none
- Open blockers: BFA-SR3-001, BFA-SR3-002
- Immediate next stage: spec revision
- Stop condition: publication-readiness authority and formal ownership must be
  corrected and rereviewed before architecture amendment.

The `R -> C ... H` model is realizable and resolves the self-reference in
`BFA-M1-R3-001`. A result can name existing producer `R`, immediate child `C`
can persist it, and publication readiness can derive current `H` independently.

## Material Findings

### Finding BFA-SR3-001

Finding ID: BFA-SR3-001
Severity: blocking
Location: BFA-R007, BFA-R017 through BFA-R022; E3 and E4; AC-BFA-007 through AC-BFA-009
Evidence: Candidate mode must reject an existing local `v0.4.0` tag, but
BFA-R018 creates that tag before asking to revalidate undefined "candidate
invariants" at `H`. The requirement does not distinguish persisted `R/C`
authority, freshly derived `H` authority, or phase-specific local and remote tag
checks. A literal candidate rerun must fail after the local tag is created.
Required outcome: Define a named publication-readiness contract at live `H`
that does not rerun pre-tag candidate mode and explicitly separates fresh and
persisted authorities.
Safe resolution path: Publication readiness verifies stored `R/C` provenance;
proves `C` lies in live `H`; freshly recomputes `P/B/T`, rollback, bundle, and
`T..H` drift; requires local `v0.4.0 -> T`, remote tag absence, and remote main
still at `P`; and binds derived `H` as the publication target.
needs-decision rationale: none; the phase ordering determines the safe contract.

### Finding BFA-SR3-002

Finding ID: BFA-SR3-002
Severity: major
Location: boundary applicability record; BND-AUTH-001; INT-002; E4 ownership
Evidence: BND-AUTH-001 and INT-002 add BFA-R017, but the identity-authority
applicability row omits BFA-R017 and E4 still maps only BFA-R014 through
BFA-R016 despite now illustrating `R/C` evidence provenance.
Required outcome: Give candidate-evidence provenance consistent normative and
example ownership throughout the boundary record.
Safe resolution path: Add BFA-R017 to the identity-authority applicability row
and E4's governing requirements, preserving its ownership in BND-AUTH-001 and
INT-002 and later updating the proof map.
needs-decision rationale: none; this is a traceability correction.

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | block |
| completeness | concern |
| testability | block |
| examples | concern |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Evidence Challenge

- `python scripts/validate-boundary-first.py --path specs/boundary-first-v1-v0-3-7-activation-release.md` passed.
- `git diff --check bd79b1e0..e756a6d6 -- specs/boundary-first-v1-v0-3-7-activation-release.md` passed.
- The proposal and downstream ADR, architecture, plan, test spec, and code still
  contain the former candidate-output model; they are expected downstream
  amendments after this specification settles.

## Prior Finding Reconciliation

- `BFA-M1-R3-001`: conceptually resolved by distinct `R`, `C`, and `H` identities.
- `BFA-SR1-001` through `BFA-SR1-004`: remain resolved.
- Open M1 implementation findings remain implementation/proof debt and do not
  block selection of the corrected identity model.

## Recommendation

Revise the publication-readiness phase and boundary ownership, then perform
spec-review R4 before changing architecture.
