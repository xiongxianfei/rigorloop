# Code Review M3 R8

Review ID: code-review-m3-r8
Stage: code-review
Round: M3 R8
Reviewer: Codex code-review skill in isolated direct-review mode
Target: M3 correction commit `6dbd55b0`
Reviewed artifact: M3 correction commit `6dbd55b0`
Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-22
Recording status: recorded
Material findings: BRF-M3-CR15
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M3-CR15` blocks M3 closeout; it does not require a product, spec, architecture, or ownership decision
- Next stage: review-resolution M3
- Review status: changes-requested
- Material findings: `BRF-M3-CR15`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m3-r8.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m3-r8`
- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution needed, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M3-CR15`
- Verify readiness: not-claimed

## Review Inputs

- Diff surface: correction commit `6dbd55b0` against its first parent.
- Tracked governing branch state: clean worktree at `6dbd55b0` before review evidence recording.
- Governing contract: canonical state ownership, `BRF-R020`, `BRF-R073`-`BRF-R078`, `BRF-R100`, and active-plan live-state ownership.
- Test spec: T6, T14-T16, CMD10-CMD14, and deterministic temporary-repository proof requirements.
- Architecture and ADR: exact change-local persistence ownership and fail-closed canonical-state synchronization.
- Active plan: M3 `review-requested` handoff for R8.
- Prior finding dispositions: `BRF-M3-CR13` and `BRF-M3-CR14` in `review-resolution.md`.

## Review Mode and Risk Map

This was an isolated direct review. It does not claim the workflow-managed automated-review manifest or automatic downstream handoff.

- Affected behavior: full-chain symlink rejection and live closeout-detail state synchronization.
- Highest-impact failures: residual repository-identity redirection and a contradictory authoritative detail accepted through vocabulary variants or unrestricted prose.
- Changed boundaries: absolute metadata path to canonical repository root, and formal review evidence to the active-plan reason detail.
- Expected evidence: the R7 ancestor-symlink reproduction fails closed, and the complete review-state detail has one closed representation that cannot contain a second state assertion.
- Direct-inspection areas: `WorkflowAutomationStateStore.__init__`, `_review_state_detail_errors`, the review-state regexes, and new regression fixtures.
- Intentionally out of scope: M4-M6, public routing, final holistic review, verification, PR, publication, and external actions.
- Applicable risk classes: filesystem trust, state integrity, workflow ownership, compatibility, and proof sufficiency.
- Non-applicable risk classes: network, credentials, deployment, database, UI, and generated adapters.
- Falsifiable questions: Does an earlier lexical symlink still pass? Can alternate structured key syntax or plain contradictory state language survive the remainder filter?

## Diff Summary

The correction now checks every absolute lexical metadata component before resolving the canonical path. It also adds a denylist-style remainder check for `finding(s)`, finding-shaped IDs, and structured fields whose keys use a restricted hyphenated identifier grammar.

The path correction satisfies the direct R7 reproduction. The review-state correction still leaves an unrestricted prose remainder and recognizes only some structured key spellings. Consequently, alternate state keys and semantically contradictory prose remain valid in the same authoritative field.

## Prior-Finding Reconciliation

| Prior finding | R8 result | Evidence |
| --- | --- | --- |
| `BRF-M3-CR13` | resolved | The direct earlier-ancestor symlink probe now raises `StateContractError` before store construction completes. |
| `BRF-M3-CR14` | failed-remediation | The original hyphenated second field is rejected, but underscore-prefixed/underscore-delimited state keys and plain contradictory state prose produce zero full-validator blockers; the remaining defect is `BRF-M3-CR15`. |

## Findings

## Finding BRF-M3-CR15

Finding ID: BRF-M3-CR15
Severity: major
Location: `scripts/lifecycle_state_sync.py:68-80` and `scripts/lifecycle_state_sync.py:330-381`; coverage gap in `scripts/test-artifact-lifecycle-validator.py:1193-1248`
Evidence: The full lifecycle validator accepted all three open-review details: a valid projection followed by `nothing remains open`, by `review_state=closed`, and by `_review-state=closed`. Each produced zero blockers. The field regex allows only letter-started hyphenated names and the prose filters recognize only `finding(s)` and finding-shaped IDs. This contradicts the R7 required outcome that the complete live detail contain exactly one review-state projection without an equivalent second claim.
Required outcome: The entire live review-state detail must use one closed, machine-generated representation for both open and closed formal review state, with no unrestricted remainder capable of restating that state.
Safe resolution path: Make the complete text after the em dash exactly `review-state=<open|closed>; open-count=<n>; open-findings=<none|sorted IDs>` with no remainder. Require the projection in both open and closed cases, update the active-plan and fixture defaults, and add direct underscore-key, prefixed-key, plain-contradiction, missing-closed-projection, and exact-open/exact-closed tests.
needs-decision rationale: none; this is the closed positive grammar already required by the accepted R7 finding and avoids further vocabulary-denylist expansion.
auto_fix_class: none

## Requirement Fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| Exact canonical persistence ownership | pass | Full-chain ancestor-symlink reproduction now fails before construction. |
| `BRF-R073`-`BRF-R078` and `BRF-R100` repository identity | pass | The reviewed path correction no longer resolves away the R7 ancestor alias. |
| `BRF-R020` and active-plan live-state ownership | block | The complete authoritative detail still permits a second contradictory state assertion. |
| Deterministic fail-closed state projection | block | Acceptance depends on an incomplete vocabulary denylist rather than a closed full-field grammar. |
| M3 non-public boundary | pass | No public skill, adapter, M4-M6 integration, or external-action surface changed. |

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Complete live-state agreement remains bypassable. |
| Test coverage | block | Alternate-key and plain-contradiction cases are absent. |
| Edge cases | block | Three direct full-validator variants return zero blockers. |
| Error handling | block | Contradictory authoritative state is accepted instead of failing closed. |
| Architecture boundaries | pass | The full lexical filesystem ownership boundary now holds for the named reproduction. |
| Compatibility | concern | The correction should migrate active-plan and fixture detail to one exact generated projection. |
| Security/privacy | pass | The reviewed path alias reproduction is rejected and no sensitive logging was added. |
| Derived artifact currency | pass | No generated output or public adapter changed. |
| Unrelated changes | pass | Commit `6dbd55b0` is limited to R7 correction code, tests, and lifecycle evidence. |
| Validation evidence | concern | Existing suites pass, but direct negative probes expose incomplete review-state coverage. |

## Validation and Direct Proof

- `python scripts/test-workflow-automation-state.py`: 48 tests passed.
- `python scripts/test-artifact-lifecycle-validator.py`: 154 tests passed.
- `git diff --check 6dbd55b0^..6dbd55b0`: passed.
- Direct ancestor-symlink probe: rejected with `canonical change metadata path must not contain symlinks`.
- Direct full-validator plain contradiction: zero blockers.
- Direct full-validator `review_state=closed`: zero blockers.
- Direct full-validator `_review-state=closed`: zero blockers.

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

The closed detail grammar should replace, rather than extend, the accumulated prose and structured-key denylists. Descriptor-based no-follow handling remains a possible future hardening measure but is not required by this correction's accepted component-walk resolution.

## Milestone Handoff

- Reviewed milestone: M3. Target Binding, Canonical Position, and Capability Evaluation
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M3-CR15`
- Remaining in-scope implementation milestones: M3 resolution needed, M4, M5, M6
- Next stage: review-resolution M3
- Final closeout readiness: not ready because M3 has one open R8 finding and M4-M6, final holistic review, explanation, verification, and PR handoff remain.

## Recommended Next Stage

This direct review remains isolated: no automatic downstream handoff or implementation correction was performed.
Enter `review-resolution` for `BRF-M3-CR15`, return M3 to `review-requested` after correction, and rerun code-review M3.
Do not start M4 while the finding remains open.
