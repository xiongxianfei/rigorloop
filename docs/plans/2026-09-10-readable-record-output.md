# Readable record output

<!-- Template: plan-skeleton-v3 -->

<!-- Skill: plan -->

<!-- Template status: normative -->

<!-- Structural-fingerprint: sha256:41e5a53fc9626de70a61c8506ea7fd8b4de125eb1c1d35e0d65831f0c7cbff35 -->

## Purpose / big picture

Deliver readable primary text and indented stored JSON without changing recorded meaning, compact machine responses or storage safety. The existing local candidate must satisfy the independently assessed contract, delivery allocation and final review before verification; this plan does not claim its gates preceded that candidate's authorship.

## Current Handoff Summary

- Owning change record: [2026-09-10-readable-record-output](../changes/2026-09-10-readable-record-output/change.json)

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Readable record output](../proposals/2026-09-10-readable-record-output.md).
- Spec: [CLI](../design/cli/cli.md), with retained [Record Format](../design/record-format/record-format.md) and [Workflow](../design/workflow/workflow.md) interactions.
- Architecture: the owning CLI model; no additional architecture change.
- Prior-contract test spec: none independently applicable; this plan allocates current-model proof.

## Context and orientation

`recording-result.js` renders primary responses. `recording-construction.js` constructs new record files; `recording-spans.js` edits exact existing token spans. All continue through the existing recorder's validation, identity and recovery boundary. The CLI package already supplies the YAML formatter. The package README documents the output choices. Existing public query, targeted mutation, contract and persistence tests are the protective baseline.

## Non-goals

- No Markdown report exports, stored schema migration, bulk reformatting, new dependencies or command families.
- No historical-byte rewrite, weaker byte limits, changed machine JSON or canonical identity/cursor encoding.
- No release, publication, push or PR operation.

## Requirements covered

- CLI-SR-11/14/17/21: M1/TG-01 text readability, literal-value preservation, complete selected data and byte limits.
- CLI-SR-03/13/17: M1/TG-02 new-file indentation, targeted replacement/append, deterministic order and unchanged neighbors/no-ops.
- CLI-SR-02/04/05/06/08/09/16/20: M1/TG-03 retained rejection, conflicts, recovery, preview and prepublication receipt safety.

## Milestones

### M1. Preserve readable presentation through recording

- Milestone kind: implementation.
- Engineering purpose: assess one small shared serialization change across terminal display and persisted-file editing.
- Requirements: CLI-SR-02/03/04/05/06/08/09/11/13/14/16/17/20/21.
- Architecture responsibility: CLI presentation and lossless construction; persistence and Record Format retain their existing responsibilities.
- Dependencies: exact approved Proposal, Design package and this Delivery allocation.
- Implementation scope: primary text rendering, new-file encoding, local object replacement/array append, regression proof and package guidance.
- Files/components likely touched: `packages/rigorloop/dist/lib/recording-{result,construction,spans}.js`, `packages/rigorloop/test/record-store-{queries,targeted}.test.js`, and `packages/rigorloop/README.md`.
- Required verification: TG-01 decoded paragraphs/code/Unicode/literal escapes, complete text/JSON parity and exact byte boundaries; TG-02 sorted two-space files through creation and subsequent updates, compact-file preservation and byte-identical no-ops/neighbors; TG-03 the existing contract/query/targeted/interactions/persistence/recovery suites and prepared package tests.
- Evidence expectations: failing-before/passing-after focused regressions, exact final engineering subjects, executed commands and any environment limitations.
- Implementation steps: reproduce the presentation failures; apply scoped rendering and storage encoding corrections; preserve machine/canonical encoding; run focused and integrated checks; resolve findings and obtain independent M1 assessment.
- Validation commands: V1–V4 below.
- Expected observable result: ordinary text narratives display real line breaks; new JSON files remain indented across edits; selected data and storage safety are preserved.
- Completion criteria: allocated proof passes and independent M1 review approves with required findings resolved.
- Required evidence: targeted implementation evidence and an independent milestone review with exact subjects.
- Review handoff: all M1 files, the owning CLI amendment, relevant unchanged Record Format interactions, and proof.
- Risks: formatting can exceed existing byte limits, alter unrelated bytes or corrupt intentional escapes.
- Rollback/recovery: revert scoped source changes; use existing exact-byte transaction recovery for interrupted writes. Do not reformat historical records or migrate schemas.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: final Verify; corrections return to their owner and require affected reassessment.

## Change-level verification

### TG-FINAL-01. Public output, stored bytes and prepared package agree

- Covers: M1/TG-01–03, CLI-SR-03/11/13/14/17/20/21 and package integration.
- Demonstrate: actual public commands and installed package preserve the complete data contract, escaped literal values and storage/recovery behavior. Verify the corrected contract and examples, final review, record validity and source preservation together.
- Evidence expectations: V1–V4, independent final review, exact prepared-source identity and actual candidate check results. Raw-checkout failures caused by absent generated release inputs are diagnostic evidence, never substituted for prepared-package success.
- Non-applicability: no public deployment or live release smoke; no external publication is authorized. This does not waive local full candidate checks or final review.

## Validation plan

- V1: `node --test packages/rigorloop/test/record-store-v2-contract.test.js packages/rigorloop/test/record-store-v2-persistence.test.js packages/rigorloop/test/record-store-targeted.test.js packages/rigorloop/test/record-store-queries.test.js packages/rigorloop/test/record-store-interactions.test.js packages/rigorloop/test/record-store-contract.test.js packages/rigorloop/test/record-store-cli.test.js` proves focused behavior and retained safety.
- V2: `bash scripts/ci.sh --mode pr --base "$READABILITY_BASE_REVISION" --head "$READABILITY_SOURCE_REVISION"` runs the repository-owned isolated candidate preparation/full-check path. Resolve both variables to exact commits. Construct the source snapshot from only this change's intended paths; preserve the user's real index and exclude unrelated untracked files. Retain source/prepared/candidate identities and actual results. This exercises the actual generated package inputs and candidate broad checks without publishing.
- V3: `python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/record-format/record-format.md --path docs/design/workflow/workflow.md` and `python scripts/validate-documentation-prose.py --mode enforce --path docs/design/cli/cli.md --path docs/proposals/2026-09-10-readable-record-output.md --path docs/plans/2026-09-10-readable-record-output.md --path packages/rigorloop/README.md` check model/prose structure. Independent assessment supplies semantic approval.
- V4: `node scripts/validate-record-store.mjs docs/changes/2026-09-10-readable-record-output/change.json` and `git diff --check` validate final records and patch whitespace after evidence saves.

## Risks and recovery

Indentation consumes the existing file/response budgets; rejection must remain explicit rather than truncate or weaken limits. Raw package tests require generated release inputs, so V2 must prepare the real candidate. Preserve historical judgments and their original subject identities during corrections. Revert only the scoped implementation if a defect remains; user-owned files and unrelated changes remain untouched.

## Dependencies

Current Design Review, then independent Delivery Review precede reliance on this allocation. M1 completion precedes fresh final Code Review and distinct Verify. Recording-only evidence updates require a coherence check; changed engineering subjects require affected independent reassessment and renewed proof.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-10 | Keep one implementation milestone and a distinct final-review checkpoint. | Rendering and token edits form one small serialization boundary with shared integrity checks. | Independent uncoordinated format changes; treating a milestone review as final Verify. |
| 2026-09-10 | Verify actual prepared package inputs through V2. | Current release generation belongs to the isolated candidate builder. | Hand-editing generated metadata or accepting raw-checkout failures as success. |

## Readiness

- See the owning change record for current workflow state.
