# Explain Change: Vision Skill Progressive Disclosure

## Summary

The vision skill now loads only the procedure needed for a particular invocation. Universal authority and safety remain in a compact `SKILL.md`; strategic authoring and README synchronization have independent references; canonical vision and strategic-positioning structure have separate copied assets. The accepted behavior did not change: `VISION.md` remains canonical, README synchronization remains default, exact skip authority remains fail-closed, and multi-file work remains identity-bound and recoverable.

Every supported procedural assembly is smaller than the former 2,268-word / 15,845-byte flat skill. The complete package is 2,243 words / 17,176 bytes because it now includes two explicit structural assets; that 8.4% byte growth is recorded rather than presented as deletion.

Final verify R1 subsequently exposed a durable-review formatting defect rather than a vision-package defect: two material findings were present only as Markdown headings, while the repository parser requires explicit `Finding ID:` fields. The bounded correction made both records discoverable, added explicit closeout links to their existing approving rereviews, and reconciled one stale evidence sentence without changing either judgment or the shipped skill package.

## Problem

The former single 2,268-word skill mixed universal authority, strategic positioning, full vision drafting, README marker mechanics, output structure, and recovery. README-only synchronization and narrow editorial revision therefore loaded substantial irrelevant strategic procedure, while repeated artifact structure had no distinct owner. The goal was to reduce real loaded context without weakening source precedence, marker safety, strategic quality, recovery, or claims.

## Decision trail

- Exploration/option: proposal Option 4 selected two independent procedural references and two structural assets. Keeping the flat file, editorial compression alone, one catch-all reference, and highly fragmented or executable machinery were rejected.
- Proposal: preserve exactly three mutation operations, classify strategic and README needs independently, represent six assemblies, keep README synchronization as default, and use identity-bound source-first manifests.
- Specification: R1-R66 define package inventory, universal/conditional ownership, operation and action vocabularies, authority, markers, assets, manifests, recovery, measurement, parity, acceptance exclusions, and architecture fallback.
- Architecture: `architecture-not-required`; the change reuses the existing mapped-resource package model and authorized Markdown evidence. Unsupported durable recovery explicitly requires architecture before planning.
- Plan: M1 froze rule/literal ownership and baselines; M2 implemented and reviewed the package split; M3 proved profile reduction and distribution parity.

## Diff rationale by area

| Area/files | Change | Reason | Source | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/vision/SKILL.md` | Reduced the universal contract to operations, state, authority, resource selection, actions, manifest/recovery, safety, claims, and results. | Every invocation needs these rules; hiding them behind a trigger would weaken safety. | R2, R5-R17, R20-R33, R40-R57, R66 | T-VIS-001-T-VIS-011, C1-C3, M2 evidence |
| `skills/vision/references/strategic-vision-authoring.md` | Moved positioning, category/methodology framing, content quality, word limits, and drafting heuristics. | Strategic procedure is needed for establishment and substantive work, not ordinary sync. | R3, R15-R17 | T-VIS-001, T-VIS-003, C2 |
| `skills/vision/references/readme-vision-sync.md` | Moved marker parsing, insertion, derivation, bounded replacement, preservation, and idempotence. | README mechanics are an independent activation boundary and do not grant authority. | R4, R18-R27 | T-VIS-003, T-VIS-004, C2 |
| `skills/vision/assets/*.md` | Added separate canonical vision and strategic-positioning skeletons. | Stable headings and placeholders need explicit structural owners without carrying policy. | R34-R39 | T-VIS-006, C1-C2 |
| `scripts/test-skill-validator.py` | Updated existing consumers to inspect applicable package resources and added six focused simplification tests. | Preserve exact compatibility while directly checking package inventory, assemblies, owners, assets, manifests, recovery, architecture fallback, and profile reduction. | R58-R63 | T-VIS-001-T-VIS-015, C0-C3 |
| M1 ledgers and fixtures | Recorded 32 semantic rules, 32 compatibility literals, unknown-value failures, scenarios, and the exact flat baseline. | Semantic meaning and exact consumed strings need separate pre-edit evidence. | R58-R60 | C0; M1 review |
| M2/M3 evidence | Recorded implementation, review correction, measurements, preservation, hashes, boundary proof, and package-chain results. | Relocation must be reviewable and total package cost must remain visible. | R43-R66 | C1-C8; M2/M3 reviews |
| Proposal, spec, plan, test spec, change record, reviews | Captured the accepted decision and stage-owned lifecycle from proposal through final review. | The change is non-trivial and governed; durable rationale and state must match the implementation. | workflow contract | metadata validation and final review R3 |
| Verify R1 correction records | Added parser-owned finding fields, explicit blocking-review closeouts, correction evidence, and final rereview R4. | PR-mode lifecycle validation must discover every durable finding and its settlement without changing historical semantics. | formal review recording contract | structure and closeout validation; PR-scope lifecycle validation; final review R4 |

## Tests added or changed

- `VisionSkillProgressiveDisclosureLedgerTests` proves closed semantic/literal ownership, unknown-value-first behavior, six assembly formulas, scenario completeness, architecture triggers, and the exact baseline.
- `VisionSkillProgressiveDisclosureTests` proves the final five-file inventory, exact `READ`/`COPY` mappings, all six assemblies, universal inline authority, distinct references, policy-free assets, governed manifest persistence, zero-write skip truthfulness, architecture fallback, recovery, and profile reduction.
- Existing vision contract tests now read the applicable package resources, preserving compatibility-sensitive phrases without requiring all procedure to remain inline.
- T-VIS-001 through T-VIS-015 map these contract tests plus build, adapter, boundary, and lifecycle commands to R1-R66. The level is appropriate because the change is a published Markdown package contract, not a runtime feature.

## Validation evidence available before final verify

| Command | Available result |
| --- | --- |
| `python scripts/validate-skills.py skills/vision/SKILL.md` | pass |
| `python scripts/test-skill-validator.py` | pass; 408 tests, 16 expected skips |
| `python scripts/test-build-skills.py` | pass; 7 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/test-adapter-distribution.py` | pass; 150 tests |
| `python scripts/validate-boundary-first.py --check --path specs/vision-skill-progressive-disclosure.md` | pass |
| `python scripts/validate-change-metadata.py docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml` | pass |
| `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-17-vision-skill-progressive-disclosure` | pass after verify R1 correction; 17 reviews, 12 findings, 17 log entries, 12 resolution entries |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-17-vision-skill-progressive-disclosure` | pass after verify R1 correction; all 12 findings closed |
| `python scripts/validate-artifact-lifecycle.py --mode pr-ci --base origin/main --head HEAD` | pass after verify R1 correction; three PR-scope artifact files validated with baseline warnings only |

Verify R1 ran the complete C0-C9 ledger but C9 failed on the now-corrected finding-discovery defect. That failed occurrence remains recorded in `verify-report.md`. A new final PR-mode CI run and branch-readiness judgment are still required and remain owned by `verify`.

## Review resolution summary

The durable [review resolution](review-resolution.md) contains 12 material findings: 12 accepted, 0 rejected, 0 deferred, 0 partially accepted, and 0 `needs-decision`; all are closed. Implementation review `VIS-M2-CR1` restored durable governed manifest preparation, architecture fallback, and complete zero-write settlement. Final review `VIS-FINAL-CR1` reconciled the overview and approving rereview evidence. Verify R1 then exposed their missing parser-owned identity fields; the bounded recording correction preserved both findings and final holistic rereview R4 approved the resulting full branch.

## Alternatives rejected

- Keep the flat package: lowest migration risk but preserves maximum context cost and mixed ownership.
- Compress only `SKILL.md`: reduces bytes but does not create real progressive disclosure and risks obscuring safety.
- One catch-all reference: still forces README and strategic procedure to load together.
- Many narrow references or executable machinery: increases navigation, missing-resource, portability, architecture, and acceptance complexity without proportional value.

## Scope control

The change does not alter project vision content, README front-matter, canonical paths, public result vocabulary, word limits, proposal-fit behavior, or historical artifacts. It adds no runtime router, synchronization script, parser, transaction service, lifecycle state, policy owner, tokenizer, target-agent evaluation, transcript grading, or manual semantic-review gate. No unrelated skill was optimized.

## Risks and follow-ups

- The VA2 byte margin is intentionally small: 15,735 versus 15,845. Focused measurement tests must remain active so future universal growth is visible.
- Total package bytes increased because structure is explicit. Future optimization should not collapse assets back into procedural prose merely to improve total size.
- Package changes must continue through the existing build/archive/install parity checks.
- The shared code-review material-finding asset still uses bulleted field labels while the current parser recognizes unbulleted field lines. That cross-package mismatch should be handled as a separate scoped bugfix rather than expanding this vision change.
- No follow-up is required for the vision implementation; a new final verification occurrence remains pending.

## Verify readiness

All implementation milestones and review resolutions are closed, final holistic rereview R4 is clean, the verify R1 recording correction passes focused lifecycle validation, and this explanation is current. The change is ready for a new `verify` invocation. Verify R1 remains a failed historical occurrence, so verification, CI, branch, and PR readiness are not claimed here.
