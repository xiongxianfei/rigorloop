# Integrate and commit the delivered repository cleanup

## Purpose / big picture

Stop expanding cleanup scope and turn the accumulated working-tree changes into a reviewed, verified and recoverable local commit. Preserve the remaining cleanup direction as explicit follow-up work.

## Current Handoff Summary

- Owning change record: [repository cleanup](../changes/2026-09-13-current-design-repository-cleanup/change.json).

Mutable activity, work, reviews and closeout live only in that record. This plan consolidates the delivered package; the token-cost and ledger plans retain their original execution intent.

## Source artifacts

- Direction: [cleanup proposal](../proposals/2026-09-13-current-design-repository-cleanup.md), with the user's September 14 instruction to stop adding removals and package the accumulated work.
- Design: System, Skill, Design, Workflow, Assessment, CLI and Engineering owners, including Validation, Packaging and Release. Scope is the actual delivered source transfers and retirements, not every future requirement in those models.
- Earlier allocation: [token-cost retirement](2026-09-13-token-cost-retirement.md) and [ledger retirement](2026-09-14-retirement-ledger-removal.md).
- Disposition: the change's source-disposition, source-inventory and batch evidence preserve source-qualified transfers and historical identities. Final integration evidence resolves their cumulative result against the actual Git diff.

## Context and orientation

The branch contains governance/vision simplification, living-model consolidation and legacy-document deletion, current consumer repairs, token-cost subsystem retirement and ledger retirement. Shared selector, test, model and change-record files connect these batches. The final review uses the entire diff from baseline `39b7c5cb1f03aa761d2f2493d3474ce985e59d6f`, including the previously untracked owning records. Inspect actual sources and evidence rather than treating the stale project map as architecture authority.

## Non-goals and deferred scope

No additional opportunistic cleanup. The remaining VAL-SR-23 representative spec-read-log retirement, DIST-SR-21/22 generated-only adapter support, REL-SR-25 historical replay changes and other legacy tests/fixtures or retained sources are follow-ups. Their Design direction is not delivered or adopted by this integration. No push, PR creation, merge, publication or history rewrite is part of local commit preparation. A reviewable PR title/body may be prepared locally.

## Requirements covered

- Engineering ENG-SR-13/14: current-tree cleanup, recoverable retired material and coherent consumer reconciliation.
- System/Skill/Design/Workflow/Assessment/CLI mapped source transfers: preserve current requirements and explicitly retire obsolete mechanics under each source-qualified displacement map.
- Validation VAL-SR-25: complete token-cost retirement and retained current qualification/proof.
- Validation VAL-SR-23: ledger portion only; spec-read-log remains deferred.
- Constitution: independent complete-package assessment, current evidence, safe Git retention and truthful scope.

## Milestones

### INTEGRATE-1. Reconcile and package the accumulated change

- Kind: implementation/integration.
- Purpose: establish one exact complete delivered package before any local commit.
- Dependencies: existing direction; fresh full affected Design assessment and review of this consolidation allocation before any material correction implementation.
- Scope: inventory actual added/modified/deleted paths and source transfers; reconcile current documentation, consumers and governing records; address recorded review findings and validation failures within this delivery.
- Required correction allocation: the supporting-subject selection finding uses the existing complete-set validator's same-snapshot Subject-path output, exact safe Subject membership and per-invocation reuse. Tests cover supported add/change/deletion, unknown/mixed paths, reserved unregistered records, malformed stores and dangling EntryRefs, unknown/mixed validator options, escaping links and no record/history mutation. Retain current record/metadata proof; do not add a new schema or generic path exemption.
- Proof TG-INTEGRATED: final selected validation plus broad smoke, independent final whole-change Code Review, provenance/identity checks, current-record validation and diff hygiene.
- Completion: every actual diff path is intentional; current reliance is coherent; required tests and reviews pass; deferred work is explicit; no untracked required evidence is omitted.
- Recovery: captured complete pre-integration working tree and index under `/tmp/cleanup-consolidation-backup`, plus recoverable Git source revisions. Preserve unrelated changes; do not reset the branch or fabricate intermediate historical records.

## Final review checkpoint

Kind: lifecycle-closeout. After all corrections, obtain fresh independent whole-change Code Review of the complete accumulated diff and cross-batch interactions, followed by distinct final Verify for this delivered package. Earlier scoped reviews are supporting evidence only. Final records explicitly exclude deferred cleanup.

## Change-level verification

TG-INTEGRATED covers real selector scheduling, model/source references, published skill structure, adapter/resource integrity, CLI and record safety, release qualification and historical rejection. New failures must be diagnosed, corrected under the proper owner and rerun; successful slice checks alone do not close this package.

## Validation plan

- Inspect `python scripts/select-validation.py --mode local`; run `bash scripts/ci.sh --mode local --jobs 4` for the complete selected diff.
- Include the repository's broad smoke through `bash scripts/ci.sh --mode local --broad-smoke --jobs 4`; this combined invocation satisfies the selected and broad obligations through the existing executor's canonical-check deduplication. Separate `bash scripts/ci.sh --mode broad-smoke --jobs 4` remains available if required for a correction. Keep the actual check population and failure status.
- Run current `python scripts/test-release-transaction.py` when not already included in successful full selected execution; token qualification changes are release-sensitive.
- Run `node scripts/validate-record-store.mjs docs/changes/2026-09-13-current-design-repository-cleanup/change.json` and `git diff --check` after final evidence recording.
- Inspect deleted-file references and recovery identities, generated README vision agreement, final index contents and final commit diff. A commit changes Git identity, not the already reviewed source bytes; verify those bytes after committing.

## Commit and handoff strategy

Prefer independent logical commits only when each can carry its own governing content, consumer fixes and valid records. Do not reconstruct intermediate change-record history or create commits whose governing references point to missing future files merely to split the diff. If shared dependencies prevent safe separation, create one coherent engineering/evidence checkpoint, followed only by any necessary verification/PR-handoff bookkeeping commit. Preserve the final working-tree bytes and existing historical judgments. Produce local PR material from the final diff; external actions remain separate.

## Risks and recovery

The accumulated scope can hide stale source pointers or claims of broader adoption. Use an explicit final manifest and independent complete reviews. Avoid source edits while freshness-sensitive release tests run. Record initial failures and the exact correction proof; do not weaken validation to accommodate the large diff.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | Freeze delivered scope and integrate before more removals | The accumulated shared-file and evidence changes need a reliable checkpoint. | Continuing deletions while the current package remains uncommitted. |
| 2026-09-14 | Commit boundaries follow coherent dependencies | Historical records and current source contracts cannot safely be split by pathname alone. | Manufacturing intermediate records or broken deletion-only commits. |

## Readiness

See the owning record for mutable state and final evidence for the exact delivered scope.
