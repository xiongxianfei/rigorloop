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
  `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`
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
- One reviewed release-activation manifest and deterministic grandfathered
  path inventory derived from its immutable parent revision.
- Generated, packed, and installed parity proof for Codex, Claude Code, and
  opencode.
- Review fixtures that distinguish structural validity from semantic
  completeness.
- Coherent release readiness across the contract, activation manifest,
  governed skills, validators, package evidence, and plan state.

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

- Current milestone: M4. Package parity and prospective activation
- Current milestone state: closed
- Latest review evidence: code-review M4 R2 is clean-with-notes; two independent reviewers confirmed PBF-M4-CR1 and PBF-M4-CR2 resolved
- Last reviewed milestone: M4
- Review status: clean-with-notes; stage=code-review; round=r2
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: explain-change-pending, verify-pending — review-state=closed; open-count=0; open-findings=none

## Milestones

### M1. Canonical reference and projection foundation

- Milestone state: closed
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
     - [x] code-review completed
     - [x] material findings resolved or explicitly dispositioned
     - [x] M1 lifecycle projection updated before starting M2
   - milestone commit message:
     `M1: add deterministic boundary reference projection`

### M2. Governed lifecycle skill behavior

- Milestone state: closed
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
     - [x] targeted validation passed
     - [x] hand off to code-review for M2
   - review closeout:
     - [x] code-review completed
     - [x] material findings resolved or explicitly dispositioned
     - [x] M2 lifecycle projection updated before starting M3
   - milestone commit message:
     `M2: teach lifecycle skills the boundary-first contract`

### M3. Structural and activation validation

- Milestone state: closed
   - primary trust boundary: deterministic shape/reference enforcement without
     semantic overclaiming
   - deliverables:
     - add boundary-record and proof-map structural validation with exact
       headings, columns, vocabulary, identifiers, sentinels, and references;
     - reject unknown closed values before downstream consistency checks;
     - replace the superseded three-state activation schema with the closed
       `pending` and `active` release-manifest fields;
     - validate immutable activating and rollback release tags, the full
       parent-revision baseline, and the sorted eligible path inventory;
     - retain existing boundary-record, proof-map, projection, containment,
       diagnostic, and selector behavior that remains governed;
     - remove rollback receipt, writer, historical-hash, and repository
       rollback-state behavior and tests;
     - validate rollback manifest and adapter-matrix schema behavior with
       isolated fixtures, including missing, additional, duplicated, failing,
       and mixed-version entries;
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
     - [x] targeted validation passed
     - [x] hand off to code-review for M3
   - review closeout:
     - [x] code-review completed
     - [x] material findings resolved or explicitly dispositioned
     - [x] M3 lifecycle projection updated before starting M4
   - milestone commit message:
     `M3: enforce boundary records and activation structure`

### M4. Package parity and prospective activation

- Milestone state: closed
   - primary trust boundary: release readiness across canonical, generated,
     packed, and installed skill surfaces
   - deliverables:
     - extend adapter and installed-tree tests to verify the reference path and
       raw bytes for Codex, Claude Code, and opencode;
     - prove the reviewed pending manifest and active fixtures use the exact
       release, baseline, and path-inventory contract;
     - perform clean installed-skill cold-read proof for every governed skill
       included by each supported adapter, inspect all three target trees, and
       leave inclusion and exclusion validity with the existing adapter
       portability evaluation and CMD9;
     - prove existing release metadata supports read-only rollback selection
       for every current adapter;
     - keep repository activation `pending` until a real reviewed release
       change can provide immutable activating and rollback release tags;
     - do not add an activation writer, rollback writer, receipt, transaction,
       attestation store, or external release action;
     - update plan and change-local lifecycle evidence to the final
       explain-change handoff.
   - dependencies: M3 reviewed and closed
   - targeted validation:
     - `python scripts/test-adapter-distribution.py`
     - `python scripts/build-skills.py --check`
     - `python scripts/project-boundary-first-reference.py --check`
     - `python scripts/validate-boundary-first.py --check`
     - `python scripts/test-boundary-first-validation.py -k active_rollback_release_matches_current_adapter_metadata`
   - broad validation:
     - `bash scripts/ci.sh --mode broad-smoke`
   - recovery: retain or restore the reviewed pending manifest and remove only
     incomplete package-readiness evidence. External package installation or
     publication remains outside this plan.
   - implementation handoff:
     - [x] targeted and broad validation passed
     - [x] installed cold-read evidence recorded
     - [x] hand off to code-review for M4
   - review closeout:
     - [x] code-review completed
     - [x] material findings resolved or explicitly dispositioned
     - [x] all in-scope implementation milestones closed
     - [x] hand off to explain-change
   - milestone commit message:
     `M4: prove portable boundary-first release readiness`

## Sequencing and proof timing

| Evidence | First required | Final owner |
| --- | --- | --- |
| Reference byte/digest proof | M1 | code-review M1 |
| Stage-local semantic fixture behavior | M2 | code-review M2 |
| Boundary/proof shape and unknown-value failures | M3 | code-review M3 |
| Grandfathered inventory and activation-state coherence | M3 | code-review M4 |
| Active rollback-release selection against current adapter metadata | M4 | code-review M4 |
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
- 2026-07-28: implemented M2 with one stage-specific `READ` mapping for each
  governed skill, stage-owned semantic responsibilities and stop behavior,
  semantic-gap routing fixtures, and a narrow validator exception for the
  approved shared reference; all targeted checks passed and M2 was handed to
  code-review.
- 2026-07-28: code-review M2 R1 recorded PBF-M2-CR1 because the semantic
  fixture proved prose presence rather than lifecycle behavior. The accepted
  declared-safe correction now supplies exact ten-stage packets, semantic
  owners, outcomes, handoffs, and negative mutation proof; M2 returned to R2.
- 2026-07-28: implemented M3 structural feature/proof validation, pending
  activation-baseline validation, grandfathered-spec review routing, durable
  positive and failure fixtures, privacy-bounded diagnostics, and selector
  integration; handed M3 to code-review after all targeted commands passed.
- 2026-07-28: code-review M3 R1 requested changes for Markdown context and
  marker placement, bounded malformed-input handling, direct projection
  parity, shared feature/test activation gating, historical membership,
  changed-path containment, diagnostic redaction, and clean-commit selector
  reproducibility. M4 remains blocked pending correction and R2.
- 2026-07-28: resolved PBF-M3-CR1 through PBF-M3-CR8 with 39 focused
  regressions, direct canonical projection checks, exact active historical
  membership, contained and redacted diagnostics, shared feature/test
  activation gating, and committed coordinator baseline `197d150b`; M3
  returned to independent R2.
- 2026-07-28: code-review M3 R2 confirmed CR1-CR8 resolved and recorded
  PBF-M3-CR9 through PBF-M3-CR13 for historical adoption/rollback
  preservation, companion and inventory containment, aligned separators, and
  deleted proof-map handling. M3 entered correction cycle 2.
- 2026-07-28: resolved PBF-M3-CR9 through PBF-M3-CR13 with 44 focused
  regressions covering adoption and rollback history, explicit and derived
  containment, aligned separators, deletion handling, and historical
  inventory symlinks; M3 returned to independent R3.
- 2026-07-28: code-review M3 R3 confirmed CR9-CR13 resolved and recorded
  PBF-M3-CR14 and PBF-M3-CR15 for new adoption after rollback and external
  symlinks on fixed authoritative inputs. M3 entered correction cycle 3.
- 2026-07-28: resolved PBF-M3-CR14 and PBF-M3-CR15 with a closed rollback
  path-and-byte inventory, fixed-authority containment, and 47 focused tests;
  M3 returned to independent R4.
- 2026-07-28: code-review M3 R4 confirmed fixed-authority containment but
  showed that the rollback inventory can be recomputed from current files and
  omits accepted proof-map identities. PBF-M3-CR14 remains open and
  PBF-M3-CR16 is new. All three authorized M3 correction cycles are consumed,
  so the workflow paused for renewed authority and an upstream trust-owner
  decision.
- 2026-07-28: the user authorized one additional M3 correction cycle and
  selected the M4 rollback transaction receipt as the pre-transition evidence
  owner with paired feature-spec and proof-map identities. M3 correction
  cycle 4 began.
- 2026-07-28: correction cycle 4 removed current-state rollback
  self-authorization. M3 reserves the M4 receipt binding and fails every
  rolled-back state and marker closed; M4 owns pre-transition provenance and
  paired feature/proof validation. All 48 focused tests, pending activation
  validation, and 134 selector tests pass; M3 returned to R5.
- 2026-07-28: code-review M3 R5 confirmed the fail-closed M3 boundary but
  recorded PBF-M3-CR17 because CMD12 excludes the receipt and no other command
  owns M4 rollback mutation, recovery, or validation. The fourth correction
  cycle is consumed; workflow paused for a command-owner decision and renewed
  authority.
- 2026-07-28: the user rejected the transaction-heavy rollback direction and
  restored the accepted proposal boundary. The draft contract now uses only
  `pending` and `active`, settles activation through an ordinary reviewed
  release-manifest change, and defines rollback as reinstalling or
  republishing the previous immutable skill package. Receipt, writer,
  repository rollback-state, and attestation requirements are removed.
  Downstream test-spec, architecture, plan, and implementation surfaces are
  stale until their owning stages align after spec-review R3.
- 2026-07-28: spec-review R5 and architecture-review R4 approved the
  release-manifest design. This plan revision resets M3 to planned, removes
  receipt/writer/rolled-back work, and limits M4 to package and release
  readiness while activation remains pending for a real release change.

## Decision log

- 2026-07-27: split execution by four primary trust boundaries so the shared
  source, skill semantics, deterministic enforcement, and package readiness
  can each close independently.
- 2026-07-27: keep activation in M4; earlier milestones remain recoverable
  while the repository state is `pending`.
- 2026-07-27: use the existing projection command and read-only structural
  validation; activation remains an ordinary reviewed release-manifest edit.
- 2026-07-28: keep activation metadata declarative and reviewed; do not add
  activation or rollback mutation commands. Operational rollback belongs to
  immutable package release selection.

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
- M2: `python scripts/validate-skills.py`,
  `python scripts/test-skill-validator.py`, and
  `python scripts/build-skills.py --check` passed after PBF-M2-CR1; the suite
  now contains 263 tests and four focused boundary-first lifecycle tests.
- Historical M3 validation passed 48 focused tests and 134 selector tests, but
  its activation and rollback assertions are invalidated by the approved
  two-state release-manifest contract and must be replaced before reliance.
- M4 targeted validation passed 56 boundary tests, 133 adapter tests, two
  focused package/install tests, and the 12-check broad-smoke suite.
- Code-review M4 R2 was clean-with-notes from two independent reviewers and
  closed all in-scope implementation milestones without adding a writer,
  receipt, transaction, publication action, runtime certification, or
  standalone support script.

## Outcome and retrospective

- Pending implementation and final verification.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Shared-reference convenience could become hidden coupling; the projection
  inventory and byte-parity tests bound that risk.
- Structural validation could overclaim semantic completeness; semantic
  omission fixtures and stage ownership keep that boundary explicit.
- Activation could create mixed skill behavior; M4 proves release readiness,
  while the later reviewed release change remains responsible for changing the
  manifest from `pending` to `active`.
- Historical specs could be misclassified; structural validation uses path
  membership while `spec-review` alone classifies substantive revisions.
