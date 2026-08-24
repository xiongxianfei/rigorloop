# Governed Lifecycle CLI Execution Plan

## Purpose / big picture

Implement the approved governed lifecycle CLI through reversible slices: freeze conformance, prove read-only interpretation, add guarded mutation and recovery, complete semantic operations, migrate skills and adapters, measure context reduction, and enable CI enforcement only after parity passes.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-24-governed-lifecycle-cli.md`
- Spec: `specs/governed-lifecycle-cli.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
- Architecture review: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/architecture-review-r2.md`
- Test spec: `specs/governed-lifecycle-cli.test.md`, pending

## Context and orientation

The Node package lives under `packages/rigorloop/`, with CLI dispatch in `dist/bin/rigorloop.js`, package modules in `dist/lib/`, and tests in `packages/rigorloop/test/`. Current lifecycle interpretation is spread across Python modules under `scripts/`, especially artifact lifecycle, change metadata, lifecycle synchronization, and review validation. Canonical governed skills live under `skills/`; existing build and adapter tooling owns generated-package parity.

Node becomes mutation-time authority through a pure engine. Python remains compatibility and dual-run proof until ledger-backed retirement. Semantic Markdown stays stage-owned. The CLI changes only `change.yaml` plus fixed transient lock/recovery siblings, while workflow remains the routing owner.

## Non-goals

- Route or invoke stages, run agents, make semantic judgments, author semantic artifacts, or infer approval.
- Open, push, or merge pull requests; publish, release, deploy, or add a hosted service or database.
- Provide cross-branch transactions, malicious-maintainer security, event sourcing, or an arbitrary state setter.
- Require portable skills to use governed lifecycle state.
- Retire Python validators before protected-failure parity and rollback are reviewed.

## Requirements covered

| Requirement and boundary scope | Owner |
| --- | --- |
| R1-R8, R11, R24-R27; BND-INPUT-001, BND-COMPAT-001, BND-ENV-001 | M1 schemas, YAML domain, identities, compatibility, and fixtures |
| R6-R11, R17, R23, R27, R32-R33; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001; INT-001, INT-004 | M2 read-only interpretation and parity |
| R18-R22, R25, R27; BND-TEMPORAL-001, BND-RECOVERY-001; INT-002 | M3 transaction and recovery core |
| R12-R15, R17, R19, R22; BND-AUTH-001, BND-AUTH-002 | M4 evidence registration and settlement |
| R16, R22-R26; BND-STATE-002, BND-RECOVERY-002, BND-COMPAT-001; INT-003 | M5 milestones, migration, and repair |
| R10, R28-R29, R31, R34; BND-COMPOSE-002 | M6 skills, adapters, semantic preservation, and tokens |
| R23, R26-R30, R33-R34; BND-COMPAT-001; INT-003 | M7 CI parity and enforcement |

## Milestones

### M1. Freeze lifecycle contracts and conformance

- Milestone kind: implementation
- Goal: Establish versioned data, operation, result, identity, compatibility, and fixture contracts before behavior.
- Requirements: R1-R8, R11, R17-R18, R24-R27, R32-R33.
- Architecture decisions: ADR-20260824 parser, pure-engine, identity, and compatibility boundaries.
- Files/components likely touched:
  - `packages/rigorloop/package.json`, npm lockfile, new `dist/lib/lifecycle-*` modules
  - versioned fixtures under `packages/rigorloop/test/fixtures/`
  - Python conformance adapters and a protected-failure ledger
- Dependencies:
  - approved specification and architecture
- Tests and proof:
  - accepted YAML domain and rejection of duplicate keys, aliases, tags, merges, multiple documents, non-finite numbers, and unknown values
  - request/result schemas, stable errors, canonical serialization, lifecycle revision, invalidation, and compatibility fixtures shared across languages
- Implementation steps:
  - inventory lifecycle fields, transitions, evidence classes, validator failures, and direct mutation sites
  - add pinned `yaml`; define immutable normalized snapshot, result, diagnostic, and operation types
  - write golden valid and invalid fixtures before interpreter code
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/test-artifact-lifecycle-validator.py`
  - `python3 scripts/test-change-metadata-validator.py`
  - `python3 scripts/test-review-artifact-validator.py`
  - `python3 scripts/validate-npm-package.py`
- Expected observable result: unsafe YAML and unknown values fail before consistency logic and every later operation has one fixture vocabulary.
- Completion criteria: schemas, fixtures, and protected failures are inventoried; Node and Python fixture loaders agree; no mutation command is exposed.
- Required evidence: M1 inventory, dependency identity, coverage, and conformance report.
- Review handoff: independent `code-review` of schemas, parser, fixtures, and ledger.
- Optional commit boundary: `M1: freeze governed lifecycle contracts`
- Risks:
  - accidental Python behavior may be mistaken for approved policy
- Rollback/recovery:
  - remove unexposed modules, dependency, and fixtures together

### M2. Deliver read-only status, context, and validation

- Milestone kind: implementation
- Goal: Prove effective-state interpretation and shared output without mutation.
- Requirements: R1-R11, R17, R23, R26-R27, R31-R33.
- Architecture decisions: ADR-20260824 snapshot, interpreter, and validator-convergence boundaries.
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`, lifecycle repository/interpreter/renderers
  - `packages/rigorloop/test/lifecycle-read.test.js`, Python parity tests
- Dependencies:
  - M1 and code review closed
- Tests and proof:
  - zero/one/multiple changes, explicit selection, malformed state, unsupported versions, invalidation, fresh checkout
  - recorded/evidence/effective state, blockers, operations, context, review rounds, human/JSON equivalence, privacy
- Implementation steps:
  - implement discovery and immutable snapshot; implement pure interpretation and revision
  - expose `status`, `context`, and `validate`; dual-run current validators
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-read.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/test-artifact-lifecycle-validator.py`
  - `python3 scripts/validate-npm-package.py`
- Expected observable result: deterministic effective status and minimal context with no writes.
- Completion criteria: all read and parity fixtures pass with no forbidden diagnostic data.
- Required evidence: M2 parity, output schemas, fresh-checkout proof, and validation.
- Review handoff: independent read-only engine `code-review`.
- Optional commit boundary: `M2: add governed lifecycle read commands`
- Risks:
  - minimal context may omit a required semantic input
- Rollback/recovery:
  - remove additive command dispatch and retain current Python validation

### M3. Implement guarded transaction and recovery core

- Milestone kind: implementation
- Goal: Add optimistic concurrency, idempotency, lock, recovery, replacement, and restoration before semantic operations.
- Requirements: R18-R22, R25, R27, R32-R33.
- Architecture decisions: ADR-20260824 fixed paths, `0600` exclusive create, closed phases, stale rule, and local-only concurrency.
- Files/components likely touched:
  - lifecycle transition/transaction modules and `packages/rigorloop/test/lifecycle-transaction.test.js`
- Dependencies:
  - M2 and code review closed
- Tests and proof:
  - competing callers, live/orphan lock, every interruption point, restoration failure, nonce mismatch, malformed bundle, cleanup, stale and already-recorded behavior
- Implementation steps:
  - implement pure transition result/fingerprint; implement fixed lock and explicit orphan repair
  - implement candidate, recovery bundle, fsync, replace, verify, restore, reconcile, cleanup, and test-only fault points
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-transaction.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/validate-npm-package.py`
- Expected observable result: each fault yields exactly prior, committed, or recovery-blocked state without partial success.
- Completion criteria: concurrency, retry, permissions, containment, and fault suites pass before semantic mutation is enabled.
- Required evidence: M3 fault matrix and filesystem identities.
- Review handoff: security- and recovery-focused `code-review`.
- Optional commit boundary: `M3: add lifecycle transaction core`
- Risks:
  - filesystem durability differs across platforms
- Rollback/recovery:
  - leave mutation disabled and remove transient state only through named repair

### M4. Add evidence registration and settlement

- Milestone kind: implementation
- Goal: Register stage-authored review, validation, and resolution evidence and settle exact artifacts.
- Requirements: R12-R15, R17-R19, R22-R23, R27.
- Architecture decisions: ADR-20260824 semantic-operation, identity, no-setter, and stage-authority boundaries.
- Files/components likely touched:
  - lifecycle request/operation modules, `packages/rigorloop/test/lifecycle-evidence.test.js`, shared fixtures
- Dependencies:
  - M3 and code review closed
- Tests and proof:
  - valid/invalid records, rounds, findings, resolutions, dependency sets, every invalidation row, stale/mismatched/unauthorized/repeated/conflicting settlement
- Implementation steps:
  - implement `record-review`, `record-validation`, `record-finding-resolution`, invalidation, and `settle-artifact`
  - prove only `change.yaml` changes and dual-run protected Python fixtures
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-evidence.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/test-review-artifact-validator.py`
  - `python3 scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: only current authorized evidence registers or settles; stale and unresolved evidence blocks before mutation.
- Completion criteria: every operation has positive, negative, stale, retry, and unknown-value proof.
- Required evidence: M4 transition diffs, parity, and operation matrix.
- Review handoff: independent evidence-authority `code-review`.
- Optional commit boundary: `M4: guard evidence and settlement operations`
- Risks:
  - registration may be mistaken for semantic approval
- Rollback/recovery:
  - disable mutating commands and retain read-only behavior before enforcement

### M5. Add milestone, migration, and named repair operations

- Milestone kind: implementation
- Goal: Complete the operation vocabulary without creating routing or a generic setter.
- Requirements: R16, R22-R26, R30-R31, R33.
- Architecture decisions: ADR-20260824 snapshot, migration, repair, and workflow separation.
- Files/components likely touched:
  - lifecycle milestone/migration/repair modules and focused Node tests/fixtures
- Dependencies:
  - M4 and code review closed
- Tests and proof:
  - milestone eligibility/order/proof/review/invalidation; enumerated legacy versions; deterministic dry runs; unknown corruption; interrupted replace; orphan lock
- Implementation steps:
  - implement milestone start/complete, enumerated migration, and only approved named repairs
  - reject unknown repair codes first; prove routing and semantic artifacts remain unchanged
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-milestone.test.js`
  - `node --test packages/rigorloop/test/lifecycle-migration-repair.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/test-workflow-automation-state.py`
- Expected observable result: supported transitions and recovery work narrowly; unknown state fails closed.
- Completion criteria: every closed operation and refusal partition passes with no workflow continuation.
- Required evidence: M5 milestone, migration, repair, and rollback matrices.
- Review handoff: independent compatibility/recovery `code-review`.
- Optional commit boundary: `M5: complete lifecycle operation vocabulary`
- Risks:
  - repair could grow into an administrative setter
- Rollback/recovery:
  - preserve original bytes and require a compatibility release after activation

### M6. Migrate skills and adapters and measure context

- Milestone kind: implementation
- Goal: Remove lifecycle mechanics from governed skills while preserving semantics, portable behavior, and package parity.
- Requirements: R10, R28-R29, R31, R34.
- Architecture decisions: ADR-20260824 semantic ownership and pre-enforcement migration.
- Files/components likely touched:
  - governed `skills/*/`, existing generators/validators, adapter output proof, measurement ledgers
- Dependencies:
  - M5 and code review closed
- Tests and proof:
  - no direct lifecycle-field mutation procedure; preserved criteria, artifacts, findings, stops, claims, handback, and portable mode
  - Codex/Claude/opencode parity; measurements split mechanics, semantics, returned context, and total profile
- Implementation steps:
  - inventory clauses, migrate stage families with dispositions, regenerate packages, run semantic review and token comparison
- Validation commands:
  - `python3 scripts/validate-skills.py`
  - `python3 scripts/test-skill-validator.py`
  - `python3 scripts/test-build-skills.py`
  - `python3 scripts/test-adapter-distribution.py`
  - `python3 scripts/build-skills.py --check`
- Expected observable result: agents stop calculating lifecycle fields but retain stage-specific rigor and portable use.
- Completion criteria: dispositions and parity pass; R34 reaches 30% or records an owner-approved revised threshold.
- Required evidence: migration ledger, semantic review, package parity, and token report.
- Review handoff: independent cross-skill `code-review`.
- Optional commit boundary: `M6: migrate governed skills to lifecycle CLI`
- Risks:
  - mechanical removal may delete semantic stop rules
- Rollback/recovery:
  - restore prior complete skill packages and regenerate all targets; keep enforcement off

### M7. Activate CI and mandatory enforcement

- Milestone kind: implementation
- Goal: Activate the boundary only after compatibility, recovery, skills, adapters, and measurement pass.
- Requirements: R23, R26-R30, R33-R34.
- Architecture decisions: ADR-20260824 five-gate adoption and ADR-20260810 ledger-backed retirement.
- Files/components likely touched:
  - `scripts/ci.sh`, focused validation integration, retirement ledgers, affected governance/workflow/package guidance
- Dependencies:
  - M6 and code review closed; every AC10 gate recorded
- Tests and proof:
  - CI lifecycle validation, full Node/Python parity, protected failures, manual corruption, mixed versions, rollback, fresh checkout, packaged command availability
- Implementation steps:
  - dual-run full corpus; retire/delegate only proved duplication; activate one versioned enforcement change; update affected guidance; run full validation
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python3 scripts/test-artifact-lifecycle-validator.py`
  - `python3 scripts/test-change-metadata-validator.py`
  - `python3 scripts/test-review-artifact-validator.py`
  - `python3 scripts/test-select-validation.py`
  - `python3 scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh`
- Expected observable result: humans, governed skills, workflow, adapters, and CI share one guarded lifecycle boundary.
- Completion criteria: AC1-AC10 are current, rollback is rehearsed, full local CI passes, and no semantic or external authority moved into the CLI.
- Required evidence: M7 enforcement decision, parity/retirement proof, full validation, compatibility, rollback, and token summary.
- Review handoff: milestone and final holistic `code-review`; later closeout gates remain separate.
- Optional commit boundary: `M7: enforce governed lifecycle CLI boundary`
- Risks:
  - mixed versions may strand governed work
- Rollback/recovery:
  - ship the prior coordinated CLI/schema/skill/CI contract; never advise undocumented YAML edits

## Validation plan

- `node --test packages/rigorloop/test/lifecycle-*.test.js`: focused lifecycle proof as files are introduced.
- `npm test --prefix packages/rigorloop`: complete CLI regression.
- Python lifecycle, metadata, and review validator tests: compatibility and protected failures.
- Skill, generator, and adapter tests: semantic package and cross-target parity.
- `python3 scripts/validate-npm-package.py`: package/dependency boundary.
- `bash scripts/ci.sh`: repository-wide final gate after focused proof.

## Risks and recovery

- Risk: Node and Python compete. Recovery: block enforcement on differences and retire only through the ledger.
- Risk: concurrency corrupts state. Recovery: keep mutation disabled until every fault point passes.
- Risk: identities over-invalidate. Recovery: prove every matrix row and route changed outcomes to spec.
- Risk: skills lose rigor. Recovery: require clause dispositions and semantic review; restore complete packages on gaps.
- Risk: mixed deployments fail. Recovery: retain read-only diagnostics and delay enforcement.

## Dependencies

- Add pinned `yaml` only in M1 with package/security review.
- Preserve validated direct mutation until M7 activation.
- Keep Python validators until parity and retirement settle.
- Close each milestone and code review before the next.
- Approve `specs/governed-lifecycle-cli.test.md` before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-24 | Freeze conformance before behavior | Prevent policy drift | Ad hoc translation |
| 2026-08-24 | Prove reads before writes | Validate interpretation without state risk | Status and settlement together |
| 2026-08-24 | Build transaction core before operations | One fault-tested mutation path | Per-command write logic |
| 2026-08-24 | Split settlement from milestones/repair | Keep authority reviews bounded | One mutation mega-slice |
| 2026-08-24 | Migrate skills after contract stability | Avoid temporary mechanics in packages | Parallel early rewrite |
| 2026-08-24 | Enforce last | Preserve mixed-version recovery | Immediate mandatory use |

## Readiness

- See the owning change record for current workflow state.
