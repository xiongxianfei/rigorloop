# Proposal-Family Assets Progressive Disclosure

## Status

approved

Approved after clean `spec-review` round 1.

## Related proposal

- [Proposal-Family `assets/` Progressive Disclosure](../docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md)

## Goal and context

This spec defines the contract for extending the assets-first progressive-disclosure pattern to the proposal-family skills: `proposal` and `proposal-review`.

The change moves reusable copy-and-fill output structures from common-path skill bodies into skill-local `assets/` files while preserving the installed skill as the user-facing operating contract. It is an asset extraction and packaging pass, not a behavior change. Rules, stop conditions, routing, enum values, review dimensions, scope-preservation rules, recording obligations, lifecycle boundaries, validation obligations, and claim boundaries remain in `SKILL.md` or governing workflow artifacts.

The existing `specs/skill-contract.md` defines generic packaged-resource behavior, resource maps, `COPY` for assets, generated-output boundaries, and prior assets-first pilot behavior. This spec owns the proposal-family extension, the conditional proposal-section boundary for `proposal`, and the review-class asset boundary for `proposal-review`. It does not broaden the scope to unrelated skills.

## Glossary

- `proposal-family skills`: the canonical skills `proposal` and `proposal-review`.
- `asset`: a skill-local file under a skill's `assets/` directory that contains a structural template copied and filled by the agent.
- `full skeleton asset`: an asset that owns the full output skeleton for an artifact-producing skill.
- `review-class asset`: an asset owned by a deliberative review skill, limited to output structure and not review judgment.
- `conditional proposal section`: a proposal section inserted only when a trigger applies, such as `Initial intent preservation` or `Scope budget`.
- `structural-label allowlist`: the exact set of field labels allowed in `proposal-review` assets.
- `forbidden review-policy label`: a field label or prose phrase that would move review judgment, policy, or rules into an asset.
- `common-path skill body`: the text in `SKILL.md` that a user or agent reads before loading packaged resources.
- `P`: the fraction of skill invocations expected to load a given asset, used to contextualize per-invocation token cost.
- `generated skill mirror`: derived local runtime output under `.codex/skills/`.
- `temporary generated adapter output`: adapter packages generated into a temporary directory for validation proof.
- `tracked-tree adapter debt`: stale repository-tracked expanded adapter layout issues unrelated to this asset extraction.

## Examples first

Example E1: `proposal` uses a full skeleton asset without losing conditional sections
Given `skills/proposal/SKILL.md` owns proposal rules, closed enums, scope-preservation rules, scope-budget triggers, and the resource map
When `assets/proposal-skeleton.md` owns the main output skeleton
Then the asset or resource-map instructions preserve triggered insertion of `Initial intent preservation` and `Scope budget`
And those sections are not made mandatory for every proposal.

Example E2: `proposal-review` assets remain structural
Given `proposal-review` is a deliberative review skill
When it gains `review-result-skeleton.md` and `material-finding.md`
Then the assets contain headings, field labels, placeholders, and short fill hints only
And review dimensions, severity policy, recording rules, scope-preservation rules, Vision fit review rules, and handoff behavior remain in `SKILL.md`.

Example E3: deterministic review-class validation rejects policy-shaped labels
Given `assets/material-finding.md` contains `- Severity: <severity>`
When the validator checks the asset
Then the field passes as an allowed structural label.

Given `assets/material-finding.md` contains `- Severity policy: <policy>`
When the validator checks the asset
Then validation fails because severity policy belongs in `SKILL.md`.

Example E4: generated output proves assets ship
Given canonical proposal-family skills include mapped assets
When generated skill mirrors and temporary adapter archives are built or checked
Then every mapped asset is present in the generated output
And no generated skill body or asset is hand-edited.

Example E5: token-cost proof includes P
Given `proposal-skeleton.md` is expected to be loaded for most fresh proposal-authoring invocations
When token-cost evidence is recorded
Then common-path `SKILL.md` reduction is reported separately from total packaged footprint
And P is recorded so reviewers understand that a full skeleton asset may increase total packaged footprint while improving readability.

## Requirements

PFA-R1. The implementation MUST add skill-local `assets/` directories only for `skills/proposal/` and `skills/proposal-review/`.

PFA-R2. The implementation MUST NOT add packaged `references/`, packaged `scripts/`, build-time partials, adapter install-root changes, lockfile changes, CLI behavior changes, or unrelated lifecycle skill assets.

PFA-R3. Every proposal-family asset MUST be a copy-and-fill structural template, not a rule reference, review rubric, decision matrix, validation checklist, tutorial, hidden enum source, or substitute for `SKILL.md` operating instructions.

PFA-R4. Every proposal-family asset MUST be substantial enough to justify a packaged template. One-line rows or trivial single-field structures SHOULD remain inline in `SKILL.md` when the skill already carries the relevant format rule.

PFA-R5. `skills/proposal/SKILL.md` MUST keep routing, evidence access, artifact-placement rules, required proposal section guidance, proposal status values, Vision fit values and rules, standing artifact gates, scope-preservation rules, scope-budget rules, decision-quality checks, workflow handoff behavior, and output obligations in `SKILL.md`.

PFA-R6. `skills/proposal-review/SKILL.md` MUST keep routing, evidence access, artifact-placement rules, review dimensions, review-dimension result values, Vision fit review rules, vision-conflict outcomes, standing artifact gate review rules, scope-preservation review rules, scope-budget review rules, material-finding sufficiency rules, recording status values, review status values, isolation and recording rules, and workflow handoff behavior in `SKILL.md`.

PFA-R7. `proposal` MUST use `assets/proposal-skeleton.md` as its full output skeleton unless code review finds that the asset hides too much contract surface.

PFA-R8. `proposal` MUST include only `proposal-skeleton.md` in this slice unless the plan records an exception with asset path, why the asset earns its place, expected usage frequency, why the content cannot remain inline, why it is substantial enough to template, and why it is an asset rather than a reference.

PFA-R9. `proposal` MUST NOT add row-only assets for initial intent, scope budget, decision log, risk rows, or similar small table rows in this slice.

PFA-R10. `proposal-review` MUST use only `assets/review-result-skeleton.md` and `assets/material-finding.md` in this slice.

PFA-R11. `proposal-review` MUST NOT include a review-dimension row asset, a full review-dimensions asset, or any asset that defines review dimensions or review judgment.

PFA-R12. Every touched `SKILL.md` MUST include a `Resource map` that names every packaged asset.

PFA-R13. Every asset resource-map entry MUST use the literal verb `COPY`, state the condition under which the asset is copied, name the fields or structures the agent fills, and instruct the agent not to emit unfilled placeholders.

PFA-R14. Full skeleton assets MUST have a corresponding compact output expectation summary in the owning `SKILL.md`.

PFA-R15. The owning `SKILL.md` and full skeleton asset MUST NOT duplicate the full artifact skeleton.

PFA-R16. If code review finds that a full skeleton asset hides too much contract surface for `proposal`, implementation MUST keep the full skeleton inline for that skill and record the fallback in behavior-preservation evidence.

PFA-R17. `assets/proposal-skeleton.md` MUST preserve trigger-based conditional proposal sections without changing their conditional behavior.

PFA-R18. `assets/proposal-skeleton.md` MAY include conditional blocks only when they are clearly labeled as conditional. Otherwise, `skills/proposal/SKILL.md` MUST instruct the agent to insert those sections when triggers apply.

PFA-R19. The extraction MUST preserve `Initial intent preservation` as a conditional section inserted when the request is broad, multi-part, or materially revised.

PFA-R20. The extraction MUST preserve `Scope budget` as a conditional section inserted when the proposal is broad, multi-workstream, touches multiple lifecycle families, generated output, workflow policy, release policy, or validation policy.

PFA-R21. `assets/proposal-skeleton.md` MUST NOT make `Initial intent preservation` or `Scope budget` mandatory for every proposal.

PFA-R22. `assets/proposal-skeleton.md` MUST NOT omit the ability to add `Initial intent preservation` or `Scope budget` when triggered.

PFA-R23. `proposal-review` assets MAY contain only headings, field labels, placeholders, and short fill hints.

PFA-R24. `proposal-review` assets MUST NOT contain review-dimension definitions, severity policy, material-finding sufficiency rules, safe-resolution decision rules, recording-status rules, scope-preservation rules, scope-budget review rules, Vision fit review rules, standing artifact gate review rules, architecture/risk/testability review guidance, security/privacy examples, or rollout examples.

PFA-R25. `proposal-review` asset validation MUST use an explicit structural-label allowlist and deterministic forbidden review-policy label checks.

PFA-R26. The structural-label allowlist for `proposal-review` assets MUST include only fields needed by `review-result-skeleton.md` and `material-finding.md`.

PFA-R27. The structural-label allowlist for `proposal-review` assets MUST include these labels when present: `Review status`, `Material findings`, `Recording status`, `Recording blocker`, `Review record`, `Review log`, `Review resolution`, `Open blockers`, `Immediate next stage`, `Review dimensions`, `Scope-preservation result`, `Recommended edits`, `Recommendation`, `Finding ID`, `Severity`, `Location`, `Evidence`, `Required outcome`, `Safe resolution path`, and `needs-decision rationale`.

PFA-R28. The forbidden review-policy label checks for `proposal-review` assets MUST reject at least these labels or prose phrases when present as asset content: `Severity policy`, `Material-finding sufficiency`, `Safe-resolution decision rule`, `Recording-status rules`, `Scope-preservation rules`, `Scope-budget review`, `Vision fit review`, `Standing artifact gate review`, and `Review dimension guidance`.

PFA-R29. Every asset MUST include metadata comments for template ID, skill name, template status, and maintained-alongside path.

PFA-R30. Asset template status MUST use only `normative` or `optional` in this slice.

PFA-R31. Asset placeholders MUST use visible placeholder forms, such as bracketed field names, all-caps fill markers, `TODO:`, or angle-bracket field names.

PFA-R32. Assets MUST NOT use empty required fields, realistic filler prose, generic filler text, `lorem ipsum`, or the phrase `your text here` as placeholder content.

PFA-R33. Before implementation changes skill text, the change MUST create `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`.

PFA-R34. The baseline summary MUST record source commit or branch point, exact canonical source paths, source file hashes or section-level normalized hashes, existing full skeleton section set, repeated substructure fields to extract, extracted asset source ranges or stable headings, conditional sections governed by `SKILL.md`, closed enums that remain in `SKILL.md`, scope-preservation and scope-budget rules that remain in `SKILL.md`, Vision fit and standing artifact gate rules that remain in `SKILL.md`, review dimensions and recording obligations that remain in `SKILL.md`, and source location for each extracted asset.

PFA-R35. The pinned baseline recorded in `baseline.md` MUST define the behavior baseline for implementation and review.

PFA-R36. Implementation MUST record preservation matrices proving source-to-asset field parity for every extracted full skeleton or repeated substructure.

PFA-R37. The preservation proof MUST show that field names, field obligations, enum values, review dimensions, review status values, recording status values, scope-preservation behavior, scope-budget behavior, recording behavior, and handoff semantics are unchanged unless a later approved spec changes them.

PFA-R38. Representative behavior parity MUST be recorded for `proposal` and `proposal-review` against the pinned baseline.

PFA-R39. No final representative output may contain unfilled asset placeholders.

PFA-R40. Generated skill mirror proof MUST show every mapped proposal-family asset is present in generated skill mirrors.

PFA-R41. Temporary generated adapter output proof MUST show every mapped proposal-family asset is present in generated adapter packages.

PFA-R42. Adapter validation MUST run against the temporary generated adapter output unless the validation tool itself is unavailable or blocked, in which case the blocker and smallest next action MUST be recorded.

PFA-R43. Tracked-tree adapter proof MUST run when the repository's tracked expanded adapter layout supports it.

PFA-R44. Known stale tracked-tree adapter debt MAY be explicitly deferred only when generated skill mirror proof, temporary generated adapter proof, and adapter validation are still completed or explicitly blocked with evidence.

PFA-R45. Generated adapter skill bodies and assets MUST NOT be hand-edited.

PFA-R46. Token-cost measurement MUST report common-path `SKILL.md` body size separately from total packaged footprint.

PFA-R47. Token-cost measurement MUST record P for each proposal-family asset to contextualize expected per-invocation cost.

PFA-R48. Token-cost evidence MUST explicitly acknowledge that `proposal-skeleton.md` may increase total packaged footprint while still being justified by common-path readability and maintainability.

PFA-R49. Common-path `SKILL.md` body size SHOULD decrease for each touched skill unless behavior preservation, self-containment, or adapter parity requires otherwise.

PFA-R50. Cold-read proof MUST confirm that installed skill output alone explains when to use each packaged asset.

PFA-R51. The implementation MUST update validator or test fixtures needed to deterministically check asset mapping, `COPY` usage, metadata comments, allowed statuses, placeholder policy, proposal conditional-section preservation, proposal-review structural-label allowlist, proposal-review forbidden policy labels, generated-output presence, and baseline-summary presence.

PFA-R52. Validator checks for hidden asset rules MUST use deterministic checks or bounded heuristics declared in the test spec or plan; they MUST NOT rely on broad semantic scoring.

PFA-R53. The matching test spec MUST be approved before implementation begins.

PFA-R54. If existing skill-contract asset rules are found insufficient for proposal-family full-skeleton assets, review-class asset restrictions, generated-output asset presence, or behavior-preservation evidence, implementation MUST stop before skill edits and create the needed spec amendment packet.

PFA-R55. If existing skill-contract asset rules are sufficient, the plan MUST record that assessment and proceed under this spec plus the matching test spec.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md`;
- proposal-review evidence under `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/`;
- `specs/skill-contract.md`, especially packaged-resource and assets-first pilot clauses;
- canonical skill sources under `skills/proposal/` and `skills/proposal-review/`;
- generated skill and adapter build/validation scripts.

Outputs:

- updated canonical `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`;
- new skill-local assets under `skills/proposal/assets/` and `skills/proposal-review/assets/`;
- focused test-spec amendment for proposal-family asset checks;
- optional skill-contract spec amendment only if a documented contract gap exists;
- change-local baseline summary;
- preservation matrices;
- representative behavior-parity evidence;
- generated skill mirror and temporary adapter proof;
- token-cost evidence with P;
- validator and fixture updates needed for this contract;
- lifecycle review, explain-change, verify, and PR handoff artifacts.

## State and invariants

- `SKILL.md` remains the operating contract for each touched skill.
- Assets are copied structures, not hidden rules.
- `proposal-review` assets remain review-class structural templates.
- Generated outputs are derived from canonical skill source and are not hand-edited.
- The pinned baseline in `baseline.md` is the behavior-preservation reference for this change.
- No rule, enum value, stop condition, review dimension, scope-preservation rule, recording rule, output obligation, lifecycle boundary, routing behavior, or representative output behavior changes in this slice.

## Error and boundary behavior

- If the focused test spec is not approved, implementation must not begin.
- If the existing skill-contract rules are insufficient, implementation must stop for a spec amendment packet before skill edits.
- If an asset lacks a resource-map entry, validation must fail.
- If a resource-map entry for an asset does not use `COPY`, validation must fail.
- If `proposal-review` assets contain forbidden review-policy labels or prose, validation must fail.
- If conditional proposal sections are lost or made universal by extraction, review must reject the implementation.
- If generated skill mirrors or temporary adapter output omit mapped assets, validation must fail or record a blocker with the smallest next action.
- If token-cost evidence reports only total footprint or only common-path size without P, verification must treat the token-cost evidence as incomplete.
- If representative output contains unfilled placeholders, validation or review must fail.

## Compatibility and migration

This change is backward-compatible for users of the published skills. Skill invocation, routing, artifact placement, status values, review statuses, recording statuses, adapter install roots, lockfile semantics, and CLI behavior do not change.

Generated output must be rebuilt or checked from canonical skill sources. Existing historical adapter archives are not retroactively rewritten.

Rollback is to reinline asset content into the owning `SKILL.md`, remove the affected skill's `assets/` directory, preserve generic validator improvements when still valid, and regenerate or revalidate derived skill and adapter output from canonical sources.

## Observability

The change must leave contributor-visible evidence in change-local artifacts or plan evidence for:

- asset mapping and generated-output presence checks;
- baseline identity and preservation matrices;
- representative behavior parity;
- token-cost common-path size, total packaged footprint, and P;
- adapter validation results or blockers;
- cold-read proof for installed skill output.

No runtime logging, metrics, tracing, or audit event behavior is introduced.

## Security and privacy

Assets must not introduce secrets, credentials, private data, machine-local paths, or repository-root internal paths as customer-facing requirements. No authentication, authorization, data exposure, or privacy behavior changes are introduced.

## Accessibility and UX

No user-interface accessibility behavior changes are introduced. The user-facing experience is the installed skill text and packaged assets; cold-read proof must confirm the installed skill output explains asset use without requiring repository maintainer context.

## Performance expectations

This change has no runtime performance contract. Token-cost performance is evidence-based:

- common-path `SKILL.md` body size is measured separately from total packaged footprint;
- P is recorded for each asset;
- total packaged footprint may increase for `proposal-skeleton.md`;
- common-path readability and maintainability justify the full skeleton asset when behavior preservation and adapter parity are proven.

## Edge cases

EC1. `proposal-skeleton.md` includes `Initial intent preservation` as a normal required section.
Expected behavior: review or validation rejects the extraction because the section is trigger-based.

EC2. `proposal-skeleton.md` omits any path for adding `Scope budget`.
Expected behavior: review rejects the extraction because triggered scope-budget behavior is not preserved.

EC3. `proposal-review` asset contains `Recording status: <recording status>`.
Expected behavior: validation accepts the field as structural.

EC4. `proposal-review` asset contains `Recording-status rules: <rules>`.
Expected behavior: validation rejects the asset because recording rules belong in `SKILL.md`.

EC5. `proposal-review` asset contains `Severity: <severity>`.
Expected behavior: validation accepts the field as structural.

EC6. `proposal-review` asset contains `Severity policy: <policy>`.
Expected behavior: validation rejects the asset because severity policy belongs in `SKILL.md`.

EC7. The generated skill mirror includes mapped assets but temporary adapter output does not.
Expected behavior: adapter proof is incomplete and verification blocks or records an explicit blocker.

EC8. Token-cost evidence shows common-path shrinkage but omits P.
Expected behavior: token-cost evidence is incomplete.

EC9. Code review finds the full `proposal` skeleton asset hides too much contract surface.
Expected behavior: the implementation falls back to keeping the full skeleton inline and records the fallback in preservation evidence.

## Non-goals

- Do not introduce packaged `references/`.
- Do not introduce packaged `scripts/`.
- Do not introduce build-time partials or include syntax.
- Do not change routing descriptions for `proposal` or `proposal-review`.
- Do not change proposal status values, Vision fit values, initial-goal treatment values, scope-budget treatment values, review status values, recording status values, review-dimension results, or vision-conflict outcomes.
- Do not change required proposal sections.
- Do not change proposal-review dimensions, material-finding requirements, standing artifact gate rules, scope-preservation rules, recording rules, or handoff behavior.
- Do not change artifact placement rules.
- Do not apply this asset pattern to `spec`, `spec-review`, `test-spec`, `plan`, `code-review`, `verify`, or `pr`.
- Do not change adapter install roots, lockfile semantics, CLI behavior, release archive trust boundaries, or canonical skill source location.
- Do not hand-edit generated adapter output.
- Do not retroactively rewrite legacy adapter archives.

## Acceptance criteria

AC-PFA-001. `proposal` has `assets/proposal-skeleton.md`.

AC-PFA-002. `proposal-review` has `assets/review-result-skeleton.md` and `assets/material-finding.md`.

AC-PFA-003. Each asset has required template metadata comments.

AC-PFA-004. Each asset has a matching `COPY` resource-map entry in the owning `SKILL.md`.

AC-PFA-005. No asset contains hidden normative rules, enum definitions, stop conditions, review-dimension guidance, scope-preservation rules, Vision fit rules, standing artifact gate rules, recording rules, or lifecycle boundaries.

AC-PFA-006. `proposal-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints.

AC-PFA-007. Each full skeleton asset has a corresponding compact output expectation summary in `SKILL.md`.

AC-PFA-008. Preservation matrices prove source-to-asset field parity for every extracted structure.

AC-PFA-009. Representative behavior-parity evidence matches the pinned baseline recorded in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`.

AC-PFA-010. Generated skill mirrors include all proposal-family assets.

AC-PFA-011. Generated adapter archives include all proposal-family assets.

AC-PFA-012. No generated adapter body or asset is hand-edited.

AC-PFA-013. Common-path `SKILL.md` token counts are recorded separately from packaged asset footprints, with P recorded for each asset and explicit acknowledgement that `proposal-skeleton.md` may increase total packaged footprint while still being justified by readability.

AC-PFA-014. Cold-read verification confirms asset usage is understandable from installed adapter output alone.

AC-PFA-015. Change-local baseline summary maps pinned skill structures to planned assets and to the rules, enums, review dimensions, recording obligations, and handoff boundaries that remain in `SKILL.md`.

AC-PFA-016. `proposal-review` asset validation uses an explicit structural-label allowlist and deterministic forbidden-label checks for review-policy terms.

AC-PFA-017. `proposal-skeleton.md` preserves conditional sections such as `Initial intent preservation` and `Scope budget` as trigger-based sections, not universal required sections.

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec amendment for proposal-family asset checks
spec amendment only if existing asset contract is insufficient
spec-review if a skill-contract spec amendment is created
plan
plan-review
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Approved; downstream plan created at `docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md`.
