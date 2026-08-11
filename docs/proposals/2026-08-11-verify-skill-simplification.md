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
- Classify every invocation through a closed requested-outcome vocabulary and an exact target-resolution result.
- Separate loaded-resource selection from isolated versus governed execution authority.
- Give each behaviorally significant verification rule one explicit owner and destination.
- Load detailed branch-readiness and final-closeout procedure only when the requested result depends on it.
- Keep evidence-type truthfulness available to scoped verification while conditionalizing only final evidence applicability and aggregation.
- Preserve `verify` ownership of `branch-ready` while preserving `pr` ownership of PR-body and PR-open readiness.
- Preserve lifecycle, review-resolution, validation, CI, release, generated-output, manual-proof, boundary-first, stop, and handoff semantics.
- Preserve deterministic canonical, generated, packed, and installed package resources.
- Measure loaded content by invocation profile and report total package size separately, so relocation is not described as deletion.

## Non-goals

- Weakening the evidence required for `branch-ready` or changing which stage owns that claim.
- Changing workflow stage order, `change.yaml` schema, review settlement, planned-work semantics, selector behavior, CI policy, release policy, or PR authorization.
- Giving `verify` authority to claim release publication, deployment completion, PR-body readiness, PR-open readiness, or external action completion.
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
| Closed requested outcomes, target resolution, execution-mode classification, and exact resource triggers | Determines the valid loaded package and permitted authority. |
| Evidence authority and source precedence | Universal to every verification claim. |
| Evidence-type interpretation | Any scoped request may inspect commands, CI, generated output, manual proof, or release metadata. |
| Compact verification dimensions | Every verification scope needs a consistent quality model. |
| Validation integrity | Tests, commands, CI, and generated-artifact claims must remain evidence-bound. |
| Direct-verification isolation | A scoped check must not imply workflow completion. |
| `branch-ready` and PR claim boundaries | Claim ownership may never depend on an optional reference. |
| Universal blockers and upstream-gap routing | Unsafe work stops before optional procedure. |
| Compact boundary-first bridge and both resource-map entries | Required for correct progressive disclosure. |
| Compact result, status, and handoff contract | Every invocation must return a useful, bounded result. |

The inline verification dimensions may be expressed compactly, but they continue to cover contract satisfaction, proof validity, architecture and artifact coherence, lifecycle and review state, validation evidence, drift, risk, and release or handoff readiness when applicable.

Universal evidence interpretation remains inline:

- actual execution is distinct from a configured or suggested command;
- current evidence is distinct from stale evidence;
- passed, failed, skipped, pending, not-run, and unknown states are not interchangeable;
- CI claims require observed CI evidence and remain distinct from local validation;
- generated-output currency is judged against its authoritative source and applicable generation contract;
- manual proof has a minimum validity contract and cannot be inferred from assertion alone;
- unknown, conflicting, circular, or insufficient evidence cannot support a stronger claim;
- a scoped conclusion identifies when broader readiness would require more evidence; and
- network, destructive-action, publication, credential, and external-state boundaries apply before any optional procedure.

A scoped verification can therefore assess an individual CI result, generated artifact, manual-proof record, release-metadata file, command result, requirement, or other supported evidence surface without loading final-closeout procedure.

### Conditional branch-readiness reference ownership

`references/branch-readiness-verification.md` owns only the detailed procedure needed when the requested outcome is `branch-readiness` or `workflow-final-verification`:

- final-verification prerequisites and authoritative related-artifact assembly;
- requirement-to-test-to-diff-to-evidence traceability procedure;
- baseline change-pack and durable-rationale checks;
- lifecycle artifact, plan/index, milestone, review-log, and review-resolution closeout inspection;
- tracked governing branch-state requirements;
- determination of which targeted proof, broad smoke, CI evidence, generated outputs, manual proof, and release metadata are mandatory for the resolved target;
- final composition of those evidence classes, including when targeted proof must be supplemented by broad smoke and when current CI evidence is required;
- release-sensitive final evidence composition when `release_sensitive: true`;
- workflow-managed Phase C applicability and fresh-actual-run completeness;
- final blocker aggregation, `branch-ready` calculation, verification recording, and `pr` handoff.

The reference does not redefine status vocabulary, evidence-type meaning, claim authority, universal stop rules, workflow stage order, or PR authorization.
It remains part of the `verify` skill package and does not become an independent lifecycle owner.

The reference may contain clearly marked common final-readiness, isolated completion, and governed-final completion sections.
Execution-mode classification determines which completion section applies.
The reference cannot infer execution mode from informal prompt wording.

### Requested verification outcomes

The first version supports exactly three requested outcomes:

```text
scoped-verification
branch-readiness
workflow-final-verification
```

| Requested outcome | Required context | Branch-readiness reference | Permitted top-level claim |
| --- | --- | ---: | --- |
| `scoped-verification` | One explicit command, artifact, requirement, evidence item, or validation surface | no | Scoped `pass`, `fail`, or `inconclusive` only |
| `branch-readiness` | Explicit repository and branch or commit plus exactly one governed change or explicit evidence root | yes | `branch-ready` or `not-ready` for the resolved target |
| `workflow-final-verification` | Exactly one valid governed change whose current authoritative routing resolves final `verify` as the applicable stage | yes | Formal final-verification outcome under existing verify authority |
| Unknown or ambiguous | No valid context | no | Stop before conditional procedure loads |

A direct invocation may request `branch-readiness` when its target resolves exactly.
A direct invocation cannot create `workflow-final-verification` by using words such as “final,” “closeout,” “ready,” or “verify”; that outcome requires current governed lifecycle evidence.
A scoped request cannot silently broaden into final readiness.

Release sensitivity is a boolean evidence-applicability property of the resolved change:

```yaml
release_sensitive: true
```

It selects additional evidence inside final-readiness procedure.
It does not create a fourth requested outcome or authorize a release, publication, deployment, or external-completion claim.

### Target resolution

Before loading the branch-readiness reference:

1. Resolve the repository and exact branch or commit being assessed.
2. Resolve exactly one governed change root or user-supplied explicit evidence root.
3. Confirm the proposed evidence set belongs to that repository, revision, and change or evidence identity.
4. Determine release sensitivity from governing evidence, or stop when applicability is material and undecidable.
5. Stop when any identity is missing, ambiguous, stale, contradictory, or spans multiple candidate changes.

The stop result names the unresolved identity and does not load or partially reconstruct final-readiness procedure.
The recommended diagnostic shape is:

```text
cannot perform branch-readiness verification:
the request does not resolve exactly one governed change or evidence root and one branch or commit identity
```

### Loaded-package profiles

Loaded resources follow requested outcome and boundary applicability, not execution authority.

The boundary-first trigger remains independently additive when approved boundary, interaction, or proof trace is missing, stale, unknown, ambiguous, conflicting, or insufficient.

| Profile | Requested outcome | Boundary-first trigger | Loaded package |
| --- | ---: | ---: | --- |
| `VP0-scoped` | `scoped-verification` | no | `SKILL.md` |
| `VP0B-scoped-boundary` | `scoped-verification` | yes | `SKILL.md` plus boundary-first reference |
| `VP1-final-readiness` | `branch-readiness` or `workflow-final-verification` | no | `SKILL.md` plus branch-readiness reference |
| `VP1B-final-readiness-boundary` | `branch-readiness` or `workflow-final-verification` | yes | `SKILL.md` plus both references |

A scoped direct verification may report only the evidence and verdict for its requested scope.
It does not claim branch readiness or workflow completion.
A direct invocation that explicitly requests a resolved branch-readiness verdict is valid `VP1` or `VP1B` and remains isolated after reporting.

### Execution authority

Loaded-package profile and execution authority are independent.
The closed execution modes are:

```text
isolated
governed-final
```

`VP1` and `VP1B` may use either mode.
Resources determine which procedure is available; execution mode determines which completion branch and writes are permitted.

| Execution mode | Required authority | Verify-owned recording | Workflow progression | PR behavior |
| --- | --- | --- | --- | --- |
| `isolated` | Direct scoped verification, or a direct branch-readiness request with an exactly resolved target | Only when explicitly requested and already allowed by the existing verify contract | forbidden | Report `pr` only as a possible next stage; never invoke it or prepare PR content |
| `governed-final` | Current governed evidence establishes `workflow-final-verification` for the same change identity | Required according to existing verify ownership | Performed only by the existing workflow owner, never by `verify` inference | Hand off toward `pr`; never prepare or open the PR itself |

`verify` writes only artifacts and evidence already assigned to `verify`.
`workflow` owns lifecycle transition and continuation.
`pr` owns PR-body preparation and PR opening.
A clean isolated result never advances workflow state.

### Resource failure behavior

If the requested outcome is `branch-readiness` or `workflow-final-verification` and `branch-readiness-verification.md` is missing or unreadable, verification stops before a dependent verdict, recording action, or handoff.
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
- Every invocation resolves to one of three requested outcomes or stops as unknown or ambiguous.
- Branch readiness resolves one repository revision and one governed change or explicit evidence root before conditional procedure loads.
- Release sensitivity adds evidence requirements without creating publication or release authority.
- Requests for `branch-readiness` or `workflow-final-verification` load one coherent branch-readiness procedure.
- Direct full branch-readiness verification remains possible but isolated; direct invocation does not activate workflow continuation.
- Loaded resources and execution authority remain independent, so direct and governed final verification can share procedure without sharing write permissions.
- Scoped requests can judge CI, generated output, manual proof, command evidence, and release metadata without loading final aggregation procedure.
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
2. Static contract scenarios cover all three requested outcomes; successful, missing, and ambiguous target resolution; both execution modes; every profile; required and forbidden reference loads; missing-resource stops; isolated write prohibitions; scoped evidence-type checks; branch-ready blockers; review and lifecycle closeout; `release_sensitive` true and false; and boundary-first additive loading.
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

The downstream specification should make these proposal decisions directly testable:

| Acceptance area | Expected contract |
| --- | --- |
| Requested outcomes | Exactly the three named outcomes; unknown or ambiguous requests stop. |
| Target identity | Final readiness resolves one repository revision and one change or evidence root. |
| Release sensitivity | Boolean applicability only; no release or publication claim. |
| Resource profiles | Exactly four loaded-package assemblies with boundary-first additive. |
| Execution authority | `isolated` and `governed-final` are independent of resource assembly. |
| Write boundaries | Isolated mode does not advance workflow or invoke `pr`; governed mode preserves existing verify, workflow, and pr ownership. |
| Evidence ownership | Item-level truthfulness stays inline; final applicability and aggregation live in the branch-readiness reference. |
| Scoped capability | CI, generated output, manual proof, commands, and release metadata can be assessed without final-closeout loading. |

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
| Ambiguous target combines evidence from different changes or revisions | A final verdict may be unsound. | Require one repository revision and one change or explicit evidence root before loading final procedure. |
| Direct and governed verification share resources and accidentally share authority | An isolated check could mutate lifecycle state or a governed run could omit recording. | Classify execution mode independently and test every permitted write and handoff. |
| Evidence-type semantics move behind final readiness | Scoped CI, drift, manual-proof, or release-metadata checks become under-specified. | Keep item-level semantics inline and conditionalize only applicability and aggregation. |
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
| 2026-08-11 | Use three requested outcomes and exact target resolution. | Scoped, direct branch, and governed final verification need deterministic claim boundaries. | Open-ended phrases such as final or release readiness are too ambiguous. |
| 2026-08-11 | Separate loaded profiles from execution authority. | Direct and governed final verification may share procedure without sharing lifecycle permissions. | Multiplying package profiles would couple authority to content loading. |
| 2026-08-11 | Keep evidence interpretation inline. | Scoped verification must judge individual evidence classes without final aggregation procedure. | Moving CI, drift, manual-proof, or release semantics entirely into the reference under-specifies `VP0`. |

## Next Artifacts

- Independent `proposal-review` of this direction.
- A focused `verify` skill-simplification spec if the proposal is accepted.
- A bounded architecture assessment after spec review; an architecture update and review only when that assessment requires it.
- An execution plan and test spec after proposal, spec, and architecture settlement.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`.
The proposal selects the package boundary, requested outcomes, target resolution, resource profiles, execution authority, evidence-rule ownership, failure behavior, proof boundary, and measurement interpretation needed for review.
It does not claim specification or implementation readiness.
