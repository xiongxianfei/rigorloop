# Boundary-First Proof Modeling Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/rigorloop-workflow.md
Additional reviewed artifact: specs/skill-contract.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: BFP-SR1, BFP-SR2, BFP-SR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Open blockers: BFP-SR1, BFP-SR2, BFP-SR3
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: boundary-model version, trace records, and release-baseline fixtures are not yet deterministic

## Findings

## Finding BFP-SR1

Finding ID: BFP-SR1
Severity: major
Location: `specs/rigorloop-workflow.md` R28, R28l, R28n
Evidence: The amendment requires feature-spec and test-spec version parity and prospective activation, but it does not define the literal artifact marker, allowed values before and after activation, or the activation release identity that determines whether an initiative is grandfathered.
Required outcome: Define one exact version marker and closed values for feature specs and test specs, deterministic pre-activation and post-activation behavior, and a durable activation-release identity in the capability report.
Safe resolution path: Require `Boundary model version: legacy | v1` in both artifacts, bind matching test specs to the same value, define `legacy` eligibility, and record the activating release tag and report identity when `v1` becomes public.
needs-decision rationale: none

## Finding BFP-SR2

Finding ID: BFP-SR2
Severity: major
Location: `specs/rigorloop-workflow.md` R28b through R28f
Evidence: The clauses name required concepts but do not close the minimum row shapes for core entries, extensions, examples, interactions, and test-spec mappings. A spec or validator author could choose incompatible fields while still claiming conformance.
Required outcome: Define exact minimum fields, conditional fields, stable-ID grammar, uniqueness, and referential-integrity rules for every boundary and proof record.
Safe resolution path: Add closed Markdown record schemas for core entries, extension entries, example declarations, selected interactions, and test-spec proof mappings; require unique IDs and reject orphan or duplicate references.
needs-decision rationale: none

## Finding BFP-SR3

Finding ID: BFP-SR3
Severity: major
Location: `specs/rigorloop-workflow.md` R28n-R28p and `specs/skill-contract.md` R56o-R56q
Evidence: The incident corpus is specified as categories with “at least one” fixture and the capability report has named fields but no stable fixture IDs, durable path, closed result vocabulary, activation identity, or deterministic aggregate rule.
Required outcome: Freeze the first-release fixture identities, report location, result vocabulary, per-fixture fields, aggregate calculation, and activation record so test-spec and implementation do not choose the release gate.
Safe resolution path: Define eight stable fixture IDs, store one versioned capability report under this change root, use `pass | fail | not-run` for checks and fixtures, compute `overall_result` rather than accepting an assertion, and prohibit activation unless every required record is `pass`.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | block |
| observability | concern |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |
