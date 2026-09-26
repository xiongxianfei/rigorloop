# Requirement Analysis method

Use this method to turn an initial need into a clear IR, verifiable system obligations, and allocated obligations.
The [requirement model](../models/requirements.md) owns hierarchy and relationship rules.
The method is independent of any skill, command, file format, or workflow host.
Apply all seven [5W2H](5w2h.md) questions at each requirement level, recording an answer, explicit unknown, or justified non-applicability for each.

## Analyze the initial need

Apply [5W2H](5w2h.md) to every IR.
Use existing project intent and stakeholder evidence as inputs, while distinguishing needs from current implementation choices.
Record material unknowns and avoid manufacturing thresholds, stakeholders, or approval.

The IR statement expresses who needs what outcome and why it matters, with relevant scope and conditions.
The analysis supports that statement; What explains the problem and desired outcome, while the other questions establish its basis and context.
Keep provisional assumptions distinct from established constraints, and retain unresolved questions from any part of the analysis.

## Name the initial requirement

An IR name must identify a concrete need or desired outcome and the subject it concerns.
Prefer a short outcome phrase that a reader can understand without opening the full record.
An action and its object often make that meaning clear; a precise noun phrase is acceptable when equally clear.
Add a distinguishing condition or context when the outcome and subject alone could be confused with another need.
For example, "Preserve engineering knowledge across sessions" names the outcome, subject, and relevant context.

| Too vague or prematurely technical | Clearer need-oriented name |
| --- | --- |
| Durability | Preserve engineering knowledge across sessions |
| Traceability | Trace engineering obligations and responsibilities |
| Change management | Control engineering changes and recover prior states |
| Verification | Assess engineering claims using applicable evidence |
| Use Git | Recover retained engineering baselines |

These are naming examples, not additional requirements.
Do not substitute a named Feature, Module, tool, delivery task, or implementation solution for the stakeholder need.
A genuine mandated technology constraint can appear when its source and necessity are established.

Review the name using three questions:

1. Can the reader identify the subject and intended outcome?
2. Does the name distinguish this need from neighboring IRs?
3. Does it match the statement without promising broader scope or prescribing an unsupported solution?

Renaming an IR preserves its stable identity.
Refining a title does not silently change the obligation, approve the IR, or renew verification evidence.
Recheck the title against its statement and 5W2H analysis whenever either changes.

Names in the engineering model remain distinct from physical storage labels.
[Operational Support](../models/operational-support.md#naming-and-location) defines how a project represents names and updates locations.
The analysis method does not prescribe a directory structure or require an extra abbreviation of the title.

## Derive system requirements

Translate each initial need into independently assessable system obligations.
State the required outcome and the relevant conditions, then describe observable acceptance criteria.
Apply 5W2H to each SR's system obligation, using the parent IR as context and answering at the system level.
Resolve or explicitly retain gaps in actors, scope, timing, quality, and quantities.

Derive each SR under exactly one parent IR.
References to related concerns do not establish another parent.
Separate behavior from rationale and distinguish a required constraint from an implementation possibility.
Use implementation-independent language unless the implementation itself is required.

An acceptance criterion describes what an assessment should observe.
It does not claim that verification has occurred or that the requirement is satisfied.
Give each SR a name that identifies its specific obligation; a clear outcome phrase or precise noun phrase is appropriate.

## Derive allocated requirements

Develop ARs when architectural responsibilities are understood sufficiently to make the allocation meaningful.
For each AR, state the lower-level obligation, retain exactly one parent SR, and identify responsible architecture.
Apply 5W2H to that allocated obligation, including its responsible parties, operating conditions, boundaries, and limits.
Check it against the Functions, state, policies, and Interfaces assigned to that responsibility.

Do not create an AR merely to fill a tree level or invent a Module to finish a worksheet.
An allocation change can require requirement refinement; preserve the historical meaning of previous states.
Give each AR a name that makes its allocated obligation understandable within the architectural context.

## Reconcile and review

Read the name, statement, analysis, acceptance criteria, and source basis together.
Resolve disagreement between them or leave the unsettled point explicit in the draft.
When using existing contracts, preserve their identities and distinguish related source material from an actual obligation transfer.

The output is a requirement draft with explicit analysis and assessment intent.
Approval, implementation, and satisfaction remain separate decisions and observations.
