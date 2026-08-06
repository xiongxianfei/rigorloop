# Review Resolution: Usability-First Boundary-First v0.4.0 Release

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: spec-review-r4
Review closeout: spec-review-r5
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3
Review closeout: test-spec-review-r4
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m3-r7
Review closeout: code-review-m4-r2
Review closeout: code-review-m4-r4
Review closeout: code-review-pr-readiness-r1

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `test-spec-review-r3`, `test-spec-review-r4`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`, `code-review-m3-r1`, `code-review-m3-r2`, `code-review-m3-r3`, `code-review-m3-r4`, `code-review-m3-r5`, `code-review-m3-r6`, `code-review-m3-r7`, `code-review-m4-r1`, `code-review-m4-r2`, `code-review-m4-r3`, `code-review-m4-r4`, `code-review-pr-readiness-r1`, `code-review-pr-full-gate-r1`, `code-review-pr-full-gate-r2`, `code-review-pr-full-gate-r3`
- Findings resolved: 33
- Unresolved findings: 1
- Current result: Code-review PR full-gate R3 resolves the canonical reciprocal marker bypass and keeps profile/package corrections green, but records `UBR-PRFG-CR3-001` for unknown-value fail-open and YAML-equivalent lifecycle-authority misclassification.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| UBR-TSR3-001 | accepted | resolved | T24 now pairs specs with change records, rejects missing or different lifecycle authority, and uses consistent integration proof labels. |
| UBR-SR4-001 | accepted | resolved | Folded marker placement into BND-COMPAT-001 so the applicability and boundary-definition requirement sets agree exactly. |
| UBR-PRFG-CR3-001 | accepted | open | Parse lifecycle authority semantically, reject present unknown values, and retain historical absence only. |
| UBR-PRFG-CR2-001 | accepted | resolved | Lifecycle authority now selects the canonical owner/status branch before acceptance and directly covers before-pointer placement. |
| UBR-PRFG-CR1-001 | accepted | resolved | The approved contract and reciprocal R3 probe now align canonical stage-owned and historical marker placement. |
| UBR-PRFG-CR1-002 | accepted | resolved | The profile namespace is exclusive and malformed names fail with `release-version-required`. |
| UBR-PRFG-CR1-003 | accepted | resolved | Current v0.4.0 fixtures remain current while historical skills-only cases use actual v0.3.3 identity. |
| UBR-M4-CR3-001 | accepted | resolved | The M4 R2 receipt now states the exact 26-finding historical inventory. |
| UBR-M4-CR1-001 | accepted | resolved | The wrapper fixture uses stable lifecycle metadata while grandfathered-spec review enforcement remains direct. |
| UBR-M3-CR6-001 | accepted | resolved | Required deferral authority is substantive and open; `none` is exclusive with real deferrals. |
| UBR-M3-CR5-001 | accepted | resolved | Every state enforces exact rows and applicable results; the sole emergency deferral is exactly bound. |
| UBR-M3-CR4-001 | accepted | resolved | All governed rows appear exactly once and passing proof rejects whitespace-only values. |
| UBR-M3-CR3-001 | accepted | resolved | Every pending gate row and exact finalized manifest/smoke semantics are required. |
| UBR-M3-CR2-001 | accepted | resolved | The requested release, hosted ref name, dereferenced tag, trusted commit, and checked HEAD are one identity. |
| UBR-M3-CR2-002 | accepted | resolved | Complete pending release-evidence validation replaces permissive preservation heuristics. |
| UBR-M3-CR1-001 | accepted | resolved | Finalized pre-publication evidence remains deterministic and passes preparation checks. |
| UBR-M3-CR1-002 | accepted | resolved | Profile-owned `latest` is validated and passed explicitly to trusted npm publication. |
| UBR-M3-CR1-003 | accepted | resolved | Hosted tag verification independently binds `github.sha`, checked HEAD, and the resolved tag. |
| UBR-M3-CR1-004 | accepted | resolved | Preparation generates and validates the pending standing v0.4.0 release record. |
| UBR-M2-CR2-001 | accepted | resolved | Restricted derivation environment preserves supplied-root authority and prevents ambient output. |
| UBR-M2-CR1-001 | accepted | resolved | Activation-record diagnostics are repository-relative and private-root CLI regressions pass. |
| UBR-M2-CR1-002 | accepted | resolved | Replacement refs and lazy fetch are disabled for every derivation Git read. |
| UBR-M2-CR1-003 | accepted | resolved | Rollback proof and validation bind to tracked immutable v0.3.6 metadata. |
| UBR-M2-CR1-004 | accepted | resolved | Non-string activation states return structured closed-vocabulary issues. |
| UBR-M1-CR1-001 | accepted | resolved | Each stable usability case is bound to independent required and forbidden semantics outside fixture-owned output. |
| UBR-M1-CR1-002 | accepted | resolved | Closed-vocabulary types are validated before membership and malformed values produce bounded errors. |
| UBR-SR1-001 | accepted | resolved | Exact activation fields and compatibility dispositions are present; R2 records the narrower snapshot/transition residual as UBR-SR2-001. |
| UBR-SR1-002 | accepted | resolved | The journeys now have concrete semantic oracles; R2 records the newly observed fixture-identity ambiguity as UBR-SR2-002. |
| UBR-SR1-003 | accepted | resolved | UBR-R013 owns the exact cleanup inventory and preserves ordinary validation and release steps. |
| UBR-SR2-001 | accepted | resolved | Pending and active are independently valid checked-revision snapshots, and activation preparation receives the reviewed baseline explicitly. |
| UBR-SR2-002 | accepted | resolved | The semantic journeys use existing RigorLoop validator, loader, cleanup, and release surfaces. |
| UBR-AR1-001 | accepted | resolved | The canonical package and ADR now define the exact internal callable, input, output, failure, no-write, one-time-use, and normal-validation separation contract. |
| UBR-PR1-001 | accepted | resolved | M3 now executes the release-selected CI bundle and the separate standing full gate before code review and baseline selection; M4 reruns them after activation. |
| UBR-TSR1-001 | accepted | resolved | T23 and its M2 evidence now align with CMD06; M1 retains direct UBR-R005 proof through T4. |

## Common Resolution Metadata

- Owner: spec author
- Owning stage: spec
- Validation target: revised specification plus rerun `spec-review`
- Validation evidence: spec revision R3 authoring checks and approved spec-review R3

## Finding Details

### spec-review-r4

#### UBR-SR4-001 - Compatibility applicability and boundary definitions disagree

Finding ID: UBR-SR4-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Normalize the compatibility-migration applicability and boundary-definition requirement sets without weakening UBR-R021 or repairing downstream test-spec content in the spec stage.
Rationale: UBR-R021 closes the normative authority gap, but each boundary cited by an applicable dimension must carry the exact governing requirement set declared by that dimension.
Validation target: feature-only boundary validation followed by spec-review-r5
Validation evidence: The direct feature check reports no boundary-definition mismatch; its sole expected failure is downstream test-spec scope staleness (`BFR-PROOF-MODEL-MISMATCH`).
Safe resolution path: Fold the new marker-placement partitions and outcomes into the existing compatibility boundary with the full requirement set, or use another normalized representation with exact-set agreement and no ownership overclaim.
Auto-fix class: requires-upstream-spec

### spec-review-r5

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The feature-only boundary record passes with no issues. Path-scoped validation reports only the expected downstream `BFR-PROOF-MODEL-MISMATCH` because the unchanged test spec still declares R001-R020.

### test-spec-review-r3

#### UBR-TSR3-001 - T24 treats pointer syntax as lifecycle authority

Finding ID: UBR-TSR3-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add paired feature-spec and change-record fixtures that prove the stage-owned lifecycle contract and reject owner-pointer placement without that authority.
Rationale: UBR-R021 conditions owner-pointer placement on `stage-owned-change-local-v1`; a syntactically normalized pointer alone cannot establish that governing contract.
Validation target: revised T24 and linked proof rows followed by test-spec-review-r4
Validation evidence: The R4 candidate T24 names paired spec/change-record fixtures, matching and non-matching lifecycle contracts, path-aware steps, bounded failures, and one consistent integration proof level.
Safe resolution path: Extend T24 with the authority positive and negative, retain the named placement/cardinality cases, align proof-level labels, and use the existing M2-owned boundary suite through a path-aware seam.
Auto-fix class: requires-test-spec

### test-spec-review-r4

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: T24 pairs feature specs with referenced change records, proves exact stage-owned authority and retained legacy status placement, rejects missing/different authority plus all named placement/cardinality failures, uses consistent integration labels, retains CMD06/M2 path-aware ownership, and names direct correction evidence.

### code-review-pr-full-gate-r1

#### UBR-PRFG-CR1-001 - Stage-owned marker placement lacks governing contract authority

Finding ID: UBR-PRFG-CR1-001
Disposition: accepted
Status: resolved
Owner: boundary-first proof-model spec author
Owning stage: spec
Chosen action: Amend the governing marker-placement rule and matching test specification to authorize the normalized owning-change-pointer form for stage-owned artifacts while retaining the legacy status form and exact fail-closed placement behavior.
Rationale: The implementation solves the lifecycle composition problem, but PBF-R002 still normatively requires `## Status` and the current replacement table does not replace that subject.
Validation target: spec review followed by independent PR full-gate correction rereview
Validation evidence: Code-review PR full-gate R3 confirms the approved contract, exact canonical stage-owned owner-form success, canonical stage-owned status-form rejection, historical absent-authority status success, and before/outside/duplicate failures. The narrower vocabulary/YAML issue is recorded separately as UBR-PRFG-CR3-001.
Safe resolution path: Update the owning contract and proof map through the spec workflow, preserve exact marker count and owner/status placement negatives, then rerun boundary regressions and changed-path validation.
Auto-fix class: requires-upstream-spec

#### UBR-PRFG-CR1-002 - Malformed release profiles fabricate release versions

Finding ID: UBR-PRFG-CR1-002
Disposition: accepted
Status: resolved
Owner: PR full-gate correction implementer
Owning stage: review-resolution
Chosen action: Treat `docs/releases/profiles/` as an exclusive parser branch and reject malformed or unsupported profile filenames with `release-version-required`.
Rationale: Canonical v0.4.0 extraction is correct, but near matches currently produce `profiles` or `v` with selector status `ok`, contradicting the existing fail-closed release-path contract.
Validation target: independent PR full-gate correction rereview
Validation evidence: Code-review PR full-gate R2 confirms the exclusive profile branch, canonical v0.4.0 selection, three malformed-path blockers, and all 150 selector tests.
Safe resolution path: Add exact filename validation and canonical plus near-match tests, then rerun the complete selector suite and direct v0.4.0 release validation.
Auto-fix class: declared-safe

#### UBR-PRFG-CR1-003 - Current CLI fixture replaces historical skills-only compatibility proof

Finding ID: UBR-PRFG-CR1-003
Disposition: accepted
Status: resolved
Owner: PR full-gate correction implementer
Owning stage: review-resolution
Chosen action: Parameterize fixture release identity, keep current v0.4.0 package assertions, and run the skills-only compatibility cases against an actual bundled historical version in v0.3.0 through v0.3.3.
Rationale: v0.4.0 declares opencode commands and no skills-only marker, while TTNI-INST-003 explicitly requires older official compatibility proof.
Validation target: independent PR full-gate correction rereview
Validation evidence: Code-review PR full-gate R2 confirms current fixture defaults remain v0.4.0 and the four skills-only compatibility cases consistently use actual historical v0.3.3 package, release-tag, archive, metadata-file, release-index, and marker identity; all 117 CLI and six npm publication tests pass.
Safe resolution path: Separate current and historical fixture identities without weakening archive, warning, root-shape, or mutation checks; rerun CLI and npm publication tests.
Auto-fix class: declared-safe

### code-review-pr-full-gate-r2

#### UBR-PRFG-CR2-001 - Lifecycle authority does not select the status branch

Finding ID: UBR-PRFG-CR2-001
Disposition: accepted
Status: resolved
Owner: PR full-gate correction implementer
Owning stage: review-resolution
Chosen action: Resolve the normalized owning change record before accepting either marker branch, reject stage-owned status placement, retain genuinely non-stage-owned status placement, and complete the approved T24 placement matrix.
Rationale: UBR-R021 conditions placement on lifecycle authority, so owner-form authentication alone is insufficient when the same stage-owned feature can still pass through the legacy branch.
Validation target: independent PR full-gate correction rereview
Validation evidence: Code-review R3 directly confirms the exact unquoted stage-owned owner form passes, the matching status form returns `BFR-MARKER-PLACEMENT`, absent historical authority retains status, before-pointer fails, and the focused plus complete boundary suites pass.
Safe resolution path: Apply authority before branch acceptance, add paired positive and table-driven negative T24 fixtures, rerun the boundary suite and path-aware feature/test-spec validation, and preserve the resolved selector and package-fixture corrections.
Auto-fix class: declared-safe

### code-review-pr-full-gate-r3

#### UBR-PRFG-CR3-001 - Lifecycle authority parsing fails open and is presentation-sensitive

Finding ID: UBR-PRFG-CR3-001
Disposition: accepted
Status: open
Owner: PR full-gate correction implementer
Owning stage: review-resolution
Chosen action: Parse the top-level lifecycle scalar semantically, treat absence as historical, recognize the exact stage-owned value across valid YAML serialization, and reject every present unknown or malformed value.
Rationale: Closed lifecycle authority cannot safely map arbitrary present values to legacy behavior, and YAML presentation must not invert the marker branch selected by the same semantic scalar.
Validation target: independent PR full-gate correction rereview
Validation evidence: Code-review R3 probes show unknown authority plus status returns no issue, while a quoted exact stage-owned scalar rejects owner placement and permits status placement; the current 64-test suite uses invented `legacy` as a passing non-stage fixture and has no unknown-value regression.
Safe resolution path: Use a bounded repository-owned semantic scalar parser or equivalent exact three-state seam, replace the `legacy` positive with absent historical authority, add quoted exact and `unknown_value` negatives, and rerun focused/complete boundary validation without changing selector, package, release, architecture, or plan surfaces.
Auto-fix class: declared-safe

### code-review-pr-readiness-r1

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: Independent review proves the canonical research Markdown category and exact path-scoped documentation checks through explicit and PR-discovered paths, preserves non-Markdown and mixed-path fail-closed behavior, passes the complete selector regression, and leaves release implementation and prior finding conclusions unchanged.

### code-review-m4-r4

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: Independent R4 confirms the live M4 R2 claim is exactly 26, the 26 pre-CR3 rows are the historical resolved inventory, the current overview and detail inventories contain 27 unique matching IDs, and CR3 is resolved without changing implementation conclusions.

### code-review-m4-r3

#### UBR-M4-CR3-001 - M4 R2 retains a stale 22-finding claim

Finding ID: UBR-M4-CR3-001
Disposition: accepted
Status: resolved
Owner: M4 review-evidence resolver
Owning stage: review-resolution
Chosen action: Change the M4 R2 receipt from `All 22 material findings` to `All 26 material findings` without changing its implementation conclusion.
Rationale: Independent parsing proves 26 unique overview rows and 26 matching unique detail IDs, so the corrected summary is accurate but the final holistic receipt remains numerically stale.
Validation target: code-review-m4-r4
Validation evidence: Commit `3a9f846ec1b0132a7976468552cc209579cff22d` changes only the stale R2 receipt count to 26. Independent R4 reconciliation proves 26 pre-CR3 historical findings and 27 current unique matching overview/detail IDs; focused review-artifact and change-metadata validation pass.
Safe resolution path: Correct only the stale M4 R2 count, rerun the overview/detail parse, stale-count search, review-artifact validation, change-metadata validation, and diff check, then request M4 R4.
Auto-fix class: mechanical

### code-review-m4-r2

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: Independent R2 proved meaningful archived-root wrapper execution, all 147 selector tests, direct grandfathered-spec review enforcement, exact no-derivation baseline/inventory provenance, active validation, release preparation/preflight/validation, and cumulative finding settlement.

### code-review-m4-r1

#### UBR-M4-CR1-001 - Active grandfathering leaves the selector wrapper fixture stale

Finding ID: UBR-M4-CR1-001
Disposition: accepted
Status: resolved
Owner: M4 implementer
Owning stage: review-resolution
Chosen action: Retarget the CI-wrapper execution fixture to a current adopting spec, or supply the required review classification through a supported fixture path, while preserving `BFR-GRANDFATHERED-REVIEW` for substantively changed frozen specs.
Rationale: The active inventory correctly changes historical-spec validation, but the cumulative selector suite still expects an inventory member to pass without semantic review classification.
Validation target: code-review-m4-r2
Validation evidence: The focused CI-wrapper reproduction and all 147 selector tests pass; the direct grandfathered-spec review regression remains green.
Safe resolution path: Update only the affected selector fixture and its path assertions, then rerun the focused CI-wrapper reproduction and all 147 selector tests.
Auto-fix class: declared-safe

### code-review-m3-r7

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: Independent R7 reconciled all M3 findings, directly challenged every deferral field and the complete three-state row matrix, and passed focused suites, historical release validation, preparation, and preflight.

### code-review-m3-r6

#### UBR-M3-CR6-001 - Emergency deferral completeness accepts placeholder authority

Finding ID: UBR-M3-CR6-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Require substantive deferral fields, a closed open-state status, and exclusive use of the `none` sentinel.
Rationale: Exact label binding is insufficient when owner approval, rationale, impact, risk, follow-up, deadline, and status can all be placeholders.
Validation target: code-review-m3-r7
Validation evidence: All eight required-field placeholder mutations, unknown status, mixed sentinel, missing/duplicate/unmatched deferral, and the existing three-state row matrix pass; 168 lifecycle and 102 transaction tests pass.
Safe resolution path: Add deferral-specific placeholder/status validation and sentinel exclusivity without changing release publication behavior.
Auto-fix class: declared-safe

### code-review-m3-r5

#### UBR-M3-CR5-001 - Emergency and public allowed-result authority fails open

Finding ID: UBR-M3-CR5-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Apply exact-one row validation in every state, make allowed results state/applicability-aware, and bind each permitted emergency deferral to its complete deferral record.
Rationale: Emergency evidence must prove all non-deferred gates, and public npm/CLI evidence cannot replace required registry or package proof with unsupported `not-applicable` or `deferred` states.
Validation target: code-review-m3-r6
Validation evidence: Exhaustive pending, finalized, and emergency missing, duplicate, unsupported, applicability, and deferral-binding mutations pass across all ten preflight and five registry rows; 166 lifecycle and 102 transaction tests, exact preparation/preflight, all tracked release records, and whitespace validation pass.
Safe resolution path: Replace the emergency bypass and unconditional allowed-result sets with one row contract plus exact deferral cross-checks.
Auto-fix class: declared-safe

### code-review-m3-r4

#### UBR-M3-CR4-001 - Governed row inventory and evidence cardinality remain incomplete

Finding ID: UBR-M3-CR4-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Complete the ten-row preflight inventory, enforce exact one-row cardinality for preflight and registry evidence, and strip passing smoke fields.
Rationale: Contradictory or whitespace-only evidence must not be classified as current.
Validation target: code-review-m3-r5
Validation evidence: Complete preflight and registry removal/result/duplicate mutations and whitespace-only smoke mutations fail; 102 transaction tests, 162 lifecycle tests, exact preparation/preflight, the full standing gate, and release-selected CI pass.
Safe resolution path: One authoritative row contract and exact-cardinality helper, plus bounded semantic checks.
Auto-fix class: declared-safe

### code-review-m3-r3

#### UBR-M3-CR3-001 - Pending and finalized release evidence remains structurally permissive

Finding ID: UBR-M3-CR3-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Always validate the complete gate-row inventory and bind finalized YAML to exact manifest and passing-smoke semantics.
Rationale: Preparation and preflight must reject malformed evidence before the later full release gate.
Validation target: code-review-m3-r4
Validation evidence: Every required row-removal mutation, unknown pending result, bogus manifest, and empty passing-smoke evidence fails; 100 transaction tests, 162 lifecycle tests, exact preparation/preflight, the full standing gate, and final-tree release-selected CI pass.
Safe resolution path: Parameterize supported pending results, reuse exact manifest authority and smoke semantics, and add focused regressions.
Auto-fix class: declared-safe

### code-review-m3-r2

#### UBR-M3-CR2-001 - Hosted tag identity accepts mixed release names

Finding ID: UBR-M3-CR2-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Require the hosted tag ref name and requested release to match, then resolve the explicit hosted tag ref and compare it with the trusted commit and checked HEAD.
Rationale: A release gate must prove one immutable release identity instead of accepting two names that happen to resolve to the same commit.
Validation target: code-review-m3-r3
Validation evidence: Real lightweight and annotated tags pass; missing refs, mixed names, rewritten tag commits, and mismatched trusted commits fail; the 96-test transaction suite and standing release gate pass.
Safe resolution path: Add one identity validator plus lightweight, annotated, mixed-name, and wrong-commit fixtures.
Auto-fix class: declared-safe

#### UBR-M3-CR2-002 - Finalized evidence preservation fails open

Finding ID: UBR-M3-CR2-002
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Validate the complete release metadata and standing-record contracts before preserving them, including strict pending-publication state and pre-public public fields.
Rationale: Preparation must not preserve incomplete or prematurely public evidence merely because a few marker strings remain.
Validation target: code-review-m3-r3
Validation evidence: Partial release YAML, missing standing sections, and premature public status fail; final-tree preparation, preflight, recorded-source validation, 162 lifecycle tests, and both complete release gates pass.
Safe resolution path: Reuse repository-owned parsers and lifecycle validation, then enforce the M3 pre-public state exactly.
Auto-fix class: declared-safe

### code-review-m3-r1

#### UBR-M3-CR1-001 - Finalized release evidence fails preparation check

Finding ID: UBR-M3-CR1-001
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Extend deterministic preparation ownership to the finalized local evidence shape and add final-state idempotency proof.
Rationale: CMD11 must pass on the exact tree handed to review, not only on an intermediate generated state.
Validation target: code-review-m3-r2
Validation evidence: Final-tree `prepare-release --check` and the post-finalization regression pass; preflight and both complete release gates pass.
Safe resolution path: Preserve or derive valid final values without letting generated placeholders overwrite them.
Auto-fix class: declared-safe

#### UBR-M3-CR1-002 - Ambient npm configuration can redirect the stable dist-tag

Finding ID: UBR-M3-CR1-002
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Add a closed profile dist-tag and pass it explicitly to trusted npm publication.
Rationale: The release profile must own the complete stable release identity.
Validation target: code-review-m3-r2
Validation evidence: Profile loading accepts only `latest`, unknown `next` fails closed, workflow parity requires the profile lookup and explicit `--tag`, and ambient trusted-tag regression passes.
Safe resolution path: Validate `latest`, propagate it through evidence, and regress ambient override and unknown values.
Auto-fix class: declared-safe

#### UBR-M3-CR1-003 - Trusted release gate self-supplies expected commit identity

Finding ID: UBR-M3-CR1-003
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Make trusted verification compare an independent checked tag/HEAD SHA with the full recorded release commit.
Rationale: One metadata record cannot supply both the asserted and expected immutable identity.
Validation target: code-review-m3-r2
Validation evidence: Missing and mismatched hosted tag authority regressions pass; local standing verification and release-selected CI pass with the independent check in place.
Safe resolution path: Use checked-out HEAD or trusted workflow SHA and add missing, abbreviated, mismatch, and rewritten-tag regressions.
Auto-fix class: declared-safe

#### UBR-M3-CR1-004 - Standing v0.4.0 release record is absent

Finding ID: UBR-M3-CR1-004
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Chosen action: Add the pending standing release-process record using the established release shape.
Rationale: The plan and architecture require a version-scoped identity, gate, recovery, follow-up, and privacy record.
Validation target: code-review-m3-r2
Validation evidence: `prepare-release` creates `docs/releases/v0.4.0.md`; missing-record and required-section validation regressions pass in the 87-test transaction suite.
Safe resolution path: Keep public facts pending and derive stable identity from the routine profile.
Auto-fix class: mechanical

### code-review-m2-r3

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: Independent R3 reconciled all M2 findings, directly challenged ambient Git authority and output, and passed the complete M2 command set.

### code-review-m2-r2

#### UBR-M2-CR2-001 - Ambient Git variables bypass supplied derivation root

Finding ID: UBR-M2-CR2-001
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Replace inherited process environment with a restricted Git-read environment and regress root redirection and trace output.
Rationale: The supplied root must exclusively own object authority and derivation must not create ambient output.
Validation target: code-review-m2-r3
Validation evidence: Ambient repository, object, namespace, config-injection, and trace variables cannot redirect an empty supplied root or create trace files; all 62 boundary tests and the complete M2 gate pass.
Safe resolution path: Allowlist PATH and fixed locale/config guards; exclude repository, object, namespace, config-injection, and trace variables.
Auto-fix class: declared-safe

### code-review-m2-r1

#### UBR-M2-CR1-001 - Activation parse diagnostics expose the absolute root

Finding ID: UBR-M2-CR1-001
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Use the repository-relative activation path in every parse/shape issue and add sentinel-root structured and CLI regressions.
Rationale: UBR-R017 forbids machine-local paths in validation evidence.
Validation target: code-review-m2-r2
Validation evidence: Missing, malformed, and wrong-shape CLI cases report `specs/boundary-first-activation.yaml` and suppress the private sentinel root; the 61-test suite passes.
Safe resolution path: Mechanical path substitution plus negative output assertions.
Auto-fix class: mechanical

#### UBR-M2-CR1-002 - Replacement refs can substitute the derivation baseline

Finding ID: UBR-M2-CR1-002
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Disable Git replacement objects and lazy fetch for every derivation object read and prove stable output under a replacement ref.
Rationale: The explicit full commit identity must bind the real local object graph and the helper must not acquire or write objects.
Validation target: code-review-m2-r2
Validation evidence: A real replacement ref leaves the baseline inventory at `specs/alpha.md`, every Git call asserts both guard variables, and the 61-test suite passes.
Safe resolution path: Shared derivation-only Git environment plus replacement-ref and environment regressions.
Auto-fix class: declared-safe

#### UBR-M2-CR1-003 - Rollback fixture does not use tracked v0.3.6 evidence

Finding ID: UBR-M2-CR1-003
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Copy tracked version-specific metadata for the positive case and reject v0.3.5 identities relabeled as v0.3.6.
Rationale: T12 requires the exact immutable rollback authority, not a structurally valid surrogate.
Validation target: code-review-m2-r2
Validation evidence: Positive selection matches parsed tracked v0.3.6 hashes and relabeled v0.3.5 identities fail; the 61-test suite passes.
Safe resolution path: Fixture-only correction and substitution regression.
Auto-fix class: mechanical

#### UBR-M2-CR1-004 - Malformed activation state raises TypeError

Finding ID: UBR-M2-CR1-004
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Type-check state before membership and regress list, object, and CLI malformed values.
Rationale: Closed vocabularies must fail closed before consistency checks.
Validation target: code-review-m2-r2
Validation evidence: Unknown string, list, and object values return `BFR-UNKNOWN-ACTIVATION-STATE` through direct and CLI validation; the 61-test suite passes.
Safe resolution path: String guard plus direct malformed-value tests.
Auto-fix class: mechanical

### code-review-m1-r1

#### UBR-M1-CR1-001 - Usability journey fixture is its own semantic oracle

Finding ID: UBR-M1-CR1-001
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Add independent per-case stage, artifact, required-topic, forbidden-topic, and depth-relation expectations plus coordinated-drift regression mutations.
Rationale: Stable journey IDs must preserve the approved E1-E3 semantic oracle; fixture metadata cannot author both the behavior and its expected proof result.
Validation target: code-review-m1-r2
Validation evidence: Contract-owned E1/E2 partition and stage/artifact expectations plus coordinated-drift mutations pass in the full 285-test skill-validator suite; the complete M1 command set passes.
Safe resolution path: Keep the semantic fixture concise, but validate it against contract-owned expectations outside the mutable case rows and prove required deletion, forbidden admission, stage reassignment, and coordinated expected-output edits fail.
Auto-fix class: declared-safe

#### UBR-M1-CR1-002 - Malformed vocabulary values escape as exceptions

Finding ID: UBR-M1-CR1-002
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Add string guards before closed-vocabulary membership or semantic evaluation and regress non-string JSON values for stage, trigger, and artifact fields.
Rationale: A validation fixture must fail closed with an explicit bounded error; malformed values must not escape as interpreter exceptions.
Validation target: code-review-m1-r2
Validation evidence: Array, object, and null vocabulary mutations return validation errors without exceptions; the focused tests and full 285-test skill-validator suite pass.
Safe resolution path: Guard the three fields mechanically, skip dependent evaluation for malformed rows, and add list, object, boolean, numeric, and null mutations.
Auto-fix class: mechanical

### code-review-m1-r2

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: The independent rereview reconciled both R1 findings as resolved, accepted the contract-owned semantic oracle and fail-closed type guards, and found no new material findings.

### proposal-review-r1

Review result: approved
Material findings: none
Resolution required: no

### spec-review-r1

#### UBR-SR1-001 - Tree-local activation transition is incomplete

Finding ID: UBR-SR1-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define the complete local activation transition and exact standing-contract disposition without restoring tag-era publication choreography.
Rationale: Architecture and tests need one unambiguous owner for retained manifest and grandfathering semantics.
Validation target: UBR-R006 through UBR-R008, UBR-R019, BND-STATE-001, BND-COMPAT-001, and later spec-review.
Validation evidence: Spec revision R2 added the exact active tuple, frozen inventory, and standing-contract disposition table. Spec-review R2 confirmed those corrections and recorded the narrower no-history transition residual as UBR-SR2-001.

#### UBR-SR1-002 - Concise journeys have no independent semantic oracle

Finding ID: UBR-SR1-002
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add three small concrete journey contracts with required inclusions, exclusions, and stage-owned outcomes.
Rationale: Representative semantic proof must distinguish concise correctness from both omission and exhaustive output without brittle prose metrics.
Validation target: E1 through E3, UBR-R001 through UBR-R003, UBR-R018, AC-UBR-001, AC-UBR-002, AC-UBR-011, and later spec-review.
Validation evidence: Spec revision R2 added concrete inclusion and exclusion oracles in E1 through E3 and AC-UBR-001/002. Spec-review R2 confirmed the semantic oracle and recorded the separate user-facing fixture-identity issue as UBR-SR2-002.

#### UBR-SR1-003 - Exact helper retirement lacks stable requirement ownership

Finding ID: UBR-SR1-003
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Give the exact helper and candidate-only selector retirement inventory a stable requirement ID and direct acceptance mapping.
Rationale: The proposal requires removal, while the current stable requirement only prevents ordinary execution and can leave misleading dormant surfaces.
Validation target: UBR-R013, the exact compatibility inventory, EC9, AC-UBR-008, and later spec-review.
Validation evidence: Spec-review R2 confirmed that UBR-R013 owns the closed eight-surface cleanup table and UBR-R012 preserves the original routine release mechanism.

### spec-review-r2

#### UBR-SR2-001 - Declarative snapshots retain an unobservable transition rule

Finding ID: UBR-SR2-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Remove local transition-state claims, keep pending and active as coherent snapshots, and make the reviewed baseline revision an explicit activation-preparation input.
Rationale: A thin tree-local validator cannot prove history after the specification deliberately removes transition-history authority.
Validation target: UBR-R006, UBR-R007, State and invariants, BND-STATE-001, AC-UBR-004, and later spec-review.
Validation evidence: Spec revision R3 removed the unobservable transition rule, made the baseline an explicit activation-preparation input, and passed focused validation. Spec-review R3 approved the resulting snapshot-only contract.

#### UBR-SR2-002 - Synthetic journey interfaces look like shipped commands

Finding ID: UBR-SR2-002
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Use existing RigorLoop surfaces for the three journeys or label fixture-only interfaces before any command-like token.
Rationale: Concrete semantic fixtures should not create user confusion about the product interface.
Validation target: glossary, E1 through E3, AC-UBR-001, AC-UBR-002, and later spec-review.
Validation evidence: Spec revision R3 replaced the synthetic interfaces with existing RigorLoop validator, loader, cleanup, and release surfaces. Spec-review R3 approved the journeys and acceptance criteria.

### spec-review-r3

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review approved all ten review dimensions, reconciled both R2 findings as resolved, and found no new material findings.

### architecture-review-r1

#### UBR-AR1-001 - Baseline inventory derivation has no exact interface

Finding ID: UBR-AR1-001
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Define one exact repository-owned, read-only authoring interface that accepts the full reviewed baseline revision and returns the deterministic sorted eligible-spec inventory without writing state or participating in normal `--check` validation.
Rationale: The approved spec requires an explicit baseline input and repeatable one-time derivation, while the current architecture only names a conceptual helper and rejects a preparation CLI. Planning must not invent the surviving interface or accidentally retain history dependence in checked-revision validation.
Validation target: Revised ADR decision and matching canonical Building Block, Runtime, and Crosscutting statements, followed by architecture-review R2.
Validation evidence: The revised canonical Building Block, Runtime, Crosscutting, quality, risk, and component-diagram surfaces plus ADR-20260806 name the exact callable contract. Architecture-review R2 independently approved the correction with no new material findings.
Safe resolution path: Prefer a pure function in the existing boundary-first validation module with a documented one-time repository invocation; if direct maintainer usability requires a command, permit only a read-only derivation command and keep activation writing out of scope.

### architecture-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review reconciled UBR-AR1-001 as resolved, approved all 13 review dimensions, confirmed arc42/C4/ADR sufficiency, and found no new material findings.

### plan-review-r1

#### UBR-PR1-001 - M3 selects but does not execute its release proof

Finding ID: UBR-PR1-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Add exact executable release-selected CI and standing full-gate commands to M3 before code-review handoff and selection of the reviewed pending baseline; preserve M4's active-state reruns.
Rationale: M3 owns the complete pending release payload and must independently prove package parity and routine-release preservation before M4 freezes its source state. Selector output alone is routing evidence, not execution evidence.
Validation target: Revised M3 validation commands, proof timing, and expected-result wording followed by plan-review R2.
Validation evidence: Plan revision R2 adds both executable gates and distinguishes pending-baseline proof from the active-state rerun. Plan-review R2 approved the sequencing and found no material findings.
Safe resolution path: Add `bash scripts/ci.sh --mode release --release-version v0.4.0` and add `bash scripts/release-verify.sh v0.4.0` unless the former demonstrably invokes the latter; run after M3 supports `v0.4.0` and before baseline selection.

### plan-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review confirmed that M3 executes both release gates before its pending revision becomes M4's baseline, M4 reruns them only after the activation state change, all boundary obligations close independently, and no new scope or mechanism was introduced.

### test-spec-review-r1

#### UBR-TSR1-001 - M1 proof depends on an M2-owned command

Finding ID: UBR-TSR1-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Keep T4 as M1's direct UBR-R005 proof and move T23 plus AC-UBR-012's fail-closed proof-map mutation coverage to M2.
Rationale: CMD06 and the boundary-validator regression suite are owned by M2 in the approved plan, so M1 cannot depend on them for code-review closeout.
Validation target: Revised T23 required milestone, M1 and M2 proof rows, and test-spec-review R2.
Validation evidence: Test-spec revision R2 moves T23 from M1 to M2, updates its evidence path, and preserves T4 under M1. Test-spec-review R2 approved the corrected proof timing with no material findings.
Safe resolution path: Remove T23 from M1, add it to M2, and change T23's required milestone to M2. Preserve T4 under M1 and do not move CMD06 or change plan sequencing.

### test-spec-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review confirmed that every milestone now closes with owner-aligned commands, all requirements and boundary obligations retain direct proof, and no new scope or mechanism was introduced.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Initial review recording | pass | Review record and open dispositions were recorded before lifecycle settlement. |
| R2 reconciliation | pass | Three R1 findings were reconciled, and the two narrower R2 findings are resolved by revision and review R3. |
| R3 authoring validation | pass | Boundary structure, boundary validator tests, change-metadata tests, metadata, review structure, and whitespace validation pass. |
| R3 review settlement | pass | Spec-review R3 approved the revised contract with no material findings. |
| Architecture review R1 recording | pass | The detailed review, log entry, open disposition, and exact architecture and ADR lifecycle settlements are recorded. |
| Architecture revision R2 | pass | The internal derivation function now has exact ownership, input, output, ordering, bounded failure, no-write, one-time-use, and normal-validation separation semantics. |
| Architecture review R2 settlement | pass | R2 approved the canonical architecture and ADR with no open material findings. |
| Plan review R1 recording | pass | The detailed review, log entry, accepted open disposition, and exact plan lifecycle settlement are recorded before any revision. |
| Plan revision R2 | pass | M3 now executes release-mode CI and the standing full gate before review and baseline selection; authoring validation passed. |
| Plan review R2 settlement | pass | R2 approved the revised plan with no material findings and closed UBR-PR1-001. |
| Test-spec review R1 recording | pass | The detailed review, log entry, accepted open disposition, and exact proof-timing gap are recorded before revision. |
| Test-spec revision R2 | pass | T23, CMD06, and M2 evidence now share one milestone boundary; authoring validation passed. |
| Test-spec review R2 settlement | pass | R2 approved all review dimensions with no material findings and closed UBR-TSR1-001. |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale or is not applicable.
- [x] Every deferred finding has follow-up or is not applicable.
- [x] Every `needs-decision` finding is resolved or is not applicable.
- [x] Validation evidence is recorded.
- [x] Closeout status is correct.
