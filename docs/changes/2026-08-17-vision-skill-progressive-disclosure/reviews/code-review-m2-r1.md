# Code Review M2 R1: Vision Skill Progressive Disclosure

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M2 range `f89b954a..4a362d1d`
Reviewed milestone: M2
Reviewed artifact: commit `4a362d1d`
Review date: 2026-08-17
Status: changes-requested
Material findings: VIS-M2-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: VIS-M2-CR1
- Next stage: review-resolution, then implement correction
- Review status: changes-requested
- Material findings: VIS-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-log.md`
- Review resolution: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: open
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: VIS-M2-CR1
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact M2 risks were moving universal authority behind conditional procedure, under-specifying the no-reference skip, omitting prepared governed recovery evidence, introducing policy-bearing assets, weakening legacy compatibility, or presenting relocation as deletion. Direct inspection covered the complete M2 diff, approved R1-R60 contract, proof map, ledgers, resource mappings, assets, focused scenarios, compatibility assertions, and recorded commands.

## Material findings

### VIS-M2-CR1 — Major: the governed prepared-manifest and zero-write settlement contract is incomplete

Finding ID: VIS-M2-CR1
Severity: major
Location: `skills/vision/SKILL.md`, `scripts/test-skill-validator.py`, and `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m2-package-implementation.md`
Evidence: `skills/vision/SKILL.md:77-81` requires resolving a manifest before writes, but does not require governed work to persist the complete manifest in authorized change-local authoring evidence before the first target write as required by R54. The same passage does not state the R46 requirement that zero-write sync skip records equal prior and intended identities for the unchanged canonical vision target, or the complete R52 truth condition of no changed files and no synchronization claim. The focused tests assert general preparation and retry phrases but do not reject these omissions.

Impact: an interrupted governed multi-file operation could lack the durable basis needed for exact retry, while a zero-write skip could claim completion without the complete identity and result evidence required by the approved contract. The implementation evidence currently overstates this behavior as proved.

Required outcome: keep the contract inline and compact, but require durable governed manifest preparation before the first write when the existing evidence model supports it; explicitly bind equal prior/intended canonical identities for zero-write sync skip; require zero changed files and prohibit synchronization or marker-validity claims; and add focused assertions that fail when these obligations disappear.

Safe resolution: amend only the main vision skill, focused validator, and M2 evidence; rerun C1-C5 and metadata validation; then perform a fresh M2 rereview.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | fail | R46, R52, and R54 are not fully projected into the shipped contract. |
| Test coverage | concern | Focused tests do not reject loss of durable governed preparation or complete zero-write truth. |
| Edge cases | concern | Interruption after the first governed write and zero-write settlement are under-specified. |
| Error handling | pass | Missing resources, conflicts, concurrency, and portable lost-context recovery fail closed. |
| Architecture boundaries | pass with correction | The intended fix uses existing authorized Markdown evidence and needs no new persistence owner. |
| Compatibility | pass | Existing consumed phrases, paths, markers, verbs, headings, and result vocabulary remain available. |
| Security/privacy | pass | The refactor retains privacy and research boundaries and adds no external behavior. |
| Derived artifact currency | pass for M2 | Build tests and check mode pass; full package-chain proof remains M3. |
| Unrelated changes | pass | The implementation range is limited to the vision package, focused validators, and M2 evidence. |
| Validation evidence | pass but insufficient | C1-C5 pass, but they do not cover the missing obligations. |

## Claim limitations

This review does not close M2 or claim final package parity, verification, branch, CI, or PR readiness.
