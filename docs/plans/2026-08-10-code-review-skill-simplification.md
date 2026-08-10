# Code-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `code-review` package without weakening review behavior. The implementation will first account for every current rule, then refactor the common path and conditional procedure, and finally prove canonical, generated, packed, and temporary installed-tree integrity plus semantic preservation.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-10-code-review-skill-simplification.md`
- Spec: `specs/code-review-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- Test spec: pending at `specs/code-review-skill-simplification.test.md`

## Context and orientation

`skills/code-review/` is the only authored package source. The current package consists of `SKILL.md`, the mapped boundary-first reference, and two mapped structural assets. The change adds exactly one conditional automation reference while retaining all universal status, recording, stop, claim, milestone, and handoff policy inline.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical skill and mapped-resource proof. `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and `scripts/test-adapter-distribution.py` own generated, packed, archive, and temporary installed-tree proof for Codex, Claude Code, and opencode. Existing owners must be used; this plan adds no standalone simplification validator.

The rule-disposition ledger and size measurements are change-local evidence. They demonstrate this change without becoming durable product budgets or new validation systems.

## Non-goals

- Simplify another skill or change native `code-review` outcomes.
- Add target-agent execution, prompts, transcript grading, model matrices, or nondeterministic retries.
- Add a new validator family, selector, scheduler, cache, service, persistent store, or runtime component.
- Hand-edit generated adapter packages or installed runtime copies.
- Treat the 35–45 percent planning target as a normative acceptance gate.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R8-R14; BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001; INT-004 | M1 rule ledger, duplication inventory, scenario fixtures, and baseline measurements |
| R1-R7, R11-R13, R23; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-001, INT-002, INT-006 | M2 common-path and conditional-reference refactor |
| R14-R22, R25; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003, INT-005 | M3 deterministic package proof, installed-tree parity, measurements, and semantic-review handoff |
| R24 | Completed architecture assessment and approved architecture-review R2 |

## Milestones

### M1. Freeze rule ownership and acceptance fixtures

- Milestone type: implementation.
- Goal: Account for every behaviorally significant current rule and establish deterministic, fixture-based acceptance inputs before moving or deleting prose.
- Requirements: R8-R16; BND-INPUT-001; BND-AUTH-001; BND-RECOVERY-001; INT-004.
- Files/components likely touched:
  - `docs/changes/2026-08-10-code-review-skill-simplification/code-review-rule-disposition.yaml`
  - `docs/changes/2026-08-10-code-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-10-code-review-skill-simplification/evidence/skill-size-baseline.md`
- Dependencies:
  - approved spec and architecture
  - current canonical `skills/code-review/` package as the inventory baseline
- Tests to add/update:
  - seven static scenarios with required and forbidden outcomes
  - fail-closed proof for an unknown ledger disposition
  - ledger coverage for every identified duplication cluster and every current rule owner
- Implementation steps:
  - inventory current rules and clusters with stable IDs, source locations, behavior, requirements, disposition, and destination
  - create one valid static scenario fixture and one unknown-disposition negative fixture without executing a model
  - record `SKILL.md` and package line, word, token-estimate, template, resource, and duplication baselines
  - stop and route any proposed obsolete rule lacking an approved contract change to the spec owner
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`
  - run the exact `M1 change-local ledger and fixture proof` command in the Validation plan
  - independent semantic inspection of ledger coverage against the current `skills/code-review/` package
- Expected observable result: every current rule has one closed disposition and destination, every requested scenario is represented, and no package prose has yet moved.
- Commit message: `M1: freeze code-review rule ownership`
- Milestone closeout: targeted proof and implementation evidence, followed by independent code review and required resolution.
- Risks:
  - subtly different repeated passages may encode distinct behavior
  - a ledger checker could accidentally become a permanent validator
- Rollback/recovery:
  - revert the M1 evidence slice; canonical skill behavior remains unchanged

### M2. Refactor the common path and conditional automation procedure

- Milestone type: implementation.
- Goal: Make `SKILL.md` a shorter linear universal contract and move only workflow-managed automation procedure into one mapped conditional reference.
- Requirements: R1-R7, R10-R13, R23; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; INT-001; INT-002; INT-006.
- Files/components likely touched:
  - `skills/code-review/SKILL.md`
  - `skills/code-review/references/workflow-managed-automated-review.md`
  - `skills/code-review/assets/review-result-skeleton.md`
  - `skills/code-review/assets/material-finding.md`
  - `scripts/test-skill-validator.py`
- Dependencies:
  - M1 ledger and fixtures are complete and code-review approved
- Tests to add/update:
  - direct and isolated reviews retain all universal policy without loading the automation reference
  - exact `READ` mapping and exact armed load trigger
  - conditional reference contains allowed automation procedure and none of the forbidden universal policy
  - assets remain sole complete copy-and-fill structures and contain no policy
  - native status, severity, recording, milestone, and handoff vocabulary remains unchanged
- Implementation steps:
  - add failing focused assertions to the existing skill-validator regression suite
  - consolidate repeated quick-guide, evidence, claim, handoff, milestone, and inline-template clusters according to the ledger
  - create the exact conditional reference and move only the allowed procedure
  - keep the compact boundary bridge and every resource trigger inline
  - update ledger destinations and refuse any unmapped or unapproved disappearance
- Validation commands:
  - `python scripts/validate-skills.py skills/code-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: direct review is complete from a materially shorter `SKILL.md`; armed automation reads one conditional reference; assets own repeated structure only.
- Commit message: `M2: simplify code-review common path`
- Milestone closeout: focused skill proof and implementation evidence, followed by independent code review and required resolution.
- Risks:
  - compression could hide a universal stop, status, or claim rule
  - a reference or asset could become a competing policy owner
- Rollback/recovery:
  - revert `SKILL.md`, the new reference, and focused assertions as one package slice; regenerate derived output from the prior canonical package

### M3. Prove package parity and record simplification evidence

- Milestone type: implementation.
- Goal: Prove the complete package through canonical, generated, packed, and temporary installed targets and record honest before-and-after and semantic evidence.
- Requirements: R14-R22, R25; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-003; INT-005.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing clean-install selection does not directly cover `code-review`
  - existing adapter fixtures only when focused coverage is missing
  - `docs/changes/2026-08-10-code-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-10-code-review-skill-simplification/evidence/semantic-preservation-review.md`
- Dependencies:
  - M2 package refactor is complete and code-review approved
- Tests to add/update:
  - all supported targets contain the new mapped reference and both assets at identical relative paths
  - missing or stale reference bytes fail for generated, packed, and temporary installed targets
  - clean-install proof selects `code-review` and ends at filesystem identity
  - no acceptance command starts or grades a target agent
- Implementation steps:
  - extend the existing adapter-distribution owner only when its current generic resource proof cannot select `code-review`
  - generate all supported packages into a temporary output directory
  - run archive and clean-install mapped-resource parity for `code-review`
  - record after metrics separately for `SKILL.md`, conditional reference, and total package
  - independently review the complete package and ledger against R17 and record any residual percentage shortfall rationale
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `ADAPTER_OUTPUT_DIR="$(mktemp -d)"; python scripts/build-adapters.py --version 0.0.0-code-review-simplification --output-dir "$ADAPTER_OUTPUT_DIR"; python scripts/validate-adapters.py --version 0.0.0-code-review-simplification --adapter-root "$ADAPTER_OUTPUT_DIR" --clean-install-smoke --skill code-review`
  - `python scripts/validate-skills.py skills/code-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
- Expected observable result: every supported package and temporary installed tree contains identical mapped resources, measurements distinguish context reduction from maintenance footprint, and semantic review approves the package without runtime execution.
- Commit message: `M3: prove code-review package simplification`
- Milestone closeout: package and evidence proof, independent code review, and required resolution before final lifecycle closeout.
- Risks:
  - generic package tests may pass without selecting the changed skill
  - a large common-path decrease may conceal total package growth or semantic loss
- Rollback/recovery:
  - restore the prior complete canonical package and regenerate all derived targets; discard temporary package trees

## Validation plan

### M1 change-local ledger and fixture proof

The ledger and fixtures use JSON serialization, which is valid YAML, so this proof needs only the Python standard library. Validation rejects unknown dispositions before destination consistency.

```bash
python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-10-code-review-skill-simplification"); ledger=json.loads((root/"code-review-rule-disposition.yaml").read_text()); scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text()); invalid=json.loads((root/"fixtures/invalid-ledger-disposition.yaml").read_text()); allowed={"retained-inline","retained-conditional-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; required_fields={"rule_id","source_locations","behavior","disposition","destination","governing_requirements"}; required_scenarios={"direct-review","formal-recorded-review","missing-governing-authority","material-finding","clean-non-final-milestone","clean-final-milestone","workflow-managed-automated-review"}; rules=ledger["rules"]; unknown=[row["disposition"] for row in rules if row.get("disposition") not in allowed]; assert not unknown, f"unknown dispositions: {unknown}"; assert rules and all(required_fields <= row.keys() for row in rules); assert all(row["source_locations"] and row["behavior"] and row["destination"] and row["governing_requirements"] for row in rules); rows=scenarios["scenarios"]; assert {row["scenario"] for row in rows} == required_scenarios; assert all(row["required"] and row["forbidden"] for row in rows); assert invalid["disposition"] not in allowed; print(f"ledger_rules={len(rules)} scenarios={len(rows)} unknown_fixture=rejected")'
```

- `python scripts/validate-skills.py skills/code-review/SKILL.md`: canonical structure, resource mapping, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary build plus `validate-adapters.py --clean-install-smoke --skill code-review`: direct all-target packed and installed-tree proof for the changed package.
- `python scripts/validate-boundary-first.py --check`: final feature/spec proof-map and projected boundary-resource consistency after the matching test spec exists.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`: lifecycle and closed-state consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-10-code-review-skill-simplification`: formal review and finding closeout structure.
- Independent semantic review: rule ownership, direct-review completeness, conditional load trigger, stops, claims, output, handoff, and lifecycle preservation.

## Risks and recovery

- Risk: universal policy moves behind the conditional trigger.
  - Recovery: ledger and focused assertions block the move; restore the prior package atomically if discovered later.
- Risk: relocation appears as deletion or a misleading percentage win.
  - Recovery: record common-path and total-package metrics separately and require complete ledger coverage.
- Risk: one generated or installed target omits the new reference.
  - Recovery: target-specific archive and temporary installed-tree proof blocks publication; regenerate from the last complete canonical package.
- Risk: test additions recreate target-runtime certification.
  - Recovery: accept only repository-local structural, static fixture, filesystem, and independent semantic evidence.

## Dependencies

- Approved proposal, spec-review R1, architecture-review R2, and closed review resolution.
- Existing `code-review` boundary-first reference and structural assets.
- Existing skill validation, adapter generation, archive validation, and clean-install mapped-resource owners.
- Approved test spec and test-spec review before implementation starts.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-10 | Use three independently reviewable implementation milestones: ownership evidence, package refactor, and parity/evidence closeout. | Each milestone has a distinct failure and rollback boundary. | One large skill-and-package rewrite. |
| 2026-08-10 | Keep ledger and size checks change-local while extending only existing skill and adapter owners when durable proof is needed. | This proves the change without creating a permanent simplicity validator. | New simplification CLI or token-budget gate. |
| 2026-08-10 | Require temporary installed-tree parity for every supported target. | The approved spec names installed targets directly and architecture-review R1 exposed the gap. | Infer installed bytes solely from archive parity. |
| 2026-08-10 | Serialize change-local ledger and fixtures as JSON-compatible YAML and validate them with one standard-library inline command. | M1 needs concrete fail-closed proof without adding a permanent validator. | Defer the command to test-spec; add a simplification validator file. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring, test-spec review, all implementation/code-review milestones, final review, explanation, verification, and PR handoff remain.
