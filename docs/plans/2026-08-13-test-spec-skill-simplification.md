# Test-Spec Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `test-spec` package without weakening proof design, governed authoring, boundary-first behavior, structural composition, or lifecycle ownership. The work first freezes semantic and literal ownership, then separates universal proof policy from governed authoring procedure, and finally proves loaded-profile reduction and package parity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-13-test-spec-skill-simplification.md`
- Spec: `specs/test-spec-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-13-test-spec-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/test-spec-skill-simplification.test.md`

## Context and orientation

`skills/test-spec/` is the only authored package source. The current package contains `SKILL.md`, two required boundary references, and five structural assets. The change adds `references/governed-test-spec-authoring.md`, preserves both boundary references and their initial-loading contract, and retains exactly the five existing assets.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical structure, resource mapping, closed vocabulary, structural composition, and focused behavior checks. `scripts/adapter_distribution.py`, adapter generation and validation commands, and `scripts/test-adapter-distribution.py` own generated, archived, and temporary installed-tree proof. Existing owners are extended only where focused `test-spec` coverage is absent.

Semantic-rule, literal-compatibility, static-scenario, and measurement artifacts are change-local evidence. They do not become a new validator family, selector input, runtime journey, or permanent size gate.

## Non-goals

- Change proof rigor, boundary-first activation, validation-command ownership, milestone proof timing, optional Manual QA behavior, review authority, implementation authorization, claim boundaries, or workflow stage order.
- Add a sixth asset, a manual-proof contract, a runtime engine, a target-agent evaluation, a tokenizer dependency, or permanent simplicity validation.
- Change `change.yaml` schema, lifecycle states, stage ownership, adapter roots, package transformation, or publication behavior.
- Rewrite historical test specs, hand-edit generated adapters, or optimize another skill.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R52-R61; BND-INPUT-001, BND-COMPAT-001, BND-ENV-001; INT-004-INT-005 | M1 preservation inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R51, R54-R56; BND-INPUT-001, BND-STATE-001, BND-STATE-002, BND-AUTH-001, BND-AUTH-002, BND-COMPOSE-001, BND-COMPOSE-002, BND-TEMPORAL-001, BND-RECOVERY-001, BND-RECOVERY-002; INT-001-INT-004 | M2 universal skill, governed reference, structural assets, transaction behavior, and focused validation |
| R57-R62; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004-INT-005 | M3 loaded-profile measurement, semantic preservation, and generated/archive/installed proof |
| R38-R42, R55-R56 | M4 final holistic review, explanation, verification, and PR-boundary evidence after implementation |

## Milestones

### M1. Freeze test-spec rule, literal, and scenario ownership

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal and establish deterministic scenarios before moving procedure or structure.
- Requirements: R52-R61; BND-INPUT-001; BND-COMPAT-001; BND-ENV-001; INT-004-INT-005.
- Architecture decisions: architecture-not-required; existing published-skill package and stage-owned lifecycle architecture.
- Files/components likely touched:
  - `docs/changes/2026-08-13-test-spec-skill-simplification/test-spec-rule-disposition.yaml`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/test-spec-literal-compatibility.yaml`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/fixtures/`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec, approved spec review, and recorded architecture assessment
  - complete current `skills/test-spec/` package and exact literal consumers
- Tests and proof:
  - static scenarios for both profiles, candidate validation, creation interruption, stale restart, revision, settlement boundaries, structural composition, resource failures, and automated/manual/hybrid proof
  - unknown disposition and literal-classification fixtures that fail before consistency checks
  - LF-normalized baseline words, bytes, load order, resource identities, duplicate clusters, and representative asset assemblies
- Implementation steps:
  - inventory significant rules with stable IDs, sources, behavior, requirements, profiles, disposition, destination, and preservation proof
  - inventory exact-string consumers separately as normative, parser/package, incidental-test, obsolete, or historical fixture
  - serialize ledgers and fixtures as JSON-compatible YAML and prove closed vocabulary and required fields deterministically
  - record current `SKILL.md`, TSA0, TSA1-equivalent baseline, asset assemblies, each resource, and total package measurements
- Validation commands:
  - run the exact M1 ledger and fixture proof defined in the test specification
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`
  - independently inspect ledger coverage against the complete current skill and literal consumers
- Expected observable result: every current rule, literal, duplicate cluster, and required scenario has one closed treatment before canonical skill prose moves.
- Completion criteria: all M1 artifacts validate, unknown values fail first, and no canonical skill resource has changed.
- Required evidence: `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence and its complete-coverage claim.
- Optional commit boundary: `M1: freeze test-spec rule and literal ownership`
- Risks:
  - similar passages may encode distinct proof or lifecycle behavior
  - incidental assertions may be mistaken for public literal contracts
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged

### M2. Separate universal proof policy from governed authoring

- Milestone kind: implementation
- Goal: Make `SKILL.md` shorter and portable, put exact governed creation/restart/revision procedure in one mapped reference, and make each existing asset the sole owner of its structural shape.
- Requirements: R1-R51, R54-R56; BND-INPUT-001; BND-STATE-001; BND-STATE-002; BND-AUTH-001; BND-AUTH-002; BND-COMPOSE-001; BND-COMPOSE-002; BND-TEMPORAL-001; BND-RECOVERY-001; BND-RECOVERY-002; INT-001-INT-004.
- Architecture decisions: reuse current reference/asset classes, raw-byte package parity, and stage-owned test-spec entry mutation.
- Files/components likely touched:
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec/references/governed-test-spec-authoring.md`
  - `skills/test-spec/assets/test-spec-skeleton.md`
  - `skills/test-spec/assets/test-case.md`
  - `skills/test-spec/assets/coverage-map-row.md`
  - `skills/test-spec/assets/validation-command-row.md`
  - `skills/test-spec/assets/milestone-proof-row.md`
  - `scripts/test-skill-validator.py`
  - directly coupled literal consumers classified by M1
- Dependencies:
  - M1 evidence and code review are closed
- Tests and proof:
  - exact TSA0 and TSA1 resource maps, trigger and forbidden-load cases, and missing/mixed resource stops
  - entry-first creation and every interrupted exact retry state
  - same-entry stale restart, partial-byte treatment, terminal-state and duplicate-path rejection, and no-reliance authority
  - every legal and illegal revision state, prior/new identity binding, historical evidence, and fresh review requirement
  - peer and workflow settlement isolation and forbidden writes
  - full creation and bounded structural revision with no duplicate bodies, insertion markers, or placeholders
  - automated proof without manual procedure and current manual/hybrid evidence without a new contract or asset
- Implementation steps:
  - add failing focused assertions to existing skill validation before changing package text
  - consolidate universal repetition according to the semantic ledger while retaining all universal proof, stop, claim, and trigger rules inline
  - create the governed reference with exact candidate validation, operations, write sets, retry identities, stops, and handoff boundaries
  - update structural assets atomically so the skeleton owns the frame and smaller assets own repeated bodies
  - migrate real literal consumers atomically and update incidental assertions rather than preserving accidental prose
- Validation commands:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/test-skill-validator.py TestSpecSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: portable proof design remains complete from a shorter universal contract, governed transactions fail closed under exact authority, and one asset owns each repeated structure.
- Completion criteria: all focused and broad skill tests pass, resource mapping is valid, no universal rule is hidden, and no new manual-proof structure exists.
- Required evidence: `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the complete canonical M2 package and directly coupled validator changes.
- Optional commit boundary: `M2: simplify test-spec package paths`
- Risks:
  - a universal proof rule could move behind governed loading
  - restart or revision could cross workflow or peer-review ownership
  - structural deduplication could remove an output field
- Rollback/recovery:
  - restore the prior complete canonical package and focused assertions together, then regenerate derived output

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove loaded-profile reduction, semantic preservation, and canonical-through-installed resource integrity without a target-agent runtime.
- Requirements: R57-R62; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004-INT-005.
- Architecture decisions: reuse existing Gate A and Gate B validation; no new validator family or package transformation.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `test-spec`
  - existing adapter fixtures only where direct coverage is absent
  - `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 implementation and code review are closed
- Tests and proof:
  - all supported generated, archived, and temporary installed targets contain the governed reference, both boundary references, and five assets at required paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail package proof
  - TSA0, TSA1, full-create, and bounded-revision measurements count each LF-normalized unique resource once in documented order
  - semantic review traces every rule and literal disposition to the final package
- Implementation steps:
  - extend only existing adapter-distribution proof where direct `test-spec` selection is absent
  - generate supported packages in a temporary directory and validate archive and clean-install resource parity
  - report before and after `SKILL.md`, TSA0, TSA1, each reference, each asset, representative assemblies, total package, duplicate clusters, and mapped-resource counts
  - explain any total-package growth, require both procedural profiles to shrink, and omit token counts unless an existing pinned implementation supports the exact assembly
  - independently review the complete package against both M1 ledgers and all 62 requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "test-spec"], check=True)""")'`
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/test-spec-skill-simplification.md`
- Expected observable result: both procedural profiles shrink, semantics remain complete, and every supported package carries byte-identical mapped resources without target-agent execution.
- Completion criteria: measurements, semantic review, canonical validation, generated build, archive, and clean-install parity all pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof under the owning change root.
- Review handoff: independent `code-review` of M3 evidence and the final canonical/derived package chain.
- Optional commit boundary: `M3: prove test-spec simplification`
- Risks:
  - generic adapter tests may pass without selecting `test-spec`
  - main-file reduction may hide governed-profile or total-package growth
  - a mixed package may retain old structural ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close any findings, explain the change, verify branch readiness, and prepare the PR handoff after every implementation milestone is closed.
- Requirements: R38-R42, R55-R56.
- Architecture decisions: none.
- Files/components likely touched:
  - final review records under the owning change root
  - `docs/changes/2026-08-13-test-spec-skill-simplification/explain-change.md`
  - `docs/changes/2026-08-13-test-spec-skill-simplification/verify-report.md`
- Dependencies:
  - M1-M3 implementation and code reviews are closed and required review resolution is closed
- Tests and proof:
  - final holistic diff review across milestones
  - exact plan and test-spec validation commands
  - requirement, boundary, artifact, generated-output, and branch-state coherence
- Implementation steps:
  - run final holistic `code-review`
  - resolve and rereview any material findings
  - record durable rationale with `explain-change`
  - run final `verify`; route to `pr` only if branch readiness passes
- Validation commands:
  - use the complete approved test-spec command ledger
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: all implementation evidence is coherent and final verification reports the truthful PR handoff state.
- Completion criteria: final holistic review is clean, explanations are current, verification is recorded, and no open lifecycle blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate valid authority.
- Optional commit boundary: `closeout: verify test-spec simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier package proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat holistic closeout

## Validation plan

- M1 change-local ledger and fixture proof: validate closed values, required fields, unique IDs, exact scenario inventory, and unknown-value-first behavior using a standard-library command specified in the test spec.
- `python scripts/validate-skills.py skills/test-spec/SKILL.md`: normalized structure, resource-map syntax, containment, placeholders, and narrow claim checks.
- `python scripts/test-skill-validator.py TestSpecSkillSimplificationTests`: focused package, transaction, structure, and failure behavior.
- `python scripts/test-skill-validator.py`: broad skill-contract regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary adapter build plus `validate-adapters.py --clean-install-smoke --skill test-spec`: direct all-target archive and installed-tree proof.
- `python scripts/validate-boundary-first.py --check --path specs/test-spec-skill-simplification.md`: final boundary-to-proof coverage after the matching test spec exists.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-13-test-spec-skill-simplification`: formal review structure.
- Independent semantic review: package ownership, universal proof completeness, governed transaction boundaries, asset composition, optional manual verification, stops, claims, compatibility, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides a universal proof, stop, or claim rule.
  - Recovery: the M1 rule ledger, portable scenarios, focused assertions, and semantic review block the move; restore the prior package atomically.
- Risk: same-entry restart or revision acquires broader lifecycle authority than the current contract permits.
  - Recovery: validate exact write sets and forbidden fields and stop on any reliance or identity mismatch.
- Risk: structural deduplication creates a partial or malformed test specification.
  - Recovery: composition fixtures require every heading, repeated body, and placeholder rule before rollout.
- Risk: relocation is reported as deletion or a misleading size win.
  - Recovery: report both loaded profiles, representative asset assemblies, and complete package words and bytes.
- Risk: a generated or installed target omits the new reference.
  - Recovery: block acceptance on direct archive and clean-installed `test-spec` selection, then regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved specification, clean formal reviews, closed finding resolution, and recorded `architecture-not-required` assessment.
- Existing boundary-first projections, published-skill resource architecture, stage-owned lifecycle contract, and test-spec proof contract.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved matching test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-13 | Use three implementation milestones plus lifecycle closeout. | Preservation, package mutation, and derived-package proof have independent review and rollback boundaries. | One large rewrite; many tiny prose milestones. |
| 2026-08-13 | Freeze semantic and literal inventories before canonical edits. | Behavior preservation and exact-string compatibility are distinct contracts. | Preserve every asserted phrase; infer preservation after editing. |
| 2026-08-13 | Implement creation, same-entry restart, and revision in one governed-reference milestone. | They share one authority and retry boundary and must remain internally consistent. | Separate references or cross-milestone partial transaction procedure. |
| 2026-08-13 | Keep optional manual verification in existing structures. | The approved proof contract forbids a new manual-proof contract and asset. | Sixth asset; conditional manual-proof group. |
| 2026-08-13 | Extend existing validators only and measure loaded plus total content. | Durable invariants already have owners, while simplification evidence is change-local. | New validator family; main-file-only metric; target-runtime journey. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
