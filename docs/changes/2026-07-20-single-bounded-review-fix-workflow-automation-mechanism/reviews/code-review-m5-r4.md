# Code Review M5 R4

Review ID: code-review-m5-r4
Stage: code-review
Round: M5 R4
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `ed8c69cc`
Reviewed artifact: M5 correction commit `ed8c69cc`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR11
Immediate next stage: review-resolution M5

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `05af0e00..ed8c69cc`
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer participated in the preceding implementation turn, so this review does not claim blind L2 independence; the risk map below was reconstructed from the tracked diff and governing requirements before implementation validation summaries and prior-finding dispositions were consulted during this review pass

## Independent risk map

### Affected behavior

- Canonical final-code path and identity derivation.
- Verification-authorization currentness.
- Git revision, worktree, rename, deletion, and post-review evidence handling.
- Branch-state projection of provider-owned revisions, paths, and identity.
- M5 lifecycle evidence and milestone rereview handoff.

### Highest-impact failure modes

- The supposedly canonical provider accepts a caller-selected base that starts after earlier in-scope changes.
- The reviewed revision does not equal the artifact actually inspected by final holistic review.
- Post-review exemptions conceal in-scope code or governing-artifact drift.
- Dirty, untracked, deleted, or renamed paths disappear from the complete final-code identity.
- A non-Git fixture seam becomes a runtime authority-injection seam.
- Branch evidence and every downstream closeout artifact agree on the same incomplete provider identity.

### Changed boundaries

- `scripts/workflow_code_state.py`: new code-state model, Git range selection, path/status parsing, worktree drift, and exemptions.
- `scripts/workflow_automation.py`: provider injection and exact branch projection checks before explanation or verification.
- `scripts/test-workflow-code-state.py` and `scripts/test-workflow-automation.py`: provider and verification-readiness proof.
- Architecture, ADR, active plan, and change-local review evidence: provider ownership and lifecycle synchronization.

### Expected evidence

- The canonical base and reviewed revision are derived from authoritative workflow or review state, not accepted as unconstrained caller input.
- The reviewed revision is bound to the final holistic review target.
- A later-base/partial-range attempt fails even when branch evidence exactly matches the partial provider result.
- Added, modified, deleted, renamed, dirty, and untracked paths are covered directly.
- Post-review exemptions come from a closed stage-owned evidence registry and cannot include code.
- Non-Git injection is restricted to a test-only boundary.

### Direct-inspection areas

- `GitCodeStateProvider.__init__` and `snapshot`.
- Construction sites for `GitCodeStateProvider`.
- `resolve_verification_readiness` and `coordinate_non_public_implementation_stage`.
- Provider fixtures and omission contrasts.
- Architecture ownership language for independent canonical derivation.

### Intentionally out-of-scope areas

- M6 public command activation and legacy-writer cutover.
- Final holistic review of the complete multi-milestone branch.
- PR opening, publication, deployment, merge, and release execution.

### Risk classes

- Applicable: authorization, integrity, canonical-state ownership, path containment, review currentness, verification freshness, and lifecycle-state consistency.
- Not applicable: end-user UI accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable review questions

1. Can a caller select a base after earlier in-scope changes and obtain a valid provider identity for only the later suffix?
2. Can branch evidence exactly match that partial provider identity and pass readiness?
3. Is any production construction site responsible for deriving the base and reviewed revisions from authoritative state?
4. Can a post-review exemption name an in-scope code path?
5. Do tests reject a valid Git range whose base is not the canonical initiative or review base?
6. Do tracked lifecycle surfaces truthfully represent the result of this exact review?

## Phase receipts

### `risk-map-recorded`

- Status: completed
- Recorded before this review pass consulted implementation validation summaries or prior-finding dispositions
- Risk map identity: this review record at its initial tracked-worktree state

### `evidence-results-released`

- Status: completed
- Released after the risk map and requirement-property inspection
- Provider suite: 4 passed
- Verification-readiness selection: 1 passed
- Verify selection: 4 passed
- Direct canonical-anchor probe: failed; the provider accepted `ed8c69cc^..ed8c69cc` as canonical and returned 12 paths while the tracked initiative diff from merge base to `HEAD` contains 96 paths
- Evidence challenge result: the tests prove status/path handling inside a caller-selected range, but no test or construction path proves that the selected range is the authoritative complete range
- Change-record bounded query: unavailable for stage `code-review`; the helper returned `stage-not-found`, so the review used the tracked review-resolution and bounded validation entries instead

### `prior-findings-reconciled`

- Status: completed
- Released after blind-first source inspection, governing-requirement decomposition, focused tests, and the direct partial-range probe
- Prior review: `code-review-m5-r3`

### `verdict-recorded`

- Status: completed
- Verdict: `changes-requested`
- Requirement-fidelity outcome: failed for canonical complete final-code anchoring
- Automatic downstream handoff: stopped because this is a direct isolated review

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR11`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR11`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r4.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r4`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR11`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `05af0e00..ed8c69cc`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `ed8c69cc`
- Governing artifacts: approved unified automation spec, active test spec, approved architecture and ADR, active M5 plan, and the R3 review-resolution disposition
- Validation evidence: provider, verification-readiness, and verify focused suites plus a direct tracked-branch partial-range probe
- Conditional evidence rationale: architecture, ADR, and R3 resolution were necessary because the diff introduces a new executable ownership boundary and claims to resolve a canonical-state finding

## Diff summary

The correction introduces a Git-backed code-state provider, hashes a base-to-reviewed change set including additions, modifications, deletions, and renames, checks post-review commits and worktree drift, requires branch evidence to project the provider's exact revisions, paths, and identity, adds a non-Git fixture provider, and synchronizes architecture and lifecycle evidence.

## Finding BRF-M5-CR11

Finding ID: BRF-M5-CR11
Severity: major
Location: `scripts/workflow_code_state.py:86-111`, `scripts/workflow_code_state.py:253-304`, `scripts/workflow_automation.py:332-383`, `scripts/workflow_automation.py:2088-2125`, and `scripts/test-workflow-code-state.py:46-115`
Evidence: `GitCodeStateProvider` accepts arbitrary non-empty `base_revision` and `reviewed_revision` constructor strings, resolves them as commits, and treats their range as canonical without comparing the base with an authoritative branch target, merge base, change manifest, final-review invocation manifest, or capability basis. No non-test construction site derives those anchors. On the tracked branch, the authoritative initiative range from merge base `52bdcbb329897225c22a593b8e04541409e2d315` to `HEAD` contains 96 paths, but constructing the provider with `base_revision='ed8c69cc^'` and `reviewed_revision='ed8c69cc'` succeeds and returns only the 12 correction-commit paths. Branch evidence can then project those same partial revisions, paths, and identity, so exact projection does not establish completeness. The four provider tests choose their own expected base and never challenge a later valid base that omits earlier in-scope changes.
Required outcome: Canonical final-code scope must be anchored to independently derived, identity-bound workflow and final-review state so callers and branch evidence cannot choose a valid but incomplete Git range.
Safe resolution path: Introduce a trusted anchor resolver owned by the automation/review boundary. Derive the base from authoritative tracked change or target-branch state and bind the reviewed revision to the exact final holistic review target and verification capability basis. Make the Git provider consume that resolved immutable anchor rather than raw caller revisions; restrict non-Git providers to an explicit test-only adapter; derive any post-review evidence exclusions from the closed stage-output registry. Add failing contrasts for a later base, wrong reviewed revision, partial range with matching branch projection, missing/stale anchor identity, and an attempted runtime fixture-provider substitution.
needs-decision rationale: none; the approved architecture already requires independently owned canonical derivation and exact final-review/currentness binding.
auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R4 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR10` | failed-remediation | Branch evidence no longer selects the path list directly, but caller-selected provider anchors can still narrow the supposedly canonical identity domain. Residual defect is `BRF-M5-CR11`. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| `BRF-R043c` | block: branch-state inputs can be concrete and mutually consistent while anchored to an incomplete caller-selected range |
| `BRF-R044` | block: canonical-state mismatch cannot be detected when the provider's base is itself the unvalidated scope choice |
| `BRF-R085` and T18 | block: fresh verification evidence may be bound to only a suffix of the implementation change |
| Approved architecture and ADR | block: the implementation provides base-to-reviewed hashing but not independently owned derivation of the base/review anchors |
| Added/deleted/renamed/dirty/untracked handling | pass within the selected range; these contrasts do not prove range completeness |
| M6/public compatibility and external actions | pass for scope: public routing and external-action surfaces are unchanged by this correction |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M5-CR11` permits incomplete but internally consistent verification basis under `BRF-R043c`, `BRF-R044`, and `BRF-R085`. |
| Test coverage | block | Status/path tests pass, but no wrong-base, partial-range, reviewed-anchor, or runtime-provider-substitution contrast exists. |
| Edge cases | block | Named omission handling is proved only after accepting caller-selected anchors; earlier valid commits remain omittable. |
| Error handling | concern | Invalid commits and post-review drift fail closed, but a valid later base is accepted silently. |
| Architecture boundaries | block | Raw constructor arguments, rather than an independently owned anchor resolver, define canonical scope. |
| Compatibility | pass | The reviewed change remains behind the M5 non-public boundary and does not alter public or legacy commands. |
| Security/privacy | concern | No secrets or unsafe logging were found, but verification authority can rely on an under-scoped code identity. |
| Derived artifact currency | block | All closeout artifacts can agree with the same partial provider identity. |
| Unrelated changes | pass | The diff is limited to the final-code correction, matching tests, architecture/ADR alignment, and lifecycle evidence. |
| Validation evidence | concern | Focused suites pass, but the direct 12-of-96 path probe falsifies their completeness claim. |

## Direct-proof gaps

- No test rejects a valid later base that excludes earlier in-scope commits.
- No test binds the reviewed revision to the final holistic review target identity.
- No runtime construction path derives an immutable code-state anchor from authoritative workflow state.
- No test prevents a non-Git fixture provider from being substituted at a runtime boundary.

## Recording validation

- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism` passed with 56 reviews, 89 findings, and 1 open finding.
- Explicit lifecycle validation passed for the review record, review ledger, resolution ledger, change metadata, plan body, plan index, and plan archive, with the existing non-blocking historical merge-language warning.
- `python scripts/test-change-metadata-validator.py` passed 53 tests.
- Direct change-metadata validation, guide-system validation, and diff checks passed.
- `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` passed all 11 checks in 414 seconds.

## Milestone handoff

- Reviewed milestone: M5
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M5-CR11`
- Remaining in-scope implementation milestones: M5 resolution and rereview, M6
- Next stage: review-resolution M5
- Final closeout readiness: not ready because M5 has one open material finding and M6 remains unimplemented
- Automatic downstream handoff: none; this direct review remains isolated
