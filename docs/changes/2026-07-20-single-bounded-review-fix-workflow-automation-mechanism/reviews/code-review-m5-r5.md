# Code Review M5 R5

Review ID: code-review-m5-r5
Stage: code-review
Round: M5 R5
Reviewer: independent same-session context-reset reviewer
Target: M5 correction commit `51ee13a7`
Reviewed artifact: M5 correction commit `51ee13a7`
Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M5-CR12
Immediate next stage: review-resolution M5

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit range `80b3617b..51ee13a7`
- Requirement-fidelity gate: applicable
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shared the implementation session and therefore does not claim blind L2 independence; the verdict is grounded in a fresh read of the committed diff, governing requirements, targeted tests, and two direct adversarial probes

## Independent risk map

### Affected behavior

- Repository-owned target-ref and merge-base discovery.
- Exact final-review commit binding.
- Runtime rejection of test-only canonical code-state providers.
- Branch-state projection of the immutable anchor and complete changed-path identity.
- Verification currentness and capability invalidation.

### Highest-impact failure modes

- A Git worktree is misclassified as non-Git and accepts caller-supplied canonical state.
- A symbolic or otherwise mutable revision expression silently rebinds an old final-review record to newer code.
- The resolver derives a valid but non-authoritative target or merge base.
- Post-review evidence exclusions conceal code drift.
- Branch evidence agrees with a substituted or retargeted anchor.

### Changed boundaries

- `scripts/workflow_code_state.py`: anchor resolution, Git membership detection, provider selection, and immutable anchor construction.
- `scripts/workflow_automation.py`: final-review field parsing and canonical code-state resolution before verification readiness.
- `scripts/test-workflow-code-state.py`: resolver, target-drift, later-base, and provider-substitution coverage.
- Architecture, ADR, active plan, and change-local evidence: canonical resolver ownership and M5 handoff.

### Expected evidence

- Git membership is determined canonically before any injected provider may run.
- Every path inside a Git worktree, including subdirectories and linked worktrees, rejects test-provider substitution.
- The final-review field is an immutable canonical commit object identity, not a ref or revision expression.
- A later-base attempt, target drift, code-path exemption, stale anchor, and branch-projection mismatch fail closed.
- A true non-Git fixture remains usable without weakening production detection.

### Direct-inspection areas

- `resolve_canonical_code_state`.
- `GitCodeStateAnchorResolver.resolve`.
- `GitCodeStateProvider.snapshot`.
- `resolve_verification_readiness`.
- Provider and verification-readiness regressions.

### Intentionally out-of-scope areas

- M6 public activation and legacy-writer cutover.
- Final holistic review of the complete six-milestone branch.
- PR, publication, deployment, merge, and release actions.

### Risk classes

- Applicable: authorization, canonical-state integrity, repository-root identity, review currentness, verification freshness, and fail-closed error handling.
- Not applicable: end-user accessibility, personal-data processing, cryptographic protocol design, and deployed-service availability.

### Falsifiable review questions

1. Can a test-only provider run when `repository_root` is a subdirectory of the current Git worktree?
2. Does the production Git probe execute before any injected provider?
3. Can `Reviewed commit: HEAD`, a branch, or another mutable revision expression become the canonical reviewed commit?
4. Does the resolver require the persisted review field to equal the resolved immutable commit identity?
5. Do the seven provider tests exercise worktree subdirectories, linked worktrees, and symbolic review revisions?
6. Does the correction preserve the complete merge-base-to-reviewed path set when the anchors are canonical?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M5-CR12`
- Next stage: review-resolution M5
- Review status: changes-requested
- Material findings: `BRF-M5-CR12`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m5-r5.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m5-r5`
- Reviewed milestone: M5. Implementation Review, Correction, and Verification Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution and rereview, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M5-CR12`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `80b3617b..51ee13a7`
- Tracked governing branch state: branch `proposal/single-bounded-review-fix-automation` at `51ee13a7`
- Governing artifacts: approved unified automation spec, active test spec, approved architecture and ADR, active M5 plan, R4 review record, and the `BRF-M5-CR11` resolution
- Validation evidence challenged: seven provider tests, one focused verification-readiness test, recorded full automation suites, direct repository merge-base evidence, and recorded broad smoke
- Conditional evidence rationale: architecture, ADR, R4, and review resolution govern the exact canonical-anchor boundary changed by this correction

## Diff summary

The correction replaces raw Git-range construction with a repository-owned resolver, immutable anchor, target-ref drift checks, exact branch projection, and Git-runtime rejection of a test-only provider. It adds later-base, target-drift, stale-anchor, and provider-substitution regressions and synchronizes the architecture and lifecycle artifacts.

## Finding BRF-M5-CR12

Finding ID: BRF-M5-CR12
Severity: major
Location: `scripts/workflow_code_state.py:387-415`, `scripts/workflow_code_state.py:445-485`, `scripts/workflow_automation.py:472-483`, and `scripts/test-workflow-code-state.py:131-175`
Evidence: `resolve_canonical_code_state` returns an injected provider immediately whenever `<repository_root>/.git` is absent, before running Git's canonical worktree probe. On this tracked repository, `git -C scripts rev-parse --is-inside-work-tree` returns `true` while `scripts/.git` is absent; calling the helper with `repository_root=Path("scripts")` therefore returned an injected `sha256:injected` state instead of rejecting the provider. The added provider-substitution test checks only the top-level repository root, where `.git` exists, so it does not cover this branch. Separately, `GitCodeStateAnchorResolver.resolve` passes the final-review `Reviewed commit` value directly to `rev-parse`; the direct probe accepted `reviewed_revision="HEAD"` and anchored it to current commit `51ee13a7`. Because the durable review record can retain the unchanged string `HEAD` while the ref advances, later code can be treated as reviewed without changing the review evidence identity. These two paths preserve caller- or environment-substitutable canonical authority despite the claimed correction.
Required outcome: Canonical code-state resolution must determine repository membership and repository-root ownership before invoking any injected provider, and final-review anchoring must accept only an immutable canonical commit identity that exactly matches the resolved reviewed commit.
Safe resolution path: Remove the `.git`-marker early return and use one canonical Git-membership/root check before provider selection, or require the already validated state-store repository root before readiness evaluation. Keep true non-Git fixtures behind an explicit test-only boundary without broadly trapping safe read-only Git discovery. Normalize the final-review commit through Git and require the persisted value itself to equal the resulting canonical object ID, rejecting `HEAD`, branch names, tags, revision operators, and other mutable expressions. Add direct regressions for a Git subdirectory, a linked worktree, symbolic review revisions, a valid full commit identity, and the existing true non-Git fixture.
needs-decision rationale: none; the approved architecture and the accepted `BRF-M5-CR11` resolution already require Git-runtime provider rejection and an exact immutable final-review commit anchor.

auto_fix_class: none

## Prior-finding reconciliation

| Prior finding | R5 result | Rationale |
| --- | --- | --- |
| `BRF-M5-CR11` | failed-remediation | The resolver now derives the normal top-level Git range, but its pre-probe `.git` shortcut still admits an injected provider inside a Git worktree and its review anchor accepts mutable revision expressions. Residual defect is `BRF-M5-CR12`. |

## Requirement-fidelity result

| Contract | Result |
| --- | --- |
| `BRF-R043c` | block: branch-state inputs can be concrete while the canonical provider or reviewed commit was substituted |
| `BRF-R044` | block: source or review drift is invisible when `HEAD` is re-resolved from unchanged review evidence |
| `BRF-R085` and T18 | block: fresh verification can bind to code that the durable final-review occurrence did not identify immutably |
| Approved architecture and ADR | block: Git repositories do not universally reject test-only providers, and the review target is not restricted to an immutable commit identity |
| Later-base and target-ref drift handling | pass for the top-level Git-root path |
| M6/public compatibility and external actions | pass for scope: the correction does not activate public routing or cross an external-action boundary |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M5-CR12` permits substituted canonical state under `BRF-R043c`, `BRF-R044`, and `BRF-R085`. |
| Test coverage | block | Seven provider tests pass, but none covers a Git subdirectory, linked worktree, or mutable review revision. |
| Edge cases | block | Direct Git-subdirectory injection and `HEAD` review-anchor probes both succeed. |
| Error handling | block | The helper returns injected state before performing its canonical Git probe. |
| Architecture boundaries | block | Provider rejection and immutable review-target binding are incomplete at the resolver boundary. |
| Compatibility | pass | M5 remains non-public and does not change legacy command behavior. |
| Security/privacy | concern | No secret exposure was found, but verification authority remains substitutable through local invocation inputs. |
| Derived artifact currency | block | Branch evidence can consistently project the substituted or dynamically retargeted anchor. |
| Unrelated changes | pass | The commit is limited to the anchor correction, tests, architecture, and required lifecycle evidence. |
| Validation evidence | concern | Recorded suites and broad smoke pass, but the two direct probes falsify the claimed provider and review-anchor completeness. |

## Direct proof

- `resolve_canonical_code_state(repository_root=Path("scripts"), test_provider=Injected())` returned `sha256:injected`, while `git -C scripts rev-parse --is-inside-work-tree` returned `true` and `scripts/.git` was absent.
- `GitCodeStateAnchorResolver.resolve(..., reviewed_revision="HEAD", ...)` accepted the mutable expression and resolved it to `51ee13a7142390d25b8034f105ec6fa54c4a3d81`.
- `python scripts/test-workflow-code-state.py` passed seven tests; the passing suite does not contain either failing contrast.
- `python scripts/test-workflow-automation.py -k verification_readiness` passed its single selected test; the fixture uses the literal non-Git reviewed revision `fixture-reviewed` and does not exercise production Git review-target validation.

## Isolation and handoff

- This formal review is recorded.
- No automatic downstream handoff occurs because this is a direct isolated review.
- `BRF-M5-CR12` requires review-resolution before any correction and M5 R6 rereview.
- No owner decision is required; the correction remains inside the approved architecture and M5 scope.
- M6, final closeout, explain-change, verify, and PR handoff remain blocked.
