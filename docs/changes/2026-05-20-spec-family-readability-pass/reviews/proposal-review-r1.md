# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-20-spec-family-readability-pass.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-20-spec-family-readability-pass.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Predecessor proposal: `docs/proposals/2026-05-20-test-spec-contract-normalization.md`
- Canonical skills: `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/test-spec/SKILL.md`

## Findings

### SFRP-PR1 - Dependency baseline needs durable proof, not only PR status

Finding ID: SFRP-PR1
Severity: major
Evidence: The proposal says PR #77 merged to `main` before this branch was created, but implementation still waits for explicit confirmation that the normalized `test-spec` baseline is present.
Required outcome: Add a baseline confirmation checklist that the plan must complete before any readability edits.
Safe resolution: Add a normalized baseline gate covering front matter, Workflow role, surfaced stop conditions, output skeleton, and behavior-preservation evidence.

### SFRP-PR2 - Section-ordering alignment needs a safe boundary

Finding ID: SFRP-PR2
Severity: major
Evidence: The proposal says the three skills should share consistent section ordering, but also says behavior must not change. It leaves the exact shared section order open and suggests strict alignment may be best effort where it risks behavior parity.
Required outcome: Define what may be reordered and what must remain early or behavior-preserved.
Safe resolution: Add a section-ordering boundary stating that family ordering is not a behavior override and that stop conditions, must-not-claim boundaries, and validation obligations stay visible before the normal output procedure.

### SFRP-PR3 - Enum fencing needs an authoritative enum map to prevent duplication

Finding ID: SFRP-PR3
Severity: major
Evidence: The proposal says remaining closed enums should be fenced so values appear once in one authoritative block. It also says some enums are already fenced in skeletons while others are narrated in prose.
Required outcome: Require an enum authority map for all three skills.
Safe resolution: Add an enum authority map requiring each changed skill to identify enum source, authoritative destination, exact values, and duplicate-handling rule.

### SFRP-PR4 - Behavior-parity oracle is too subjective as written

Finding ID: SFRP-PR4
Severity: major
Evidence: The proposal says behavior parity will be verified by running each skill against a representative input and comparing verdict, structure, and coverage. It also says implementation proof should include per-skill preservation matrices.
Required outcome: Make the preservation matrix mandatory and define what it must contain.
Safe resolution: Add a content-preservation proof requiring every moved, tabulated, fenced, or reordered content block to map from source location to destination location with preservation proof.

### SFRP-PR5 - Produced-artifact readability should be classified as deferred, not left open

Finding ID: SFRP-PR5
Severity: moderate
Evidence: The proposal classifies produced-artifact readability as an open question and says none of the open questions block proposal review.
Required outcome: Change produced-artifact readability from `open question` to `deferred follow-up`, or block planning until the owner decides.
Safe resolution: Revise the initial intent table and scope text so produced-artifact readability is explicitly out of scope and deferred to a separate proposal.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal clearly targets spec-family skill readability after `test-spec` normalization. |
| User value | pass | Tables, fenced enums, and family ordering improve cold-read usability for adopters. |
| Option diversity | pass | The options are appropriate for this decision. |
| Decision rationale | pass | A coordinated family pass is justified by the consistency goal. |
| Scope control | revise | Produced-artifact readability and section-ordering need sharper boundaries. |
| Architecture awareness | pass | The proposal avoids packaging, build changes, routing changes, and retroactive archives. |
| Testability | revise | Needs stronger preservation-matrix and enum-authority requirements. |
| Risk honesty | pass | The proposal names enum drift, tabulation rewording, section-order context risk, and dependency risk. |
| Rollout realism | revise | Dependency baseline gate should be explicit. |
| Readiness for plan | changes-requested | Add the five guardrails before planning. |

## Recommended next stage

Revise the proposal to resolve SFRP-PR1, SFRP-PR2, SFRP-PR3, SFRP-PR4, and SFRP-PR5, then rerun proposal-review before downstream plan reliance.
