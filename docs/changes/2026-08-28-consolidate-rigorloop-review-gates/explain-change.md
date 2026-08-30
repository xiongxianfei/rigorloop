<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Consolidate RigorLoop Review Gates

Stage: explain-change
Status: current
Final diff identity: `8f80771ea0d85264e3ca33be443e17c30d77d179..7c6bdd7f84bd036fc97355c084fd53862659e1f0`
Final review identity: `code-review-final-r5` recorded in `b31fccdd31e8e7e619ab47327db26bbee51e9d3e`

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
| Boundary-first review resources | Moved review projections and activation ownership from the four retired artifact reviewers to `design-review` and `delivery-review`; updated frozen identities and cutover fixtures. | The public gate cutover must include the shared review-method resources consumed by the replacement gates. | CRG-R4–R6, R38, R43–R44 | Boundary reference: 28 passed; boundary validation: 65 passed; projection check passed. |
| Workflow automation fixtures | Replaced the obsolete `architecture-assessment` skip fixture with a rejection check and retained the supported review-resolution edge. | Tests must prove the consolidated stage graph rather than preserve a retired optional transition. | CRG-R4–R6, R35–R39 | Workflow metadata: 68 passed; workflow automation: 76 passed. |
| Change-local evidence | Recorded milestone reviews, findings, resolutions, cutover proof, and final holistic review; removed 84 transient CLI request inputs that were neither durable evidence nor referenced authority. | Preserve durable independent evidence and precise finding ownership without treating invocation inputs as lifecycle artifacts. | CRG-R32, R38, R41, R45 | Closeout validator passes with 41 reviews and 29 resolved findings; PR selection has zero request paths. |

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
| `python scripts/test-select-validation.py` | passed; restored strict handling after removing transient current-change requests. | final subject `93f212a8` |
| `python scripts/select-validation.py --mode pr --base origin/main --head HEAD` | passed; 174 changed paths, zero blockers, zero unclassified paths, and zero request paths. | final subject `93f212a8` |
| `bash scripts/ci.sh --mode broad-smoke` | passed; 11 checks in 796 seconds. | final subject `93f212a8` |
| `python scripts/test-boundary-first-reference.py` | 28 passed. | corrected subject `7c6bdd7f` |
| `python scripts/test-boundary-first-validation.py` | 65 passed. | corrected subject `7c6bdd7f` |
| `python scripts/project-boundary-first-reference.py --check` | passed; 13 projections, manifest `040fe7aa`, projection `e88317d3`. | corrected subject `7c6bdd7f` |
| `python scripts/test-validate-workflow-automation.py` | 68 passed. | corrected subject `7c6bdd7f` |
| `python scripts/test-workflow-automation.py` | 76 passed. | corrected subject `7c6bdd7f` |
| `bash scripts/ci.sh --mode pr --base 7510513c669f6cf17a155f88378cc4f4f6a7c045 --head HEAD` | passed locally; direct gate graph completed all 28 selected checks. | corrected subject `7c6bdd7f` |
| Final holistic Code Review | `code-review-final-r5` is clean for the exact CI-corrected subject. | review revision `b31fccdd` |

## Review resolution summary

The change-local resolution record closes all 29 material findings. `CRG-FH-CR1` was accepted and corrected by the bounded design-package owner route. `CRG-SEL-CR1` was accepted and resolved by reverting a selector route that did not inspect JSON and removing the transient request inputs from the final diff. The final CI correction did not add a material finding: R5 independently confirmed that boundary-resource ownership and workflow fixtures now match the consolidated gates. See `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`; closeout validation reports no open finding.

## Alternatives rejected

The change rejects merging authored artifacts, per-document or aggregate package hashes, a package-manifest document, automatic semantic edit classification, generic status mutation, settlement-driven implicit advancement, runtime old/new topology selection, activation manifests, in-place legacy migration, and rollback-specific workflow state. Each would add coupling or machinery without improving the distinct decisions this slice needs to authorize.

## Scope control

This slice does not merge architecture/specification or plan/test specification; create combined authoring skills; simplify proposal content beyond Feasibility; change Code Review or Verify ownership; add workflow profiles; define external settlement services; or preserve obsolete progression as aliases. Direct file edits outside governed authoring remain outside automatic package invalidation in this first slice.

## Risks and follow-ups

- Post-cutover changes must use actual Design and Delivery package evidence; this implementing change's grandfathered individual reviews cannot authorize later work.
- An omitted applicable ADR remains a semantic review risk; explicit architecture-stage ADR registration makes membership deterministic but cannot replace reviewer judgment.
- Direct ungoverned edits do not automatically invalidate a package. The project intentionally accepts that first-slice limit instead of restoring content hashes.
- The first hosted PR run exposed two cutover omissions: frozen boundary-first ownership still named retired review skills, and one workflow-automation fixture still accepted the retired `architecture-assessment` path. Both are corrected in `7c6bdd7f`; the exact 28-check PR graph passes locally, but hosted CI has not yet been observed for the corrected head.

## Workflow handback

Explanation status: current
Explanation basis: `b31fccdd31e8e7e619ab47327db26bbee51e9d3e`
Validation-evidence cutoff: final reviewed subject `7c6bdd7f84bd036fc97355c084fd53862659e1f0` on 2026-08-30
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
