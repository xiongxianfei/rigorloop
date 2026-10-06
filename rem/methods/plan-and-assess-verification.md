# Plan and assess verification

## Purpose and basis

Determine whether an identified subject satisfies specified obligations and acceptance criteria.
The [assurance concepts](../concepts/assurance.md) distinguish a verification definition, actual Evidence and Judgment; the [assurance model](../models/README.md#assurance) owns their relationship.
[NASA Product Verification](../sources/S04.md) supports this assessment purpose and the choice of test, analysis, inspection or demonstration; REM owns the procedure and its application to REM requirements.

## Inputs

Use the applicable requirement and criterion versions, subject and configuration, relevant design/Interface assumptions, available evidence and the project's assessment authority.
Identify dependencies and missing inputs before claiming an executable plan.
For integrated obligations, include interactions and composition assumptions that individual component checks cannot establish.

## Procedure

1. State the claim, requirement criteria and exact subject state to be assessed.
2. Select techniques appropriate to the claim: test, analysis, inspection, demonstration, review or measurement. Define conditions, inputs, expected observations, tools and invalid-run or stopping conditions.
3. Identify coverage of success, relevant failure and boundary cases. Allocate integrated observations where local checks cannot establish the obligation.
4. Record the plan as unexecuted until it is performed. A test file, linked check or planned review is not evidence of success.
5. Execute within the applicable authority and environment. Retain actual subject/configuration identity, procedure, observations, anomalies and conditions affecting interpretation. If execution is unavailable, leave the claim unassessed.
6. Compare observations with each in-scope criterion. State supported, unsupported or inconclusive conclusions with their scope, reasoning, assessor and limitations; do not hide failed or missing criteria behind a broader passing label.
7. Reuse earlier evidence only after checking applicability to the current subject, criteria and conditions. A stable entity ID or unchanged timestamp alone is insufficient.
8. Return deficiencies to the requirement, design, implementation or assessment owner. Reassess affected support after correction; preserve the original meaning of earlier results.

## Outputs and completion

Produce the verification definition, attributable observations when executed, criterion coverage, discrepancies and a scoped judgment.
Keep waiver or risk-acceptance decisions distinguishable from evidence that a criterion passed.
Use the project's [Operational Support](../models/operational-support.md#engineering-knowledge-and-operational-records) to represent and retain the account; this method prescribes no file format, storage product or review cadence.

A verification result is complete for its declared scope when another assessor can identify what was assessed, under which conditions, what happened, what remains unsupported and why the conclusion follows.
This does not establish [intended-use success](validate-stakeholder-outcomes.md) or authorize release, baseline approval or workflow closeout.

## Example and limits

An offline export check may verify that required relationships remain available without a network connection.
It does not demonstrate that an engineer can understand responsibility from the exported presentation.
See the [worked assessment plans](../practices/engineer-change/WORKED-EXAMPLE.md#assessment-plans) for that distinction.
An unrun check or evidence from a different export version must leave the affected claim unestablished.
