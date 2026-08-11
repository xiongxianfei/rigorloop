<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->

# Verify Skill Simplification

## Owning change record

`docs/changes/2026-08-11-verify-skill-simplification/change.yaml`

## Problem

The published `verify` skill currently places scoped direct verification, workflow-managed final verification, branch-readiness calculation, lifecycle and review closeout inspection, release-sensitive proof, validation evidence rules, and a substantial boundary-first bridge in one 308-line, 2,896-word `SKILL.md`.
Every invocation therefore loads detailed final-closeout procedure even when the user asks for a bounded validation check that neither needs nor may claim branch readiness.

The package already maps the 857-word `boundary-first-method-v1.md` reference, but the main file repeats 336 words of boundary procedure.
Other repeated clusters include purpose and output ownership, direct versus workflow-managed behavior, evidence discovery, lifecycle and review closeout, claim boundaries, stops, and handoff wording.

The problem is not that final verification is too rigorous.
The problem is that universal verification safety and conditional branch-readiness procedure have more than one prose owner and are loaded for contexts that do not need them.

## Goals

- Make scoped direct verification shorter and easier to execute correctly.
- Keep `SKILL.md` self-sufficient for invocation classification, safe evidence handling, scoped verification, and truthful claims.
- Give each behaviorally significant verification rule one explicit owner and destination.
- Load detailed branch-readiness and final-closeout procedure only when the requested result depends on it.
- Preserve `verify` ownership of `branch-ready` while preserving `pr` ownership of PR-body and PR-open readiness.
- Preserve lifecycle, review-resolution, validation, CI, release, generated-output, manual-proof, boundary-first, stop, and handoff semantics.
- Preserve deterministic canonical, generated, packed, and installed package resources.
- Measure loaded content by invocation profile and report total package size separately, so relocation is not described as deletion.

## Non-goals

- Weakening the evidence required for `branch-ready` or changing which stage owns that claim.
- Changing workflow stage order, `change.yaml` schema, review settlement, planned-work semantics, selector behavior, CI policy, release policy, or PR authorization.
- Turning `verify` into code review, review resolution, artifact authoring, automatic repair, PR preparation, or PR opening.
- Creating an executable verification engine, scheduler, cache, state store, or agent-runtime harness.
- Splitting every verification dimension into a separate reference.
- Adding an output asset when the compact inline result shape remains sufficient.
- Optimizing another skill or introducing a cross-skill verification abstraction in this change.
- Making a line, word, byte, or token percentage a permanent product invariant.

## Vision fit

fits the current vision

The change reduces ceremony for bounded verification while retaining the tracked evidence and explicit readiness boundaries that make AI-assisted work reviewable, resumable, and trustworthy.

## Context

`verify` is the largest remaining common-path skill after the recent `code-review`, `implement`, and `workflow` simplifications.
Its current authored package measures:

| Surface | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `skills/verify/SKILL.md` | 308 | 2,896 | 20,715 |
| Existing boundary-first reference | 110 | 857 | 6,346 |
| Total package | 418 | 3,753 | 27,061 |

The largest main-file sections are the 521-word verification process, 336-word boundary-first method, 200-word rules, 167-word command-and-evidence guidance, and 159-word dimension list.
Some of this content is universal, but much of the detailed process exists to support final branch-readiness rather than a scoped direct check.

The existing skill-package contract already supports mapped `READ` references, resource containment, byte identity, generated and installed parity, and fail-safe handling for required missing resources.
The existing boundary-first reference remains mandatory and unchanged as a deterministic projection owned by its governing contract.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `verify` skill | in scope | Goals; Recommended Direction |
| Preserve verification rigor while improving usability | in scope | Goals; Expected Behavior Changes |
| Start from a new branch | in scope | Owning change record and branch workflow evidence |
| Create a decision-oriented proposal | in scope | This artifact |
| Perform proposal review after authoring | in scope | Readiness and owning change record |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal `verify` common path | core to this proposal | This is the primary user-value change. |
| Add one branch-readiness reference | core to this proposal | Detailed final-closeout procedure has one coherent activation boundary. |
| Preserve the existing boundary-first reference | same-slice dependency | `verify` is a governed boundary-first skill and its package must remain complete. |
| Normalize required frontmatter and resource mapping | same-slice dependency | A changed published skill must satisfy the current package contract. |
| Semantic and literal preservation evidence | same-slice dependency | Simplification must not silently lose policy or freeze accidental test wording. |
| Canonical, generated, packed, and installed parity proof | same-slice dependency | The new mapped resource is part of the published package. |
| New result asset | out of scope | The inline result structure is already compact and profile-neutral. |
| New runtime verifier or target-agent test harness | out of scope | The change is packaged guidance, not runtime architecture. |
| Optimization of another skill | separate proposal | Cross-skill work would obscure this package boundary. |

## Options Considered

### O0: keep the current package

This has no migration risk, but every scoped verification continues to pay the full final-closeout context cost and duplicated rule ownership remains unresolved.

### O1: edit and deduplicate only within `SKILL.md`

This is the smallest packaging change.
It can remove repeated wording, but final branch-readiness procedure still loads for every bounded validation request and the main file remains responsible for two materially different verification profiles.

### O2: shorten only the boundary-first bridge

This removes the most obvious mapped-reference repetition with little package change.
It does not address the much larger branch-readiness, lifecycle, review-closeout, evidence, and release procedure that dominates the common path.

### O3: compact universal skill plus one conditional branch-readiness reference

Keep universal verification authority and safety inline, retain the existing boundary-first reference, and move detailed final branch-readiness procedure into one mapped reference with an exact load condition.
This aligns progressive disclosure with a real claim boundary and is the recommended direction.

### O4: separate references for lifecycle, review closeout, CI, release, and generated output

This minimizes each individual load but creates a fragmented dependency graph, overlapping triggers, and more opportunities to omit a required procedure.
Those concerns participate in one branch-readiness decision and should remain together.

### O5: replace prose verification with an executable verifier

An executable engine could automate some deterministic checks, but it cannot own semantic coherence or safely replace project-specific evidence judgment.
It would introduce runtime, compatibility, and maintenance scope unrelated to simplifying the skill.

## Recommended Direction

Choose O3.

The final package is expected to be:

```text
skills/verify/
├── SKILL.md
└── references/
    ├── boundary-first-method-v1.md
    └── branch-readiness-verification.md
```

No result asset is added in the first version.
The compact result block is used by every profile, has little structural repetition, and is clearer when its labels remain visible in `SKILL.md`.

### Universal `SKILL.md` ownership

The main file remains sufficient for every scoped direct verification and owns:

| Inline contract | Reason |
| --- | --- |
| Purpose, description, trigger, workflow role, and near-miss routing | Needed before reference selection. |
| Invocation classification and exact resource triggers | Determines the valid loaded package. |
| Evidence authority and source precedence | Universal to every verification claim. |
| Compact verification dimensions | Every verification scope needs a consistent quality model. |
| Validation integrity | Tests, commands, CI, and generated-artifact claims must remain evidence-bound. |
| Direct-verification isolation | A scoped check must not imply workflow completion. |
| `branch-ready` and PR claim boundaries | Claim ownership may never depend on an optional reference. |
| Universal blockers and upstream-gap routing | Unsafe work stops before optional procedure. |
| Compact boundary-first bridge and both resource-map entries | Required for correct progressive disclosure. |
| Compact result, status, and handoff contract | Every invocation must return a useful, bounded result. |

The inline verification dimensions may be expressed compactly, but they continue to cover contract satisfaction, proof validity, architecture and artifact coherence, lifecycle and review state, validation evidence, drift, risk, and release or handoff readiness when applicable.

### Conditional branch-readiness reference ownership

`references/branch-readiness-verification.md` owns only the detailed procedure needed when the requested outcome would support branch readiness, workflow final closeout, or release-sensitive final readiness:

- final-verification prerequisites and authoritative related-artifact assembly;
- requirement-to-test-to-diff-to-evidence traceability procedure;
- baseline change-pack and durable-rationale checks;
- lifecycle artifact, plan/index, milestone, review-log, and review-resolution closeout inspection;
- tracked governing branch-state requirements;
- targeted proof, broad-smoke triggers, CI evidence, generated-output drift, and manual-proof handling;
- release-metadata and release-sensitive evidence handling when applicable;
- workflow-managed Phase C and fresh-actual-run constraints;
- final blocker aggregation, `branch-ready` calculation, verification recording, and `pr` handoff.

The reference does not redefine status vocabulary, claim authority, universal stop rules, evidence truthfulness, workflow stage order, or PR authorization.
It remains part of the `verify` skill package and does not become an independent lifecycle owner.

### Closed invocation profiles

Classification follows the requested claim and governing context, not merely whether the user invoked the skill directly.

`branch_readiness_context` is true when either:

- the governed workflow is at final `verify`; or
- the user explicitly requests branch readiness, final workflow closeout readiness, or release-sensitive final readiness whose result would be used for PR handoff.

A direct request for one bounded command, artifact, requirement, or validation scope does not establish branch-readiness context.
Conversational use of words such as “check,” “verify,” or “ready” does not silently broaden the claim.

The boundary-first trigger remains independently additive when approved boundary, interaction, or proof trace is missing, stale, unknown, ambiguous, conflicting, or insufficient.

| Profile | Branch-readiness context | Boundary-first trigger | Loaded package |
| --- | ---: | ---: | --- |
| `VP0-scoped` | no | no | `SKILL.md` |
| `VP0B-scoped-boundary` | no | yes | `SKILL.md` plus boundary-first reference |
| `VP1-final-readiness` | yes | no | `SKILL.md` plus branch-readiness reference |
| `VP1B-final-readiness-boundary` | yes | yes | `SKILL.md` plus both references |

A scoped direct verification may report only the evidence and verdict for its requested scope.
It does not claim branch readiness or workflow completion.
A direct invocation that explicitly requests a full branch-readiness verdict is valid `VP1`, remains isolated after reporting, and does not invoke `pr`.

### Resource failure behavior

If branch-readiness context is true and `branch-readiness-verification.md` is missing or unreadable, verification stops before a branch-readiness verdict or state-changing handoff.
If the boundary-first trigger is true and its governed reference is missing or unreadable, verification stops with the package-integrity blocker required by the existing boundary contract.
An untriggered conditional reference is not loaded and does not block `VP0`.
The shortened common path is intentionally insufficient to reconstruct missing conditional procedure from memory.

### Rule ownership and compatibility evidence

Before rewriting the package, create two separate change-local inventories.

The semantic rule-disposition ledger records every behaviorally significant current rule with source locations, applicable profiles, governing requirements, disposition, destination, and preservation proof.
Allowed dispositions are:

```text
retained-inline
retained-branch-readiness-reference
retained-boundary-reference
removed-duplicate
removed-obsolete-with-approved-contract-change
```

No behaviorally significant rule disappears without one disposition.

The literal-compatibility inventory separately records exact headings, fields, phrases, capitalization, and vocabulary consumed by specs, parsers, validators, fixtures, or package tooling.
Each dependency is classified as:

```text
normative-contract
parser-or-package-contract
test-only-incidental
obsolete
```

Normative literals are preserved unless their governing contract changes.
Parser or package contracts are preserved or migrated with all consumers.
Incidental assertions are updated instead of becoming prose-policy owners.

### Validation ownership

Permanent deterministic validation remains with existing owners for frontmatter, normalized sections and vocabulary, claim-boundary phrases, Resource-map syntax, mapped-resource existence and containment, boundary projection identity, and generated, packed, and installed parity.

The semantic ledger, literal inventory, representative scenario matrix, duplicate-cluster count, profile measurements, and independent semantic review are change-local evidence.
This change does not add a permanent simplicity validator, profile-size gate, prose-quality score, generic fixture framework, selector evidence class, tokenizer dependency, or target-agent journey test.

## Expected Behavior Changes

- Scoped verification loads a shorter common path and omits final-closeout procedure it cannot use.
- Requests that support `branch-ready`, workflow final closeout, or release-sensitive final readiness load one coherent branch-readiness procedure.
- Direct full branch-readiness verification remains possible but isolated; direct invocation does not activate workflow continuation.
- Boundary-first guidance loads only under its existing governed trigger and no longer has a long duplicate owner inline.
- Missing required conditional resources stop safely instead of causing partial reconstruction.
- Output retains a compact verdict, scope, evidence, blockers, validation, readiness, and next-stage summary without adding profile-inapplicable placeholders.
- Claim ownership, validation coverage, lifecycle settlement, review closeout, release safety, and downstream authorization remain unchanged.

## Architecture Impact

The expected result is `architecture-not-required` after a bounded assessment.
The proposal uses the existing published-skill package model: canonical `SKILL.md` plus mapped references, generated adapters as derived output, and raw-byte resource parity.
It introduces no runtime, service, dependency, persistent state, schema, new lifecycle owner, or new package class.

If the current architecture contains a flat `verify` package example or otherwise requires a current-state correction, this change will own that architecture update through an `architecture` entry in its `change.yaml` and the existing canonical architecture document.
An ADR is needed only if downstream specification changes the normative package model or gives the new reference independent policy ownership, neither of which is recommended.

## Testing and Verification Strategy

Use four proof classes:

1. Deterministic structural proof checks frontmatter, required sections, claim vocabulary, both Resource-map entries, resource existence, placeholder absence, and package containment.
2. Static contract scenarios cover every profile, direct versus final-readiness classification, required and forbidden reference loads, missing-resource stops, scoped claim limits, branch-ready blockers, review and lifecycle closeout, release-sensitive evidence, and boundary-first additive loading.
3. Package-chain proof compares canonical, generated, locally packed, and temporary installed Codex, Claude Code, and opencode resources through existing repository commands.
4. Independent semantic review compares the final package against the rule ledger, literal inventory, governing contracts, current skill behavior, and expected profile outcomes.

No Codex, Claude Code, opencode, or other target-agent runtime executes for acceptance.
No prompt journey, transcript grading, model-selection fixture, or runtime-version evidence is introduced.

Measure canonical resources with LF-normalized profile assembly, counting each loaded file once in documented load order.
Report UTF-8 bytes and Unicode whitespace-separated words as the primary portable metrics.
Use a token estimate only when the repository already supplies a pinned implementation; otherwise omit it rather than adding a dependency.

Report before and after for:

- `SKILL.md` lines, words, bytes, and optional pinned token estimate;
- every reference contribution;
- `VP0`, `VP0B`, `VP1`, and `VP1B` loaded words and bytes;
- total package words and bytes;
- duplicate-rule clusters and inline template count.

A 30–40 percent reduction in `VP0` loaded words is a planning target, not a normative semantic gate.
Acceptance requires complete rule disposition, one owner per repeated cluster, material scoped-profile reduction, no unjustified final-readiness profile growth, honest total-package accounting, and preserved behavior.

## Rollout and Rollback

Roll out the canonical `verify` package, both mapped references, validator or consumer migrations, and generated package proof atomically.
Do not publish an intermediate package in which `SKILL.md` points to a missing reference or generated targets carry mixed resource versions.

Rollback restores the prior canonical `verify` package and any coupled literal-consumer changes together, then regenerates and revalidates derived packages.
Change-local ledgers and measurements remain as historical evidence even if the package layout is rolled back.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| A universal blocker moves behind the conditional reference | Scoped verification could overclaim or proceed unsafely. | Closed ownership table plus complete semantic-rule ledger and independent review. |
| Branch-readiness classification is too narrow | Full verification may omit required procedure. | Define the trigger by requested claim and governed stage; cover direct and workflow-managed cases statically. |
| Branch-readiness classification is too broad | Context savings disappear for ordinary checks. | Add required and forbidden load scenarios and measure every profile. |
| The new reference becomes a competing policy owner | Lifecycle or claim behavior can diverge. | Keep universal authority inline and limit the reference to procedure. |
| Relocation increases total package size | Maintenance cost may grow despite a shorter main file. | Report common-path and package totals separately; reject unjustified duplication. |
| Tests freeze accidental wording | Simplification becomes cosmetic. | Separate semantic rules from literal consumers and migrate incidental tests. |
| Package output drifts | Installed agents may lack required procedure. | Use existing mapped-resource and generated/packed/installed parity gates. |
| Numerical targets pressure semantic deletion | Important safeguards may be hidden or removed. | Keep the percentage advisory and make rule preservation the acceptance gate. |

## Open Questions

- Which current exact headings and phrases are normative or parser-sensitive? The pre-edit literal inventory will classify each consumer; this does not change the selected package direction.
- Does the canonical architecture contain a `verify`-specific flat-package example that needs correction? The bounded architecture assessment will decide between `architecture-not-required` and a change-owned documentation update.
- Does the repository's existing pinned measurement script provide a stable token estimate for all profile assemblies? Words and bytes remain sufficient if it does not.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Optimize `verify` next. | It is the largest remaining common-path skill and mixes scoped checks with final readiness procedure. | O0 leaves the usability problem intact. |
| 2026-08-11 | Use one branch-readiness reference. | One claim boundary explains the conditional procedure without fragmenting lifecycle, review, CI, and release checks. | O1 and O2 under-address conditional loading; O4 over-fragments it. |
| 2026-08-11 | Keep the result structure inline. | It is compact, shared across profiles, and does not justify another package resource. | A new asset adds indirection without meaningful common-path savings. |
| 2026-08-11 | Keep simplification evidence change-local. | Size and disposition evidence proves this refactor but is not a durable product invariant. | Permanent simplicity gates and runtime journeys add unrelated infrastructure. |
| 2026-08-11 | Default architecture assessment to not required. | Existing architecture already defines mapped skill packages and parity. | Architecture changes remain conditional and will be owned by this change if required. |

## Next Artifacts

- Independent `proposal-review` of this direction.
- A focused `verify` skill-simplification spec if the proposal is accepted.
- A bounded architecture assessment after spec review; an architecture update and review only when that assessment requires it.
- An execution plan and test spec after proposal, spec, and architecture settlement.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`.
The proposal selects the package boundary, trigger model, resource ownership, failure behavior, proof boundary, and measurement interpretation needed for review.
It does not claim specification or implementation readiness.
