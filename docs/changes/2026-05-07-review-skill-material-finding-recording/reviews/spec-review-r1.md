# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Maintainer spec-review
Target: specs/formal-review-recording.md; specs/review-finding-resolution-contract.md; specs/rigorloop-workflow.md
Status: changes-requested

## Scope

Reviewed the drafted spec amendments for review skill material-finding recording, including the formal review recording contract, review finding resolution contract, and top-level workflow alignment.

## Findings

### SR1: Isolated material-finding trigger conflicts with detailed-record trigger

Finding ID: SR1

Evidence: `specs/formal-review-recording.md` requires a detailed review file when a formal lifecycle review produces material findings, but later says an isolated or review-only review with no tracked change proceeding may omit a detailed review file unless durable capture is requested.

Required outcome: Make the relationship between the general material-finding trigger and the isolated/no-tracked-change exception explicit so tests and implementation do not have to guess which rule wins.

Suggested resolution: Amend the detailed-record trigger or the isolated-review rule to state that the isolated/no-tracked-change case is an explicit exception to the general material-finding trigger. Keep the record-before-edit rule for any material finding that will drive tracked artifact edits.

## Recommendation

Request changes before approving the spec amendments. This finding is material because it affects when isolated material review findings create durable records and therefore changes downstream test and skill behavior.
