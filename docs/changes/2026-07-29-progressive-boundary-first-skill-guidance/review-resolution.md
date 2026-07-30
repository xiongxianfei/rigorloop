# Review Resolution: Progressive Boundary-First Skill Guidance

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m1-r4
Review closeout: code-review-m1-r5
Review closeout: code-review-m1-r6
Review closeout: code-review-m1-r7
Review closeout: code-review-m1-r8
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m2-r4
Review closeout: code-review-m3-r1
Review closeout: code-review-m4-r1
Review closeout: code-review-m4-r2
Review closeout: code-review-m4-r3
Review closeout: code-review-m4-r4
Review closeout: code-review-m4-r5
Review closeout: code-review-m4-r6
Review closeout: code-review-m4-r7
Review closeout: code-review-m4-r8
Review closeout: code-review-m4-r9
Review closeout: code-review-m4-r10
Review closeout: code-review-m4-r11
Review closeout: code-review-m4-r12
Review closeout: code-review-m4-r13
Review closeout: code-review-m4-r14
Review closeout: code-review-m4-r15
Review closeout: code-review-m4-r16
Review closeout: code-review-m4-r17
Review closeout: code-review-m4-r18
Review closeout: code-review-m4-r19
Review closeout: code-review-m4-r20
Review closeout: code-review-m4-r21

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`,
  `proposal-review-r3`, `architecture-review-r1`,
  `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`,
  `test-spec-review-r1`, `test-spec-review-r2`, `code-review-m1-r1`,
  `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m1-r4`,
  `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`,
  `code-review-m2-r4`, `code-review-m3-r1`, `code-review-m4-r1`,
  `code-review-m4-r2`, `code-review-m4-r3`, `code-review-m4-r4`,
  `code-review-m4-r5`, `code-review-m4-r6`, `code-review-m4-r7`,
  `code-review-m4-r8`, `code-review-m4-r9`, `code-review-m4-r10`,
  `code-review-m4-r11`, `code-review-m4-r12`, `code-review-m4-r13`,
  `code-review-m4-r14`, `code-review-m4-r15`, `code-review-m4-r16`,
  `code-review-m4-r17`, `code-review-m4-r18`, `code-review-m4-r19`,
  `code-review-m4-r20`, `code-review-m4-r21`
- Findings resolved: 62
- Unresolved findings: 1
- Current result: M4 code-review R21 finding requires closing-dollar resolution.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PBS-PR1 | accepted | resolved | Selector removal now follows contract review while the existing-contract bug fix remains independent. |
| PBS-PR2 | accepted | resolved | Proposal-review R3 confirms one test specification is authored after the reviewed plan and settled through `test-spec-review`. |
| PBS-AR1 | accepted | resolved | ADR-20260729 defines the exact closed projection-manifest schema and the canonical package identifies it as the sole resource matrix. |
| PBS-AR2 | accepted | resolved | The architecture separates tracked activation state and rollback from derived package, archive, and clean-install proof. |
| PBS-TSR1 | accepted | resolved | M2 directly proves its compatibility-guidance state matrix and includes every plan-required M2 command; M4 retains composed activation and rollback proof. |
| CR-M1-R1-001 | accepted | resolved | Exact resource tuples and canonical versions now fail closed. |
| CR-M1-R1-002 | accepted | resolved | The four-question compact scan is restored to the compact core. |
| CR-M1-R1-003 | accepted | resolved | Catchable interruption restores present and absent targets before propagation. |
| CR-M1-R1-004 | accepted | resolved | Manifest and family-source identity is preserved through public consumers. |
| CR-M1-R2-001 | accepted | resolved | Canonical and skill-local recursive inventory rejects alternate and nested additions. |
| CR-M1-R2-002 | accepted | resolved | Projection and activation diagnostics preserve structured resource identity. |
| CR-M1-R3-001 | accepted | resolved | Catchable interruption restores target state before propagation. |
| CR-M1-R3-002 | accepted | resolved | Projection derives from the manifest without a parallel tuple matrix. |
| CR-M1-R3-003 | accepted | resolved | Missing-manifest diagnostics are structured through CLI and activation. |
| CR-M1-R4-001 | accepted | resolved | Skill validation translates manifest failures without traceback or private roots. |
| CR-M1-R4-002 | accepted | resolved | Manifest scalars are represented by one-way identities. |
| CR-M1-R5-001 | accepted | resolved | Canonical resource-version values use one-way diagnostic identities. |
| CR-M1-R5-002 | accepted | resolved | Symlink inventory is scoped to governed boundary resources. |
| CR-M1-R6-001 | accepted | resolved | Drift through the final stability barrier restores targets; success binds the reported snapshot identity. |
| CR-M1-R7-001 | rejected | resolved | The approved contract does not require exclusion of non-cooperative writes after the linearization read. |
| CR-M1-R7-002 | accepted | resolved | Descriptor-relative no-follow writes prevent outside mutation and recovery aggregates unsafe paths. |
| CR-M1-R7-003 | accepted | resolved | Identity diagnostics name affected stable resource layers. |
| CR-M2-R1-001 | accepted | resolved | Independent decision derivation, complete identity coverage, and shipped-guidance bindings replace self-assertion. |
| CR-M2-R2-001 | accepted | resolved | Closed sets, boolean types, stable property IDs, and unknown/removal mutations now fail closed for valid-shaped rows. |
| CR-M2-R3-001 | accepted | resolved | Unknown identities and malformed rows fail before dependent logic; valid rows remain order-independent. |
| CR-M4-R1-001 | accepted | resolved | Additional installed governed boundary resources now fail exact-inventory validation. |
| CR-M4-R1-002 | accepted | resolved | Loading profiles require exact integer schema version 1 and a closed top-level shape. |
| CR-M4-R1-003 | accepted | resolved | Evidence records reproducible baseline, candidate, and adapter-layer identities. |
| CR-M4-R2-001 | accepted | resolved | The comparable pre-split downstream operation records one initially loaded 8,318-byte resource. |
| CR-M4-R2-002 | accepted | resolved | Workflow and every requested governed resource are required in all supported adapters. |
| CR-M4-R3-001 | accepted | resolved | Exact workflow identity and shared argument semantics govern cross-adapter invocation equivalence. |
| CR-M4-R3-002 | accepted | resolved | Unknown, noncanonical, and duplicate explicit mapped-skill selections fail closed. |
| CR-M4-R4-001 | accepted | resolved | Every recognized adapter invocation occurrence must match the approved identity, operation, argument, and case. |
| CR-M4-R4-002 | accepted | resolved | Explicit skill-name preflight runs before archive validation. |
| CR-M4-R5-001 | accepted | resolved | One normalized whole-body occurrence domain rejects formatting and composed invocation corruption. |
| CR-M4-R6-001 | accepted | resolved | HTML-normalized exact-block subtraction rejects every residual adapter label. |
| CR-M4-R7-001 | accepted | resolved | Bounded inline-HTML normalization exposes residual adapter labels. |
| CR-M4-R7-002 | accepted | resolved | Exact Codex code-span multisets reject prefixes, suffixes, and trailing arguments. |
| CR-M4-R8-001 | accepted | resolved | Parser-derived rendered text exposes labels hidden by HTML or Markdown formatting. |
| CR-M4-R8-002 | accepted | resolved | Exact command spans and their owning list items enforce complete boundaries. |
| CR-M4-R9-001 | accepted | resolved | Reference-style Markdown labels and invisible separators are normalized conservatively. |
| CR-M4-R9-002 | accepted | resolved | Placeholder handling is parser-local and collision-free. |
| CR-M4-R10-001 | accepted | resolved | Exact equivalence approval uses literal raw Markdown records. |
| CR-M4-R10-002 | accepted | resolved | Combining and variation marks cannot split residual labels. |
| CR-M4-R11-001 | accepted | resolved | Approved Markdown records match byte-for-byte. |
| CR-M4-R11-002 | accepted | resolved | Residual labels use a conservative ASCII-alphanumeric projection. |
| CR-M4-R12-001 | accepted | resolved | Visible boundaries remain intact and benign negative controls stay portable. |
| CR-M4-R12-002 | accepted | resolved | Non-rendering controls are removed before whitespace normalization. |
| CR-M4-R13-001 | accepted | resolved | Nested Markdown normalizes recursively while intraword underscores remain literal. |
| CR-M4-R13-002 | accepted | resolved | Mongolian and Khmer variation controls cannot split tokens. |
| CR-M4-R14-001 | accepted | resolved | Only recognized Markdown constructs lose visible delimiters. |
| CR-M4-R15-001 | accepted | resolved | Published-skill portability now follows R3l's narrow phrase/path boundary. |
| CR-M4-R16-001 | accepted | resolved | One case-insensitive governed-skill vocabulary now drives the trigger and residual check. |
| CR-M4-R16-002 | accepted | resolved | Variables and longer paths remain portable while actual invocation syntax is rejected. |
| CR-M4-R17-001 | accepted | resolved | Complete governed dollar tokens exclude variable and math continuations. |
| CR-M4-R17-002 | accepted | resolved | Exact slash commands terminate at structural whitespace and safe phrase punctuation. |
| CR-M4-R18-001 | accepted | resolved | Unicode identifiers and paired-dollar math are excluded from governed invocation candidates. |
| CR-M4-R18-002 | accepted | resolved | Case-insensitive command identity is limited to ASCII spellings. |
| CR-M4-R18-003 | accepted | resolved | Hyphenated parent paths are excluded from slash-command scope. |
| CR-M4-R19-001 | accepted | resolved | ZWNJ and ZWJ are treated as identifier continuation. |
| CR-M4-R19-002 | accepted | resolved | Paired-dollar suppression is limited to candidate-local arithmetic forms. |
| CR-M4-R20-001 | accepted | resolved | A bounded structural suffix replaces the compressed arithmetic atom. |
| CR-M4-R21-001 | accepted | open | Require a plausible unescaped paired-math closer boundary. |

## Finding Details

### code-review-m4-r21

#### CR-M4-R21-001 - An opening dollar can masquerade as the math closer

Finding ID: CR-M4-R21-001
Disposition: accepted
Status: open
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Require an unescaped closer not followed by identifier, digit, dollar, or hyphen continuation.
Rationale: An opening token dollar is not the current candidate's closing delimiter.
Validation target: code-review-m4-r22
Validation evidence: pending

### code-review-m4-r20

#### CR-M4-R20-001 - Paired-dollar arithmetic is compressed to one ASCII atom

Finding ID: CR-M4-R20-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Use an operator-led bounded suffix without interpreting operand grammar.
Rationale: R3l distinguishes an invocation phrase from structurally paired math; it does not validate arithmetic.
Validation target: code-review-m4-r21
Validation evidence: Chained, grouped, Unicode, exponent, comparison, and unary paired expressions remain portable while every generic unrelated-later-dollar invocation control still fails; all 148 adapter tests and the planned ten-skill, three-adapter clean install pass.

### code-review-m4-r19

#### CR-M4-R19-001 - Join-control identifiers match governed prefixes

Finding ID: CR-M4-R19-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Add ZWNJ and ZWJ to the identifier-continuation predicate.
Rationale: Narrow command detection must not split portable identifier syntax.
Validation target: code-review-m4-r20
Validation evidence: Public-evaluator ZWNJ and ZWJ identifiers remain portable while standalone governed tokens fail; all 148 adapter tests pass.

#### CR-M4-R19-002 - Any later dollar suppresses a real invocation

Finding ID: CR-M4-R19-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Replace the nonlocal later-dollar scan with an empty-or-arithmetic candidate-local form.
Rationale: An unrelated later dollar is not the current candidate's math delimiter.
Validation target: code-review-m4-r20
Validation evidence: Generic-skill governed invocations followed by variables, currency, escaped dollars, or later math fail while isolated paired math remains portable; all 148 adapter tests and the planned ten-skill, three-adapter clean install pass.

### code-review-m4-r18

#### CR-M4-R18-001 - Unicode identifiers and paired math match governed prefixes

Finding ID: CR-M4-R18-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Post-filter governed-name candidates for Unicode identifier continuation and same-line paired dollars.
Rationale: R3l checks explicit invocation phrases, not identifier or math syntax.
Validation target: code-review-m4-r19
Validation evidence: Combining-mark and variation-selector identifiers plus immediate and multi-token paired math remain portable; complete governed invocations still fail; all 147 adapter tests pass.

#### CR-M4-R18-002 - Unicode case folding expands command vocabulary

Finding ID: CR-M4-R18-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Use ASCII-only case-insensitive matching for closed command names.
Rationale: Closed published names do not include Unicode case-fold aliases.
Validation target: code-review-m4-r19
Validation evidence: Long-s, dotless-i, and Kelvin-sign dollar and slash aliases remain portable while ASCII case variants fail; all 147 adapter tests pass.

#### CR-M4-R18-003 - Hyphenated parent paths match slash commands

Finding ID: CR-M4-R18-003
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Add hyphen to the slash-command left path-context exclusion.
Rationale: A command identity cannot begin inside a hyphenated route or file component.
Validation target: code-review-m4-r19
Validation evidence: `docs-/workflow` remains portable while exact punctuation-terminated commands fail; all 147 adapter tests and the planned ten-skill, three-adapter clean install pass.

### code-review-m4-r17

#### CR-M4-R17-001 - Governed names still match variable and math prefixes

Finding ID: CR-M4-R17-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Exclude Unicode identifier continuation, hyphens, and closing dollar delimiters after governed names.
Rationale: R3l checks complete invocation tokens, not prefixes in variable or math notation.
Validation target: code-review-m4-r18
Validation evidence: Underscore, Unicode-subscript, and closing-dollar continuations remain portable while complete lower-, mixed-, and uppercase governed names fail; all 147 adapter tests pass.

#### CR-M4-R17-002 - Exact slash commands escape at phrase terminators

Finding ID: CR-M4-R17-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Permit structural whitespace and safe phrase punctuation as exact slash-command terminators while excluding route and file continuations.
Rationale: Exact invocation phrases can end before prose without becoming project paths.
Validation target: code-review-m4-r18
Validation evidence: LF, CRLF, code-span, comma, and sentence-period terminations fail while route/file continuations remain portable; all 147 adapter tests and the planned ten-skill, three-adapter clean install pass.

### code-review-m4-r16

#### CR-M4-R16-001 - Dollar-token trigger and residual vocabulary differ

Finding ID: CR-M4-R16-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Compile one case-insensitive governed-skill pattern and reuse it for outer activation and residual checks.
Rationale: One vocabulary prevents context-dependent classification of the same token.
Validation target: code-review-m4-r17
Validation evidence: Standalone mixed- and uppercase governed invocations fail, the vocabulary matches all canonical published skills, and all 146 adapter tests pass.

#### CR-M4-R16-002 - Raw invocation patterns reject variables and longer paths

Finding ID: CR-M4-R16-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Restrict dollar tokens to governed skill names and make slash-command identity terminate before path punctuation.
Rationale: R3l permits narrow phrase- and path-based validation, not generic variable or path interpretation.
Validation target: code-review-m4-r17
Validation evidence: Shell and math variables plus hyphenated, dotted, and nested workflow paths remain portable; actual dollar and whitespace-delimited slash commands fail; the planned ten-skill, three-adapter clean install passes.

### code-review-m2-r1

#### CR-M2-R1-001 - Semantic scenario proof does not validate scenario decisions

Finding ID: CR-M2-R1-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Add an independent test oracle, complete the distinct scenario matrix, bind cases to shipped guidance, and prove contradictory mutations fail.
Rationale: Fixture-authored expected values cannot prove their own semantic correctness.
Validation target: code-review-m2-r2
Validation evidence: Code-review M2 R2 confirmed contradictory outcomes, routes, missing identities, missing skills, and missing guidance now fail.

### code-review-m2-r2

#### CR-M2-R2-001 - Semantic oracle accepts unknown vocabulary and removable partitions

Finding ID: CR-M2-R2-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Validate every closed input and output vocabulary and boolean type before evaluation, enforce stable property coverage, and add unknown-value and removal mutations.
Rationale: A proof oracle must fail closed before semantic consistency checks.
Validation target: code-review-m2-r3
Validation evidence: Code-review M2 R3 confirmed declared vocabularies, booleans, and required property removals fail; malformed row identity remains separately tracked.

### code-review-m2-r3

#### CR-M2-R3-001 - Case identity and malformed rows do not fail closed

Finding ID: CR-M2-R3-001
Disposition: accepted
Status: resolved
Owner: M2 implementation
Owning stage: review-resolution
Chosen action: Validate row shape, case and skill identity, and types before all dependent logic, then aggregate only validated rows.
Rationale: Closed-vocabulary validators must reject unknowns before consistency evaluation and must not crash on malformed input.
Validation target: code-review-m2-r4
Validation evidence: Code-review M2 R4 confirmed every malformed category returns bounded errors without oracle invocation and the complete M2 suite passes.

### code-review-m2-r4

No new findings. Both independent reviewers issued clean-with-notes receipts.

### code-review-m3-r1

No findings. Both independent reviewers confirmed exact path-owned routing.

### code-review-m4-r1

#### CR-M4-R1-001 - Clean-install validation accepts unowned boundary resources

Finding ID: CR-M4-R1-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Compare installed governed boundary-resource inventory with the manifest-derived adapter inventory and add representative regressions.
Rationale: Required-resource presence alone does not prove exact package ownership.
Validation target: code-review-m4-r2
Validation evidence: Representative injected compact, feature-authoring, and proof resources fail across Codex, Claude, and opencode; all 135 adapter-distribution tests and the v0.1.5 clean-install command pass.

#### CR-M4-R1-002 - Loading-profile schema version accepts non-integers

Finding ID: CR-M4-R1-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Enforce exact integer version 1 and mutate every top-level shape and version-type boundary.
Rationale: Closed schemas must fail before measurement or consistency logic.
Validation target: code-review-m4-r2
Validation evidence: Boolean, float, string, null, missing-version, extra-field, and unknown-version mutations fail; all 282 skill tests pass with 16 documented skips.

#### CR-M4-R1-003 - Package-readiness evidence is incomplete

Finding ID: CR-M4-R1-003
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Add pre-split and current byte/load baselines, exact candidate identities, and per-adapter generated/archive/install identity summaries.
Rationale: Package readiness must be reproducible from accurately labelled evidence.
Validation target: code-review-m4-r2
Validation evidence: M4 evidence identifies the pre-split commit and resource, current source and projection inventories, reviewed and fixed commit/tree/diff identities, and normalized generated/archive/install identities for all adapters; broad smoke passes 12 checks.

### code-review-m4-r2

#### CR-M4-R2-001 - Historical downstream initial-load count is inaccurate

Finding ID: CR-M4-R2-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Correct the comparable governed-operation baseline to one 8,318-byte initially loaded resource and explain its derivation.
Rationale: The cited historical skill rules explicitly load the full shared reference for governed downstream work.
Validation target: code-review-m4-r3
Validation evidence: The evidence uses one governed-operation comparison, cites the historical conditional read, and records one 8,318-byte initial resource for every pre-split family.

#### CR-M4-R2-002 - Supported-adapter resource matrix is incomplete

Finding ID: CR-M4-R2-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Make workflow adapter-portable, require each requested governed skill for each supported adapter, and assert exact per-layer resource identities.
Rationale: Report-derived portability filtering must not turn a requested all-adapter completeness check into a partial check.
Validation target: code-review-m4-r3
Validation evidence: Workflow documents Codex, Claude, and OpenCode invocation equivalents; exact generated, archive, and installed identities are 14 resources with digest `68c6f88c...004329` for each adapter; deleting requested Claude workflow fails; 137 adapter tests, the explicit v0.1.5 clean-install command, and 12-check broad smoke pass.

### code-review-m4-r3

#### CR-M4-R3-001 - Invocation-equivalence detection is fail-open

Finding ID: CR-M4-R3-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Bind portability to exact workflow identities and identical `auto: <target-stage>` arguments, with mutation coverage.
Rationale: Loose prose fragments cannot prove usable adapter commands.
Validation target: code-review-m4-r4
Validation evidence: Exact-form mutations for Codex, Claude, OpenCode, shared arguments, mismatched skill identity, and unrelated prose fail portability; the canonical workflow remains portable.

#### CR-M4-R3-002 - Explicit selection ignores unknown names

Finding ID: CR-M4-R3-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Reject unresolved and duplicate explicit mapped-skill selections before install validation.
Rationale: A completeness command must fail closed on every requested identity.
Validation target: code-review-m4-r4
Validation evidence: Mixed valid/unknown, noncanonical case, duplicate selection, and the real CLI fail before install success; 141 adapter tests, the ten-skill clean-install command, and 11-check broad smoke pass.

### code-review-m4-r4

#### CR-M4-R4-001 - Additive invocation forms evade closure

Finding ID: CR-M4-R4-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Parse all adapter invocation occurrences and reject unapproved identity, operation, argument, or case.
Rationale: A valid block cannot neutralize a contradictory invocation elsewhere.
Validation target: code-review-m4-r5
Validation evidence: Replacement and additive mutations cover bare, non-auto, case-variant, wrong-identity, and wrong-argument Codex, Claude, and OpenCode forms; all fail portability.

#### CR-M4-R4-002 - Explicit-name preflight runs too late

Finding ID: CR-M4-R4-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Share a selection-preflight helper and call it before archive validation.
Rationale: Archive state must not mask invalid requested identities.
Validation target: code-review-m4-r5
Validation evidence: Unknown selection with an empty archive root reports the selection error before any missing-archive error; 142 adapter tests, the planned ten-skill command, and 11-check broad smoke pass.

### code-review-m4-r5

#### CR-M4-R5-001 - Invocation occurrence parsing is not compositional

Finding ID: CR-M4-R5-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Discover whole-body adapter-labeled candidates before validating their fields.
Rationale: Formatting and multiple invalid fields must not remove a contradictory occurrence from validation.
Validation target: code-review-m4-r6
Validation evidence: Plain-text, HTML, whitespace, replacement, additive, pairwise, and all-field corruptions fail; all 142 adapter tests and the planned ten-skill command pass.

### code-review-m4-r6

#### CR-M4-R6-001 - Residual adapter-label closure is incomplete

Finding ID: CR-M4-R6-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Decode HTML, subtract the exact equivalence block, and reject every residual adapter label.
Rationale: Candidate discovery must not depend on a verb, identity, operation, argument, or formatting already being valid.
Validation target: code-review-m4-r7
Validation evidence: Codex, Claude, and OpenCode residual labels with alternate verbs, noun syntax, HTML, entities, wrong identity, and wrong operation all fail; all 142 adapter tests and the planned ten-skill command pass.

### code-review-m4-r7

#### CR-M4-R7-001 - Inline HTML hides residual adapter labels

Finding ID: CR-M4-R7-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Normalize bounded inline HTML to visible text before residual-label rejection and add split-tag regressions for each adapter.
Rationale: Residual-label closure must not depend on the absence of ordinary formatting tags.
Validation target: code-review-m4-r8
Validation evidence: Split-tag Codex, Claude, and OpenCode mutations fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R7-002 - Approved Codex commands are accepted as invalid prefixes

Finding ID: CR-M4-R7-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Validate the exact multiset of dollar-command code spans before removing approved forms, then add prefix, suffix, and trailing-argument regressions.
Rationale: An approved command substring does not make a malformed invocation valid.
Validation target: code-review-m4-r8
Validation evidence: Prefix, suffix, trailing-argument, HTML-suffix, and exact-block-suffix mutations fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r8

#### CR-M4-R8-001 - Rendered formatting still hides adapter labels

Finding ID: CR-M4-R8-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Derive visible HTML text with a bounded parser, normalize supported Markdown inline constructs, and add representative cross-adapter regressions.
Rationale: Residual-label closure must follow rendered visible text rather than raw formatting syntax.
Validation target: code-review-m4-r9
Validation evidence: Comment, quoted-attribute, unknown-element, emphasis, and link mutations fail across adapter labels; all 142 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R8-002 - Adjacent text extends exact command code spans

Finding ID: CR-M4-R8-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Validate the complete Markdown list items owning target, status, and off commands and add adjacent-token regressions.
Rationale: Exact code-span content is insufficient when surrounding text remains part of the same command token.
Validation target: code-review-m4-r9
Validation evidence: Adjacent suffix and trailing-argument mutations fail for target, status, and off owning records; all 142 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r9

#### CR-M4-R9-001 - Reference-style Markdown hides rendered adapter labels

Finding ID: CR-M4-R9-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Conservatively remove reference-link brackets after inline-link normalization and add full, collapsed, and shortcut-reference regressions.
Rationale: Markdown reference syntax must not interrupt a rendered adapter label.
Validation target: code-review-m4-r10
Validation evidence: Full, collapsed, and shortcut-reference mutations and invisible-separator mutations fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R9-002 - In-band placeholder normalization changes invocation semantics

Finding ID: CR-M4-R9-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Remove in-band sentinels and preserve approved placeholder start tags only while parsing exact contract records.
Rationale: Caller-controlled text must not collide with normalization state or hide labels through globally protected custom tags.
Validation target: code-review-m4-r10
Validation evidence: Literal and encoded sentinel mutations and custom placeholder-tag mutations fail while the canonical contract remains portable; all 142 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r10

#### CR-M4-R10-001 - Rendered text substitutes for exact equivalence source

Finding ID: CR-M4-R10-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Require one exact raw code-span multiset for every Codex, Claude, OpenCode, and declared-placeholder record before rendered residual checks.
Rationale: Approval semantics must preserve copyable literal command and placeholder source.
Validation target: code-review-m4-r11
Validation evidence: Zero-width/private identities, altered operations, uppercase, spaced, self-closing, encoded, and nested placeholders fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R10-002 - Invisible combining and variation marks hide adapter labels

Finding ID: CR-M4-R10-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Remove CGJ and variation-selector ranges during rendered residual normalization and add literal and entity regressions.
Rationale: Invisible marks must not interrupt a rendered adapter identity.
Validation target: code-review-m4-r11
Validation evidence: Literal and encoded CGJ and variation-selector label splits fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r11

#### CR-M4-R11-001 - Whitespace folding bypasses exact source validation

Finding ID: CR-M4-R11-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Compare each approved Markdown list record byte-for-byte with its canonical multiline source.
Rationale: Exact copyable commands require literal source whitespace.
Validation target: code-review-m4-r12
Validation evidence: NBSP, EM SPACE, and tab mutations in Claude and OpenCode records fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R11-002 - Invisible controls and Hangul fillers split residual labels

Finding ID: CR-M4-R11-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Detect labels on a conservative ASCII-alphanumeric projection of rendered remaining text.
Rationale: Enumerating Unicode invisibility categories leaves avoidable fail-open gaps.
Validation target: code-review-m4-r12
Validation evidence: C0 control, Hangul filler, entity, combining, format, and private-use label splits fail; all 142 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r12

#### CR-M4-R12-001 - Projection synthesizes labels from visible portable prose

Finding ID: CR-M4-R12-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Preserve visible boundaries, normalize paired Markdown constructs contextually, and add benign negative controls.
Rationale: Portability detection must remain narrow as well as fail closed.
Validation target: code-review-m4-r13
Validation evidence: Encode-X, open-code, cod_ex, and visible non-ASCII slash tokens remain portable; all 143 adapter tests and the planned ten-skill clean-install command pass.

#### CR-M4-R12-002 - Whitespace folding hides control-split invocations

Finding ID: CR-M4-R12-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Remove governed non-rendering characters before ASCII structural whitespace normalization and syntax checks.
Rationale: Invisible controls join tokens; visible characters and whitespace remain boundaries.
Validation target: code-review-m4-r13
Validation evidence: Unit, file, and group separators plus NEL cannot split residual slash commands; all 143 adapter tests and the planned ten-skill clean-install command pass.

### code-review-m4-r13

#### CR-M4-R13-001 - Markdown normalization is not recursively delimiter-aware

Finding ID: CR-M4-R13-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Recursively normalize bounded paired delimiters and add nested positives plus intraword-underscore negatives.
Rationale: Rendered labels and literal identifier punctuation must both be preserved correctly.
Validation target: code-review-m4-r14
Validation evidence: Triple, mixed, nested strike, and link-label formatting expose labels while intraword underscore keys remain portable; all 143 adapter tests and the planned clean-install command pass.

#### CR-M4-R13-002 - Default-ignorable variation ranges remain incomplete

Finding ID: CR-M4-R13-002
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Add Mongolian and Khmer ranges with literal, entity, and slash-command regressions.
Rationale: Governed variation controls are non-rendering token joiners.
Validation target: code-review-m4-r14
Validation evidence: Literal/entity Mongolian and Khmer label splits plus Mongolian slash-command splits fail; all 143 adapter tests and the planned clean-install command pass.

### code-review-m4-r14

#### CR-M4-R14-001 - Literal delimiters are treated as rendered Markdown

Finding ID: CR-M4-R14-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Normalize recognized code spans, links, references, and paired emphasis before HTML entity decoding, preserving every unmatched or unresolved delimiter.
Rationale: Visible punctuation must remain a boundary and entity-origin text must not become formatting.
Validation target: code-review-m4-r15
Validation evidence: Recognized code, links, references, and emphasis expose labels while unmatched, unresolved, and entity-origin delimiters remain portable; all 143 adapter tests and the planned clean-install command pass.

### code-review-m4-r15

#### CR-M4-R15-001 - Reference handling requires a Markdown block parser

Finding ID: CR-M4-R15-001
Disposition: accepted
Status: resolved
Owner: M4 implementation
Owning stage: review-resolution
Chosen action: Keep byte-exact approved records and narrow raw dollar/slash checks; remove residual rendered-label parsing and the speculative CommonMark matrix.
Rationale: `specs/skill-contract.md` R3l requires narrow phrase- or path-based static validation.
Validation target: code-review-m4-r16
Validation evidence: Byte-exact records and narrow raw dollar/slash phrases fail as required; rendered Markdown, HTML, Unicode, and adapter-labeled prose remain outside semantic interpretation; all 143 adapter tests and the planned clean-install command pass.

### code-review-m1-r1

#### CR-M1-R1-001 - Exact resource authority is not closed

Finding ID: CR-M1-R1-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Validate the manifest against one immutable exact resource contract and validate every canonical resource version before projection.
Rationale: Generic containment and known-consumer membership do not prove the ADR-exact ownership matrix.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirmed exact tuple and canonical version mutations fail closed.

#### CR-M1-R1-002 - Compact core omits the compact scan

Finding ID: CR-M1-R1-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Add the exact PBS-R007 questions to the compact core, reproject, and refresh identities.
Rationale: PBS-R012 assigns compact scan semantics to the compact resource independently of M2 stage-local invocation.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirmed the compact core and all ten projections contain the exact scan.

#### CR-M1-R1-003 - Interrupted writes leave a mixed tree

Finding ID: CR-M1-R1-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Snapshot target state after preflight, restore on handled write failure, and prove early, middle, final, and retry paths.
Rationale: T2 requires an interrupted-write proof, while current code proves only invalid-input preflight.
Validation target: code-review-m1-r4
Validation evidence: Code-review M1 R3 reproduced partial mutation on `KeyboardInterrupt`; broader recovery proof remains pending.

#### CR-M1-R1-004 - Activation diagnostics erase manifest failure identity

Finding ID: CR-M1-R1-004
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Use structured projection errors and retain source check, path, expectation, and reason through activation validation.
Rationale: PBS-R037 requires the actual affected resource and blocking reason.
Validation target: code-review-m1-r4
Validation evidence: Code-review M1 R3 confirmed family-source identity but reproduced missing-manifest fallback; complete public diagnostic proof remains pending.

### code-review-m1-r2

#### CR-M1-R2-001 - Alternate-version resources escape inventory validation

Finding ID: CR-M1-R2-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Inventory every `boundary-first-*.md` resource in canonical and governed reference roots and reject non-manifest paths.
Rationale: A version-specific glob cannot prove additional or mixed-version closure.
Validation target: code-review-m1-r3
Validation evidence: Code-review M1 R3 confirmed recursive canonical and skill-local inventory rejects alternate and nested additions.

#### CR-M1-R2-002 - Structured diagnostics remain incomplete on sibling paths

Finding ID: CR-M1-R2-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Structure missing-source and path errors, use one bounded CLI formatter, and prove activation and CLI family-resource failures.
Rationale: Fixing one manifest-version case does not satisfy PBS-R037 across public and sibling validation paths.
Validation target: code-review-m1-r3
Validation target: code-review-m1-r4
Validation evidence: Family-resource and missing-manifest CLI and activation diagnostics pass in the 24-test projection and 61-test activation suites; independent R4 confirmation remains pending.

### code-review-m1-r3

#### CR-M1-R3-001 - Catchable interruption leaves a mixed projection tree

Finding ID: CR-M1-R3-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Restore snapshots for catchable in-process interruptions before preserving the original exception.
Rationale: T2 requires coherent recovery from an interrupted projection, not only `OSError`.
Validation target: code-review-m1-r4
Validation evidence: Both pre-existing and initially absent target-set interruption cases restore exactly, re-raise `KeyboardInterrupt`, and retry successfully in the 24-test projection suite; independent R4 confirmation remains pending.

#### CR-M1-R3-002 - Projection code retains a parallel resource inventory

Finding ID: CR-M1-R3-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Remove the duplicated source, target, and consumer matrix and validate manifest structure through independent invariants.
Rationale: The ADR assigns sole declarative projection authority to the manifest.
Validation target: code-review-m1-r4
Validation evidence: The source-level no-parallel-matrix regression and approved manifest-identity mutations pass in the 24-test projection suite; independent R4 confirmation remains pending.

#### CR-M1-R3-003 - Missing-manifest diagnostics lose path and expectation

Finding ID: CR-M1-R3-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Raise a structured missing-manifest error and prove exact CLI and activation propagation.
Rationale: PBS-R037 applies to required manifest absence as well as family resources.
Validation target: code-review-m1-r4
Validation evidence: Missing-manifest CLI and activation regressions preserve exact path and expected condition in the 24-test projection and 61-test activation suites; independent R4 confirmation remains pending.

### code-review-m1-r4

#### CR-M1-R4-001 - Skill validation leaks malformed-manifest exceptions

Finding ID: CR-M1-R4-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Translate projection contract failures into bounded skill-validation errors and prove missing and malformed CLI paths.
Rationale: PBS-R037 applies consistently across public validator consumers.
Validation target: code-review-m1-r5
Validation evidence: Missing and unknown-schema isolated skill-validation CLI cases return code 1 with structured repository-relative errors, no traceback, and no temporary root; independent R5 confirmation remains pending.

#### CR-M1-R4-002 - Manifest diagnostics expose untrusted scalar values

Finding ID: CR-M1-R4-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Remove untrusted values from diagnostic messages and consistently redact the offending-value field.
Rationale: Actionable diagnostics do not require disclosure of the rejected payload.
Validation target: code-review-m1-r5
Validation evidence: Secret-bearing consumer fixtures preserve stable identities while excluding the scalar from projection CLI and activation serialization; independent R5 confirmation remains pending.

### code-review-m1-r5

#### CR-M1-R5-001 - Canonical resource diagnostics disclose untrusted version scalars

Finding ID: CR-M1-R5-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Hash canonical version offending values and prove public and activation paths.
Rationale: Resource contents are untrusted diagnostic input.
Validation target: code-review-m1-r6
Validation evidence: Secret-bearing canonical version fixtures preserve stable check, path, reason, and expected version while emitting only a SHA-256 offending identity through CLI and activation; independent R6 confirmation remains pending.

#### CR-M1-R5-002 - Projection inventory rejects unrelated symlinked resources

Finding ID: CR-M1-R5-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Restrict recursive symlink discovery to the boundary resource namespace while retaining governed path ancestor checks.
Rationale: The boundary validator must not claim unrelated packaged resources.
Validation target: code-review-m1-r6
Validation evidence: Unrelated skill-local and canonical reference symlinks pass, while existing governed and boundary-resource symlink cases fail closed in the 26-test projection suite; independent R6 confirmation remains pending.

### code-review-m1-r6

#### CR-M1-R6-001 - Projection can return success for an already-stale transaction

Finding ID: CR-M1-R6-001
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Snapshot canonical inputs and enforce a final stability barrier, restoring write targets on drift.
Rationale: Cached-byte target checks cannot prove currency against inputs that change during the transaction.
Validation target: code-review-m1-r7
Validation evidence: Twelve manifest/resource and early/middle/final mutation cases reject success, restore prior targets, and retry deterministically. Success reports the snapshot identities; later non-cooperative drift is rejected by activation or the next check as required by PBS-R033, PBS-R034, and BND-TEMPORAL-001.

### code-review-m1-r7

#### CR-M1-R7-001 - Final-read race is treated as an unbounded concurrency guarantee

Finding ID: CR-M1-R7-001
Disposition: rejected
Status: resolved
Owner: workflow orchestrator
Owning stage: review-resolution
Chosen action: Keep success defined by the reported immutable input snapshot and retain downstream drift rejection.
Rationale: PBS-R033 requires incomplete or divergent states to fail closed, PBS-R034 governs atomic activation, and BND-TEMPORAL-001 says drift blocks activation. None requires a global lock against non-cooperative writes occurring after the projector's final read.
Validation target: code-review-m1-r8
Validation evidence: Static contract interpretation plus existing snapshot-identity, drift, activation, and retry tests.

#### CR-M1-R7-002 - Target topology drift can escape containment or abort recovery

Finding ID: CR-M1-R7-002
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Use descriptor-relative no-follow target operations and aggregate restoration path failures.
Rationale: Repository containment applies even under a target-parent swap.
Validation target: code-review-m1-r8
Validation evidence: A target-parent swap cannot write outside; restoration continues for every unaffected target and reports `BFR-PROJECTION-RESTORE` for the unsafe path in the 28-test projection suite; independent R8 confirmation remains pending.

#### CR-M1-R7-003 - Exact-manifest diagnostics omit the affected resource layer

Finding ID: CR-M1-R7-003
Disposition: accepted
Status: resolved
Owner: M1 implementation
Owning stage: review-resolution
Chosen action: Add opaque per-layer diagnostic identities and report differing stable resource IDs.
Rationale: PBS-R037 requires the affected resource layer without requiring disclosure of rejected values.
Validation target: code-review-m1-r8
Validation evidence: Exact compact, feature-authoring, and proof tuple mutations identify the affected stable layer while retaining one-way offending identities in the 28-test projection suite; independent R8 confirmation remains pending.

### code-review-m1-r8

Status: approved
Material findings: none
Resolution required: no new findings
Evidence: reviews/code-review-m1-r8.md

### proposal-review-r1

#### PBS-PR1 - Selector removal precedes its contract gate

Finding ID: PBS-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Separate the already-approved embedded-status bug fix from the new selector policy, and place selector removal plus boundary-guidance implementation after amended feature and test specifications, spec review, architecture assessment, plan review, and proof-map review.
Rationale: The stage-owned lifecycle specification already governs the embedded-status correction, while selector routing is a new contributor-visible behavior that requires contract-first review.
Validation target: proposal-review-r2
Validation evidence: Proposal-review R2 confirmed that selector removal is separated from the existing-contract bug fix and remains behind contract review.

### proposal-review-r2

#### PBS-PR2 - Test-spec timing and review ownership are duplicated

Finding ID: PBS-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Chosen action: Use one stage-owned sequence in which feature contracts settle through `spec-review`, architecture settles through `architecture-review`, the plan settles through `plan-review`, and one test specification is then authored and settled through `test-spec-review` before implementation.
Owning stage: proposal
Rationale: This follows the approved workflow, prevents duplicate proof-map work, and keeps each review stage within its artifact authority.
Expected proof: A revised proposal and proposal-review R3 confirm one test-spec artifact, correct review ownership, and the approved artifact order.
Validation evidence: Proposal-review R3 confirmed the corrected artifact order, one test-spec artifact, and stage-owned review authority.

### architecture-review-r1

#### PBS-AR1 - Projection manifest shape is not exact

Finding ID: PBS-AR1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Add the exact closed top-level and resource-entry schema,
resource IDs, paths, consumer ordering, duplicate rules, and unknown-field
behavior to the ADR and matching canonical architecture.
Rationale: The approved spec and spec-review explicitly delegate this closed
data contract to architecture, and downstream planning and proof need one
implementable vocabulary.
Validation target: architecture-review-r2
Validation evidence: Architecture-review R2 confirms the exact top-level and
entry keys, values, resource IDs, paths, order, consumers, duplicate rules,
unsafe-path rules, and unknown-field behavior are complete and testable.

#### PBS-AR2 - Commit-level rollback includes ephemeral outputs

Finding ID: PBS-AR2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Separate the exact tracked activation transaction from
generated, packed, and installed proof; define pre-activation rollback as
tracked revert plus derived-output regeneration or discard.
Rationale: Generated packages and clean target installs are derived validation
surfaces under repository governance and cannot be Git-reverted as commit
contents.
Validation target: architecture-review-r2
Validation evidence: Architecture-review R2 confirms the tracked activation
transaction, derived proof set, atomic acceptance boundary, pre-activation
recovery, and immutable post-activation rollback are distinct and
implementable.

### test-spec-review-r1

#### PBS-TSR1 - M2 compatibility and command proof is deferred or omitted

Finding ID: PBS-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add direct M2 proof for pending, active-candidate,
grandfathered non-substantive, and substantive revision guidance; bind
`BND-COMPAT-001` and `INT-004` to M2 evidence as well as later M4
composition; and add CMD2 to the M2 proof row.
Rationale: The approved plan changes this guidance in M2 and names the
projection check as an M2 command, so proof cannot be deferred entirely to
M4.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R2 confirms T4, PRF-014, PRF-020,
PRF-022, PRF-023, and the M2 milestone row close the finding without changing
the contract or scenario count.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Proposal review | changes-requested | `PBS-PR1` records the contract-first sequencing defect. |
| Proposal review R2 | changes-requested | `PBS-PR1` is resolved; `PBS-PR2` records the remaining artifact-order defect. |
| Proposal review R3 | approved | `PBS-PR1` and `PBS-PR2` are resolved; no material findings remain. |
| Architecture review R1 | changes-requested | `PBS-AR1` and `PBS-AR2` are recorded and remain open pending architecture revision. |
| Architecture review R2 | approved | `PBS-AR1` and `PBS-AR2` are resolved; no material findings remain. |
| Plan review R1 | blocked | No plan-content finding was recorded; the plan remains `authoring` because primary-plan registration requires workflow-owned `planned_work`. |
| Plan review R2 | approved | One-time plan initialization resolves the lifecycle precondition; the plan is ready for test-spec. |
| Test-spec review R1 | changes-requested | `PBS-TSR1` records the M2 proof-timing and command-ledger mismatch. |
| Test-spec review R2 | approved | `PBS-TSR1` is resolved; the proof map permits isolated M1 implementation handoff. |

## Clean review receipts

### proposal-review-r3

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/proposal-review-r3.md

### spec-review-r1

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/spec-review-r1.md

### architecture-review-r2

Status: approved
Material findings: none
Resolution required: no new findings; reconciles `PBS-AR1` and `PBS-AR2`
Evidence: reviews/architecture-review-r2.md

### plan-review-r1

Status: blocked
Material findings: none
Resolution required: no finding disposition; lifecycle precondition resolved
by planned-work initialization and confirmed by plan-review R2
Evidence: reviews/plan-review-r1.md

### plan-review-r2

Status: approved
Material findings: none
Resolution required: no
Evidence: reviews/plan-review-r2.md

### test-spec-review-r1

Status: changes-requested
Material findings: PBS-TSR1
Resolution required: accepted and resolved by test-spec-review R2
Evidence: reviews/test-spec-review-r1.md

### test-spec-review-r2

Status: approved
Material findings: none
Resolution required: no new findings; confirms `PBS-TSR1` resolution
Evidence: reviews/test-spec-review-r2.md

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [ ] Validation evidence is recorded for all accepted findings.
- [x] Closeout status is correct.
