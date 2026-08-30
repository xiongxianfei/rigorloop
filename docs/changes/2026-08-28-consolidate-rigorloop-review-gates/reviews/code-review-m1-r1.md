# Code Review M1 R1: Topology Identity and Activation Foundation

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex isolated independent code-review context with fresh-assumption reset
Review date: 2026-08-29
Target: working-tree M1 topology-foundation implementation slice
Reviewed milestone: M1
Reviewed artifact: working-tree packet `sha256:4ca8e7dfa1f4bd8a8d38d8b3ccf63a57164f9dcc07ed7abb867eaeba3644d392`
Status: blocked
Review status: blocked
Review gate outcome: blocked
Material findings: CRG-M1-CR1, CRG-M1-CR2
Recording status: recorded
Automated review: yes
Native review status: blocked
Independence level: L0
Author context ID: root-m1-implementation
Reviewer context ID: root-m1-code-review-r1-context-reset
Context separation mechanism: fresh-assumption-reset
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: workflow topology authority; compatibility baseline; public CLI output; lifecycle routing
Risk-tier classifier: deterministic changed-surface classification
Governing artifacts: `specs/consolidated-review-gates.md`; `specs/consolidated-review-gates.test.md`; `docs/adr/ADR-20260828-consolidated-review-package-topology.md`; `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md`; `specs/cli-observability-and-token-efficient-results.md`
Formal criteria: code-review-first-pass-v1; boundary-first-v1; requirement-fidelity-gate-v1
Initial packet inventory: packages/rigorloop/dist/lib/review-topology.js@working-tree#sha256:eb2d85775da9696679d053cf3c8eea635c784f45ad09ce45af744c8a37c4daaa; packages/rigorloop/dist/lib/new-change.js@working-tree#sha256:49531b0e606a3b0fce84ee74627fb649ecc9379695b9cd622df3515d34a500b0; packages/rigorloop/dist/bin/rigorloop.js@working-tree#sha256:af830ef032e7553ed9c180e29d4ffb6e6f7ca0c20a8a996cce44829ce1c7b730; packages/rigorloop/dist/lib/lifecycle-contract.js@working-tree#sha256:a5f55ef1587ceaeba2eb85f5d2db7fcc0d5fe02fb32f93909b6aff40f2cecbbc; packages/rigorloop/dist/lib/lifecycle-read.js@working-tree#sha256:d3b34c4d0fe1b4a12ffe36fb9f8278f8a35f62c4f29ef7f2d9b478bd654beb4c; packages/rigorloop/dist/lib/lifecycle-cli.js@working-tree#sha256:03198b0dd4ab9e86e86207beb11b605b5519014201f9f9c4f6b689199d5edaca; schemas/change.schema.json@working-tree#sha256:0305fbf499fca6dd2e35d0dbfe949e90cb98a5889af2e2e5b1f7e00e20cbf4ec; schemas/review-topology-activation.schema.json@working-tree#sha256:e32816801696f9eb771b46415dd4e265a35d0dd029366fe9f494cb69275bc31d; specs/review-topology-activation.yaml@working-tree#sha256:43e01b5e79a07b4e492be3d4866efc7fc47b9915992b6fbcba04ba8dcf4ada2e; scripts/change_metadata_semantics.py@working-tree#sha256:5d4e6111c08d6a13246e5c884382089427949eb6a30705b69124cd10ab3ea3b5; scripts/test-change-metadata-validator.py@working-tree#sha256:a87bb9424c51a95bdfe52b9f057a3c622b746f77f29d18cfb4c736de9182b65f; packages/rigorloop/test/cli.test.js@working-tree#sha256:32b061cc5790af81b12345aabf5c6b258ba3c4ac5e53d25f04660b7f70ae4a8a; packages/rigorloop/test/lifecycle-contract.test.js@working-tree#sha256:15a199cdba8706f93354970a29175b9c11527e5d87e62db8944a4c240157bf76; packages/rigorloop/test/lifecycle-read.test.js@working-tree#sha256:7c9f2d0679f17cf3edbee49abaca72d14132e859ddaebe9cd1ba03f960ec0fb6; docs/changes/2026-08-28-consolidate-rigorloop-review-gates/evidence/m1-topology-foundation-implementation.md@working-tree#sha256:87ef3490b99c31c62beda93e36717b0736c619e574dae85a9449e96bc0cf681d
Prompt template version: code-review-v1
Initial packet hash: sha256:4ca8e7dfa1f4bd8a8d38d8b3ccf63a57164f9dcc07ed7abb867eaeba3644d392
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: topology admission, legacy inheritance, new-change metadata, and lifecycle status/context output
Highest-impact failure modes: ambiguous topology authority; premature v2 activation; rejection of legitimate legacy changes; public-output compatibility break
Changed boundaries: BND-INPUT-001; BND-AUTH-001; BND-COMPAT-001; INT-005; INT-008
Evidence expected: CRG-T01, CRG-T02, M1 command ledger, absent-manifest failure, byte-stable legacy interpretation, and public-output compatibility
Areas requiring direct inspection: topology parser; manifest; new-change path; lifecycle read model; schemas; focused tests; public-output compatibility fixture
Areas intentionally out of scope: M2 package settlement, M3 topology-specific stage graphs, M4 skills, M5 adapters, M6 activation, and final verification
Risk classes considered: input; authority; compatibility; state; failure; public output; derived fixture currency
Falsifiable review questions: Can missing manifest state grant v1; can unknown topology pass; can v2 activate early; can existing v0.4.x output change unnoticed

## Result

- Skill: code-review
- Status: blocked
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m1-r1.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`, and `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Open blockers: CRG-M1-CR1 and CRG-M1-CR2
- Next stage: blocked
- Review status: blocked
- Material findings: CRG-M1-CR1, CRG-M1-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: blocked
- Remaining implementation milestones: M1, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-M1-CR1, CRG-M1-CR2
- Verify readiness: not-claimed

## Actual-diff summary

M1 adds a pending activation manifest and schema, a deterministic baseline calculator and topology interpreter, explicit topology output from `new-change`, status/context projection, schema and semantic validation, and focused regressions. The reviewed packet is local working-tree state rather than tracked milestone commits, so it supports the findings below but not a clean branch-scoped conclusion.

## Findings

### Finding CRG-M1-CR1

Finding ID: CRG-M1-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/review-topology.js:114-139`; absent-manifest topology interpretation and new-change default
Evidence: `interpretReviewTopology({ changeId: "unlisted", manifest: null })` returns `artifact-gates-v1` with source `pre-manifest-compatibility`, and `reviewTopologyForNewChange` also returns v1 when the authoritative manifest is absent. CRG-R35 and the accepted ADR permit markerless v1 only for an exact accepted-baseline member and require every other missing marker to fail closed. The focused status test explicitly preserves the unapproved absent-manifest fallback.
Required outcome: A markerless change must inherit v1 only through exact membership in a validated accepted baseline; missing authoritative manifest state must not manufacture topology authority. New-change assignment must consume an authoritative reviewed activation state or fail with an actionable invariant error.
Safe resolution path: Remove the `pre-manifest-compatibility` admission path, require a valid manifest for topology assignment and markerless interpretation, update older test repositories with explicit v1 markers or exact baseline fixtures, and add public absent-manifest regressions that prove unchanged failure.
needs-decision rationale: none

### Finding CRG-M1-CR2

Finding ID: CRG-M1-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/new-change.js:42-71`, `packages/rigorloop/dist/lib/lifecycle-cli.js:117-140`, and `packages/rigorloop/test/fixtures/observability/v0.4.x-output-compatibility-v1.json`
Evidence: `node --test packages/rigorloop/test/result-renderer.test.js` reports 13 passed and 1 failed. The frozen `new-change-json-success` v0.4.x case differs because `planned_change_metadata.content` now includes `review_topology`; later lifecycle cases would also add topology lines and fields. Existing `specs/cli-observability-and-token-efficient-results.md` R21-R22 and AC6 require existing v0.4.x human and JSON output to remain unchanged, while the new specification requires durable explicit topology. Updating the frozen fixture alone would silently discard the existing compatibility authority.
Required outcome: The topology contract and the still-active v0.4.x public-output compatibility contract must have one explicit, testable precedence or versioning decision before M1 changes default human or JSON projections.
Safe resolution path: Route the conflict to specification ownership. Choose a compatible versioned result/schema boundary, a legacy projection that remains truthful while the written artifact gains topology, or an explicit supersession of the old compatibility window; then implement the selected behavior and make both focused topology and public compatibility suites pass.
needs-decision rationale: Specification owner must decide how the new required topology field crosses the existing frozen v0.4.x output boundary; code review cannot silently select or supersede that public contract.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-M1-CR1 violates CRG-R35; CRG-M1-CR2 exposes a same-priority spec conflict. |
| Test coverage | concern | M1 tests cover manifest values and membership but encode the absent-manifest fallback and omit the frozen public-output suite. |
| Edge cases | block | Missing authoritative manifest state produces v1 authority rather than a fail-closed result. |
| Error handling | block | Absent manifest and marker are treated as compatibility success. |
| Architecture boundaries | concern | The repository manifest boundary is implemented, but its absence is not authoritative and public projection versioning is unresolved. |
| Compatibility | block | The frozen v0.4.x compatibility suite fails directly. |
| Security/privacy | pass | No credential, secret, network, personal-data, or external-account surface was added. |
| Derived artifact currency | block | The versioned public-output fixture disagrees with runtime output; generated adapter work remains correctly deferred to M5. |
| Unrelated changes | concern | The branch contains earlier lifecycle CLI edits and untracked governing artifacts; the review is bound to the explicit M1 packet rather than a clean commit range. |
| Validation evidence | block | The three M1 commands pass, but the directly affected public-output compatibility test fails 1 of 14 cases. |

## Direct proof

```text
interpretReviewTopology({ changeId: "unlisted", manifest: null })
=> { topology: "artifact-gates-v1", source: "pre-manifest-compatibility", baseline_id: null }

node --test packages/rigorloop/test/result-renderer.test.js
=> 13 passed, 1 failed: T10 v0.4.x public output remains exact
```

## Handoff

This direct review is isolated. There is no automatic downstream handoff. `CRG-M1-CR1` is an accepted implementation correction; `CRG-M1-CR2` requires an upstream specification decision. After disposition and correction, M1 requires a fresh `code-review-m1-r2` over the changed implementation and current compatibility evidence. Workflow state remains owner-controlled.
