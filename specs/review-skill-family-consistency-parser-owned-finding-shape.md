# Review-Skill Family Consistency and Parser-Owned Finding Shape

## Status

approved

## Related proposal

- [Review-Skill Family Consistency and Parser-Owned Finding Shape](../docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md)

## Goal and context

This spec defines the contract for applying asset-based progressive disclosure to the first-slice review skills: `code-review`, `proposal-review`, and `spec-review`.

The change makes the parser-owned material-finding field block the copied starting structure for review findings while preserving review behavior. It adds skill-local structural assets for material findings and review result blocks, updates resource maps, and adds validation that binds the material-finding asset shape to the existing review-artifact parser contract. Review judgment, review dimensions, severity semantics, recording rules, stop conditions, lifecycle boundaries, and handoff behavior remain in each owning `SKILL.md` or the governing workflow artifacts.

This spec extends the existing packaged-asset pattern from `specs/skill-contract.md`, `specs/proposal-family-assets-progressive-disclosure.md`, and `specs/spec-family-assets-progressive-disclosure.md`. It does not change the review-artifact parser's accepted field contract.

## Glossary

- `review-skill family`: review-stage skills whose names end in `-review`.
- `first-slice review skills`: `code-review`, `proposal-review`, and `spec-review`.
- `deferred review skills`: `plan-review` and `architecture-review`.
- `material-finding asset`: `assets/material-finding.md`, a copied structural template for one material finding.
- `result-skeleton asset`: `assets/review-result-skeleton.md`, a copied structural template for one review result.
- `parser-owned field block`: the material-finding labels parsed by `scripts/review_artifact_validation.py`.
- `parser-conformance check`: validation proving the material-finding asset labels match the review-artifact parser contract.
- `invalid fill`: a copied material-finding asset whose filled output is structurally invalid for parser-owned reasons, such as a blank, missing, or renamed `Finding ID:` label.
- `referential-integrity check`: a future validation check that a Finding ID referenced in review-log or review-resolution artifacts resolves to a detailed record containing the literal `Finding ID:` field.
- `review-class asset`: an asset owned by a deliberative review skill, limited to output structure and not review judgment or policy.

## Examples first

Example E1: material finding starts from the parser-shaped block
Given `proposal-review` includes `assets/material-finding.md`
When a reviewer records a material finding
Then the reviewer copies the asset and fills the literal `Finding ID:`, `Severity:`, `Location:`, `Evidence:`, `Required outcome:`, and `Safe resolution path:` fields
And the resulting valid finding passes review-artifact structure validation.

Example E2: invalid fills remain validator failures
Given a reviewer starts from `assets/material-finding.md`
When the reviewer leaves `Finding ID:` blank, omits the parser-owned finding identity, or renames `Finding ID:` to another label
Then structure validation fails
And the asset is treated as the default shape, not a replacement for validation
And this example does not assert severity-enum validation.

Example E3: review result status vocabularies remain distinct
Given `code-review` uses `clean-with-notes` and gate review skills use `approved`
When each first-slice review skill gains `assets/review-result-skeleton.md`
Then each result-skeleton asset preserves its source skill's review-status enum and skill-specific fields
And no shared skeleton homogenizes status semantics.

Example E4: deferred review skills are visible
Given the current `*-review` family includes `code-review`, `proposal-review`, `spec-review`, `plan-review`, and `architecture-review`
When this first slice is implemented
Then only `code-review`, `proposal-review`, and `spec-review` receive review-family assets
And `plan-review` and `architecture-review` remain named follow-ons.

Example E5: generated output proves assets ship
Given canonical first-slice review skills include mapped assets
When generated skill mirrors and temporary adapter archives are built or checked
Then every mapped asset is present in generated output
And no generated skill body or asset is hand-edited.

## Requirements

RSF-R1. The implementation MUST add review-family assets only for `skills/code-review/`, `skills/proposal-review/`, and `skills/spec-review/` in this slice.

RSF-R2. The implementation MUST defer `skills/plan-review/`, `skills/architecture-review/`, and any future `*-review` skills to follow-on work unless this spec is amended.

RSF-R3. The implementation MUST NOT add packaged `references/`, packaged `scripts/`, build-time partials, adapter install-root changes, lockfile changes, CLI behavior changes, or unrelated skill assets in this slice.

RSF-R4. Each first-slice review skill MUST include exactly these new review-family assets unless the plan records a narrower fallback required by review: `assets/material-finding.md` and `assets/review-result-skeleton.md`.

RSF-R5. Every review-family asset MUST be a copy-and-fill structural template, not a rule reference, review rubric, severity-policy source, recording-policy source, decision matrix, tutorial, hidden enum source, or substitute for `SKILL.md` operating instructions.

RSF-R6. Review-family assets MAY contain only headings, field labels, placeholders, and short fill hints.

RSF-R7. Review-family assets MUST NOT contain review-dimension definitions, review guidance, severity policy, review-status policy, material-finding sufficiency rules, safe-resolution decision rules, recording-status rules, isolation rules, scope-preservation rules, Vision fit review rules, standing artifact gate rules, workflow handoff behavior, or lifecycle-boundary rules.

RSF-R8. Each touched first-slice review `SKILL.md` MUST keep its review dimensions, review guidance, severity enum and meanings, review-status enum, recording rules, isolation rules, stop conditions, workflow handoff behavior, and artifact-placement behavior in `SKILL.md` or governing workflow artifacts.

RSF-R9. Each touched first-slice review `SKILL.md` MUST include a `Resource map` that names every packaged asset.

RSF-R10. Every review-family asset resource-map entry MUST use the literal verb `COPY`, state when to copy the asset, name the fields the reviewer fills, and instruct the reviewer not to emit unfilled placeholders.

RSF-R11. Each material-finding resource-map entry MUST instruct the reviewer to confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`.

RSF-R12. Every review-family asset MUST include metadata comments for template ID, skill name, template status, and maintained-alongside path.

RSF-R13. Review-family asset template status MUST use `normative` in this slice.

RSF-R14. Asset placeholders MUST use visible placeholder forms such as angle-bracket field names.

RSF-R15. Assets MUST NOT use empty required fields, realistic filler prose, generic filler text, `lorem ipsum`, or `your text here` as placeholder content.

RSF-R16. `assets/material-finding.md` MUST include exactly the parser-owned material-finding labels accepted by the review-artifact parser: `Finding ID:`, `Severity:`, `Location:`, `Evidence:`, `Required outcome:`, and `Safe resolution path:`, plus the accepted `needs-decision rationale:` variant when the owning skill supports that safe-resolution path.

RSF-R17. The material-finding asset field labels MUST match the existing review-artifact parser contract. This spec does not authorize parser-contract changes.

RSF-R18. The parser-owned material-finding field block MUST be byte-identical across first-slice review skills unless the plan and preservation evidence record intentional harmless non-parser variation outside the parser-owned field block.

RSF-R19. Validation MUST include a representative valid finding copied from the material-finding asset and filled with accepted values.

RSF-R20. Parser-owned structure validation MUST be exercised only for fields and shapes currently owned by the review-artifact parser.

For material findings, parser-owned structure checks include the parser-owned finding identity surface, especially `Finding ID:` presence, spelling, and non-blank value.

This requirement does not add severity-enum validation. `Severity:` remains a review artifact field but is not treated as a parser-owned enum in this slice.

RSF-R21. Representative invalid fills MUST include parser-owned structure failures, such as:

- blank `Finding ID:`;
- renamed `Finding ID:` label, such as `Finding:`;
- missing parser-owned finding identity when a material finding block is present.

Representative invalid fills MUST NOT claim that non-enum `Severity:` values fail structure validation unless a future approved spec explicitly adds severity-enum validation and names the accepted enum source.

RSF-R22. Each `review-result-skeleton.md` MUST be skill-specific.

RSF-R23. Each `review-result-skeleton.md` MUST preserve the source skill's review-status enum verbatim.

RSF-R24. The implementation MUST NOT use a shared result skeleton or shared result-skeleton base in this slice.

RSF-R25. The implementation MUST preserve `code-review` status semantics such as `clean-with-notes` separately from proposal/spec gate-review status semantics such as `approved`.

RSF-R26. Each `review-result-skeleton.md` MUST preserve the source skill's skill-specific result fields, such as code-review milestone fields and spec-review downstream readiness fields.

RSF-R27. The implementation MUST create behavior-preservation evidence that maps each extracted material-finding field and result-skeleton field from source `SKILL.md` text to the asset field.

RSF-R28. Preservation evidence MUST prove field names, field obligations, severity values, review-status values, review dimensions, recording status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, and handoff semantics are unchanged.

RSF-R29. Representative behavior parity MUST show each first-slice review skill reaches the same verdicts, material findings, recording outcomes, and handoff statements on representative review inputs after extraction as before extraction.

RSF-R30. No representative final review output may contain unfilled asset placeholders.

RSF-R31. Generated skill mirror proof MUST show every mapped first-slice review-family asset is present in generated skill mirrors.

RSF-R32. Temporary generated adapter output proof MUST show every mapped first-slice review-family asset is present in generated adapter packages.

RSF-R33. Adapter validation MUST run against temporary generated adapter output unless the validation tool itself is unavailable or blocked, in which case the blocker and smallest next action MUST be recorded.

RSF-R34. Generated adapter skill bodies and assets MUST NOT be hand-edited.

RSF-R35. Token-cost evidence MUST report common-path `SKILL.md` body size separately from total packaged footprint.

RSF-R36. Token-cost evidence MUST record per-skill asset usage expectations or rationale so reviewers can understand common-path savings separately from packaged-footprint growth.

RSF-R37. Cold-read proof MUST confirm that installed skill output plus packaged assets is sufficient for a reviewer to produce a valid material finding without repository-maintainer context.

RSF-R38. The implementation MUST update validator or fixture coverage needed to deterministically check asset inventory, resource-map `COPY` usage, asset metadata, placeholder policy, review-class asset boundaries, parser-conformance, byte-identical parser-owned field blocks, invalid-fill rejection, generated-output asset presence, and no-hand-edit proof.

RSF-R39. Validator checks for review-policy leakage into assets MUST use deterministic labels, allowlists, forbidden-label checks, or bounded heuristics declared in the test spec or plan. They MUST NOT rely on broad semantic scoring.

RSF-R40. The matching test spec MUST be approved before implementation begins.

RSF-R41. If existing `specs/skill-contract.md` asset rules are insufficient for review-family assets, parser-conformance checks, or generated-output asset presence, implementation MUST stop before skill edits and create the needed spec amendment packet.

RSF-R42. If existing `specs/skill-contract.md` asset rules are sufficient, the plan MUST record that assessment and proceed under this spec plus the matching test spec.

RSF-R43. The resource-map cross-file confirmation instruction is required in this slice, but referential-integrity validation is deferred.

RSF-R44. A future referential-integrity validator check MUST be proposed if the cross-file-reference failure recurs once after this slice ships, or if the next review-artifact learn session cites the same failure.

RSF-R45. A future build-time partials proposal SHOULD be created when another shared review concept needs single-sourcing or when a checked material-finding copy drifts despite RSF-R17 and RSF-R18.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md`;
- clean proposal-review evidence under `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`;
- `specs/skill-contract.md`;
- adjacent asset specs for proposal-family and spec-family skills;
- canonical first-slice review skill sources under `skills/code-review/`, `skills/proposal-review/`, and `skills/spec-review/`;
- review-artifact validation scripts and skill/adapters validation scripts.

Outputs:

- updated canonical first-slice review `SKILL.md` files;
- new `assets/material-finding.md` and `assets/review-result-skeleton.md` under each first-slice review skill;
- matching test spec for review-family asset and parser-conformance checks;
- optional skill-contract amendment only if a documented contract gap exists;
- change-local baseline or preservation evidence;
- representative behavior-parity evidence;
- generated skill mirror and temporary adapter proof;
- token-cost and cold-read evidence;
- validator and fixture updates needed for this contract;
- lifecycle review, explain-change, verify, and PR handoff artifacts.

## State and invariants

- `SKILL.md` remains the operating contract for review judgment, routing, policy, and lifecycle behavior.
- Review-family assets are structural copied templates only.
- The review-artifact parser remains the source of truth for parsed material-finding fields.
- The material-finding asset is downstream of the parser contract and must not compete with it.
- Asset use is the first line of defense against source-shape substitution; validation remains the backstop for malformed fills.
- First-slice review skills preserve existing verdicts, findings, recording outcomes, and handoff behavior.
- Generated outputs remain derived from canonical `skills/` sources and are not hand-edited.

## Error and boundary behavior

- If proposal status is not settled to `accepted`, downstream spec reliance blocks until settlement evidence is clear.
- If the matching test spec is not approved, implementation must not begin.
- If a review-family asset contains review policy, review judgment, enum definitions, or lifecycle rules, validation or review must fail.
- If a material-finding asset label diverges from the parser contract, validation must fail.
- If the parser-owned material-finding field block differs across first-slice skills without recorded harmless non-parser variation, validation must fail.
- If a representative valid fill from the material-finding asset fails structure validation, implementation must fix the asset, validator fixture, or both before review closeout.
- If representative parser-owned invalid fills pass structure validation, implementation must fix validation coverage before review closeout.
- If a result skeleton homogenizes review-status enums across skills, review must reject the implementation as a behavior change.
- If generated skill mirrors or temporary adapter output omit mapped assets, readiness blocks unless the blocker and smallest next action are recorded.
- If token-cost evidence reports only total packaged footprint or only common-path body size, verification must treat the token-cost evidence as incomplete.

## Compatibility and migration

This change is backward-compatible for users of the published review skills. Skill invocation, routing descriptions, review dimensions, severity values, review-status values, recording status values, artifact placement, lifecycle boundaries, handoff behavior, adapter install roots, lockfile semantics, CLI behavior, and the review-artifact parser contract remain compatible.

Generated output must be rebuilt or checked from canonical skill sources. Existing historical adapter archives are not retroactively rewritten.

Rollback is to reinline asset content into the owning `SKILL.md`, remove the affected skill's `assets/` directory, preserve generic validator improvements only when still valid, and regenerate or revalidate derived skill and adapter output from canonical sources.

## Observability

The change must leave contributor-visible evidence for:

- first-slice asset inventory and resource-map coverage;
- parser-conformance checks;
- invalid-fill rejection checks;
- byte-identical material-finding field block checks;
- review-class asset-boundary checks;
- behavior-preservation matrices;
- representative behavior parity;
- generated skill mirror and temporary adapter proof;
- token-cost common-path size and packaged-footprint reporting;
- cold-read proof;
- lifecycle review, explain-change, verify, and PR handoff artifacts.

No runtime logging, metrics, tracing, or audit event behavior is introduced.

## Security and privacy

No secrets, credentials, private data flows, authorization behavior, or external services are introduced. Assets must not contain secrets, credentials, private user data, machine-local paths, or repository-root internal paths as customer-facing requirements. Generated output must remain reproducible from canonical sources rather than hand-edited.

## Accessibility and UX

This is a Markdown skill-text and packaged-asset change. No graphical UI accessibility surface is affected. The user-facing experience is the installed review skill text plus packaged assets; cold-read proof must confirm the installed skill output explains when and how to copy each asset.

## Performance expectations

No runtime performance behavior is affected. Common-path `SKILL.md` body size should decrease or have recorded rationale when behavior preservation prevents a decrease. Total packaged footprint may increase; that is acceptable only when common-path size, total packaged footprint, and usage expectations are reported separately.

## Edge cases

EC1. A reviewer copies `material-finding.md` but leaves `Finding ID:` blank. Structure validation must fail.

EC2. Invalid material-finding fill with parser-owned identity defect.

Input: A review artifact contains a material finding block where `Finding ID:` is blank, missing, or renamed to a non-parser-owned label.

Expected: `python scripts/validate-review-artifacts.py --mode structure <change-root>` fails with a structure validation error for the parser-owned finding identity.

Non-goal: This edge case does not assert severity-enum validation.

EC3. A reviewer copies `material-finding.md` but renames `Finding ID:`. Structure validation must fail because the parser-owned label is missing.

EC4. A `material-finding.md` copy differs only in non-parser fill-hint wording. The plan or preservation evidence must either record the variation as intentional and harmless, or the copy must be made identical.

EC5. A shared result skeleton is proposed for all first-slice review skills. The shared skeleton is rejected in this slice because it risks homogenizing skill-specific review-status semantics.

EC6. `plan-review` or `architecture-review` is discovered to share the same material-finding block. It remains deferred unless this spec is amended or a follow-on proposal is accepted.

EC7. Temporary adapter proof passes but tracked expanded adapter checks show unrelated stale debt. The debt may be deferred only if temporary generated output proof and adapter validation still pass or are explicitly blocked with the smallest next action.

EC8. A representative final review output contains unfilled asset placeholders. The implementation must fix asset use or output guidance before readiness.

## Non-goals

- No changes to review-artifact parser accepted labels or parsing semantics.
- No changes to review judgment, review dimensions, severity values, severity-enum validation, review-status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, or handoff behavior.
- No packaged `references/`.
- No packaged `scripts/`.
- No build-time partials or include syntax.
- No shared result skeleton or shared result-skeleton base in this slice.
- No row assets for one-line structures.
- No application to `plan-review`, `architecture-review`, or future `*-review` skills in this slice.
- No changes to adapter install roots, lockfiles, CLI behavior, or release archive trust boundaries.
- No generated adapter hand edits.
- No retroactive legacy adapter archive rewrites.
- No produced-review-artifact readability change beyond preserving existing output structure through assets.

## Acceptance criteria

AC-RSF-001. `code-review`, `proposal-review`, and `spec-review` each have exactly `assets/material-finding.md` and `assets/review-result-skeleton.md` as review-family assets for this slice.

AC-RSF-002. `plan-review` and `architecture-review` remain unchanged by this slice and are routed through follow-on work.

AC-RSF-003. Each first-slice review skill has resource-map entries for every packaged asset using literal `COPY`, fill guidance, copy conditions, and no-unfilled-placeholder guidance.

AC-RSF-004. Every review-family asset has required metadata comments and normative template status.

AC-RSF-005. Every review-family asset is limited to headings, labels, placeholders, and short fill hints.

AC-RSF-006. No review-family asset contains review judgment, review dimensions, severity policy, review-status policy, recording rules, isolation rules, or lifecycle rules.

AC-RSF-007. `material-finding.md` field labels exactly match the review-artifact validator parser contract.

AC-RSF-008. The parser-owned material-finding field block is byte-identical across all first-slice review skills unless intentional harmless non-parser variation is recorded.

AC-RSF-009. A representative valid finding copied from `material-finding.md` passes review-artifact structure validation.

AC-RSF-010. Fixture-backed parser validation proves that invalid parser-owned finding identity shapes fail structure validation.

The proof must include at least one invalid material-finding fixture with a blank, missing, or renamed `Finding ID:` label.

The proof must not require non-enum `Severity:` values to fail unless a separate approved requirement explicitly adds severity-enum validation and names the accepted enum source.

AC-RSF-011. Each `review-result-skeleton.md` preserves its source skill's review-status enum and skill-specific result fields verbatim.

AC-RSF-012. Preservation matrices prove source-to-asset field parity per first-slice review skill.

AC-RSF-013. Representative behavior parity is unchanged per first-slice review skill.

AC-RSF-014. Generated skill mirror proof shows all mapped review-family assets are present.

AC-RSF-015. Temporary generated adapter proof and adapter validation show all mapped review-family assets are present.

AC-RSF-016. No generated skill body or generated adapter asset is hand-edited.

AC-RSF-017. Common-path `SKILL.md` token counts are recorded separately from total packaged footprint and usage expectations.

AC-RSF-018. Cold-read proof confirms an installed-skill reviewer can produce a valid material finding from the skill and packaged assets alone.

AC-RSF-019. The matching test spec is approved before implementation begins.

AC-RSF-020. The plan records whether `specs/skill-contract.md` is sufficient or whether a spec amendment packet is needed before skill edits.

## Open questions

None.

## Next artifacts

```text
plan
plan-review
test-spec
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

Planned follow-ons after this slice:

- Build-time partials proposal when another shared concept needs single-sourcing or when a checked copy drifts despite validation.
- Proposal to extend the pattern to `plan-review` and `architecture-review`.
- Proposal for review-artifact referential-integrity validation if the cross-file-reference failure recurs once after this slice ships, or if the next review-artifact learn session cites the same failure.

## Readiness

Approved after `spec-review-r2`. Ready for `plan`.
