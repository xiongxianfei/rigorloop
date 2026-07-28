# Boundary-First M3 Code Review R7

Review ID: code-review-m3-r7
Stage: code-review
Round: 7
Reviewer: two independent Codex code reviewers
Target: commit 95c71180
Reviewed artifact: commit 95c71180
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-M3-CR18, PBF-M3-CR19, PBF-M3-CR20, PBF-M3-CR21, PBF-M3-CR22
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: PBF-M3-CR18, PBF-M3-CR19, PBF-M3-CR20, PBF-M3-CR21, PBF-M3-CR22
- Recording status: recorded
- Reviewed milestone: M3
- Milestone closeout: not-allowed
- Remaining implementation milestones: M3, M4
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Verify readiness: not claimed

## Packet integrity and independence

Pass. Both reviewers used the exact R7 packet. Every pinned artifact and the
full `15b5f69f..95c71180` diff identity matched. The required second review is
satisfied.

## Findings

### PBF-M3-CR18

Finding ID: PBF-M3-CR18
Severity: blocker
Location: `scripts/boundary_first_validation.py`, active baseline validation
Evidence: A non-string baseline is not rejected, and any readable commit can
be declared. Direct probes accepted both an integer and a child or grandparent
revision, allowing paths outside the activating change's exact parent to be
omitted or self-grandfathered.
Required outcome: Bind active baseline identity to the exact parent of the
source-control commit that changed the manifest from pending to active, and
reject malformed, unrelated, grandparent, and child identities.
Safe resolution path: Derive the transition commit from repository history and
compare the recorded full baseline to its exact parent; add isolated-history
regressions.
needs-decision rationale: none

### PBF-M3-CR19

Finding ID: PBF-M3-CR19
Severity: blocker
Location: `scripts/boundary_first_validation.py`, release selection
Evidence: Rollback release is compared only with
`dist/adapters/manifest.yaml#version`. Equal activating and rollback releases,
nonexistent activating tags, and skipped older releases can pass.
Required outcome: Prove both tags exist in a repository-owned published-release
ordering and that rollback is the immediate predecessor of activation.
Safe resolution path: Use immutable repository tags as the ordering authority,
with direct equality, nonexistent, skipped, malformed, and success fixtures.
needs-decision rationale: none

### PBF-M3-CR20

Finding ID: PBF-M3-CR20
Severity: major
Location: `scripts/boundary_first_validation.py`, adapter manifest authority
Evidence: A symlinked `dist/` ancestor can redirect the adapter manifest read
outside the repository.
Required outcome: Reject a leaf or ancestor symlink and any resolved path
outside the repository before reading the adapter manifest.
Safe resolution path: Apply one repository-contained regular-file guard and
add immutable outside-sentinel regressions.
needs-decision rationale: none

### PBF-M3-CR21

Finding ID: PBF-M3-CR21
Severity: major
Location: `scripts/boundary_first_validation.py`, baseline tree enumeration
Evidence: Default `git ls-tree` quoting converts a Unicode path such as
`specs/é.md` into an escaped quoted string, which is silently excluded.
Required outcome: Enumerate raw NUL-delimited Git paths and sort decoded paths
by raw UTF-8 bytes.
Safe resolution path: Use `git ls-tree -z` and add a Unicode-path regression.
needs-decision rationale: none

### PBF-M3-CR22

Finding ID: PBF-M3-CR22
Severity: major
Location: `scripts/boundary_first_validation.py`, baseline tree modes
Evidence: A mode-`120000` symlink blob containing accepted-looking Markdown is
treated as an eligible historical feature spec.
Required outcome: Accept only regular blob modes before reading baseline
content.
Safe resolution path: Parse the NUL-delimited tree mode and reject symlink or
non-blob entries with a direct regression.
needs-decision rationale: none

## Verified clean

Two-state vocabulary, pending sentinels, pending marker rejection, ASCII
lifecycle coverage, declared-revision child exclusion, manifest-entry ordering,
live-path containment, unknown closed values, and removal of receipt, writer,
transaction, and attestation authority behave as intended.

## Recommendation

Apply one bounded M3 correction covering PBF-M3-CR18 through PBF-M3-CR22, rerun
targeted validation, and return M3 to independent review. M4 remains blocked.
