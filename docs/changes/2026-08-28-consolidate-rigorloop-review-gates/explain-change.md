<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Consolidate RigorLoop Review Gates

Stage: explain-change
Status: current
Final diff identity: `8f80771ea0d85264e3ca33be443e17c30d77d179..638b9ccabde7b42b584c1773eec540b16098fdfd`
Final review identity: `code-review-final-r2` recorded in `fec22dbf31fd4e737ed2753d6992bbddb95946d1`

## Summary

RigorLoop now reviews coherent engineering decisions instead of approving every authored file separately. Proposal Review evaluates direction and embedded feasibility; Design Review approves architecture, specification, and applicable ADRs together; Delivery Review approves the plan and test specification together. Code Review and Verify remain separate. The implementation exposes exact artifact ID-to-path maps and upstream review IDs, deliberately avoids package/member hashes, and retires the four old artifact-review progression entrypoints in one cutover.

## Problem

The former sequence allowed architecture and specification, and later plan and proof design, to acquire separate progression authority even though each pair must agree before downstream work is safe. That produced repeated review ceremony, partial approval states, duplicated lifecycle rules, and weak cross-artifact reasoning. The selected direction preserves each useful authoring artifact and its owner while consolidating only the decisions that authorize progression.

## Decision trail

- The accepted proposal chose five decision gates—Proposal Review, Design Review, Delivery Review, Code Review, and Verify—and embedded one Feasibility section in the proposal.
- `specs/consolidated-review-gates.md` defines CRG-R1 through CRG-R45, eight boundary classes, and INT-001 through INT-008. It expressly rejects aggregate/member hashes, activation manifests, runtime topology selection, and rollback-specific lifecycle machinery.
- `ADR-20260828-consolidated-review-package-topology.md` selects explicit member maps in `change.yaml`, package-specific record/settle operations within the existing lifecycle command family, workflow-owned `advance-stage`, stage-owned artifact editing, and one atomic public cutover.
- The approved plan divided the work into topology foundation, package authority, routing, public review skills, validation/parity, atomic cutover, and lifecycle closeout.
- CRG-R40 governs this implementing change under the pre-cutover reviews recorded in its change pack. Its historical individual reviews are intentionally grandfathered for this change only; they are not inferred as Design or Delivery package authority for post-cutover work.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| Proposal template and Proposal Review | Added and evaluates one embedded Feasibility section. | Keep feasibility useful without another artifact or gate. | CRG-R7–R11 | Skill and adapter validation; proposal review evidence. |
| Lifecycle contract and package engine | Added `design` and `delivery` member maps, package review recording/settlement, invalidation, status, and closed outcomes. | Make package authority explicit, atomic, inspectable, and hash-free. | CRG-R12–R34; ADR package identity | Lifecycle evidence, contract, read, transaction, and metadata tests. |
| Stage and correction routing | Added the consolidated adjacent graph, isolated `advance-stage`, package-aware corrections, and Design Review rerouting for Delivery upstream-direction findings. | Separate judgment from continuation and preserve exact owning-stage correction. | CRG-R2–R6, R29–R34; INT-007 | Stage-advance and correction-route tests, including CRG-FH-CR1 regression. |
| Milestone lifecycle | Preserved implementation/code-review milestone behavior and final closeout boundaries. | Consolidation must not weaken implementation review or Verify. | CRG-R41–R42 | Milestone and lifecycle-read suites. |
| Canonical skills and guidance | Added `design-review` and `delivery-review`; removed public `architecture-review`, `spec-review`, `plan-review`, and `test-spec-review`; updated workflow and downstream consumers. | Publish one unambiguous decision-gate model with separate authorship. | CRG-R4–R6, R33, R41 | Skill validator: 450 passed, 90 retired-topology skips. |
| Validators and schema | Added package shapes, closed vocabularies, historical-authority rejection, cutover inventory, and review-attribution checks. | Fail closed before consistency and prevent partial/mixed authority. | CRG-R22–R29, R35–R45 | Metadata validator: 66 passed; review validator: 104 passed; CLI conformance passed. |
| Adapter distribution | Published the two new review skills and removed the four retired entrypoints from generated adapter inventories and archives. | Canonical and packaged public behavior must cut over together. | CRG-R38, R43–R44 | Adapter distribution: 154 passed. |
| Change-local evidence | Recorded milestone reviews, findings, resolutions, cutover proof, and final holistic review. | Preserve durable independent evidence and precise finding ownership. | CRG-R32, R38, R41, R45 | Closeout validator passes with 38 reviews and 28 resolved findings. |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| CRG-T01–T03 | Topology vocabulary, embedded feasibility, and exact stage graph. | static and integration |
| CRG-T04–T07 | Deterministic package membership, compact status, atomic outcomes, and authority. | integration |
| CRG-T08–T11 | Finding attribution, correction routing, invalidation, replay, interruption, and closed vocabulary. | integration and failure-path |
| CRG-T12–T17 | Historical-authority rejection, cutover completeness, generated parity, downstream assurance, and full traceability. | repository and distribution |
| CRG-FH-CR1 regression | Delivery upstream-direction and named blocked results route through a new Design Review; wrong routes do not mutate state. | public lifecycle operation |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `npm test --prefix packages/rigorloop` | 298 total; 296 passed; 2 explicitly historical individual-review correction scenarios skipped. | corrected subject `638b9cca` |
| Focused lifecycle contract/evidence/routing/read/milestone/transaction suite | 97 total; 95 passed; the same 2 historical scenarios skipped. | corrected subject `638b9cca` |
| `python scripts/test-lifecycle-cli-conformance.py` | passed; invalid=6, protected=10. | corrected subject `638b9cca` |
| `python scripts/test-change-metadata-validator.py` | 66 passed. | corrected subject `638b9cca` |
| `python scripts/test-review-artifact-validator.py` | 104 passed. | corrected subject `638b9cca` |
| `python scripts/test-skill-validator.py` | 450 passed; 90 retired-topology scenarios skipped by design. | corrected subject `638b9cca` |
| `python scripts/test-adapter-distribution.py` | 154 passed. | corrected subject `638b9cca` |
| Final holistic Code Review | `code-review-final-r2` is clean-with-notes. | review revision `fec22dbf` |

## Review resolution summary

The change-local resolution record closes 28 material findings: 26 accepted, one partially accepted, and one rejected owner-level finding. `CRG-FH-CR1`, the only final holistic finding, was accepted and corrected by the bounded design-package owner route. See `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`; closeout validation reports no open finding.

## Alternatives rejected

The change rejects merging authored artifacts, per-document or aggregate package hashes, a package-manifest document, automatic semantic edit classification, generic status mutation, settlement-driven implicit advancement, runtime old/new topology selection, activation manifests, in-place legacy migration, and rollback-specific workflow state. Each would add coupling or machinery without improving the distinct decisions this slice needs to authorize.

## Scope control

This slice does not merge architecture/specification or plan/test specification; create combined authoring skills; simplify proposal content beyond Feasibility; change Code Review or Verify ownership; add workflow profiles; define external settlement services; or preserve obsolete progression as aliases. Direct file edits outside governed authoring remain outside automatic package invalidation in this first slice.

## Risks and follow-ups

- Post-cutover changes must use actual Design and Delivery package evidence; this implementing change's grandfathered individual reviews cannot authorize later work.
- An omitted applicable ADR remains a semantic review risk; explicit architecture-stage ADR registration makes membership deterministic but cannot replace reviewer judgment.
- Direct ungoverned edits do not automatically invalidate a package. The project intentionally accepts that first-slice limit instead of restoring content hashes.
- Hosted CI has not yet been observed for the final handoff revision. Final Verify must run current required validation, broad smoke, drift checks, and immutable branch-basis resolution.

## Workflow handback

Explanation status: current
Explanation basis: `fec22dbf31fd4e737ed2753d6992bbddb95946d1`
Validation-evidence cutoff: corrected subject `638b9ccabde7b42b584c1773eec540b16098fdfd` on 2026-08-30
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
