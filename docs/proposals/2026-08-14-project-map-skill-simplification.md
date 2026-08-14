# Project-Map Skill Simplification

## Owning change record

`docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`

## Problem

The published `project-map` skill is evidence-rigorous but makes every invocation load 2,297 words of procedure spanning creation, refresh, audit, root/area coordination, freshness repair, command evidence, diagrams, downstream reliance, and follow-up routing. Its current mode model also conflates operation and scope: `create`, `refresh`, and `audit` describe actions, while `area` describes a target and can coexist with each action.

The main file repeats output structure already owned by `assets/project-map-skeleton.md`, repeats orientation and evidence-access guidance across several sections, and keeps detailed refresh and area-coordination procedure on the common path. This makes small root-map creation and bounded audits harder to scan while increasing the chance that duplicated rules drift.

The current approved contract and architecture intentionally keep freshness, evidence, and root/area policy in `SKILL.md`. This change cannot safely move those responsibilities by editorial rewrite alone; it needs an explicit contract amendment and a bounded architecture update to distinguish universal policy from conditional procedure.

## Goals

- Reduce the real loaded context for root creation, refresh, audit, and area-map work without weakening current-state evidence, freshness, or downstream reliance.
- Replace the overlapping mode list with independent closed `operation` and `scope` axes.
- Keep universal orientation, evidence truthfulness, source ranking, freshness meanings, command honesty, stops, claims, and handoff rules inline.
- Move detailed refresh, correction, audit, overlap, and area-registration procedure into one conditionally loaded skill-owned reference.
- Make the existing skeleton the sole structural owner of metadata labels, section order, registration-table shape, evidence-trail shape, and placeholders.
- Preserve customer-project portability, generated package parity, historical maps, and current lifecycle ownership.
- Prove semantic preservation and loaded-profile reduction without target-agent runtime execution or permanent size validation.

## Non-goals

- Change `project-map` from a current-state orientation surface into architecture design, planning, backlog, verification, or workflow authority.
- Change evidence precedence, the meanings of `observed`, `inferred`, `unknown`, `current`, `partial`, or `stale`, or the requirement to cite material claims.
- Add a repository scanner, executable mapping engine, runtime observer, network crawler, target-agent evaluation, tokenizer dependency, or dedicated project-map artifact validator.
- Add another output asset, automatically migrate historical maps, rewrite `docs/project-map.md`, or optimize another skill.
- Change artifact paths, adapter packaging architecture, lifecycle schema, workflow stage order, or downstream stage ownership.

## Vision fit

fits the current vision

The change makes a frequently reused orientation artifact easier to apply while preserving the traceability, evidence visibility, reviewability, and resumability that distinguish RigorLoop.

## Context

The canonical package currently contains a 304-line, 2,297-word, 15,545-byte `SKILL.md` and a 73-line, 313-word, 2,010-byte skeleton. The complete package is 377 lines, 2,610 words, and 17,555 bytes.

`specs/project-map.md` owns 84 requirements covering role, modes, placement, freshness, evidence, commands, area maps, structure, diagrams, reliance, validation, and rollout. `scripts/skill_validation.py` currently requires the four mode literals and several policy-bearing sections and literals in the main file. `docs/architecture/system/architecture.md` explicitly says evidence ranking, inference policy, refresh triggers, prohibitions, handoff, and claims stay in `SKILL.md`; it also records the existing four-mode classifier. The specification and architecture documentation therefore participate directly in this refactor.

The existing skeleton is already the correct structural asset. It should not receive policy, and no second skeleton or output asset is needed.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `project-map` skill | in scope | Goals and Recommended Direction |
| Reduce unnecessary common-path content | in scope | Problem, Expected Behavior Changes, and success measurements |
| Preserve map trustworthiness and usability | in scope | Goals, universal ownership, and Testing and Verification Strategy |
| Create a new branch and proposal | in scope | Governed change record and authoring evidence |
| Perform proposal review | in scope | Readiness and formal review evidence |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal `SKILL.md` | core to this proposal | This is the primary user-value surface. |
| One conditional maintenance and area-coordination reference | core to this proposal | It creates the real progressive-disclosure boundary. |
| Operation/scope classification model | core to this proposal | It removes the current overlapping mode ambiguity. |
| Existing skeleton ownership cleanup | core to this proposal | Structural duplication must have one owner. |
| `specs/project-map.md` amendment | same-slice dependency | The approved four-mode and policy-location contract must change atomically. |
| Bounded architecture documentation update | same-slice dependency | Current architecture explicitly fixes refresh-trigger ownership and four-mode classification. |
| Existing validator and fixture migration | same-slice dependency | Parser and test contracts must follow the approved semantic contract rather than freeze old prose. |
| Semantic, literal, profile, and package evidence | same-slice dependency | Simplification must prove preservation and honest context reduction. |
| Runtime mapping engine or target-agent evaluation | out of scope | It would create a different runtime and acceptance system. |

## Options Considered

### Option 1: Keep the package unchanged

This preserves all current contracts but retains overlapping modes, duplicated structure, and full common-path loading. It does not address the usability problem.

### Option 2: Edit and deduplicate only within `SKILL.md`

This is the lowest-risk change and can remove some repeated prose, but every invocation still loads detailed refresh and area-map coordination. It also leaves the operation/scope ambiguity unresolved unless the approved contract changes anyway.

### Option 3: Use one conditional maintenance and area-coordination reference

Keep a self-sufficient universal file, introduce independent operation and scope axes, move only detailed maintenance and multi-map procedure into one mapped reference, and leave structure in the existing asset. This reduces real profiles while keeping navigation shallow and ownership explicit.

### Option 4: Split refresh, audit, area maps, commands, diagrams, and reliance into several references

This maximizes theoretical disclosure but fragments one cohesive orientation method and creates excessive trigger and navigation complexity. Command honesty, evidence classes, and reliance safety are universal and should not depend on several optional resources.

### Option 5: Replace prose with an executable repository-mapping engine

An engine could collect deterministic inventories but cannot safely own semantic boundaries, inferred claims, unknowns, or downstream reliance. It adds runtime, maintenance, and acceptance scope unrelated to simplifying the published skill.

## Recommended Direction

Choose Option 3.

Use this package:

```text
skills/project-map/
├── SKILL.md
├── references/
│   └── map-maintenance-and-area-coordination.md
└── assets/
    └── project-map-skeleton.md
```

The published `project-map` package remains the sole owner. The reference is conditional procedure inside that package, not a new lifecycle or policy owner.

### Closed classification model

Classify two independent axes before broad reads:

```text
operation:
  create
  refresh
  audit

scope:
  repository
  area
```

Use six valid profiles:

| Profile | Operation | Scope | Loaded procedure |
| --- | --- | --- | --- |
| `PM0-root-create` | `create` | `repository` | `SKILL.md` plus skeleton when writing |
| `PM1-root-refresh` | `refresh` | `repository` | `SKILL.md` plus conditional reference |
| `PM2-root-audit` | `audit` | `repository` | `SKILL.md` plus conditional reference |
| `PM3-area-create` | `create` | `area` | `SKILL.md`, conditional reference, and skeleton when writing |
| `PM4-area-refresh` | `refresh` | `area` | `SKILL.md` plus conditional reference |
| `PM5-area-audit` | `audit` | `area` | `SKILL.md` plus conditional reference |

Audit is read-only unless the user separately requests a correction after the audit result. Loading the reference never grants write, command-execution, network, test, build, downstream, or workflow authority.

### Universal ownership in `SKILL.md`

Keep purpose, trigger, workflow role, placement, operation/scope classification, basic freshness meanings, baseline truthfulness, `observed`/`inferred`/`unknown`, source ranking, material-claim citations, configured-versus-executed command meaning, runtime-observation truthfulness, universal map/reliance invariants, stops, claims, resource triggers, and next-stage behavior inline.

The main file must remain sufficient to create a trustworthy root map with the skeleton and to classify safely when conditional procedure is required.

### Conditional-reference ownership

Load `references/map-maintenance-and-area-coordination.md` exactly for every refresh or audit and every area-scoped invocation. It owns the detailed refresh-trigger inventory, affected-section selection, correction notes, audit procedure, root registration, parent/child rules, overlap ownership, contradiction handling, missing-area behavior, dirty-baseline reconciliation, and interrupted or partial maintenance recovery.

The reference may specialize procedure but may not redefine universal evidence meanings, source ranking, command authority, map statuses, claims, stops, or downstream ownership. A missing, unreadable, escaped, contradictory, or mixed-version required reference stops dependent work rather than causing reconstruction from memory.

### Structural ownership

Keep exactly one asset. `project-map-skeleton.md` owns metadata labels, required section order, root registration table headers, evidence-trail table headers, placeholders, and insertion locations. It does not own evidence ranking, freshness semantics or triggers, inference policy, command authority, future-design prohibitions, reliance, handoff, or claims.

Remove the duplicated `Required output structure` inventory and metadata-label inventory from the main file after validators and the governing contract are migrated to validate the asset as the structural source. The `Area maps` section is emitted only for a root map with registered area maps; it is omitted for an area map and for a root map with no registered areas.

### Compact inline consolidation

Merge customer-project orientation, evidence-access efficiency, and full-file escalation into one concise evidence-access contract. Consolidate downstream reliance, follow-up boundary, and next-stage routing without weakening direct-source inspection or the rule that project maps do not own deferred execution. Keep command and runtime truthfulness inline because every map can make test, runtime, or data-flow claims.

## Expected Behavior Changes

- Root creation loads a shorter common procedure and the existing skeleton.
- Refresh and audit load one conditional reference containing detailed maintenance behavior.
- Every area-scoped invocation loads that reference for root registration, parent identity, overlap, and contradiction handling.
- The result reports operation and scope separately instead of using `area` as an overlapping mode.
- Audit remains read-only, and map writing remains limited to create or explicitly requested refresh/correction behavior.
- Required resources fail closed; the common file does not reconstruct maintenance or area procedure.
- Produced maps preserve the same status values, evidence classes, required substantive sections, citations, command truthfulness, diagrams, risks, unknowns, and downstream reliance behavior.
- Existing maps are not migrated automatically.

## Architecture Impact

A bounded architecture update is required because `docs/architecture/system/architecture.md` currently records the four-mode classifier and states that refresh triggers stay in `SKILL.md`. The update should describe universal policy in the main file, conditional maintenance/area procedure in one skill-owned reference, and unchanged structural ownership in the skeleton.

No ADR is expected because the change reuses the existing published-skill package, mapped-reference, structural-asset, canonical-source, and adapter-parity architecture. A new ADR is required only if specification discovers an independent policy owner, new runtime, persistence mechanism, package transformation, or lifecycle authority.

## Testing and Verification Strategy

Before editing the canonical package, create separate change-local inventories for behaviorally significant rules and exact literal consumers. Closed rule dispositions should include `retained-inline`, `retained-conditional-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`. Literal dependencies should be classified as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `obsolete`, or `historical-fixture`.

Use deterministic static scenarios for all six profiles, false and ambiguous triggers, audit read-only behavior, create/refresh authority, dirty baselines, correction notes, root/area registration, overlaps, contradictions, missing resources, configured/executed commands, current/partial/stale outcomes, asset composition, placeholders, and forbidden downstream claims.

Extend existing project-map and package validators instead of creating a new validator family. Migrate real parser contracts atomically and update incidental tests rather than preserving accidental prose. Preserve the existing representative-output and cold-read evidence where still semantically valid.

Measure LF-normalized UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, each reference and asset, every loaded profile, representative create/refresh assemblies, and the complete package. Report mapped-resource count and duplicate-cluster count separately. Require every real loaded profile to decrease unless an explicit semantic-preservation finding proves a specific exception; do not use a fixed percentage as a semantic gate.

Validate canonical structure, generated skills, adapter archives, clean-installed resources, sentence readability, change metadata, formal review artifacts, and the complete repository-owned PR gate. Do not execute Codex, Claude Code, OpenCode, or another target-agent runtime for acceptance.

## Rollout and Rollback

Amend the project-map spec and bounded architecture documentation first, then migrate validators, canonical skill, reference, and skeleton atomically. Generate and validate public adapter packages only through existing repository tooling. Existing project-map artifacts remain readable and are not rewritten merely to adopt the package refactor.

Rollback restores the prior complete canonical package, coupled validators and fixtures, governing spec text, and bounded architecture text together, then regenerates derived packages through existing tooling. Do not leave a shortened main file installed without its required reference.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| A universal evidence or freshness rule moves behind conditional loading | Freeze a semantic-rule ledger first and keep meanings, source rank, claims, and stops inline. |
| The new classification changes behavior unintentionally | Define all six profiles, migration from each old mode, ambiguity stops, and static scenarios in the spec. |
| Root and area maps acquire competing owners | Keep one conditional reference with explicit parent, registration, overlap, and contradiction rules. |
| The skeleton becomes a hidden policy surface | Validate it as structural only and keep applicability and semantics in procedure. |
| Main-file reduction merely relocates or enlarges content | Report each loaded profile and complete package separately. |
| Exact validator literals freeze accidental prose | Separate semantic-rule and literal-compatibility inventories before edits. |
| A missing installed reference weakens safety | Stop before dependent maintenance or area behavior and retain archive/install parity checks. |
| The architecture update becomes broader redesign | Limit it to the documented package ownership and classification corrections; require a new ADR only for a newly discovered durable decision. |

## Open Questions

None. The specification should define the exact old-mode-to-new-profile compatibility mapping and enumerate the existing validator literals that are normative versus incidental.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-14 | Use independent operation and scope axes. | `area` is a scope and currently overlaps create, refresh, and audit. | Preserve the ambiguous four-mode list. |
| 2026-08-14 | Add one conditional maintenance and area-coordination reference. | Refresh, audit, and multi-map work share a genuine procedure boundary and one reference keeps navigation shallow. | Inline-only compression; many small references. |
| 2026-08-14 | Keep command and runtime truthfulness inline. | Every map may make test, runtime, or data-flow claims. | A separate runtime-evidence reference. |
| 2026-08-14 | Keep exactly one structural asset. | The existing skeleton already owns the necessary output structure. | Additional result, area-map, or evidence assets. |
| 2026-08-14 | Require a spec amendment and bounded architecture update. | Current approved sources explicitly own the old modes and policy placement. | Treat the change as prose-only refactoring. |
| 2026-08-14 | Exclude target-agent acceptance and permanent simplicity gates. | Static contract proof, package parity, and independent semantic review are sufficient and deterministic. | Runtime journeys, transcript grading, and token-budget enforcement. |

## Next Artifacts

- Formal `proposal-review` record.
- Focused amendment to `specs/project-map.md` after proposal approval.
- Bounded update to `docs/architecture/system/architecture.md` after specification settles the package boundary.
- Execution plan and test specification after approved contract and architecture review as required.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim acceptance, specification readiness, architecture approval, implementation readiness, verification, branch readiness, or PR readiness.
