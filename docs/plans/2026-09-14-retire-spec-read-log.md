# Retire fixed spec-read-log instrumentation

## Purpose / big picture

Complete the selected remaining VAL-SR-23 instrumentation retirement without losing substantive requirement-fidelity protection or broadening repository cleanup.

## Current Handoff Summary

- Owning change record: [spec-read-log retirement](../changes/2026-09-14-retire-spec-read-log/change.json).

Mutable activity, milestone state, reviews and closeout live only in that record.

## Source artifacts

- Proposal: [repository cleanup](../proposals/2026-09-13-current-design-repository-cleanup.md), applied to this explicitly selected follow-up.
- Spec: [Validation](../design/engineering/validation.md), VAL-SR-23 and current selection/protection rules; [Engineering](../design/engineering/engineering.md), ENG-SR-13/14.
- Architecture: existing Validation selection and execution responsibilities; no new runtime owner or interface.
- Prior-contract test spec: [requirement fidelity](../../specs/requirement-fidelity-gate.test.md), exact scoped frozen-instrumentation supersession. Remaining legacy obligations retain their declared applicability.

## Context and orientation

The checker reads a committed JSON log of claimed clause IDs, bytes and full-file flags. It does not observe real reads, aggregate repeated reads or measure clause length. Its only production fixture, catalog entry, parallel-safety qualification and selector expectations form one removable unit. Inspect actual readers rather than relying on the stale project map. Baseline is `020e4d2c76129ac89b488cf9436d0e6efb453f5a`.

## Non-goals

No replacement metric, pass receipt, historical ledger, new reader instrumentation, broader requirement-fidelity redesign, adapter support or replay retirement. Preserve historical records and public skill/CLI contracts. PR submission is authorized; merge and publication are separate.

## Requirements covered

- VAL-SR-23: remove the fixed spec-read-log subsystem and exclusive fixture together.
- VAL-SR-03/04 and ENG-SR-13/14: coherent selected checks, recoverable retired content and reconciled consumers.
- TEST-SR-13/14 and retained requirement fidelity: keep useful negative, property/surface and omission/compression protection; no claim that a frozen log proves reader behavior.

## Milestones

### M1. Retire instrumentation and reconcile selection

- Milestone kind: implementation.
- Engineering purpose: remove the complete private check and its consumers in one reviewable slice.
- Requirements: VAL-SR-23, VAL-SR-03/04, ENG-SR-13/14 and retained fidelity criteria.
- Architecture responsibility: Validation owns catalog/selection; current review and skill proof retain their existing owners.
- Dependencies: independent scoped Proposal/Design assessment and approved Delivery package.
- Implementation scope: delete the checker and sole fixture; remove catalog, qualification and executable references; reconcile selector tests and the approved test-spec supersession.
- Files/components likely touched: `scripts/validation_selection.py`, `scripts/test-select-validation.py`, the retired script/fixture, retained test spec and current change evidence.
- Required verification: TG-1 proves exact retired-path selection, absence of the retired check in supported mode inventories, unknown sibling rejection, and recreated-file/symlink rejection. Retained selector, skill, review and CLI suites prove current protective behavior.
- Evidence expectations: failing-before/passing-after selector regression, actual Git deletion selection, current mode inventory assertions, recoverable source identities and integrated execution outcomes.
- Implementation steps: establish retirement regression tests; remove production subsystem and update selected checks; execute focused proof; run full selected/broad proof; record exact evidence and hand off for independent review.
- Validation commands: `python scripts/test-select-validation.py -k spec_read`; `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode local --broad-smoke --jobs 4`.
- Expected observable result: local/PR changes to the two absent retired paths select current selector, skill and review regression protection. Present recreated paths and unsafe links block; unknown fixture siblings stay unclassified and block. No runtime consumer schedules the retired checker or manufactures a replacement pass.
- Completion criteria: both sources removed, callers reconciled, all required protection passes, exact recovery data and current evidence recorded, no required finding open.
- Required evidence: TG-1 and TG-FINAL-1 execution results and source identities in the owning evidence record.
- Review handoff: fresh independent complete final diff, retained protection and source recovery.
- Optional commit boundary: `Retire fixed spec-read-log instrumentation`.
- Risks: overly broad deleted-path exemptions or loss of useful tests.
- Rollback/recovery: recover both exact repository-relative files from baseline Git and revert coupled consumer changes as one unit; preserve any new user changes.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 implementation and all required corrections complete.
- Assessment: fresh independent whole-change Code Review of the entire final diff and interactions.
- Evidence: exact final subjects, independent reviewer judgment and owned finding dispositions.
- Successor: distinct final Verify, then the authorized PR handoff.

## Change-level verification

### TG-FINAL-1. Current validation still protects the delivered contract

Covers all M1 requirements through actual selected and broad execution, including selector/catalog completeness, review/skill/CLI negative cases, model/navigation and generated package checks when selected. The combined command satisfies selected and broad allocation through existing canonical deduplication. Record actual check population and failures; do not infer protection from a smaller test count.

## Validation plan

- Run the M1 commands above, starting with focused proof; rerun affected checks after corrections.
- Run `node scripts/validate-record-store.mjs docs/changes/2026-09-14-retire-spec-read-log/change.json` and `git diff HEAD --check` after final evidence recording.
- Compare retired file bytes against the baseline, review live references, verify final source identities against current review/proof, and inspect the committed diff and clean branch before push.
- Hosted CI is observed after PR creation; local results never claim hosted success.

## Risks and recovery

The test spec mixes historical obligations with current reliance. Keep the stable PERF ID as an explicit retirement disposition and preserve unrelated requirements and original reviews. Exact recovery identities remain in current change evidence; Git preserves the removed content.

## Dependencies

Current Validation authorizes the retirement; reviewers must confirm this precise scope and retained legacy amendment. Existing Python/Node and repository-owned execution are sufficient. No package or workflow configuration change is required.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | Retire the fixed-log unit without a replacement metric | It validates authored claims rather than reader behavior; VAL-SR-23 explicitly retires it. | New instrumentation or synthetic passing evidence. |
| 2026-09-14 | Keep exact retired-path selection and current protective suites | Deletion must remain reviewable without admitting arbitrary siblings or recreated inputs. | Broad fixture-directory exemption. |

## Readiness

See the owning change record for current workflow state.
