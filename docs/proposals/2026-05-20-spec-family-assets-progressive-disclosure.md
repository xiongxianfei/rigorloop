# Proposal: Spec-Family `assets/` Progressive Disclosure

## Status

accepted

Accepted after clean `proposal-review` round 2.

## Problem

PR #79 merged the spec-family readability pass. It made `spec`, `spec-review`, and `test-spec` easier to scan without changing behavior: `spec` and `test-spec` required-section guidance became tables, `spec-review` review dimensions became a table, and changed closed enums were centralized. The PR also recorded preservation matrices, behavior parity, generated-adapter proof, and final verification for the presentation-only pass. See [PR #79](https://github.com/xiongxianfei/rigorloop/pull/79).

That leaves the next natural follow-up: apply the proven `assets/` progressive-disclosure pattern to the spec family.

The earlier accepted assets-first pilot deliberately started with `plan`, used `assets/` only, kept rules in `SKILL.md`, and treated assets as structural templates copied and filled by the agent. It explicitly excluded `proposal`, `proposal-review`, `spec`, and `spec-review` from that first pilot to avoid reopening settled or in-flight skill rewrites.

Now the spec-family readability work has landed, so `spec`, `spec-review`, and `test-spec` share a cleaner baseline. The open opportunity is to move reusable output structures out of the common-path skill body and into packaged skill-local assets, while preserving the installed skill as the user-facing operating contract.

The main risk is scope confusion. `assets/` must not become a hiding place for rules, review judgment, validation obligations, or lifecycle boundaries. For the spec family, assets should be used only for copy-and-fill structural templates.

## Goals

- Extend the already-shipped assets-first pattern from `plan` to the spec family.
- Add skill-local `assets/` for `spec`, `spec-review`, and `test-spec`.
- Keep `SKILL.md` as the source of operating rules, routing, stop conditions, claim boundaries, and validation obligations.
- Use assets only for structural templates that the agent copies and fills.
- Validate that every asset is present in generated adapter output.
- Validate that every asset has an explicit `COPY` resource-map entry in the owning `SKILL.md`.
- Preserve the behavior achieved by PR #79: no rule, enum value, stop condition, output obligation, routing behavior, lifecycle boundary, or representative output behavior changes.
- Record common-path `SKILL.md` token-cost impact separately from packaged asset content.
- Avoid introducing `references/`, `scripts/`, build-time partials, or produced-artifact readability changes in this proposal.

Priority order:

```text
1. Preserve spec-family behavior from PR #79.
2. Preserve published-skill self-containment.
3. Prove assets are packaged and mapped for all three spec-family skills.
4. Reduce common-path SKILL.md body size.
5. Create a reusable pattern for future spec-family references/assets work.
```

## Non-goals

- Do not introduce packaged `references/`.
- Do not introduce packaged `scripts/`.
- Do not introduce build-time partials or include syntax.
- Do not change routing descriptions.
- Do not change any normative rule, stop condition, enum value, output obligation, review dimension, coverage obligation, or lifecycle boundary.
- Do not change the readability of produced specs, produced reviews, or produced test-spec artifacts beyond preserving existing output structure through assets.
- Do not change adapter install roots, lockfile semantics, CLI behavior, release archive trust boundaries, or canonical skill source location.
- Do not hand-edit generated adapter output.
- Do not retroactively rewrite legacy adapter archives.
- Do not apply the asset pattern to unrelated lifecycle skills in this proposal.

## Vision fit

fits the current vision

This proposal supports RigorLoop's artifact-first model by making installed skills easier to inspect and maintain while preserving durable artifact quality. The skill remains the operating contract; assets provide reusable structural templates that are packaged, mapped, validated, and copied into output.

The proposal is falsified if the asset work causes any of these outcomes:

```text
- a rule, stop condition, enum value, output obligation, review dimension,
  coverage rule, or lifecycle boundary changes meaning;
- an asset contains hidden normative guidance;
- an asset is referenced but missing from generated adapter output;
- an asset is packaged but not mapped in SKILL.md;
- a final artifact emits unfilled placeholders;
- behavior parity from PR #79 regresses;
- common-path SKILL.md size grows without an approved rationale;
- generated adapter output is hand-edited instead of built from canonical skills.
```

Token reduction is valuable only after behavior preservation, self-containment, and adapter parity are proven.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Continue `assets/` work after PR #79 | in scope | Problem, Goals |
| Apply asset work to `spec` | in scope | Recommended direction |
| Apply asset work to `spec-review` | in scope | Recommended direction |
| Apply asset work to `test-spec` | in scope | Recommended direction |
| Preserve PR #79 behavior | in scope | Vision fit, Testing and Verification Strategy |
| Use assets rather than references or scripts | in scope | Non-goals, Asset Contract |
| Keep rules in `SKILL.md` | in scope | Asset Contract |
| Validate generated adapter output | in scope | Testing and Verification Strategy, Acceptance Criteria |
| Avoid broad packaging mechanisms | in scope | Non-goals |
| Produced-artifact readability | deferred follow-up | Scope Budget, Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Add structural `assets/` to `spec` | core to this proposal | `spec` is a constructive artifact-producing skill and is a strong candidate for skeleton and repeated-row assets. |
| Add narrow structural `assets/` to `spec-review` | core to this proposal | The family should prove review-class output skeleton assets without moving review judgment or fixed review-dimension structure into assets. |
| Add structural `assets/` to `test-spec` | core to this proposal | `test-spec` is a constructive artifact-producing skill and should mirror the spec-family asset pattern. |
| Validate generated skill mirrors and adapter archives include assets | same-slice dependency | Asset packaging is part of the observable public adapter contract. |
| Add deterministic validator coverage for asset mapping and metadata | same-slice dependency | The proposal depends on proving asset presence, `COPY` mapping, and metadata conventions. |
| Record behavior-preservation and parity evidence | same-slice dependency | This is required to prove the pass is structural, not behavioral. |
| Package `references/` for spec-family skills | separate proposal | References have different risk because they can hide judgment and rules. |
| Package `scripts/` for spec-family skills | separate proposal | Scripts introduce executable-resource and validation concerns. |
| Introduce build-time partials or include syntax | separate proposal | That changes the authoring/build mechanism and is outside the assets-only slice. |
| Improve produced spec or test-spec artifact readability | separate proposal | Produced artifact readability is different from moving existing output structures into assets. |
| Apply the asset pattern to unrelated lifecycle skills | out of scope | This proposal is limited to `spec`, `spec-review`, and `test-spec`. |

## Context

PR #79's merged summary says the spec-family readability pass tabulated required-section guidance, review dimensions, and coverage rules; centralized changed closed enums; recorded preservation and parity evidence; and listed spec-family packaging using assets or references as a follow-up.

The accepted assets-first pilot established the baseline pattern:

```text
assets/ only
structural templates copied and filled by the agent
SKILL.md remains the execution contract and resource map
no references/
no scripts/
no build-time partials
behavior parity outranks token savings
```

It also defined a useful distinction: constructive skills that assemble structured artifacts are stronger candidates for `assets/`, while deliberative review skills are often stronger candidates for `references/`, with `assets/` only for output skeletons or rows.

This proposal applies that distinction carefully:

- `spec` and `test-spec` are constructive artifact-producing skills, so they are good `assets/` candidates.
- `spec-review` is deliberative, so its asset use should be narrow: output skeletons, review-result blocks, and material-finding structures only. Review judgment and review dimensions stay in `SKILL.md`.

## Proof route

This proposal proceeds through a focused test-spec amendment for spec-family asset checks.

A spec amendment is required only if the existing skill-contract asset rules do not already cover multi-skill asset rollout, full-skeleton asset boundaries, or review-class asset restrictions.

Implementation must not begin until the plan names one approved route:

1. existing skill-contract rules plus an approved test-spec amendment are sufficient;
2. spec amendment plus test-spec amendment packet is approved.

Recommended decision: require the test-spec amendment, and keep the spec amendment conditional on the current skill-contract coverage assessment.

## Options considered

### Option 1: Do nothing

Keep the spec-family skills flat after PR #79.

Pros:

- No new risk.
- No adapter packaging work.
- No additional validation surface.

Cons:

- The PR #79 follow-up remains unaddressed.
- Reusable output skeletons stay in common-path `SKILL.md`.
- The asset pattern remains proven only for `plan`.
- Future authors lack a spec-family packaging example.

### Option 2: Add `assets/`, `references/`, and `scripts/` to the spec family together

Use the whole progressive-disclosure model at once.

Pros:

- Exercises the full resource system.
- Could reduce `SKILL.md` size more aggressively.
- Could move long guidance out of the common path.

Cons:

- Too broad.
- `references/` can hide rules and judgment.
- `scripts/` introduce executable-resource and command-validation concerns.
- Harder to isolate regressions.
- Contradicts the earlier staged approach.

### Option 3: Add assets only to constructive skills: `spec` and `test-spec`

Skip `spec-review` for now.

Pros:

- Lowest behavior risk.
- Strong fit for copy-and-fill templates.
- Avoids review-class governance risk.

Cons:

- Leaves the spec-family package inconsistent.
- Does not create a narrow asset pattern for review-class output skeletons.
- Misses useful material-finding and review-result skeleton candidates.

### Option 4: Add assets to all three spec-family skills, but keep review-skill assets narrow

Add `assets/` to `spec`, `spec-review`, and `test-spec`, with a stricter asset boundary for `spec-review`.

Pros:

- Treats the family consistently.
- Builds directly on PR #79.
- Proves asset packaging across constructive and review-class skills.
- Keeps review judgment in `SKILL.md`.
- Still avoids `references/` and `scripts/`.

Cons:

- Touches three skill directories.
- Needs per-skill behavior-parity proof.
- Requires careful asset contract enforcement so `spec-review` assets do not become hidden review guidance.

## Recommended direction

Choose Option 4.

Add `assets/` to all three spec-family skills, but use different asset scopes by skill type.

```text
spec:
  assets for spec skeleton and repeated requirement/decision structures

spec-review:
  assets only for result/review-record/finding skeletons
  no review-dimension guidance moved into assets

test-spec:
  assets for test-spec skeleton, test-case block, coverage-map row/block
```

The principle:

```text
Assets are copied structures, not hidden rules.
```

## Per-skill skeleton decision

| Skill | Decision | Boundary |
|---|---|---|
| `spec` | Use `assets/spec-skeleton.md` as the full output skeleton. | `SKILL.md` keeps compact output expectations, owns rules/enums/stop conditions, and maps the skeleton with `COPY`; trivial row formats stay inline. |
| `spec-review` | Use only `review-result-skeleton.md` and `review-finding.md`. | Keep review dimensions, review-dimension table structure, review guidance, verdict enum, and recording obligations in `SKILL.md`. |
| `test-spec` | Use `assets/test-spec-skeleton.md` as the full output skeleton, plus test-case and coverage-map substructure assets. | `SKILL.md` keeps compact output expectations, owns rules/enums/stop conditions, and maps the skeleton with `COPY`. |

If a full skeleton asset hides too much contract surface during code review, fallback is allowed for that skill: keep the full skeleton inline and use assets only for repeated substructures.

## Asset contract

For this proposal, an asset is:

```text
a packaged, skill-local, copy-and-fill structural template that the agent uses
to produce the skill-owned artifact, substantial enough to justify a separate
file.
```

An asset is not:

```text
- a rule reference;
- a review rubric;
- a decision matrix;
- a validation checklist;
- a tutorial;
- a hidden source of enum values;
- a substitute for SKILL.md operating instructions.
- a one-line row whose format is already governed inline.
```

Smell test: if the metadata header is larger than the template body, the asset
probably does not earn a file.

Use the established resource-map verb convention:

| Verb | Resource class | In this proposal? |
|---|---|---|
| `COPY` | `assets/` | yes |
| `READ` | `references/` | no |
| `RUN` | `scripts/` | no |

Each asset entry in `SKILL.md` should use `COPY`.

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

`SKILL.md` should instruct the agent not to emit unfilled placeholders.

## Review-class asset boundary

For `spec-review`, assets may contain only:

- headings;
- field labels;
- placeholders;
- short fill hints.

They must not contain:

- review-dimension definitions;
- severity policy;
- material-finding sufficiency rules;
- safe-resolution decision rules;
- recording-status rules;
- security/privacy or observability examples.

Those rules remain in `SKILL.md`.

## Proposed asset layout

### `spec`

```text
skills/spec/
  SKILL.md
  assets/
    spec-skeleton.md
```

| Asset | Use |
|---|---|
| `spec-skeleton.md` | Starting structure for a new spec artifact. |

`spec-skeleton.md` may own the full output structure only if `skills/spec/SKILL.md` keeps a compact output expectation summary and a resource-map entry. Do not duplicate the full skeleton in both `SKILL.md` and the asset.

Requirement, acceptance-criterion, and decision-log row formats stay inline.
They are too small to justify packaged files because the inline format guidance
already owns their shape. Closed enums stay in `SKILL.md`.

### `spec-review`

```text
skills/spec-review/
  SKILL.md
  assets/
    review-result-skeleton.md
    review-finding.md
```

| Asset | Use |
|---|---|
| `review-result-skeleton.md` | Overall result block for a spec review artifact. |
| `review-finding.md` | Material finding block with ID, severity, location, evidence, required outcome, and safe resolution path. |

`spec-review` is a deliberative skill. Assets must not contain review-dimension explanations, severity policy, review judgment, security/privacy guidance, observability guidance, or material-finding rules beyond field labels and placeholders.

The review dimensions, dimension table structure, and verdict enum remain in `SKILL.md`. The fixed ten-row dimension table is not a copy-and-fill asset because it is the PR #79 failure surface and is owned by the skill contract.

This avoids repeating the PR #79 risk where richer review-dimension focus text could be read as new review obligations; that issue was specifically corrected during the PR #79 review loop.

### `test-spec`

```text
skills/test-spec/
  SKILL.md
  assets/
    test-spec-skeleton.md
    test-case.md
    coverage-map-row.md
```

| Asset | Use |
|---|---|
| `test-spec-skeleton.md` | Starting structure for a new test-spec artifact. |
| `test-case.md` | One stable test-case block. |
| `coverage-map-row.md` | Requirement and example coverage-map row variants. |

Stop conditions, coverage obligations, status enum values, and required test-spec section rules remain in `SKILL.md`.

Edge-case coverage row guidance stays inline because it is a trivial one-line
mapping. Assets only provide substantial structure.

## Resource map pattern

Each touched `SKILL.md` should include a resource map shaped like:

```md
## Resource map

- COPY `assets/<asset>.md` when <specific condition>.
  Fill: <field list>.
  Do not emit unfilled placeholders.
```

Examples:

```md
- COPY `assets/review-finding.md` once per material finding.
  Fill: finding ID, severity, location, evidence, required outcome,
  and safe resolution path.
  Do not emit unfilled placeholders.
```

```md
- COPY `assets/test-case.md` once per test case.
  Fill: test ID, level, target requirement, setup, steps, expected result,
  and coverage link.
  Do not emit unfilled placeholders.
```

## Output skeleton boundary

For each skill, choose one source of the full artifact skeleton.

Preferred approach:

```text
Full skeleton lives in assets/<skill>-skeleton.md.
SKILL.md keeps a compact output expectation summary.
SKILL.md resource map tells the agent when to COPY the full skeleton.
```

Do not duplicate the full skeleton in both `SKILL.md` and the asset.

If code review finds that a full skeleton asset hides too much contract surface for a skill, keep the full skeleton inline for that skill and use assets only for repeated substructures.

## Behavior preservation boundary

This proposal is an asset extraction pass, not a behavior change.

For each asset extraction, record a preservation matrix:

| Skill | Source content | Existing location | Asset destination | Preservation proof |
|---|---|---|---|---|
| `spec` | spec skeleton section set | `SKILL.md` output expectations | `assets/spec-skeleton.md` | same section set |
| `spec-review` | finding fields | `SKILL.md` finding guidance | `assets/review-finding.md` | same field set |
| `test-spec` | test-case fields | `SKILL.md` output skeleton | `assets/test-case.md` | same field set |
| `test-spec` | requirement/example coverage-map rows | `SKILL.md` output skeleton | `assets/coverage-map-row.md` | same row shapes |

A structural pass is insufficient if the extraction changes field names, field obligations, enum values, or stop conditions.

## Expected behavior changes

- `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, and `skills/test-spec/SKILL.md` become more common-path focused.
- Each skill ships a skill-local `assets/` directory.
- Generated adapter output contains each referenced asset.
- Every packaged asset is mapped from `SKILL.md`.
- Full artifact skeletons or repeated substructures move to assets.
- Rules, stop conditions, review dimensions, enums, coverage obligations, and lifecycle boundaries remain in `SKILL.md`.
- Representative behavior parity from PR #79 remains intact.

## Architecture impact

| Surface | Impact |
|---|---|
| `skills/spec/SKILL.md` | Adds resource map; may replace full inline skeleton with compact summary plus asset pointer. |
| `skills/spec/assets/*.md` | New packaged templates. |
| `skills/spec-review/SKILL.md` | Adds resource map; preserves review rules and dimensions. |
| `skills/spec-review/assets/*.md` | New structural templates only. |
| `skills/test-spec/SKILL.md` | Adds resource map; may replace full inline skeleton with compact summary plus asset pointer. |
| `skills/test-spec/assets/*.md` | New packaged templates. |
| `scripts/skill_validation.py` | May need asset coverage checks for spec-family assets. |
| `scripts/test-skill-validator.py` | Add positive and negative fixture coverage. |
| `scripts/build-skills.py` | Must preserve asset directories in generated skill mirrors. |
| `scripts/build-adapters.py` | Must package assets in adapter archives. |
| `scripts/validate-adapters.py` | Must verify asset presence and parity. |
| Adapter roots | No change. |
| Lockfile schema | No change. |
| CLI behavior | No change. |

## Testing and verification strategy

| Check ID | What is verified |
|---|---|
| `SFA-001` | Each spec-family skill has a resource map for every packaged asset. |
| `SFA-002` | Each resource-map entry uses literal `COPY`. |
| `SFA-003` | Each asset has required metadata comments. |
| `SFA-004` | Each asset has allowed template status. |
| `SFA-005` | Assets contain visible placeholders and no disallowed filler prose. |
| `SFA-006` | Assets do not contain hidden normative rules, stop conditions, enum value definitions, review-dimension explanations, or coverage obligations. |
| `SFA-007` | Assets do not require repository-root internal paths. |
| `SFA-008` | Generated skill mirror includes all assets. |
| `SFA-009` | Generated adapter archives include all assets. |
| `SFA-010` | No generated adapter skill body or asset is hand-edited. |
| `SFA-011` | Preservation matrices prove source-to-asset field parity. |
| `SFA-012` | Representative behavior parity remains unchanged from PR #79 baseline. |
| `SFA-013` | No unfilled placeholders appear in representative output. |
| `SFA-014` | Common-path `SKILL.md` token count is measured separately from total packaged skill footprint. |
| `SFA-015` | Cold-read confirms a user can understand when to use each asset from installed skill output alone. |
| `SFA-016` | `spec-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints. |
| `SFA-017` | A change-local baseline summary maps PR #79 skill structures to the planned assets and identifies which rules, enums, stops, review dimensions, and coverage obligations remain in `SKILL.md`. |

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

## Generated output proof boundary

Required:

- generated skill mirror includes each spec-family asset;
- temporary generated adapter output includes each asset;
- adapter validation passes against the temporary generated output;
- no generated body or asset is hand-edited.

Tracked-tree adapter checks are required when the repository's tracked expanded adapter layout supports them. If known stale tracked-tree debt remains, record a deferral with rationale, but temporary generated archive proof remains mandatory.

If lifecycle artifacts are touched:

```bash
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md \
  --path docs/plans/<plan>.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/changes/<change-id>/review-log.md \
  --path docs/changes/<change-id>/review-resolution.md
```

## Baseline summary artifact

Before implementation, create a change-local baseline summary:

```text
docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md
```

It must record, per skill:

- existing full skeleton section set;
- repeated substructure fields to extract;
- closed enums that remain in `SKILL.md`;
- stop conditions that remain in `SKILL.md`;
- review dimensions or coverage obligations that remain in `SKILL.md`;
- source location for each extracted asset.

This artifact feeds the preservation matrix. PR #79 remains the authoritative behavior baseline; the baseline summary is a change-local review aid, not a replacement baseline.

### Behavior-parity baseline

Use PR #79 as the baseline.

| Skill | Baseline proof to preserve |
|---|---|
| `spec` | Same required section set, same enum values, same settlement-result behavior. |
| `spec-review` | Same ten review dimensions, same review-dimension verdict values, same material-finding shape, same recording behavior. |
| `test-spec` | Same required sections, same coverage rules, same test-case format, same status/level enum values. |

PR #79 documented that `SFRP-M1-CR1` and `SFRP-M2-CR1` were resolved and re-reviewed, so this proposal should not reintroduce global fixture weakening or new review-dimension guidance.

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Complete the proof-route decision.
3. Amend `specs/skill-contract.md` only if existing asset rules do not cover multi-skill asset rollout, full-skeleton asset boundaries, or review-class asset restrictions.
4. Amend the matching test spec for spec-family asset packaging and preservation.
5. Create the change-local baseline summary.
6. Plan per-skill implementation milestones:
   - M1: `spec` assets.
   - M2: `spec-review` assets.
   - M3: `test-spec` assets.
   - M4: generated adapter proof and family closeout, if needed.
7. Record a per-asset justification in the plan, including expected usage count per invocation and why the asset earns its place.
8. Implement one skill at a time.
9. Run code review per milestone.
10. Run generated skill and adapter validation.
11. Record explain-change, verify, and PR handoff.

Rollback:

- Reinline asset content into the owning `SKILL.md`.
- Remove the skill's `assets/` directory.
- Preserve generic validator improvements if still valid.
- Rebuild generated mirrors and adapter archives from canonical skills.
- Do not alter adapter roots, lockfiles, or CLI behavior.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Assets hide behavior. | Keep rules, dimensions, stop conditions, enums, and lifecycle boundaries in `SKILL.md`. |
| `spec-review` assets become review guidance. | Restrict review assets to field labels and placeholders. |
| Full skeleton asset removes too much visible contract from `SKILL.md`. | Keep compact output expectation summary in `SKILL.md`; allow inline fallback if needed. |
| Adapter output misses assets. | Require generated adapter archive validation. |
| Asset placeholders leak into final output. | Validate representative outputs for no unfilled placeholders. |
| Common-path size reduction is overstated. | Measure `SKILL.md` separately from total packaged footprint. |
| PR #79 behavior parity regresses. | Use PR #79 preservation and parity artifacts as the baseline. |
| Validator overblocks legitimate assets. | Use deterministic checks and avoid broad semantic scoring. |
| Scope creeps into references/scripts. | Keep those as deferred follow-ups. |

## First-slice boundary

This proposal's first implementation sequence is limited to:

```text
skills/spec/SKILL.md
skills/spec/assets/*.md
skills/spec-review/SKILL.md
skills/spec-review/assets/*.md
skills/test-spec/SKILL.md
skills/test-spec/assets/*.md
validator/test fixtures needed for asset coverage
generated skill and adapter validation proof
behavior-preservation and behavior-parity evidence
lifecycle artifacts for this change
```

Out of scope:

```text
proposal
proposal-review
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
|---|---|
| `AC-SFA-001` | Each of `spec`, `spec-review`, and `test-spec` has an `assets/` directory with approved structural templates. |
| `AC-SFA-002` | Each asset has required template metadata comments. |
| `AC-SFA-003` | Each asset has a matching `COPY` resource-map entry in the owning `SKILL.md`. |
| `AC-SFA-004` | No asset contains hidden normative rules, enum definitions, stop conditions, review-dimension guidance, or coverage obligations. |
| `AC-SFA-005` | Each full skeleton asset has a corresponding compact output expectation summary in `SKILL.md`. |
| `AC-SFA-006` | Preservation matrices prove source-to-asset field parity for every extracted structure. |
| `AC-SFA-007` | Representative behavior-parity evidence matches the PR #79 baseline. |
| `AC-SFA-008` | Generated skill mirrors include all spec-family assets. |
| `AC-SFA-009` | Generated adapter archives include all spec-family assets. |
| `AC-SFA-010` | No generated adapter body or asset is hand-edited. |
| `AC-SFA-011` | Common-path `SKILL.md` token counts are recorded separately from packaged asset footprints. |
| `AC-SFA-012` | Cold-read verification confirms asset usage is understandable from installed adapter output alone. |
| `AC-SFA-013` | `spec-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints. |
| `AC-SFA-014` | A change-local baseline summary maps PR #79 skill structures to planned assets and to the rules, enums, stops, dimensions, and coverage obligations that remain in `SKILL.md`. |

## Open questions

None for proposal-review.

Resolved decisions:

- Full skeleton assets are used for `spec` and `test-spec`; `spec-review` uses result and finding assets only.
- Asset count is capped per skill at `spec`: 4, `spec-review`: 2, `test-spec`: 4. A higher count requires plan-recorded justification.
- Generated skill mirror proof and temporary generated adapter archive proof are mandatory. Tracked-tree proof is required when supported; known stale tracked-tree debt may be explicitly deferred.
- PR #79 remains the authoritative behavior baseline; this proposal adds a change-local baseline summary for source-to-asset review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-20 | Continue asset work after PR #79. | The spec-family skills now share a stable readability baseline. | Start before PR #79 closed. |
| 2026-05-20 | Use assets only. | The earlier plan pilot proved assets-first; references/scripts remain separate mechanisms. | Add references/scripts in the same slice. |
| 2026-05-20 | Apply to all three spec-family skills. | The family should remain consistent after PR #79. | Only `spec` and `test-spec`. |
| 2026-05-20 | Keep `spec-review` assets narrow. | Review-class skills are deliberative; assets must not become hidden review guidance. | Move review guidance into assets. |
| 2026-05-20 | Use PR #79 as baseline. | It closed the presentation-only pass with preservation and generated-adapter proof. | Re-baseline from older skill text. |
| 2026-05-20 | Exclude `spec-review/assets/review-dimension-row.md`. | The review-dimension table is a fixed list owned by `SKILL.md`, not a copy-and-fill substructure, and it sits on the PR #79 failure surface. | Defer the decision to implementation; duplicate dimension table structure in an asset. |
| 2026-05-20 | Use full skeleton assets only for `spec` and `test-spec`. | Constructive artifact-producing skills fit full skeleton extraction; `spec-review` is deliberative and should stay narrow. | Leave skeleton boundary open until implementation. |
| 2026-05-20 | Cap assets per skill. | The cap keeps the pilot disciplined and forces each asset to justify its place. | Use an uncapped family-wide asset pool. |
| 2026-05-20 | Require generated mirror and temporary adapter archive proof. | Asset work must prove resources reach generated public output while allowing explicit deferral for unrelated stale tracked-tree debt. | Archive-only proof with no mirror check; tracked-tree proof as a hard blocker despite known unrelated debt. |
| 2026-05-20 | Add a change-local baseline summary. | Reviewers need a concise source-to-asset mapping without replacing PR #79 as the authoritative baseline. | Force reviewers to reconstruct the extraction baseline from PR #79 alone. |

## Next artifacts

```text
proposal-review
test-spec amendment for spec-family asset checks
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

Deferred future directions to route through separate proposals if still desired:

- packaged `references/` in spec-family skills;
- produced spec/test-spec artifact readability;
- build-time partials to reduce duplicated rule text;
- review-class asset/reference split across `proposal-review`, `spec-review`, and `code-review`.

## Follow-on artifacts

- [Spec-Family Assets Progressive Disclosure](../../specs/spec-family-assets-progressive-disclosure.md)

## Readiness

Ready for `spec`.

## Core invariant

```text
Spec-family assets are copied structures, not hidden rules.

After PR #79, `spec`, `spec-review`, and `test-spec` have a stable
presentation baseline. This proposal may extract reusable skeletons into
packaged assets only if the installed skills remain self-contained, generated
adapters include the assets, and every rule, enum value, review dimension,
coverage obligation, stop condition, lifecycle boundary, and representative
output behavior remains unchanged.
```
