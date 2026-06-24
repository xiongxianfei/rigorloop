# Semantic Source-Line Contract for Review-Critical Markdown

## Status

accepted

## Problem

RigorLoop has repeatedly corrected arbitrary hard wrapping in human-facing Markdown.
The rendered Markdown often looked acceptable, but meaningful phrases, lifecycle chains, commands, or public positioning were split across physical source lines.

The pattern first appeared in adopter-facing `README.md` and `VISION.md` prose.
It later recurred in architecture-skill and change-explanation prose.
A later correction overreacted by wrapping complete sentences and list content more aggressively, which clarified the real issue: long source lines are not the defect; splitting complete semantic units is the defect.

The latest README recurrence followed the same sequence:

```text
mechanically wrap prose
receive correction
fix the most visible command
leave surrounding prose wrapped
receive another correction
finally re-read and repair the complete source section
```

Durable learn guidance already recommends semantic line breaks for adopter-facing, source-of-truth, and review-critical prose.
That guidance is explanatory rather than authoritative, so the repository still lacks a normative source-line formatting contract, a defined coverage set, deterministic versus audit-only classification, bounded validation, generated-content ownership rules, regression fixtures, and a source-review step before PR handoff.

The result is repeated correction and avoidable validation churn.

## Goals

- Establish an authoritative semantic source-line contract for review-critical Markdown.
- Preserve semantic units rather than wrapping prose to an arbitrary column width.
- Define the first-slice Markdown surfaces covered by enforcement or audit.
- Distinguish prose paragraphs, list items, table rows, commands, code blocks, generated content, and other Markdown structures.
- Add a bounded, non-mutating documentation-prose validator.
- Make deterministic violations fail on selected high-value surfaces.
- Report ambiguous cases as audit warnings rather than guessing.
- Add regression fixtures for the observed README, vision, skill, and explain-change failure patterns.
- Add a source-form review step before PR handoff.
- Preserve existing rendered Markdown, marker synchronization, vocabulary checks, and guide validation.
- Avoid repository-wide prose reflow.
- Keep learn records as rationale while moving the enforceable rule into an action-owning contract.

## Non-goals

- Do not impose an 80-, 88-, 100-, or other fixed-column limit on prose.
- Do not require all Markdown paragraphs to be physically one line.
- Do not rewrite every existing Markdown file.
- Do not reflow specs, test specs, plans, review records, logs, or historical evidence in the first slice.
- Do not add a general grammar or writing-quality checker.
- Do not automatically rewrite prose.
- Do not hand-edit generated README marker content.
- Do not treat every long line as an error.
- Do not forbid deliberate clause-level line breaks when they preserve meaning.
- Do not change Markdown rendering semantics.
- Do not change workflow stage order, skill behavior, lifecycle claims, or artifact locations.
- Do not make learn topics the normative owner of formatting policy.

## Vision fit

fits the current vision

RigorLoop emphasizes artifacts that humans can inspect, review, and resume from source.
For Markdown artifacts, source shape is part of reviewability even when rendered output is unchanged.
A mechanically wrapped sentence can obscure a value proposition, lifecycle transition, instruction, or review finding in a diff.

This proposal strengthens source review without changing document meaning.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Explain why prose kept being split | in scope | Problem, Context |
| Preserve complete semantic units | in scope | Goals, Recommended Direction |
| Avoid arbitrary hard wrapping | in scope | Goals, Non-goals |
| Improve README and human-facing Markdown reviewability | in scope | Scope Budget, Expected Behavior Changes |
| Prevent recurrence automatically | in scope | Recommended Direction, Testing and Verification Strategy |
| Avoid a blanket rule for all Markdown | in scope | Non-goals, Scope Budget |
| Preserve generated marker ownership | in scope | Recommended Direction, Architecture Impact |
| Avoid another symptom-only correction | in scope | Review guidance in Recommended Direction |
| Rewrite historical documentation | out of scope | Non-goals, Scope Budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Authoritative semantic source-line contract | core to this proposal | Existing learn guidance is not authoritative. |
| README and VISION enforcement | core to this proposal | These are high-value adopter-facing surfaces with direct recurrence evidence. |
| Canonical skill prose audit | first-slice candidate | Related recurrence occurred in `SKILL.md`, but broad enforcement needs false-positive evidence. |
| `explain-change.md` prose audit | first-slice candidate | Related recurrence occurred in change-explanation prose, but immediate enforcement would widen the slice. |
| Deterministic validator fixtures | core to this proposal | Fixtures protect against repeating named failures. |
| Ambiguous-case warning mode | core to this proposal | Semantic boundaries cannot all be inferred safely. |
| README marker ownership handling | same-slice dependency | Generated sections must not be hand-edited. |
| Workflow and authoring guidance update | same-slice dependency | Contributors need the rule before validation fails. |
| Repository-wide enforcement | separate proposal | Existing Markdown contains unknown baseline debt. |
| Automatic prose rewriting | out of scope | It is too likely to alter meaning or create noisy diffs. |
| Full Markdown AST or style framework | deferable follow-up | The first slice needs bounded structure awareness, not a broad formatting framework. |

## Context

The durable learn guidance recommends source line breaks optimized for review rather than rendering alone.
Its preferred shape is one sentence or natural semantic unit per line, with bullets, tables, or diagrams used when dense content becomes difficult to scan.

The June 23 correction sharpened the distinction:

```text
semantic line:
  one complete sentence, list item, table row, or command unit

bad hard wrap:
  one sentence split across multiple source lines only because it is visually long
```

The June 24 recurrence adds enough evidence to route this beyond learn guidance.
The same pattern survived multiple corrections, and existing validation still could not distinguish the undesired source shape.

Current validation checks Markdown and repository syntax, README marker shape, retired vocabulary, skill contracts, guide-system relationships, and whitespace hygiene.
It does not check whether a prose unit is split at an arbitrary physical line boundary.

The repository also lacks a taxonomy that separates review-critical prose, normative long-form contracts, generated prose, tables and code, and historical evidence.
A universal Markdown wrapping rule would therefore be inappropriate.

## Options considered

### Option 1: Keep learn guidance only

This has no implementation cost and the current guidance is directionally correct.
It is insufficient because the issue has already recurred despite that guidance, and the rule remains outside action-owning contracts.

Rejected.

### Option 2: Add a fixed Markdown line-length rule

This is easy to automate and common tool support exists.
It directly recreates the defect by optimizing column width instead of reviewability, and it would flag correct long sentences, links, tables, commands, and lifecycle chains.

Rejected.

### Option 3: Configure a formatter to reflow Markdown automatically

This could make output mechanically consistent with low author effort.
Most formatters optimize width rather than meaning, can rewrite reviewer-sensitive prose, and can conflict with marker-generated sections.

Rejected for the first slice.

### Option 4: Add an authoring checklist without validation

This supports human judgment with low implementation risk.
It still relies entirely on author and reviewer memory, and repeated incidents show memory-only mitigation is insufficient.

Useful but incomplete.

### Option 5: Add an authoritative contract, targeted review guidance, and bounded validation

This fixes the ownership gap, preserves human judgment for ambiguous prose, automates deterministic cases, limits enforcement to high-value surfaces first, avoids broad repository reflow, and gives direct regression coverage.
It requires a small Markdown-aware validator and careful false-positive control.

Recommended.

## Recommended direction

Choose Option 5.

Use three layers:

```text
authoritative contract:
  defines semantic source-line behavior

authoring and review guidance:
  tells contributors how to apply it

bounded validator:
  catches deterministic violations and audits ambiguous cases
```

Create or amend these normative artifacts:

```text
specs/documentation-source-formatting.md
specs/documentation-source-formatting.test.md
```

The spec should own semantic source-unit definitions, first-slice coverage, exclusions, validator severity, generated-content behavior, rollout, and compatibility.
`CONTRIBUTING.md` should own the short contributor-facing summary and validation command because GitHub surfaces it during pull request creation.
`docs/workflows.md` may link to that contributor-facing policy without duplicating the contract.
`docs/learn/topics/documentation-prose.md` should remain historical rationale and example material, not the normative owner.

The first-slice coverage should be:

| Tier | Surface | Treatment |
| --- | --- | --- |
| A | `README.md`, `VISION.md` | enforce deterministic violations on human-authored prose |
| B | `skills/**/SKILL.md`, `docs/changes/**/explain-change.md` | audit and review evidence in the first slice |
| C | `specs/**`, `docs/plans/**`, `docs/changes/**/reviews/**`, `docs/learn/**`, generated output, historical release evidence, third-party documentation | exclude from first-slice enforcement |

The source-line contract should distinguish semantic units from mechanical wraps:

| Content | Source unit |
| --- | --- |
| Ordinary prose | One complete sentence per physical line when practical |
| Long sentence | Keep intact, rewrite, or split only at a deliberate clause boundary |
| List item | One complete item; use nested structure rather than arbitrary continuation |
| Table | One complete row per physical line |
| Command | One complete command line or fenced multiline command |
| Lifecycle chain | One intact chain or a list or diagram |
| Heading | One heading line |
| Blockquote | One semantic quoted unit per line |
| Code | Governed by its language formatter, not prose rules |

The validator should be non-mutating and structure-aware.
It should identify Markdown blocks before evaluating prose and exclude or separately handle fenced code blocks, indented code, tables, HTML blocks, link definitions, headings, thematic breaks, generated or marker-owned regions, URLs, long inline code, explicit Markdown hard breaks, and YAML frontmatter.

Deterministic errors should fail in Tier A for cases such as ordinary prose split mid-phrase, commands split outside valid fenced or continuation structures, lifecycle chains split between connected elements, mechanically continued list items, and known regression phrases such as `AI agents` or `proposal to spec`.
Deliberate clause-level breaks should be allowed when they preserve meaning and improve source review.
The validator should use a positive list of acceptable break points, such as after semicolons, colons, or dashes and before top-level coordinating conjunctions.
Breaks outside deterministic prohibited patterns or the positive list should produce warnings rather than failures.

Generated and marker-owned content should keep its current source ownership.
When README marker content is generated from `VISION.md`, source-line corrections should happen in `VISION.md` or the synchronization mechanism rather than by hand-editing the generated projection.

The review procedure should require reviewers to inspect rendered output and physical source lines for changed review-critical Markdown, read the complete changed section rather than only a reported line, confirm phrase integrity, lifecycle readability, command copyability, current vocabulary, and generated-content ownership, then run prose validation.

Formatter configuration should prevent tools from reintroducing mechanical wrapping.
The spec should require disabling Markdown line-length enforcement such as `MD013` for covered files and configuring Prettier `proseWrap: "preserve"` repository-wide or at minimum for Tier A and Tier B paths through an overrides block or ignore file.

## Expected behavior changes

- README and VISION prose are no longer mechanically wrapped by default.
- Long source lines are allowed when they represent complete semantic units.
- Dense prose is rewritten structurally instead of reflowed mechanically.
- Deterministic source-line defects fail before PR handoff for Tier A.
- Ambiguous cases receive reviewable warnings.
- Canonical source and generated marker ownership remain intact.
- Skill and explain-change prose receive audit feedback without immediate broad enforcement.
- Historical Markdown is not mass-reformatted.

## Architecture impact

| Surface | Impact |
| --- | --- |
| Documentation source-format spec | New or amended normative contract |
| Test spec | Boundary-matrix fixtures |
| README and VISION authoring guidance | Concise link or summary |
| Prose validator | New bounded non-mutating validator |
| README validation | Compose or select prose validation |
| Selected validation | Route changed covered files |
| Guide-system validation | No duplicate prose contract |
| Generated marker sync | Preserve existing ownership |
| Historical docs | No migration |

The prose validator should own semantic source-line checks.
Existing README, guide-system, skill, and marker validators should retain their current responsibilities and compose or select the prose validator rather than duplicate its rules.

Architecture is not expected unless implementation introduces a shared Markdown parsing subsystem or changes generated-content ownership.

## Testing and verification strategy

The test spec should cover these proof areas:

| Check ID | What is verified |
| --- | --- |
| `PROSE-001` | Mechanical mid-sentence wrapping fails in Tier A. |
| `PROSE-002` | Long complete source lines pass. |
| `PROSE-003` | Semantic sentence-per-line paragraphs pass. |
| `PROSE-004` | Dense lifecycle prose rewritten as a list passes. |
| `PROSE-005` | Fenced commands are excluded from prose checks. |
| `PROSE-006` | Tables are not treated as prose paragraphs. |
| `PROSE-007` | Generated marker ownership is preserved. |
| `PROSE-008` | README recurrence fixtures fail before correction and pass after joining or restructuring. |
| `PROSE-009` | `AI agents` and `proposal to spec` regression fixtures are protected. |
| `PROSE-010` | Tier B produces audit warnings without repository failure. |
| `PROSE-011` | Specs, plans, and historical evidence remain outside first-slice enforcement. |
| `PROSE-012` | The validator never rewrites files. |
| `PROSE-013` | Existing README vocabulary and marker validation still run. |
| `PROSE-014` | Source-review evidence covers the complete changed section. |
| `PROSE-015` | A Tier A file fails when a previously passing semantic line is later mechanically wrapped by an editor or tool. |

Boundary fixtures should include paired contrasts:

```text
same words, mechanically wrapped:
  fail

same meaning, rewritten into bullets:
  pass

command split as prose:
  fail

same command in a fenced code block:
  pass
```

Behavior preservation evidence should compare rendered README content, README marker ownership, VISION meaning, retired vocabulary checks, skill behavior, historical documentation non-migration, and source reviewability.

## Rollout and rollback

Rollout should start with baseline capture and fixture coverage while canonical enforcement remains disabled.
After the source-formatting spec is accepted, the implementation should clean only covered current README and VISION violations while preserving marker ownership and rendered meaning.
Audit-mode validation should then run across Tier A and Tier B to record false positives and refine fixtures.
Tier A enforcement should enable deterministic errors for README and VISION, with ambiguous cases and Tier B remaining warnings.
Closeout should record behavior preservation and decide whether evidence justifies later expansion to canonical skills or explain-change artifacts.

Rollback should revert policy, validator, selected canonical prose edits, and enforcement routing together.
Enforcement should be disabled before removing the validator.
Rollback should not restore mechanically wrapped prose solely to match an old line width and should not modify generated marker content directly.
Historical files should remain untouched.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Validator becomes a grammar checker | Limit it to physical source-line boundaries. |
| False positives from Markdown structure | Parse blocks before examining prose. |
| Long lines become difficult in editors | Allow editor soft wrap; do not alter source. |
| Different reviewers prefer different clause breaks | Fail only deterministic cases and warn on ambiguity. |
| Broad repository churn | Enforce only selected Tier A surfaces first. |
| Marker-generated content drifts | Fix canonical source or generator, never generated blocks by hand. |
| Existing formatters reintroduce hard wrapping | Document exclusions or disable prose reflow for covered files. |
| Guidance duplicates the spec | Keep one normative contract and link to it. |
| Audit warnings are ignored | Require disposition only when covered files change. |

## Open questions

1. Which artifact should own the short contributor-facing policy?

   Decision: the spec owns the full contract, `CONTRIBUTING.md` owns the concise contributor-facing summary and validation command, and `docs/workflows.md` may link to `CONTRIBUTING.md`.

2. Should Tier A enforce one sentence per line or one paragraph per line?

   Decision: one semantic unit per physical line when practical, without requiring one paragraph per line.

3. Should deliberate clause breaks be allowed?

   Decision: yes.
   Clause-level breaks remain review-owned unless a deterministic structural rule applies; the validator should treat positive-list break points as acceptable and other non-deterministic cases as warnings.

4. Should validation operate on whole files or only changed lines?

   Decision: clean the small Tier A baseline, then validate complete Tier A files; use changed-file audit for Tier B.

5. Should Prettier or markdownlint be configured?

   Decision: configure them only to prevent automatic prose reflow on covered files, not to enforce a max-line-length rule.
   Disable `MD013` for covered files and configure Prettier `proseWrap: "preserve"` repository-wide or at minimum for Tier A and Tier B paths.

6. Should the validator fail on every suspicious break?

   Decision: no; fail deterministic patterns and report ambiguous cases as warnings.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Route recurrence to an authoritative proposal. | The issue persisted after durable learn guidance already existed. | Add another learn-topic entry only. |
| 2026-06-24 | Preserve semantic units rather than enforce width. | Source reviewability depends on meaning, not column count. | Add an 80- or 100-character Markdown limit. |
| 2026-06-24 | Start enforcement with README and VISION. | These are high-value, bounded, adopter-facing surfaces with direct recurrence evidence. | Enforce across all Markdown immediately. |
| 2026-06-24 | Use warnings for ambiguous clause boundaries. | Automated prose semantics are imperfect. | Fail every multiline prose paragraph. |
| 2026-06-24 | Keep validation non-mutating. | Automatic reflow can alter meaning and create noisy diffs. | Autoformat prose. |
| 2026-06-24 | Put the short contributor policy in `CONTRIBUTING.md`. | GitHub surfaces it during pull request creation, when source-form review guidance is most useful. | Put the full policy or primary summary only in `docs/workflows.md`. |
| 2026-06-24 | Add explicit formatter guardrails. | Markdown line-length linting and prose wrapping can reintroduce the exact defect. | Leave formatter behavior implicit. |
| 2026-06-24 | Add editor-tool wrap regression coverage. | The validator should prove that a previously passing Tier A semantic line fails after mechanical rewrap. | Rely only on static bad-example fixtures. |

## Next artifacts

```text
spec-review
architecture assessment
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

Architecture is not expected unless implementation introduces a shared Markdown parsing subsystem or changes generated-content ownership.

Potential later proposals include expanding enforcement to canonical skill prose, expanding enforcement to `explain-change.md`, formatter configuration for covered files, and editor recommendations for soft wrapping without source changes.

## Follow-on artifacts

- Proposal review: [proposal-review-r1](../changes/2026-06-24-semantic-source-line-contract/reviews/proposal-review-r1.md)
- Spec: [documentation source formatting](../../specs/documentation-source-formatting.md)

## Readiness

Accepted.
Downstream authoring is continuing under the workflow-managed `authoring-through-plan-review` profile.

## Core invariant

```text
Markdown source should break where meaning breaks, not where a column counter reaches a threshold.

A long complete sentence may be correct.
A mechanically split sentence is not made correct by rendering it as one paragraph.

Use structure when prose becomes dense, validate only bounded high-value surfaces first, and never auto-rewrite meaning-bearing prose.
```
