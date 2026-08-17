# Proposal Review: Vision Skill Progressive Disclosure

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md`

Reviewed artifact: `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md` at commit `610765e0`
Review date: 2026-08-17
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: VISSIM-PR1, VISSIM-PR2, VISSIM-PR3
- Open blockers: the assessment profile, revision-to-README coupling, and strategic-rationale structural ownership require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, mutate the vision package, or continue the workflow

## Overall assessment

The proposal selects a strong progressive-disclosure direction. Universal authority, state classification, revision significance, canonical-path safety, privacy, stops, claims, and resource triggers remain inline. Detailed strategic authoring and README synchronization follow independent activation boundaries, and copied assets remain structural rather than normative.

The proposal also correctly preserves the active consolidated vision contract instead of reviving the superseded lowercase-path, user-facing mode, or 500-word behavior. Its semantic-rule and compatibility-literal inventories are necessary because current tests bind many exact phrases to the flat file.

Three package and invocation contracts remain incomplete. The smallest claimed profile is not currently an approved vision operation, the editorial revision profile can omit procedure that the active update contract normally requires, and the second structured artifact produced by strategic authoring has no structural owner.

## What is strong

### The conditional boundaries are genuine

Product-category judgment and README marker mechanics activate independently. Two references are more proportionate than a catch-all resource or a fragmented reference tree.

### Universal fail-closed behavior remains available

The main skill retains source precedence, intent and state classification, write authority, substantive linkage, retired-path handling, privacy, research, stops, claims, and missing-resource behavior.

### Compatibility proof is evidence-led

The proposal distinguishes semantic rules from literal consumers and requires real loaded assemblies, assets, references, and total package size to be reported separately.

### The testing boundary is proportionate

Deterministic contract scenarios, existing package validation, and ordinary lifecycle review are appropriate. A target-agent runtime or separate prose grader would add little useful proof.

## Material findings

### VISSIM-PR1 — Major: `assess-vision` and `VA0-assessment` are not grounded in the approved invocation contract

Finding ID: VISSIM-PR1
Severity: major
Location: `Recommended Direction` sections `Classify operation independently from revision significance`, operation matrix, loaded assemblies, and measurement
Evidence: The proposal introduces `assess-vision` as one of four internal operations and makes `VA0-assessment` a primary acceptance surface. The approved `specs/vision-skill.md` defines establishment, update, and README synchronization inputs and outputs, and the current published skill does not expose a separate formal assessment operation. The proposal does not identify a current caller, request envelope, result contract, or distinction between a formal assessment and an ordinary read-only question. An implementation could optimize and measure an invented no-write path while leaving every real invocation on larger assemblies.
Required outcome: Retain only evidence-backed invocation surfaces, or add a complete assessment contract justified by a current caller.
Safe resolution path: Inventory current repository-owned callers and user-facing guidance. If no current caller specifically invokes a formal vision assessment, remove `assess-vision` and `VA0`; treat ordinary questions as read-only answers outside the mutation operation model and measure the three real assemblies. If a caller exists, bind one exact subject and evidence basis, define outputs and forbidden writes, and distinguish the operation from proposal `Vision fit` review.
needs-decision rationale: none; current repository evidence can settle whether the profile exists.

### VISSIM-PR2 — Major: vision revision and README synchronization have an ambiguous activation boundary

Finding ID: VISSIM-PR2
Severity: major
Location: `Recommended Direction` operation matrix, resource ownership, and `VA2-editorial-revision`
Evidence: The active contract and current skill make README synchronization part of an authorized vision update when a valid marker block exists; missing or malformed markers stop unless insertion or skipping is explicitly authorized. The proposal says an editorial revision loads the README reference only when synchronization is “requested or required by the authorized operation,” but it never defines which condition applies by default. This permits an implementation to complete a vision edit without loading marker validation or updating the derived README, while another implementation loads the reference for every edit. It also makes the `VA2` measurement assembly non-deterministic.
Required outcome: Define one closed revision-to-README matrix and derive the loaded assembly from it.
Safe resolution path: Preserve the active default: establishment includes README synchronization and may insert markers; revision includes README synchronization through an existing valid block; explicit current skip authority omits the README write; explicit insertion authority permits insertion; invalid or ambiguous marker state stops. Therefore every establishment and every revision without a pre-resolved skip loads the README reference before marker-dependent judgment or writes. Measure revision-with-sync as the primary real profile and report an explicitly skipped variant separately when retained.
needs-decision rationale: none; the active contract already establishes the safer default.

### VISSIM-PR3 — Major: the strategic-positioning rationale has no structural owner

Finding ID: VISSIM-PR3
Severity: major
Location: package recommendation, strategic-reference ownership, asset ownership, and testing strategy
Evidence: Initial establishment and material repositioning create or update two structured artifacts: root `VISION.md` and `docs/vision/strategic-positioning.md`. The active contract requires the rationale to contain compact sections for ten named positioning fields. The proposal gives `VISION.md` one structural skeleton, but assigns the rationale only a procedural “rationale procedure” in the strategic reference. It does not say whether the reference owns exact rationale headings and order, whether they remain ad hoc prose in `SKILL.md`, or whether a second asset owns them. This leaves a required repeated output shape outside the proposal's structure-versus-policy ownership model.
Required outcome: Give the strategic-positioning rationale one explicit structural owner without moving applicability or adequacy policy into an asset.
Safe resolution path: Add `assets/strategic-positioning-skeleton.md` as a second structural asset. It should own only the ten compact headings, authority statement location, ordering, and placeholders. The strategic reference retains when the rationale is required, what each field means, conflict behavior, and adequacy. Load or copy the asset only for initial establishment, material repositioning, or an explicitly authorized full rationale rewrite; preserve narrow historical edits in place. Report both assets separately from procedural loaded-context totals.
needs-decision rationale: none; a second structural asset is the cleanest fit with the selected ownership model.

## Architecture assessment

The bounded expectation remains `architecture-not-required`. Removing an artificial profile, closing an existing README activation rule, and adding a second structural asset all fit the current packaged-skill model. Architecture becomes required only if implementation discovers a new loader, persisted operation classifier, generated-content owner, or executable synchronization mechanism.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-VISSIM-001` | Every measured procedural profile corresponds to a current supported invocation surface. |
| `AC-VISSIM-002` | A formal assessment operation is absent unless one current caller and complete read-only contract are identified. |
| `AC-VISSIM-003` | Establishment always includes the approved README synchronization behavior. |
| `AC-VISSIM-004` | Vision revision loads README procedure unless exact current skip authority was resolved before marker-dependent judgment. |
| `AC-VISSIM-005` | Missing, malformed, nested, duplicate, or ambiguous markers cannot be interpreted as an implicit skip. |
| `AC-VISSIM-006` | Revision-with-sync is represented as one deterministic primary loaded assembly. |
| `AC-VISSIM-007` | Root vision and strategic-positioning rationale have separate explicit structural owners. |
| `AC-VISSIM-008` | The strategic-positioning asset owns labels, ordering, and placeholders only. |
| `AC-VISSIM-009` | Strategic applicability and adequacy remain owned by the skill and strategic reference. |
| `AC-VISSIM-010` | Both structural assets are reported separately from procedural profile measurements. |
| `AC-VISSIM-011` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-VISSIM-012` | No target-agent runtime or separate prose-grading system is used for acceptance. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The flat common path, duplicated structural ownership, and literal placement coupling are concrete. |
| User value | pass | Real authoring and synchronization paths should load less unrelated procedure. |
| Option diversity | pass | Flat, inline, catch-all, two-reference, fragmented, and executable approaches are materially distinct. |
| Decision rationale | pass | Two independent procedural references are appropriate. |
| Vision fit | pass | The proposal preserves durable, human-reviewable vision authority. |
| Scope control | pass | Runtime, migration, project-vision revision, and unrelated skill work remain excluded. |
| Universal safety | pass | Authority, paths, privacy, stops, claims, and triggers remain inline. |
| Invocation model | block | The smallest profile is not yet grounded in an approved or observed invocation. |
| README activation | block | Revision may omit normally required synchronization and marker procedure. |
| Structural ownership | block | The required strategic rationale shape has no explicit owner. |
| Compatibility | pass with revisions | Rule and literal ledgers are sound once all output shapes and real profiles are represented. |
| Measurement | concern | `VA0` may be artificial and `VA2` currently has two possible assemblies. |
| Testing boundary | pass | Static contract and package proof are proportionate. |
| Architecture awareness | pass | Existing package architecture should suffice after the bounded assessment. |
| Readiness for spec | changes-requested | VISSIM-PR1 through VISSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; the proposal represents every user goal without expanding into project-vision revision, runtime evaluation, helper scripts, or unrelated skill changes.

## Recommended Proposal Edits

- Remove the formal assessment profile unless a current caller and complete read-only contract are demonstrated.
- Make README synchronization and explicit skip behavior deterministic for every establishment and revision path.
- Add a structural asset for the ten-field strategic-positioning rationale and update package, measurement, rollout, risk, and proof sections.
- Rerun independent proposal review against the committed revision.

## Recommendation

- Recommendation: revise the proposal to resolve VISSIM-PR1 through VISSIM-PR3, then perform a new independent proposal review. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass; initial intent and directly coupled package scope have explicit dispositions
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-log.md`
- Review resolution: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-17-vision-skill-progressive-disclosure`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
