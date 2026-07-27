# Explain Change: Boundary-First Proof Modeling for Published Lifecycle Skills

| Field | Value |
| --- | --- |
| Change ID | `2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` |
| Stage | `explain-change` |
| Recorded | `2026-07-27` |
| Status | `current` |
| Reviewed diff | `f4c9354e..282550ef` |
| Final diff identity | `sha256:c923cf2e942ab2075cfcfa11d0f396029db60ff717bb4bc6f69b293b6aacd4a1` |
| Final review identity | `sha256:1e1e57a4460a0f8fffe2a27cf676975120c3d3c524786ce473b8fd0164b65a2c` |
| Final verify | Not claimed |
| PR readiness | Not claimed |

## Summary

This change makes lifecycle proof boundary-first rather than example-first.

Examples remain useful demonstrations and regressions, but they no longer define completeness.
Behavior-changing work now identifies the governing rule, applicable boundary dimensions, valid and invalid partitions or transitions, important interactions, and direct proof obligations before implementation handoff.

The first release projects that contract through eight published lifecycle skills:

- `spec`;
- `spec-review`;
- `test-spec`;
- `test-spec-review`;
- `implement`;
- `code-review`;
- `verify`;
- `workflow`.

The implementation adds a typed deterministic model, fail-closed validation, a standalone hermetic behavior harness, immutable recovery evidence, downstream behavior-preservation proof, adapter parity, deterministic changed-path routing, and a reconstructed capability report.
It does not activate a release, publish an adapter, open a PR, or resume the paused progressive-disclosure initiative.

## Problem

The preceding single bounded review-fix automation initiative accumulated 104 material findings, including 82 implementation code-review findings.
The accepted proposal found a repeated root cause: examples were implemented without first closing the surrounding trust, identity, authority, state, transaction, recovery, compatibility, and composition boundaries.

That produced recurring escape shapes:

- caller-provided evidence was trusted instead of canonical state;
- shape checks passed records whose semantics or cross-record relationships were invalid;
- one reported example was fixed while sibling bypasses remained;
- helper-level proof passed while the composed public path failed;
- success paths existed without interruption and reconciliation proof; and
- narrow fixtures stood in for closed vocabularies or transition matrices.

The intended transformation is now explicit:

```text example
-> governing rule
-> applicable boundary dimensions
-> partitions, transitions, and invariants
-> hazard-selected interactions
-> executable proof obligations ```

## Decision Trail

### Proposal decision

The accepted proposal selected Option 4: embed boundary-first modeling in the existing lifecycle owners.

It rejected relying on code review alone, adding only a longer checklist, requiring a new universal boundary artifact, and generating tests directly from examples.
The selected direction keeps normative behavior in feature specs, proof mapping in test specs, semantic sufficiency in independent review, and stable closed-shape checks in validators.

### Requirements

The implementation follows two approved requirement families:

- `specs/rigorloop-workflow.md` `R28` through `R28z` own lifecycle boundary records, behavior evidence, adoption, aggregation, and resumption gates.
- `specs/skill-contract.md` `R56` through `R56q` own the portable eight-skill projection and packaged-resource contract.

The key contract decisions are:

- examples are subordinate evidence rather than coverage owners;
- the mandatory core dimension vocabulary is closed;
- feature-specific extensions use namespaced identities;
- complete partition or transition coverage is distinct from hazard-selected interaction coverage;
- validators own stable shape, vocabulary, identity, and traceability checks;
- reviewers retain semantic completeness judgment;
- sibling-boundary analysis is required after a material escape;
- accepted historical work remains valid;
- activation is prospective and all-or-nothing; and
- progressive disclosure cannot resume from a partial baseline.

### Architecture and ADRs

`ADR-20260725-boundary-first-proof-modeling` places normative semantics in the approved specs and uses immutable Python projections for execution.

The accepted follow-on ADRs close the runtime trust boundary:

- `ADR-20260726-codex-permission-profile-boundary-harness` binds behavior generation to an exact runtime and read-only sandbox evidence.
- `ADR-20260726-stage-authored-artifact-envelope-transport` keeps stages as semantic authors while a parent materializes reviewed bytes after workspace integrity proof.
- `ADR-20260727-capability-projected-file-change-control` binds enforcement to the exact executable capability projection.
- `ADR-20260727-three-category-runtime-feature-projection` separates permitted commands, permitted non-tool runtime behavior, and required-disabled tool-bearing features.

The architecture preserves four ownership boundaries:

1. specs own normative meaning;
2. typed modules own deterministic projection and comparison;
3. the standalone harness owns one bounded nondeterministic observation and
   immutable publication transaction; and
4. independent reviews own semantic adequacy and preservation decisions.

### Plan milestones

| Milestone | Purpose | Closeout |
| --- | --- | --- |
| M1 | Typed records, closed vocabularies, incident fixtures, synthetic trace, and report primitives | Closed after deterministic and negative proof |
| M2 | Runtime feasibility, hermetic harness, recovery transaction, upstream skill behavior, and fresh immutable evidence | Closed after thirteen implementation review rounds |
| M3 | Downstream skill projection and 40-pair preservation proof | Closed after structural claims were separated from semantic review |
| M4 | Selector routing, adapter parity, capability aggregation, activation/rollback proof, and final integration | Closed after public-CI composition and scheduling correction |
| M5 | Verification routing and lifecycle synchronization correction | Closed after bounded nested-evidence routing, actual PR-range proof, and independent review |

Final holistic code review R3 approved the complete cross-milestone diff after
M5.
The active plan therefore has no remaining implementation milestone.

## Diff Rationale by Area

| Area and representative files | Change | Why | Source | Proof |
| --- | --- | --- | --- | --- |
| `specs/rigorloop-workflow.md`, `specs/skill-contract.md` | Added the boundary model, ownership, adoption, runtime evidence, aggregation, and portability contracts. | Make the state space and its owner explicit before code exists. | Proposal Option 4; `R28-R28z`; `R56-R56q`. | Matching test specs and spec reviews R1-R58. |
| `specs/rigorloop-workflow.test.md`, `specs/skill-contract.test.md` | Added traceable proof maps for records, incidents, harness inputs, recovery, fresh behavior, preservation, parity, activation, and rollback. | Convert each normative boundary into direct, deterministic, or bounded manual proof. | Test cases `T46-T54` and portable skill-contract proof. | Test-spec reviews R1-R27. |
| `docs/architecture/system/architecture.md`, boundary C4 diagrams, five ADRs | Defined component ownership, runtime trust boundaries, transport, publication, recovery, and capability projection. | Prevent the harness, validator, or parent adapter from silently owning lifecycle semantics or child authority. | Accepted architecture and ADR decisions. | Architecture reviews R1-R30. |
| `scripts/boundary_proof_model.py` | Added frozen records, closed enums, identity calculation, pure invariants, operation results, and report reconstruction. | Give deterministic properties one immutable executable projection without making code normative. | `R28-R28e`, `R28k`, `R28s-R28y`. | M1 tests and reconstruction contrasts. |
| `scripts/validate-boundary-proof.py` | Added validation and sole-writer report commands. | Reject unknown values and stale or asserted report rows before consistency or pass calculation. | Architecture sole-writer decision; `R28y`. | `generate-report`, `validate-report`, and mutation tests. |
| `scripts/boundary_proof_behavior.py` | Added the standalone runtime preflight, isolated lifecycle invocation, stage envelope transport, immutable publication, recovery, and preservation commands. | Observe real published-skill behavior without allowing the observed system to define or mutate its own proof boundary. | Harness, transport, file-change, and feature-projection ADRs. | M2 `T48-T52` and M3 `T53`. |
| `tests/fixtures/boundary-proof/` | Added the exact incident registry, compact simple-change scenario, behavior, transport, activation, and rollback fixtures. | Prove closed boundary classes and contrasts while keeping examples subordinate. | `R28k`, `R28q-R28y`. | Incident replay, false-blocking, recovery, and release tests. |
| `skills/*/SKILL.md`, `skills/*/references/boundary-proof-model.md`, `templates/shared/boundary-proof-model.md` | Added stage-local responsibilities and byte-identical on-demand reference material for the eight governed skills. | Make the capability portable and self-contained without duplicating eight normative contracts. | `R56-R56q`; packaged-resource architecture. | Skill validation, 261 skill tests, drift checks, 40 preservation pairs. |
| `scripts/skill_validation.py`, adapter distribution and tests | Added resource mapping, identity, packaging, and four-surface parity checks. | Ensure canonical, generated, packed, and installed skills expose the same capability. | `R56n`, `R56q`, M4. | Adapter 132 tests and fresh v0.1.5 candidate archive validation. |
| `scripts/validation_selection.py`, `scripts/test-select-validation.py` | Registered six boundary check IDs, classified governed inputs, made shared-state suites sequential-only, and made change-evidence matching honor bounded full roots and explicit descendant patterns. | Prove the composed public validation path and route nested durable evidence without accepting unrelated siblings. | `R28p`, CRM-R1-R19, M4-M5, `BFP-CR-FINAL-1`. | 142 selector tests, complete tracked-evidence inventory, and actual `origin/main..c015ff96` PR selection. |
| Release transaction tests and fixtures | Added complete activation, partial-activation rejection, and rollback behavior without changing published release state. | Prove prospective all-or-nothing adoption and safe rollback. | `R28l-R28o`, `R28z`, `T47`, `T54`. | 87 release-transaction tests. |
| Change-local immutable runs, recovery decisions, preservation snapshots, parity manifests, and capability report | Recorded exact inputs, outputs, interruptions, quarantine decisions, current pointers, and reconstructed results. | Preserve auditability and resume safety without treating chat or generated summaries as authority. | `R28y`, publication/recovery ADRs, M2-M4. | Current run, 40 preservation pairs, four parity manifests, capability report. |

The reviewed range contains 692 files and about 94,000 added lines.
Most of that volume is immutable behavior, recovery, before/after, and formal review evidence.
The primary authored runtime surface is concentrated in the boundary model, behavior harness, validator, selector, skill projections, contracts, and fixtures listed above.

## Tests Added or Changed

### `T46-T47`: aggregation and lifecycle boundary

- `T46` proves the capability report is computed from a closed operation graph and current evidence rather than asserted rows.
- `T47` keeps report pass, activation, rollback, final verification, and progressive-disclosure resumption as distinct decisions.

These are integration and contract tests because the risk is cross-artifact composition rather than one helper.

### `T48-T52`: hermetic behavior and recovery

- `T48` closes every manifest and executable input.
- `T49` proves import, runtime, configuration, tool, permission, credential, and network boundaries fail closed before lifecycle output is accepted.
- `T50` binds fresh generation to the exact immutable input set and runtime attestation.
- `T51` crashes and resumes every durable publication and recovery boundary.
- `T52` proves stage-owned authoring, independent review, bounded correction, owner-decision stops, request-only child input, and post-observation outcome comparison.

These tests combine pure model contrasts with isolated runtime integration because neither level alone proves the trust boundary.

### `T53-T54`: preservation and portability

- `T53` validates the complete eight-skill by five-category preservation inventory without reinvoking upstream behavior.
- `T54` proves raw-byte parity across canonical, generated, packed, and installed adapters and exercises activation/rollback evidence.

Semantic preservation remains reviewer-owned.
The harness reports `structural-pass`; final semantic decisions are recorded by code review rather than generated by the same tool that produced the bytes.

### Selector and fail-closed regressions

Selector tests prove:

- every governed boundary script and fixture has deterministic routing;
- all six `R28p` check IDs are selected;
- release fixtures retain release-transaction proof;
- unrelated unsupported scripts still block; and
- three aliases of the shared publisher-state suite cannot run concurrently.

The M5 selector contrasts additionally prove:

- safe nested roots are accepted while traversal, non-change roots, and
  unbounded roots are rejected;
- basename patterns remain immediate and recurse only through an explicit
  descendant pattern;
- unknown evidence siblings still produce `manual-routing-required`;
- the initiative-specific routes do not capture another change; and
- all tracked boundary evidence routes exactly once with no registration debt.

Closed-vocabulary tests cover unknown values directly, so consistency checks cannot silently skip unrecognized states.

## Validation Evidence Available Before Final Verify

The following evidence passed before this explanation:

| Command or evidence | Result |
| --- | --- |
| `python scripts/test-boundary-proof.py` | pass; 115 tests in the M4 baseline |
| `python scripts/test-select-validation.py` | pass; 142 tests after M5 |
| `python scripts/test-adapter-distribution.py` | pass; 132 tests |
| `python scripts/test-release-transaction.py` | pass; 87 tests |
| `python scripts/test-skill-validator.py` | pass; 261 tests |
| `python scripts/validate-skills.py` | pass; 24 skills |
| `python scripts/build-skills.py --check` | pass |
| Fresh v0.1.5 adapter build and validation | pass; three candidate archives |
| Current behavior run | pass; `run-62735d2bff6ab29bfe208183cf33fc03` |
| Current preservation run | structural pass; 40 pairs; zero upstream reinvocations |
| Capability report reconstruction | pass after M5; `sha256:eee559b1ce85878a3ba5891a35ef9305b705fde721ab2f09131400806e255632` |
| Exact plan-owned selected CI | pass; 14 selected checks |
| `python scripts/select-validation.py --mode pr --base origin/main --head HEAD` | pass at `c015ff96`; status `ok`, no blockers, no registration debt, broad smoke not required |
| Review artifact structure validation | pass after final R3; 167 reviews and 185 findings |
| Change metadata and lifecycle validation | pass, with existing merge-language warnings only |
| `git diff --check` | pass |

The first exact selected-CI execution was not discarded as a flake.
It exposed unsupported boundary script classifications, unclassified fixtures, unsafe parallel scheduling of a shared-state suite, and a stale report after selector changes.
The second run passed only after direct regressions, sequential-only safety metadata, current report regeneration, and independent reconstruction.

This is pre-final-verify evidence.
It does not claim hosted CI success, branch readiness, PR readiness, release readiness, or final verification.

## Review Resolution Summary

The detailed review ledger contains:

- 185 material findings;
- 185 accepted and resolved dispositions;
- zero rejected, deferred, partially accepted, or `needs-decision` dispositions; and
- zero open findings.

Final holistic review R3 introduced no new material finding.
It confirmed final R2 remains valid for the unchanged M1-M4 implementation and
that M5 closes the verification-discovered routing debt without widening
semantic validation or scope.

See [review-resolution.md](review-resolution.md) and
[code-review-final-r3.md](reviews/code-review-final-r3.md).

The scan-first prose summary near the top of `review-resolution.md` still contains historical intermediate counts.
The validator-derived detailed ledger and current `change.yaml` metadata own the current 185/185 closeout count.
Normalizing that presentation is a lifecycle-documentation cleanup, not a change to any disposition.

## Alternatives Rejected

- Keep examples and rely on code review: rejected because omission discovery remains late and remediation stays example-local.
- Add only a longer checklist: rejected because a generic list does not derive the feature-specific state space.
- Require a standalone boundary artifact for every change: rejected because it duplicates spec and test-spec ownership and creates ceremony.
- Generate tests from examples: rejected because generated proof inherits the same blind spots.
- Let validators score semantic completeness: rejected because applicability, meaningful partitions, hazards, and sufficiency require independent judgment.
- Reuse the workflow automation engine as the behavior harness: rejected because the proof would depend on the dynamic mechanism it observes.
- Run lifecycle skills in the parent process or grant child workspace writes: rejected because caller context and mutation authority would become unbound inputs.
- Adopt orphaned output after interruption: rejected because incomplete nondeterministic work cannot become current authority.
- Resume progressive disclosure before the complete baseline: rejected because context optimization must preserve a proven capability, not a partial one.

## Scope Control

The change preserves these boundaries:

- no new lifecycle stage or universal boundary artifact;
- no alternate “light” workflow lane;
- no exhaustive Cartesian-product requirement;
- no validator-owned semantic judgment;
- no retroactive invalidation of accepted historical artifacts;
- no reopening of the single bounded review-fix automation direction;
- no progressive-disclosure implementation or activation;
- no public release marker;
- no publication, deployment, PR opening, merge, or destructive Git action;
- no rewriting of historical published adapter evidence; and
- no claim that material-finding count alone measures quality.

## Risks and Follow-ups

- The behavior harness is intentionally bound to a reviewed Codex runtime projection. A different executable or feature inventory stops as `environment-unavailable` until separately reviewed; it does not fall back by version label alone.
- Nondeterministic lifecycle generation has real runtime and model cost. Validation reuses immutable evidence and does not reinvoke skills.
- The change-local evidence set is large because failed attempts and recovery decisions are preserved. Future compaction must retain identity and audit guarantees.
- The `review-resolution.md` scan-first summary has stale historical counts, although the detailed ledger, metadata validator, and closeout validator agree on 185 resolved findings.
- The unified automation verification handoff currently has a separate implementation gap: automatic `explain-change` requires verification capability while verification readiness expects current explanation evidence. This direct invocation records the explanation but does not repair or resume that mechanism.
- Capability-preserving progressive disclosure remains paused. Resumption requires final verification plus a separate explicit decision; a passing capability report alone is insufficient.
- The selector registry now contains exact initiative-specific evidence
  registrations because the existing semantic checks are initiative-specific.
  A future reusable evidence family should receive its own reviewed generic
  contract rather than broadening these roots.

## Readiness Statement

All five implementation milestones are closed, all material review findings
are resolved, and final holistic code review R3 is approved.

This explanation is current through the final reviewed M5 correction.
It does not itself run final verification or claim branch or PR readiness.
