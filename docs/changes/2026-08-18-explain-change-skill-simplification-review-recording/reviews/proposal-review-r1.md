# Proposal Review: Explain-Change Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-18-explain-change-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-18-explain-change-skill-simplification.md` at `sha256:65ae800e28325ae962585be88396903eb417b90f784832c04637b6e70ca8847d`
Review date: 2026-08-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: EXCSIM-PR1, EXCSIM-PR2, EXCSIM-PR3
- Open blockers: the loaded-assembly model, single-file recovery contract, and complete measurement gate require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this isolated review records judgment only; it does not settle the portable proposal, activate a governed change, authorize specification, or continue the workflow

## Overall assessment

The selected package shape is proportionate:

```text
compact universal SKILL.md
+ one governed workflow-explanation reference
+ one durable explanation skeleton
```

The proposed boundary is real. Actual-diff grounding, truthful traceability, scope honesty, validation-gap disclosure, stops, claims, and resource triggers belong on every invocation. Exact change-local placement, final-review eligibility, review-resolution closeout, staleness comparison, and workflow return apply only after governed context is detected. Giving repeated durable Markdown structure one asset is also consistent with the accepted constructive-skill resource model.

The proposal is particularly strong in keeping `explain-change` read-only toward upstream artifacts and lifecycle state, preserving final `explain-change -> verify -> pr` ownership, rejecting target-agent acceptance, distinguishing semantic rules from consumed literals, and requiring the real workflow-loaded profile to improve.

Three operational details remain incomplete. A valid governed inline invocation has no loaded assembly, the promised interrupted-write retry cannot prove its own identities without a prepared record or an atomic-write guarantee, and one declared profile is excluded from the acceptance reduction requirement.

## What is strong

### The progressive-disclosure boundary follows authority

Portable explanation does not need RigorLoop-specific lifecycle inspection. Governed explanation still validates the exact final reviewed change and cannot infer authority merely because a reference loaded.

### Universal explanation quality remains self-sufficient

The root file retains the rules needed to produce a truthful inline explanation: actual diff, evidence-backed traceability, unknowns, unrelated changes, scope, risks, validation limits, privacy, stops, and claims.

### Structural ownership is appropriately narrow

The proposed asset owns headings, ordering, table columns, metadata locations, conditional-group insertion points, and placeholders. Applicability, evidence sufficiency, staleness, and readiness remain procedural.

### Compatibility and measurement are evidence-led

Separate semantic and literal inventories avoid treating every current exact-string assertion as permanent root-file ownership. Canonical-through-installed resource parity and complete package size remain visible.

## Material findings

### EXCSIM-PR1 - Governance and durable output are not represented as independent axes

Finding ID: EXCSIM-PR1
Severity: major
Location: `Recommended Direction`, sections `Classify output action independently from governance`, `Use tri-state governed-signal classification`, and `Define three real loaded assemblies`
Evidence: The proposal says output action and governance are independent. It also makes an explicit change ID or structured change-local target a governed signal. A direct isolated request can therefore name an exact change while asking only for an inline explanation when the project contract does not require durable reasoning. That invocation must load the governed reference to validate the signal, but it does not copy the durable skeleton. None of `EC0`, `EC1`, or `EC2` represents `SKILL.md + governed reference` without the asset. `EC2` is explicitly governed-durable and always includes the skeleton. The same gap makes late reclassification and measurement non-exhaustive.
Required outcome: Represent every valid governance/output combination or explicitly prohibit the missing combination under an existing higher-priority contract.
Safe resolution path: Keep the axes independent and define four assemblies: portable-inline (`SKILL.md`), portable-durable (`SKILL.md` plus asset), governed-inline (`SKILL.md` plus reference), and governed-durable (`SKILL.md` plus reference and asset). State that invalid governed signals stop before either output and that a workflow durable obligation selects the governed-durable assembly. Measure all four. If governed inline is intentionally prohibited, cite the contract that makes every exact governed invocation durable and remove contradictory inline language.
needs-decision rationale: none; the proposal can close the cross-product without changing the selected package.

### EXCSIM-PR2 - Retry claims lack a durable or atomic recovery basis

Finding ID: EXCSIM-PR2
Severity: major
Location: `Recommended Direction`, sections `Bind governed explanation to one exact basis` and `Use one bounded durable write protocol`, plus `Architecture Impact`
Evidence: The proposal permits an interrupted identical refresh to continue when the target matches a recorded prior or intended identity, but it does not durably record those identities before mutation. It explicitly rejects a new transaction record and defers metadata location. If interruption occurs after a partial non-atomic write and before the completed artifact contains its basis, a later invocation cannot distinguish the intended partial output from unrelated edits or reconstruct the intended identity. The phrase “ordinary safe file-write mechanism” does not guarantee atomic replacement or establish where the retry identity survives a crash.
Required outcome: Choose one provable single-file mutation and recovery model before specification.
Safe resolution path: Prefer the smaller first-version contract: prepare and validate the complete artifact, re-read the prior identity and decision basis, perform one atomic replacement of the exact target, and read it back. Remove resumable partial-write claims. A failed or uncertain replacement reports `blocked`; a later invocation resolves current bytes and begins a fresh create or refresh rather than adopting a partial attempt. Persist the successful explanation basis in the completed artifact. If the repository cannot guarantee the required replacement semantics and resumable recovery remains required, add a durable prepared manifest and change the architecture expectation when that needs a new schema or owner.
needs-decision rationale: none; the proposal should select atomic single-file replacement or prepared persistence explicitly.

### EXCSIM-PR3 - Acceptance does not require every declared profile to improve

Finding ID: EXCSIM-PR3
Severity: major
Location: `Goals`, `Testing and Verification Strategy`, measurement block, and `Risks and Mitigations`
Evidence: The goals promise reduced loaded procedure for inline portable, durable portable, and governed durable explanation, and the measurement block reports all three. The acceptance sentence requires only `EC0` and `EC2` to decrease. `EC1` may therefore grow beyond the current flat baseline while the proposal still claims success. After EXCSIM-PR1 is resolved, the same omission would apply to governed-inline. The proposal also does not state whether copied asset bytes count in a durable assembly, although its loaded-content table includes the asset.
Required outcome: Define one measurement formula and require improvement for every supported loaded assembly.
Safe resolution path: Count each loaded file once in the assembly's words and bytes: root only, root plus reference, root plus asset, or root plus both. Require every supported assembly to be smaller than the current 1,175-word / 8,224-byte flat baseline, while reporting root, reference, asset, complete package, and optional estimated-token values separately. If one assembly cannot improve without weakening clarity, require an explicit proposal amendment rather than silently exempting it.
needs-decision rationale: none; this closes the proposal's central value claim.

## Architecture assessment

The expected outcome remains `architecture-not-required` if revision selects atomic single-file replacement and stores the successful basis in the existing explanation artifact. Four loaded assemblies do not add resources; they only make existing combinations explicit. Architecture becomes required if safe recovery needs a new prepared transaction artifact, schema, lifecycle state, or write owner.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-EXCSIM-001` | Governance classification and output action remain independent. |
| `AC-EXCSIM-002` | Every valid governance/output combination has one named loaded assembly. |
| `AC-EXCSIM-003` | Governed inline explanation loads the reference but not the durable skeleton. |
| `AC-EXCSIM-004` | A governed durable obligation loads both the reference and skeleton. |
| `AC-EXCSIM-005` | Invalid or ambiguous governed signals stop without portable fallback. |
| `AC-EXCSIM-006` | The first-version single-file write protocol has one explicit atomic or prepared recovery model. |
| `AC-EXCSIM-007` | No retry adopts partial content whose intended identity was not durably established. |
| `AC-EXCSIM-008` | A completed governed explanation stores the exact basis needed for later staleness checks. |
| `AC-EXCSIM-009` | Every supported loaded assembly is measured using one closed formula. |
| `AC-EXCSIM-010` | Every supported assembly decreases from the current flat baseline. |
| `AC-EXCSIM-011` | Complete package growth is reported independently from loaded-profile improvement. |
| `AC-EXCSIM-012` | No target-agent runtime or separate prose-grading acceptance stage is introduced. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Flat common-path lifecycle procedure and embedded repeated structure are concrete. |
| User value | pass | A mandatory workflow stage and common manual explanation path both benefit from smaller context. |
| Option diversity | pass | Flat, editorial, asset-only, one-reference, fragmented, and executable approaches are materially distinct. |
| Decision rationale | pass | One governed reference and one structural asset match the real activation boundaries. |
| Vision fit | pass | Durable human-readable rationale and explicit authority remain intact. |
| Scope control | pass | Runtime, new lifecycle state, historical migration, and unrelated skill optimization remain excluded. |
| Architecture awareness | pass with revision | Existing package architecture suffices if single-file recovery is made provable without new persistence. |
| Testability | block | The current retry claim has no observable pre-write identity and one declared profile may escape the improvement gate. |
| Risk honesty | pass | Universal-rule loss, parser literals, stale basis, concurrent edits, resource failure, and package growth are named. |
| Rollout realism | concern | Rule/literal inventories and package parity are sound; the mutation and measurement contracts need closure. |
| Readiness for spec | block | Resolve EXCSIM-PR1 through EXCSIM-PR3 and pass same-stage rereview. |

## Scope Preservation Review

- Scope-preservation result: pass. Every user goal is classified with an allowed treatment, directly coupled contract and package work remains visible, and runtime generation, unrelated skills, and new persistence are explicitly out of scope.

## Recommended Proposal Edits

- Replace the three-profile table with an exhaustive governance/output assembly matrix.
- Replace partial-write retry with atomic single-file replacement and fresh reclassification after uncertain failure, unless a prepared durable manifest is explicitly selected.
- Persist the successful governed explanation basis in the completed artifact using specification-defined fields.
- Require every supported loaded assembly to decrease under one formula that includes each copied or read resource once.
- Rerun independent proposal review against the revised artifact identity.

## Recommendation

- Recommendation: changes-requested. Retain the one-reference/one-asset direction, revise the proposal to close EXCSIM-PR1 through EXCSIM-PR3, then perform a new isolated proposal review. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; directly coupled contract, package, validator, architecture, and excluded runtime work are classified explicitly
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: `proposal-review-r1`
- Review record: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-08-18-explain-change-skill-simplification-review-recording/review-resolution.md#proposal-review-r1`
- Proposal settlement: not-settled; the recording-only root has no proposal lifecycle authority
- Governed change identity: none; recording-only root `2026-08-18-explain-change-skill-simplification-review-recording`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
