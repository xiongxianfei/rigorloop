# Code Review M3 R1: Adapter and Release Parity

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: commit 658a6a05
Reviewed artifact: M3 commit 658a6a05
Reviewed milestone: M3
Review date: 2026-09-02
Status: changes-requested
Review status: changes-requested
Material findings: RFR-M3-CR1, RFR-M3-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m3-r1.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`
- Open blockers: RFR-M3-CR1, RFR-M3-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-M3-CR1, RFR-M3-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3
- Required review-resolution: yes
- Finding IDs: RFR-M3-CR1, RFR-M3-CR2
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `658a6a05` against parent `c30757df`.
- Approved Design package: `design-review-r1`, with exact architecture, specification, and ADR members current and authority granted.
- Approved Delivery package: `delivery-review-r1`, with exact plan identity `sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d` and authority granted.
- Current milestone: M3 in `review-requested`; no later implementation milestone exists.
- Implementation evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m3-adapter-and-release-parity.md`.
- Validation evidence: all seven M3 commands passed, including 155 adapter tests, 363 passing package tests with 2 historical skips, and 11 broad-smoke checks.
- Additional evidence loaded: published v0.5.0 release notes, adapter metadata, CLI bundled release index, lockfile drift behavior, and current package version were needed because TG-13 and TG-15 require migration and current-versus-historical release coherence.

## Actual-diff summary

M3 changes supported adapter inventories and invocation portability from workflow to route, removes guide fixtures from token benchmarks, adds obsolete and mixed workflow-package detection to target init, documents the migration, and records clean generated/archive validation. Temporary generated adapters are route-only and the implementation does not modify historical release archives. The package runtime and migration guidance, however, do not compose with existing released metadata or lockfile-managed installations.

## Findings

### Finding RFR-M3-CR1

Finding ID: RFR-M3-CR1
Severity: major
Location: `packages/rigorloop/package.json:3`; `packages/rigorloop/dist/metadata/releases.json:33`; `packages/rigorloop/README.md:73`; `packages/rigorloop/README.md:78`; `packages/rigorloop/dist/bin/rigorloop.js:2032`
Evidence: The changed CLI package remains version `0.5.0` and therefore selects bundled metadata for the already-published v0.5.0 archives. The tracked v0.5.0 release notes explicitly say the workflow-to-route implementation is not part of that release, and the published release's adapter support manifest contains `workflow`. The new archive preflight rejects any archive containing that package. Consequently the README's statement that current archives install route is false, and its pinned `npx ...@0.5.0 init` examples select an archive the changed CLI rejects. Tests pass by injecting synthetic current-route metadata and do not exercise the package's real bundled release identity. This violates RT-R29-RT-R32, TG-13-TG-15, and M3's no-publication/no-availability-claim boundary.
Required outcome: Bind the route-only candidate and its CLI installer to one unpublished release identity distinct from immutable v0.5.0, keep the published v0.5.0 metadata byte-stable, make package documentation distinguish published from candidate behavior, and add direct proof that the real bundled candidate metadata selects archives whose inventory passes the new route/workflow preflight. Publication remains out of scope.
Safe resolution path: Prepare the next repository-owned unpublished package/release metadata identity through the existing release tooling; generate route-only candidate archives and metadata into temporary validation output; update package version/index/docs only for that candidate; add a test using the actual bundled candidate metadata rather than an injected fixture; rerun M3 and release-oriented validation without publishing.
needs-decision rationale: none; immutable v0.5.0 cannot be repurposed, while the exact publish operation remains explicitly outside M3.

### Finding RFR-M3-CR2

Finding ID: RFR-M3-CR2
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:1245`; `packages/rigorloop/dist/bin/rigorloop.js:1260`; `packages/rigorloop/dist/bin/rigorloop.js:2011`; `packages/rigorloop/dist/bin/rigorloop.js:2041`; `packages/rigorloop/test/cli.test.js:1227`; `packages/rigorloop/README.md:73`
Evidence: Obsolete-package detection tells every user to remove only `<install-root>/workflow` and rerun init. For a stateful install, `rigorloop.lock` hashes the complete install root. Removing that directory makes the recorded tree drift, and the next init invokes existing-state safety and stops on `generated-output-drift` or `generated-output-missing` before installation. The added tests create unmanaged bare skill folders and therefore do not cover the documented remediation for a lockfile-managed install. The diagnostic is deterministic but leads managed users into a second blocker instead of an actionable upgrade path, leaving TG-13 and BND-RECOVERY-001 unproved.
Required outcome: Obsolete and mixed package diagnostics must provide a safe, executable remediation for both unmanaged and lockfile-managed installs without deleting unrelated adapter state, and direct tests must prove the complete remove/retry or upgrade sequence leaves one coherent route package and compatible lifecycle automation state.
Safe resolution path: Add an explicit bounded migration or replacement path that validates the old managed tree before changing its recorded target, or return state-aware instructions that identify the exact existing lifecycle operation needed to update only the selected target. Exercise intact managed workflow state, interrupted remediation, retry, and unrelated-target preservation in CLI tests.
needs-decision rationale: none; the approved architecture already requires deterministic stale-install diagnostics, coherent upgrade, and recovery without historical archive rewriting.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | RFR-M3-CR1 breaks current package/release coherence; RFR-M3-CR2 leaves RT-R30 recovery incomplete. |
| Test coverage | block | Synthetic archive tests omit real bundled metadata and lockfile-managed migration. |
| Edge cases | block | Existing managed install and remove/retry behavior are not proved. |
| Error handling | concern | Obsolete input stops before mutation, but the prescribed recovery produces a second blocker for managed state. |
| Architecture boundaries | pass | Canonical skills remain authored under `skills/`; generated bodies are temporary and CLI does not gain semantic routing authority. |
| Compatibility | block | Immutable v0.5.0 identity is selected for behavior that v0.5.0 did not ship. |
| Security/privacy | pass | Diagnostics expose repository-relative paths and bounded protocol names only. |
| Derived artifact currency | concern | Temporary route packages are coherent, but package-bundled release metadata still resolves the old archive generation. |
| Unrelated changes | pass | Changes are within M3 adapter, installer, documentation, benchmark, and evidence scope. |
| Validation evidence | concern | Commands passed, but fixture substitution prevents them from proving the deployed package and managed-upgrade paths. |

## No automatic downstream handoff

This formal Code Review stops after recording. Review Resolution must accept and scope RFR-M3-CR1 and RFR-M3-CR2 before implementation correction. M3 requires rereview after correction; final holistic Code Review and Verify cannot start while M3 remains open.
