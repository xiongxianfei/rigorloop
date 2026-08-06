# Usability-First Boundary-First v0.4.0 Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: c7b0babe..d672c40f
Reviewed artifact: commit d672c40f
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-implementation
Reviewer context ID: m3-r1-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: routine-release-identity; generated-artifact-reproducibility; trusted-publication-authority; rollback-and-recovery
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@d672c40f#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@d672c40f#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@d672c40f#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@d672c40f#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@d672c40f#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@d672c40f#sha256:160a6688fbcbfcff2a9e0783700a221f5bceda86b8af7c7b658354278a19ca3c; range:c7b0babe..d672c40f.diff@d672c40f#sha256:ee70ac432f499b64860c9c1386663b2546f90fdd601754e6e415e00cd2052525
Prompt template version: code-review-v1
Initial packet hash: sha256:ee70ac432f499b64860c9c1386663b2546f90fdd601754e6e415e00cd2052525
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: routine v0.4.0 identity; generated release evidence; package and archive selection; release validation; pending/public separation
Highest-impact failure modes: prepared-output drift; ambient npm tag redirection; unbound tag commit; incomplete standing evidence; mixed release identities; false public claims
Changed boundaries: BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; BND-STATE-001; INT-002; INT-003
Evidence expected: deterministic final preparation; exact identity binding; reproducible archives; three-target packed smoke; pending-state and rollback proof; both executable release gates
Areas requiring direct inspection: release profile and generated surfaces; adapter and package metadata; closed release sets; standing gate; trusted workflow; activation and rollback records; closeout tooling
Areas intentionally out of scope: M4 active snapshot; live tag or publication; final holistic review; explain-change; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; release-identity-and-authority=applicable; generated-artifact-reproducibility=applicable; package-supply-chain=applicable; recovery-and-rollback=applicable; privacy=applicable; live-publication=not-applicable:out-of-scope-M3; active-snapshot-authoring=not-applicable:owned-by-M4
Falsifiable review questions: Does the final reviewed tree pass preparation drift checks? Can ambient npm configuration change the required latest tag? Does the trusted gate independently bind the immutable tag commit? Is every architecture-required standing release surface present?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: docs/releases/profiles/v0.4.0.yaml; docs/releases/v0.4.0/; docs/reports/adapter-artifacts/releases/v0.4.0.yaml; packages/rigorloop/; scripts/adapter_distribution.py; scripts/release-verify.sh; tests/fixtures/release-transaction/current-version.json
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*
Requirement-fidelity matched category triggers: spec-derived validators; metadata validators; generated-output or package parity validators; closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M3-CR1-001 through UBR-M3-CR1-004
Material findings: UBR-M3-CR1-001, UBR-M3-CR1-002, UBR-M3-CR1-003, UBR-M3-CR1-004
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR1-001 through UBR-M3-CR1-004
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR1-001, UBR-M3-CR1-002, UBR-M3-CR1-003, UBR-M3-CR1-004
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR1-001, UBR-M3-CR1-002, UBR-M3-CR1-003, UBR-M3-CR1-004
- Verify readiness: not-claimed

## Finding UBR-M3-CR1-001

Finding ID: UBR-M3-CR1-001
Severity: blocker
Location: `scripts/release_transaction.py:1425-1478`, `scripts/release_transaction.py:1586-1621`
Evidence: `python scripts/prepare-release.py v0.4.0 --check` exits 1 on the reviewed final tree and would rewrite the bundled release index, release YAML, and adapter artifact report. The implementation receipt records CMD11 only before finalization edits.
Required outcome: The reviewed final pre-publication tree is reproducible and passes CMD11.
Safe resolution path: Give archive-derived finalization deterministic generator ownership, or explicitly separate generated placeholders from finalized evidence without overwriting valid final values; add a post-finalization regression.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M3-CR1-002

Finding ID: UBR-M3-CR1-002
Severity: blocker
Location: `docs/releases/profiles/v0.4.0.yaml`, `scripts/release_transaction.py:28-39`, `scripts/release_transaction.py:109-122`, `.github/workflows/release.yml:67-83`
Evidence: The profile/schema have no npm dist-tag field, and trusted publication omits `--tag latest`. Ambient `NPM_CONFIG_TAG=next` can therefore redirect publication even though later evidence expects `latest`.
Required outcome: The profile owns the closed `latest` value and trusted publication uses that exact value.
Safe resolution path: Add and validate a profile dist-tag field, propagate it through preparation/evidence, publish with the profile-owned tag, and regress unknown or ambient overrides.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M3-CR1-003

Finding ID: UBR-M3-CR1-003
Severity: blocker
Location: `scripts/release-verify.sh:64-82`, `scripts/release-verify.sh:102-106`, `.github/workflows/release.yml:21-29`, `.github/workflows/release.yml:67-80`
Evidence: The standing gate reads `release_commit` from the adapter report and supplies that same value as the validator's expected commit. Trusted workflow supplies no independent checked tag/HEAD identity, so self-consistent metadata can name a different commit and pass.
Required outcome: Trusted-tag verification independently binds the checked tag/HEAD SHA to the exact full reviewed release commit and rejects missing, abbreviated, rewritten, or mismatched identity.
Safe resolution path: Record the final full reviewed release commit in M4, compare it with checked-out HEAD or trusted workflow SHA in the standing gate, and add missing/mismatch/rewritten-tag contract fixtures.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M3-CR1-004

Finding ID: UBR-M3-CR1-004
Severity: major
Location: missing `docs/releases/v0.4.0.md`; `docs/plans/2026-08-06-usability-first-boundary-release.md:170-181`; `docs/architecture/system/architecture.md:887-889`
Evidence: M3 names `docs/releases/v0.4.0.md` as a release payload surface, and the accepted architecture assigns it the standing release-process record. The file is absent.
Required outcome: Add the pending standing v0.4.0 release record with architecture-required identity, gate, recovery, follow-up, and privacy sections.
Safe resolution path: Derive the record from the established v0.3.6 shape, keeping publication and registry facts pending until public closeout, and validate its presence/content.
needs-decision rationale: none
auto_fix_class: mechanical

## Checklist coverage

- Spec alignment: block; UBR-R009, UBR-R011, and UBR-R020 are incomplete.
- Test coverage: block; final-state CMD11 and independent tag-binding regressions are missing.
- Edge cases: block; ambient npm tag and mismatched tag commit remain open.
- Error handling: concern; valid finalized evidence is currently reported as generator drift.
- Architecture boundaries: block; the standing release record is absent.
- Compatibility: pass; the existing routine path and v0.3.6 rollback remain present.
- Security/privacy: pass for the reviewed evidence; no secret or machine-local path was found.
- Derived artifact currency: block; final preparation check fails.
- Unrelated changes: pass; the diff is scoped to the M3 payload and routing evidence.
- Validation evidence: concern; focused suites and full release gate pass, but required CMD11 fails on the review head.

## Independent evidence

- Independently rebuilt all three archives from the recorded full source commit; archive hashes, tree hashes, file counts, and bundled metadata digest match.
- Release transaction, adapter distribution, npm package, recorded-source release validation, selector, full release verification, diff, and privacy checks passed.
- `python scripts/prepare-release.py v0.4.0 --check` failed and reproduced UBR-M3-CR1-001.
- The broad release-CI bundle was not independently repeated; the reviewer challenged its focused and standing-gate constituents directly.

## Handoff

M3 remains open. Resolve all four findings, rerun the complete M3 command set, and request an independent M3 R2 review. M4 remains blocked until M3 receives a clean review.
