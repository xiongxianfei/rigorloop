# Change Explanation: Portable Boundary-First Capability for Published Skills

## Summary

This change publishes one portable `boundary-first-v1` proof method through
the existing lifecycle skills. All ten governed skills read byte-identical
skill-local copies projected from one canonical reference. Feature specs own
normative boundaries, test specs map those exact boundaries to proof, and the
existing review stages retain semantic judgment.

The implementation deliberately reuses the repository's projection, skill
validation, adapter distribution, validation selection, and broad-smoke
surfaces. It does not add a standalone packaging command, activation or
rollback writer, receipt, transaction, installer, publication action,
attestation system, or runtime certification dependency.

## Problem

Examples can illustrate behavior without proving that a contract covers its
valid, invalid, stale, interrupted, composed, and adversarial boundaries. The
earlier runtime-certification direction tried to close that gap with
maintainer-only runtime machinery that published-skill users would not
receive. The accepted proposal instead makes the published instructions and
packaged reference the capability.

## Decision trail

| Decision level | Selected decision | Implementation consequence |
| --- | --- | --- |
| Proposal | Portable contract rather than examples alone, runtime certification, or per-adapter live evaluation | Published content is sufficient without a particular runtime or network service. |
| PBF-R001-PBF-R040 | Closed v1 dimensions, records, IDs, examples, interactions, and proof mappings | One canonical reference and structural record validator implement the portable grammar. |
| PBF-R041-PBF-R045 and PBF-R059-PBF-R064 | Ten governed lifecycle skills with distinct stage ownership | Each skill has one stage-specific `READ` mapping, responsibility, and stop rule. |
| PBF-R046-PBF-R051 | One source, deterministic projections, byte parity, and structural-only claims | Ten skill-local copies are projected; validators check shape and references without claiming semantic completeness. |
| PBF-R052-PBF-R058 | Prospective two-state activation and read-only package rollback readiness | One pending/active manifest and existing release metadata own activation and rollback selection. |
| PBF-R065 | No runtime, model, network, sandbox, interception, or attestation dependency | Cold-read package tests prove the method from installed skill contents alone. |
| Release-manifest ADR | Ordinary reviewed manifest change; source control and existing release metadata own identity | No custom activation or rollback transaction machinery was added. |
| Plan M1-M4 | Isolate source projection, stage behavior, structural enforcement, and package readiness | Each primary boundary received separate implementation evidence and independent code review. |

## Diff rationale by area

| Area | Change | Reason and governing source | Test or evidence |
| --- | --- | --- | --- |
| `specs/references/boundary-first-method-v1.md` and ten `skills/*/references/` projections | Added one complete portable method and byte-identical skill-local copies | PBF-R001-PBF-R040 and PBF-R046-PBF-R048 require a common, self-contained contract | T1-T3; `boundary-reference-evidence.yaml` |
| `scripts/boundary_first_reference.py` and existing projection entry point | Added the closed consumer inventory, safe path handling, deterministic digest, and check/write projection | The canonical source must project reproducibly without hand-maintained copies | 10 reference tests and projection check |
| Ten governed `SKILL.md` files | Added stage-specific `READ` mappings, responsibilities, and stop behavior | PBF-R041-PBF-R045 and PBF-R059-PBF-R064 keep semantic ownership with existing stages | T3, T6, T10, T16; four focused lifecycle tests |
| `scripts/skill_validation.py` and semantic fixtures | Allowed only the approved shared reference and proved exact owner/outcome/handoff behavior | Published skills must remain self-contained while validators avoid semantic-completeness claims | 263 skill-validator tests and 24-skill validation |
| `scripts/boundary_first_validation.py`, CLI, fixtures, and selector integration | Added closed feature/proof grammar, exact references, two-state activation, source-control baseline proof, and authoritative read-only rollback selection | PBF-R002-PBF-R040 and PBF-R049-PBF-R058 require fail-closed structure and prospective compatibility | T4-T9, T13, T15; 56 boundary tests and 134 selector tests |
| `scripts/adapter_distribution.py` and its existing test suite | Preserved mapped resources through supported archives and clean local installs; made installed skill files part of the cold read | PBF-R046-PBF-R048 and PBF-R065 require portable packaged bytes without repository or network lookup | T11, T12, T14; 2 focused and 133 full adapter tests |
| `specs/boundary-first-activation.yaml` and change-local evidence | Recorded pending release state and implementation evidence | Activation must remain pending until a real reviewed release transition provides immutable tags | Activation, validation, and install evidence files |
| Proposal, specs, architecture, ADR, plan, and review records | Closed vocabulary, ownership, rollout, proof, sequencing, and review decisions before implementation | The contract and rationale must remain auditable outside chat | Approved lifecycle artifacts; 45 formal review entries |

The workflow-coordinator correction encountered during execution is governed
by its own bugfix change. This explanation does not treat that unrelated
implementation as part of the boundary-first product diff.

## Tests added or changed

| Test IDs | What they prove | Why this level is appropriate |
| --- | --- | --- |
| T1-T2 | Canonical content, exact ten-consumer projection, raw-byte identity, idempotency, drift, and path containment | Unit tests isolate the deterministic source/projection boundary. |
| T3, T6, T10, T16-T17 | Exact stage mappings, semantic owners, stop outcomes, handoffs, readability, and privacy-bounded diagnostics | Integration fixtures exercise published skill behavior without pretending a structural parser can judge semantics. |
| T4-T9, T15 | Closed boundary/proof grammar, fail-closed vocabularies, activation history, grandfathering, and validation selection | Repository integration tests are needed for cross-record and source-control behavior. |
| T11-T12, T14 | Canonical/generated/archive/install parity and offline skill-local cold reads for all 28 adapter-included governed pairs | Archive and clean-install tests prove the actual user-visible package boundary. |
| T13 | Fixed-authority rollback release selection, complete metadata matrix, containment, and non-mutation | Integration proof is appropriate because the behavior composes the activation manifest with existing release metadata. |

## Validation evidence available before final verify

| Command | Latest pre-verify result |
| --- | --- |
| `python scripts/test-boundary-first-reference.py` | pass; 10 tests |
| `python scripts/project-boundary-first-reference.py --check` | pass; 10 consumers |
| `python scripts/validate-skills.py` | pass; 24 skills |
| `python scripts/test-skill-validator.py` | pass; 263 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/test-boundary-first-validation.py` | pass; 56 tests |
| `python scripts/validate-boundary-first.py --check` | pass; pending manifest |
| `python scripts/test-select-validation.py` | pass; 134 tests |
| `python scripts/test-adapter-distribution.py -k boundary_first` | pass; 2 tests |
| `python scripts/test-adapter-distribution.py` | pass; 133 tests |
| `bash scripts/ci.sh --mode broad-smoke` | pass; 12 checks |

These results are implementation and review evidence. Final verification has
not yet been claimed and must rerun its owned commands.

## Review resolution summary

The lifecycle recorded 64 material findings: 62 were accepted and resolved,
and two were deferred from M3 to their explicit M4 owner and then resolved.
There are no open findings or `needs-decision` dispositions. The final M4 R2
review was clean-with-notes from two independent reviewers.

The detailed dispositions remain in
[`review-resolution.md`](review-resolution.md); this explanation does not
duplicate the review transcripts.

## Alternatives rejected

- Examples alone were rejected because they do not establish completeness.
- Runtime certification and immutable runtime evidence were rejected because
  they are not portable published-skill capabilities.
- Ten hand-maintained reference copies were rejected because they drift.
- A repository-root-only shared file was rejected because installed skills
  must be self-contained.
- Cartesian interaction generation was rejected in favor of hazard-selected
  interactions.
- Activation and rollback writers, receipts, and transactions were rejected
  because an ordinary reviewed manifest, source control, and existing release
  metadata already own the required evidence.
- A new packaging test script was rejected; M4 extends the existing adapter
  distribution suite.

## Scope control

The repository activation state remains `pending`. This change performs no
release, publication, external installation, or historical-spec migration.
It does not create a new lifecycle stage, add proposal-stage boundary
authoring, infer semantic completeness in validators, require all interaction
products, or alter existing adapter portability decisions.

## Risks and follow-ups

- A future release activation must be one reviewed manifest change with
  immutable activating and immediately preceding rollback tags.
- Existing accepted historical feature specs remain valid until a substantive
  revision; `spec-review` owns that semantic classification.
- The ten projections can drift only if repository checks are bypassed; final
  verify must confirm projection, generated, packed, and installed parity.
- External rollback remains an authorized release-operator action. This
  capability only proves that the selected prior package set is complete.

All implementation milestones and their code reviews are closed. The change
is ready for final verify, but this artifact does not claim verification or PR
readiness.
