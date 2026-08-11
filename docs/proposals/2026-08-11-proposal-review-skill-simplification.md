# Proposal-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`

## Problem

The published `proposal-review` skill is rigorous but its common path loads substantially more procedure than a typical advisory review needs. Its 346-line, 2,295-word `SKILL.md` combines universal proposal judgment with detailed durable-recording mechanics, lifecycle settlement, automated review independence, bootstrap gates, standing-artifact rules, scope-budget procedure, and repeated output structures.

Several contracts also have more than one textual owner. Material-finding fields appear in the main file and an asset, result fields appear in inline output guidance and an asset, and recording, settlement, artifact lookup, and handoff rules overlap across multiple sections. This increases reading cost, creates synchronization risk, and makes the skill harder to use without improving review quality.

The optimization must reduce ordinary loaded context without weakening independent challenge, vision and scope checks, material-finding rigor, formal recording, lifecycle ownership, or claim boundaries. Moving prose into references is useful only when the references correspond to genuine conditional procedure and total package growth is reported honestly.

## Goals

- Make the direct advisory review path materially shorter and easier to scan while preserving all behaviorally significant review rules.
- Give every universal rule, conditional procedure, and repeated output structure one clear owner.
- Keep `SKILL.md` self-sufficient for target identification, authority resolution, core proposal judgment, materiality decisions, safe status selection, isolation, stops, claims, and resource selection.
- Load detailed recording and settlement procedure only when durable review evidence is required.
- Load specialized proposal gates only when vision exception, standing-artifact, bootstrap, or broad scope-budget evidence triggers them.
- Preserve canonical-to-generated, packed, and installed resource parity under the existing published-skill package model.
- Prove semantic preservation and literal compatibility without executing a target-agent runtime or creating a permanent simplicity validator.

## Non-goals

- Do not weaken problem framing, option diversity, decision rationale, vision fit, scope control, risk analysis, or readiness judgment.
- Do not change proposal statuses, material-finding meaning, recording obligations, lifecycle settlement, workflow continuation authority, or downstream stage ownership.
- Do not create a generic shared review framework or move `proposal-review` policy into another skill.
- Do not optimize other skills in this change.
- Do not add a runtime router, scheduler, state store, model journey, transcript grader, or target-agent acceptance harness.
- Do not add another result or finding asset.
- Do not turn line, word, token, or prose-quality measurements into permanent product gates.

## Vision fit

**Aligned.** The change strengthens the project vision of explicit, auditable, deterministic workflow contracts by reducing accidental prose duplication while keeping evidence, review independence, lifecycle recording, and claim safety intact. Progressive disclosure improves daily usability without replacing governed procedure with opaque automation.

## Context

The current package contains `SKILL.md`, `assets/review-result-skeleton.md`, and `assets/material-finding.md`. Its baseline is 397 lines, 2,485 words, and 18,375 UTF-8 bytes across the complete package; `SKILL.md` alone is 346 lines, 2,295 words, and 16,879 bytes.

The skill serves several different contexts:

| Context | Typical need |
| --- | --- |
| Direct advisory review | Identify the target, challenge the proposal, report findings and readiness, and stop without workflow continuation. |
| Formal lifecycle review | Perform the same judgment, then create durable review evidence and settle only the proposal artifact's review state. |
| Material advisory review | Preserve isolation but create detailed durable finding evidence even when formal lifecycle authority is absent. |
| Specialized proposal gate | Apply detailed vision-exception, bootstrap, standing-artifact, or broad scope-budget procedure when evidence triggers it. |
| Automated formal review | Preserve reviewer independence, neutral evidence packets, phase receipts, and workflow-managed recording without changing the review standard. |

The existing architecture already defines a published skill as a canonical `SKILL.md` plus explicitly mapped references and assets. References are packaged procedure rather than independent lifecycle owners, and assets may own structure but not policy. This change applies that model to `proposal-review`.

The initial user goals are all in scope: optimize `proposal-review`, select the best solution, work on a new branch, author a proposal, and perform proposal review. No initial goal is dropped or deferred.

## Options Considered

### Option 0: Keep the package unchanged

This preserves behavior with no migration risk but leaves common-path overload and duplicated ownership unresolved.

### Option 1: Edit and deduplicate only inside `SKILL.md`

This can remove repeated phrasing and inline templates with the smallest package change. It cannot avoid loading detailed lifecycle, automation, and specialized-gate procedure during an ordinary advisory review, so its context reduction is limited.

### Option 2: Add only a recording-and-settlement reference

This removes the largest formal-lifecycle block from advisory use and gives durable recording one owner. Specialized vision, bootstrap, standing-artifact, and scope-budget procedure would still load for every review, even though most proposals do not trigger those gates.

### Option 3: Use two coherent conditional references and the existing assets

This keeps universal proposal judgment inline, moves detailed durable recording and settlement into one reference, and moves specialized proposal-gate procedure into a second reference. The existing assets become the sole structural output source. Two references match two independent activation boundaries without fragmenting the review method.

### Option 4: Split each review dimension into a separate reference

This could minimize individual files but would create excessive resource selection, cross-reference traffic, and ownership ambiguity. Core judgment would become harder to perform and missing-resource failures would multiply.

### Option 5: Replace prose procedure with a shared review engine or generic review skill

This could centralize mechanics but would introduce new runtime or cross-skill policy ownership, broaden scope, and obscure the proposal-specific decision contract. It is disproportionate to a content simplification.

## Recommended Direction

Adopt Option 3.

The target package is:

```text
skills/proposal-review/
├── SKILL.md
├── references/
│   ├── proposal-review-recording-and-settlement.md
│   └── conditional-proposal-gates.md
└── assets/
    ├── review-result-skeleton.md
    └── material-finding.md
```

### Universal common path

`SKILL.md` remains the semantic owner of:

- purpose, trigger, role, and near-miss routing;
- advisory versus formal classification and isolated versus workflow-managed handoff authority;
- review-target identity, evidence authority, and bounded evidence reading;
- the default formal review record path required by the installed-skill artifact-placement contract;
- core review dimensions, including problem clarity, user value, option quality, decision rationale, scope, risks, rollout, testing, readiness, and basic vision fit;
- material-finding definition, severity, required fields, status vocabulary, and readiness limits;
- universal isolation, stop conditions, claim boundaries, and downstream handoff restrictions;
- universal durable-recording obligation and exact resource-load triggers;
- output applicability and missing-resource failure behavior.

### Recording-and-settlement reference

`references/proposal-review-recording-and-settlement.md` owns only detailed durable procedure:

- artifact and owning-change-record lookup;
- clean receipt versus detailed review record selection;
- material-finding recording, review-log synchronization, and review-resolution requirements;
- exact formal proposal artifact settlement and bounded change-record writes;
- retry and concurrent-update handling;
- automated formal-review independence, neutral packet, phase receipt, and correction-loop boundaries;
- workflow-managed review completion and handoff mechanics.

The reference loads when `durable_recording_context` is true. That predicate is true for a formal lifecycle review, a material or blocking result, or an explicit durable-record request. Formal review implies durable recording, but durable recording does not imply workflow authority or downstream continuation.

The formal-only settlement subsection applies only when current workflow evidence identifies this exact proposal review for the same governed change. An isolated material review records findings but does not settle lifecycle state or advance the workflow.

### Conditional proposal-gates reference

`references/conditional-proposal-gates.md` owns detailed procedure for:

- vision conflict and explicit exception handling beyond the universal basic vision-fit check;
- bootstrap and standing-artifact gates;
- broad or multi-workstream scope-budget review;
- specialized source-of-truth and governance checks activated by those contexts.

The reference loads when at least one closed predicate is true:

```text
vision_exception_context
standing_artifact_context
scope_budget_context
```

Basic vision alignment, initial-goal preservation, ordinary scope control, and unknown-authority stops remain inline. The conditional reference specializes a triggered gate but does not redefine review status, materiality, recording, or handoff.

### Closed resource assemblies

| Assembly | Durable recording | Specialized gate | Loaded content |
| --- | ---: | ---: | --- |
| `PRR0-core` | no | no | `SKILL.md` and applicable output assets |
| `PRR0G-context-gated` | no | yes | Core plus conditional proposal gates |
| `PRR1-recorded` | yes | no | Core plus recording and settlement |
| `PRR1G-recorded-context-gated` | yes | yes | Core plus both references |

Loading profile and execution authority are separate. A recorded isolated review may use `PRR1` without formal settlement, while a formal review uses the same package and applies only the workflow-managed subsection authorized by current change-local state.

If a clean advisory review becomes material during judgment, the skill loads the recording reference before emitting the final result and records the finding without inventing workflow authority.

### Output ownership

`assets/review-result-skeleton.md` remains the sole copy-and-fill structure for the overall result. `assets/material-finding.md` remains the sole repeated structure for each material finding. The assets own labels and layout only; `SKILL.md` and the applicable reference own field meaning, status selection, applicability, recording, and handoff policy.

Inapplicable conditional fields are omitted. Unfilled placeholders and inline copies of the asset structures are forbidden.

### Conflict and failure rules

A conditional reference may specialize procedure for its activation context but may not override an inline universal rule or another reference's owned contract. A contradiction among package resources is a package defect and stops the dependent action.

When a required reference or asset is missing or unreadable, the skill stops before the dependent recording, settlement, specialized-gate judgment, or output operation. The shortened common path must not reconstruct conditional procedure from memory. An untriggered missing reference does not block a review that does not need it, although package validation remains failing.

### Preservation evidence

Create two separate change-local inventories:

```text
docs/changes/2026-08-11-proposal-review-skill-simplification/proposal-review-rule-disposition.yaml
docs/changes/2026-08-11-proposal-review-skill-simplification/proposal-review-literal-compatibility.yaml
```

Every behaviorally significant rule receives one disposition: `retained-inline`, `retained-recording-reference`, `retained-conditional-gates-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`.

Every exact heading, phrase, field label, path, and vocabulary dependency is separately classified as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`. Contract literals are preserved or formally amended; parser contracts and consumers migrate atomically; incidental assertions do not become prose-policy owners.

## Expected Behavior Changes

- A routine advisory proposal review loads a shorter linear `SKILL.md` and the applicable structural assets, without detailed formal lifecycle or specialized-gate procedure.
- A formal review loads the recording-and-settlement reference and preserves current durable evidence, settlement, independence, and handoff behavior.
- An isolated material review records detailed findings while remaining isolated from lifecycle mutation and downstream continuation.
- Vision exceptions, standing-artifact or bootstrap cases, and broad multi-workstream proposals load the conditional proposal-gates reference only when their evidence predicates apply.
- Result and material-finding structures are copied from the existing assets instead of being restated inline.
- Missing required resources stop the dependent action with a precise package-incomplete diagnostic.
- Review statuses, severity, proposal readiness, recording requirements, and stage ownership remain unchanged.

## Architecture Impact

Record a bounded architecture assessment with the expected result `architecture-not-required`. The existing architecture already supports canonical packaged skills with mapped references and assets, raw-byte generated and installed parity, references as skill-owned procedure, and assets as structural leaves.

A bounded architecture documentation update is appropriate only if a current table, diagram, or example incorrectly depicts `proposal-review` as a permanently flat package or lists an outdated resource inventory. No ADR is warranted unless the specification changes the normative package model or gives a reference independent policy ownership.

If the owning `change.yaml` determines that an architecture artifact is required, this change owns that architecture document and its review rather than assigning architecture ownership to an unrelated change.

## Testing and Verification Strategy

Use three proof classes.

### Deterministic structural proof

Validate frontmatter, normalized headings, closed vocabularies, `Resource map` syntax, resource existence and containment, placeholder absence, forbidden claims, canonical skill structure, generated package inventory, archive contents, installed-resource presence, and raw-byte parity.

### Static contract scenarios

Create change-local fixtures for at least:

- clean direct advisory review using `PRR0-core`;
- clean formal lifecycle review using `PRR1-recorded`;
- an advisory review that discovers a material finding and loads recording late;
- a formal review whose record cannot be written;
- a vision-conflict proposal using the conditional gates reference;
- a bootstrap or standing-artifact proposal;
- a broad multi-workstream scope-budget review;
- a review with no specialized trigger that does not load the conditional gates reference;
- a formal specialized review using both references;
- isolated recording without lifecycle settlement;
- missing required reference and missing required asset failures;
- canonical, generated, packed, and installed package parity.

Scenarios assert required and forbidden contract outcomes without executing an LLM.

### Independent semantic review

Review the final package and the two inventories for trigger clarity, target identity, evidence authority, option and vision rigor, scope preservation, materiality, status correctness, recording, settlement, isolation, stop conditions, claims, output usefulness, and handoff clarity.

Do not execute Codex, Claude Code, opencode, or another target-agent runtime for implementation, verification, or release acceptance. Do not add prompt journeys, transcript grading, model-version evidence, or a permanent simplicity/tokenizer validator.

Use normalized-LF UTF-8 bytes and Unicode whitespace-separated words as primary measurements. Count each uniquely loaded resource once in documented load order. Report `SKILL.md`, each resource, each valid assembly, and total package size separately. A 30–45 percent reduction in common-path words and bytes is a planning target, not a normative semantic gate; no material common-path reduction means the proposal objective is not met.

## Rollout and Rollback

Implement the change atomically in canonical `skills/` source, update directly coupled specs or deterministic consumers, regenerate temporary adapter packages through existing commands, and prove mapped-resource parity before release. Do not hand-edit generated public adapter output.

Rollback reverts the canonical skill, references, coupled contract changes, and validation updates as one unit, then regenerates and revalidates packages. The change-local inventories and measurements remain historical evidence of what was attempted.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| A universal review rule is hidden behind a conditional reference. | Require a complete semantic rule-disposition ledger and independent semantic review; keep target, evidence, materiality, status, isolation, stops, and claims inline. |
| A recorded isolated review accidentally settles workflow state. | Separate loading profile from execution authority and make formal settlement depend on current identity-bound workflow evidence. |
| Specialized gates overlap with the core review method. | Give the reference only detailed exception, bootstrap, standing-artifact, and scope-budget procedure; retain ordinary vision and scope judgment inline. |
| Assets become policy owners. | Limit assets to labels and layout and reject policy explanations or status semantics in them. |
| Tests freeze incidental prose. | Classify literal dependencies separately and update test-only incidental assertions rather than preserving accidental wording. |
| Relocation is reported as deletion. | Report common-path and total-package measurements separately and explain any package growth. |
| A partial installation encourages invented fallback behavior. | Stop before dependent actions when a triggered resource is unavailable and preserve deterministic package parity checks. |
| The change expands into a generic review-platform redesign. | Keep scope to `proposal-review` and directly coupled contract and package surfaces. |

## Open Questions

None. The specification should inventory exact current literal consumers and validation command owners, but the proposal closes the package design, activation predicates, ownership, failure behavior, measurement boundary, and architecture expectation.

## Decision Log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-11 | Use two conditional references. | Durable recording and specialized proposal gates are independent, evidence-triggered procedures. |
| 2026-08-11 | Keep universal proposal judgment inline. | Every review must classify the target, challenge the decision, determine materiality, and respect claims before optional procedure is loaded. |
| 2026-08-11 | Separate loading profile from execution authority. | Durable evidence may be required in an isolated review without granting lifecycle settlement or continuation authority. |
| 2026-08-11 | Reuse the two existing assets as sole structural templates. | This removes duplicate layout while keeping policy in the governing skill package. |
| 2026-08-11 | Use semantic and literal ledgers as change-local evidence. | Behavior preservation and accidental wording compatibility are different proof problems. |
| 2026-08-11 | Exclude target-agent runtime testing and permanent simplicity gates. | Static contract proof, package parity, and independent semantic review match the change boundary. |
| 2026-08-11 | Treat percentage reduction as advisory. | Semantic preservation and single ownership outrank numeric optimization. |

## Next Artifacts

- Formal `proposal-review` evidence for this proposal.
- A focused skill-contract specification if the proposal is accepted.
- A bounded architecture assessment owned by this change.
- An execution plan and matching test specification after specification approval.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. This proposal does not claim specification approval, architecture completion, implementation readiness, branch readiness, or PR readiness.
