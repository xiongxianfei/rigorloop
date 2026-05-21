# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `fc6c82b`
Status: changes-requested

## Review inputs

- Review surface: commit `fc6c82b` (`M1: audit script output baseline`).
- Governing artifacts: `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, and `docs/plans/2026-05-21-script-output-optimization.md`.
- M1 implementation evidence: `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md` and `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`.
- Validation evidence recorded in the active plan and change metadata for M1.

## Diff summary

M1 added the change-local script-output audit and baseline behavior-preservation matrix. The reviewed commit also contains the previously approved lifecycle artifacts for proposal, spec, architecture, plan, test-spec, and their review records. No production script code changed in M1.

## Findings

### SRO-M1-CR1: Selected test-set baseline proof is count-only

Finding ID: SRO-M1-CR1
Severity: major
Location: `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md:17`

Evidence: The behavior-preservation row for `selected tests/checks` records only that `python scripts/test-select-validation.py` ran `62` tests. The approved test spec requires TSRO-010 reviewers to "Confirm the selected test/check set is represented by count/list/hash or another reviewable stable proof." The active plan also requires baseline proof entries for selected tests/checks. A count-only baseline cannot prove later that M3 preserved the same selected test set instead of running a different set of 62 tests.

Required outcome: M1 behavior-preservation evidence must include durable, reviewable baseline proof of the selected `scripts/test-select-validation.py` test/check set, not only the count.

Safe resolution path: Add an ordered list of the 62 baseline unittest identifiers, a stable hash derived from that ordered list, or another stable proof that lets M3 compare the post-change selected set against the M1 baseline. Update the `selected tests/checks` row to reference that proof and rerun the M1 artifact and metadata validation commands.

## Checklist coverage

- Spec alignment: concern. M1 follows the audit-first scope and changes no production code, but TSRO-010's selected-set proof requirement is not met.
- Test coverage/proof: concern. M1 records pass/fail and wrapper baseline evidence, but selected tests/checks are represented only by count.
- Edge cases: pass. Baseline records unsupported JSON and `NoSuchTest` failure behavior for later preservation comparison.
- Error handling: pass. Baseline failure and unsupported-argument behavior are recorded.
- Architecture boundaries: pass. M1 records evidence only and does not alter script architecture or wrapper behavior.
- Compatibility: pass. No production behavior changed in M1.
- Security/privacy: pass. The reviewed artifacts contain command and validation evidence only; no secrets or sensitive runtime values were observed.
- Derived artifact currency: pass. No generated artifacts were changed in M1.
- Unrelated changes: pass. The commit contains lifecycle artifacts for the same script-output optimization initiative and the M1 evidence.
- Validation evidence: concern. Recorded M1 validation commands are relevant, but the behavior-preservation matrix lacks the stable selected-set proof required for later comparison.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M1. Audit and baseline preservation evidence
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRO-M1-CR1`
Remaining implementation milestones: M1 resolution, M2, M3, M4 when triggered, M5
Verify readiness: not-claimed
