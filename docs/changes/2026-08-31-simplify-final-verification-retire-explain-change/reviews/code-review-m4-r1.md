# Code Review M4 R1: V3 Package Parity and Preactivation Publication

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: M4 implementation commit `56ce590e`
Reviewed artifact: committed implementation diff `585c2bee..56ce590e`; handoff commit `9dde5933` contains review-requested state only
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-m4-r1.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M4-CR1`, `FV-M4-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M4-CR1`, `FV-M4-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M4
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5, M6
- Required review-resolution: yes
- Finding IDs: `FV-M4-CR1`, `FV-M4-CR2`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the exact committed M4 product diff against approved Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, TG-15 through TG-18, FV-R1 through FV-R3, FV-R19, FV-R22 through FV-R30, FV-R35 through FV-R38, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001, and INT-002 through INT-004. The review inspected canonical stage guidance, Verify's progressive resource profile, the semantic boundary validator, three staged adapter candidates, activation and historical manifests, tests, and the M4 evidence record.

The formal review is isolated from implementation repair. It records findings and review evidence only; Workflow owns correction routing and lifecycle mutation.

## Actual-diff summary

- Separates active v2 wording from the staged inactive v3 lifecycle across current governance and several canonical stage skills.
- Adds staged v3 adapter candidate assembly for Codex, Claude Code, and opencode, with `explain-change` removed and Verify resources retained.
- Makes boundary-proof allocation use the registered primary plan for stage-owned v2 and v3 changes.
- Adds parity and mixed-inventory tests while leaving public adapter manifests and final-verification activation preactivation unchanged.

## Material findings

## Finding FV-M4-CR1

Finding ID: FV-M4-CR1
Severity: major
Location: `skills/verify/SKILL.md:3-5,17,23,74-80,144-148`; staged Codex, Claude Code, and opencode v3 candidates generated from that canonical skill
Evidence: M4 removes `explain-change` from every staged v3 adapter inventory and adds an inactive-v3 paragraph, but the same published Verify entrypoint still unconditionally says verification runs after durable rationale, validates after `explain-change`, requires the rationale to be complete, reads an explain-change artifact, requires a current explanation for consolidated gates, and routes missing rationale back to `explain-change`. These are operative global prerequisites and handoff rules, not historical or v2-keyed text. Therefore an activated candidate would omit the only skill that can satisfy or repair Verify's stated prerequisite while Verify simultaneously says v3 has no such prerequisite. The new skill tests assert selected v3 phrases and resource names but do not reject these contradictory global clauses. This violates FV-R1 through FV-R3, FV-R24, FV-R27, FV-R28, FV-R35 through FV-R38, TG-15, TG-16, TG-18, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, INT-002, and INT-004.
Required outcome: The canonical Verify entrypoint and every staged v3 adapter candidate must contract-key all explanation prerequisites and correction handoffs: active v1/v2 may require the standalone explanation, while v3 begins after final review and applicable CI with no explanation input, emits the durable explanation only after successful verification, and emits none on failure.
Safe resolution path: Rewrite the global description, purpose, use conditions, input requirements, consolidated-gate prerequisites, and handoff routes so they are explicitly selected by lifecycle contract. Add semantic regressions that scan all prerequisite and handoff clauses in the canonical skill and each of the three generated candidates, proving v3 has no pre-Verify explanation dependency while v2 wording remains exact. Retain the existing progressive resource triggers for impact, applicability, and success-only explanation guidance.
needs-decision rationale: none; the approved v3 graph and compatibility boundary already determine the two contract-specific outcomes.

## Finding FV-M4-CR2

Finding ID: FV-M4-CR2
Severity: major
Location: `scripts/boundary_first_validation.py:322-337,1732-1820`; `scripts/validate-change-metadata.py:310-338`; `scripts/test-boundary-first-validation.py`
Evidence: `_parse_change_record` rejects duplicate keys only at indentation zero, then delegates nested mappings to `parse_yaml_mapping`, which overwrites a repeated key without error. The v2/v3 proof validator reads `artifact_states.plan` from that last-wins result and treats it as the exact authority-selected primary plan. An adversarial repository with two nested `plan` entries—first pointing to a missing plan and second to a valid plan—returned an empty issue tuple, so ambiguous authority was accepted. The same defect applies to repeated nested `kind`, `role`, or `path` keys. This contradicts the M4 evidence claim that duplicate mapping keys fail closed and violates TG-17, BND-AUTH-001, BND-COMPOSE-001, and BND-COMPAT-001.
Required outcome: Governed v2/v3 plan-proof discovery must reject duplicate keys at every mapping depth before selecting lifecycle contract, artifact state, kind, role, or path; no ordering of duplicate values may acquire authority.
Safe resolution path: Make the shared safe-YAML parser or the boundary validator detect duplicate mapping keys recursively, before last-wins normalization. Add direct regressions for duplicate `artifact_states`, duplicate `plan`, and duplicate `kind`, `role`, and `path`, including first-valid/last-valid reversals and v2/v3 cases; retain explicit malformed, unknown-contract, path-containment, and active-v2 compatibility proof.
needs-decision rationale: none; fail-closed authority parsing is already required and does not change the approved proof model.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The staged v3 Verify package retains an impossible standalone-explanation prerequisite. |
| Test coverage | block | All planned suites pass, but no test rejects the contradictory global Verify clauses or nested duplicate mapping keys. |
| Edge cases | block | Nested duplicate authority keys are accepted last-wins. |
| Error handling | block | Malformed top-level and unknown contracts fail closed, but nested duplicate mappings do not. |
| Architecture boundaries | block | Publication composition and exact plan authority are not coherent. |
| Compatibility | pass | Active v2 routing, public manifests, rollback archives, and preactivation state remain unchanged. |
| Security/privacy | pass | No credentials, external network authority, or secret-bearing output was introduced. |
| Derived artifact currency | concern | Three staged candidates are byte-consistent with canonical sources, but canonical Verify semantics are internally contradictory. |
| Unrelated changes | pass | The diff is scoped to M4 governance, skill/package composition, validators, tests, and evidence. |
| Validation evidence | concern | Planned suites pass, but direct semantic inspection and an adversarial parser probe disprove two completion claims. |

## Validation performed

- `python scripts/test-skill-validator.py` — 385 tests passed.
- `python scripts/validate-skills.py` — 21 canonical skills passed.
- `python scripts/test-build-skills.py` — 8 tests passed.
- `python scripts/build-skills.py --check` — passed.
- `python scripts/test-boundary-first-validation.py` — 68 tests passed.
- `python scripts/validate-boundary-first.py --check` — passed.
- `python scripts/test-adapter-distribution.py` — completed successfully with 156 tests passed.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` — 0 errors and 48 pre-existing warnings.
- `git diff --check 585c2bee..56ce590e` — passed.
- Reviewer nested-duplicate probe — two `artifact_states.plan` mappings were parsed last-wins and `_stage_owned_plan_proof_issues` returned `()`.
- Reviewer Verify composition trace — all three staged candidates omit `explain-change`, while their canonical Verify body retains unconditional explanation prerequisite and correction clauses.

## No automatic handoff

This review records findings before repair. There is no automatic downstream handoff, no implementation edit, no M5 start, and no Verify or PR readiness claim. Both findings have bounded corrections under the approved M4 authority.

## Handoff

- Reviewed milestone: M4
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5, M6
- Required review-resolution: yes
- Recommended next stage: Workflow records `FV-M4-CR1` and `FV-M4-CR2`, routes the correction to M4 implementation ownership, and returns the complete corrected M4 diff for Code Review M4 R2.
- Final closeout readiness: not ready; M4 has two material findings and M5-M6 remain planned.
