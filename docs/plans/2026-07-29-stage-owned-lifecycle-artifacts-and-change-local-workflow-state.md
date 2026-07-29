<!-- Template: plan-skeleton-v2 -->
<!-- Skill: plan -->
<!-- Template status: normative -->

# Stage-Owned Lifecycle Artifacts and Change-Local Workflow State

## Purpose / big picture

Implement the approved stage-owned lifecycle contract as one prospective,
repository-local workflow mechanism.

Governed proposal, specification, architecture, ADR, plan, and test-spec
content remains stable after review.
Author and review peers change only the matching artifact-state entry.
Workflow changes routing only.
Implementation and later stages write their own code or evidence and route
upstream defects back to the owning stage.

The implementation must replace the existing plan-owned and
capability-driven automation model without introducing hashes, write
interception, another public authorization parameter, a hosted service, or
selective downstream reuse.

## Current Handoff Summary

- Owning change record:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers,
routing, and closeout readiness live only in that record.

## Source artifacts

- Proposal:
  `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
- Spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Approved spec review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md`
- Architecture:
  `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Approved architecture review:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r2.md`
- Boundary-first method:
  `skills/plan/references/boundary-first-method-v1.md`
- Compatibility audit:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/compatibility-audit.md`
- Test spec: pending `test-spec` after plan-review

## Context and orientation

The current repository distributes lifecycle guidance across canonical
published skills, change metadata, workflow helpers, generated adapters, and
older plan- and capability-era contracts.
This implementation must improve the user-facing skill contract first and
change only the minimum repository support needed to store and check that
contract.

The approved design makes `change.yaml` the sole mutable state surface for
governed changes:

- `artifact_states` stores transition-scoped lifecycle entries keyed by stable
  artifact ID;
- `workflow_state` stores routing, planned work, blockers, and final-closeout
  readiness;
- `workflow.automation` stores one target-driven run without parent
  authorization, effective-capability, selector, or typed-policy layers; and
- linked stage evidence remains in its owning change-local Markdown or YAML
  record instead of being duplicated into lifecycle state.

Canonical authored behavior lives in `skills/`.
Generated public adapter bodies are derived release output and must preserve
the canonical ownership and isolation rules.
Repository scripts remain subordinate.
The implementation reuses the existing change-metadata validator, skill
validator, build checks, and adapter distribution checks.
It does not add a selector ledger, stage-policy registry, protected-path
validator, writer-attribution check, content identity, or another lifecycle
validator.

Activation is atomic and prospective.
Earlier milestones may author and prove the new published guidance and accept
the new change-metadata shape, but public workflow marker creation remains
disabled until the generated surfaces, compatibility behavior, and
preactivation scenarios pass.
The atomic cutover is the workflow-skill source change that makes
`stage-owned-change-local-v1` the default for new governed changes and causes
resumed nonterminal work to migrate before its first mutation.
No feature flag, selector, or public parameter controls that cutover.

## Non-goals

- Do not add content hashes, immutable document snapshots, protected-path
  manifests, or write interception.
- Do not add parent authorization, effective capability, activation selector,
  risk-profile, selector-ledger, or typed stage-policy mechanisms.
- Do not add a hosted database, scheduler, control plane, background worker,
  or external-state mutation.
- Do not implement selective downstream reuse after upstream revision.
- Do not mass-migrate historical changes or rewrite historical evidence.
- Do not let workflow manufacture review settlement or let reviewers advance
  workflow routing.
- Do not make scripts, examples, fixtures, or generated adapters the
  normative owner of published stage behavior.
- Do not open a PR, push, publish, release, deploy, merge, or access
  credentials through this implementation.

## Requirements covered

| Requirement group | Owning milestones |
| --- | --- |
| SLA-R001 through SLA-R017: activation, state shape, governed artifacts, and navigation-only plans | M3, M4, M6 |
| SLA-R018 through SLA-R021c: authoring transitions and closeout | M1, M3 |
| SLA-R022 through SLA-R033: review settlement, isolation, and reconciliation | M1, M2, M3 |
| SLA-R034 through SLA-R041: workflow routing and planned-work ownership | M2, M3 |
| SLA-R042 through SLA-R047: downstream challenge, owner correction, and conservative replay | M1, M2 |
| SLA-R048 through SLA-R064a: one target, closed automation, stop behavior, status, and cancellation | M2, M3, M6 |
| SLA-R065 through SLA-R071: prospective migration, validation, portability, and proof limits | M3, M4, M5, M6 |
| SLA-R072 through SLA-R074b: canonical skill ownership, unknown-value checks, and adapter parity | M1, M3, M5 |
| SLA-R074c through SLA-R074e: closed compatibility subjects, reciprocal notices, and stale proof maps | preimplementation test-spec gate, M4, M5 |
| SLA-R075 through SLA-R077: boundary record, exact proof-map consumption, and example ownership | preimplementation test-spec gate, M5 |
| AC-SLA-001 through AC-SLA-012: artifact and review lifecycle behavior | M1, M2, M3 |
| AC-SLA-013 through AC-SLA-022: routing, plan ownership, route-back, target, and final verification behavior | M1, M2, M3, M6 |
| AC-SLA-023 through AC-SLA-032: migration, semantic validation, published skills, terminal history, planned work, and adapter consistency | M1, M3, M4, M5, M6 |
| AC-SLA-033 through AC-SLA-035: boundary-first completeness and stale test-spec replacement | preimplementation test-spec gate, M5 |

### Boundary and interaction ownership

| Boundary or interaction | Owning milestone | Affected surfaces | Rollback unit | Proof timing |
| --- | --- | --- | --- | --- |
| BND-INPUT-001 | M3 | contract marker, state schema, paths, IDs, and closed values | minimal change-metadata commit | M3 focused metadata tests before code review |
| BND-STATE-001 | M3 | artifact, review, milestone, closeout, and automation transitions | minimal change-metadata commit | M3 transition matrix before code review |
| BND-AUTH-001 | M1 | author, reviewer, workflow, downstream, and adapter write boundaries | canonical skill-source commit | M1 skill contract and semantic review before code review |
| BND-COMPOSE-001 | M2 | isolated/manual review, workflow-managed review, route-back, status, and off paths | workflow-skill routing commit | M2 composed published-skill scenarios before code review |
| BND-TEMPORAL-001 | M2 | interrupted authoring, settlement retry, milestone binding, and terminal runs | workflow-skill recovery commit | M2 retry and reconciliation scenarios before code review |
| BND-RECOVERY-001 | M2 | review failure, upstream correction, validation failure, cancellation, and conservative replay | workflow-skill recovery commit | M2 failure and route-back scenarios before code review |
| BND-COMPAT-001 | M4 | historical reads, resumed migration, mixed writers, reciprocal notices, and stale proof maps | compatibility adapter and fixture commit | M4 old/new/mixed fixtures before code review |
| BND-ENV-001 | M6 | repository paths, generated adapters, external-action prohibition, and activation | workflow-skill cutover commit | M6 focused post-cutover proof before code review |
| INT-001 | M1 | authoring-in-progress versus independent review | canonical author/reviewer skill commit | M1 composed skill scenario |
| INT-002 | M2, M3 | durable review evidence with interrupted settlement or routing | workflow guidance plus metadata consistency commits | M3 focused reconciliation proof |
| INT-003 | M3 | current milestone, review occurrence, and final readiness | minimal change-metadata commit | M3 stale-occurrence and readiness tests |
| INT-004 | M2, M3 | later target versus current prerequisites and fixed ownership | workflow guidance plus metadata consistency commits | M3 target-bound scenario |
| INT-005 | preimplementation test-spec gate, M4 | current writer versus retired writer and stale test proof | test-spec replacement plus compatibility adapter commit | M4 mixed-state fixture after proof maps are approved |
| INT-006 | M6 | verification or cancellation versus repair or external mutation | workflow-skill cutover commit | M6 verification and cancellation containment proof |
| INT-007 | M1, M2 | downstream discovery versus upstream write-back | published stage and workflow skill commits | M2 route-back and conservative replay scenario |

## Milestones

### Preimplementation gate. Test-proof alignment

- Gate kind: upstream lifecycle gate, not an implementation milestone.
- Owner: `test-spec`, followed by `test-spec-review`.
- Goal: Create the matching boundary-first proof map and revise every
  dependent test specification whose proof still expects plan-owned status,
  reviewer write-back, downstream status settlement, or capability-era
  authorization.
- Inputs are read-only during implementation:
  - `docs/plan.md`
  - the approved feature spec and the 32 reciprocal-notice specs
  - every dependent `specs/*.test.md` identified by SLA-R074e
- Exit criteria:
  - every approved boundary and interaction maps to direct proof or a visible
    blocking gap;
  - all required dependent test-spec revisions are approved;
  - no stale proof map authorizes M1;
  - concrete command IDs and temporary adapter-generation behavior are bound.
- Failure behavior: return to the owning `test-spec` or feature-spec stage;
  implementation does not repair upstream proof artifacts.

### M1. Canonical published-skill ownership and artifact quality

- Milestone kind: implementation
- Goal: Make canonical published skills and their user-facing assets the
  primary portable contract for stable governed content, peer author/review
  transitions, independent invocation, fixed write boundaries, and
  downstream route-back.
- Requirements: SLA-R013 through SLA-R033, SLA-R042 through SLA-R047,
  SLA-R072 through SLA-R074b; BND-AUTH-001; INT-001; INT-007.
- Files/components likely touched:
  - canonical authoring skills under `skills/`
  - matching review skills under `skills/*-review/`
  - downstream skills: `implement`, `code-review`, `explain-change`,
    `verify`, `learn`, and `pr`
  - governed artifact and current-handoff assets under affected skill
    directories
  - existing skill-contract tests only where structural enforcement is
    already supported
- Dependencies:
  - approved spec and architecture;
  - preimplementation test-proof alignment complete.
- Tests to add/update:
  - each affected skill names writable outputs and read-only inputs;
  - authoring skills never claim review settlement;
  - review peers record their own evidence and state settlement without
    editing reviewed content or workflow routing;
  - downstream skills route upstream defects and never update plans,
    governed content, or another stage's state;
  - public assets omit mutable status, milestone, blocker, review, and
    next-stage ownership.
- Implementation steps:
  - inventory the exact affected canonical skills and assets;
  - add or update focused skill-contract checks before changing wording;
  - author stage-specific ownership language and recovery guidance;
  - keep repository-maintainer implementation detail out of published
    bodies;
  - review each skill as user-facing documentation, not merely as a token or
    substring surface.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
- Expected observable result: Every changed published stage explains its
  writable outputs, read-only inputs, peer-review boundary, and route-back
  behavior without instructing an upstream write-back.
- Commit message: `M1: improve published stage ownership guidance`
- Milestone closeout evidence:
  - affected-skill inventory and semantic review;
  - focused skill validation;
  - M1 implementation evidence under the owning change root;
  - clean or resolved code-review for M1.
- Risks:
  - generic shared wording can erase stage-specific responsibilities or make
    the public skill read like repository-maintainer documentation.
- Rollback/recovery:
  - revert the canonical skill and asset slice together;
  - do not regenerate or publish from a partially reverted source tree.

### M2. Workflow-skill composition, routing, and recovery

- Milestone kind: implementation
- Goal: Express the single-target automation behavior in the published
  workflow skill: current prerequisites, fixed stage ownership,
  evidence-first settlement, route-back, conservative replay, read-only
  status, evidence-preserving off, and explicit stop behavior.
- Requirements: SLA-R022 through SLA-R064a; BND-COMPOSE-001;
  BND-TEMPORAL-001; BND-RECOVERY-001; INT-002; INT-004; INT-007.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - workflow skill assets or references only when they improve portable
    clarity and are actually used
  - focused canonical skill tests
- Dependencies:
  - M1 published ownership contract.
- Tests to add/update:
  - isolated review settles only its own review evidence and artifact state;
  - workflow-managed review routes only after settlement evidence exists;
  - later targets do not skip current prerequisites;
  - interrupted authoring, conflicting review reuse, cancellation, status,
    off, and terminal retry produce the specified stop or resume behavior;
  - downstream discovery routes to the owner and resumes conservatively after
    fresh review;
  - verify success stops before PR and verify failure does not repair.
- Implementation steps:
  - write the user-facing workflow scenarios first;
  - simplify the workflow skill around target, prerequisites, evidence, and
    fixed owners;
  - remove capability/profile/selector language from the public path;
  - keep review independence and requirement fidelity as evidence gates, not
    authorization modes;
  - leave public marker creation disabled until M6.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
- Expected observable result: The public workflow skill can explain and route
  one target-driven lifecycle without adding write authority or another
  activation control.
- Commit message: `M2: simplify published workflow routing`
- Milestone closeout evidence:
  - scenario-to-requirement review matrix;
  - focused canonical skill validation;
  - clean or resolved code-review for M2.
- Risks:
  - simplifying public guidance can accidentally omit interruption,
    independent invocation, or route-back behavior.
- Rollback/recovery:
  - revert the workflow-skill slice;
  - use explicit stage invocation;
  - preserve all existing stage evidence and fixed write boundaries.

### M3. Minimal change-metadata state and consistency checks

- Milestone kind: implementation
- Goal: Add the smallest closed `change.yaml` shape needed by the published
  contract and validate it through the existing change-metadata path.
- Requirements: SLA-R001 through SLA-R041 where they define state shape,
  identity, transition, evidence, and routing consistency; SLA-R048 through
  SLA-R064a; SLA-R070; SLA-R073; BND-INPUT-001; BND-STATE-001; INT-002;
  INT-003; INT-004.
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/change_metadata_semantics.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
  - `scripts/workflow_automation_state.py`
  - `scripts/test-workflow-automation-state.py`
- Dependencies:
  - M1 and M2 define the normative public behavior;
  - preimplementation proof maps bind the focused command IDs.
- Tests to add/update:
  - valid multi-artifact state, planned work, routing, blockers, and the
    approved six-field automation record;
  - duplicate IDs or paths, escaping paths, missing or additional fields,
    illegal transitions, stale occurrences, and false final readiness;
  - explicit `unknown_value` or `not_in_vocabulary` tests for every new
    closed set;
  - unknown-value rejection occurs before consistency branching;
  - unmarked historical records remain readable.
- Implementation steps:
  - write focused metadata failures first;
  - extend one schema and one semantic validator instead of adding a
    lifecycle-validator family;
  - use `workflow_automation_state.py` only as the bounded persistence adapter
    for the approved fields;
  - reject unknown values before consistency checks;
  - keep the marker opt-in and creation disabled;
  - do not add protected-path, process-attribution, policy-registry,
    selector, or hash checks.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`
  - `python scripts/test-workflow-automation-state.py`
- Expected observable result: `change.yaml` can represent and reject the
  approved lifecycle states with actionable diagnostics while published
  skills remain the normative behavior owner.
- Commit message: `M3: add minimal change-local lifecycle state`
- Milestone closeout evidence:
  - focused schema, semantic, and persistence-adapter validation;
  - clean or resolved code-review for M3.
- Risks:
  - expanding a generic validator could recreate a second workflow engine.
- Rollback/recovery:
  - revert the dormant metadata and bounded state-adapter support;
  - preserve fixtures and review evidence;
  - keep marker creation disabled.

### M4. Prospective compatibility and bounded migration adapter

- Milestone kind: implementation
- Goal: Keep historical reads side-effect free and provide one bounded
  migration path for resumed nonterminal work without editing upstream plans,
  specs, architecture, ADRs, or test specs.
- Requirements: SLA-R065 through SLA-R074e; BND-COMPAT-001; INT-005;
  AC-SLA-023 through AC-SLA-025, AC-SLA-027, AC-SLA-032, AC-SLA-035.
- Files/components likely touched:
  - `scripts/workflow_automation_state.py`
  - `scripts/test-workflow-automation-state.py`
  - `scripts/test-change-metadata-validator.py`
  - compatibility fixtures under `tests/fixtures/change-metadata/`
- Read-only inputs:
  - `docs/plan.md`
  - the approved proposal, spec, architecture, and ADR
  - the 32 reciprocal-notice specifications named by SLA-R074c
  - all approved dependent test specifications
- Dependencies:
  - M1 through M3;
  - the preimplementation test-spec gate has already revised and approved
    every stale dependent proof map.
- Tests to add/update:
  - read-only historical inspection has no mutation;
  - first resumed mutation migrates exactly once;
  - target, completed evidence, stop reason, and external-action prohibition
    survive migration;
  - mixed artifact-local, plan-owned, capability-era, and current writers fail;
  - missing retired profile/capability/selector records do not block;
  - compatibility fixtures reflect the already-approved reciprocal notices;
  - a stale dependent test spec blocks reliance rather than being rewritten;
  - deterministic checks never claim process-level writer attribution.
- Implementation steps:
  - write old, current, and mixed-state fixtures first;
  - keep historical reads side-effect free;
  - migrate only resumed nonterminal work before its first mutation;
  - use the bounded state adapter and change-metadata semantics from M3;
  - do not introduce a generic lifecycle synchronizer, query subsystem,
    profile compatibility layer, or selector ledger;
  - treat plan and plan-index content as navigation-only read-only input.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-workflow-automation-state.py`
- Expected observable result: Historical work stays unchanged, resumed work
  migrates once before mutation, current work has one writer model, and no
  stale status-era proof map authorizes implementation.
- Commit message: `M4: add prospective lifecycle migration and compatibility`
- Milestone closeout evidence:
  - migration matrix results;
  - reciprocal-notice and stale-proof audit;
  - clean or resolved code-review for M4.
- Risks:
  - migration may silently reinterpret ambiguous legacy state or broaden the
    scope into mass normalization.
- Rollback/recovery:
  - disable automatic continuation;
  - preserve migrated and historical evidence;
  - require explicit owner inspection for ambiguous records;
  - never restore multiple writable state owners.

### M5. Generated skill parity and preactivation proof

- Milestone kind: implementation
- Goal: Rebuild derived skill surfaces, prove canonical/generated parity and
  the complete boundary and interaction map while public marker creation
  remains disabled.
- Requirements: SLA-R061 through SLA-R074e; AC-SLA-001 through AC-SLA-035
  except the prospective activation outcome owned by M6.
- Files/components likely touched:
  - canonical `skills/` source corrected when parity exposes a source defect
  - existing skill-build and adapter-distribution fixtures
  - end-to-end lifecycle fixtures under `tests/fixtures/`
  - `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/behavior-preservation.md`
- Dependencies:
  - M1 through M4 closed;
  - approved test spec with no boundary or interaction gaps;
  - all affected dependent test specs reviewed;
  - no open material review findings.
- Tests to add/update:
  - canonical skills and every supported generated adapter preserve ownership,
    isolation, and route-back behavior;
  - generated output is rebuilt from canonical sources and not hand-edited;
  - one end-to-end path for authoring, clean review, revision request,
    independent review, workflow-managed continuation, milestone resume,
    route-back, conservative replay, cancellation, verify success, and verify
    failure;
  - all eight boundaries and seven selected interactions have direct proof;
  - external action, credential, destructive Git, and hosted mutation remain
    impossible;
  - marker creation remains disabled in every preactivation scenario.
- Implementation steps:
  - use the existing adapter-distribution test harness to generate a
    versioned temporary output tree;
  - run canonical skill and adapter parity before activation;
  - execute the complete boundary-first proof map;
  - record behavior-preservation evidence;
  - correct defects in canonical `skills/`, never in generated output;
  - confirm marker creation is still disabled when this milestone closes.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: Canonical and generated skill surfaces agree,
  every boundary and selected interaction has proof, and the repository is
  ready for cutover without exposing the new marker.
- Commit message: `M5: prove published skill and adapter parity`
- Milestone closeout evidence:
  - generated parity report;
  - boundary-first proof results;
  - behavior-preservation matrix;
  - explicit preactivation marker-disabled evidence;
  - clean or resolved code-review for M5.
- Risks:
  - generated parity could pass structurally while user-facing skill guidance
    is incomplete or contradictory.
- Rollback/recovery:
  - keep activation disabled;
  - correct canonical skill sources and rerun the same parity harness;
  - never hand-edit generated output.

### M6. Atomic workflow-skill activation

- Milestone kind: implementation
- Goal: Perform one independently closeable prospective cutover after M5,
  prove the post-cutover public behavior, and preserve a simple rollback.
- Requirements: SLA-R001 through SLA-R004, SLA-R061 through SLA-R069;
  BND-ENV-001; INT-006; AC-SLA-001, AC-SLA-002, AC-SLA-019 through
  AC-SLA-025.
- Exact activation owner:
  - `skills/workflow/SKILL.md` owns the public default that creates
    `stage-owned-change-local-v1` for new governed changes and requires
    migration before the first mutation of resumed nonterminal work;
  - `scripts/workflow_automation_state.py` may perform only the bounded
    persistence operation already specified and proved in M3/M4.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `scripts/workflow_automation_state.py` only if the persisted default
    cannot be enabled without a code change
  - focused existing skill, metadata, state-adapter, and lifecycle scenario
    fixtures
  - activation evidence under the owning change root
- Dependencies:
  - M1 through M5 closed;
  - no open material findings;
  - preactivation marker-disabled evidence and generated adapter parity pass.
- Tests to add/update:
  - a new governed change receives the current marker without another
    parameter;
  - a resumed nonterminal change migrates exactly once before mutation;
  - historical read-only inspection remains unchanged;
  - status and off retain their read-only/evidence-preserving behavior;
  - verify failure stops without repair and verify success stops before PR;
  - cancellation never reaches external or destructive actions.
- Implementation steps:
  - re-run the focused preactivation checks;
  - change the workflow-skill default as the single public cutover;
  - enable only the already-proved bounded persistence path when required;
  - run focused post-cutover scenarios before any broad gate;
  - record the exact diff and post-cutover evidence;
  - do not add a flag, selector, policy registry, or second activation source.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: New governed work uses the stage-owned
  change-local mechanism by default; resumed work migrates safely; historical
  reads remain unchanged; external actions stay unreachable.
- Commit message: `M6: activate stage-owned workflow default`
- Milestone closeout evidence:
  - exact activation-source diff;
  - focused pre- and post-cutover results;
  - current adapter parity;
  - clean or resolved code-review for M6.
- Risks:
  - a second activation source could create mixed behavior.
- Rollback/recovery:
  - revert the M6 workflow-skill default and bounded marker-creation change;
  - preserve all state and review evidence already written;
  - retain the fixed stage ownership guidance from M1;
  - return to explicit invocation without restoring retired writers.

### M7. Lifecycle closeout

- Milestone kind: lifecycle-closeout
- Goal: Complete cross-milestone review, explanation, final verification, and
  PR handoff without treating plan readiness as Done.
- Requirements: SLA-R037m through SLA-R037ob, SLA-R061, SLA-R062;
  AC-SLA-020 through AC-SLA-022.
- Files/components likely touched:
  - change-local final holistic review evidence
  - `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/explain-change.md`
  - change-local verify and PR handoff evidence
- Dependencies:
  - M1 through M6 closed;
  - required review-resolution closed;
  - fresh generated and broad-smoke evidence.
- Tests to add/update:
  - none owned by closeout; it consumes the approved test spec and fresh
    implementation evidence.
- Implementation steps:
  - run final holistic code review over the complete diff;
  - run `ci-maintenance` only if the risk-to-check assessment triggers it;
  - create durable change explanation;
  - run final verify from current inputs;
  - stop before PR unless `pr` is invoked explicitly.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state`
  - `python scripts/validate-change-metadata.py docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`
  - `bash scripts/ci.sh --mode pr --base <merge-base> --head HEAD`
- Expected observable result: All implementation milestones, reviews,
  rationale, verification, and handoff evidence are current and linked;
  external PR creation still requires the `pr` stage.
- Commit message: `M7: close stage-owned lifecycle evidence`
- Milestone closeout evidence:
  - approved final holistic code review;
  - current explain-change;
  - passing final verify;
  - PR handoff evidence when explicitly invoked.
- Risks:
  - stale milestone or generated evidence could be mistaken for final proof.
- Rollback/recovery:
  - keep final closeout not-ready;
  - rerun only the stale owning gate;
  - never infer readiness from plan prose or a prior review.

## Validation plan

| Validation command | Purpose and timing |
| --- | --- |
| `python scripts/validate-boundary-first.py --path specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` | Confirm the approved feature boundary record remains structurally valid before test-spec authoring and after compatibility edits. |
| `python scripts/test-skill-validator.py` | Prove the existing structural claims for canonical published ownership and isolation guidance in M1, M2, M5, and M6. |
| `python scripts/validate-skills.py` | Validate every canonical skill after published guidance changes. |
| `python scripts/test-change-metadata-validator.py` | Prove state shape, closed vocabularies, legal transitions, migration inputs, and unknown-value failures in M3, M4, and M6. |
| `python scripts/validate-change-metadata.py docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml` | Validate the owning change record after every state-changing handoff. |
| `python scripts/test-workflow-automation-state.py` | Prove only the bounded persistence and migration adapter used by M3, M4, and M6. |
| `python scripts/build-skills.py --check` | Prove canonical generated skill parity after M1/M2 and before activation. |
| `python scripts/test-adapter-distribution.py` | Prove every supported generated adapter preserves canonical behavior in M5. |
| `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state` | Validate every formal review recording event after each review. |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state` | Block milestone or final closeout while findings remain open. |
| `bash scripts/ci.sh --mode broad-smoke` | Run one repository-wide integration gate at M5 preactivation and once after the M6 cutover. |
| `bash scripts/ci.sh --mode pr --base <merge-base> --head HEAD` | Run the final selected PR gate from the actual branch diff during M7. |

Test-spec must assign stable command IDs to these commands, prefer the
smallest focused command that proves each obligation, and map every boundary
and interaction to direct proof.
It must not add a selector test, standalone lifecycle validator, or
script-level semantic duplicate merely because the behavior appears in a
published skill.
No milestone may substitute a helper-only test for an admitted public or
sibling path.

## Risks and recovery

- Risk: The repository already contains pre-adoption changes whose shapes are
  ambiguous.
  - Recovery: Keep reads side-effect free, migrate only before resumed
    mutation, and pause for owner inspection when projection is ambiguous.
- Risk: Published skills and scripts could define competing workflow behavior.
  - Recovery: Treat canonical skills and the approved spec as normative;
    constrain scripts to the existing change-metadata, skill-build, and
    adapter-support roles named by this plan.
- Risk: Removing capability-era state could weaken review independence.
  - Recovery: Retain manifests, blind-first evidence release,
    requirement-fidelity proof, second-review escalation, and final holistic
    review as evidence gates.
- Risk: A generic validator might let unknown closed values bypass
  consistency checks.
  - Recovery: Add direct unknown-value tests for each new closed set and
    reject unknowns before branching into consistency logic.
- Risk: More validators could make a simple published-skill rule costly to
  maintain and harder to explain.
  - Recovery: Extend only the existing change-metadata validator for durable
    state, use the existing skill and adapter checks for publication quality,
    and require a new validator proposal only when an unproved deterministic
    invariant cannot fit those owners.
- Risk: Partial rollout could expose different behavior between canonical and
  generated skills.
  - Recovery: Keep marker creation off through M5, activate only in M6, and
    roll back only the M6 default while preserving fixed skill ownership.
- Risk: The large existing dirty worktree can obscure milestone attribution.
  - Recovery: Scope each milestone by explicit files and evidence, inspect the
    real diff before every code review, and preserve unrelated user changes.

## Dependencies

- `plan-review` must approve this plan before test-spec authoring.
- `test-spec` must consume the exact approved boundary and interaction IDs.
- `test-spec-review` must close all proof gaps, and every stale dependent test
  spec identified under SLA-R074e must be revised by `test-spec` and approved,
  before M1 implementation.
- Each implementation milestone requires targeted tests first, implementation
  evidence, code-review, and any required review-resolution before the next
  milestone.
- M5 preactivation proof depends on M1 through M4 being closed.
- M6 activation depends on M5 being closed, marker-disabled evidence being
  current, and generated adapter parity passing.
- M7 depends on all implementation milestones being closed.
- External PR creation remains owned by `pr` and is not implied by this plan.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-29 | Use six implementation milestones plus one lifecycle-closeout milestone. | This isolates published stage guidance, workflow composition, minimal state support, compatibility, preactivation parity, atomic cutover, and final evidence into independently reviewable rollback units. | One large cutover; one milestone per skill or requirement. |
| 2026-07-29 | Make canonical published skills M1 and keep repository scripts subordinate. | Portable user-facing behavior is the primary contract; scripts only store or check the minimum deterministic state and publication invariants. | Script-first workflow semantics; generated-adapter ownership. |
| 2026-07-29 | Reuse one metadata validator instead of adding lifecycle, policy, selector, or writer-attribution validators. | The approved mechanism needs closed state consistency, not a second executable workflow specification. | New protected-path validator; selector ledger; generic lifecycle validator family. |
| 2026-07-29 | Complete stale proof-map revisions before M1 and treat upstream artifacts as implementation read-only. | Test-spec owns proof and implementation may not repair a previous stage's artifact. | Revising specs, plans, or test specs during migration implementation. |
| 2026-07-29 | Keep marker creation disabled through M5 and make the workflow-skill default the M6 cutover. | Separating preactivation proof from the exact public activation owner makes rollback and post-cutover proof independently closeable without a new parameter. | Activating during schema work; a feature flag or selector; combined parity and activation milestone. |
| 2026-07-29 | Preserve review-independence receipts but remove them as workflow authorization state. | Review proof remains independently approved while the capability-era state model is superseded. | Removing review evidence; retaining receipt-heavy automation state. |
| 2026-07-29 | Use conservative replay after upstream revision. | It is the complete approved first-version behavior and avoids a dependency-analysis subsystem. | Selective downstream reuse; full initiative restart. |

## Readiness

- See the owning change record for current workflow state.
- Stable plan intent is ready for `plan-review`.
- Readiness is not Done.
- Remaining completion gates: plan-review, test-spec, test-spec-review, M1-M6
  implementation and milestone reviews, M7 lifecycle closeout, final
  verification, and explicit PR handoff.
