# Explain Change: Test-Spec Contract Normalization

## Summary

This change normalizes `skills/test-spec/SKILL.md` to the published-skill design contract without changing what the skill asks agents to produce. The skill now has reviewed frontmatter metadata, a `Workflow role`, visible `Stop conditions`, and a fenced `Output skeleton`.

The surrounding spec, test spec, validator fixtures, plan, and change-local evidence exist to prove that the normalization is structural only: the routing description, required test-spec sections, test-case format, coverage rules, stop conditions, and output obligations are preserved.

## Problem

The accepted proposal identified `test-spec` as behind the spec-family skill shape already used by `spec` and `spec-review`. It lacked:

- frontmatter `version` and `schema-version`;
- a `Workflow role` block;
- a fenced output skeleton;
- visible invocation stop conditions before normal artifact-generation guidance.

The proposal made behavior preservation the highest priority. The change would fail if any rule, stop condition, coverage rule, output obligation, lifecycle boundary, representative output shape, or routing behavior changed materially.

## Decision Trail

| Decision point | Decision | Source |
| --- | --- | --- |
| Proposal option | Normalize only; defer family-wide readability work. | `docs/proposals/2026-05-20-test-spec-contract-normalization.md` |
| Schema value | Use `schema-version: skill-readability-v1`. | `specs/skill-contract.md` `R29h`; plan M3 |
| Stop-condition shape | Use a dedicated `Stop conditions` section. | `specs/skill-contract.md` `R31e`; proposal implementation decisions |
| Proof route | Require a focused test-spec amendment before implementation. | plan M1; `specs/skill-contract.test.md` T37-T40 |
| Architecture | No architecture artifact needed. | active plan source artifacts and decision log |
| Implementation sequence | M1 proof obligations, M2 validator fixture support, M3 skill normalization. | active plan milestones |
| Review outcome | M2 and M3 code reviews were clean-with-notes with no material findings. | `reviews/code-review-m2-r1.md`, `reviews/code-review-m3-r1.md` |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `specs/skill-contract.md` | Added explicit normalized-skill metadata requirements, spec-family schema-version rule, visible stop-condition guidance, and output-skeleton preservation proof. | Proposal review found the contract needed an explicit proof route before implementation could rely on it. | Proposal findings TSCN-PR3 and TSCN-PR4; `R29g`, `R29h`, `R31e`, `R34c` | `spec-review-r1`; lifecycle validation |
| `specs/skill-contract.test.md` | Added T37-T40 covering proof scaffold, validator support, behavior-preserving skill rewrite, and generated-output validation. | The implementation needed concrete test-spec proof obligations before editing `skills/test-spec/SKILL.md`. | Plan M1; `R29g`, `R29h`, `R30`, `R30a`, `R31e`, `R34`, `R34c` | owner approval for focused test-spec amendment; lifecycle validation |
| `scripts/test-skill-validator.py` | Added regression tests for missing `version`, invalid `schema-version`, missing `Workflow role` field, and output skeleton without placeholders. | Existing validator logic already enforced these cases; the change added narrow regression coverage for M2. | Plan M2; T38 | `python scripts/test-skill-validator.py` passed with 132 tests |
| `tests/fixtures/skills/skill-readability/*/SKILL.md` | Added four negative readability fixtures for the validator tests. | Fixtures isolate each machine-checkable structural failure without semantic scoring. | Plan M2; T38 | `code-review-m2-r1` clean-with-notes |
| `skills/test-spec/SKILL.md` | Added `version: "1.0.0"`, `schema-version: skill-readability-v1`, `Workflow role`, `Stop conditions`, and `Output skeleton`; moved two stop-condition rules into the new section. | This is the core normalization target. The moved conditions and skeleton preserve existing behavior and output obligations. | Proposal goals; plan M3; T39 | `behavior-preservation.md`, `behavior-parity.md`, `code-review-m3-r1` |
| `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-preservation.md` | Recorded a source-to-destination preservation matrix. | Proposal review required durable proof for moved stop conditions and skeletonized output obligations. | TSCN-PR2; T37; T39 | M3 code-review inspected and accepted it |
| `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-parity.md` | Recorded representative structural parity for the proposal/spec/plan input. | The proposal invariant required no material output-shape change on a representative input. | T37; T39 | M3 code-review inspected and accepted it |
| `docs/proposals/2026-05-20-test-spec-contract-normalization.md` | Recorded the accepted direction, baseline audit, preservation proof requirements, amendment sequencing, and generated-output boundary. | Proposal-review R1 requested durable baseline and proof controls before planning. | TSCN-PR1 through TSCN-PR4 | `proposal-review-r2` approved |
| `docs/plans/2026-05-20-test-spec-contract-normalization.md` | Created and updated the living plan through M1, M2, M3, review closeout, and current handoff. | The initiative needed ordered proof planning, validator support, implementation, and handoff state. | Plan-review R1; code-review M2/M3 | plan validation and selected CI |
| `docs/plan.md` | Added the active plan entry and updated the current next stage. | Repository workflow requires the plan index to reflect active planned work. | AGENTS plan file policy; active plan | lifecycle validation |
| `docs/changes/2026-05-20-test-spec-contract-normalization/reviews/*.md` | Recorded proposal, spec, plan, and code reviews. | Formal lifecycle review evidence is required for material reviews and milestone handoff. | AGENTS review recording rules | review artifact validation |
| `docs/changes/2026-05-20-test-spec-contract-normalization/review-log.md` | Logged formal review entries and open-finding state. | Review discovery and closeout need durable indexing. | AGENTS review recording rules | review artifact validation |
| `docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md` | Closed four proposal-review R1 findings and summarized no-material later reviews. | Material findings needed dispositions before downstream reliance. | TSCN-PR1 through TSCN-PR4 | review artifact validation |
| `docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml` | Tracked requirements, tests, validation, changed files, and latest review. | Change-local metadata keeps lifecycle evidence discoverable. | AGENTS baseline change-local artifact pack | change metadata validation |

## Tests Added Or Changed

| Test ID or surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| T37 | The normalization target and proof scaffold are explicit before skill-body implementation. | Manual and integration proof is needed because preservation semantics cannot be fully validated by static structure. |
| T38 | Validator support covers machine-checkable metadata, schema, workflow-role, stop-condition, and skeleton expectations without broad semantic scoring. | Static validator regression tests are appropriate for structural fields. |
| T39 | The actual `test-spec` rewrite preserves stop conditions, required section set, test-case format, coverage maps, routing description, and output obligations. | Manual preservation and parity review is appropriate for behavior-significant moved prose. |
| T40 | Generated output is rebuilt or validated from canonical `skills/`, or an explicit deferral is recorded. | Adapter currency is an integration concern across canonical skills and generated archives. |
| `scripts/test-skill-validator.py` fixture tests | Missing metadata, wrong schema version, missing workflow-role field, and non-fillable output skeleton fail validation. | Unit-level fixture tests are narrow and deterministic. |

## Validation Evidence Available Before Final Verify

Key validation already recorded:

- `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed.
- `python scripts/validate-skills.py` passed for 23 skill files.
- `python scripts/test-skill-validator.py` passed with 132 tests.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.NBI6tpmMoX` built temporary adapter archives.
- `python scripts/validate-adapters.py --root /tmp/tmp.NBI6tpmMoX --version v0.1.5` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for touched lifecycle surfaces.
- `git diff --check -- ...` passed for touched skill, spec, plan, and change-local paths.
- `bash scripts/ci.sh --mode explicit ...` passed selected skill, generated-output, adapter, review-artifact, lifecycle, and change-metadata checks.

Known validation caveat:

- `python scripts/build-adapters.py --version v0.1.5 --check` failed against tracked expanded-tree adapter output. The plan and M3 review record treat this as stale baseline release-layout debt because current generated public adapter skill bodies are release archives, not tracked expanded trees. The current generated-output proof used temporary archive generation and `validate-adapters --root`.

This is not final verification. The `verify` stage still owns final coherence and readiness checks.

## Review Resolution Summary

Review resolution is closed in `docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md`.

- Material findings resolved: 4.
- Unresolved findings: 0.
- Dispositions: TSCN-PR1 through TSCN-PR4 accepted and resolved.
- Later reviews: proposal-review R2, spec-review R1, plan-review R1, code-review M2 R1, and code-review M3 R1 had no material findings.

## Alternatives Rejected

- Do nothing: rejected because `test-spec` would remain behind the published-skill design contract.
- Bundle normalization with readability work: rejected because tabulating prose lists and fencing enums is presentation work for a later family-wide readability pass.
- Implement immediately after proposal review: rejected because the proof route needed spec and test-spec amendments first.
- Add duplicate validator production logic: rejected because existing readability validator behavior already enforced the structural checks; M2 only needed regression fixtures.
- Hand-edit generated adapter skill bodies: rejected because canonical `skills/` remains the authored source and generated adapter bodies must not be hand-edited.

## Scope Control

Preserved non-goals:

- no `spec` or `spec-review` skill-body edits;
- no routing-description rewrite for `test-spec`;
- no tabulation of required-section prose;
- no enum fencing;
- no packaged `assets/`, `references/`, or `scripts/`;
- no legacy adapter archive rewrite;
- no change to test-spec output obligations, coverage rules, stop-condition semantics, or durable states.

## Risks And Follow-Ups

- Final `verify` still needs to confirm artifact-code-test coherence and lifecycle readiness.
- PR handoff remains incomplete until after verification.
- The tracked expanded-tree adapter `--check` baseline remains stale relative to the current archive-based public adapter surface; this change records the caveat and uses temporary archive validation, but does not solve the broader adapter-layout baseline.
- Follow-on readability work across `spec`, `spec-review`, and `test-spec` remains separate and should not be folded into this normalization change.

## Readiness

All implementation milestones are closed and code-reviewed. This explanation is the durable change rationale needed before final verification.

Next stage after this artifact is recorded: `verify`.
