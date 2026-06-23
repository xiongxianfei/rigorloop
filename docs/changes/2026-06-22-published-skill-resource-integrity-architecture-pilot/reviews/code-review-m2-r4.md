# Code Review M2 R4: Published Skill Resource Integrity Architecture Pilot

Review ID: code-review-m2-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: commit `007ebdf`
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r4.md`; `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`; `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`; `docs/plan.md`; `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: implement M3
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r4.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5, M6, M7
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review status

clean-with-notes

## Review inputs

- Diff/review surface: commit `007ebdf` (`Resolve M2 instruction segmentation review`)
- Tracked governing branch state: branch `proposal/published-skill-resource-integrity`
- Governing artifacts: `specs/skill-contract.md` R49-R49d; `specs/skill-contract.test.md` T43; active plan M2; `review-resolution.md` SRI-M2-CR3 disposition
- Validation evidence:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design`
  - `python scripts/test-build-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plan.md --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/validator-fixtures.md --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
  - `git diff --check --`

## Diff summary

The implementation replaces broad contiguous-line assembly with bounded `ResourceInstructionSegment` segmentation. The legacy-resource lint now evaluates resource-loading intent within one prose paragraph or one Markdown list item plus continuation lines. New list items, blank lines, headings, fenced blocks, and `## Resource map` boundaries terminate the segment.

The tests add direct coverage for the CR3 false-positive boundary and preserve CR2 behavior for same-line, wrapped prose, wrapped list-item, reverse-order, individually qualified, illustrative, Resource map, and exact temporary-exception cases. `validator-fixtures.md`, `review-resolution.md`, `review-log.md`, active plan state, and change metadata were updated for the SRI-M2-CR3 resolution handoff.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R49-R49d require bounded legacy-reference lint without broad path scanning. The segmenter limits loading intent to one paragraph or one list item and leaves mapped resources to mapped validation. |
| Test coverage | pass | `scripts/test-skill-validator.py` adds direct CR3 boundary tests for separate unordered and ordered list items, separate paragraphs, heading boundaries, fenced examples, Resource map exclusion, and exact exception adjacency. |
| Edge cases | pass | The reviewed tests preserve same-line, wrapped prose, wrapped list-item, reverse-order mixed references, individually qualified references, illustrative examples, and exact temporary architecture exceptions. |
| Error handling | pass | Diagnostics still identify the specific unmapped path, while mapped-resource verb/class, containment, existence, and packageability checks are unchanged. |
| Architecture boundaries | pass | The diff does not normalize architecture resources, change package parity, change clean-install behavior, or move architecture policy out of `SKILL.md`. |
| Compatibility | pass | No new parser dependency is introduced; the segmenter is bounded and existing project-provided helper compatibility remains narrowly scoped. |
| Security/privacy | pass | The change only classifies local skill-resource references and does not introduce network loading, secret handling, or new runtime trust boundaries. |
| Derived artifact currency | pass | `python scripts/test-build-skills.py` passed; generated-resource parity is not part of M2 and remains scheduled for later milestones. |
| Unrelated changes | pass | The diff is scoped to validator segmentation, validator tests, fixture evidence, and lifecycle records for the M2 review-resolution. |
| Validation evidence | pass | The recorded validator, skill, selected, generated-skill, lifecycle, review-artifact, metadata, and whitespace checks are relevant to the M2 surface. |

## No-finding rationale

SRI-M2-CR3 asked for an instruction-boundary model so a loading verb in one Markdown structure cannot make a resource-looking artifact string in another structure operative. The implementation supplies that boundary and tests both sides: genuine wrapped instructions still fail for unqualified resource references, while separate list items, paragraphs, headings, fences, and Resource map entries no longer inherit loading intent.

The prior CR1 and CR2 protections remain covered: ordinary conditional wording no longer suppresses resource lint, external ownership is still path-specific, and the temporary architecture migration exception remains exact by skill, path, and approved instruction text.

## Residual risks

The segmenter is intentionally a bounded Markdown recognizer, not a full Markdown parser. That is acceptable for this lint because the contract is bounded to recognized resource-loading instructions and approved skill-local prefixes, and the current edge-case matrix covers the known false-negative and false-positive boundaries.

## Milestone handoff

- Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
- Milestone state after review: closed
- Required review-resolution: no
- Remaining implementation milestones: M3, M4, M5, M6, M7
- Next stage: implement M3
- Final closeout readiness: not ready; implementation milestones remain and explain-change, verify, and PR handoff have not run.
