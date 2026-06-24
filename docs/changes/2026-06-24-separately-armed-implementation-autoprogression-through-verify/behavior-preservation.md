# Behavior Preservation: Implementation Autoprogression Through Verify

## Scope

This evidence closes M5 for the first implementation slice of separately armed implementation autoprogression.

It proves that the implementation adds a change-local, separately authorized `implementation-through-verify` policy and Phase A/B route evaluation without widening authoring autoprogression, inventing `test-spec-review`, repairing verify failures automatically, or crossing the PR boundary.

## Validation Inputs

| Milestone | Evidence |
| --- | --- |
| M1 profile policy | `python scripts/test-change-metadata-validator.py`, change metadata schema validation, and code-review-m1-r2. |
| M2 route and settlement evaluation | `python scripts/test-artifact-lifecycle-validator.py -k implementation_profile`, full artifact lifecycle tests, and code-review-m2-r1. |
| M3 reviewer classification and correction guardrails | `python scripts/test-review-artifact-validator.py`, `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails`, review-resolution closeout, and code-review-m3-r2. |
| M4 public skills and generated adapter support | `python scripts/test-skill-validator.py -k implementation_through_verify_public_skill_surfaces`, `python scripts/build-skills.py --check`, adapter archive build/validation, `python scripts/test-adapter-distribution.py`, and code-review-m4-r1. |

## Behavior Preservation Matrix

| Surface | Baseline | New proof | Result |
| --- | --- | --- | --- |
| Profile off | Existing workflow requires explicit stage routing after `test-spec`; no implementation automation is implied. | `ITV-001`, `ITV-035`, `AC-ITV-002`, and `AC-ITV-023` are covered by policy defaults, unknown-profile failure, and behavior-preservation evidence. | preserved |
| Authoring autoprogression | `authoring-through-plan-review` stops after clean `plan-review`. | `ITV-002`, `ITV-037`, and `AC-ITV-001` prove implementation authorization is a separate record and cannot be inherited from authoring. | preserved |
| Change-local profile | Automation policy is scoped to the change metadata record. | `AC-ITV-002`, `AC-ITV-025`, and `ITV-003` prove closed values, phase persistence, and fail-closed unknown values. | strengthened |
| Activation gates | Clean planning and synchronized state are required before downstream execution. | `ITV-004`, `ITV-005`, `ITV-036`, and `AC-ITV-024` prove plan-review approval, dirty-state stop, phase boundaries, and promotion-evidence refusal. | strengthened |
| Test-spec settlement | No formal review stage exists between `test-spec` and implementation. | `ITV-006`, `ITV-007`, `ITV-008`, `ITV-038`, and `AC-ITV-003` prove deterministic settlement, no gaps, static absence of a `test-spec-review` skill or stage, and first-review identity recheck. | extended without topology change |
| No test-spec-review stage | There is no `test-spec-review` skill or stage in the workflow topology. | Static validator check confirms no `skills/test-spec-review/SKILL.md`, `.agents/skills/test-spec-review/SKILL.md`, lifecycle stage enum, or workflow stage row is introduced. | preserved |
| Milestone order | Milestones run one at a time, in approved order. | `ITV-009`, `ITV-010`, `ITV-022`, `ITV-033`, `AC-ITV-004`, `AC-ITV-014`, and `AC-ITV-021` are covered by route fixtures, independent code-review records, and handoff synchronization. | strengthened |
| Reviewer classification | Reviewers own auto-fix eligibility. | `ITV-011`, `ITV-012`, `ITV-013`, `ITV-014`, `AC-ITV-005`, `AC-ITV-006`, `AC-ITV-007`, and `AC-ITV-008` are covered by review-artifact parser checks and correction guardrail fixtures. | strengthened |
| Owner decisions | Owner-intent choices remain manual. | `ITV-014` proves owner-decision findings pause; no workflow route chooses between alternatives. | preserved |
| Correction loop convergence | Automatic fixes must be bounded, shrinking, path-local, and auditable. | `ITV-015`, `ITV-016`, `ITV-017`, `ITV-018`, `ITV-019`, `ITV-020`, `ITV-021`, `ITV-034`, `AC-ITV-009`, `AC-ITV-010`, `AC-ITV-011`, `AC-ITV-012`, `AC-ITV-013`, and `AC-ITV-022` are covered by correction guardrail fixtures and review-resolution evidence. | strengthened |
| CI maintenance | CI changes can hide external-boundary risk. | `ITV-025` and `ITV-039` prove automatic CI maintenance pauses unless CI files are enumerated and deny-list checks pass. | strengthened |
| Review independence | Implementation cannot self-approve. | `ITV-010`, `ITV-022`, and `AC-ITV-014` are backed by per-milestone code-review records and public skill guidance requiring context-reset evidence and final full review. | strengthened |
| Final review before closeout | Explain-change cannot start from a targeted rereview alone. | `ITV-023`, `ITV-024`, and `AC-ITV-015` are covered by Phase B boundary routing and M4 skill-surface proof. | strengthened |
| Explain-change | Explanation remains after clean implementation review and before verify. | `ITV-026` and `AC-ITV-016` are covered by public explain-change guidance requiring the final reviewed diff. | extended |
| Fresh verify | Final verify must use current evidence. | `ITV-027`, `ITV-028`, `ITV-029`, `ITV-030`, `AC-ITV-017`, `AC-ITV-018`, and `AC-ITV-019` are covered by Phase C route design and M4 skill-surface proof. Not enabled in first slice. | designed and guarded |
| PR boundary | Opening a PR is external. | `ITV-031` and `AC-ITV-020` are covered by Phase C stop-before-PR guidance and non-goal enforcement. | preserved |
| Bugfix and manual skill invocations | Manual invocations and bugfix flows remain explicit or isolated unless a higher-priority artifact says otherwise. | Public workflow and skill guidance preserve isolation; no M1-M5 implementation expands bugfix or manual skill invocation behavior. | preserved |
| Phase C promotion | Automatic `explain-change` and `verify` are not available until promotion evidence exists. | `ITV-036`, `AC-ITV-024`, and `AC-ITV-025` prove persisted phase and promotion evidence gating. Phase C is Not enabled in first slice. | preserved rollout boundary |
| Audit reconstruction | Future maintainers must reconstruct each automatic transition and fix. | `ITV-034` and `AC-ITV-022` are covered by structured policy fields, review records, review-resolution dispositions, and change metadata validation. | strengthened |

## Acceptance Criteria Coverage

| Acceptance criteria | Evidence |
| --- | --- |
| `AC-ITV-001`, `AC-ITV-002`, `AC-ITV-025` | M1 change metadata schema/validator and query tests prove separate authorization, off-by-default policy, and persisted phase. |
| `AC-ITV-003`, `AC-ITV-004` | M2 route fixtures prove deterministic settlement and independent review before milestone close. |
| `AC-ITV-005`, `AC-ITV-006`, `AC-ITV-007`, `AC-ITV-008` | M3 review-artifact and correction guardrail fixtures prove reviewer-owned classifications, unclassified pause, closed mechanical kinds, and declared-safe recipe fields. |
| `AC-ITV-009`, `AC-ITV-010`, `AC-ITV-011`, `AC-ITV-012`, `AC-ITV-013` | M3 correction guardrail fixtures prove governing-artifact stop, shrinking-set rule, new-finding pause, three-round cap per milestone, and affected-path scope limits. |
| `AC-ITV-014`, `AC-ITV-015`, `AC-ITV-016` | M4 public skills and review records prove context reset, final full review, and final reviewed diff requirements. |
| `AC-ITV-017`, `AC-ITV-018`, `AC-ITV-019`, `AC-ITV-020` | M4 verify and workflow skill guidance preserves fresh actual-run evidence, verify-failure pause, profile completion before PR, and explicit PR authorization. |
| `AC-ITV-021`, `AC-ITV-022`, `AC-ITV-023`, `AC-ITV-024` | M2/M3/M4 route, audit, profile-off, and phase-promotion tests prove idempotent resume, auditability, profile-off preservation, and Phase C promotion gating. |

## Test Check Coverage

| Test checks | Evidence |
| --- | --- |
| `ITV-001`, `ITV-002`, `ITV-003`, `ITV-004`, `ITV-005` | M1/M2 profile and activation fixtures. |
| `ITV-006`, `ITV-007`, `ITV-008`, `ITV-038` | M2 settlement fixtures and M5 static absence check for `test-spec-review`. |
| `ITV-009`, `ITV-010`, `ITV-022`, `ITV-033` | M2 ordered milestone/resume fixtures and code-review records through M4. |
| `ITV-011`, `ITV-012`, `ITV-013`, `ITV-014` | M3 review-artifact parser and correction eligibility tests. |
| `ITV-015`, `ITV-016`, `ITV-017`, `ITV-018`, `ITV-019`, `ITV-020`, `ITV-021`, `ITV-034` | M3 correction guardrail fixtures and review-resolution closeout evidence. |
| `ITV-023`, `ITV-024`, `ITV-026`, `ITV-027`, `ITV-028`, `ITV-029`, `ITV-030`, `ITV-031`, `ITV-036` | M2 route fixtures and M4 public skill-surface static proof. Phase C remains guarded. |
| `ITV-025`, `ITV-039` | M3 CI-maintenance guardrail fixtures. |
| `ITV-032`, `ITV-035`, `ITV-037` | M1 policy/cancellation/off/default and independent authorization metadata tests. |

## Falsification Checklist

| Falsification condition | First-slice result |
| --- | --- |
| Unclassified finding is automatically fixed | Blocked by M3 parser and correction guardrails. |
| Auto-fix changes a governing artifact | Blocked by M3 governing-artifact stop. |
| Review loop grows or oscillates | Blocked by shrinking-set, no-new-finding, and round-cap fixtures. |
| New review finding is automatically chased | Blocked by new-finding pause. |
| Review independence collapses | Preserved by independent code-review records and M4 skill guidance. |
| Verify reuses stale evidence | Phase C not enabled; M4 guidance requires fresh actual-run evidence. |
| Workflow opens a PR automatically | Phase C guidance stops before `pr`; PR opening remains explicit. |
| Resumption repeats a completed stage | M2 resume fixtures skip closed milestones. |
| Unrelated dirty change enters automated diff | M2 activation fixtures pause on unrelated dirty state. |
| Six-month audit cannot reconstruct authority | M1-M4 evidence records policy, reviews, classifications, dispositions, paths, commands, and validation. |

## Rollout Evidence Placeholders

Phase A audit-only and Phase B dogfood metrics are not completed in this first implementation slice. Promotion to Phase C requires a later recorded evidence package with:

- at least 10 eligible simulated or real Phase B cycles, or 30 days with at least 10 eligible cycles;
- no observed unauthorized auto-fixes;
- no observed governing-artifact auto-edits;
- no observed new-finding loops;
- no observed exceeded round caps;
- no observed duplicate milestone runs;
- all reviewer-declared pauses occurring correctly;
- a synthetic-fixture audit proving every documented stop condition pauses.

Until that package exists, Phase C remains Not enabled in first slice.

## Boundary Statement

This M5 proof does not claim final `explain-change`, final `verify`, branch readiness, PR readiness, or PR opening. It only proves the first implementation slice is ready for final implementation code-review.
