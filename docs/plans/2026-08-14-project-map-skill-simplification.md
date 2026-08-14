# Project-Map Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `project-map` package without weakening current-state evidence, freshness, command truthfulness, root/area consistency, downstream reliance safety, or customer-project portability. The work first freezes semantic and literal ownership, then separates universal orientation policy from maintenance and coordination procedure, and finally proves procedural-profile reduction and package parity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-14-project-map-skill-simplification.md`
- Spec: `specs/project-map.md`
- Architecture: `docs/architecture/system/architecture.md`
- Test spec: pending revision at `specs/project-map.test.md`

## Context and orientation

`skills/project-map/` is the only authored package source. The current package contains `SKILL.md` and `assets/project-map-skeleton.md`; the change adds `references/map-maintenance-and-area-coordination.md` while retaining the existing skeleton as the only structural asset.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical structure, resource mapping, closed vocabulary, and focused behavior checks. Adapter generation and validation scripts own generated, archived, and temporary installed-tree parity. Existing owners are extended only where focused `project-map` coverage is absent.

Semantic-rule, literal-compatibility, static-scenario, and measurement artifacts are change-local evidence. They do not become a new validator family, selector input, runtime journey, or permanent size gate.

## Non-goals

- Change current-state evidence meanings, freshness statuses, command authority, area split criteria, map structure, downstream reliance boundaries, or workflow stage order.
- Add another structural asset, a runtime mapping engine, target-agent evaluation, tokenizer dependency, or permanent simplicity validator.
- Change `change.yaml` schema, lifecycle ownership, adapter roots, package transformation, publication behavior, or project-map artifact authority.
- Rewrite historical maps, hand-edit generated adapters, or optimize another skill.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R1-R84, R112-R117; BND-INPUT-001, BND-COMPAT-001, BND-ENV-001; INT-001, INT-004, INT-005 | M1 preservation inventories, static scenarios, literal classification, and baseline measurements |
| R6-R11, R85-R111; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001-INT-004 | M2 universal skill, conditional reference, structural asset, operation/assembly behavior, and area transaction |
| R81, R85, R101, R112-R117; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004, INT-005 | M3 profile measurement, semantic preservation, and generated/archive/installed package proof |
| R72-R84, R116-R117 | M4 final holistic review, explanation, verification, and PR-boundary evidence after implementation |

## Milestones

### M1. Freeze project-map rule, literal, and scenario ownership

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, compatibility-sensitive literal, duplicate cluster, and required scenario before moving procedure.
- Requirements: R1-R84, R112-R117; BND-INPUT-001; BND-COMPAT-001; BND-ENV-001; INT-001; INT-004; INT-005.
- Architecture decisions: existing mapped-resource package, project-map container, and generated-package parity architecture.
- Files/components likely touched:
  - `docs/changes/2026-08-14-project-map-skill-simplification/project-map-rule-disposition.yaml`
  - `docs/changes/2026-08-14-project-map-skill-simplification/project-map-literal-compatibility.yaml`
  - `docs/changes/2026-08-14-project-map-skill-simplification/fixtures/`
  - `docs/changes/2026-08-14-project-map-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved proposal, specification, architecture, and formal reviews
  - complete current `skills/project-map/` package and exact literal consumers
- Tests and proof:
  - static scenarios for target-state operation selection, each scope, PMA0/PMA1 loading, late coordination, missing resources, dirty baselines, refresh correction, audit isolation, and area transaction recovery
  - unknown disposition and literal-classification fixtures that fail before consistency checks
  - LF-normalized baseline words, bytes, load order, resource identities, duplicate clusters, and representative output assembly
- Implementation steps:
  - inventory significant rules with stable IDs, sources, behavior, governing requirements, applicable profiles, disposition, destination, and preservation proof
  - inventory exact-string consumers separately as normative, parser/package, incidental-test, obsolete, or historical fixture
  - serialize ledgers and fixtures as JSON-compatible YAML and prove closed vocabulary, required fields, and unknown-value failure deterministically
  - record current `SKILL.md`, PMA0-equivalent, PMA1-equivalent, skeleton, representative output, and total package measurements
- Validation commands:
  - run the exact M1 ledger and fixture proof defined in the test specification
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`
  - independently inspect ledger coverage against the complete current skill and literal consumers
- Expected observable result: every current rule, literal, duplicate cluster, and required scenario has one closed treatment before canonical package prose moves.
- Completion criteria: all M1 artifacts validate, unknown values fail first, and no canonical project-map resource has changed.
- Required evidence: `docs/changes/2026-08-14-project-map-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence and its complete-coverage claim.
- Optional commit boundary: `M1: freeze project-map rule and literal ownership`
- Risks:
  - similar passages may encode distinct evidence or reliance behavior
  - incidental assertions may be mistaken for public literal contracts
- Rollback/recovery:
  - revert M1 evidence only; the canonical package remains unchanged

### M2. Separate universal mapping policy from maintenance and coordination

- Milestone kind: implementation
- Goal: Make `SKILL.md` shorter and self-sufficient for simple root creation, move detailed maintenance and coordination into one reference, and preserve one structural owner.
- Requirements: R6-R11, R85-R111; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001; INT-001-INT-004.
- Architecture decisions: `PMA0-simple-root-create`, `PMA1-maintenance-or-coordinated`, one mapped conditional reference, one existing structural asset, and root-registration-last area commit.
- Files/components likely touched:
  - `skills/project-map/SKILL.md`
  - `skills/project-map/references/map-maintenance-and-area-coordination.md`
  - `skills/project-map/assets/project-map-skeleton.md`
  - `scripts/test-skill-validator.py`
  - directly coupled literal consumers classified by M1
- Dependencies:
  - M1 evidence and code review are closed
- Tests and proof:
  - create/refresh/audit target-state matrix and no implicit reclassification
  - seven-surface coordination preflight, late PMA1 load, required-resource failure, and forbidden reference loads
  - root and area scope, area split floor, registration and parent relationships, overlap ownership, and contradiction stops
  - area creation prerequisite, bound identities, write order, commit point, idempotent success, exact missing-registration completion, and every conflict stop
  - new `Operation` and `Map scope` output plus legacy mapping and ambiguous legacy-area rejection
  - skeleton sole structural ownership and absence of unfilled placeholders
- Implementation steps:
  - add failing focused assertions to existing skill validation before changing package text
  - consolidate universal repetition according to the rule ledger while keeping evidence, freshness, authority, stops, claims, preflight, and trigger rules inline
  - create the conditional reference with exact refresh, audit, coordination, transaction, retry, and recovery procedure
  - update the skeleton only where structural ownership requires it and keep policy out
  - migrate real literal consumers atomically and update incidental assertions rather than preserving accidental prose
- Validation commands:
  - `python scripts/validate-skills.py skills/project-map/SKILL.md`
  - `python scripts/test-skill-validator.py ProjectMapSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: simple root creation remains complete from a shorter universal contract, maintenance and coordination load only when required, and area writes fail closed under exact transaction identity.
- Completion criteria: focused and broad skill tests pass, resource mapping is valid, every universal rule remains available, and the skeleton remains the only structural asset.
- Required evidence: `docs/changes/2026-08-14-project-map-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the canonical package, directly coupled validators, and architecture/spec fidelity.
- Optional commit boundary: `M2: simplify project-map package paths`
- Risks:
  - a universal evidence or stop rule could move behind conditional loading
  - transaction prose could permit adoption of a stale or unrelated area file
  - structural deduplication could remove a required map section or result field
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions together, then regenerate derived output

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove both procedural assemblies shrink, semantics remain complete, and mapped resources retain parity without a target-agent runtime.
- Requirements: R81, R85, R101, R112-R117; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004; INT-005.
- Architecture decisions: reuse existing Gate A and Gate B validation; no new validator family or package transformation.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `project-map`
  - existing adapter fixtures only where direct coverage is absent
  - `docs/changes/2026-08-14-project-map-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-14-project-map-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-14-project-map-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 implementation and code review are closed
- Tests and proof:
  - all supported generated, archived, and temporary installed targets contain the conditional reference and skeleton at required paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail package proof
  - PMA0 and PMA1 measurements count each LF-normalized unique procedural resource once in documented order
  - semantic review traces every rule and literal disposition to the final package
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `project-map` selection is absent
  - generate supported packages in a temporary directory and validate archive and clean-install resource parity
  - report before and after `SKILL.md`, PMA0, PMA1, each resource, representative output, total package, duplicate clusters, and mapped-resource counts
  - explain total-package change, require both procedural assemblies to shrink, and omit token counts unless an existing pinned implementation supports the exact assembly
  - independently review the complete package against both M1 ledgers and all requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "project-map"], check=True)""")'`
  - `python scripts/validate-skills.py skills/project-map/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/project-map.md`
- Expected observable result: PMA0 and PMA1 shrink, semantics remain complete, and every supported package carries byte-identical mapped resources without target-agent execution.
- Completion criteria: measurements, semantic review, canonical validation, generated build, archive, and clean-install parity pass with no unexplained procedural-profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof under the owning change root.
- Review handoff: independent `code-review` of M3 evidence and the final canonical/derived package chain.
- Optional commit boundary: `M3: prove project-map simplification`
- Risks:
  - generic adapter tests may pass without selecting `project-map`
  - main-file reduction may hide PMA1 or total-package growth
  - a mixed package may retain the old four-mode or inline ownership contract
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close any findings, explain the change, verify branch readiness, and prepare the PR handoff after all implementation milestones close.
- Requirements: R72-R84, R116-R117.
- Architecture decisions: none.
- Files/components likely touched:
  - final review records under the owning change root
  - `docs/changes/2026-08-14-project-map-skill-simplification/explain-change.md`
  - `docs/changes/2026-08-14-project-map-skill-simplification/verify-report.md`
- Dependencies:
  - M1-M3 implementation and code reviews are closed and required review resolution is closed
- Tests and proof:
  - final holistic diff review across milestones
  - exact plan and test-spec validation commands
  - requirement, boundary, architecture, package, generated-output, and branch-state coherence
- Implementation steps:
  - run final holistic `code-review`
  - resolve and rereview any material findings
  - record durable rationale with `explain-change`
  - run final `verify`; route to `pr` only under separate authority after readiness passes
- Validation commands:
  - use the complete approved test-spec command ledger
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports the truthful PR handoff state.
- Completion criteria: final holistic review is clean, explanations are current, verification is recorded, and no lifecycle blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate valid authority.
- Optional commit boundary: `closeout: verify project-map simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier package proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat holistic closeout

## Validation plan

- M1 change-local ledger and fixture proof validates closed values, required fields, unique IDs, exact scenario inventory, and unknown-value-first behavior using a standard-library command specified in the test spec.
- `python scripts/validate-skills.py skills/project-map/SKILL.md` validates normalized structure, resource-map syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py ProjectMapSkillSimplificationTests` provides focused package, operation, transaction, structure, and failure behavior proof.
- `python scripts/test-skill-validator.py` provides broad skill-contract regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check` prove generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py` proves adapter generation, archive, resource, and clean-install behavior.
- Temporary adapter build plus `validate-adapters.py --clean-install-smoke --skill project-map` proves direct all-target archive and installed-tree parity.
- `python scripts/validate-boundary-first.py --check --path specs/project-map.md` proves final feature-to-proof coverage after the matching test spec is revised.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-14-project-map-skill-simplification/change.yaml` validates lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-14-project-map-skill-simplification` validates formal review structure.
- Independent semantic review checks universal evidence completeness, conditional ownership, operation and assembly selection, area transaction safety, structural ownership, stops, claims, compatibility, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides a universal evidence, authority, stop, or claim rule.
  - Recovery: M1 rule ownership, PMA0 scenarios, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: coordination preflight falsely selects PMA0.
  - Recovery: prove all seven known surfaces, ambiguity behavior, and late loading before accepting package edits.
- Risk: area creation leaves an orphan or overwrites a changed root.
  - Recovery: bind complete identities, validate area first, register last, and accept retry only for exact matching partial state.
- Risk: relocation is reported as deletion or a misleading size win.
  - Recovery: report PMA0, PMA1, representative output, and complete package words and bytes separately.
- Risk: a generated or installed target omits the new reference.
  - Recovery: block acceptance on direct archive and clean-installed `project-map` selection, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved specification and architecture, clean formal reviews, and closed finding resolution.
- Existing boundary-first resources, published-skill resource architecture, project-map artifact contract, and generated package pipeline.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved matching test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-14 | Use three implementation milestones plus lifecycle closeout. | Preservation, package mutation, and derived-package proof have independent review and rollback boundaries. | One large rewrite; many tiny prose milestones. |
| 2026-08-14 | Freeze semantic and literal inventories before canonical edits. | Behavior preservation and exact-string compatibility are distinct contracts. | Preserve every asserted phrase; infer preservation after editing. |
| 2026-08-14 | Implement operation selection, progressive loading, and area recovery together. | They form one package classification and transaction contract and must remain internally consistent. | Split the reference across milestones; permit partial package semantics. |
| 2026-08-14 | Keep the existing skeleton as the sole structural asset. | The contract needs one layout owner and no additional repeated result structure. | Add a result asset; retain inline output templates. |
| 2026-08-14 | Extend existing validators only and measure loaded plus total content. | Durable invariants already have owners, while simplification evidence is change-local. | New validator family; main-file-only metric; target-runtime journey. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec revision and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
