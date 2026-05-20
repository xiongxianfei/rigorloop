# Proposal-Family Assets Progressive Disclosure Baseline

This baseline pins the canonical source state used to prove that M2 and M3 are structural asset extractions, not behavior changes.

## Source commit or branch point

- Branch point: `386ff42834e9489ad17a9194b863f40d5332e0af`
- Current implementation branch at baseline capture: `386ff42834e9489ad17a9194b863f40d5332e0af`
- Baseline date: 2026-05-20
- Governing spec: `specs/proposal-family-assets-progressive-disclosure.md`
- Active plan: `docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md`

The phrase "current canonical skill state" means this pinned baseline, not a later branch state.

## Exact canonical source paths

- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`

## Source file hashes

| Source path | SHA-256 |
| --- | --- |
| `skills/proposal/SKILL.md` | `068ceee1efaea9f645c7faf27589a59e3bd795b11b4ad8df7db7774d649b0744` |
| `skills/proposal-review/SKILL.md` | `a1b6a38b0d75f38668bb97a500d0d04471c87f08e050608efd636868d724e5be` |

## `proposal` baseline

### Existing full skeleton section set

Source location: `skills/proposal/SKILL.md`, stable heading `## Output skeleton`.

- `<Proposal title>`
- `Status`
- `Problem`
- `Goals`
- `Non-goals`
- `Vision fit`
- `Context`
- `Options Considered`
- `Recommended Direction`
- `Expected Behavior Changes`
- `Architecture Impact`
- `Testing and Verification Strategy`
- `Rollout and Rollback`
- `Risks and Mitigations`
- `Open Questions`
- `Decision Log`
- `Next Artifacts`
- `Follow-on Artifacts`
- `Readiness`

### Repeated substructure fields to extract

No repeated row-only substructures are extracted for `proposal` in this slice. Initial-intent rows, scope-budget rows, decision-log rows, risk rows, and similar small table rows remain inline in `SKILL.md`.

### Extracted asset source ranges or stable headings

| Planned asset | Source location | Preservation proof |
| --- | --- | --- |
| `skills/proposal/assets/proposal-skeleton.md` | `skills/proposal/SKILL.md`, `## Output skeleton` | Same full skeleton section set and placeholders, plus conditional-section insertion preserved by `SKILL.md` or clearly labeled conditional asset blocks. |

### Conditional sections governed by `SKILL.md`

- `Initial intent preservation`: source location `skills/proposal/SKILL.md`, stable heading `## Initial intent preservation`; include for broad, multi-part, or materially revised requests.
- `Scope budget`: source location `skills/proposal/SKILL.md`, stable headings `## Scope budget for broad proposals` and `## Scope budget`; include when the proposal is broad or multi-workstream.

The extraction must not make either section mandatory for every proposal and must not omit the ability to add either section when triggered.

### Closed enums that remain in `SKILL.md`

- `proposal status`: `draft`, `under review`, `accepted`, `rejected`, `abandoned`, `superseded`, `archived`
- `Vision fit`: `fits the current vision`, `may conflict with the current vision`, `proposes a vision revision`, `no vision exists yet`
- `initial goal treatment`: `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, `open question`
- `scope budget treatment`: `core to this proposal`, `first-slice candidate`, `same-slice dependency`, `separate implementation slice`, `deferable follow-up`, `separate proposal`, `out of scope`

### Scope-preservation and scope-budget rules that remain in `SKILL.md`

- Extract the user's initial goals, concerns, constraints, and requested outcomes before drafting or materially revising a proposal.
- Every initial user goal must be visible with one `initial goal treatment` value.
- Do not silently drop or narrow user goals.
- Use a scope budget when the proposal is broad or multi-workstream.
- Scope-budget applicability remains proposal/proposal-review judgment, not mechanical validator inference.
- Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership.

### Vision fit and standing artifact gate rules that remain in `SKILL.md`

- Include `Vision fit` in new or substantively revised proposals after the vision spec is adopted.
- Use the exact `Vision fit` enum value as the first non-empty line.
- `VISION.md` absence blocks the first substantive proposal unless the proposal is bootstrap work to create project vision.
- `CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless bootstrap work creates or migrates the constitution.
- Bootstrap proposals must identify the bootstrap exception in `Vision fit`.

### Rules, obligations, and handoff boundaries that remain in `SKILL.md`

- Routing, evidence access, artifact placement, required proposal section guidance, decision-quality checks, workflow handoff behavior, output obligations, and full-file-read rules remain in `SKILL.md`.

### Source location for each extracted asset

| Asset | Source location |
| --- | --- |
| `assets/proposal-skeleton.md` | `skills/proposal/SKILL.md`, stable heading `## Output skeleton` |

## `proposal-review` baseline

### Existing full skeleton section set

Source location: `skills/proposal-review/SKILL.md`, stable heading `## Output skeleton`.

- `Result`
- `Material Findings`
- `Review Dimensions`
- `Scope Preservation Review`
- `Recommended Proposal Edits`
- `Recommendation`

### Repeated substructure fields to extract

`review-result-skeleton.md` fields:

- `Skill`
- `Review status`
- `Material findings`
- `Recording status`
- `Recording blocker`
- `Review record`
- `Review log`
- `Review resolution`
- `Open blockers`
- `Immediate next stage`

`material-finding.md` fields:

- `Finding ID`
- `Severity`
- `Location`
- `Evidence`
- `Required outcome`
- `Safe resolution path`
- `needs-decision rationale`

### Extracted asset source ranges or stable headings

| Planned asset | Source location | Preservation proof |
| --- | --- | --- |
| `skills/proposal-review/assets/review-result-skeleton.md` | `skills/proposal-review/SKILL.md`, `## Output skeleton`, `## Result` block | Same result field set and placeholders. |
| `skills/proposal-review/assets/material-finding.md` | `skills/proposal-review/SKILL.md`, `## Material findings` and `## Output skeleton`, `## Material Findings` block | Same material-finding field set. |

### Conditional sections governed by `SKILL.md`

No proposal-review output sections are extracted as conditional trigger changes in M1. Review-class decision rules and any finding inclusion behavior remain governed by `SKILL.md`.

### Closed enums that remain in `SKILL.md`

- `review dimension result`: `pass`, `concern`, `block`
- `Vision fit`: `fits the current vision`, `may conflict with the current vision`, `proposes a vision revision`, `no vision exists yet`
- `vision conflict outcome`: `revise proposal`, `revise vision`, `record explicit exception`
- `initial goal treatment`: `in scope`, `out of scope`, `deferred follow-up`, `rejected option`, `open question`
- `scope budget treatment`: `core to this proposal`, `first-slice candidate`, `same-slice dependency`, `separate implementation slice`, `deferable follow-up`, `separate proposal`, `out of scope`
- `Recording status`: `recorded`, `blocked`; `not-required` remains reserved for non-formal review-like requests outside the formal lifecycle review model.

### Scope-preservation and scope-budget rules that remain in `SKILL.md`

- Compare the user's initial request with the proposal.
- Every initial goal must be visibly classified with one `initial goal treatment` value.
- Return `changes-requested` for disappearing goals, unrouted deferred goals, rejected goals without rationale, or narrowing without rationale.
- For broad or multi-workstream proposals, check clear classification of current scope, same-slice dependencies, separate implementation slices, deferable follow-ups, separate proposals, and out-of-scope work.
- Do not request a scope budget solely as routine ceremony.
- Scope-budget applicability remains proposal/proposal-review judgment, not validator inference.

### Vision fit and standing artifact gate rules that remain in `SKILL.md`

- Check the proposal's `Vision fit` section when required by the project workflow.
- Request revision when a required `Vision fit` section is missing or conflicts with root `VISION.md` state.
- Classify vision conflicts as `revise proposal`, `revise vision`, or `record explicit exception`.
- Check standing artifact gates before accepting bootstrap or governance-related direction.
- Request revision for missing bootstrap exceptions or silent bypass of required standing artifact gates.

### Review dimensions and recording obligations that remain in `SKILL.md`

Review dimensions:

- `Problem clarity`
- `User value`
- `Option diversity`
- `Decision rationale`
- `Scope control`
- `Architecture awareness`
- `Testability`
- `Risk honesty`
- `Rollout realism`
- `Readiness for spec`

Recording obligations:

- Isolation governs handoff; recording follows formal review triggers.
- Every formal lifecycle review result must be recorded or explicitly blocked.
- Clean reviews create the lightweight review receipt and index it in `review-log.md`.
- Material or blocking findings require detailed review records and disposition artifacts.
- Material findings must include Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale.
- `not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

### Rules, obligations, and handoff boundaries that remain in `SKILL.md`

- Routing, evidence access, artifact placement, review dimensions, Vision fit review, standing artifact gate review, scope preservation review, scope-budget review, adversarial questions, material-finding sufficiency, isolation and recording rules, workflow handoff behavior, output obligations, and full-file-read rules remain in `SKILL.md`.

### Source location for each extracted asset

| Asset | Source location |
| --- | --- |
| `assets/review-result-skeleton.md` | `skills/proposal-review/SKILL.md`, stable heading `## Output skeleton`, `## Result` block |
| `assets/material-finding.md` | `skills/proposal-review/SKILL.md`, stable headings `## Material findings` and `## Output skeleton`, `## Material Findings` block |

## Skill-contract sufficiency assessment for M1

Existing `specs/skill-contract.md` asset rules plus the approved proposal-family spec and active test spec are sufficient for M1 validator and baseline work. M1 does not change skill text or generated output. No skill-contract amendment is required before M1.

Implementation must reassess this before M2 skill edits if M1 validation exposes a gap in full-skeleton assets, review-class asset restrictions, generated-output asset presence, or behavior-preservation evidence.
