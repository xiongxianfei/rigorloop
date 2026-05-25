# Installed-Skill Artifact Placement Contract

## Status

accepted

## Problem

RigorLoop's installed skills are now used outside this repository, and external use exposed a placement-contract gap. In two maintainer sessions on other projects, a skill-only adopter asked where lifecycle artifacts should go, but the answer lived primarily in RigorLoop repo-local files such as `docs/workflows.md` and `CONSTITUTION.md`.

For skill-only adopters, the installed skill is the portable contract. If a user can ask "where does this artifact go?" while only having installed skills, the answer needs to be available from the relevant skill body, not only from a repository workflow guide the adopter may never receive.

The current pattern is split:

```text
skills:
  say what the stage does and that formal evidence may be recorded

docs/workflows.md:
  maps artifact locations and review-record locations

adopter reality:
  the adopter may have the skills but not the RigorLoop repository workflow guide
```

This creates visible ambiguity for proposal-review record placement, spec-review record placement, early-lifecycle findings before a `docs/changes/<change-id>/` pack exists, which plan surface a skill means, and whether `docs/workflows.md` is the owning contract or only a project-local map.

The early-lifecycle gap is especially acute: `proposal-review` and `spec-review` can run before a change pack exists, but current installed skill wording does not clearly state where formal review findings go in that case.

## Goals

- Make installed skills self-contained for artifact-placement questions.
- State each lifecycle and review skill's default artifact placement in the skill body.
- Resolve early-lifecycle review-record placement before a change pack exists.
- Prefer one consistent change-local home for lifecycle evidence.
- Make plan surfaces unambiguous wherever skills say "plan."
- Keep `docs/workflows.md` as a project-local map, not the only source of portable placement rules.
- Add validation that skill-stated placement rules and `docs/workflows.md` do not drift.
- Preserve customized project placement through explicit paths and project-local workflow maps.
- Preserve exact artifact schemas in specs, schemas, and validators where appropriate.
- Keep published-skill wording portable and avoid hard dependency on RigorLoop repository internals.

## Non-goals

- Do not make `docs/workflows.md` irrelevant.
- Do not duplicate every artifact schema, review-record field, or lifecycle validator rule inside every skill.
- Do not require every adopter project to copy the full RigorLoop repository docs.
- Do not change review-finding semantics, severity semantics, review-status values, or stage ordering.
- Do not hand-edit generated adapter output.
- Do not bulk-migrate historical artifact locations in this first slice.
- Do not make a change pack mandatory for isolated, chat-only, non-recorded advisory use.
- Do not let `docs/workflows.md` override explicit user paths, active artifact metadata, approved specs or schemas, or safety constraints.

## Vision fit

fits the current vision

RigorLoop's vision depends on artifacts that remain inspectable and reconstructable after chat history is gone. If an installed skill cannot tell an adopter where to put the artifact it asks them to create, the artifact-first model is weakened at the external-adoption boundary. This proposal strengthens the installed-skill contract while preserving project-local customization.

## Context

A prior artifact-location guide treated `docs/workflows.md` as the project-local artifact map and told public stage skills to consult explicit user paths, active metadata, governing specs or schemas, `docs/workflows.md`, and portable defaults before blocking on ambiguity. That model remains useful for customization and for projects that have a workflow guide.

The external-adopter signal adds a correction: the workflow guide cannot be the only place a placement rule lives. The stage skill itself must carry enough default placement guidance for a skill-only installation.

This proposal reconciles the models:

```text
installed skills:
  portable default placement and stage-owned recording contract

docs/workflows.md:
  project-local customization and summary map

specs/schemas:
  exact artifact shape, validation, and edge-case contracts

validators:
  drift checks and placement consistency checks
```

## Options Considered

### Option 1: Update only `docs/workflows.md`

This is the smallest change and keeps location policy centralized in one project-local map. It is insufficient because it does not help skill-only adopters, leaves the installed skill contract incomplete, and repeats the failure external adopters found.

### Option 2: Put full artifact-location tables in every stage skill

This makes every skill fully self-contained, but it bloats skills, creates high drift risk, duplicates `docs/workflows.md`, and conflicts with progressive-disclosure and concise-skill principles.

### Option 3: Put concise stage-owned default placement in each skill and keep `docs/workflows.md` synchronized

This lets skill-only adopters get placement answers at the point of use, preserves project-local customization, keeps exact shapes in specs and schemas, and allows deterministic drift checks. It creates a dual-surface maintenance obligation, but that can be managed by validation.

### Option 4: Create review records beside proposal/spec until a change pack exists

This is minimally disruptive, but it splits lifecycle evidence across source-adjacent and change-local locations and creates later copy, mirror, or link rules.

### Option 5: Record beside-source first, then mirror into the change pack later

This preserves early local placement and later centralization, but creates duplicate evidence, reconciliation rules, validator complexity, and stale mirror risk.

### Option 6: Change-pack-first for formal lifecycle evidence

Create or identify `docs/changes/<change-id>/` at the first formal lifecycle recording point so proposal-review, spec-review, plan-review, code-review, review log, and review resolution all share one lifecycle evidence home. This requires earlier change-pack creation than some flows may assume, but it removes the early-review ambiguity and keeps the recording rule simple.

## Recommended Direction

Choose Option 3 for installed-skill placement rules and Option 6 for formal lifecycle recording locality.

The governing rule:

```text
Installed skills carry the portable placement contract.
docs/workflows.md carries the project-local map.
Specs and schemas carry exact artifact shape.
Validators prevent drift.
```

For workflow-managed formal lifecycle evidence, use change-pack-first:

```text
docs/changes/<change-id>/
  change.yaml
  review-log.md
  review-resolution.md
  reviews/
    proposal-review-r1.md
    spec-review-r1.md
    plan-review-r1.md
    code-review-m1-r1.md
```

This does not mean every casual or isolated review creates a change pack. Once a review result is formal lifecycle evidence, however, it has a change-local home.

Every artifact-producing or review-producing skill should include the artifact it owns, its portable default path, where formal review records go, what to do if the expected change pack is missing, how `docs/workflows.md` can customize paths, and when to block instead of guessing.

Recommended concise wording pattern:

```md
## Artifact placement

Default artifact:
`<portable default path>`

Formal lifecycle records:
`docs/changes/<change-id>/...`

Use explicit user paths and active artifact metadata first. Use the project
workflow guide when present. Use this portable default when no project-local
map exists. Block when placement remains ambiguous or when a governing spec or
schema forbids the path.
```

For formal lifecycle reviews:

```text
proposal-review:
  docs/changes/<change-id>/reviews/proposal-review-r<n>.md

spec-review:
  docs/changes/<change-id>/reviews/spec-review-r<n>.md

plan-review:
  docs/changes/<change-id>/reviews/plan-review-r<n>.md

review log:
  docs/changes/<change-id>/review-log.md

review resolution:
  docs/changes/<change-id>/review-resolution.md when material findings or blocking outcomes require disposition
```

If no change pack exists, a formal lifecycle review should create or request creation of `docs/changes/<change-id>/` before recording. An isolated advisory review may answer in chat or write to an explicitly requested artifact path, but it must not claim formal lifecycle recording unless recorded in the change pack.

Skills should also disambiguate plan surfaces:

| Surface | Meaning | Owning surface |
|---|---|---|
| `docs/workflows.md` | Stable project workflow and artifact-location map. | `workflow` skill / project maintainers |
| `docs/plan.md` | Active plan index: current live work, blocked work, recent done work. | `plan` / lifecycle bookkeeping |
| `docs/plans/<change-id>.md` | Concrete execution plan body for a planned initiative. | `plan` skill |
| `docs/changes/<change-id>/change.yaml` | Change metadata and validation ledger. | workflow / relevant stage |
| `docs/changes/<change-id>/...` | Change-local evidence pack. | relevant stage skills |

Avoid ambiguous wording like "read the plan," "update the plan," or "record in the plan" when a concrete surface can be named.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Treat adopter confusion as important signal. | in scope | Problem, Context |
| Put placement rules in installed skills. | in scope | Goals, Recommended Direction |
| Resolve early lifecycle review placement. | in scope | Recommended Direction, Expected Behavior Changes |
| Consider change-pack-first. | in scope | Options Considered, Recommended Direction |
| Clarify plan surfaces. | in scope | Recommended Direction |
| Update `docs/workflows.md` secondarily. | in scope | Goals, Recommended Direction |
| Add drift check between skills and workflow map. | in scope | Goals, Testing and Verification Strategy |
| Avoid docs-only FAQ fix. | rejected option | Options Considered |
| Preserve project-local customization. | in scope | Goals, Non-goals, Recommended Direction |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Proposal-review placement contract. | first-slice candidate | It is the clearest exposed adopter failure. |
| Spec-review placement contract. | first-slice candidate | It shares the early-lifecycle locality gap. |
| Plan surface disambiguation in plan-related skills. | first-slice candidate | It prevents recurring ambiguity around `docs/workflows.md`, `docs/plan.md`, and `docs/plans/`. |
| Workflow skill and `docs/workflows.md` synchronization. | first-slice candidate | The project-local map must match portable skill defaults. |
| Deterministic skill/workflow placement checks. | first-slice candidate | Dual surfaces need drift protection. |
| Generated adapter validation. | same-slice dependency | Installed skills must contain the revised skill bodies. |
| Bulk migration of historical review records. | separate proposal | It is a data migration concern, not needed to define the contract. |
| CLI scaffolding for `new-change`. | separate proposal | Useful follow-up, but not required for first-slice wording and validation. |
| Build-time partials for shared placement wording. | deferable follow-up | Reduces maintenance later but is not necessary to prove the contract. |

## Expected Behavior Changes

- A skill-only adopter can tell where review records go.
- Proposal-review and spec-review no longer leave early-lifecycle findings without a defined home.
- Formal lifecycle reviews create or require a change pack before claiming `Recording status: recorded`.
- The phrase "the plan" becomes unambiguous in installed skills.
- `docs/workflows.md` remains useful as a project-local map but is no longer the only placement source.
- Validator coverage prevents skill/workflow placement drift.
- Artifact schema and review-status behavior remain unchanged.

## Architecture Impact

| Surface | Impact |
|---|---|
| Review skills | Add concise placement contracts and pre-change-pack behavior. |
| Artifact-producing skills | Clarify portable default paths and plan-surface terms. |
| `workflow` skill | Clarify that the workflow guide is a map, not the owning skill contract. |
| `docs/workflows.md` | Update rows to match skill defaults. |
| Skill validator | Add deterministic placement-contract checks where feasible. |
| Adapter build/validation | Confirm generated skill output includes revised bodies. |
| Artifact lifecycle validation | May need checks for change-pack-first formal review recording. |
| Review-artifact validation | May need fixture updates for early lifecycle change-pack creation. |
| CLI behavior | No direct change. |

## Testing and Verification Strategy

First-slice validation should use deterministic checks for stable headings and path strings, plus review for semantic quality. It should verify:

| Check ID | What is verified |
|---|---|
| SAP-001 | Each updated review skill states its formal review record path under `docs/changes/<change-id>/reviews/`. |
| SAP-002 | Each updated review skill states what to do when no change pack exists. |
| SAP-003 | `proposal-review` and `spec-review` use the same early-lifecycle locality rule. |
| SAP-004 | `docs/workflows.md` formal review row matches review skill placement. |
| SAP-005 | Plan-related skills distinguish `docs/workflows.md`, `docs/plan.md`, and `docs/plans/<change-id>.md`. |
| SAP-006 | `docs/workflows.md` is described as project-local map, not a replacement for owning skills. |
| SAP-007 | Skill-only cold-read proof answers: "Where does a proposal-review record go?" |
| SAP-008 | Skill-only cold-read proof answers: "Where does a spec-review record go before a change pack exists?" |
| SAP-009 | Skill-only cold-read proof answers: "Which plan surface should I update?" |
| SAP-010 | Generated adapters contain the revised skill bodies. |
| SAP-011 | Public skills do not require RigorLoop repository-internal docs for default placement. |
| SAP-012 | Exact review record schema remains owned by the relevant formal review contract or validator. |
| SAP-013 | Explicit paths and valid project-local workflow-map customizations remain supported. |

Suggested validation commands for the downstream plan to confirm or refine:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/workflows.md \
  --path skills/proposal-review/SKILL.md \
  --path skills/spec-review/SKILL.md \
  --path skills/plan/SKILL.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/plans/<plan>.md \
  --path docs/plan.md
git diff --check --
```

Use actual repository command names and adapter validation commands in the implementation plan.

## Rollout and Rollback

Rollout:

1. Approve this proposal.
2. Write or amend the spec for the installed-skill artifact placement contract.
3. Write the test spec for placement wording, early-lifecycle locality, plan-surface clarity, and workflow-map synchronization.
4. Update review skills first.
5. Update plan and artifact-producing skills.
6. Update the `workflow` skill and `docs/workflows.md`.
7. Add deterministic validation or fixture coverage.
8. Rebuild or validate generated skills and adapters.
9. Run a cold-read test from installed-skill context.
10. Code-review and verify.

Rollback:

- Revert skill wording if it creates ambiguity or conflicts with project customization.
- Restore previous `docs/workflows.md` placement rows if the new synchronization rule is wrong.
- Keep validator checks disabled until wording stabilizes if they overfit.
- Do not delete change packs or review records created under the approved contract.
- Do not move historical artifacts in rollback unless a separate migration plan exists.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Skills become too verbose. | Use concise per-skill placement rules, not full location tables. |
| Placement rules drift between skills and `docs/workflows.md`. | Add deterministic sync checks. |
| Change-pack-first creates extra artifacts for casual reviews. | Limit the rule to formal lifecycle recording; isolated advisory reviews remain non-recording unless requested. |
| Existing projects customize paths. | Keep explicit user paths and project workflow maps above portable defaults. |
| Exact review schema gets duplicated in skills. | Skills state placement; specs, schemas, and validators own exact fields. |
| Early lifecycle change pack naming is unclear. | Spec defines `change_id` derivation and creation triggers. |
| Generated adapters miss revised skill text. | Require build and adapter validation from canonical `skills/`. |
| Validator overfits wording. | Use stable headings and path strings, with code review for semantic quality. |

## Open Questions

No proposal-level open questions remain before spec. Proposal-review resolved the seeded questions as follows:

| Question | Answer for the spec |
|---|---|
| Who creates the first formal lifecycle artifact? | `proposal` creates the change pack when authoring a workflow-managed proposal. Review skills create or block only as a fallback when a formal review is requested and no pack exists. |
| Does change-pack-first apply to all formal reviews or only material-finding reviews? | All formal lifecycle reviews. Clean formal reviews still need durable receipts, so locality must not depend on whether findings are material. |
| Should `docs/workflows.md` remain above portable defaults in lookup order? | Yes, for artifacts it specifies. Portable defaults fill gaps in a present but partial workflow guide. |
| Where should the drift check live? | `validate-skills.py` should own the first deterministic skill/workflow placement drift check. Artifact lifecycle validation should not duplicate the check in the first slice. |
| Should the first implementation slice update all review skills or start smaller? | Start with `proposal-review` and `spec-review`, plus plan-surface disambiguation, then generalize after proof. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-25 | Treat adopter placement confusion as a contract gap. | A skill-only adopter cannot rely on RigorLoop repo-local docs. | Treat as FAQ or docs-only fix. |
| 2026-05-25 | Put portable placement defaults in skill bodies. | Installed skills travel; `docs/workflows.md` may not. | Only update workflow guide. |
| 2026-05-25 | Recommend change-pack-first for formal lifecycle evidence. | One consistent home eliminates early review-record ambiguity. | Beside-source or mirror-later placement. |
| 2026-05-25 | Keep `docs/workflows.md` as synchronized secondary map. | Projects need customization and an index, but not as the sole contract. | Remove workflow guide from placement model. |
| 2026-05-25 | Add drift validation. | Dual surfaces can disagree unless checked. | Rely on manual review only. |

## Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-SAP-001 | `proposal-review` states the formal record path `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`. |
| AC-SAP-002 | `spec-review` states the formal record path `docs/changes/<change-id>/reviews/spec-review-r<n>.md`. |
| AC-SAP-003 | Review skills state that formal lifecycle review requires a change pack before claiming `Recording status: recorded`. |
| AC-SAP-004 | The spec chooses one early-lifecycle locality rule; first-slice recommendation is change-pack-first. |
| AC-SAP-005 | `docs/workflows.md` matches the installed-skill placement defaults. |
| AC-SAP-006 | A validator or test fixture detects a skill/workflow placement mismatch. |
| AC-SAP-007 | Plan-related skills distinguish workflow map, plan index, and plan body. |
| AC-SAP-008 | Isolated advisory reviews remain possible without forced lifecycle artifact creation. |
| AC-SAP-009 | Exact review-record field schema remains owned by the formal review contract or validator. |
| AC-SAP-010 | Generated adapters include the revised skill bodies. |
| AC-SAP-011 | Cold-read proof from installed skills alone answers review placement and plan-surface questions. |
| AC-SAP-012 | Explicit user paths and valid project-local workflow-map customizations still override portable defaults where safe. |

## Behavior Preservation

The downstream change should create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

with this proof matrix:

| Surface | Baseline | New proof | Preservation result |
|---|---|---|---|
| proposal-review recording | placement ambiguous or workflow-guide-dependent | skill states default review path and pre-change-pack rule | strengthened |
| spec-review recording | placement ambiguous or workflow-guide-dependent | skill states default review path and pre-change-pack rule | strengthened |
| plan references | "plan" may be ambiguous | skills distinguish workflow map, plan index, and plan body | strengthened |
| `docs/workflows.md` | project-local map | synchronized with skill defaults | preserved and strengthened |
| custom paths | explicit/workflow-map paths | still honored by lookup order | preserved |
| review schema | exact fields owned outside skill | unchanged | preserved |
| generated adapters | old skill text | revised skill text packaged | current |

## Next Artifacts

```text
proposal-review
spec: installed-skill artifact placement contract
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on Artifacts

- Spec: [Installed-Skill Artifact Placement Contract](../../specs/installed-skill-artifact-placement-contract.md)
- Proposal for `rigorloop new-change` or scaffolding support that creates change packs before formal reviews.
- Proposal for bulk migration of historical beside-source review records if any exist.
- Proposal for build-time partials to avoid repeated placement wording across skills while preserving installed self-containment.
- Proposal for richer customer-project workflow-guide generation if adopters need a generated `docs/workflows.md`.
- Proposal for review-record schema simplification if recording friction remains high after placement is clarified.

## Readiness

Accepted and ready for `spec`.

## Core Invariant

```text
A skill-only adopter must be able to answer "where does this artifact go?"
from the installed skill itself.

docs/workflows.md remains the project-local map, but it is not the only
contract. Formal lifecycle evidence should have one change-local home from the
first recorded stage, and skills plus workflow maps must be kept in sync by
validation.
```
