# Spec Review R1 - Plan Index Lifecycle Ownership Archive Contract

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/plan-index-lifecycle-ownership.md
Reviewed artifact: specs/plan-index-lifecycle-ownership.md
Review date: 2026-05-22
Status: changes-requested
Recording status: recorded

## Review inputs

- Spec: `specs/plan-index-lifecycle-ownership.md`
- Accepted proposal: `docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Proposal review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/proposal-review-r1.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`
- Workflow guide: `docs/workflows.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: BPIX-SR1, BPIX-SR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md`
- Review resolution: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`
- Open blockers: BPIX-SR1, BPIX-SR2
- Immediate next stage: spec revision

## Findings

### BPIX-SR1 - Terminal lifecycle detection is required but not defined

Finding ID: BPIX-SR1
Severity: major
Location: `specs/plan-index-lifecycle-ownership.md:167-175`
Evidence: R15 says validation checks terminal-plan conservation when `docs/plan.md` or `docs/plan-archive.md` changes, and R15a defines the set as every plan file under `docs/plans/` "whose plan body has terminal lifecycle state." The spec does not define what validator-visible field, heading, status line, or allowed wording establishes that a plan body has terminal lifecycle state. Existing plan bodies are prose-heavy, so downstream tests and implementation would have to infer terminal state from unspecified text.
Required outcome: Define the deterministic source of terminal lifecycle state for plan bodies before validators or test specs rely on terminal-plan conservation.
Safe resolution path: Add requirements that identify one validator-owned terminal-state source, such as a normalized plan-body status field or a narrowly defined set of accepted lifecycle status lines. Specify unknown, missing, contradictory, and legacy prose behavior. Then update examples, edge cases, and acceptance criteria so tests can prove terminal detection without broad prose guessing.

### BPIX-SR2 - Active supersession context is subjective but controls archive placement

Finding ID: BPIX-SR2
Severity: major
Location: `specs/plan-index-lifecycle-ownership.md:29-31`, `specs/plan-index-lifecycle-ownership.md:99`, `specs/plan-index-lifecycle-ownership.md:179-181`
Evidence: The glossary defines `active supersession context` as a "currently useful replacement pointer," R3a allows nonterminal entries in active `Superseded` context, and R17 requires terminal superseded history to move to the archive when it "no longer provides active supersession context." The spec does not define who decides usefulness, how the decision is recorded, or what structural signal separates active supersession context from terminal superseded history.
Required outcome: Make superseded archive placement testable and reviewable without relying on unstated judgment.
Safe resolution path: Define a structural rule or required rationale for superseded entries. For example, require `docs/plan.md` Superseded entries to include an active replacement link plus an explicit active-context marker or short rationale, and require entries without that marker to be archived. Alternatively, make superseded archive placement a manual code-review-owned semantic judgment and remove validator-implied enforcement for that boundary.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | BPIX-SR1 and BPIX-SR2 leave two required archive decisions underspecified. |
| normative language | concern | Most `MUST` requirements are concrete, but R15a and R17 use undefined detection and judgment criteria. |
| completeness | concern | Normal archive flow is covered, but terminal-state source and superseded active-context boundary are missing. |
| testability | block | Terminal-plan conservation and terminal superseded archival cannot be tested reliably without guessing. |
| examples | concern | Examples E7 and E9 cover desired outcomes but not the detection criteria needed to prove them. |
| compatibility | pass | The spec preserves plan bodies, lifecycle semantics, rollback, and old terminal history. |
| observability | concern | Validation output is specified, but the validator's source of truth for terminal state is not. |
| security/privacy | pass | The archive remains tracked repository state and forbids secrets, private local paths, credentials, and host-only state. |
| non-goals | pass | Non-goals prevent plan-file replacement, milestone/PR semantic changes, generated registry work, and broad CI automation. |
| acceptance criteria | concern | Acceptance criteria name exact terminal conservation outcomes but need terminal-state and supersession-boundary criteria to be executable. |

## Eventual test-spec readiness

conditionally-ready

The spec is close enough to shape the test-spec surface, but BPIX-SR1 and BPIX-SR2 should be resolved before test-spec approval or implementation because they define what the validator must detect.

## Stop condition

Do not proceed to architecture, plan, test-spec approval, or implementation until BPIX-SR1 and BPIX-SR2 are resolved or explicitly deferred by an authorized owner with a reduced validation contract.

## Scope preservation review

Pass.

The spec preserves the accepted proposal direction: bounded `docs/plan.md`, `docs/plan-archive.md`, recent Done cap, structural common-read budget, terminal-plan conservation, migration proof, newest-first ordering, terminal superseded archival, validation responsibility, and no lifecycle-state semantic changes.

## Recommendation

Revise the spec before downstream reliance. This review is isolated and does not automatically hand off to spec revision, test-spec, plan, or implementation.
