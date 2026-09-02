# Code Review M2 R1: Route Canonical Cutover

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: commit a4f4befa
Reviewed artifact: M2 commit a4f4befa
Reviewed milestone: M2
Review date: 2026-09-02
Status: changes-requested
Review status: changes-requested
Material findings: RFR-M2-CR1, RFR-M2-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m2-r1.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Open blockers: RFR-M2-CR1, RFR-M2-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-M2-CR1, RFR-M2-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: RFR-M2-CR1, RFR-M2-CR2
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `a4f4befa` against parent `2a345591`.
- Approved Design package: `design-review-r1`, with exact architecture, specification, and ADR members current and authority granted.
- Approved Delivery package: `delivery-review-r1`, with exact plan identity `sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d` and authority granted.
- Current milestone: M2 in `review-requested`; M3 remains planned.
- Implementation evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m2-route-canonical-cutover.md`.
- Validation evidence: all ten M2 commands passed, covering 874 focused tests plus canonical skill and generated-skill checks; 25 cache tests and direct guide/review/lifecycle validation also passed.
- Additional evidence loaded: current canonical skill and validator scans were required because TG-09 and the implementation evidence claim complete removal of current guide and old public-identity dependencies.

## Actual-diff summary

M2 replaces the canonical `workflow` package with `route`, removes `docs/workflows.md` and guide-only resources, changes the public automation parser to `$route auto:`, preserves stored workflow protocol names, updates current governance and design surfaces, refocuses the guide validator, and fixes the two allocated v3 validation defects. The package/resource and automation tests are strong, but the current-surface cutover is incomplete in stage guidance and retained guide-validation code.

## Findings

### Finding RFR-M2-CR1

Finding ID: RFR-M2-CR1
Severity: major
Location: `skills/code-review/SKILL.md:84`; `skills/plan/SKILL.md:82`; `skills/verify/SKILL.md:78`; `scripts/skill_validation.py:1039`; `scripts/skill_validation.py:1520`; `scripts/skill_validation.py:1630`; `scripts/skill_validation.py:1759`; `scripts/test-skill-validator.py:5843`
Evidence: Three current stage skills still direct artifact placement through a “project workflow guide”. The current `skill_validation` module also retains callable workflow-map and workflow-guide-skeleton validators, old guide metadata, and exact `skills/workflow`/`docs/workflows.md` diagnostics; multiple active unit tests continue to exercise those retired parsers. `python scripts/validate-guide-system.py` passes despite these current dependencies because its scan covers only six exact surfaces and searches exact legacy paths rather than semantic guide fallbacks. This contradicts RT-R19, RT-R21, RT-R33, TG-09, and the M2 evidence claim that current canonical skills and validators have no workflow-guide dependency.
Required outcome: Remove every current stage-skill workflow-guide fallback and retire the callable guide/map parsing and validation behavior, while preserving unrelated plan placement, review-recording, and historical-fixture coverage. Current validation must detect semantic guide fallback reintroduction across the canonical skill inventory.
Safe resolution path: Replace stage placement order with explicit input, authoritative CLI context or governing schema, then safe portable defaults; remove the unused workflow-map/skeleton constants and helpers plus active tests that assert their behavior; retain only explicit negative/migration fixtures; expand route/guide validation with a stage-skill fixture containing generic workflow-guide fallback text and prove it fails.
needs-decision rationale: none; the approved specification already forbids current guide consultation and preserves portable defaults.

### Finding RFR-M2-CR2

Finding ID: RFR-M2-CR2
Severity: major
Location: `skills/code-review/SKILL.md:93`; `skills/code-review/SKILL.md:194`; `skills/design-review/SKILL.md:101`; `skills/delivery-review/SKILL.md:102`; `skills/proposal-review/SKILL.md:175`; `skills/proposal-review/references/proposal-review-recording-and-settlement.md:23`; `skills/design-review/references/design-review-recording-and-settlement.md:19`; `skills/delivery-review/references/delivery-review-recording-and-settlement.md:19`; `skills/proposal/references/governed-proposal-authoring.md:11`
Evidence: Current user-facing stage guidance repeatedly names `workflow` as the actor receiving handoff, choosing continuation, owning impact handling, or receiving failures. These are public skill-actor references, not the deliberately retained `stage_authority: workflow`, `workflow.automation`, or “workflow-managed” protocol vocabulary. The route cutover tests check exact old paths and commands but do not reject these semantic old-name references. This violates RT-R1, RT-R29, RT-R33, BND-AUTH-001, and TG-09 by leaving two public actor names in the current package.
Required outcome: Current skill prose must name `route` whenever it refers to the semantic routing actor, while retaining `workflow` only for explicitly classified protocol/state vocabulary, generic process descriptions, history, and migration diagnostics.
Safe resolution path: Update the cited handoff, continuation, correction, and impact-routing sentences to `route`; add a bounded semantic old-actor scan or explicit fixture matrix that rejects “return/report/route to workflow” and “workflow owns/routes” in current published skills while allowing `workflow-managed`, `stage_authority: workflow`, `workflow.automation`, CI workflow, and historical/migration contexts.
needs-decision rationale: none; the approved rename and stable-token distinction already settle the intended vocabulary.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | RFR-M2-CR1 violates RT-R19/RT-R21 and RFR-M2-CR2 violates RT-R1/RT-R29. |
| Test coverage | block | Existing exact-string tests pass while missing semantic guide fallback and semantic old-actor cases. |
| Edge cases | pass | Route resource failure, portable/governed separation, review `not-required`, and v3 pre-plan spec cases have direct tests. |
| Error handling | pass | Missing/mixed route resources and invalid public automation commands fail closed. |
| Architecture boundaries | concern | CLI/route and stage-authority boundaries are stated correctly, but old handoff actor wording makes the current public boundary ambiguous. |
| Compatibility | pass | Stored `workflow.automation` identity, targets, budgets, receipts, and pause/cancel state remain unchanged and tested. |
| Security/privacy | pass | The M2 diff introduces no credential, logging, external, or unsafe-path surface. |
| Derived artifact currency | pass | M2 intentionally stops at canonical source; temporary generated-skill parity passes and adapter publication remains M3. |
| Unrelated changes | pass | Validator fixes and cache-policy adjustment are allocated M2 work; historical records and release archives remain unchanged. |
| Validation evidence | concern | Named commands pass, but their coverage cannot substantiate the claimed complete current-reference removal. |

## No automatic downstream handoff

This formal Code Review stops after recording. Review Resolution must accept and scope RFR-M2-CR1 and RFR-M2-CR2 before implementation correction. Neither finding requires a new product or Design decision. M2 requires rereview after correction, and M3 must not start while M2 remains open.
