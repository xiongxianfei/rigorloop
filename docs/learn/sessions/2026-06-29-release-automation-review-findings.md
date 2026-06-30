# Learn Session: Release Automation Review Findings

## Status

- captured
- routing pending contributor confirmation

## Frame

- Trigger: explicit maintainer invocation asking why release transaction automation produced many review findings, what the root cause was, and whether the spec and test spec were not good enough.
- Trigger type: explicit maintainer request / repeated review findings / workflow-process observation.
- Date: 2026-06-29
- Scope:
  - review finding pattern for `2026-06-29-release-transaction-automation`;
  - `test-spec-review` findings `RTA-TSR1` and `RTA-TSR2`;
  - code-review findings `CR-RTA-M1-F1` through `CR-RTA-M6-F1`;
  - whether the failures point to spec/test-spec weakness, implementation proof gaps, or review-process gaps.
- Evidence in scope:
  - `docs/changes/2026-06-29-release-transaction-automation/review-log.md`
  - `docs/changes/2026-06-29-release-transaction-automation/review-resolution.md`
  - prior learn sessions about review finding volume, test-spec review ownership, and requirement compression during review.
- Explicit exclusions:
  - no proposal, spec, test-spec, plan, workflow, skill, validator, or topic update from this learn session;
  - no claim about branch readiness, PR readiness, verification readiness, review-resolution closeout, or CI status;
  - no durable topic entry without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/sessions/2026-06-25-test-spec-review-ownership.md`
  - `docs/learn/sessions/2026-06-26-m2-test-spec-review-evidence-review-miss.md`
- Session record path: `docs/learn/sessions/2026-06-29-release-automation-review-findings.md`

## Observe

### O1 - The first upstream defect was proof-contract ambiguity, not the overall release direction

Evidence:

- `RTA-TSR1` found that the test spec deferred proof-contract details to implementation, including generated-region marker behavior, literal-audit baseline shape, timing evidence fields, and fixture layout.
- `RTA-TSR2` found that the test spec did not classify referenced commands as existing, planned, manual-only, or external/release-owned, and did not define when planned commands became required.
- Both findings were resolved before implementation by adding proof-contract details and an implementation-handoff command matrix.

Observation:

The proposal/spec direction was not the main problem. The release transaction model was strong enough to guide the work. The first weakness was that the initial test spec still left some observable proof semantics and command ownership to implementation. That made the implementation boundary too soft until `test-spec-review` forced the details into the test spec.

Practical answer:

The spec and test spec were not simply "bad." The feature contract was directionally strong, but the test spec needed more concrete proof-shape decisions before implementation could safely proceed.

### O2 - Most code-review findings were direct-proof omissions against already-approved artifacts

Evidence:

- `CR-RTA-M1-F1` required direct negative fixtures for every missing required profile field.
- `CR-RTA-M2-F1` required direct proof that a literal-audit entry missing `classification` fails.
- `CR-RTA-M2-F2` required direct proof that a surface inventory entry missing `classification` fails, and required prior profile snapshots in the inventory.
- `CR-RTA-M4-F2` required direct preflight negative tests for malformed profile, incomplete profile, and missing required local input.
- The second review for each implementation milestone was clean after these direct proofs were added.

Observation:

Several findings were not caused by missing product requirements. They were caused by first-pass implementation claiming a milestone with incomplete direct negative coverage for named edge cases. The approved artifacts named the edge cases; implementation did not turn every named case into a fixture and assertion before review.

Practical answer:

This is primarily an implementation proof-discipline issue. The prevention is a pre-review checklist: every named edge case in the plan and test spec must have a direct fixture/test, expected diagnostic, and validation result before requesting code review.

### O3 - Several findings came from helper-level proof substituting for maintainer command-path proof

Evidence:

- `CR-RTA-M4-F1` found that helper behavior could catch unauthorized literals only when `--changed-file` was explicitly passed, while the normal `python scripts/release-preflight.py <tag>` invocation could miss them.
- `CR-RTA-M5-F1` found that timing validation helper tests existed, but `scripts/validate-release.py`, the path used by `release-verify.sh`, did not call the helper.
- `CR-RTA-M6-F1` found that closeout validated a local public-evidence file but did not collect public GitHub/npm metadata or run fresh public `npx` smoke in the routine closeout path.

Observation:

The implementation repeatedly proved lower-level helpers or local fixtures while the maintainer-facing release command path remained weaker. This is the same class as requirement compression: "the helper can do it" was treated as equivalent to "the release command does it."

Practical answer:

For release tooling, command-path integration proof is mandatory. Tests must exercise the command maintainers actually run, not only helper functions.

### O4 - Trust-boundary proof was compressed into field-shape validation

Evidence:

- `CR-RTA-M6-F1` found that a local `public-evidence.yaml` could satisfy closeout even though the requirement was to collect public GitHub release metadata, npm registry metadata, tarball identity/integrity, and fresh public `npx` smoke.
- The resolution changed routine closeout to use injectable providers, with local evidence allowed only in explicit fixture mode.

Observation:

The first implementation proved that generated published evidence had the right shape, but not that the evidence came from the required public sources. In supply-chain release work, source ownership is part of the proof, not an implementation detail.

Practical answer:

Tests must prove data provenance for release evidence. A fixture may prove shape, but provider-call tests prove ownership of public evidence collection.

### O5 - One validator used global presence checks where the contract required target-bound structure

Evidence:

- `CR-RTA-M3-F1` found that pending npm-publication validation searched fragments across the whole file, so one valid target row could mask one invalid target row.
- The resolution parsed target-init smoke evidence and validated missing, duplicate, unknown, wrong-result, wrong-command, and table/YAML mismatch cases per target.

Observation:

The validator checked that required strings existed somewhere, not that each target carried the correct values. That is a validator-design miss: release evidence is structured data and must be validated by target, not by global substring presence.

Practical answer:

Release validators should parse the owned structure, derive expected rows from the release profile, and validate every row independently.

### O6 - The review loop worked, but it was acting as the first complete proof audit

Evidence:

- `review-log.md` records material first-pass findings for `test-spec-review-r1` and for M1 through M6 first reviews.
- `review-log.md` records clean follow-up reviews for `test-spec-review-r2`/`r3` and for M1 through M6 second reviews.
- `review-resolution.md` records all findings as resolved after targeted implementation corrections.

Observation:

The findings were real and review did its job. The problem is that code review became the first place where the full proof matrix, command path, and trust boundary were checked exhaustively. That is expensive and creates repeated review-resolution loops.

Practical answer:

The target is not weaker review. The target is stronger pre-review self-audit, using the same dimensions review keeps finding.

## Root Cause

The root cause was not simply that the spec and test spec were poor.

The deeper root cause was proof translation failure across three boundaries:

1. Proof-contract boundary:
   the initial test spec left some proof-shape and command-ownership decisions unresolved until `test-spec-review` forced them closed.

2. Implementation proof boundary:
   implementation repeatedly satisfied the general milestone intent but missed direct negative fixtures and diagnostics for every named edge case.

3. Integration/trust boundary:
   implementation sometimes proved helper behavior, local fixture shape, or global string presence instead of proving the maintainer command path, provider-owned public evidence collection, or target-bound structured validation.

The spec provided the destination. The improved test spec provided many edge cases. The repeated code-review findings show that implementation still needed a first-pass completeness audit before handoff.

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record only | Review-resolution `RTA-TSR1`, `RTA-TSR2` | The test spec did have initial gaps, and those were resolved before implementation. |
| O2 | process-follow-up | pending confirmation | Possible implementation checklist or implement-skill guidance for direct negative fixture completeness before code review. | Not yet confirmed | The pattern repeated across M1, M2, and M4. |
| O3 | process-follow-up | pending confirmation | Possible test-spec or code-review checklist requiring command-path proof for maintainer-facing release commands. | Not yet confirmed | The pattern repeated in M4 and M5, with related trust-boundary evidence in M6. |
| O4 | process-follow-up | pending confirmation | Possible release-proof guidance requiring provenance tests for public evidence. | Not yet confirmed | Supply-chain evidence requires source ownership, not only shape validation. |
| O5 | durable-lesson | pending confirmation | Possible validator-design topic entry about parsing structured release evidence instead of global substring checks. | Not yet confirmed | This is reusable across validators, but topic routing requires confirmation. |
| O6 | observation | observation | Session record only | Clean second reviews after targeted fixes | Review gates were effective; the preventable cost was incomplete pre-review self-audit. |

## Route

No derivative routing performed.

Contributor confirmation is unavailable for updates to workflow, skills, specs, test specs, validators, or learn topics. This session records the evidence-bound analysis and candidate follow-ups, then stops.

## Best Practices

- Turn every named edge case into a direct negative fixture and assertion before code review.
- For each negative test, assert the stable diagnostic names the file, field, target, command, or provider that failed.
- Prove the maintainer command path, not only helper functions.
- For release evidence, prove source ownership and provenance, not only Markdown/YAML field shape.
- Treat public release closeout as a provider-owned proof boundary: GitHub, npm, tarball integrity, and fresh public `npx` smoke must be collected or executed by the closeout path.
- Validate structured release evidence structurally. Avoid global substring checks for per-target, per-artifact, or per-provider contracts.
- Before code review, run a self-audit with three columns: named requirement, direct proof, command/trust boundary proof.

## No Durable Route Rationale

No topic entry or authoritative artifact update was created. The session found reusable patterns and likely follow-ups, but routing them would change implementation workflow, review guidance, skill behavior, or validator-design guidance. Those changes need contributor confirmation and an action-owning artifact rather than a learn session alone.
