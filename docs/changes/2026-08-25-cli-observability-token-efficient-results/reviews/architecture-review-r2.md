# Architecture Review R2: Filesystem Threat-Model Correction

Review ID: architecture-review-r2
Stage: architecture-review
Round: r2
Target: ADR-20260825 filesystem correction
Reviewed artifact: `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md` at `sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e`
Reviewer: Codex independent architecture-review context
Review date: 2026-08-25
Recording status: recorded
Status: approved
Material findings: none

## Result

- Review surface: ADR
- Review status: approved
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/architecture-review-r2.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: not-required
- Settlement: exact-target-set approved
- Next stage: return correction to M2 code review

## Subject and basis

Governing spec: `specs/cli-observability-and-token-efficient-results.md` at `sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba`.

Target and identity: docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e

Prepared settlement manifest: `docs/changes/2026-08-25-cli-observability-token-efficient-results/architecture-review-settlement-r2.yaml`.

## Target dispositions

| Target ID | Kind | Disposition | Expected lifecycle result |
| --- | --- | --- | --- |
| `adr-cli-observability` | ADR | approved | accepted |

## Findings

None.

## Assessment

The correction aligns the implementation mechanism with the approved R11/R14 threat model. It retains pre-mutation no-follow validation, complete candidate publication, bounded cooperating-writer locking, and fail-safe stale-lock retention while explicitly refusing to present portable pathname checks as an atomic security boundary. The rejected native-helper alternative records the material portability and packaging tradeoff instead of concealing it. Descriptor ownership and event-sequence validation remain implementation responsibilities and are not weakened by this decision.

## Blockers and required updates

None at the architecture gate. M2 tests and evidence still require correction before implementation closeout.

## Claim limitations

This approval settles only the exact ADR correction. It does not approve implementation, test evidence, verification, branch, CI, release, or PR readiness.
