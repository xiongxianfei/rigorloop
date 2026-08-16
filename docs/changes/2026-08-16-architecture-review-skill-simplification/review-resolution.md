# Review Resolution: Architecture Review Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required before specification

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `ARRSIM-PR1` | accepted | open | Preserve the exact shared inline recording block and give stage-specific recording procedure one owner. |
| `ARRSIM-PR2` | accepted | open | Define every valid mode combination, write boundary, and handoff result. |
| `ARRSIM-PR3` | accepted | open | Make rationale and gap surfaces record-only and close artifact settlement authority and retry. |

## Finding details

### proposal-review-r1

#### ARRSIM-PR1

Finding ID: ARRSIM-PR1
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Reconcile the new recording reference with the normative shared inline recording subsection.
Chosen action: Preserve the byte-identical shared block inline and move only architecture-review-specific recording and settlement procedure.
Rationale: The formal-review recording spec and static validation make the shared subsection a cross-skill literal contract.
Required outcome: Classify the shared block explicitly, preserve it unless all governing consumers change atomically, and define one owner for stage-specific procedure.
Safe resolution path: Add compatibility wording, acceptance criteria, literal-ledger treatment, and exact validation before rereview.
Validation target: revised ownership, compatibility, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### ARRSIM-PR2

Finding ID: ARRSIM-PR2
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close every recording, settlement, and automation mode combination and its side effects.
Chosen action: Add an exhaustive valid-combination and write/handoff matrix and reject every unlisted combination.
Rationale: Independent closed vocabularies do not define which combinations are legal or what authority each grants.
Required outcome: Define valid pairs or triples, permitted review evidence, lifecycle writes, automation evidence, and continuation behavior.
Safe resolution path: Keep loading profiles independent and use one explicit authority matrix in the proposal.
Validation target: revised modes, loaded profiles, scenarios, stops, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### ARRSIM-PR3

Finding ID: ARRSIM-PR3
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Remove implicit rationale settlement authority and close exact architecture and ADR settlement semantics.
Chosen action: Make no-impact and proposal/spec-gap review evidence-only, restrict settlement to exact existing artifact entries, and define deterministic state authority and interrupted retry.
Rationale: The current exception has no approved artifact kind or owner, and future specification must not invent one.
Required outcome: Define non-settling surfaces, per-kind state mapping, exact intended ADR state source, partial physical retry, and downstream eligibility.
Safe resolution path: Reuse current artifact entries, authoring evidence, lifecycle states, and workflow routing without a new schema or target.
Validation target: revised target identity, settlement matrix, architecture impact, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.
