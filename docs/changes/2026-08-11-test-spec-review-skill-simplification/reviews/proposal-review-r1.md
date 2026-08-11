# Proposal Review R1: Test-Spec-Review Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent product, engineering, and delivery reviewer
Target: docs/proposals/2026-08-11-test-spec-review-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-test-spec-review-skill-simplification.md` at commit `a50b2bc6`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: TSRSIM-PR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-11-test-spec-review-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-test-spec-review-skill-simplification/review-resolution.md
- Open blockers: isolated material-finding recording and resource loading require proposal revision
- Immediate next stage: proposal revision

## Review Inputs

- Tracked proposal: `docs/proposals/2026-08-11-test-spec-review-skill-simplification.md` at commit `a50b2bc6`.
- User intent: simplify the next selected skill without weakening its approved behavior, on a new branch, then perform formal proposal review.
- Standing authority: `CONSTITUTION.md`, `VISION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/skill-contract.md`.
- Governing feature contracts: `specs/test-spec-review-gate.md`, `specs/formal-review-recording.md`, `specs/boundary-first-proof-model.md`, and `specs/progressive-boundary-first-skill-guidance.md`.
- Current implementation context: the complete canonical `skills/test-spec-review/` package and `docs/architecture/system/architecture.md`.

## Material Findings

### Finding TSRSIM-PR1

Finding ID: TSRSIM-PR1
Severity: major
Location: Recommended Direction, Loaded-resource assemblies; Formal settlement reference ownership; Structural assets
Evidence: `TSR0-isolated` and `TSR0B-isolated-boundary` load assets only when the caller requests a durable advisory record, while the proposed reference is triggered only by formal lifecycle review. The governing recording contract requires every material finding to receive durable change-local review evidence and states that isolation stops downstream handoff, not recording. An isolated review can discover a material finding after it begins, so the proposed package has neither a mandatory recording-resource trigger nor complete artifact-root procedure for that outcome.
Required outcome: Preserve formal versus isolated handoff authority while defining durable-recording applicability independently. Any isolated material finding must load the required recording procedure and assets, resolve or create the required change-local review root under existing authority, record the finding or report blocked recording, and remain isolated from downstream handoff.
Safe resolution path: Rename the conditional resource to a recording-and-settlement reference and define `durable_recording_context` as formal review, any material or blocking outcome, or an explicit durable-record request. Formal review loads it before review settlement; isolated clean advisory review does not; isolated material or blocking review loads it as soon as the trigger is known and before final output. Keep lifecycle settlement sections formal-only, but share record-root, result, finding, review-log, and resolution procedure. Add static fixtures for isolated clean, isolated material recorded, isolated material recording-blocked, formal clean, and formal material outcomes.
needs-decision rationale: none; the governing recording contract determines the required behavior and the reviewer supplied a bounded correction.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and duplicated rule ownership are concrete and measured. |
| User value | pass | Isolated ordinary review should become easier to scan without losing proof rigor. |
| Option diversity | pass | No change, inline-only, settlement-only, hybrid disclosure, fragmented resources, and executable replacement are materially distinct. |
| Decision rationale | pass with revision | O3 remains the best design, but its conditional trigger must cover mandatory isolated finding records. |
| Scope control | pass | The work remains bounded to `test-spec-review` and directly governed package and proof surfaces. |
| Trigger model | block | Formal-review context and boundary-first context do not capture the independent mandatory-recording trigger. |
| Resource ownership | concern | The reference owns recording mechanics needed outside its proposed formal-only activation condition. |
| Boundary-first ownership | pass | The proposal keeps the governed resources unchanged and gives applicability a safe evidence-based rule. |
| Semantic preservation | concern | Isolated material-finding recording would regress despite the proposed semantic ledger. |
| Testing boundary | pass | Static fixtures, deterministic package checks, and semantic review are appropriate; target-agent execution is excluded. |
| Measurement | pass | Loaded assemblies and total package size are reported separately, with percentages advisory. |
| Architecture awareness | pass | `architecture-not-required` remains plausible after the bounded package-model assessment. |
| Rollout realism | pass | Atomic canonical and derived package rollout and fail-safe resource behavior are sound. |
| Readiness for spec | block | TSRSIM-PR1 requires proposal-level closure before normative requirements are authored. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains represented, and the finding repairs a governing behavior rather than expanding the initiative.
- Scope-budget result: pass. The correction changes the trigger and ownership of the already proposed reference; it does not require another skill, runtime, or validator family.
- Vision-fit result: pass. The direction still reduces unnecessary common-path procedure while retaining durable evidence and explicit authority.

## Recommended Proposal Edits

- Recommended edits: add `durable_recording_context` as a third independent predicate; rename and broaden the conditional reference to recording-and-settlement procedure; define pre-review formal loading and post-finding isolated loading; make result and finding assets mandatory for isolated material or blocking outcomes; and keep lifecycle settlement and implementation handoff formal-only.

## Recommendation

- Recommendation: changes requested. Retain the compact universal skill, exact boundary-first trigger, existing structural assets, preservation ledgers, deterministic package proof, and no-runtime testing boundary. Revise the recording trigger and resource ownership to resolve TSRSIM-PR1, then run an independent proposal-review rerun.
- No automatic downstream handoff follows this review.
