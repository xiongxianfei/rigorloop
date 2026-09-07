# Unify Review and Closeout Policy Ownership

## Purpose / big picture

Implement the approved ownership extraction as one coherent consumer update. Review and Closeout defines assessment policy; specialized skills apply it, Workflow coordinates it, and existing Record Format and CLI contracts retain representation and mechanics.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-07-unify-review-closeout-policy/change.json).

Mutable activity, work, reviews, concerns and completion evidence live only in the selected `rigorloop-records-v2` records.

## Source artifacts

- Proposal: [Unify Review and Closeout Policy Ownership](../proposals/2026-09-07-unify-review-closeout-policy.md).
- Design: [Review and Closeout](../design/review-closeout/review-closeout.md) and [Workflow](../design/workflow/workflow.md), exact revisions in the owning record and approved Design Review.
- Retained dependencies: [Record Format](../design/record-format/record-format.md), [CLI](../design/cli/cli.md).
- Prior-contract test spec: none; this plan allocates v2 verification.

## Context and orientation

Canonical skill sources are under `skills/`; their conditional references and assets ship through existing adapter generation. Shared application resources can use the existing shared-reference projection pattern, with deterministic parity validation. The Design's clause-level map controls relocation; the implementation inventory records each mapped consumer's edit or justified historical/unaffected disposition. Direct source inspection replaces reliance on the older project map.

## Non-goals

No schema, CLI judgment selector, new review skill, migration, v1 retirement, historical approval reinterpretation, spec/architecture skill merger, release or customer activation. Unrelated workspace archives are outside this change.

## Requirements covered

| Requirements | Allocation | Proof |
| --- | --- | --- |
| RC-SR-01–04, RC-SR-08–10 | M1 reviewer applications, specialist reconciliation | TG-1 semantic scenarios and exact-subject independent review |
| RC-SR-05–07, RC-SR-13–15, RC-SR-18 | M1 reliance/closeout applications and handoffs | TG-1 composed applicability, correction and failure scenarios |
| RC-SR-11–12 | M1 plan, Delivery Review, route, Code Review and Verify checkpoint | TG-1 single/multiple milestone and post-final-review correction scenarios; M2 |
| RC-SR-16–17, WF-SR-16 | M1 governance adoption, complete consumer inventory, selective packaging | TG-2 deterministic package proof; TG-FINAL-1 cross-consumer semantic review |

## Milestones

### M1. Coherent policy application and consumer alignment

- Milestone kind: implementation.
- Engineering purpose: deliver the complete extraction together so no intermediate release mixes shared judgment rules with stale consumer exceptions.
- Requirements: RC-SR-01–18 and WF-SR-16.
- Architecture responsibility: RC-DEC-01–05; existing Workflow coordination and Record Format/CLI boundaries.
- Dependencies: exact approved Design and Delivery Review; no partial adoption.
- Implementation scope: shared portable assessment and reliance guidance; targeted skill/reference/asset reconciliation; governance ownership references; explicit final-review plan checkpoint; deterministic packaging and focused regression proof.
- Files/components likely touched: `skills/{proposal-review,design-review,delivery-review,code-review,plan,route,verify,pr,implement,ci-maintenance}/`, `templates/shared/`, affected historical review templates only for explicit contract scoping, `CONSTITUTION.md`, `AGENTS.md`, `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, `docs/architecture/system.md`, shared resource build/validation helpers and focused tests, including `scripts/validation_selection.py`, `scripts/artifact_lifecycle_validation.py` and their existing regression suites for correct v2 root dispatch when a plan index and JSON records change together. This bounded compatibility correction must select the existing complete-set validator, preserve v1 dispatch and reject malformed/unknown contracts without fallback; it adds no semantic readiness enforcement. Locate the actual system architecture path before editing. Record Format, CLI models, schemas and runtime commands remain unchanged.
- Required verification: TG-1 reviewer-guided scenario assessment; TG-2 resource parity, canonical structure and all supported adapter archives.
- Evidence expectations: stage-owned evidence lists actual commands, exact subject identities, semantic scenario observations and every clause-map consumer's disposition. Text matching alone cannot establish policy sufficiency.
- Implementation steps: establish focused resource proof; author selective shared applications; replace affected policy repetitions while retaining specialist criteria; scope historical procedures explicitly; align governance and closeout handoffs; build and validate generated packages; hand the complete slice to independent Code Review.
- Validation commands: `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/test-build-skills.py`; `python scripts/test-select-validation.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/build-skills.py --check`; `python scripts/test-adapter-distribution.py`; `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-rc-adapters`; `python scripts/validate-adapters.py --version v0.1.5 --adapter-root /tmp/rigorloop-rc-adapters`; `git diff --check`.
- Expected observable result: adopted reviewers consistently select shared judgments, retain material findings, require real independence and apply a distinct final review; installed skills remain usable without this repository.
- Completion criteria: all mapped consumers reconciled or explicitly justified unaffected; focused checks pass; independent milestone review and its required corrections complete.
- Required evidence: M1 validation and manual semantic assessment in v2 evidence; independent milestone review.
- Review handoff: full M1 engineering diff, approved package, allocation, consumer inventory and proof.
- Risks: accidental historical reinterpretation; duplicated authority; stale packaged references; overlarge common reading.
- Rollback/recovery: restore the coherent pre-adoption consumer set before delivery. After reliance on adopted guidance, stop affected continuation and fix forward without rewriting old records. An unmapped normative clause or representation gap returns to Design before dependent edits.

### M2. Final review, Verify and requested PR

- Milestone kind: lifecycle-closeout.
- Engineering purpose: independently assess the complete delivered change and its coherence before external handoff; this checkpoint is not implementation work.
- Requirements: RC-SR-05–15, RC-SR-18.
- Architecture responsibility: RC-DEC-02/03; distinct Code Review, Verify and PR owners.
- Dependencies: M1 implementation, milestone review and every required correction complete.
- Implementation scope: none; any engineering correction returns to M1 and receives affected independent reassessment.
- Files/components likely touched: stage-owned v2 review/evidence/Verify records only.
- Required verification: TG-FINAL-1; fresh independent final whole-change Code Review after M1, then successful final Verify, then authorized PR.
- Evidence expectations: distinct final review of complete engineering diff and interactions, current proof/applicability and justified concern dispositions; successful Verify explanation only after prerequisites hold.
- Implementation steps: run final selected repository checks; obtain final whole-change review; complete Verify's distinct coherence assessment; commit scoped changes, push and open the requested PR. New final-review corrections require renewed integrated assessment.
- Validation commands: `bash scripts/ci.sh --mode local --jobs 4`; `python scripts/validate-change-metadata.py docs/changes/2026-09-07-unify-review-closeout-policy/change.json`; `git diff --check`; after commit, `bash scripts/ci.sh --mode pr --base <actual-base-sha> --head <actual-head-sha>` with resolved actual revisions.
- Expected observable result: justified completion and a reviewable PR; local checks are not hosted CI claims.
- Completion criteria: final whole-change review approved on applicable basis, Verify successful, requested PR exists or an explicit external blocker is recorded.
- Required evidence: final review, Verify result, actual validation results and PR URL.
- Review handoff: Verify consumes the independent final review; PR consumes applicable Verify.
- Risks: engineering drift after review, recording-only circular invalidation, baseline validation failures.
- Rollback/recovery: route engineering drift to its owner and reassess; classify record-only changes semantically; repair in-scope failures and disclose unrelated baseline failures without claiming a pass.

## Change-level verification

### TG-FINAL-1. Complete policy-to-package closeout

- Covers: all RC requirements, M1 and M2, all eight Design boundary dimensions and its named combined hazards.
- Demonstrate: reviewers, plans, routing, verification and downstream handoff agree; standalone advisory scope stays bounded; historical outcomes remain historical; installed consumers have their triggered local resources.
- Evidence expectations: independent complete-diff inspection and manual scenario walkthrough, plus repository-selected checks and generated archive validation. Walk through decision+defect, evidence-gap+defect, optional notes, same-author role reset, bookkeeping+failed evidence, changed final subject, Verify-owned blocker+review approval, concurrent basis change, interrupted recording, changed proof environment and single-milestone missing checkpoint. Record expected versus observed guidance and limits against current subjects.
- Non-applicability: no executable judgment selector is designed; automated assertions prove packaging/structure only. Human/agent semantic review proves guidance adequacy. No test-group exemption waives final Code Review.

## Validation plan

TG-1 uses the bounded manual walkthrough above: implementation author records observed guidance and independent reviewer assesses it. Inputs are current installed resources and approved policy; expected results come from RC requirements, not a transcript score. Evidence expires when relevant subjects, governing basis or execution environment change. TG-2 uses M1 commands; M2 adds selected integrated checks. Reuse requires explicit unaffected-surface rationale and cannot override a required fresh/current check.

## Risks and recovery

Baseline Workflow historical links must be assessed for reliance; unrelated historical debt is disclosed, not silently repaired or counted as proof. The existing project-wide workflow-context failure does not replace v2 primary status/context or justify lifecycle fallback. Dependency models and stored contracts stay unchanged.

## Dependencies

Design approval precedes Delivery approval; M1 precedes its independent review and correction closeout; M2 final whole-change review precedes successful Verify; PR requires separate user authority already supplied by the request to continue through PR.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-08 | Correct v2 dispatch in the existing validation wrappers | Integrated checks synthesized a nonexistent change.yaml for this JSON root; preserve existing structural validation and historical compatibility | Fabricating v1 records, skipping complete-set validation, changing record or CLI contracts |
| 2026-09-08 | One coherent implementation milestone plus separate lifecycle closeout | Consumer policy changes must land together; review can inspect bounded resource and consumer groups within one exact diff | Partial activation across milestones; using milestone review as final review |

## Readiness

See the owning change record for current workflow state.
