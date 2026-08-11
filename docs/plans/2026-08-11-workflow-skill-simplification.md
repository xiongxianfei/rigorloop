# Workflow Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `workflow` package without weakening routing, lifecycle, automation, guide-authoring, or fail-safe behavior. The work first accounts for semantic rules and exact-string dependencies, then refactors the universal and conditional instruction surfaces, and finally proves assembly-specific context reduction plus canonical, generated, archived, and temporary installed package integrity.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-11-workflow-skill-simplification.md`
- Spec: `specs/workflow-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- Test spec: pending at `specs/workflow-skill-simplification.test.md`

## Context and orientation

`skills/workflow/` is the only authored package source. The current package contains `SKILL.md`, the boundary-first reference, and the workflow-guide skeleton. This change adds three conditionally loaded procedure references while retaining universal classification, source precedence, unknown-artifact behavior, lifecycle outline, isolation, stops, claims, resource triggers, and handoff policy inline.

`scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own canonical structure and mapped-resource proof. `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and `scripts/test-adapter-distribution.py` own generated, archived, and temporary installed-tree proof. Existing owners may gain focused workflow coverage; this plan creates no standalone simplification validator.

The semantic-rule ledger, literal-compatibility ledger, static assembly fixtures, and size measurements are change-local evidence. They prove this refactor without becoming permanent prose or size budgets.

## Non-goals

- Change lifecycle order, stage ownership, automation persistence, review outcomes, milestone semantics, isolation, claims, or downstream handoffs.
- Add a routing engine, scheduler, selector, state store, runtime hash protocol, or new validator family.
- Execute a target agent, send prompt journeys, retain transcripts, grade model output, or select model versions for acceptance.
- Give a reference or asset independent workflow authority.
- Hand-edit generated adapter packages or installed skill copies.
- Treat the 35–50 percent `WP0` target as a normative acceptance threshold.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R21-R24, R26-R28; BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001; INT-005-INT-007 | M1 inventories, fixtures, negative proof, and baseline measurements |
| R1-R20, R30; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-001-INT-004 | M2 universal contract, three conditional references, retained skeleton, and focused validator coverage |
| R25-R29, R32; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006-INT-008 | M3 assembly measurements, semantic preservation, and generated/archive/installed package proof |
| R31 | Completed architecture assessment, canonical update, and architecture-review before this plan |

## Milestones

### M1. Freeze workflow rule and literal ownership

- Milestone state: planned
- Goal: Account for every behaviorally significant current rule and compatibility-sensitive literal, and establish deterministic assembly fixtures before moving or deleting prose.
- Requirements: R21-R24, R26-R28; BND-INPUT-001; BND-AUTH-001; BND-RECOVERY-001; BND-COMPAT-001; INT-005-INT-007.
- Files/components likely touched:
  - `docs/changes/2026-08-11-workflow-skill-simplification/workflow-rule-disposition.yaml`
  - `docs/changes/2026-08-11-workflow-skill-simplification/workflow-literal-compatibility.yaml`
  - `docs/changes/2026-08-11-workflow-skill-simplification/fixtures/`
  - `docs/changes/2026-08-11-workflow-skill-simplification/evidence/assembly-size-baseline.md`
- Dependencies:
  - approved spec and architecture
  - current canonical workflow package and exact literal consumers
- Tests to add/update:
  - static scenarios for all seven valid assemblies and every invalid predicate class
  - bootstrap order; status/off with and without a run; governed read; active automation plus guide authoring; contradictory, missing, unreadable, and mixed resources
  - unknown semantic disposition and unknown literal classification negative fixtures
- Implementation steps:
  - inventory significant rules and duplication clusters with stable IDs, sources, behavior, requirements, assemblies, disposition, destination, and proof
  - classify normative, parser/package, incidental-test, and obsolete literals separately from semantic rules
  - create JSON-compatible YAML scenarios with required and forbidden outcomes
  - record LF-normalized resource identities and baseline words and UTF-8 bytes for all assemblies and the total package
  - route any obsolete semantic rule lacking an approved contract change back to spec
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`
  - run the exact change-local ledger and fixture proof defined in the matching test spec
  - independently inspect coverage against the complete current `skills/workflow/SKILL.md` and literal consumers
- Expected observable result: every significant rule and discovered literal has one closed treatment, scenario coverage is complete, unknown values fail closed, and canonical workflow prose has not moved.
- Commit message: `M1: freeze workflow rule and literal ownership`
- Milestone closeout:
  - validation passed
  - progress updated in stage-owned evidence
  - decision log updated if needed
  - milestone committed
  - independent code review recorded
- Risks:
  - similar passages may encode distinct lifecycle behavior
  - an incidental assertion may be mistaken for a normative contract
- Rollback/recovery:
  - revert the M1 evidence slice; the canonical skill remains unchanged

### M2. Refactor universal and conditional workflow surfaces

- Milestone state: planned
- Goal: Make `SKILL.md` a shorter self-sufficient dispatcher and move only governed, automation, and guide-authoring procedure to their exact references.
- Requirements: R1-R20, R30; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; INT-001-INT-004.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/workflow/references/governed-lifecycle-routing.md`
  - `skills/workflow/references/bounded-workflow-automation.md`
  - `skills/workflow/references/workflow-guide-authoring.md`
  - `skills/workflow/references/boundary-first-method-v1.md` only if mapping compatibility requires it
  - `skills/workflow/assets/workflows-skeleton.md` only if structural ownership needs clarification
  - `scripts/test-skill-validator.py`
  - literal consumers classified for atomic migration in M1
- Dependencies:
  - M1 inventories, fixtures, baseline, and code review are complete
- Tests to add/update:
  - exact predicate and seven-assembly classification plus explicit invalid combinations
  - `WPS` state-free behavior and `WPB` validation-before-persistence order
  - exact `READ` mappings and required/forbidden reference loads
  - one-way governed-to-automation and established-policy-to-guide dependencies
  - unavailable, unreadable, contradictory, and mixed-version fail-safe behavior
  - preservation of universal routing, isolation, status, milestone, review, claim, and handoff semantics
- Implementation steps:
  - add failing focused assertions to the existing skill-validator suite before package edits
  - consolidate universal repetition according to the rule ledger while retaining all R2 policy inline
  - create the governed reference and move only R10-R11 procedure
  - create the automation reference and move only R12 procedure, including command/bootstrap mechanics
  - create the guide-authoring reference and move only R13 procedure; retain skeleton as a structural leaf
  - migrate real literal consumers atomically, update incidental tests, and finalize ledger destinations
- Validation commands:
  - `python scripts/validate-skills.py skills/workflow/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: generic routing is complete from a shorter `SKILL.md`; each valid assembly loads only its required resources; no conditional resource competes for policy ownership.
- Commit message: `M2: simplify workflow package paths`
- Milestone closeout:
  - validation passed
  - progress updated in stage-owned evidence
  - decision log updated if needed
  - milestone committed
  - independent code review recorded
- Risks:
  - universal safety could move behind a conditional trigger
  - bootstrap procedure could persist authority too early
  - references could duplicate transitions or source precedence
- Rollback/recovery:
  - restore the prior complete canonical package and tests as one slice, then regenerate derived packages

### M3. Prove assembly reduction and package parity

- Milestone state: planned
- Goal: Prove deterministic behavior and filesystem identity across all assemblies and package targets, then record honest size and semantic-preservation evidence.
- Requirements: R25-R29, R32; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-006-INT-008.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if existing focused selection cannot prove `workflow`
  - existing adapter fixtures only when focused coverage is absent
  - `docs/changes/2026-08-11-workflow-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-11-workflow-skill-simplification/evidence/semantic-preservation-review.md`
- Dependencies:
  - M2 package refactor and code review are complete
- Tests to add/update:
  - every supported generated, archived, and temporary installed target contains all three references, boundary reference, and skeleton at identical paths and bytes
  - missing, escaped, additional, or stale mapped resources fail package proof
  - all static assembly scenarios remain deterministic and no command starts or grades a target agent
  - LF-normalized accounting counts each unique loaded resource once in documented order
- Implementation steps:
  - extend only existing adapter-distribution proof where direct workflow selection is missing
  - generate all supported packages into a temporary output directory and validate archive plus clean-install parity
  - record before/after words, UTF-8 bytes, resource identities, `SKILL.md`, each resource, total package, duplicate clusters, inline templates, and mapped-resource counts
  - require material `WP0` improvement, explain any other assembly regression, and keep token evidence optional and pinned
  - independently review the complete package against both ledgers and R30
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "workflow"], check=True)""")'`
  - `python scripts/validate-skills.py skills/workflow/SKILL.md`
  - `python scripts/test-skill-validator.py`
- Expected observable result: `WP0` materially shrinks, other assemblies have no unjustified regression, semantics are preserved, and canonical through installed resource bytes match without target-runtime execution.
- Commit message: `M3: prove workflow simplification`
- Milestone closeout:
  - validation passed
  - progress updated in stage-owned evidence
  - decision log updated if needed
  - milestone committed
  - independent code review recorded
- Risks:
  - generic adapter tests may pass without selecting workflow
  - common-path reduction may hide total-package growth
  - partial packaging may mix old and new ownership
- Rollback/recovery:
  - restore the prior complete canonical package, regenerate every derived target, and discard temporary package trees

## Validation plan

- The matching test spec will define one deterministic standard-library command for change-local ledgers and scenarios, including fail-closed unknown-value checks.
- `python scripts/validate-skills.py skills/workflow/SKILL.md`: canonical structure, Resource-map syntax, containment, placeholders, and claim checks.
- `python scripts/test-skill-validator.py`: focused skill-contract and regression proof.
- `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check`: generated skill inventory and resource parity.
- `python scripts/test-adapter-distribution.py`: adapter generation, archive, resource, and clean-install regression proof.
- Temporary build plus `validate-adapters.py --clean-install-smoke --skill workflow`: direct all-target archive and installed-tree proof.
- `python scripts/validate-boundary-first.py --check --path specs/workflow-skill-simplification.md`: final feature-to-proof boundary coverage.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`: lifecycle and planned-work consistency.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-workflow-skill-simplification`: formal review structure.
- Independent semantic review: assembly authority, universal completeness, reference and asset ownership, bootstrap and stateless behavior, failure stops, lifecycle preservation, claims, handoff, and literal treatment.

## Risks and recovery

- Risk: conditional extraction hides universal behavior.
  - Recovery: rule ledger, assembly fixtures, validator assertions, and semantic review block the move; restore the prior package atomically.
- Risk: automation and governed procedure give different transition answers.
  - Recovery: keep transition ownership exclusively governed and test one-way dependency.
- Risk: relocation is presented as deletion or a percentage win.
  - Recovery: report every assembly and the total package in words and bytes; semantic preservation takes precedence.
- Risk: one package target omits a new reference.
  - Recovery: block acceptance on selected archive and temporary installed-tree parity, then regenerate from the last complete canonical revision.

## Dependencies

- Approved proposal, spec, canonical architecture update, approving formal reviews, and closed review resolution.
- Existing boundary-first reference, workflow-guide skeleton, and published-skill resource/package architecture.
- Existing skill validation, adapter generation, archive validation, and clean-install resource owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Use three implementation milestones: preservation evidence, package refactor, and assembly/package proof. | Each slice has an independent failure, review, and rollback boundary. | One large prose-and-package rewrite. |
| 2026-08-11 | Keep semantic and literal inventories separate and validate both before prose movement. | Behavior preservation and exact-string compatibility are different contracts. | One combined ledger; preserve every asserted phrase. |
| 2026-08-11 | Keep transitions governed and make automation and guide authoring consumers. | This prevents conditional references from becoming competing workflow owners. | Shared or duplicated transition procedure. |
| 2026-08-11 | Extend only existing skill and adapter validators for durable proof. | The approved contract excludes a permanent simplicity validator family. | New simplification CLI or token budget gate. |
| 2026-08-11 | Measure all seven assemblies plus boundary variants and total package words and bytes. | Main-file size alone can hide conditional or maintenance regressions. | `SKILL.md` percentage as the acceptance gate. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation milestones, code review, rationale, verification, and PR gates remain.
