# Final Holistic Code Review R1

Review ID: code-review-final-r1

Stage: code-review

Round: 1

Reviewer: Codex code-review skill

Target: complete boundary-first proof modeling initiative through `12beb1df`

Reviewed artifact: implementation diff `f4c9354e..12beb1df`

Reviewed milestone: M1-M4 and final cross-milestone composition

Review scope: final-holistic

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-FINAL-1

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-initiative-implementation

Reviewer context ID: boundary-final-review-r1-reset

Context separation mechanism: initiative-base diff and selected-CI execution
before validation summaries, milestone conclusions, or prior finding content

Risk tier: elevated

Risk-tier triggers: cross-milestone integration, validation routing, generated
evidence, public skills, adapter portability, immutable runtime evidence, and
release non-activation

Risk-tier classifier: integration, generated-evidence, requirement-fidelity,
release, security-boundary, and validation triggers

Governing artifacts: accepted proposal; `specs/rigorloop-workflow.md`
R28-R28z; `specs/skill-contract.md` R56-R56q; matching test specs; accepted
boundary architecture and ADRs; active M1-M4 plan

Formal criteria: complete cross-milestone composition, current generated
evidence, exact selected-check routing, executable plan validation commands,
closed review resolution, preserved stage responsibilities, and no release,
publication, deployment, PR, or progressive-disclosure activation

Initial packet inventory: scripts/validation_selection.py@12beb1df#sha256:59a64dbb5da9e85cf8d829be6577c7362215ea926d042e83d595a4cffc72709b; scripts/test-select-validation.py@12beb1df#sha256:c3bcb3149d30b5db2cb22303375f13be5a896b98e802b29c6472a934996b2a5c; scripts/ci.sh@12beb1df#sha256:8a3a06355b520b47ff8664100980dc95bb84901a0b64b3aa3a873a6644ab4385; specs/rigorloop-workflow.md@12beb1df#sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced; specs/rigorloop-workflow.test.md@12beb1df#sha256:e627ff46ca104c7ec26114b42545e81500ecb2137540923f10bf5bd7c1eeccec

Prompt template version: code-review-template-v1

Initial packet hash: sha256:dd4fed097b7dda2fe477d82e0ad888730747d8141accae4a2625338c45043239

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: boundary contract authoring and review guidance, hermetic
behavior generation, immutable recovery, downstream responsibility
preservation, selector routing, adapter parity, report reconstruction, and
final workflow handoff.

Highest-impact failure modes: a proof bypasses a stage boundary; a valid model
path is rejected; a stale run or report is accepted; published skill behavior
drifts; changed inputs do not select their required checks; or the documented
validation path cannot execute.

Changed boundaries: stage author versus parent materializer; deterministic
structure versus semantic review; current versus historical evidence;
component-level selector registration versus the public CI composition.

Evidence expected: complete requirement/property coverage, eight-skill
resource parity, current immutable behavior and preservation runs, typed report
reconstruction, negative fixtures, exact selector integration, and one
successful execution of the plan-selected cross-surface CI command.

Areas requiring direct inspection: initiative diff boundary, contract and
proof maps, runtime and recovery code, stage resources, preservation records,
typed report graph, selector classification and routing, CI composition, and
final lifecycle state.

Areas intentionally out of scope: activating a release marker, publishing or
deploying adapters, opening a PR, and resuming progressive-disclosure work.

Risk classes considered: authorization=applicable at stage/materialization
boundaries; generated-evidence=applicable; validation=applicable;
requirement-fidelity=applicable; release=applicable;
security/privacy=applicable; migration=applicable to historical evidence

Falsifiable review questions: Does the exact selected-CI command named by the plan execute every changed boundary input without manual routing?

## Result

- Skill: code-review
- Status: completed
- Open blockers: BFP-CR-FINAL-1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-FINAL-1
- Recording status: recorded
- Reviewed milestone: final holistic composition
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 correction reopened
- Required review-resolution: yes
- Verify readiness: not-claimed

## Review finding

Finding ID: BFP-CR-FINAL-1

Severity: major

Location: `scripts/validation_selection.py`, selector integration for boundary
scripts and `tests/fixtures/boundary-proof/`

Evidence: `boundary_proof_checks_for_path()` returns the six exact R28p checks
for the four boundary scripts, but `classify_path()` still labels those paths
`script-unsupported`. `_apply_path_selection()` consequently adds the boundary
checks and also emits `manual-routing-required`. The two plan-named fixture
paths are unclassified. Running the exact plan command
`bash scripts/ci.sh --mode explicit ...` exits 2 before executing selected
checks, with four `manual-routing-required` and two `unclassified-path`
blockers. The current selector test proves only the helper return value, not
the composed public selection/CI path.

Required outcome: Every governed boundary script and fixture path must receive
one deterministic selector classification, select the required R28p checks,
and execute through `ci.sh --mode explicit` without manual-routing or
unclassified-path blockers. Boundary release fixtures must retain their
release-transaction regression. Unrelated unsupported scripts must remain
blocked.

Safe resolution path: Add a closed `boundary-proof` path category for the
governed scripts and complete fixture subtree, return after its deterministic
routes are added, preserve normal skill/spec/template routing, add the release
transaction check for boundary release fixtures, and add full
`select_validation()` plus `ci.sh` integration regressions. Rerun the exact
plan command and final holistic review.

Auto-fix class: declared-safe

Declared-safe recipe: change only `scripts/validation_selection.py`,
`scripts/test-select-validation.py`, active plan/validation evidence, and
required review records; do not change boundary semantics, report evidence,
skills, adapters, release state, or external actions.

Required validation: `python scripts/test-select-validation.py`; the exact
plan-owned `bash scripts/ci.sh --mode explicit ...` command; focused M4
validation; final holistic code-review R2.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Component behavior matches R28/R56, but changed-path selection does not compose through the approved validation surface. |
| Test coverage | block | Helper-level selector tests miss the public selector/CI path that fails. |
| Edge cases | concern | Unrelated unsupported scripts must remain blocked while all governed boundary fixture families become deterministic. |
| Error handling | pass | The selector fails closed rather than silently skipping checks. |
| Architecture boundaries | pass | Stage, parent materialization, immutable evidence, and report ownership remain separated. |
| Compatibility | pass | Skill and adapter parity suites pass; no external release action occurred. |
| Security/privacy | pass | Current bounded evidence and child-input isolation remain intact. |
| Derived artifact currency | pass | Behavior, preservation, parity, and report evidence are current. |
| Unrelated changes | pass | Initiative diff from `f4c9354e` contains only the approved project and its durable evidence. |
| Validation evidence | block | The exact cross-surface plan command exits before check execution. |

## Handoff

Reopen the M4 integration correction for the selector/CI composition only.
Record the fix and rerun final holistic code review before `explain-change`.
