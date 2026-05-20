# Spec-Family Assets Progressive Disclosure

## Status

approved

Approved after clean `spec-review` round 1.

## Related proposal

- [Spec-Family `assets/` Progressive Disclosure](../docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md)

## Goal and context

This spec defines the contract for extending the assets-first progressive-disclosure pattern from the `plan` pilot to the spec-family skills: `spec`, `spec-review`, and `test-spec`.

The change moves reusable copy-and-fill output structures from common-path skill bodies into skill-local `assets/` files while preserving the installed skill as the user-facing operating contract. It is an asset extraction and packaging pass, not a behavior change. Rules, stop conditions, routing, enum values, review dimensions, coverage obligations, lifecycle boundaries, validation obligations, and claim boundaries remain in `SKILL.md` or governing workflow artifacts.

The existing `specs/skill-contract.md` already defines generic packaged-resource behavior, resource maps, `COPY` for assets, generated-output boundaries, and the earlier `plan` pilot. This spec owns the spec-family extension and the review-class restrictions for `spec-review`. It does not amend the `plan` pilot clauses or broaden the scope to unrelated skills.

## Glossary

- `spec-family skills`: the canonical skills `spec`, `spec-review`, and `test-spec`.
- `asset`: a skill-local file under a skill's `assets/` directory that contains a structural template copied and filled by the agent.
- `full skeleton asset`: an asset that owns the full output skeleton for an artifact-producing skill.
- `substructure asset`: an asset that owns one repeated row or block within an artifact.
- `substantial asset`: an asset whose template body carries enough structure to justify a packaged file, typically a full skeleton or a multi-field block where field ordering or table shape is easy to get wrong.
- `review-class asset`: an asset owned by a deliberative review skill, limited to output structure and not review judgment.
- `common-path skill body`: the text in `SKILL.md` that a user or agent reads before loading packaged resources.
- `generated skill mirror`: derived local runtime output under `.codex/skills/`.
- `temporary generated adapter output`: adapter packages generated into a temporary directory for validation proof.
- `tracked-tree adapter debt`: stale repository-tracked expanded adapter layout issues that are unrelated to this asset extraction.

## Examples first

Example E1: `spec` uses a full skeleton asset without hiding rules
Given `skills/spec/SKILL.md` owns the operating rules, stop conditions, closed enums, and resource map
When `assets/spec-skeleton.md` owns the output skeleton
Then `SKILL.md` still names the expected output shape and points to the asset with a `COPY` entry
And the full skeleton is not duplicated in both places.

Example E2: `spec-review` keeps review dimensions in `SKILL.md`
Given `spec-review` has a fixed review-dimension table and verdict enum
When `spec-review` gains assets
Then the assets are limited to `review-result-skeleton.md` and `review-finding.md`
And review dimensions, review policy, severity policy, recording rules, and material-finding sufficiency rules remain in `SKILL.md`.

Example E3: generated output proves assets ship
Given canonical spec-family skills include mapped assets
When generated skill mirrors and temporary adapter archives are built or checked
Then every mapped asset is present in the generated output
And no generated skill body or asset is hand-edited.

Example E4: baseline summary prevents extraction drift
Given PR #79 is the authoritative behavior baseline
When implementation extracts a skeleton or repeated structure into an asset
Then a change-local baseline summary maps the source structure, preserved rules, and extracted fields before implementation changes the skill.

## Requirements

SFA-R1. The implementation MUST add skill-local `assets/` directories only for `skills/spec/`, `skills/spec-review/`, and `skills/test-spec/`.

SFA-R2. The implementation MUST NOT add packaged `references/`, packaged `scripts/`, build-time partials, adapter install-root changes, lockfile changes, CLI behavior changes, or unrelated lifecycle skill assets.

SFA-R3. Every spec-family asset MUST be a copy-and-fill structural template, not a rule reference, review rubric, decision matrix, validation checklist, tutorial, hidden enum source, or substitute for `SKILL.md` operating instructions.

SFA-R3A. Every spec-family asset MUST be substantial enough to justify a packaged template. One-line rows or trivial single-field structures SHOULD remain inline in `SKILL.md` when the skill already carries the relevant format rule.

SFA-R3B. A repeated structure MUST NOT become an asset solely because it is multi-instance. The structure MUST also be substantial enough to reduce copy errors, preserve a non-trivial shape, or remove meaningful full-skeleton bulk from the common-path skill body.

SFA-R3C. If an asset's required metadata header is larger than the template body, implementation MUST treat that as evidence that the asset is too small and either keep the format inline or record a specific exception in the plan.

SFA-R4. `skills/spec/SKILL.md` MUST keep rules, stop conditions, routing, claim boundaries, closed enums, validation obligations, and lifecycle boundaries in `SKILL.md`.

SFA-R5. `skills/test-spec/SKILL.md` MUST keep rules, stop conditions, routing, claim boundaries, status and level enums, coverage obligations, validation obligations, and lifecycle boundaries in `SKILL.md`.

SFA-R6. `skills/spec-review/SKILL.md` MUST keep review dimensions, review-dimension table structure, review guidance, verdict enum, severity policy, material-finding sufficiency rules, recording obligations, validation obligations, and lifecycle boundaries in `SKILL.md`.

SFA-R7. `spec` MUST use `assets/spec-skeleton.md` as its full output skeleton unless code review finds that the asset hides too much contract surface for that skill.

SFA-R8. `spec` MUST include only `spec-skeleton.md` in this slice unless the plan records the required exception justification. Requirement, acceptance-criterion, and decision-log row shapes remain inline because they are trivial relative to their metadata and are already governed by inline format guidance.

SFA-R9. `spec-review` MUST use only `review-result-skeleton.md` and `review-finding.md` assets in this slice.

SFA-R10. `spec-review` MUST NOT include a review-dimension row asset, a full review-dimensions asset, or any asset that defines review dimensions or review judgment.

SFA-R11. `test-spec` MUST use `assets/test-spec-skeleton.md` as its full output skeleton unless code review finds that the asset hides too much contract surface for that skill.

SFA-R12. `test-spec` MUST include only `test-spec-skeleton.md`, `test-case.md`, and `coverage-map-row.md` in this slice unless the plan records the required exception justification. Edge-case row shape remains inline because it is a trivial one-line mapping.

SFA-R13. Any additional spec-family asset beyond the approved per-skill inventory MUST be justified in the plan with asset path, why the asset earns its place, expected usage frequency, why the content cannot remain inline, why it is substantial enough to template, and why it is an asset rather than a reference.

SFA-R14. Every touched `SKILL.md` MUST include a `Resource map` that names every packaged asset.

SFA-R15. Every asset resource-map entry MUST use the literal verb `COPY`, state the condition under which the asset is copied, name the fields or structures the agent fills, and instruct the agent not to emit unfilled placeholders.

SFA-R16. Full skeleton assets MUST have a corresponding compact output expectation summary in the owning `SKILL.md`.

SFA-R17. The owning `SKILL.md` and full skeleton asset MUST NOT duplicate the full artifact skeleton.

SFA-R18. If code review finds that a full skeleton asset hides too much contract surface for `spec` or `test-spec`, implementation MUST keep the full skeleton inline for that skill and use assets only for repeated substructures.

SFA-R19. Every asset MUST include metadata comments for template ID, skill name, template status, and maintained-alongside path.

SFA-R20. Asset template status MUST use only `normative` or `optional` in this slice.

SFA-R21. Asset placeholders MUST use visible placeholder forms, such as a bracketed field name, an all-caps fill marker, or an explicit fill-in prefix.

SFA-R22. Assets MUST NOT use empty required fields, realistic filler prose, generic filler text, or the phrase `your text here` as placeholder content.

SFA-R23. `spec-review` assets MAY contain only headings, field labels, placeholders, and short fill hints.

SFA-R24. `spec-review` assets MUST NOT contain review-dimension definitions, severity policy, material-finding sufficiency rules, safe-resolution decision rules, recording-status rules, or security/privacy or observability examples.

SFA-R25. Before implementation changes skill text, the change MUST create `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`.

SFA-R26. The baseline summary MUST record, per skill, existing full skeleton section set, repeated substructure fields to extract, closed enums that remain in `SKILL.md`, stop conditions that remain in `SKILL.md`, review dimensions or coverage obligations that remain in `SKILL.md`, and source location for each extracted asset.

SFA-R27. PR #79 remains the authoritative behavior baseline; the change-local baseline summary is a review aid and MUST NOT redefine baseline behavior.

SFA-R28. Implementation MUST record preservation matrices proving source-to-asset field parity for every extracted full skeleton or repeated substructure.

SFA-R29. The preservation proof MUST show that field names, field obligations, enum values, stop conditions, coverage obligations, review dimensions, and lifecycle boundaries are unchanged unless a later approved spec changes them.

SFA-R30. Representative behavior parity MUST be recorded for `spec`, `spec-review`, and `test-spec` against the PR #79 baseline.

SFA-R31. Representative behavior parity MUST show no regression in required section set, enum values, review dimensions, verdict behavior, material-finding shape, recording behavior, test-case format, coverage rules, status values, or level values as applicable to the skill.

SFA-R32. Generated skill mirror proof MUST show every mapped spec-family asset is present in generated skill mirrors.

SFA-R33. Temporary generated adapter output proof MUST show every mapped spec-family asset is present in generated adapter packages.

SFA-R34. Adapter validation MUST run against the temporary generated adapter output unless the validation tool itself is unavailable or blocked, in which case the blocker and smallest next action MUST be recorded.

SFA-R35. Tracked-tree adapter proof MUST run when the repository's tracked expanded adapter layout supports it.

SFA-R36. Known stale tracked-tree adapter debt MAY be explicitly deferred only when generated skill mirror proof, temporary generated adapter proof, and adapter validation are still completed or explicitly blocked with evidence.

SFA-R37. Generated adapter skill bodies and assets MUST NOT be hand-edited.

SFA-R38. Token-cost measurement MUST report common-path `SKILL.md` body size separately from total packaged footprint.

SFA-R39. Common-path `SKILL.md` body size SHOULD decrease for each touched skill unless behavior preservation, self-containment, or adapter parity requires otherwise.

SFA-R40. No final representative output may contain unfilled asset placeholders.

SFA-R41. Cold-read proof MUST confirm that installed skill output alone explains when to use each packaged asset.

SFA-R42. The implementation MUST update validator or test fixtures needed to deterministically check asset mapping, `COPY` usage, metadata comments, allowed statuses, placeholder policy, review-class asset boundary, generated-output presence, and baseline-summary presence.

SFA-R43. Validator checks for hidden asset rules MUST use deterministic checks or bounded heuristics declared in the test spec or plan; they MUST NOT rely on broad semantic scoring.

SFA-R44. If existing skill-contract asset rules are found insufficient for multi-skill rollout, full-skeleton boundaries, or review-class restrictions, implementation MUST stop before skill edits and create the needed spec amendment packet.

SFA-R45. If existing skill-contract asset rules are sufficient, the plan MUST record that assessment and proceed under this spec plus the matching test spec.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md`;
- PR #79 behavior baseline and change-local evidence for the spec-family readability pass;
- `specs/skill-contract.md`, especially packaged-resource and assets-first pilot clauses;
- canonical skill sources under `skills/spec/`, `skills/spec-review/`, and `skills/test-spec/`;
- generated skill and adapter build/validation scripts.

Outputs:

- updated canonical spec-family `SKILL.md` files;
- new skill-local assets under the three touched skills;
- change-local baseline summary;
- preservation matrices;
- representative behavior-parity evidence;
- generated skill mirror and temporary adapter proof;
- token-cost evidence;
- validator and fixture updates needed for this contract;
- lifecycle review, explain-change, verify, and PR handoff artifacts.

## State and invariants

- `SKILL.md` remains the installed skill operating contract.
- Assets are copied structures, not hidden rules.
- Canonical authored skill source remains under `skills/`.
- Generated skill mirrors and adapter output remain derived from canonical skills.
- PR #79 remains the behavior baseline.
- `spec-review` remains deliberative; its assets remain narrow.
- Produced spec, review, and test-spec artifact readability is not changed by this slice.

## Error and boundary behavior

- If the proposal is not accepted before downstream reliance, spec work blocks until proposal status is settled.
- If the skill-contract sufficiency assessment finds a contract gap, implementation blocks until a spec amendment packet is approved.
- If a full skeleton asset hides rules or makes the installed skill less self-contained, keep that skeleton inline and use only repeated substructure assets for that skill.
- If an asset needs review judgment, rule text, enum definitions, coverage obligations, or validation policy to be useful, the content stays in `SKILL.md` or a later `references/` proposal.
- If generated adapter validation cannot prove temporary archive presence, readiness blocks unless the blocker and smallest next action are recorded.
- If unrelated tracked-tree adapter debt appears, it may be deferred only after temporary generated output proof is preserved.

## Compatibility and migration

Existing users should observe the same skill behavior with shorter common-path skill bodies and packaged structural templates. Skill invocation, routing descriptions, lifecycle state semantics, adapter install roots, lockfiles, CLI behavior, and produced artifact contracts remain compatible.

Rollback is to reinline asset content into the owning `SKILL.md`, remove the skill's `assets/` directory, preserve generic validator improvements that remain valid, and rebuild generated mirrors and adapter archives from canonical skills. Rollback must not hand-edit generated adapter output.

## Observability

The change is observable through:

- canonical skill diffs;
- asset file diffs;
- resource-map entries;
- baseline summary;
- preservation matrices;
- behavior-parity evidence;
- generated skill mirror and temporary adapter proof;
- token-cost measurements;
- validator/test fixture results;
- review, explain-change, verify, and PR handoff artifacts.

## Security and privacy

No secrets, credentials, private data flows, authorization behavior, or external services are introduced. Assets must not require repository-root internal paths as customer-project dependencies. Generated output must remain reproducible from canonical sources rather than hand-edited.

## Accessibility and UX

This is a Markdown skill-text change. The user-facing effect is easier scanning of installed skills while preserving output quality. No UI accessibility surface is otherwise affected.

## Performance expectations

No runtime performance behavior is affected. Common-path skill body token cost should decrease, but token reduction is subordinate to behavior preservation, self-containment, and generated-output parity.

## Edge cases

EC1. A full skeleton asset for `spec` or `test-spec` makes required sections harder to discover from `SKILL.md`. The implementation must keep a compact summary in `SKILL.md` or fall back to inline skeleton ownership for that skill.

EC2. A proposed `spec-review` asset needs review policy to be understandable. The asset is rejected for this slice and the policy remains in `SKILL.md`.

EC3. Generated skill mirror proof passes but temporary adapter archive proof fails. The change is not ready for implementation closeout until adapter proof passes or the blocker is recorded with the smallest next action.

EC4. Tracked expanded adapter checks fail because of known stale layout debt unrelated to this proposal. The debt may be deferred only if temporary generated archive proof and adapter validation still prove asset packaging.

EC5. Token measurement shows total packaged footprint grows. The change may still proceed if common-path body size is reported separately and behavior preservation, self-containment, and adapter parity justify the footprint.

EC6. A representative output contains an unfilled placeholder. The implementation must fix the asset use or output generation instructions before readiness.

## Non-goals

- No packaged `references/`.
- No packaged `scripts/`.
- No build-time partials or include syntax.
- No routing-description changes.
- No changes to normative rules, stop conditions, enum values, output obligations, review dimensions, coverage obligations, or lifecycle boundaries.
- No produced-artifact readability changes beyond preserving existing output structure through assets.
- No adapter install-root, lockfile, CLI behavior, or release archive trust-boundary changes.
- No generated adapter hand edits.
- No retroactive legacy adapter archive rewrites.
- No application of this asset pattern to unrelated lifecycle skills.

## Acceptance criteria

AC-SFA-001. Each of `spec`, `spec-review`, and `test-spec` has an `assets/` directory with only approved structural templates for this slice.

AC-SFA-002. Every asset has required metadata comments and an allowed template status.

AC-SFA-003. Every asset has a matching `COPY` resource-map entry in the owning `SKILL.md`.

AC-SFA-004. No asset contains hidden normative rules, enum definitions, stop conditions, review-dimension guidance, coverage obligations, or repository-root internal dependency requirements.

AC-SFA-005. `spec` and `test-spec` full skeleton assets have corresponding compact output expectation summaries in `SKILL.md`, or code review records an inline fallback for that skill.

AC-SFA-006. `spec-review` assets contain no review judgment or review-policy prose beyond headings, field labels, placeholders, and short fill hints.

AC-SFA-007. Preservation matrices prove source-to-asset field parity for every extracted structure.

AC-SFA-008. Representative behavior-parity evidence matches the PR #79 baseline for all three spec-family skills.

AC-SFA-009. Generated skill mirrors include all mapped spec-family assets.

AC-SFA-010. Temporary generated adapter archives include all mapped spec-family assets and adapter validation passes against that temporary output.

AC-SFA-011. No generated adapter body or asset is hand-edited.

AC-SFA-012. Common-path `SKILL.md` token counts are recorded separately from packaged asset footprints.

AC-SFA-013. Cold-read verification confirms asset usage is understandable from installed skill output alone.

AC-SFA-014. The change-local baseline summary maps PR #79 skill structures to planned assets and to the rules, enums, stops, dimensions, and coverage obligations that remain in `SKILL.md`.

AC-SFA-015. Validator or fixture coverage exists for asset mapping, `COPY` usage, metadata, statuses, placeholders, review-class asset boundary, generated-output presence, and baseline-summary presence.

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec amendment for spec-family asset checks
plan
plan-review
implementation milestones
code-review
explain-change
verify
pr
```

If `spec-review` finds the current skill-contract asset rules insufficient, add:

```text
skill-contract spec amendment
spec-review for that amendment
```

## Follow-on artifacts

- [Spec-Family Assets Progressive Disclosure Plan](../docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md)
- [Spec-Family Assets Progressive Disclosure Test Spec](spec-family-assets-progressive-disclosure.test.md)

## Readiness

Approved. The active plan owns downstream milestone handoff state.
