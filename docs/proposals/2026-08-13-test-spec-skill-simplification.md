<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/proposal/SKILL.md -->
<!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Test-Spec Skill Simplification

## Owning change record

`docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`

## Problem

The published `test-spec` skill loads 2,427 words of stage-local guidance before its two required boundary-first references and output assets are considered. Its common path mixes portable proof design, governed `change.yaml` mutation, workflow-managed settlement, repeated structural formats already owned by five assets, and a long inline restatement of procedure already owned by the boundary-first references.

This makes the skill harder to scan and increases context cost for both portable and governed authoring. It also creates multiple maintenance locations for test-case layout, output structure, boundary procedure, and proof-ledger guidance. The package already has appropriate references and assets, but `SKILL.md` does not consistently treat them as the sole owners of their detailed procedure or structure.

The problem is not that the test-spec contract is too rigorous. Requirement traceability, boundary proof, validation-command ownership, milestone proof timing, lifecycle isolation, and implementation handoff remain necessary. The problem is that universal policy, conditional state mutation, shared boundary procedure, and structural layout are not separated cleanly.

## Goals

- Reduce the procedural context loaded for portable and governed test-spec authoring without weakening proof quality or lifecycle safety.
- Keep a self-sufficient universal `SKILL.md` for proof design, coverage integrity, stop conditions, claims, and handoff.
- Move only governed artifact-entry mutation and workflow-managed settlement procedure into one conditionally loaded reference.
- Preserve the existing contract that `test-spec` initially loads both boundary-first references; remove duplicated inline boundary procedure instead of changing that loading policy.
- Make the five existing assets the sole owners of repeated output labels, columns, ordering, and placeholders.
- Preserve current requirement, example, edge-case, command, milestone, manual-proof, and boundary-proof semantics.
- Measure real loaded profiles and total package size separately so relocation is not presented as deletion.

## Non-goals

- Reducing test rigor, removing requirement-to-proof traceability, or allowing implementation with unresolved proof gaps.
- Changing the `boundary-first-v1` model, resource bytes, stable IDs, capability activation, or required initial loading profile.
- Changing test-spec-review authority, workflow stage order, implementation authorization, or review settlement ownership.
- Replacing Markdown authoring with an executable proof-map engine, schema-driven generator, scheduler, or model-runtime evaluator.
- Adding a new test-spec asset, permanent simplicity validator, tokenizer dependency, or target-agent journey test.
- Rewriting historical test specs or changing their status merely to adopt the simplified skill.

## Vision fit

fits the current vision

The change makes a core traceability artifact easier for agents and humans to author without weakening the evidence chain from requirements and boundaries to tests, validation, milestones, review, and implementation. It improves reviewability and portability while keeping durable proof explicit.

## Context

The canonical package currently contains:

```text
skills/test-spec/
├── SKILL.md
├── references/
│   ├── boundary-first-method-v1.md
│   └── boundary-first-proof-v1.md
└── assets/
    ├── test-spec-skeleton.md
    ├── test-case.md
    ├── coverage-map-row.md
    ├── validation-command-row.md
    └── milestone-proof-row.md
```

Current canonical measurements are:

| Resource | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `SKILL.md` | 304 | 2,427 | 16,766 |
| Boundary-first method reference | 110 | 857 | 6,346 |
| Boundary-first proof reference | 41 | 356 | 2,305 |
| Five structural assets | 162 | 763 | 4,900 |
| Complete package | 617 | 4,403 | 30,317 |

The active boundary-first contract requires `test-spec` to package and initially load both the compact core and proof guidance. This proposal does not make those resources conditional. Instead, it removes the stage-local restatement of their detailed procedure and keeps only the test-spec-specific bridge and routing rules inline.

The stage-owned lifecycle contract permits `test-spec` to create or revise only its own artifact, authoring evidence, and matching artifact-state entry. A portable invocation has no such mutation authority. The current skill states both paths inline even though governed mutation applies only when one exact change grants it.

The five assets already provide the normative document skeleton and repeated row or case layouts. `SKILL.md` nevertheless repeats the test-case format, output skeleton, and parts of the structural contract. Those repetitions should be removed without moving policy into the assets.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `test-spec` skill | in scope | Goals and Recommended Direction |
| Identify the best solution rather than only shortening prose | in scope | Options Considered and Recommended Direction |
| Create a new branch | in scope | Governed change branch and Decision Log |
| Generate a proposal | in scope | This artifact |
| Run `proposal-review` after authoring | in scope | Next Artifacts and Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Simplify universal `test-spec` guidance | core to this proposal | This is the primary common-path reduction. |
| Add one governed authoring reference | core to this proposal | It isolates conditional lifecycle mutation behind exact authority. |
| Preserve both boundary-first references and their initial loading | same-slice dependency | The governing boundary contract is compatibility-sensitive and must remain intact. |
| Remove inline structural duplication | core to this proposal | Existing assets already own the repeated shapes. |
| Update skill and package validators | same-slice dependency | Resource ownership, closed vocabularies, and package parity require deterministic proof. |
| Add change-local preservation and measurement evidence | same-slice dependency | Simplification needs semantic accounting and honest profile metrics. |
| Redesign boundary-first loading across the spec family | out of scope | That would change an independently governed capability contract. |
| Optimize `test-spec-review` further | out of scope | It was simplified separately and owns a different review responsibility. |

## Options Considered

### Option 1: Leave the package unchanged

This avoids compatibility risk but leaves governed mutation, duplicated structures, and repeated boundary procedure on every authoring path. It does not address the usability problem.

### Option 2: Editorial compression inside `SKILL.md`

This would reduce some wording without changing package shape. It is lower risk, but governed and portable responsibilities would remain interleaved and structural ownership would remain duplicated. Future changes could restore the same drift.

### Option 3: One governed reference, retained boundary resources, and asset-owned structure

This option shortens `SKILL.md`, adds one conditional governed-authoring reference, preserves the two always-loaded boundary references unchanged, and removes inline structures already owned by the five assets. Universal proof policy stays inline, while lifecycle mutation becomes progressively disclosed.

This is the recommended option because each resource boundary corresponds to a real authority or ownership boundary and both primary procedural profiles can shrink.

### Option 4: Split commands, milestones, fixtures, and proof policy into several references

This could make `SKILL.md` very short, but most test specs use several of those concerns together. Multiple small references would increase navigation and package complexity while providing little loaded-context benefit.

### Option 5: Replace prose authoring with an executable proof-map engine

An engine could enforce structure deterministically, but it would introduce runtime, schema, migration, and maintenance architecture far beyond the problem. Semantic proof design still requires judgment, so the engine would not eliminate the core skill contract.

## Recommended Direction

Adopt Option 3.

The final package should be:

```text
skills/test-spec/
├── SKILL.md
├── references/
│   ├── governed-test-spec-authoring.md
│   ├── boundary-first-method-v1.md
│   └── boundary-first-proof-v1.md
└── assets/
    ├── test-spec-skeleton.md
    ├── test-case.md
    ├── coverage-map-row.md
    ├── validation-command-row.md
    └── milestone-proof-row.md
```

### Invocation and authority model

Use two procedural profiles:

| Profile | Governed candidate | Loaded procedure |
| --- | ---: | --- |
| `TSA0-portable` | no | `SKILL.md` plus both required boundary references |
| `TSA1-governed` | yes | portable procedure plus `governed-test-spec-authoring.md` |

Structural assets are loaded or copied according to the authoring operation and are measured separately from procedural context. A complete new test spec normally uses all five assets; a bounded revision uses only the structures it changes.

`governed_test_spec_candidate_context` is a load predicate, not mutation authority. It is true only when current evidence points to exactly one `stage-owned-change-local-v1` change whose workflow stage or artifact state plausibly requires test-spec creation or revision. Conversational wording alone is insufficient.

The governed reference validates exact authority after loading. It resolves one of two operations:

```text
create-primary-test-spec
revise-primary-test-spec
```

Creation requires one exact change, settled governing inputs, current test-spec authoring authority, and one deterministic intended path; it does not require a pre-existing test-spec entry or file. Revision requires one existing entry, matching file and artifact identity, and a legal revision state. An entry/file mismatch, multiple candidates, stale inputs, illegal state, or ambiguous path stops before content or state mutation.

Loading the reference never grants workflow continuation, test-spec-review settlement, implementation authority, or permission to modify another artifact-state entry or `workflow_state`.

### Resource ownership

| Content | Owner |
| --- | --- |
| Purpose, prerequisites, evidence selection, proof-design policy, coverage integrity, stops, claims, and handoff | `SKILL.md` |
| Governed candidate trigger and missing-resource stop | `SKILL.md` |
| Exact governed validation, create/revise transition, authoring evidence, retry, and workflow-managed settlement preparation | `governed-test-spec-authoring.md` |
| Shared boundary vocabulary, compact scan, identifiers, interactions, and upstream-gap routing | Existing boundary-first method reference |
| Boundary proof record, coverage state, proof levels, automation modes, negative/composed proof, and adequacy checks | Existing boundary-first proof reference |
| Document headings, test-case labels, row columns, ordering, and placeholders | Existing five assets |
| Applicability, closed-vocabulary meaning, coverage sufficiency, readiness, and lifecycle authority | Skill procedure, never assets |

The governed reference may invoke established boundary and proof concepts, but it must not duplicate or override them. The boundary references remain byte-identical projections of their canonical sources.

### Universal `SKILL.md` content

Keep inline:

- purpose, workflow role, prerequisites, output path, artifact placement, and evidence access;
- universal stops before authoring;
- exact resource map and failure behavior;
- requirement, example, error, migration, architecture-boundary, and regression coverage obligations;
- stable test, command, milestone, manual-proof, gap, and evidence identities;
- closed test-level and command-classification vocabularies;
- command ownership, zero-test, side-effect, and first-required-milestone rules;
- milestone proof timing and code-review gate mapping;
- uncovered-gap routing, isolation, claims, and `test-spec-review` handoff;
- a compact test-spec-specific boundary bridge that points to the two required references without restating them.

Consolidate the coverage, validation-command, and milestone-proof rules into one concise proof-ledger section. These semantics remain universal; moving them into another optional reference would only relocate common-path content.

### Structural ownership

Delete the inline `Test case format` and `Output skeleton` blocks and avoid reproducing asset-owned row shapes in prose. Retain compact applicability rules in `SKILL.md`:

- copy the full skeleton for creation or full rewrite;
- copy repeated assets once per applicable row or case;
- omit inapplicable structures only when the governing contract permits an explicit rationale;
- never emit an unfilled placeholder;
- assets define layout only and never determine proof adequacy, lifecycle state, or handoff.

### Missing-resource behavior

The two boundary references are required for every test-spec authoring profile. If either is missing, unreadable, escaped, or mixed-version, stop before proof-map authoring. If governed candidate context is true and the governed reference is unavailable, stop before reading or mutating governed state. Missing inapplicable structural assets block only the authoring operation that requires them. The skill must not reconstruct missing procedure or layout from memory.

## Expected Behavior Changes

- Portable authoring loads a shorter stage-local contract while retaining the same two required boundary references and proof rigor.
- Governed authoring additionally loads one reference that validates exact change authority and owns only the permitted artifact-entry transition.
- New governed test-spec creation no longer depends on a pre-existing test-spec identity; revision still requires an exact current identity.
- Repeated test-case, coverage, command, milestone, and document layouts come only from their mapped assets.
- Detailed boundary-first procedure appears only in its existing mapped references, not again in stage-local prose.
- Coverage, command, milestone, manual-proof, stop, claim, and handoff behavior remains unchanged.
- Missing required resources fail safely without fallback invention.

## Architecture Impact

The expected assessment is `architecture-not-required`. The change adds one skill-local reference inside the existing published-skill package model and does not introduce a runtime, service, dependency, persistence mechanism, schema, or lifecycle owner.

A bounded architecture assessment is still required because the published package inventory changes. Existing architecture documentation should be corrected only if it depicts `test-spec` as permanently limited to its current resources or contradicts the general `SKILL.md` plus mapped references and assets model. A new ADR is required only if specification discovers a new durable package, state, runtime, or ownership decision.

The proposal does not amend the boundary-first resource model: both existing references remain required consumers and initial resources for `test-spec`.

## Testing and Verification Strategy

Use three proof classes.

### Deterministic structural and package proof

Validate:

- normalized frontmatter and required skill sections;
- exact resource-map paths and verbs;
- required initial boundary resources and their byte parity;
- governed-reference presence, containment, and exact load predicate;
- existing asset count, metadata, structure, and placeholder rules;
- closed operation, test-level, command-classification, coverage-state, proof-level, and automation-mode vocabularies;
- unknown values fail before consistency checks;
- canonical, generated, archived, and clean-installed package parity.

### Static contract scenarios

Cover at least:

- portable creation and bounded revision;
- governed new-entry creation and existing-entry revision;
- candidate loading followed by valid or invalid authority;
- entry/file absence, asymmetry, mismatch, multiplicity, stale input, illegal state, and concurrent-write stops;
- boundary proof with exact approved IDs and upstream routing for new behavior or proof-only gaps;
- commands with zero-test and side-effect boundaries;
- milestones with current, planned, deferred, and missing commands;
- uncovered gaps blocking downstream reliance;
- missing governed, boundary, or structural resources;
- isolated versus workflow-managed handoff and forbidden writes.

Scenario proof is deterministic and fixture-based. It does not execute Codex, Claude Code, opencode, or another target-agent runtime.

### Semantic preservation and measurement

Create two change-local inventories:

```text
docs/changes/2026-08-13-test-spec-skill-simplification/test-spec-rule-disposition.yaml
docs/changes/2026-08-13-test-spec-skill-simplification/test-spec-literal-compatibility.yaml
```

Every behaviorally significant rule receives one disposition: `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`.

Every exact consumer is classified separately as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, `obsolete`, or `historical-fixture`. Preserve contract literals, migrate parser contracts atomically, and update incidental tests rather than freezing prose.

Measure canonical authored files with LF-normalized UTF-8 bytes and Unicode whitespace-separated words. Report:

| Measurement | Purpose |
| --- | --- |
| `SKILL.md` words and bytes | Main stage-local scale |
| `TSA0-portable` procedural words and bytes | Core plus both required boundary references |
| `TSA1-governed` procedural words and bytes | Portable profile plus governed reference |
| Representative full-create assembly | Procedural profile plus all five structural assets |
| Bounded-revision assemblies | Procedural profile plus only applicable assets |
| Each resource | Ownership contribution |
| Total package words and bytes | True maintenance footprint |
| Duplicate rule clusters | Ownership improvement |

Acceptance requires both procedural profiles to decrease, every rule and literal dependency to be accounted for, every identified duplication cluster to have one loaded owner, and semantic behavior to remain intact. A 25–35 percent portable reduction and 10–20 percent governed reduction are planning targets, not normative gates. Token estimates are optional only when an existing pinned repository-owned implementation supports the exact assembly; no tokenizer dependency is added.

Permanent validation should enforce durable structure, vocabularies, resource integrity, and package parity. Change-local size measurements, disposition ledgers, duplicate counts, and prose judgment must not create a new permanent validator family.

## Rollout and Rollback

Implement the canonical package and directly coupled validators or fixtures atomically. Regenerate or validate all supported adapter packages through existing repository-owned commands. Do not hand-edit generated public adapter bodies.

Historical test specs remain unchanged. Existing boundary references retain their canonical bytes and current initial-loading classification. The new skill writes the existing test-spec format; this change introduces no document migration.

Rollback is an atomic revert of `SKILL.md`, the governed reference, directly coupled validator or fixture changes, and change-local evidence, followed by existing package generation and parity validation. No persisted customer data or schema rollback is required.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal proof policy is hidden in the governed reference | Use a rule-disposition ledger and require portable semantic review. |
| The boundary-first loading contract is weakened accidentally | Preserve both references, initial-resource fixtures, canonical bytes, and boundary validation unchanged. |
| Structural assets become policy owners | Limit assets to labels and layout; keep applicability and meaning in procedure. |
| New governed creation becomes circular | Separate candidate loading from authority validation and creation from revision. |
| Loading a reference is mistaken for write authority | State that exact validation occurs after loading and stops before mutation on mismatch. |
| Package splitting merely moves content | Require both loaded profiles to shrink and report total package size separately. |
| Literal assertions freeze accidental wording | Classify semantic rules and literal consumers in separate inventories. |
| Missing resources lead to remembered or partial procedure | Make every triggered missing resource a fail-safe stop. |
| Validator work expands into semantic classification | Keep validators structural and use independent review for semantic preservation. |
| Simplification pressures removal of required rigor | Make percentage targets subordinate to complete rule accounting and semantic preservation. |

## Open Questions

None at proposal level. The specification should inventory exact literal consumers and existing validation command owners, but the ownership, invocation, boundary-resource, asset, measurement, architecture, and acceptance directions are selected here.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-13 | Create branch `proposal/test-spec-skill-simplification` from current `origin/main`. | Isolate the initiative in a reviewable branch. | Reuse the merged plan-review branch. |
| 2026-08-13 | Select one governed authoring reference. | Governed mutation has one real conditional authority boundary. | Inline-only compression and fragmented references. |
| 2026-08-13 | Preserve both boundary references as initial resources. | The current approved boundary-first contract requires them for `test-spec`. | Making proof guidance conditional as an unapproved simplification. |
| 2026-08-13 | Keep proof-ledger semantics inline but remove asset-owned shapes. | Commands and milestones are broadly applicable; their structures already have owners. | Another common-path reference or duplicated formats. |
| 2026-08-13 | Require portable and governed profile reduction without a fixed percentage. | Loaded context is the real outcome, while semantic safety outranks numeric optimization. | `SKILL.md`-only or hard percentage acceptance. |
| 2026-08-13 | Exclude target-agent runtime acceptance and permanent simplicity validators. | Static contract proof, package parity, and semantic review are proportionate. | Model journeys, transcript grading, and token-budget gates. |

## Next Artifacts

- Independent proposal review.
- Focused `test-spec` skill-contract specification or amendment after proposal approval.
- Bounded architecture assessment.
- Execution plan and plan review.
- Test specification and independent test-spec review.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim approval, specification readiness, implementation readiness, verification, branch readiness, or PR readiness.
