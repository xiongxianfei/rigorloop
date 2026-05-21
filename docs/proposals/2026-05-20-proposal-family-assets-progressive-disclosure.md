# Proposal: Proposal-Family `assets/` Progressive Disclosure

## Status

accepted

Accepted after clean `proposal-review` round 2.

## Problem

`proposal` and `proposal-review` are among the most visible RigorLoop published skills. They define how new change direction is recorded and how weak or risky proposals are stopped before specification. Their current `SKILL.md` bodies are self-contained and contract-rich, but they still carry large inline output structures that are better treated as packaged copy-and-fill templates.

The current `proposal` skill includes a full proposal output skeleton and detailed artifact-shape guidance for required sections, initial intent preservation, scope budgets, vision fit, standing artifact gates, and handoff behavior. The current `proposal-review` skill likewise includes an output skeleton, review dimensions, material-finding requirements, recording rules, scope-preservation checks, and workflow handoff rules.

The accepted spec-family `assets/` proposal established the current rule for progressive disclosure: assets are copied structures, not hidden rules; `SKILL.md` remains the source of operating rules, stop conditions, lifecycle boundaries, and validation obligations. The prior assets-first pilot also established that packaged resources must remain self-contained, mapped from `SKILL.md`, included in generated adapter output, and behavior-preserving.

The open opportunity is to apply that pattern to the proposal family:

```text
proposal:
  move the full proposal skeleton into assets/

proposal-review:
  move the review result skeleton and material-finding skeleton into assets/
```

The main risk is the same as in earlier asset work: `assets/` must not become a hidden source of rules, review judgment, status values, lifecycle boundaries, or validation policy. The asset design guidance also warns that assets must earn their file; tiny one-line rows usually do not justify asset files because the metadata can outweigh the template body.

## Goals

* Add `assets/` progressive disclosure to `proposal` and `proposal-review`.
* Keep `SKILL.md` as the operating contract for rules, routing, evidence access, lifecycle boundaries, enum values, validation, and handoff.
* Use assets only for substantial copy-and-fill output structures.
* Move the full proposal skeleton out of `skills/proposal/SKILL.md` into `skills/proposal/assets/proposal-skeleton.md`.
* Move the proposal-review result skeleton and material-finding skeleton out of `skills/proposal-review/SKILL.md` into `skills/proposal-review/assets/`.
* Avoid small row-only assets that do not earn their file.
* Require every asset to have an explicit `COPY` resource-map entry.
* Validate that generated skill mirrors and adapter archives include the assets.
* Preserve current behavior: no rule, enum value, stop condition, review dimension, scope-preservation rule, recording rule, output obligation, lifecycle boundary, routing behavior, or representative output behavior changes.
* Record common-path `SKILL.md` token-cost impact separately from total packaged skill footprint.

## Non-goals

* Do not introduce packaged `references/` in this proposal.
* Do not introduce packaged `scripts/` in this proposal.
* Do not introduce build-time partials or include syntax.
* Do not change routing descriptions for `proposal` or `proposal-review`.
* Do not change proposal status values, Vision fit values, initial-goal treatment values, scope-budget treatment values, review status values, recording status values, review-dimension results, or vision-conflict outcomes.
* Do not change the required proposal sections.
* Do not change proposal-review dimensions, material-finding requirements, standing artifact gate rules, scope-preservation rules, recording rules, or handoff behavior.
* Do not change artifact placement rules.
* Do not apply this asset pattern to `spec`, `spec-review`, `test-spec`, `plan`, `code-review`, `verify`, or `pr`.
* Do not change adapter install roots, lockfile semantics, CLI behavior, release archive trust boundaries, or canonical skill source location.
* Do not hand-edit generated adapter output.
* Do not retroactively rewrite legacy adapter archives.

## Vision fit

fits the current vision

This proposal supports RigorLoop's artifact-first model by making two high-visibility published skills easier to inspect and maintain while preserving durable artifact quality. The installed skill remains the user-facing operating contract; assets provide reusable structural templates that are packaged, mapped, validated, and copied into output.

The proposal is falsified if asset extraction causes any of these outcomes:

```text
- proposal or proposal-review behavior changes;
- a rule, enum value, review dimension, stop condition, output obligation,
  recording rule, or lifecycle boundary changes meaning;
- an asset contains hidden normative guidance;
- an asset is referenced but missing from generated output;
- an asset is packaged but not mapped in SKILL.md;
- a final artifact emits unfilled placeholders;
- common-path SKILL.md size grows without approved rationale;
- generated adapter output is hand-edited instead of built from canonical skills.
```

Token reduction is useful only after behavior preservation, self-containment, and adapter parity are proven.

## Priority order

```text
1. Preserve proposal and proposal-review behavior.
2. Preserve published-skill self-containment.
3. Prove assets are packaged and mapped for both skills.
4. Reduce common-path SKILL.md body size.
5. Create a reusable pattern for future proposal-family references/assets work.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Add progressive disclosure for `proposal` | in scope | Goals, Recommended direction |
| Add progressive disclosure for `proposal-review` | in scope | Goals, Recommended direction |
| Use best-practice skill asset design | in scope | Asset contract, Testing |
| Preserve current skill behavior | in scope | Vision fit, Non-goals, Behavior preservation |
| Keep rules in `SKILL.md` | in scope | Asset contract |
| Use assets rather than references/scripts for this slice | in scope | Non-goals, Asset contract |
| Validate generated adapter output | in scope | Testing and acceptance criteria |
| Avoid tiny asset formalism | in scope | Asset contract, Proposed layout |
| References for rule-heavy proposal-review guidance | deferred follow-up | Follow-on artifacts |
| Build-time partials | deferred follow-up | Follow-on artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Add structural `assets/` to `proposal` | core to this proposal | `proposal` is a constructive artifact-producing skill with a full skeleton that earns an asset. |
| Add narrow structural `assets/` to `proposal-review` | core to this proposal | `proposal-review` is deliberative; assets should cover output/result structure only. |
| Validate generated skill mirrors and adapter archives include assets | same-slice dependency | Asset packaging is part of the observable public adapter contract. |
| Add deterministic validator coverage for asset mapping and metadata | same-slice dependency | The proposal depends on proving asset presence, `COPY` mapping, metadata, and no hidden rules. |
| Record behavior-preservation and parity evidence | same-slice dependency | Required to prove the pass is structural, not behavioral. |
| Package `references/` for proposal/proposal-review | separate proposal | References can hide rule-heavy guidance and need their own boundary. |
| Package `scripts/` for proposal/proposal-review | out of scope | No deterministic helper script candidate is selected in this proposal. |
| Build-time partials/includes | separate proposal | This changes authoring/build mechanics and should not be bundled with assets. |
| Apply asset pattern to other lifecycle skills | out of scope | This proposal is limited to `proposal` and `proposal-review`. |

## Context

The current `proposal` skill is constructive: it turns exploration into a reviewable proposal artifact and already exposes required proposal sections, status values, Vision fit handling, scope preservation, scope budget handling, decision-quality checks, workflow handoff, and a full output skeleton.

The current `proposal-review` skill is deliberative: it challenges proposal quality across problem clarity, user value, option diversity, decision rationale, scope, architecture, testability, risk, rollout, and readiness; it also records material findings, scope-preservation results, recording status, review status, and handoff boundaries.

The accepted asset design guidance is clear: full skeleton assets can earn a file, multi-field blocks can earn a file when field order or completeness is easy to get wrong, and one-line rows usually do not earn a file when `SKILL.md` already carries the format rule.

This proposal therefore treats the two skills differently:

```text
proposal:
  constructive artifact-producing skill;
  full skeleton asset is appropriate.

proposal-review:
  deliberative review skill;
  assets should be narrow result/finding structures;
  review judgment and rules remain in SKILL.md.
```

## Proof route

This proposal requires a focused test-spec amendment for proposal-family asset checks before implementation begins.

A spec amendment is conditional on whether the existing skill-contract asset rules already cover:

```text
- multi-skill asset rollout;
- full-skeleton asset boundaries;
- deliberative review-skill asset restrictions;
- generated-output asset presence;
- behavior-preservation evidence for asset extraction.
```

Approved route:

```text
1. focused test-spec amendment is required;
2. spec amendment is conditional on a documented skill-contract gap;
3. implementation must not begin until the test-spec amendment is approved.
```

As with the `plan` skeleton, `proposal-skeleton.md` is expected to increase total packaged footprint while reducing the common-path `SKILL.md` body. This is acceptable for a skeleton asset; the justification is common-path reduction and readability, not total-token reduction. Record P, the fraction of proposal invocations that author a fresh proposal versus amend an existing proposal, to contextualize per-invocation cost.

## Options considered

### Option 1: Do nothing

Keep both skills flat after the readability/self-containment pass.

**Pros**

* No implementation risk.
* No adapter packaging work.
* No new validator surface.

**Cons**

* The output skeletons remain in the common path.
* Progressive disclosure remains less proven for proposal-family skills.
* The pair lacks the packaged-template pattern now used by other skill families.

### Option 2: Add `assets/`, `references/`, and `scripts/` together

Introduce the whole progressive-disclosure model in one pass.

**Pros**

* Maximum potential reduction of `SKILL.md`.
* Could separate rule-heavy guidance into references.

**Cons**

* Too broad.
* `references/` can hide normative rules.
* `scripts/` are not justified by the current workflow.
* Harder to isolate regressions.
* Contradicts the assets-first pattern used in prior accepted work.

### Option 3: Add assets only to `proposal`

Skip `proposal-review` because it is deliberative.

**Pros**

* Lowest review-governance risk.
* Strong fit for copy-and-fill output structure.
* Touches only one skill.

**Cons**

* Leaves the proposal family inconsistent.
* Misses a clear review-result and material-finding skeleton candidate.
* Does not prove safe asset use for a review-class skill in this family.

### Option 4: Add assets to both skills, but keep `proposal-review` assets narrow

Add one full skeleton asset to `proposal`; add only result/finding skeleton assets to `proposal-review`.

**Pros**

* Treats the family consistently.
* Keeps rule-heavy review judgment in `SKILL.md`.
* Extracts only substantial copy-and-fill structures.
* Avoids references/scripts.
* Applies accepted asset lessons without broadening the scope.

**Cons**

* Touches two high-visibility skills.
* Requires per-skill preservation proof.
* Requires strict review-class asset boundary enforcement.

## Recommended direction

Choose **Option 4**.

Add `assets/` to both `proposal` and `proposal-review`, with different scopes by skill type.

```text
proposal:
  full proposal skeleton asset

proposal-review:
  review result skeleton asset
  material finding skeleton asset
```

The principle:

```text
Assets are copied structures, not hidden rules.
```

## Asset contract

### Asset definition

For this proposal, an asset is:

```text
a packaged, skill-local, copy-and-fill structural template that the agent uses
to produce the skill-owned artifact, substantial enough to justify a separate file.
```

An asset is not:

```text
- a rule reference;
- a review rubric;
- a decision matrix;
- a validation checklist;
- a tutorial;
- a hidden source of enum values;
- a substitute for SKILL.md operating instructions;
- a one-line row whose format is already governed inline.
```

Smell test:

```text
If the required metadata header is larger than the template body, the asset
probably does not earn a file.
```

This follows the asset design guidance that full skeletons and multi-field blocks can earn a file, while trivial rows usually should stay inline.

### Resource verbs

Use the established resource-map verb convention:

| Verb | Resource class | In this proposal? |
| --- | --- | ---: |
| `COPY` | `assets/` | yes |
| `READ` | `references/` | no |
| `RUN` | `scripts/` | no |

Each asset entry in `SKILL.md` should use `COPY`.

### Asset metadata

Every asset should include metadata comments:

```md
<!-- Template: <template-id> -->
<!-- Skill: <skill-name> -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/<skill-name>/SKILL.md -->
```

Allowed statuses:

```text
normative
optional
example
deprecated
```

For this proposal, use only:

```text
normative
optional
```

### Placeholder policy

Allowed placeholder styles:

```text
<field-name>
[FILL IN]
TODO:
```

Disallowed:

```text
empty required fields
realistic filler prose
lorem ipsum
"your text here"
```

`SKILL.md` must instruct the agent not to emit unfilled placeholders.

## Review-class asset boundary

`proposal-review` is a deliberative review skill.

Its assets may contain only:

```text
- headings;
- field labels;
- placeholders;
- short fill hints.
```

Its assets must not contain:

```text
- review-dimension definitions;
- severity policy;
- material-finding sufficiency rules;
- safe-resolution decision rules;
- recording-status rules;
- scope-preservation rules;
- Vision fit review rules;
- standing artifact gate rules;
- architecture/risk/testability review guidance;
- security/privacy or rollout examples.
```

Those rules remain in `SKILL.md`.

The `proposal-review` skill currently owns review dimensions, Vision fit review, standing artifact gate review, scope preservation review, scope-budget review, material-finding requirements, recording status, and handoff rules in the skill body. This proposal must not move that judgment into assets.

## Proposal-review asset validation boundary

For `proposal-review` assets, validation must use an explicit structural-label allowlist and deterministic forbidden review-policy label checks.

Allowed structural labels are limited to fields needed by `review-result-skeleton.md` and `material-finding.md`, including:

* Review status
* Material findings
* Recording status
* Recording blocker
* Review record
* Review log
* Review resolution
* Open blockers
* Immediate next stage
* Review dimensions
* Scope-preservation result
* Recommended edits
* Recommendation
* Finding ID
* Severity
* Location
* Evidence
* Required outcome
* Safe resolution path
* needs-decision rationale

Forbidden labels or prose include:

* Severity policy
* Material-finding sufficiency
* Safe-resolution decision rule
* Recording-status rules
* Scope-preservation rules
* Scope-budget review
* Vision fit review
* Standing artifact gate review
* Review dimension guidance

## Proposed asset layout

### `proposal`

```text
skills/proposal/
  SKILL.md
  assets/
    proposal-skeleton.md
```

| Asset | Use |
| --- | --- |
| `proposal-skeleton.md` | Starting structure for a new proposal artifact. |

#### Boundary

`proposal-skeleton.md` may own the full output structure only if `skills/proposal/SKILL.md` keeps:

```text
- compact output expectation summary;
- required proposal section table;
- proposal status enum;
- Vision fit enum and rules;
- standing artifact gates;
- scope preservation rules;
- scope budget rules;
- decision quality checklist;
- workflow handoff behavior.
```

Do not duplicate the full skeleton in both `SKILL.md` and the asset.

Small table rows such as initial-intent rows, scope-budget rows, decision-log rows, or risk rows stay inline unless a later plan records why they earn files.

#### Conditional proposal-section boundary

`assets/proposal-skeleton.md` must preserve trigger-based proposal sections without changing their conditional behavior.

The asset may include conditional blocks only when they are clearly labeled as conditional. Otherwise, `SKILL.md` must instruct the agent to insert the conditional sections when their triggers apply.

Preserve these trigger-based sections:

* `Initial intent preservation`: include when the request is broad, multi-part, or materially revised.
* `Scope budget`: include when the proposal is broad, multi-workstream, touches multiple lifecycle families, generated output, workflow policy, release policy, or validation policy.
* Other conditional sections remain governed by `SKILL.md`.

The asset must not make conditional sections mandatory for every proposal, and must not omit the ability to add them when triggered.

### `proposal-review`

```text
skills/proposal-review/
  SKILL.md
  assets/
    review-result-skeleton.md
    material-finding.md
```

| Asset | Use |
| --- | --- |
| `review-result-skeleton.md` | Overall result block for a proposal-review artifact. |
| `material-finding.md` | One material finding block with required fields. |

#### Boundary

`proposal-review` assets must not contain review guidance. They contain output shape only.

Keep these in `SKILL.md`:

```text
- review dimensions table;
- review dimension result enum;
- Vision fit review rules;
- vision conflict outcome enum;
- standing artifact gate review rules;
- scope preservation review rules;
- scope budget review rules;
- material-finding sufficiency rule;
- recording status enum;
- review status enum;
- isolation and recording rules;
- workflow handoff behavior.
```

Do not add a `review-dimension-row.md` asset. The review-dimension table is a fixed deliberative checklist, not a copy-and-fill structure.

## Resource map pattern

Each touched `SKILL.md` should include a resource map entry under that skill's `## Resource map` heading shaped like:

```md
- COPY `assets/<asset>.md` when <specific condition>.
  Fill: <field list>.
  Do not emit unfilled placeholders.
```

### `proposal` resource map

Recommended entry:

```md
- COPY `assets/proposal-skeleton.md` when creating a new proposal artifact.
  Fill the core proposal sections: title, status, problem, goals, non-goals, Vision fit, context,
  options considered, recommended direction, expected behavior changes,
  architecture impact, testing and verification strategy, rollout and rollback,
  risks and mitigations, open questions, decision log, next artifacts,
  follow-on artifacts, and readiness. Add conditional sections such as
  `Initial intent preservation` and `Scope budget` when the triggers in this
  skill apply.
  Do not emit unfilled placeholders.
```

### `proposal-review` resource map

Recommended entries:

```md
- COPY `assets/review-result-skeleton.md` when producing the proposal-review
  result artifact.
  Fill: review status, material findings, recording status, recording blocker,
  review record, review log, review resolution, open blockers, immediate next
  stage, review dimensions, scope-preservation result, recommended edits, and
  recommendation.
  Do not emit unfilled placeholders.

- COPY `assets/material-finding.md` once per material finding.
  Fill: finding ID, severity, location, evidence, required outcome, and safe
  resolution path or needs-decision rationale.
  Do not emit unfilled placeholders.
```

## Output skeleton boundary

For each skill, choose one source of the full output skeleton.

Preferred approach:

```text
Full skeleton lives in assets/<skeleton>.md.
SKILL.md keeps compact output expectation summary.
SKILL.md resource map tells the agent when to COPY the full skeleton.
```

Do not duplicate the full skeleton in both `SKILL.md` and the asset.

If code review finds that a full skeleton asset hides too much contract surface, fallback is allowed for that skill:

```text
keep the full skeleton inline
use assets only for repeated substructures
record the fallback in behavior-preservation evidence
```

## Behavior preservation boundary

This proposal is an asset extraction pass, not a behavior change.

For each extraction, record a preservation matrix:

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `proposal` | proposal skeleton section set | `SKILL.md` output skeleton | `assets/proposal-skeleton.md` | same section set and placeholders |
| `proposal` | initial intent preservation section | `SKILL.md` conditional section | `SKILL.md` trigger plus optional labeled asset block | trigger preserved; not mandatory for every proposal |
| `proposal` | scope budget section | `SKILL.md` conditional section | `SKILL.md` trigger plus optional labeled asset block | trigger preserved; not mandatory for every proposal |
| `proposal-review` | review result fields | `SKILL.md` output skeleton | `assets/review-result-skeleton.md` | same result field set |
| `proposal-review` | material finding fields | `SKILL.md` output skeleton / material-finding rules | `assets/material-finding.md` | same required field set |

A structural pass is insufficient if the extraction changes field names, field obligations, enum values, review status, recording status, or handoff semantics.

## Expected behavior changes

* `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` become more common-path focused.
* Each skill ships a skill-local `assets/` directory.
* Generated adapter output contains each referenced asset.
* Every packaged asset is mapped from `SKILL.md`.
* Full output skeletons move to assets; rules remain in `SKILL.md`.
* Representative behavior parity from the pinned canonical skill baseline remains intact.
* No routing behavior changes.
* No references or scripts are introduced.

## Architecture impact

| Surface | Impact |
| --- | --- |
| `skills/proposal/SKILL.md` | Adds resource map; may replace full inline skeleton with compact summary plus asset pointer. |
| `skills/proposal/assets/proposal-skeleton.md` | New packaged proposal skeleton. |
| `skills/proposal-review/SKILL.md` | Adds resource map; preserves review rules and dimensions. |
| `skills/proposal-review/assets/review-result-skeleton.md` | New packaged review result skeleton. |
| `skills/proposal-review/assets/material-finding.md` | New packaged material finding skeleton. |
| `scripts/skill_validation.py` | May need asset coverage checks for proposal-family assets. |
| `scripts/test-skill-validator.py` | Add positive and negative fixture coverage. |
| `scripts/build-skills.py` | Must preserve asset directories in generated skill mirrors. |
| `scripts/build-adapters.py` | Must package assets in adapter archives. |
| `scripts/validate-adapters.py` | Must verify asset presence and parity. |
| Adapter roots | No change. |
| Lockfile schema | No change. |
| CLI behavior | No change. |

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `PFA-001` | `proposal` and `proposal-review` each have a resource map for every packaged asset. |
| `PFA-002` | Each resource-map entry uses literal `COPY`. |
| `PFA-003` | Each asset has required metadata comments. |
| `PFA-004` | Each asset has allowed template status. |
| `PFA-005` | Assets contain visible placeholders and no disallowed filler prose. |
| `PFA-006` | Assets do not contain hidden normative rules, stop conditions, enum definitions, review-dimension explanations, scope-preservation rules, Vision fit rules, recording rules, or lifecycle boundaries. |
| `PFA-007` | Assets do not require repository-root internal paths. |
| `PFA-008` | Generated skill mirror includes all proposal-family assets. |
| `PFA-009` | Generated adapter archives include all proposal-family assets. |
| `PFA-010` | No generated adapter skill body or asset is hand-edited. |
| `PFA-011` | Preservation matrices prove source-to-asset field parity. |
| `PFA-012` | Representative behavior parity remains unchanged from the pinned canonical skill baseline. |
| `PFA-013` | No unfilled placeholders appear in representative output. |
| `PFA-014` | Common-path `SKILL.md` token count is measured separately from total packaged skill footprint, and P is recorded for each asset to explain expected per-invocation cost. |
| `PFA-015` | Cold-read confirms a user can understand when to use each asset from installed skill output alone. |
| `PFA-016` | `proposal-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints. |
| `PFA-017` | A change-local baseline summary maps pinned skill structures to planned assets and identifies which rules, enums, stops, review dimensions, and recording obligations remain in `SKILL.md`. |
| `PFA-018` | `proposal-review` asset validation uses an explicit structural-label allowlist and rejects forbidden review-policy labels such as `Recording-status rules`, `Material-finding sufficiency`, `Vision fit review`, and `Scope-preservation rules`. |
| `PFA-019` | `proposal-skeleton.md` preserves trigger-based conditional sections without making them mandatory for every proposal. |

Fixture expectations for `PFA-018`:

```text
valid:   `- Recording status: <recording status>`
valid:   `- Severity: <severity>`
invalid: `- Recording-status rules: <rules>`
invalid: `- Material-finding sufficiency: <rule>`
invalid: `- Vision fit review: <guidance>`
invalid: `- Scope-preservation rules: <rules>`
```

Suggested validation commands:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --output-dir <tmpdir>
python scripts/validate-adapters.py --root <tmpdir> --version <version>
python scripts/measure-skill-tokens.py
git diff --check --
```

Use the repository's current version value for `<version>`.

If lifecycle artifacts are touched:

```bash
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/proposals/<proposal>.md \
  --path docs/plans/<plan>.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/changes/<change-id>/review-log.md \
  --path docs/changes/<change-id>/review-resolution.md
```

## Generated output proof boundary

Required:

* generated skill mirror includes each proposal-family asset;
* temporary generated adapter output includes each asset;
* adapter validation passes against the temporary generated output;
* no generated body or asset is hand-edited.

Tracked-tree adapter checks are required when the repository's tracked expanded adapter layout supports them. If known stale tracked-tree debt remains, record a deferral with rationale, but temporary generated archive proof remains mandatory.

## Baseline summary artifact

Before implementation, create a change-local baseline summary:

```text
docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md
```

It must record, per skill:

* source commit or branch point;
* exact canonical source paths;
* source file hashes or section-level normalized hashes;
* existing full skeleton section set;
* repeated substructure fields to extract;
* extracted asset source ranges or stable headings;
* conditional sections that remain governed by `SKILL.md`;
* closed enums that remain in `SKILL.md`;
* scope-preservation and scope-budget rules that remain in `SKILL.md`;
* Vision fit and standing artifact gate rules that remain in `SKILL.md`;
* review dimensions and recording obligations that remain in `SKILL.md`;
* source location for each extracted asset.

This artifact feeds the preservation matrix.

The phrase "current canonical skill state" means the pinned baseline recorded in this artifact, not whatever state happens to exist when implementation runs.

## Behavior-parity baseline

Use the pinned baseline from `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md` as the behavior baseline.

| Skill | Baseline proof to preserve |
| --- | --- |
| `proposal` | Same required section set, same proposal status values, same Vision fit values, same initial-intent and scope-budget handling, same handoff boundary. |
| `proposal-review` | Same review dimensions, same review dimension result values, same material-finding field set, same review status values, same recording status values, same scope-preservation behavior, same recording behavior. |

The current `proposal` skeleton and proposal required-section table provide the baseline shape for the proposal asset. The current `proposal-review` skeleton and material-finding requirements provide the baseline shape for review assets.

## Rollout and rollback

### Rollout

1. Approve proposal.
2. Complete proof-route decision.
3. Amend `specs/skill-contract.md` only if existing asset rules do not cover proposal-family or review-class asset restrictions.
4. Amend the matching test spec for proposal-family asset packaging and preservation.
5. Create the change-local baseline summary.
6. Plan per-skill implementation milestones:

   * M1: validator/test-spec amendment and baseline summary.
   * M2: `proposal` assets.
   * M3: `proposal-review` assets.
   * M4: generated adapter proof and family closeout, if needed.
7. Record a per-asset justification in the plan, including expected usage count and why the asset earns its place.
8. Implement one skill at a time.
9. Run code review per milestone.
10. Run generated skill and adapter validation.
11. Record explain-change, verify, and PR handoff.

### Rollback

* Reinline asset content into the owning `SKILL.md`.
* Remove the skill's `assets/` directory.
* Preserve generic validator improvements if still valid.
* Rebuild generated mirrors and adapter archives from canonical skills.
* Do not alter adapter roots, lockfiles, or CLI behavior.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Assets hide proposal or review behavior. | Keep rules, dimensions, gates, enums, recording obligations, and lifecycle boundaries in `SKILL.md`. |
| `proposal-review` assets become review guidance. | Restrict review assets to field labels and placeholders. |
| Full skeleton asset removes too much visible contract from `SKILL.md`. | Keep compact output expectation summary in `SKILL.md`; allow inline fallback if needed. |
| Adapter output misses assets. | Require generated adapter archive validation. |
| Asset placeholders leak into final output. | Validate representative outputs for no unfilled placeholders. |
| Common-path size reduction is overstated. | Measure `SKILL.md` separately from total packaged footprint. |
| Current behavior parity regresses. | Use change-local baseline and preservation matrices. |
| Validator overblocks legitimate assets. | Use deterministic checks and avoid broad semantic scoring. |
| Scope creeps into references/scripts. | Keep those as deferred follow-ups. |
| Tiny assets add ceremony. | Use the "asset earns its file" rule and metadata-to-content smell test. |

## First-slice boundary

This proposal's first implementation sequence is limited to:

```text
skills/proposal/SKILL.md
skills/proposal/assets/*.md
skills/proposal-review/SKILL.md
skills/proposal-review/assets/*.md
validator/test fixtures needed for asset coverage
generated skill and adapter validation proof
behavior-preservation and behavior-parity evidence
lifecycle artifacts for this change
```

Out of scope:

```text
spec
spec-review
test-spec
plan
code-review
verify
pr
references/
scripts/
build-time partials
adapter install roots
lockfiles
CLI behavior
produced-artifact readability changes
```

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PFA-001` | `proposal` has `assets/proposal-skeleton.md`. |
| `AC-PFA-002` | `proposal-review` has `assets/review-result-skeleton.md` and `assets/material-finding.md`. |
| `AC-PFA-003` | Each asset has required template metadata comments. |
| `AC-PFA-004` | Each asset has a matching `COPY` resource-map entry in the owning `SKILL.md`. |
| `AC-PFA-005` | No asset contains hidden normative rules, enum definitions, stop conditions, review-dimension guidance, scope-preservation rules, Vision fit rules, standing artifact gate rules, recording rules, or lifecycle boundaries. |
| `AC-PFA-006` | `proposal-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints. |
| `AC-PFA-007` | Each full skeleton asset has a corresponding compact output expectation summary in `SKILL.md`. |
| `AC-PFA-008` | Preservation matrices prove source-to-asset field parity for every extracted structure. |
| `AC-PFA-009` | Representative behavior-parity evidence matches the pinned baseline recorded in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`. |
| `AC-PFA-010` | Generated skill mirrors include all proposal-family assets. |
| `AC-PFA-011` | Generated adapter archives include all proposal-family assets. |
| `AC-PFA-012` | No generated adapter body or asset is hand-edited. |
| `AC-PFA-013` | Common-path `SKILL.md` token counts are recorded separately from packaged asset footprints, with P recorded for each asset and explicit acknowledgement that `proposal-skeleton.md` may increase total packaged footprint while still being justified by readability. |
| `AC-PFA-014` | Cold-read verification confirms asset usage is understandable from installed adapter output alone. |
| `AC-PFA-015` | Change-local baseline summary maps pinned skill structures to planned assets and to the rules, enums, review dimensions, recording obligations, and handoff boundaries that remain in `SKILL.md`. |
| `AC-PFA-016` | `proposal-review` asset validation uses an explicit structural-label allowlist and deterministic forbidden-label checks for review-policy terms. |
| `AC-PFA-017` | `proposal-skeleton.md` preserves conditional sections such as `Initial intent preservation` and `Scope budget` as trigger-based sections, not universal required sections. |

## Open questions

None for proposal-review.

Resolved decisions:

* Use `assets/` only; defer `references/` and `scripts/`.
* Use one full skeleton asset for `proposal`.
* Use two narrow assets for `proposal-review`: result skeleton and material-finding skeleton.
* Do not add row-only assets for initial intent, scope budget, decision log, or review dimensions.
* Keep all rules, enums, gates, review dimensions, and recording obligations in `SKILL.md`.
* Require generated skill mirror proof and temporary generated adapter archive proof.
* Use a pinned source commit, canonical source paths, and source hashes or section hashes as the behavior baseline, summarized in a change-local baseline artifact.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-20 | Continue asset work for proposal-family skills. | Current skills are stable, self-contained, and have clear output skeletons that can be extracted. | Keep them flat indefinitely. |
| 2026-05-20 | Use assets only. | Assets are the proven progressive-disclosure resource class; references and scripts have separate risks. | Add references/scripts in same slice. |
| 2026-05-20 | Apply to both `proposal` and `proposal-review`. | Treats the proposal family consistently while keeping review assets narrow. | Only `proposal`; only `proposal-review`. |
| 2026-05-20 | Keep `proposal-review` assets narrow. | Review-class skills are deliberative; assets must not become hidden review guidance. | Move review dimensions or review policies into assets. |
| 2026-05-20 | Avoid tiny row assets. | Asset design guidance says one-line rows usually do not earn files. | Add separate row files for every small table. |
| 2026-05-20 | Pin the behavior baseline in a change-local baseline artifact. | Reviewers need an exact source commit, canonical source paths, and source hashes or section hashes rather than a time-dependent "current" baseline. | Rely on whatever canonical skill text exists when implementation starts. |

## Next artifacts

```text
spec-review for specs/proposal-family-assets-progressive-disclosure.md
test-spec for proposal-family asset checks
spec amendment only if existing asset contract is insufficient
spec-review if a spec amendment is created
plan
plan-review
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

* Proposal-review R2: `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md`.
* Feature spec: `specs/proposal-family-assets-progressive-disclosure.md`.
* Deferred proposal for packaged `references/` in `proposal-review` if rule-heavy guidance needs conditional loading.
* Deferred proposal for packaged `references/` in `proposal` if Vision fit, standing artifact gates, or scope-budget rules become too large for common-path `SKILL.md`.
* Deferred proposal for build-time partials to reduce duplicated rule text across review-class skills.
* Deferred proposal for review-class asset/reference split across `proposal-review`, `spec-review`, and `code-review`.

## Readiness

Accepted; downstream feature spec created at `specs/proposal-family-assets-progressive-disclosure.md`.

## Core invariant

```text
Proposal-family assets are copied structures, not hidden rules.

`proposal` and `proposal-review` may extract reusable skeletons into packaged
assets only if the installed skills remain self-contained, generated adapters
include the assets, and every rule, enum value, review dimension, gate,
recording obligation, lifecycle boundary, and representative output behavior
remains unchanged.
```
