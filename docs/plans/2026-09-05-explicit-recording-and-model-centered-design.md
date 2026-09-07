# Explicit Recording and Model-Centered Design — Delivery Plan

## Purpose / big picture

Deliver an explicit recording CLI and one authoritative Design document per coherent model. Workflow actors retain decisions; the CLI protects persistence without imposing lifecycle transitions. Sequence the implementation so that new writers are not adopted before the contract, safe-save behavior, skills and validation agree.

## Current Handoff Summary

- Owning change record: None established for this portable plan. The user requested planning and independent Delivery Review following the isolated advisory Design Review.

This plan does not create lifecycle authority. Before implementation, establish the governing approval and recording basis through the responsible workflow owner. Do not fabricate an upstream review ID or initialize planned work from this draft. Mutable progress and command results belong in execution/review evidence, not this plan. Formal settlement is not replaced by a clean advisory review.

## Source artifacts

- Proposal: [Explicit Workflow Recording and Model-Centered Design](../proposals/2026-09-05-explicit-recording-and-model-centered-design.md).
- Specification and architecture, combined by user-authorized exception: [Workflow model](../design/workflow/workflow.md) and [CLI model](../design/cli/cli.md).
- Design assessment: The former outside-change assessment was removed at the user’s direction. This plan reference supplies no Design Review authority; use the owning change’s registered review records.
- Prior-contract test spec: None; this is not a manifest-bound v1 continuation.
- Governing repository rules: [Constitution](../../CONSTITUTION.md) and [AGENTS.md](../../AGENTS.md), unchanged by this plan.

## Context and orientation

The Node package at `packages/rigorloop/` already contains historical lifecycle and compact engines. The new `record-store` namespace must not silently invoke their semantic eligibility rules. Preserve those handlers and their tests; reuse persistence helpers only where their safety can be separated from state derivation. Canonical skills are under `skills/`; installed mirrors are not authored sources. Existing adapter generation and validation scripts remain the distribution mechanism.

The two Design inventories, WF-MAP-01–10 and CLI-MAP-01–07, identify the principal adoption surfaces. Use their source links rather than treating all architecture, specs or historical change records as rewrite targets. No project-map inference is required for this bounded plan. Existing unrelated working-tree edits must be preserved and baseline failures distinguished from regressions.

## Non-goals

- OS selection, OS-specific implementation prescriptions, a platform matrix or separate OS investigation.
- Automatic workflow transitions, automatic approval, hosted coordination or new execution permissions.
- Migrating historical change roots, deleting old engines or retargeting old approvals.
- Removing final Code Review, releasing packages, opening PRs or changing unrelated commands.
- New mandatory Design sidecars or a separate test-spec artifact.

## Requirements covered

The model requirement ID and named architectural boundary are the traceability keys. The designs' existing scenario tables supply boundary meaning; the plan does not invent normative boundary outcomes or claim that those tables already implement the old formal boundary format.

| Requirement | Architectural boundary | Milestone | Proof group |
| --- | --- | --- | --- |
| WF-SR-01 | Explicit actor decisions | M3 | TG-05, TG-FINAL-01 |
| WF-SR-02 | Change schema, registry and model identities | M1, M3 | TG-01, TG-05 |
| WF-SR-03 | Independent judgment and applicability | M3 | TG-05, TG-FINAL-01 |
| WF-SR-04 | Explicit invalidation and correction impact | M3 | TG-05, TG-FINAL-01 |
| WF-SR-05 | Verify-originated blocker | M3 | TG-05, TG-FINAL-01 |
| WF-SR-06 | Reopen and rereview without stage prerequisite | M3 | TG-05, TG-FINAL-01 |
| WF-SR-07 | One engineering truth per model | M3 | TG-06 |
| WF-SR-08 | Exact model/review and requirement references | M1, M3 | TG-01, TG-06, TG-FINAL-01 |
| WF-SR-09 | Downstream reliance and success-only completion | M3 | TG-05, TG-FINAL-01 |
| WF-SR-10 | New-change-only adoption and historical isolation | M1, M4 | TG-02, TG-07, TG-FINAL-02 |
| CLI-SR-01 | Read-only coherent snapshot | M2 | TG-03 |
| CLI-SR-02 | Closed schema and structural rejection | M1, M2 | TG-01, TG-03 |
| CLI-SR-03 | Explicit replacement and byte preservation | M2 | TG-03 |
| CLI-SR-04 | Revision and declared read/write basis | M2 | TG-04 |
| CLI-SR-05 | Coherent publication | M2 | TG-04 |
| CLI-SR-06 | Explicit interrupted-save recovery | M2 | TG-04 |
| CLI-SR-07 | Observation versus semantic judgment | M2, M3 | TG-03, TG-05 |
| CLI-SR-08 | Retry and duplicate-effect prevention | M2 | TG-04 |
| CLI-SR-09 | Containment and common write protection | M2 | TG-03, TG-04 |
| CLI-SR-10 | Contract isolation and no implicit migration | M1, M4 | TG-02, TG-07 |
| CLI-SR-11 | Commands, snapshot/results and safe diagnostics | M2 | TG-03, TG-04 |

## Milestones

### M1. Establish contract fixtures and compatibility isolation

- Milestone kind: implementation.
- Engineering purpose: Establish a reviewable representation boundary before a writer exists.
- Requirements: WF-SR-02/08/10; CLI-SR-02/10.
- Architecture responsibility: Workflow Explicit record schema; CLI Candidate update contract; WF-DEC-02 and CLI-DEC-02.
- Dependencies: The formal implementation authority prerequisite above, and independent Delivery Review of this plan. Advisory assessments alone do not satisfy it.
- Implementation scope: Add new-contract schema validation, representative fixtures and compatibility dispatch tests; keep new record-store writes unavailable to ordinary users. Do not modify old discriminators or broaden old schemas.
- Files/components likely touched: New schema and fixtures under `schemas/` and `tests/fixtures/`; package validation helpers and `packages/rigorloop/test/`; `scripts/validate-change-metadata.py` and its regression tests where contract dispatch is shared.
- Required verification:
  - TG-01 — All Workflow record types and CLI request/result shapes: required fields, unknown values, duplicate keys/IDs/paths, malformed encodings, reference integrity, null/empty partitions, exact limits and stable subject references. Include an explicit unknown-value regression for every new closed vocabulary.
  - TG-02 — Historical and unknown contracts reject new-contract writes without changing bytes; old fixtures retain their original interpretation. Initial creation requires an absent root, not merely an absent manifest.
- Evidence expectations: Tests discovered by the existing package test runner, plus Python metadata regression coverage when touched. Evidence names actual cases and assertions, not just a green suite count.
- Implementation steps: Write failing fixtures/checks first; implement representation validation; confirm registry/subject distinction; demonstrate all rejection paths unchanged; review the slice before persistence work.
- Validation commands: `npm --prefix packages/rigorloop test`; `python scripts/test-change-metadata-validator.py`; `git diff --check`.
- Expected observable result: New records are structurally recognizable in tests; no new public writer or changed historical semantics.
- Completion criteria: TG-01/02 have direct proof, existing contract regressions pass, new closed values fail explicitly and the slice has independent Code Review.
- Required evidence: Requirement/group-to-test mapping, command outcomes, affected fixture identities and before/after rejection evidence.
- Review handoff: Code Review of new schema/validation and historical separation only.
- Risks: Treating schema validation as permission or carrying over semantic state checks.
- Rollback/recovery: Remove only this slice's unadopted new-contract additions through a reviewed revert; preserve existing schemas and user changes.

### M2. Implement inspect, check, record and recover

- Milestone kind: implementation.
- Engineering purpose: Deliver the complete storage boundary together; do not expose writes before their recovery and reader behavior exist.
- Requirements: CLI-SR-01–09/11.
- Architecture responsibility: CLI command/result, snapshot, revision/read-set and Save safety and recovery boundary; CLI-DEC-01–04.
- Dependencies: M1 independently reviewed. New behavior runs in isolated fixture roots until M4 adoption.
- Implementation scope: New namespace and storage library, exact-byte parsing/output, coherent inspection, candidate validation, conflict-safe replacement and explicit recovery. Reuse existing safety machinery proportionately without OS-specific research or redesign. No call to old workflow eligibility as a prerequisite.
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, new package-local record-store modules and package tests. Existing compact transaction helpers only if extraction is justified and historical regressions accompany it.
- Required verification:
  - TG-03 — Invoke every public command in text and JSON. Inspect actual record content, missing registered files, absent root and unsafe/malformed manifest; preserve null snapshots for other operations and failed reads. Check is read-only; record preserves supplied status and unnamed bytes. Cover exact argument errors, limits, safe diagnostics and containment via public and helper paths.
  - TG-04 — Competing writers from the same revision; read-set drift; stale retry after lost response; no duplicate findings; interruption before/during/after publication; coherent reader or busy/recovery-required; complete and restore; interruption of recovery; changed/tampered/missing recovery data; an external third-state edit; committed success not rolled back. Observe both resulting bytes and command outcomes.
- Evidence expectations: Controlled failure injection and deterministic competing-operation tests, plus real public CLI subprocess tests in temporary repositories. Helper-only tests cannot substitute for the public read/write/recover boundary. No multi-OS matrix.
- Implementation steps: Write command and failure tests first; implement read/check; implement record and recovery behind non-adopted access; reconcile result rendering; demonstrate the full save/recovery pair before exposing it for adoption.
- Validation commands: `npm --prefix packages/rigorloop test`; `git diff --check`.
- Expected observable result: Fixture users can read and explicitly save decisions; an interrupted save cannot be mistaken for usable current state.
- Completion criteria: TG-03/04 direct proof, all unchanged historical package tests passing, no normal public activation and independent Code Review of the complete storage slice.
- Required evidence: Exact selected cases, request basis, outcomes, affected bytes and recovery completion/stop evidence. Preserve failure evidence, not only successful retries.
- Review handoff: Code Review of command/library integration and safe-save negative paths.
- Risks: Reintroducing a semantic engine inside validation; partial publication; inspection leaking content into errors.
- Rollback/recovery: Before adoption, disable/revert new dispatch only; recover any temporary fixture transactions with the tested mechanism. Never remove unknown external bytes to make a test pass.

### M3. Integrate actor-owned workflow and model documentation

- Milestone kind: implementation.
- Engineering purpose: Align guidance and semantic proof before enabling new-contract work.
- Requirements: WF-SR-01–09; CLI-SR-07.
- Architecture responsibility: Workflow responsibility table, model-document ownership, correction and Verify paths; WF-DEC-01–04.
- Dependencies: M1/M2 independently reviewed; keep ordinary new writers unadopted.
- Implementation scope: Canonical stage skills/references/assets, model/document references, governance amendments and validators identified by WF-MAP-01–10. Keep changes explicitly prospective until M4; historical roles remain selectable under their contracts. Boundary mapping is reference/verification allocation, not authority to invent behavior. Any discovered behavioral gap returns to Design and affected rereview before dependent code.
- Files/components likely touched: `CONSTITUTION.md`, `AGENTS.md`, `specs/rigorloop-workflow.md`, relevant sections of `docs/architecture/system/architecture.md`, canonical `skills/architecture`, `skills/spec`, `skills/route`, `skills/design-review`, `skills/plan`, `skills/delivery-review`, `skills/implement`, `skills/code-review`, `skills/verify` and their actually affected resources; skill/boundary validators and tests.
- Required verification:
  - TG-05 — Scenario fixtures and independent walkthrough: author invalidation, route selection of a completed owner, Verify-originated blocker, independent rereview, explicit final completion, stale evidence prohibiting reliance but not correction recording, role text not proving independent review, and no automatic stage/approval change after a save.
  - TG-06 — Map every WF/CLI requirement and existing scenario row to these groups and concrete checks; cross-model references have one owner; overlapping features retain exact review subjects; adoption inventory identifies every changed source and retained historical contract. Validate affected skill resources and model references without creating sidecar engineering truth.
- Evidence expectations: Automated record/skill fixtures plus a concise independent human/agent walkthrough of the exact changed guidance. A structural validator cannot establish actual reviewer independence or semantic adequacy.
- Implementation steps: Expand inventory rows to exact affected files; update prospective guidance and mappings; run fixtures through M2 commands; record walkthrough evidence; resolve any contradiction at its owner before review.
- Validation commands: `python scripts/validate-skills.py skills`; `python scripts/test-skill-validator.py`; `python scripts/test-boundary-first-validation.py`; `python scripts/validate-boundary-first.py --check --path docs/design/workflow/workflow.md --path docs/design/cli/cli.md --path docs/design/record-format/record-format.md` after model-aware recognition exists; `npm --prefix packages/rigorloop test`; `git diff --check`.
- Expected observable result: A fresh actor can follow the new process using model files and explicit records, with no engine-driven stage decision and no public adoption yet.
- Completion criteria: TG-05/06 proved; changed resources reconciled; no unresolved normative behavior gap hidden as a mapping task; independent Code Review.
- Required evidence: Exact requirement/test mapping and walkthrough note identifying actor, fixture, actions, expected/observed records, review provenance and current source identities. Rerun when referenced guidance or commands change.
- Review handoff: Code Review of workflow integration and governance compatibility, with Design-owner escalation for new behavior.
- Risks: Global guidance accidentally changing historical work; treating independent review as a metadata assertion.
- Rollback/recovery: Revert only prospective new-contract guidance and affected generated outputs; historical records and review findings remain untouched.

### M4. Prove integrated adoption and enable new changes coherently

- Milestone kind: implementation.
- Engineering purpose: Make adoption the final integration slice rather than enabling a partially compatible writer.
- Requirements: WF-SR-10 and integrated WF-SR-01–09; CLI-SR-10 and integrated CLI-SR-01–11.
- Architecture responsibility: Both Adoption/compatibility boundaries and the replacement inventories.
- Dependencies: M1–M3 reviewed; all required local proofs and the cross-milestone scenarios below pass before enabling ordinary new-change writes. The activation mechanism must be explicitly agreed in the adoption diff; do not invent a silent default or historical bootstrap reuse.
- Implementation scope: Contract selection/support metadata, new-contract scaffolds, package routing, all supported adapter output and final governing cutover. New changes require explicit selection; no existing root migrates. Include contributor compatibility/rollback instructions.
- Files/components likely touched: Package command/contract registration, new schema/templates, validation/CI selectors, canonical skill generation inputs, `dist/adapters/manifest.yaml` and its support README when actually affected. Generated public archives are built by repository scripts, not hand-edited or committed as authored source.
- Required verification:
  - TG-07 — Coherent new-change-only adoption, historical fixture non-mutation, unknown/mixed versions fail closed, explicit root creation, old handlers remain usable, rollback before new records and write-stop/fix-forward after new records.
  - TG-FINAL-01 and TG-FINAL-02 below.
- Evidence expectations: Fresh temporary project exercising the packaged CLI and generated adapters; check each advertised adapter, not installed local runtime mirrors. Byte-preservation checks for historical fixtures and no-network/no-Git reconstruction.
- Implementation steps: Build artifacts from reconciled sources; run end-to-end and compatibility checks; inspect the exact adoption diff; enable only after agreement is demonstrated; independently review the adoption slice, then obtain final whole-change Code Review before Verify.
- Validation commands: `npm --prefix packages/rigorloop test`; `python scripts/build-adapters.py --check`; `python scripts/test-adapter-distribution.py`; `python scripts/test-change-metadata-validator.py`; `bash scripts/ci.sh --mode local`; `git diff --check`.
- Expected observable result: Explicit new-contract creation works only with coherent guidance and tooling; historical contracts remain unchanged.
- Completion criteria: TG-07 and both final groups pass; affected inventory has no required deferred dependency; independent Code Review; no release/publication implied.
- Required evidence: Package/adapter identities, generated parity, full historical compatibility outcomes, adoption agreement and rollback evidence. Do not claim a command covered newly added behavior unless its selected checks actually include it.
- Review handoff: M4 slice Code Review of adoption and compatibility, then a distinct independent final whole-change Code Review of the complete M1–M4 implementation, cross-milestone interactions and current design/delivery basis. Resolve material findings through their owning milestones and obtain affected rereview before separately authorized Verify. Passing integrated tests or the M4 slice review does not substitute for the final judgment.
- Risks: Activating before supported skills agree, or reverting to an old writer after new records exist.
- Rollback/recovery: Before first new root, restore prior distribution/guidance. After new roots, stop new writes and retain compatible readers; fix forward or obtain a separately approved conversion. Never erase new roots or reinterpret them to simulate rollback.

### M5. Verify and record final closeout

- Milestone kind: lifecycle-closeout.
- Engineering purpose: Assess complete-change coherence after all implementation slices; do not hide remaining implementation here.
- Requirements: WF-SR-09/10 and all proof obligations above.
- Architecture responsibility: Success-only Verify and durable evidence.
- Dependencies: M1–M4 closed through their independent slice reviews; a clean independent final whole-change Code Review covers the current complete implementation and cross-milestone interactions; material findings are resolved with required rereview; any triggered CI maintenance is completed. If correction or CI work changes the final review's basis, refresh that review before Verify relies on it.
- Implementation scope: None; rerun final proof and record truthful Verify/evidence under the established governing authority.
- Files/components likely touched: Authorized stage-owned verification and lifecycle evidence only.
- Required verification: TG-FINAL-01/02, freshness of every required result and exact approved subject.
- Evidence expectations: Actual named command outcomes and current identities, the final whole-change Code Review judgment and exact reviewed subjects, finding dispositions and affected rereview evidence, residual risks, final explanation and any failed-Verify blocker; no success report on failure.
- Implementation steps: Confirm the final whole-change review is clean and current; reconcile artifact/code/test basis; run required final checks; handle failures at the owning milestone and obtain affected independent rereview when the reviewed basis changes; then record successful closeout only if warranted.
- Validation commands: All applicable M4 commands plus focused reruns identified by evidence drift.
- Expected observable result: Evidence supports completion or clearly names the unresolved failure.
- Completion criteria: Successful independent Verify under proper authority; no implementation or review obligation remains.
- Required evidence: Success-only Verify report or explicit failure/blocker evidence, referencing the current final whole-change review and any correction/rereview evidence used for reliance.
- Review handoff: Isolated stop. No PR, push or release authorized by this plan.
- Risks: Confusing clean milestone reviews with whole-change correctness.
- Rollback/recovery: Failed Verify returns to the owning correction without changing evidence into success.

## Change-level verification

### TG-FINAL-01. Explicit workflow end to end

- Covers: M1–M4; WF-SR-01–09; CLI-SR-01/03–09/11.
- Demonstrate: In a fresh local fixture, inspect content, record an explicit decision, revise a model, retain the old reviewed hash, record applicability/correction, reopen a completed owner, originate a Verify blocker, independently rereview and explicitly complete. Add a competing save and interrupted transaction at the public command boundary. No command supplies stage, judgment or ownership automatically.
- Evidence expectations: Package tests exercise the public commands; an independent walkthrough checks semantic responsibility and provenance against the exact changed skills. Record the fixture identity, participants, action sequence, observed data and exceptions. This note expires on changes to its governing guidance or executable subjects.
- Non-applicability: None; milestone-local proof cannot establish the integrated agent/storage contract. Automated fixtures do not establish real independent judgment, so the scoped walkthrough is required, not OS testing.

### TG-FINAL-02. Adoption and compatibility across supported outputs

- Covers: M1–M4; WF-SR-07/08/10; CLI-SR-02/09/10 and inventories.
- Demonstrate: Generated adapters agree with model paths and commands; historical roots are byte-unchanged; new/unknown/mixed contracts are distinguished; rejected writes cannot alter old roots; no Git/PR/chat dependency; rollback retains interpretable records.
- Evidence expectations: Adapter archive validation, historical/new fixture assertions, integration tests, and a reviewed inventory with explicit treatment of every affected source. Full CI selected checks must include these new fixtures, not only historical suites.
- Non-applicability: No historical conversion test is required because conversion is prohibited; tests must prove that prohibition instead.

## Validation plan

Commands above are future implementation checks, not results obtained while authoring this plan. `npm --prefix packages/rigorloop test` invokes the existing Node test runner; each milestone must add discoverable tests for its groups before claiming coverage. Implementation may run focused tests first, but the named regression scope remains required for milestone handoff.

Boundary-format recognition must be updated alongside reference mapping, not bypassed by skipping the validator. If that work needs a new normative outcome, return it to the Design owner and rereview the affected basis rather than encoding a decision in tests. Whole-project baseline failures must be reported separately; they are not permission to ignore task regressions or announce passing CI.

Manual semantic proof uses only temporary project records and observed actor/reviewer actions. It does not rely on chat reconstruction or require a new committed raw-output artifact. Store concise execution proof in the appropriate stage-owned evidence after authority is established. Reviewer independence cannot be proved by a test assigning two role strings.

## Risks and recovery

- Risk: Scope expands from a recorder into another lifecycle engine. Recovery: reject transition inference in TG-03/05 and return the offending change to its owning milestone.
- Risk: Mapping work conceals a design change. Recovery: stop the affected slice for explicit Design correction and review; keep unrelated safe work isolated.
- Risk: Record-store is usable before recovery or guidance integration. Recovery: keep it unavailable for ordinary adoption through M3; M4 owns coherent enablement.
- Risk: Existing worktree changes are mistaken for initiative output. Recovery: establish a read-only baseline and preserve unrelated files; do not reset or overwrite historical work.

## Dependencies

Formal implementation authority must be resolved outside this portable plan before M1 execution. The plan does not register itself, approve itself or implement its own governance exception. Repository-owned test/generation commands and the existing runtime are the execution assumptions. No external publication, credentials or OS research is a dependency.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-05 | Separate representation, complete storage, workflow integration and adoption into M1–M4. | Keep intermediate states safe and independently reviewable. | Early public writer followed later by recovery or compatible skills. |
| 2026-09-05 | Allocate boundary references and adoption reconciliation as delivery tasks under existing model requirements. | Avoid another speculative design round; escalate only actual new behavior. | Inventing a new boundary artifact or silently deciding behavior in validators. |
| 2026-09-05 | Preserve historical contracts and exclude OS investigation. | Match the accepted user scope and maintain evidence meaning. | Bulk migration, old-engine deletion or a platform-certification gate. |

## Readiness

This portable plan is intended for the requested independent advisory Delivery Review. It is not implementation permission. Current formal authority and later milestone state must be recorded through the responsible workflow owner, not inferred from this plan's existence or review wording.
