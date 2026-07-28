# Portable Boundary-First Capability for Published Skills

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Change ID: 2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording
- Start date: 2026-07-27
- Last updated: 2026-07-28
- Related issue or PR: none
- Supersedes: none

## Goal

Ship `boundary-first-v1` as one portable method used by all ten governed
published lifecycle skills, with deterministic structural validation,
package/install parity, prospective activation, and stage-local semantic
review ownership.

## Why now

The accepted proposal and approved specification replace an abandoned
runtime-certification direction with a portable published-skill contract.
Execution must preserve that smaller trust boundary while closing the shared
reference, lifecycle, validation, packaging, and activation work as separately
reviewable slices.

## Governing artifacts

- Proposal:
  `docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md`
- Feature spec: `specs/boundary-first-proof-model.md`
- Workflow amendment: `specs/rigorloop-workflow.md`
- Skill contract amendment: `specs/skill-contract.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md`
- Change record:
  `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/change.yaml`
- Test spec: `specs/boundary-first-proof-model.test.md`

## Scope

### In scope

- One canonical method reference and raw-byte projections into the ten
  governed skill roots.
- Stage-specific `READ` mappings, instructions, ownership, and stop conditions
  in `workflow`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`,
  `test-spec-review`, `implement`, `code-review`, and `verify`.
- Closed structural validation for boundary records, proof maps, activation
  state, source/consumer inventory, identifiers, and references.
- Deterministic activation and grandfathered-spec inventory evidence.
- Generated, packed, and installed parity proof for Codex, Claude Code, and
  opencode.
- Review fixtures that distinguish structural validity from semantic
  completeness.
- Atomic lifecycle settlement of the contract, activation record, governed
  skills, validators, package evidence, and plan state.

### Out of scope

- Runtime, model, server, transport, network, sandbox, or workspace-attestation
  enforcement.
- A new boundary-review lifecycle stage.
- Retrofitting accepted historical feature specs.
- Feature-specific dimensions or a full Cartesian interaction matrix.
- A release or public publication.

## Constraints

- `skills/` remains the only authored skill source; generated public adapter
  output is not hand-edited.
- Every installed governed skill reads its own skill-local byte-identical
  reference and never a repository-root path.
- Structural validation fails closed on unknown closed-vocabulary values
  before consistency checks and does not claim semantic completeness.
- `spec-review`, `plan-review`, `test-spec-review`, `code-review`, and `verify`
  retain their distinct semantic responsibilities.
- The activation state stays `pending` until every required surface and proof
  is current in M4.
- No implementation milestone starts before plan-review and test-spec-review
  approve their governing artifacts.

## Requirement coverage

| Workstream | Governed requirements |
| --- | --- |
| Contract and activation | PBF-R001 through PBF-R007, PBF-R049a through PBF-R058 |
| Boundary and example records | PBF-R008 through PBF-R031 |
| Proof map | PBF-R032 through PBF-R040 |
| Governed lifecycle skills | PBF-R041 through PBF-R045, PBF-R059 through PBF-R064 |
| Reference and package parity | PBF-R046 through PBF-R049 |
| Portability | PBF-R065 |
| Workflow integration | WF-R028 through WF-R036 |
| Published-skill resource contract | SC-R056 through SC-R063 |

The matching test spec must map every `MUST` in these ranges to direct proof or
an explicit blocking gap before implementation begins.

## Current Handoff Summary

- Current milestone: M1. Canonical reference and projection foundation
- Current milestone state: review-requested
- Latest review evidence: code-review-m1-r3 plus correction commit 877a697f; PBF-M1-CR1 through PBF-M1-CR4 resolved
- Last reviewed milestone: M1
- Review status: review-requested; stage=code-review; round=r4
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: code-review M1 R4
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending — review-state=closed; open-count=0; open-findings=none

## Milestones

### M1. Canonical reference and projection foundation

- Milestone state: review-requested
   - primary trust boundary: one authored method and a closed deterministic
     projection inventory
   - deliverables:
     - add `specs/references/boundary-first-method-v1.md` as the single
       authored method;
     - add a repository-owned projection module and a
       `--check`/`--write` command that own the closed version, source, and ten
       consumers;
     - write raw bytes to each governed
       `skills/<skill>/references/boundary-first-method-v1.md`;
     - centralize the specified path/raw-byte digest algorithm for reuse by
       projection and activation validation;
     - add unit tests for check/write idempotency, exact consumer membership,
       byte divergence, missing projections, digest reproducibility, and
       unknown closed values.
   - dependencies: approved architecture-review and test-spec-review
   - targeted validation:
     - `python scripts/test-boundary-first-reference.py`
     - `python scripts/project-boundary-first-reference.py --check`
   - recovery: remove the new projection command, canonical source, and only
     the ten generated reference copies; activation remains `pending`.
   - implementation handoff:
     - [x] targeted validation passed
     - [x] hand off to code-review for M1
   - review closeout:
     - [ ] code-review completed
     - [ ] material findings resolved or explicitly dispositioned
     - [ ] M1 lifecycle projection updated before starting M2
   - milestone commit message:
     `M1: add deterministic boundary reference projection`

### M2. Governed lifecycle skill behavior

- Milestone state: planned
   - primary trust boundary: stage-local authoring, review, stop, and handoff
     behavior
   - deliverables:
     - add one stage-specific `READ` resource-map entry to every governed
       `SKILL.md`;
     - update each skill only for its PBF-R043 responsibility and PBF-R064
       stop behavior;
     - keep stage approval semantics and artifact placement in the owning
       skill rather than the shared method;
     - add skill fixtures for structurally valid but semantically incomplete
       boundary and proof records so review skills reject them for the correct
       semantic reason;
     - prove all governed skills point to the same projected reference.
   - dependencies: M1 reviewed and closed
   - targeted validation:
     - `python scripts/validate-skills.py`
     - `python scripts/test-skill-validator.py`
     - `python scripts/build-skills.py --check`
   - recovery: revert the ten resource-map and stage-local behavior edits;
     M1 projections may remain dormant and activation remains `pending`.
   - implementation handoff:
     - [ ] targeted validation passed
     - [ ] hand off to code-review for M2
   - review closeout:
     - [ ] code-review completed
     - [ ] material findings resolved or explicitly dispositioned
     - [ ] M2 lifecycle projection updated before starting M3
   - milestone commit message:
     `M2: teach lifecycle skills the boundary-first contract`

### M3. Structural and activation validation

- Milestone state: planned
   - primary trust boundary: deterministic shape/reference enforcement without
     semantic overclaiming
   - deliverables:
     - add boundary-record and proof-map structural validation with exact
       headings, columns, vocabulary, identifiers, sentinels, and references;
     - reject unknown closed values before downstream consistency checks;
     - validate `specs/boundary-first-activation.yaml`, the authoritative spec
       state, grandfathered inventory membership, and both specified digests;
     - route changed grandfathered specs to `spec-review` without inferring
       whether a revision is substantive;
     - add positive, negative, unknown-value, stale-evidence, cross-feature ID,
       missing-proof, and semantic-omission fixtures;
     - integrate the new validators with repository-owned validation
       selection.
   - dependencies: M2 reviewed and closed
   - targeted validation:
     - `python scripts/test-boundary-first-validation.py`
     - `python scripts/validate-boundary-first.py --check`
     - `python scripts/test-select-validation.py`
   - recovery: remove selector routing and the new structural validators;
     leave the method and governed skills present but inactive.
   - implementation handoff:
     - [ ] targeted validation passed
     - [ ] hand off to code-review for M3
   - review closeout:
     - [ ] code-review completed
     - [ ] material findings resolved or explicitly dispositioned
     - [ ] M3 lifecycle projection updated before starting M4
   - milestone commit message:
     `M3: enforce boundary records and activation structure`

### M4. Package parity and prospective activation

- Milestone state: planned
   - primary trust boundary: one reviewed activation baseline across canonical,
     generated, packed, and installed surfaces
   - deliverables:
     - extend adapter and installed-tree tests to verify the reference path and
       raw bytes for Codex, Claude Code, and opencode;
     - generate and validate the complete grandfathered accepted-spec
       inventory and deterministic identities;
     - perform clean installed-skill cold-read proof for all ten governed
       skills on each supported target;
     - settle `specs/boundary-first-activation.yaml`, the proof-model spec
       activation state and record identity, generated surfaces, fixtures, and
       package evidence together;
     - prove rollback changes state coherently while preserving accepted
       marked artifacts and historical activation evidence;
     - update plan and change-local lifecycle evidence to the final
       explain-change handoff.
   - dependencies: M3 reviewed and closed
   - targeted validation:
     - `python scripts/test-adapter-distribution.py`
     - `python scripts/build-skills.py --check`
     - `python scripts/project-boundary-first-reference.py --check`
     - `python scripts/validate-boundary-first.py --check`
   - broad validation:
     - `bash scripts/ci.sh --mode broad-smoke`
   - recovery: set activation to `rolled-back` through the approved activation
     path, restore coherent inactive validator/skill behavior, preserve the
     accepted contract and activation history, and rerun package parity.
   - implementation handoff:
     - [ ] targeted and broad validation passed
     - [ ] installed cold-read evidence recorded
     - [ ] hand off to code-review for M4
   - review closeout:
     - [ ] code-review completed
     - [ ] material findings resolved or explicitly dispositioned
     - [ ] all in-scope implementation milestones closed
     - [ ] hand off to explain-change
   - milestone commit message:
     `M4: activate portable boundary-first skill capability`

## Sequencing and proof timing

| Evidence | First required | Final owner |
| --- | --- | --- |
| Reference byte/digest proof | M1 | code-review M1 |
| Stage-local semantic fixture behavior | M2 | code-review M2 |
| Boundary/proof shape and unknown-value failures | M3 | code-review M3 |
| Grandfathered inventory and activation-state coherence | M3 | code-review M4 |
| Generated, packed, and installed parity | M4 | verify |
| Contract-to-proof-to-implementation coherence | after explain-change | verify |

No later milestone may use an unreviewed earlier milestone as approval evidence.
A material review finding reopens its owning milestone and blocks the next one.

## Progress

- 2026-07-27: plan created from the accepted proposal, approved specs,
  approved architecture, accepted ADR, and closed upstream review findings.
- 2026-07-28: authored the boundary-first test spec after approved plan-review
  and repaired the coordinator defect that prevented its formal transition.
- 2026-07-28: test-spec-review R1 requested changes for incomplete normative
  traceability and conflicting broad-smoke ownership. Implementation remains
  blocked pending disposition, revision, and R2.
- 2026-07-28: revised the proof map with exact acceptance-criterion,
  edge-case, supplemental normative, privacy/readability, and command-owner
  mappings; PBF-TSR1 and PBF-TSR2 are pending R2 confirmation.
- 2026-07-28: test-spec-review R2 approved the revised proof map and allowed
  M1 implementation under separate implementation authority.
- 2026-07-28: implemented M1 with one authored method, a closed ten-consumer
  projection inventory, shared digest serialization, raw-byte write/check
  modes, and seven focused tests; handed M1 to code-review.

## Decision log

- 2026-07-27: split execution by four primary trust boundaries so the shared
  source, skill semantics, deterministic enforcement, and activation/package
  transaction can each close independently.
- 2026-07-27: keep activation in M4; earlier milestones remain recoverable
  while the repository state is `pending`.
- 2026-07-27: use dedicated projection and structural-validation commands so a
  mutating writer is not hidden inside ordinary validation.

## Surprises and discoveries

- 2026-07-27: the existing unified workflow coordinator cannot represent
  `plan-review` in its pre-plan canonical-position sequence and rejects the
  required `plan-review -> test-spec` transaction. The test spec was authored,
  but automated continuation stopped before recording that stage rather than
  bypassing the authority model or changing unrelated workflow-engine
  behavior. The run schema also prevents an arbitrary pause while its latest
  proposal-review projection is approved, so the valid persisted run remains
  active but no further transition is attempted.
- 2026-07-28: the coordinator defect was an implementation gap, not a contract
  gap. The canonical sequence and active-plan resolver now represent
  `plan-review -> test-spec -> test-spec-review`, with regression coverage for
  artifact resolution and an authorized test-spec transaction.

## Validation notes

- Upstream proposal-review, spec-review, and architecture-review findings are
  closed in the change-local review record.
- Plan-review R1 approved the milestone isolation, sequencing, recovery, and
  proof timing for test-spec authoring.
- `specs/boundary-first-proof-model.test.md` passed artifact-lifecycle and
  Markdown readability validation, and the repaired coordinator recorded its
  transition.
- Test-spec-review R1 recorded PBF-TSR1 and PBF-TSR2 and routed the workflow to
  review-resolution without granting implementation handoff.
- The accepted resolutions add stable direct proof for previously unmapped
  normative surfaces and split M4 versus final-verify broad-smoke ownership.
- Test-spec-review R2 found no additional material issue and confirmed that M1
  can begin without inventing proof obligations.
- M1's first read-only projection check failed on all ten missing consumers as
  expected. Write mode then produced ten byte-identical tracked projections,
  and the repeated check stabilized at one inventory identity.
- M1: `python scripts/test-boundary-first-reference.py` passed 7 tests.
- M1: `python scripts/project-boundary-first-reference.py --check` passed with
  10 consumers and projection identity
  `a764f05f5427e13ac69e44210fe6b006313afca0fa9d94135095358c64cec2d9`.
- M1: change metadata validation and scoped `git diff --check` passed.
- M1 aligned-surface audit: `SKILL.md` mappings are deferred to M2;
  structural/activation validation is deferred to M3; package/install parity
  is deferred to M4. These surfaces are unaffected by M1 with rationale.
- M2 through M4 implementation validation commands remain planned and have
  not run.

## Outcome and retrospective

- Pending implementation and final verification.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Shared-reference convenience could become hidden coupling; the projection
  inventory and byte-parity tests bound that risk.
- Structural validation could overclaim semantic completeness; semantic
  omission fixtures and stage ownership keep that boundary explicit.
- Activation could create mixed skill behavior; M4 blocks state settlement
  until all canonical, generated, packed, and installed surfaces agree.
- Historical specs could be misclassified; structural validation uses path
  membership while `spec-review` alone classifies substantive revisions.
