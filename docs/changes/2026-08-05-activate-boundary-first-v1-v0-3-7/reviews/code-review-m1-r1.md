# Code Review: M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: two independent L2 Codex reviewers
Target: 3852a010..048cf61f
Reviewed artifact: commit 048cf61f
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-implementation
Reviewer context ID: m1-r1-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; remote authority read; release boundary; lifecycle gate
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/boundary-first-v1-v0-3-7-activation-release.md@048cf61f#sha256:48a42eb23156330bc7a60a869c93ec512e3c0b8e79b29587ccfbd94eebab8db9; specs/boundary-first-v1-v0-3-7-activation-release.test.md@048cf61f#sha256:bb434cc5390d7490aa64fe7bfbbc377b16e5bc4fe1fa2cb6d8c183b4c6aa3baa; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@048cf61f#sha256:e940e7d27ad26287f33bb65a2616e096d6b5ed805b6aa95346ea4a4c5370af91; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@048cf61f#sha256:911b77ee4384c8576269a04233e7581865075bda3a78277f67371b3afca2d2e5
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@048cf61f#sha256:48a42eb23156330bc7a60a869c93ec512e3c0b8e79b29587ccfbd94eebab8db9; specs/boundary-first-v1-v0-3-7-activation-release.test.md@048cf61f#sha256:bb434cc5390d7490aa64fe7bfbbc377b16e5bc4fe1fa2cb6d8c183b4c6aa3baa; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@048cf61f#sha256:e940e7d27ad26287f33bb65a2616e096d6b5ed805b6aa95346ea4a4c5370af91; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@048cf61f#sha256:911b77ee4384c8576269a04233e7581865075bda3a78277f67371b3afca2d2e5; commit:048cf61f.diff@048cf61f#sha256:06bd3b09e6eff7c33b076840a98e1808970b78bba67872724b5e94f844bfecb1
Prompt template version: code-review-v1
Initial packet hash: sha256:9f9b6168f8e12713f854db3651d17731a483fd031964735b031f60852ad97f26
Manifest owner: workflow-orchestrator
Affected behavior: exact candidate CLI; fresh remote authority; first-parent P/B/T/H; strict validation reuse; post-transition path classification; publication readiness; non-public diagnostics; selector composition
Highest-impact failure modes: malformed input becomes strict success; remote or graph ambiguity is trusted; reverted or disguised payload drift passes; placeholder evidence authorizes publication; diagnostics leak private values; sibling proof is bypassed
Changed boundaries: BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; INT-001; INT-002; INT-004; INT-007
Evidence expected: direct T1-T6, T12, and T16 negative matrices using Git histories, bare remotes, ref/tree snapshots, privacy sentinels, exact paths, repeated output, strict regression, and sibling selection/failure
Areas requiring direct inspection: parser dispatch; Git subprocesses; transition topology; strict helper reuse; lifecycle classifier; readiness authority; serialization; regression tests; selector preflight
Areas intentionally out of scope: M2 atomic mutation; M3 payload generation; M4 real transition; public release actions; final verification
Risk classes considered: contract fidelity; remote authority; first-parent topology; temporal drift; lifecycle settlement; composition bypass; security/privacy; compatibility
Falsifiable review questions: Does every supplied candidate option obey the closed input contract; can forbidden history be hidden by a revert; can arbitrary or placeholder evidence authorize readiness; are diagnostics bounded and actionable; does selector proof cover sibling owners
Material findings: BFA-M1-CR1-001, BFA-M1-CR1-002, BFA-M1-CR1-003, BFA-M1-CR1-004, BFA-M1-CR1-005, BFA-M1-CR1-006, BFA-M1-CR1-007, BFA-M1-CR1-008
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Second review: satisfied; both reviewers requested changes

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Reviewed target: `3852a010..048cf61f`
- Reviewed milestone: M1
- Material findings: BFA-M1-CR1-001 through BFA-M1-CR1-008
- Recording status: recorded
- Review resolution: required
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Next stage: review-resolution M1
- Verify readiness: not-claimed

## Review inputs

- Actual commit diff `3852a010..048cf61f`
- Approved feature spec, test spec, M1 plan slice, and activation-publication ADR
- Direct candidate, strict-mode, selector, and lifecycle tests
- M1 implementation evidence, released only after both reviewers recorded blind-first risk maps

## Independent review gate

Two separate reviewers performed blind-first review at independence level L2.
Both recorded risk maps before validation summaries were released. Reviewers
then inspected the diff and tests, ran adversarial reproductions, challenged the
reported evidence, decomposed the applicable requirements, and returned
`changes-requested` independently.

Risk classes considered: remote authority and freshness, first-parent topology,
closed input vocabulary, strict compatibility, temporal drift, lifecycle
settlement, validation composition, diagnostics/privacy, mutation safety, and
derived-output classification. Live atomic publication and public registry
behavior remain outside M1.

## Findings

### BFA-M1-CR1-001 — Empty candidate value falls through to strict mode

Finding ID: BFA-M1-CR1-001
Severity: blocker
Location: `scripts/validate-boundary-first.py`
Evidence: both candidate dispatch branches test truthiness; `--check --activation-candidate ''` exits zero with ordinary strict success.
Required outcome: any supplied candidate option enters candidate validation and only exact `v0.4.0` succeeds.
Safe resolution path: distinguish `None` from an empty supplied value and add CLI empty-value regressions with and without `--check`.
needs-decision rationale: none
- Reviewer aliases: `CR-M1-R1-001`, `BFA-M1-CR2-004`

### BFA-M1-CR1-002 — Reverted post-transition payload drift is accepted

Finding ID: BFA-M1-CR1-002
- Severity: blocker
- Location: `scripts/boundary_first_validation.py` post-transition path scan
- Evidence: endpoint-only `git diff T..H` is empty after a forbidden skill change and later revert; candidate validation then succeeds.
- Required outcome: every first-parent commit after T changes only approved lifecycle evidence; a revert cannot rehabilitate invalid history.
- Safe resolution path: inspect every first-parent commit parent-relatively, reject the union of forbidden paths, and test change/revert, rename, deletion, multiple paths, second transition, and replacement history.
- needs-decision rationale: none
- Reviewer alias: `CR-M1-R1-002`

### BFA-M1-CR1-003 — Publication readiness treats file presence as settlement

Finding ID: BFA-M1-CR1-003
- Severity: blocker
- Location: `scripts/boundary_first_validation.py` publication-readiness check and candidate fixtures
- Evidence: literal `settled` placeholder files and matching review filenames pass; lifecycle state, review outcome, open resolution, authority, and canonical candidate JSON are not validated.
- Required outcome: publication readiness proves settled proposal-through-candidate evidence through canonical lifecycle authority.
- Safe resolution path: compose change-metadata, artifact-lifecycle, and review authority; require canonical candidate evidence; add missing, placeholder, pending, changes-requested, unresolved, stale, malformed, and settled fixtures.
- needs-decision rationale: none
- Reviewer aliases: `CR-M1-R1-003`, `BFA-M1-CR2-002`

### BFA-M1-CR1-004 — Candidate failure output lacks bounded context and corrective action

Finding ID: BFA-M1-CR1-004
- Severity: blocker
- Location: `scripts/validate-boundary-first.py` candidate failure serialization
- Evidence: failure JSON contains only status, mode, and issues even when release, P/B/T/H, rollback, or tag state is available; no corrective-action field is emitted.
- Required outcome: failures expose available bounded identities, invariant, and actionable correction without leaking private values.
- Safe resolution path: return a bounded partial candidate context and stable corrective actions; test local-tag, remote, topology, and drift failures.
- needs-decision rationale: none
- Reviewer alias: `CR-M1-R1-004`

### BFA-M1-CR1-005 — M1 direct proof is materially incomplete

Finding ID: BFA-M1-CR1-005
- Severity: major
- Location: candidate and selector regression tests; M1 implementation evidence
- Evidence: T4 lacks the candidate zero/multiple/non-first-parent matrix; T5 lacks per-class, multi-path, revert/repair, second-transition, and replacement histories; T6 lacks required privacy sentinels and complete snapshots; T12 tests one missing filename and placeholders; T16 lacks multi-class selection and injected sibling failures. CMD4 also omits newly touched selector files.
- Required outcome: every M1-owned T1-T6, T12, and T16 property has direct executable proof and the recorded selector scope matches the complete changed surface.
- Safe resolution path: add the missing table-driven partitions and aligned selector proof; route any normative CMD4 text correction through test-spec ownership before claiming that revised command.
- needs-decision rationale: none
- Reviewer aliases: `CR-M1-R1-005`, `BFA-M1-CR2-005`

### BFA-M1-CR1-006 — Directory preflight hides mixed tracked and untracked contents

Finding ID: BFA-M1-CR1-006
- Severity: major
- Location: `scripts/validation_selection.py` tracked-authoritative preflight
- Evidence: a directory passes when any tracked descendant exists, even when another authoritative descendant is untracked.
- Required outcome: an explicit authoritative directory passes only when every applicable existing descendant is tracked.
- Safe resolution path: enumerate applicable descendants and add fully tracked, mixed, only-untracked, empty, and unsafe-path tests.
- needs-decision rationale: none
- Reviewer alias: `CR-M1-R1-006`

### BFA-M1-CR1-007 — Lifecycle subtree allowlist admits arbitrary payload

Finding ID: BFA-M1-CR1-007
- Severity: blocker
- Location: `scripts/boundary_first_validation.py` activation lifecycle path classifier
- Evidence: any descendant of `evidence/` or `reviews/` is accepted; a post-T `evidence/release-package.tgz` commit passes candidate validation.
- Required outcome: only actual approved lifecycle evidence paths/shapes are allowed after T; packages, generated outputs, release inputs, and arbitrary files fail.
- Safe resolution path: replace open subtrees with a closed lifecycle-owned policy and add accepted canonical evidence plus rejected archive/generated/arbitrary fixtures.
- needs-decision rationale: none
- Reviewer alias: `BFA-M1-CR2-001`

### BFA-M1-CR1-008 — Drift diagnostics disclose private path sentinels

Finding ID: BFA-M1-CR1-008
- Severity: blocker
- Location: `scripts/boundary_first_validation.py` drift issue path serialization
- Evidence: a post-T path containing a private token sentinel is emitted verbatim in failure JSON; T6 injects none of its required token, OTP, user, host, environment, or temporary-path sentinels.
- Required outcome: diagnostics identify drift actionably without exposing prohibited private values.
- Safe resolution path: use privacy-bounded path identities and add every T6 sentinel through candidate failure serialization.
- needs-decision rationale: none
- Reviewer alias: `BFA-M1-CR2-003`

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BFA-R004, R015-R017, R031, R034-R035 violations |
| Test coverage | block | T4, T5, T6, T12, and T16 are incomplete |
| Edge cases | block | Empty input, reverted drift, arbitrary evidence payload, and private paths reproduce |
| Error handling | concern | Remote failures block, but bounded context/action is incomplete |
| Architecture boundaries | block | Open lifecycle subtree and false settlement weaken the approved authority split |
| Compatibility | pass | Ordinary strict mode remains strict in the tested normal path |
| Security/privacy | block | Drift path can expose injected private values |
| Derived artifact currency | concern | Generated payload can be misclassified as lifecycle evidence |
| Unrelated changes | concern | Selector correction is motivated by CMD4 but is incomplete |
| Validation evidence | block | Passing suites do not cover the approved property matrix |

## Evidence challenge

The reported 70 boundary-first tests, 142 selector tests, strict check,
compilation, selector result, and lifecycle validation are credible for the
assertions they execute. They are insufficient for clean review because direct
adversarial reproductions establish the findings above.

No finding requires a product, specification, or architecture decision. All
eight have bounded resolution paths inside the approved M1 behavior, except
that any literal CMD4 artifact amendment remains owned by test-spec.
