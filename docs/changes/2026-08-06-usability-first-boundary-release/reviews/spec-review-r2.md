# Spec Review R2: Usability-First Boundary-First v0.4.0 Release

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex independent spec-review peer
Target: specs/usability-first-boundary-release.md
Review date: 2026-08-06
Status: changes-requested
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: UBR-SR2-001, UBR-SR2-002
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#spec-review-r2`
- Open blockers: UBR-SR2-001, UBR-SR2-002
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Make declarative activation snapshot-only or name an observable transition authority, and replace or unmistakably label the synthetic journey interfaces before architecture assessment.

## Findings

## Finding UBR-SR2-001

Finding ID: UBR-SR2-001
Severity: blocking
Location: UBR-R006, UBR-R007; State and invariants lines 143-145; Error and boundary behavior line 159; BND-STATE-001
Evidence: The revision correctly makes local activation a declarative checked-tree claim and explicitly rejects baseline reachability and transition-history proof. It nevertheless declares `active -> pending` unsupported and places that illegal transition in BND-STATE-001, while both coherent pending and coherent active snapshots pass local validation. Without a history or another named state authority, the validator cannot distinguish an initial pending snapshot from a reverted active snapshot. The same ambiguity affects “recorded reviewed pending-tree baseline”: pending stores `-`, and the spec does not identify the observable input that authorizes the one-time baseline recorded in the active snapshot.
Required outcome: Use one internally consistent activation model whose valid and invalid states can be observed and tested without inventing hidden history or authority.
Safe resolution path: Keep the thin declarative model. Treat `pending` and `active` as independently valid checked-tree snapshots, remove the unobservable `active -> pending` prohibition and transition language from state and BND-STATE-001, and state that activation preparation takes the exact reviewed pending-tree revision as an explicit input and records that revision plus its derived inventory in the active snapshot. Public immutability remains owned by the routine release tag and does not need a local state transition rule.
needs-decision rationale: none; the proposal selects tree-local declarative state and rejects Git publication choreography.

## Finding UBR-SR2-002

Finding ID: UBR-SR2-002
Severity: minor
Location: Examples E1 through E3; AC-UBR-001, AC-UBR-002; glossary
Evidence: E1 introduces a plausible `render --format` CLI, and E2/E3 introduce other plausible interfaces, then only later explain that they are fixture-only and not RigorLoop behavior. The user's immediate question about how to use `--format` demonstrates that the examples can be read as shipped commands. Their semantic inclusion/exclusion oracles are now adequate, but their identity is not sufficiently clear for a user-facing feature contract.
Required outcome: Preserve the concrete semantic journey oracles while making it impossible to mistake fixture inputs for supported RigorLoop interfaces.
Safe resolution path: Prefer existing RigorLoop surfaces: use tree-local `validate-boundary-first.py --check` for the specification journey, the activation-record loader for inspection, and the candidate-removal/retained-release diff for code review. Alternatively, label every synthetic interface in its example title and first line as `fixture-only hypothetical` and define that term before the examples. Do not add output-length metrics or more scenarios.
needs-decision rationale: none; either wording path preserves the approved test strategy, and existing surfaces are the clearest option.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | Snapshot validation and an unobservable transition prohibition conflict. |
| normative language | pass | The custom-experiment cleanup and routine-release preservation now use stable, direct `MUST` requirements. |
| completeness | concern | The reviewed baseline must be an explicit activation-preparation input. |
| testability | block | `active -> pending` cannot be distinguished without an authority the spec intentionally removed. |
| examples | concern | Semantic oracles are concrete, but synthetic interfaces can be mistaken for shipped commands. |
| compatibility | pass | The standing activation subjects now have exact retained/replaced dispositions. |
| observability | concern | The current snapshot is observable; the prohibited historical transition is not. |
| security/privacy | pass | Local validation and committed evidence remain credential-free and privacy bounded. |
| non-goals | pass | No custom publisher, extra release mode, or brittle prose checker was reintroduced. |
| acceptance criteria | block | AC-UBR-004 cannot prove the claimed illegal transition under the declared no-history model. |

## Prior finding reconciliation

- `UBR-SR1-001`: substantially addressed by the exact field and standing-contract tables; the remaining snapshot/transition contradiction is recorded as `UBR-SR2-001`.
- `UBR-SR1-002`: the semantic journey oracle is addressed; the newly observed user-facing fixture-identity ambiguity is recorded as `UBR-SR2-002`.
- `UBR-SR1-003`: resolved. UBR-R013 now owns the closed cleanup inventory and explicitly preserves the routine release mechanism.

## Exact wording direction

- Describe `pending` and `active` as valid snapshots, not a locally enforced state machine; remove `active -> pending` from BND-STATE-001.
- Make the exact reviewed pending-tree revision an explicit activation-preparation input that becomes provenance in the active snapshot.
- Replace E1 through E3 with existing RigorLoop surfaces, or label each interface as fixture-only before its first command-like token.
- Keep UBR-R012, UBR-R013, the eight-surface cleanup table, and the routine release acceptance criteria unchanged.

## Recommendation

Changes requested.
The release simplification and exact custom-experiment cleanup are now sound, but the remaining state contradiction would force architecture or tests to recreate the history mechanism the proposal rejects.

This direct review is isolated and does not start spec revision, architecture, planning, test specification, implementation, or release work.
