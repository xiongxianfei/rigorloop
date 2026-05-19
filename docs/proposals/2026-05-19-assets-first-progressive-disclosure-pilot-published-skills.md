# Proposal: Assets-First Progressive Disclosure Pilot for Published Skills

## Status

accepted

---

## Problem

RigorLoop's published skill design contract recommends progressive disclosure: keep `SKILL.md` focused on common-path execution and move optional depth into packaged `references/`, `scripts/`, and `assets/` when that content earns its place.

So far, the published-skill rewrites have mostly stayed flat: the skill body carries the full operating procedure, output skeletons, examples, and repeated substructures directly inside `SKILL.md`. That was reasonable for early readability work because it reduced blast radius. However, if every future rewrite stays flat, progressive disclosure becomes a design principle with no lived implementation.

The problem is now concrete:

- Published skills must remain self-contained because adopters may receive only installed skill files, while RigorLoop's internal `specs/`, `schemas/`, and `docs/` remain maintainer-side context.
- Existing readability work expects installed skills to be clear, non-redundant, enum-fenced, and equipped with fillable output skeletons.
- Resource-map validation and repository-root versus skill-local path distinctions have already appeared as important validator concerns. In particular, root `scripts/` requirements must be blocked while properly mapped packaged skill-local resources remain allowed.
- When canonical skills change, generated skills and adapters must be rebuilt or validated from canonical `skills/` rather than hand-edited.

The missing piece is a small, focused pilot that proves packaged resources work end-to-end without reopening settled skill rewrites or introducing build-time partials.

---

## Goals

- Prove progressive disclosure with a single low-risk pilot skill.
- Start with `assets/` only, not `references/` or `scripts/`.
- Use assets for structural templates that are copied and filled by the agent at runtime.
- Keep `SKILL.md` as the execution contract and resource map.
- Exercise adapter packaging with a non-empty skill-local resource directory.
- Validate that every packaged asset is reachable from a resource-map entry.
- Preserve behavior parity, self-containment, and lifecycle claim boundaries.
- Record common-path token-cost impact separately from packaged asset content.
- Avoid reopening recently settled or in-flight skill rewrites.

---

## Non-goals

- Do not retrofit `proposal`, `proposal-review`, `spec`, or `spec-review` in this proposal.
- Do not introduce build-time partials or include syntax.
- Do not move rule-heavy guidance into `references/` in this first pilot.
- Do not add skill-local `scripts/` in this first pilot.
- Do not change adapter install roots, lockfile semantics, CLI behavior, or release archive trust boundaries.
- Do not change canonical authored source location: `skills/<name>/SKILL.md` remains canonical.
- Do not make every skill use `assets/`.
- Do not weaken self-containment: packaged assets must ship with the skill and must not require repository-root internal files.
- Do not claim branch readiness, PR readiness, verification readiness, or final closeout from this proposal alone.

---

## Vision fit

fits the current vision

This proposal improves RigorLoop's artifact-first model by making published skills easier to inspect, maintain, and validate. It separates common-path instructions from reusable structural templates while preserving the installed skill as the user-facing operating contract.

The proposal is falsified if the pilot causes any of these outcomes:

```text
- behavior-parity regression;
- self-containment regression;
- missing asset in generated adapter output;
- resource-map ambiguity;
- output skeleton drift;
- common-path token-cost regression beyond the approved budget;
- lifecycle handoff or claim-boundary weakening.
```

Token reduction is not allowed to justify quality loss.

---

## Initial intent preservation

| Initial goal | Treatment | Where recorded |
| --- | --- | --- |
| Make progressive disclosure real, not only aspirational | in scope | Problem, Goals |
| Keep published skills self-contained | in scope | Goals, Non-goals, Validation |
| Use packaged resources deliberately | in scope | Recommended direction |
| Start with a focused pilot | in scope | Asset pilot implementation slice |
| Avoid reopening settled or in-flight work | in scope | Non-goals |
| Avoid build-time partials | out of scope | Non-goals |
| Preserve adapter trust boundaries | in scope | Architecture impact |
| Validate generated adapter output | in scope | Testing and acceptance criteria |
| Preserve behavior parity | in scope | Testing and validation strategy |

---

## Context

The current published-skill design direction says that `SKILL.md` should be lean, self-contained, and focused on the procedure the agent needs for normal execution. Prior skill-readability work also emphasizes that users may not receive RigorLoop's internal repository files, so published skills must not rely on those files as required dependencies.

The earlier readability proposal also established the need for fillable output skeletons and cold-read verification: build adapters, install one into a clean project, open each installed skill without repository context, and treat unresolved references or missing skeletons as defects.

This proposal narrows progressive disclosure to its smallest useful form:

```text
assets/ only
one pilot skill
no references/
no scripts/
no build-time partials
no settled-skill retrofit
```

---

## Options considered

### Option 1: Do nothing

Leave progressive disclosure as a recommendation only.

**Pros**

- No implementation risk.
- No validator changes.
- No adapter packaging risk.

**Cons**

- Progressive disclosure remains unproven.
- Future skill rewrites keep growing flat `SKILL.md` bodies.
- Resource-map and adapter-packaging validation lack lived practice.
- The design contract drifts from actual authoring behavior.

### Option 2: Add `references/`, `scripts/`, and `assets/` in one pilot

Exercise all packaged resource types at once.

**Pros**

- Broadly proves the full progressive-disclosure model.
- Exercises resource-map logic across all resource classes.

**Cons**

- Too much surface area for a first pilot.
- `scripts/` introduces command, safety, and repository-root ambiguity.
- `references/` can become a parking lot for rule text.
- Harder to isolate whether failures come from packaging, content movement, scripts, or resource-map semantics.

### Option 3: Retrofit assets into recently rewritten `proposal` / `proposal-review`

Use existing parity baselines and visible output skeletons.

**Pros**

- Strong baseline artifacts.
- Obvious reusable substructures such as finding blocks and decision-log rows.

**Cons**

- Reopens settled work.
- Bundles readability retrofit with packaging mechanics.
- Creates a precedent that recently closed skill work can be reopened immediately without a separate retrofit rationale.

### Option 4: Pilot `assets/` only on `plan`

Use the `plan` skill as the first packaged-resource pilot.

**Pros**

- Strong structured artifact.
- Strong reusable substructure: milestone blocks.
- Lower risk than review-class skills.
- Not part of the settled `proposal` / `proposal-review` pair.
- Not part of the active `spec` / `spec-review` pair.
- Many existing plans can serve as behavior-parity references.
- Proves adapter packaging and resource-map validation without introducing scripts or references.

**Cons**

- Does not prove `references/` or `scripts/`.
- Still requires careful behavior-parity review to avoid changing plan semantics.
- Requires asset drift validation between `SKILL.md` and asset skeletons.

---

## Recommended direction

Choose Option 4: pilot `assets/` only on `plan`.

The pilot should package reusable structural skeletons under:

```text
skills/plan/assets/
```

The `plan` skill should keep `SKILL.md` focused on:

```text
- when to use the skill;
- workflow role;
- operating procedure;
- resource map;
- plan-authoring rules;
- validation and handoff rules;
- output expectations.
```

The assets should contain only structural templates copied and filled by the agent.

Recommended pilot asset layout:

```text
skills/plan/
|-- SKILL.md
`-- assets/
    |-- plan-skeleton.md
    |-- milestone.md
    |-- current-handoff-summary.md
    `-- decision-log-row.md
```

### Asset contract

An asset is a structural template, not a tutorial.

It should be copied, filled, and adapted by the agent. It should not contain long prose explaining the workflow.

Allowed asset content:

| Allowed | Example |
| --- | --- |
| Headings | `## Milestone <n>: <name>` |
| Tables | milestone table, decision-log row |
| Placeholder fields | `<owner>`, `<status>`, `<validation command>` |
| Short field hints | `Fill all required fields.` |
| Template metadata comments | `<!-- Template: plan-milestone-v1 -->` |

Disallowed asset content:

| Disallowed | Reason |
| --- | --- |
| Paragraph-length explanations | belongs in `SKILL.md` or `references/` |
| Filled example narratives | belongs in examples, not skeleton assets |
| Repository-root paths | violates self-containment if required |
| Policy/rule text | belongs in `SKILL.md` or future `references/` |
| Hidden trigger logic | belongs in description or `SKILL.md` |

### Resource map contract

The `plan` skill must include a resource map that tells the agent exactly when and how to use each asset.

Example:

```md
## Resource map

- COPY `assets/plan-skeleton.md` when creating a new plan.
  Fill: status, owner, related proposal, milestones, validation commands,
  decision log, current handoff summary.
  Do not emit unfilled placeholders.

- COPY `assets/milestone.md` once per milestone.
  Fill: milestone ID, purpose, deliverables, acceptance criteria,
  validation evidence, handoff state.

- COPY `assets/current-handoff-summary.md` for the active plan handoff section.
  Update: current milestone, milestone state, next stage, open blockers.

- COPY `assets/decision-log-row.md` once per material planning decision.
  Fill: date, decision, rationale, alternatives rejected.
```

The important convention is the `COPY` verb. It distinguishes structural assets from references that should merely be read.

### Spec-slice dependency

This proposal defines a follow-on asset pilot. It does not change the current published-skill design-contract first slice unless `specs/skill-contract.md` is explicitly amended and approved.

Implementation must not begin until the spec amendment defines how this `plan` asset pilot relates to existing `proposal` / `proposal-review` published-skill work and any historical `plan` normalization scope.

If `plan` is currently part of another active or unresolved skill-contract change, this proposal must either wait for that change to close or record an owner decision explaining why the overlap is safe.

### Handoff asset boundary

`assets/current-handoff-summary.md` may contain only section headings, field labels, and placeholders.

It must not define lifecycle status values, next-stage transition rules, claim ownership, branch-ready semantics, PR-ready semantics, or validation requirements.

`skills/plan/SKILL.md` remains responsible for instructing the agent to keep the Current Handoff Summary consistent with the active plan, plan index, and change metadata.

If this boundary cannot be kept, `current-handoff-summary.md` must remain inline in `SKILL.md` for the pilot.

### Output skeleton boundary

For the `plan` asset pilot, `assets/plan-skeleton.md` may serve as the reviewed equivalent output template for the full plan artifact only if `SKILL.md` includes a compact output expectation summary and a Resource map entry that tells the agent when to copy the asset.

The full section layout must not be duplicated in both `SKILL.md` and the asset.

### Template metadata

Each asset should begin with stable metadata comments:

```md
<!-- Template: plan-milestone-v1 -->
<!-- Skill: plan -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/plan/SKILL.md -->
```

Allowed template statuses:

```text
normative
optional
example
deprecated
```

For this pilot, all shipped assets should be either:

```text
normative
optional
```

No filled examples should be introduced in this slice.

### Placeholder policy

Use placeholders that are visibly non-content:

| Placeholder style | Allowed? |
| --- | ---: |
| `<milestone-id>` | yes |
| `<owner>` | yes |
| `<validation command>` | yes |
| `[FILL IN]` | yes |
| `TODO:` | acceptable |
| `your text here` | no |
| filler prose | no |
| empty required fields | no |

The resource map must instruct the agent not to emit unfilled placeholders.

### Why `plan` is the best pilot

| Criterion | `plan` result |
| --- | --- |
| Produces structured artifact | yes |
| Has reusable substructure | yes: milestones |
| Low risk compared with review skills | yes |
| Not recently settled | yes |
| Not in active `spec` / `spec-review` slice | yes |
| Has parity baseline | yes: existing plans |
| Exercises multi-instance asset use | yes: one milestone asset copied multiple times |

`code-review` is also a strong future candidate, but it has heavier recording obligations. A defect in a `code-review` finding template has higher review-governance impact than a defect in a plan milestone skeleton. Start with `plan`.

---

## Expected behavior changes

- `skills/plan/SKILL.md` becomes shorter and more common-path focused.
- `skills/plan/assets/` ships structural templates.
- Adapter builds include non-empty skill-local `assets/`.
- Validators prove every packaged asset is mapped in `SKILL.md`.
- Generated adapter validation proves assets are present after packaging.
- Behavior-parity fixtures show generated plans preserve required sections, milestone shape, handoff semantics, decision-log shape, and validation discipline.
- No changes are made to `proposal`, `proposal-review`, `spec`, or `spec-review`.
- No `references/` or `scripts/` are introduced in this asset pilot implementation slice.

---

## Architecture impact

| Surface | Impact |
| --- | --- |
| `skills/plan/SKILL.md` | updated to use a resource map and asset references |
| `skills/plan/assets/*.md` | new packaged structural templates |
| `scripts/build-skills.py` | only if needed to preserve asset directories |
| `scripts/build-adapters.py` | must package skill-local assets |
| `scripts/validate-adapters.py` | must prove assets reach generated adapter output |
| `scripts/skill_validation.py` | must validate resource-map coverage for assets |
| `scripts/measure-skill-tokens.py` | should measure common-path `SKILL.md` separately from packaged assets |
| adapter install roots | unchanged |
| lockfile schema | unchanged |
| CLI behavior | unchanged |

---

## Testing and verification strategy

| Check ID | What is verified | Expected result |
| --- | --- | --- |
| `PD-AST-001` | `skills/plan/assets/` exists and contains only approved asset files. | pass |
| `PD-AST-002` | Every asset has metadata comments: template ID, skill, status, maintained-alongside. | pass |
| `PD-AST-003` | Every asset is referenced by `SKILL.md` resource map. | pass |
| `PD-AST-004` | Resource map entries use `COPY`, state trigger condition, and name fields to fill. | pass |
| `PD-AST-005` | Assets pass the deterministic structural-template checks defined by the spec amendment. | pass |
| `PD-AST-006` | Assets do not require repository-root internal paths. | pass |
| `PD-AST-007` | Generated adapter output contains the same asset files. | pass |
| `PD-AST-008` | Plan behavior-parity fixtures preserve plan shape and handoff semantics. | pass |
| `PD-AST-009` | Common-path `SKILL.md` token cost is measured separately from assets. | pass |
| `PD-AST-010` | Cold-read verification can locate all assets and load conditions from installed skill only. | pass |

### Asset validation oracle boundary

Asset validation must be deterministic in the first pilot.

Static validation may check:

- asset file count;
- approved asset paths;
- required template metadata comments;
- presence of a matching Resource map entry;
- Resource map entry includes `COPY`;
- Resource map entry names fields to fill;
- asset contains visible placeholders such as `<...>` or `[FILL IN]`;
- asset does not contain forbidden repository-root required paths;
- generated adapter output contains the asset path.

Static validation must not use broad semantic scoring to decide whether asset prose is too explanatory.

For prose-heavy assets, use bounded heuristics or code-review judgment. Example bounded heuristic: fail if an asset contains a paragraph over a spec-defined word count outside a table or placeholder block.

Behavior parity must be fixture-based or review-recorded. It must not rely on an unbounded semantic claim that the new plan is similar enough.

Recommended commands:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
python scripts/measure-skill-tokens.py
git diff --check --
```

If change metadata and lifecycle artifacts are in scope:

```bash
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/plans/<plan-file>.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/changes/<change-id>/review-log.md \
  --path docs/changes/<change-id>/review-resolution.md
```

### Behavior-parity requirements

The pilot must prove that moving structural templates to assets does not change plan behavior.

Parity evidence should cover:

| Area | Required proof |
| --- | --- |
| Required plan sections | unchanged |
| Milestone shape | unchanged |
| Current handoff summary | unchanged |
| Decision log | unchanged |
| Validation commands | still represented |
| Review and implementation handoff | not weakened |
| Claim boundaries | no branch-ready or PR-ready overclaim |
| Recording discipline | no lifecycle state ambiguity |

A structural pass alone is not enough.

---

## Rollout and rollback

### Rollout

1. Approve proposal.
2. Amend `specs/skill-contract.md` to add the assets-first pilot contract.
3. Add or amend test spec for asset metadata, resource map, adapter packaging, and behavior parity.
4. Update `skills/plan/SKILL.md`.
5. Add `skills/plan/assets/*.md`.
6. Run validator, adapter build, token-cost, and behavior-parity checks.
7. Cold-read the generated adapter install.
8. Return to code review.
9. After pilot closeout, decide whether to propose `references/`, `scripts/`, or additional skill assets.

### Rollback

- Reinline asset skeletons into `skills/plan/SKILL.md`.
- Remove `skills/plan/assets/`.
- Keep validator improvements if they remain valid and do not block flat skills.
- Do not change adapter roots, lockfiles, or CLI behavior.
- Do not roll back unrelated published-skill design work.

---

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Assets become hidden behavior. | Keep rules in `SKILL.md`; assets contain structure only. |
| Assets are not packaged into adapters. | Add adapter validation for asset presence. |
| Resource map is vague. | Require `COPY`, trigger condition, and fields-to-fill. |
| Common-path token savings are overstated. | Measure `SKILL.md` body separately from assets. |
| Asset placeholders leak into final artifacts. | Resource map says not to emit unfilled placeholders; behavior-parity fixtures check output. |
| The pilot changes plan semantics. | Require behavior-parity proof. |
| The pilot reopens settled work. | Do not touch `proposal`, `proposal-review`, `spec`, or `spec-review`. |
| Asset count grows too large. | Cap pilot assets at four. |
| The skill actually needs references, not assets. | Defer references; keep this pilot structural only. |
| Repository-root paths sneak into assets. | Self-containment validation covers assets as published surfaces. |

---

## Asset pilot implementation slice

The asset pilot implementation slice is:

```text
skills/plan/SKILL.md
skills/plan/assets/plan-skeleton.md
skills/plan/assets/milestone.md
skills/plan/assets/current-handoff-summary.md
skills/plan/assets/decision-log-row.md
validator/test fixtures needed for asset resource-map coverage
adapter build/validation proof for packaged assets
token-cost measurement update if needed
behavior-parity fixtures for plan output shape
```

Out of scope for the asset pilot implementation slice:

```text
proposal
proposal-review
spec
spec-review
code-review
verify
pr
references/
scripts/
build-time partials
adapter install roots
lockfile changes
CLI changes
```

---

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PD-001` | `plan` is the only skill modified in the asset pilot implementation slice. |
| `AC-PD-002` | `skills/plan/assets/` contains no more than four asset files. |
| `AC-PD-003` | Every asset has template metadata comments. |
| `AC-PD-004` | `SKILL.md` resource map references every asset with `COPY`, trigger condition, and fields to fill. |
| `AC-PD-005` | Assets contain structural templates, not paragraph-length workflow prose. |
| `AC-PD-006` | No asset requires repository-root internal paths. |
| `AC-PD-007` | Generated adapter output includes the packaged assets. |
| `AC-PD-008` | Behavior-parity evidence shows plan output shape and lifecycle handoff semantics are preserved. |
| `AC-PD-009` | Common-path token-cost delta is measured and recorded. |
| `AC-PD-010` | Cold-read verification passes from installed adapter output. |
| `AC-PD-011` | No generated adapter skill body or asset is hand-edited. |
| `AC-PD-012` | Follow-on adoption for other skills is deferred to a separate proposal or explicit spec amendment. |
| `AC-PD-013` | `current-handoff-summary.md` contains no lifecycle transition rules. |
| `AC-PD-014` | `SKILL.md` retains the handoff consistency rule. |

---

## Open questions

None blocking proposal review.

The spec amendment should still settle exact requirement and acceptance-criteria IDs for the spec input decisions below before implementation begins.

---

## Spec input decisions

The original five proposal questions are answered here as input to the spec amendment. These decisions should be normalized into `specs/skill-contract.md` before implementation relies on them.

| Question | Spec input answer | Rationale |
| --- | --- | --- |
| Token-cost budget for the `plan` common path | Strict no-regression for `SKILL.md`; total `SKILL.md` plus assets may use `+5%` tolerance with rationale and `+10%` hard cap. | The pilot should shrink common-path instructions; total packaged content may grow modestly because assets are loaded only when used. |
| Asset count cap | Exactly four assets for this pilot. | The cap is a forcing function. A fifth asset requires explicit spec amendment or follow-up rationale. |
| Normative asset status | All four shipped assets are normative. `plan-skeleton.md` owns canonical section order, headers, and placeholders; `SKILL.md` keeps only a compact output expectation summary and Resource map entry. | This proves the asset pattern without duplicating full section layout in both files. |
| Resource-map verb | Require literal `COPY` for `assets/`. Reserve `READ` for future `references/` and `RUN` for future `scripts/`. | The verb is part of the contract and should distinguish resource classes deterministically. |
| Asset metadata comments | Require metadata comments in all assets; use the status field to distinguish `normative`, `optional`, `example`, and `deprecated`. | Universal metadata supports drift detection. Status controls which checks apply. |

Additional spec input decisions from adversarial review:

| Question | Spec input answer | Rationale |
| --- | --- | --- |
| What proves `plan` improved, not only that packaging works? | Add separate no-regression and demonstrated-improvement gates. Keep behavior parity as the no-regression gate. Add a required common-path size reduction gate: `SKILL.md` body token count must decrease by at least 15%. Add supporting evidence that the milestone asset is used once per milestone across the behavior-parity baseline corpus. | A pilot that proves mechanism without measurable benefit should not ship. Common-path size reduction is the strongest improvement signal because it is mechanical and script-measurable. |
| What drift signal catches independent edits to `SKILL.md` or `plan-skeleton.md`? | For normative assets, require automated section-set parity checks between the asset and `SKILL.md` references, plus a structural fingerprint in asset metadata that the validator recomputes. Drift is resolved by reverting the structural change or bumping the template version and updating the fingerprint. | Manual version metadata helps authors express intent, but validator-level drift detection is needed to make multi-file skill packages trustworthy. |
| Should review-class follow-ons use `assets/` or `references/`? | Treat `code-review` and other deliberative skills as primarily `references/` candidates, with `assets/` as a small secondary pattern for output skeletons or finding rows. The `plan` asset pilot does not authorize broad assets rollout. | Constructive skills copy repeated structures; deliberative skills mostly read rule-heavy guidance. Pattern choice should follow the dominant content category. |
| Which plans are valid behavior-parity references? | Split the corpus into a contract-era reference corpus and a historical corpus. The reference corpus should include at least three contract-compliant plans and require strict structural parity. Candidate reference plans are `docs/plans/2026-05-18-skill-readability-self-containment.md`, `docs/plans/2026-05-19-published-skill-design-spec-family.md`, and `docs/plans/2026-05-19-published-skill-design-plan-family.md`. The historical corpus should include 3-5 pre-contract plans and require coverage parity only, with gaps recorded in change-local evidence. | Behavior parity must be calibrated to the contract era of the artifact. Older plans are useful for gap analysis but should not be held to current structural requirements. |

Spec acceptance criteria should avoid reusing existing proposal IDs. This proposal already uses `AC-PD-013` and `AC-PD-014` for the handoff asset boundary, so the spec should allocate distinct IDs for common-path size reduction and substructure reusability.

---

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-19 | Use an assets-only progressive-disclosure pilot. | Smallest useful packaged-resource test; avoids scripts/references complexity. | Full `references`/`scripts`/`assets` pilot. |
| 2026-05-19 | Pilot on `plan`. | Strong multi-instance template case, low coupling, many parity examples. | `code-review`, `proposal-review`, `spec-review`. |
| 2026-05-19 | Do not touch settled or in-flight skill pairs. | Avoids reopening settled work and bundling with active rewrites. | Retrofit `proposal`/`proposal-review` or `spec`/`spec-review`. |
| 2026-05-19 | Use `COPY` resource-map convention. | Makes asset use explicit and distinguishes assets from references. | Vague "see assets" wording. |
| 2026-05-19 | Keep behavior parity above token savings. | Quality and lifecycle semantics are higher priority than size reduction. | Optimize primarily for token cost. |
| 2026-05-19 | Seed spec input answers for the five open questions. | Keeps proposal review unblocked while giving the spec amendment concrete budget, asset-count, normative-status, verb, and metadata defaults. | Leave all five questions unresolved until spec drafting. |
| 2026-05-19 | Seed spec input answers for improvement proof, drift detection, follow-on pattern selection, and behavior-parity corpus. | Converts adversarial questions into concrete spec amendment inputs while keeping implementation gated on the spec. | Leave improvement and drift proof undefined until implementation. |

---

## Next artifacts

```text
proposal-review
spec amendment: specs/skill-contract.md
spec-review
plan
plan-review
test-spec amendment
implementation
code-review
explain-change
verify
pr
```

---

## Deferred follow-up candidates

- Proposal for packaged `references/` for rule-heavy skills such as `code-review` or `verify`.
- Proposal for secondary `assets/` in review-class skills only for output skeletons or finding rows.
- Proposal for packaged `scripts/` if deterministic helpers become repeated.
- Proposal for build-time partials if cross-skill duplication remains costly.
- Proposal for retrofitting assets into `proposal`, `proposal-review`, `spec`, and `spec-review`.

### Pattern selection guidance for follow-on skills

- Constructive skills such as `plan`, `proposal`, and `spec` that assemble structured artifacts from repeating substructures should treat `assets/` as the primary packaged-resource pattern.
- Deliberative skills such as `code-review`, `verify`, `proposal-review`, and `spec-review`, where most content is rule-heavy guidance the agent reads to make judgments, should treat `references/` as the primary packaged-resource pattern, with `assets/` as a secondary pattern for output skeletons and finding rows.
- Mixed skills may use both patterns, with the larger content category determining the proposal framing.

---

## Follow-on artifacts

- Proposal-review: [proposal-review-r2](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/proposal-review-r2.md).
- Spec amendment: [Skill Contract](../../specs/skill-contract.md), draft pending spec-review.

---

## Readiness

Accepted for spec amendment. Current downstream stage: `spec-review` for the `specs/skill-contract.md` assets-first plan pilot amendment.

---

## Core invariant

```text
Progressive disclosure is allowed only when it preserves the installed skill as
the user-facing operating contract.

For the first pilot, assets are structural templates copied and filled by the
agent; rules stay in SKILL.md, packaged assets ship with adapters, and behavior
parity outranks token savings.
```
