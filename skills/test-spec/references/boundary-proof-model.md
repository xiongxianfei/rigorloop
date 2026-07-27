# Boundary-first proof model

Use this reference when a change creates or reviews a contract, proof map, or
workflow handoff. Examples illustrate the contract; they never define its
complete boundary.

## Boundary record

Record `Boundary model version: v1` and the governed requirement range.
Serialize the record with these exact headings and columns:

```md
Boundary model version: v1
Boundary model scope: <governed requirement range>

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
```

When feature-specific dimensions are required, replace the exact
`Extensions: none.` line with:

```md
Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
```

When no interaction is selected, replace the interaction table with an
explicit none-selected rationale.
For a selected interaction, `Rationale` is exactly one of:
`state-coupling`, `trust-or-authority`, `mutation-or-recovery`,
`compatibility-or-migration`, `composed-path`, or `incident-evidence`.

The `## Boundary model`, `Extensions:`, `## Examples`, and `## Interactions`
surfaces form one contiguous boundary record in exactly that order. Do not
interleave another section or relocate examples outside that record.

Classify every core dimension exactly once:

| Dimension | Question |
| --- | --- |
| canonical-trust | Which source is authoritative, and what fails on conflict? |
| identity-freshness | Which identity binds evidence, and when does it become stale? |
| closed-vocabulary | Which values are accepted, and how do unknown values fail? |
| state-transition | What are the legal states and transitions? |
| authorization-scope | Who may authorize each action, against which basis and scope? |
| mutation-atomicity | What is the commit point, and what partial state is forbidden? |
| interruption-recovery | How is prepared or interrupted work reconciled without repetition? |
| concurrency-idempotency | What prevents duplicate, conflicting, or replayed work? |
| composition-bypass | Which direct, helper, public, sibling, and retry paths need independent proof? |
| compatibility-migration | How are old representations read, migrated, rejected, or retired? |
| outcome-stop | Which result continues, pauses, blocks, or fails closed? |
| evidence-claims | Which current evidence supports each claim, and what must not be inferred? |

Each row records one stable dimension ID, `applicable` or `not-applicable`,
governing requirement IDs, boundary IDs, and a rationale only when
not applicable. Add extensions only for feature-specific dimensions not
represented by the core. Use exactly `Extensions: none.` when there are no
extensions. Otherwise use exactly `Extensions:` followed by the seven-column
extension table shown above.

Every authored boundary, extension, example, interaction, proof-obligation,
regression, discovery-gap, and manual-procedure ID must match
`^[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+$`; uppercase and undotted IDs are
invalid. Test-case IDs may instead use the repository's uppercase numeric
grammar such as `T1`. In table cells with no
IDs or no applicable value, write the literal ASCII `-` sentinel. Do not use
an em dash, another Unicode dash, or a blank cell.
Extension IDs have the narrower required grammar
`^x\.[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+$`.

Apply these closed serialization rules:

- list every core dimension exactly once;
- for `applicable`, provide nonempty requirement and boundary IDs and use `-`
  for the non-applicability rationale;
- for `not-applicable`, use `-` for requirement and boundary IDs and provide a
  nonempty rationale;
- define each boundary ID in exactly one core or extension row;
- give each example a unique ID, cite only defined boundaries, keep its
  requirement IDs within the union owned by those boundaries, and overlap the
  owner requirements of every cited boundary;
- use `illustration` with requirement and boundary IDs and no regression or
  discovery ID; use `regression` with those links plus one regression ID;
- either provide an interaction table with unique IDs, at least two defined
  boundary IDs, a closed rationale, and governing requirements, or state
  explicitly that no interaction is selected; and
- in the proof map, use unique proof IDs, cite only approved requirements and
  exact boundary or interaction IDs defined by the governing feature's
  boundary record, never invent or rename an ID, cover every applicable
  boundary and selected interaction, provide at least one test-case ID per
  row, use no manual procedure for `automated`, and require one for `manual`
  or `hybrid`.

Classify every example as `illustration`, `regression`, `discovery`, or
`non-normative`. Illustrations and regressions link to governing requirements
and boundary IDs. Discovery examples expose an explicit contract gap.
Non-normative examples state their limited purpose.

Select interactions from actual hazards: stale authority, partial retry,
helper/public bypass, sibling drift, or another requirement-owned cross-boundary
risk. Select an interaction whenever correctness depends on two or more
boundaries composing; this includes classification at one boundary determining
the success, failure, or stop outcome at another. Record the involved boundary
IDs and rationale. Do not generate a full Cartesian product.

## Proof record

Map every applicable boundary and selected interaction to a stable proof
obligation. Each obligation records governing requirements, boundary or
interaction IDs, test IDs, automation level, and any exact manual procedure.
Serialize it with these exact headings and columns:

```md
Boundary model version: v1
Boundary model scope: <governed requirement range>

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |

## Test cases

<stable test case records>
```

Proof partitions must include valid, invalid, missing, additional, stale,
substituted, unknown, and conflicting states when the boundary admits them.
Stateful behavior includes legal and illegal transitions. Mutation behavior
includes commit, partial, retry, reconciliation, conflict, and replay paths.
Composed behavior proves the public path and every material sibling path, not
only a helper.

The feature boundary record owns boundary and interaction definitions. A test
spec consumes those exact IDs; it does not define, rename, infer, or repair
them. Before returning a proof map, audit every boundary or interaction
reference for exact membership in the governing feature record. If a needed ID
is absent, stop for feature-spec correction instead of coining a replacement.

Structural validation checks closed shape and references. Semantic review
decides applicability, requirement ownership, interaction selection, evidence
adequacy, and whether a boundary is missing. Neither examples nor validators
may invent normative behavior.

## Stop rules

Stop and record a finding when:

- a core dimension is absent, duplicated, or uses an unknown value;
- `not-applicable` lacks a defensible rationale;
- an example is the only owner of behavior;
- an applicable boundary or selected interaction lacks direct proof;
- a helper test substitutes for a public or sibling path;
- evidence is missing, stale, caller-asserted, circular, or broader than its
  claim; or
- a discovered boundary requires a new owner decision.
