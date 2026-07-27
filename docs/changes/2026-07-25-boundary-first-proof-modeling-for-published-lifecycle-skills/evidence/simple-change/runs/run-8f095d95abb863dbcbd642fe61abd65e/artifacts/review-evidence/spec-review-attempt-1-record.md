# Portable text normalizer spec review

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: finding.unicode-whitespace.definition
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/spec-review.md
- Review log: review-log/spec-review.md
- Review resolution: review-resolution/spec-review.md
- Open blockers: finding.unicode-whitespace.definition
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: R2 does not identify an exact Unicode whitespace classification, so portable implementations and exhaustive tests could disagree.

Review ID: spec-review-r1
Stage: spec-review
Status: changes-requested
Reviewed artifact identity: sha256:bf987984b96748b14aa60fb94eab0673ebda843a570a3f66eb277cb5290d3700
Material findings: finding.unicode-whitespace.definition
Recording status: recorded

## Boundary-first review

Boundary model version: v1
Boundary model scope: R1-R4

The boundary record has all twelve core dimensions exactly once, a valid feature-specific extension, requirement-owned examples, and explicit interactions. Boundary IDs, example IDs, and interaction IDs satisfy the required grammar and reference ownership rules. The material issue is the semantic precision of `boundary.text.output`, not its serialization.

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | concern |
| normative language | pass |
| completeness | concern |
| testability | concern |
| examples | pass |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Findings

## Finding finding.unicode-whitespace.definition

- Finding ID: finding.unicode-whitespace.definition
- Severity: major
- Location: Glossary; R2; criterion.trim.output; boundary.text.output
- Evidence: `Unicode whitespace` is defined only as characters “classified as whitespace by the Unicode standard.” The specification does not identify the exact Unicode property or classification meant by that phrase. Different portable implementations can therefore select different character sets while claiming compliance, and tests cannot derive one exhaustive expected boundary set.
- Required outcome: Define the exact Unicode whitespace classification governing R2 so implementations and tests derive the same leading and trailing character set, without adding behavior outside R1-R4.
- Safe resolution path: Revise the glossary to name the intended Unicode classification precisely, then align the R2 acceptance criterion with that term and submit the same specification for a new spec-review round.
- needs-decision rationale: The specification owner must choose the intended Unicode classification; the reviewer cannot infer it without creating normative behavior.

Suggested wording after owner confirmation: `Unicode whitespace: characters having the Unicode White_Space property.` If Unicode-version handling is intentionally left to the execution environment, state that explicitly only with owner authorization.

No automatic downstream handoff is authorized. The finding is recorded before revision and requires an owner decision followed by same-stage re-review.