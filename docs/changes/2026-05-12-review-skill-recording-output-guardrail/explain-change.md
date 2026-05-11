# Review Skill Recording and Status Output Guardrail Change Explanation

## Summary

This change makes formal lifecycle review output explicit about three separate states:

- the review verdict;
- review-recording status;
- artifact-status sync status.

It applies to `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

## Why this changed

The accepted proposal identified a recurring execution failure: formal review skills could report material findings without creating required durable review artifacts or reporting a concrete blocker. A related learn session showed that approving or clean review results could leave the reviewed artifact's lifecycle status stale.

The approved spec amendment in `specs/formal-review-recording.md` defines the contract in `R24`-`R33a`:

- review verdict, recording status, and status sync are separate;
- material findings require complete durable recording;
- clean or approving reviews update the reviewed artifact's owned status surface when clear and edits are allowed, otherwise they report `Status sync: blocked`;
- generated skill and adapter output must be refreshed after canonical skill changes.

## What changed

Milestone M1 added recording-status output guidance to all five formal review skills and static validator coverage for:

- `Recording status`;
- `Recording blocker`;
- complete material-finding shape;
- change ID selection;
- required review artifact paths.

Milestone M2 added status-sync output guidance to the same five skills and static validator coverage for:

- `Status sync`;
- `Status artifact`;
- `Status sync blocker`;
- no-edit and ambiguous-target blockers;
- per-skill status-sync targets.

Milestone M3 regenerated the local Codex skill mirror and public adapter output from the canonical skills:

- `.codex/skills/**`;
- `dist/adapters/claude/**`;
- `dist/adapters/codex/**`;
- `dist/adapters/opencode/**`.

## Why the shape is intentionally static

The approved test spec keeps this slice structural/static. It does not add semantic review-output parsing or runtime enforcement. The first slice improves the skill output contract and validator coverage; a later proposal is required if a future recurrence proves runtime/output validation is needed.

## Safety boundaries

The implementation preserves these boundaries:

- clean reviews with no material findings remain lightweight;
- material findings still require change-local review files and `review-resolution.md`;
- no-material detailed records do not require an empty `review-resolution.md`;
- status sync is not downstream workflow continuation;
- explicit no-edit instructions block status sync;
- `code-review` uses active plan or review-owned milestone state and does not edit source files solely to record review status;
- generated output was produced by repository scripts, not hand-edited.

## Validation evidence

The active plan and `change.yaml` record the validation commands run for each milestone. M3 specifically refreshed generated outputs and passed the required generated-output and adapter checks:

- `python scripts/test-skill-validator.py`;
- `python scripts/validate-skills.py`;
- `python scripts/build-skills.py --check`;
- `python scripts/build-adapters.py --version 0.1.1 --check`;
- `python scripts/validate-adapters.py --version 0.1.1`.

Final closeout validation remains owned by the downstream `code-review`, `verify`, and `pr` stages.
