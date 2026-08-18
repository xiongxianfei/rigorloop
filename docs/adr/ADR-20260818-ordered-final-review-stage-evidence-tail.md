# ADR-20260818: Ordered Final-Review Stage-Evidence Tail

## Owning change record

`docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml`

## Context

RigorLoop requires final holistic code review before `explain-change` and requires durable formal review evidence. The earlier explain-change simplification contract allowed only one explanation-only direct-child commit after the reviewed subject. That model could not represent ordinary repository operation: committing final-review evidence and then the explanation required two revisions, combining them violated the explanation-only rule, and leaving review evidence uncommitted violated repository-backed identity and clean-worktree checks.

The solution must preserve four constraints:

- the final reviewed product diff remains fixed at the exact reviewed subject;
- every formal review and explanation remains durably recorded;
- review, explain-change, workflow, and verify retain their existing write authority; and
- implementation or decision-bearing drift after final review must fail closed.

## Decision

Use one ordered, Git-derived pre-verify stage-evidence tail:

```text
S: reviewed subject
-> R: final-review recording and matching workflow transition
-> E: explanation recording and matching workflow handback
-> verify
```

`S`, `R`, and `E` are non-merge commits with direct-child ancestry. `E` is the handoff revision. The final reviewed diff remains base-to-`S`; neither evidence commit redefines the reviewed implementation subject.

Git derives the recording identities after the commits exist. The explanation records its content identity, reviewed basis, final-review identity, and validation cutoff, but never embeds its own commit hash.

Revision `R` may contain only the exact final-review record, review invocation, review log, conditional review-resolution update, and workflow-owned fields required for that review transition. Revision `E` may contain only the exact explanation artifact and workflow-owned fields required for handback. Shared files such as `change.yaml` are validated by changed field as well as changed path. A path allowlist cannot authorize unrelated lifecycle mutation.

The ordered commits compose existing owners; they do not create a joint writer. The review peer writes review evidence and matching settlement, `explain-change` writes its artifact, and workflow writes routing and handback state.

The only resumable partial tail is exact `S -> R`. When its basis and identities remain current and no intervening change exists, retry may create only direct-child `E`. Broader paths or fields, merge commits, reversed ordering, additional or intervening pre-verify commits, changed governing identities, or recorded/Git identity mismatch make final-review reuse stale and require a fresh final holistic review.

Verify consumes the reviewed subject plus the exact closed tail. Verify evidence written after `E` does not retroactively become part of the pre-verify tail and does not by itself stale the explanation.

## Alternatives considered

### One combined review-and-explanation commit

Rejected because explain-change logically and contractually follows the final-review result, and combining both stages weakens review occurrence identity and recovery.

### One explanation-only commit after an uncommitted review

Rejected because formal review evidence must be durable and repository-backed before settlement or downstream reliance.

### Arbitrary lifecycle-evidence commits after final review

Rejected because a broad path allowlist can hide implementation drift, unrelated lifecycle mutation, reordered stages, or stale evidence reuse.

### Git notes or a new transaction artifact

Rejected because they introduce another persistence or portability boundary when tracked review evidence, the explanation artifact, `change.yaml`, and Git ancestry already provide the required surfaces.

## Consequences

- Final review, explain-change, workflow, and verify can complete in their required order without self-staleness.
- Code-state resolution must represent four revision roles and validate exact ancestry, changed paths, and changed fields.
- Shared lifecycle files need semantic diff validation for the two evidence commits.
- A real temporary-repository scenario must prove the complete `S -> R -> E -> verify` sequence; isolated ancestry and path fixtures are insufficient.
- Conservative final-review replay remains the recovery for every unknown or broader tail.
- No service, database, external system, new lifecycle state, new write owner, or self-referential commit field is introduced.

## Follow-up

- Architecture-review this ADR and the canonical runtime, cross-cutting, quality, and risk updates.
- Revise the execution plan and test specification for the four-part identity model, field-level validation, partial-tail retry, and end-to-end Git proof.
- Update workflow code-state resolution, automation integration, fixtures, and published explain-change guidance only after architecture approval.
