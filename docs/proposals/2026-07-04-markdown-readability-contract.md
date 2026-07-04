# Proposal: Markdown Readability Contract for Generated RigorLoop Documents

## Status

accepted

Accepted after clean `proposal-review-r2`.

## Problem

RigorLoop depends on generated and semi-generated Markdown artifacts for workflow state, review evidence, and contributor handoff.
Those artifacts must work for two audiences:

```text
1. Human readers of rendered Markdown.
2. Human reviewers of source diffs.
```

The repository has seen repeated readability failures where Markdown rendered acceptably but became harder to review in source.
README and `VISION.md` prose split meaningful phrases such as `AI agents`, `proposal to spec`, and `reviewable in Git` across arbitrary physical lines.
A later README recurrence showed that moving a command into a fenced block did not fix mechanically wrapped surrounding prose.
The real issue was source-line semantics, not rendered Markdown.

Current validation can pass while source prose remains mechanically wrapped because existing checks primarily validate syntax, lifecycle contracts, closed vocabularies, generated output, or whitespace.
Recent test-spec proof-contract work also showed that broad section shape is not enough when commands, milestone proof, and evidence ownership are not structurally explicit.

The root problem is:

```text
Generated Markdown currently optimizes for artifact existence and broad section shape more consistently than for source readability, skimability, evidence locality, and reviewer usability.
```

## Goals

- Define a project-wide readability contract for generated and generator-shaped Markdown.
- Preserve semantic source lines for review-critical prose.
- Reject fixed-width prose wrapping as the default readability rule.
- Use stable skeletons and repeated assets for substantial generated artifact types.
- Make lifecycle and review artifacts skim-first with concise status or result blocks.
- Prefer IDs, tables, ledgers, and proof contracts for mappings and evidence.
- Make proof-bearing commands copyable and explicitly owned.
- Mark generated regions with source-owner rules.
- Add deterministic validation for high-confidence readability failures.
- Keep ambiguous prose clarity review-owned rather than over-automated.
- Avoid broad historical reflow or mass migration.

## Non-goals

- Do not impose a universal 80-, 88-, 100-, or 120-character line limit.
- Do not reflow all existing Markdown.
- Do not make every Markdown paragraph a single physical line.
- Do not auto-format meaning-bearing prose.
- Do not replace human review for prose clarity.
- Do not change artifact schemas unrelated to readability.
- Do not hand-edit generated or marker-owned regions.
- Do not make learn topics the authoritative formatting policy.
- Do not require every artifact to use every possible section.
- Do not add or enforce manual-proof contracts in this proposal.
- Do not add a heavy Markdown AST framework unless bounded validators prove insufficient.
- Do not make readability validation block historical files in the first slice.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted work traceable, resumable, and reviewable in Git.
Markdown readability is part of that contract.
If generated documents are hard to skim, hard to diff, or structurally inconsistent, humans and agents spend more effort reconstructing workflow state.

This proposal improves reviewability without weakening lifecycle proof.
It is falsified if generated docs become longer but not clearer, a formatter splits semantic units by width, validation creates many false positives, generated regions are hand-edited instead of regenerated, reviewers still cannot quickly identify status and evidence, or historical Markdown is mass-reflowed without a migration decision.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize generated Markdown for rendered readability and source-diff reviewability. | in scope | Problem, Goals, Recommended Direction |
| Use semantic source lines instead of short lines everywhere. | in scope | Goals, Recommended Direction, Decision Log |
| Use structure for dense prose and workflow chains. | in scope | Goals, Recommended Direction, Expected Behavior Changes |
| Give generated documents stable skeletons. | in scope | Goals, Scope Budget, Architecture Impact |
| Separate prose, tables, code, generated regions, reviews, specs, and learn sessions by readability rule. | in scope | Recommended Direction, Expected Behavior Changes |
| Make documents skim-first with result or status blocks. | in scope | Goals, Recommended Direction |
| Prefer stable IDs over prose references. | in scope | Goals, Recommended Direction |
| Keep evidence close to claims. | in scope | Goals, Recommended Direction |
| Distinguish observed, planned, inferred, unknown, blocked, required, and deferred states. | in scope | Expected Behavior Changes |
| Keep long-form artifacts bounded. | in scope | Recommended Direction, Risks and Mitigations |
| Validate deterministic readability problems while leaving ambiguous prose to review. | in scope | Testing and Verification Strategy |
| Avoid broad historical reflow or mass migration. | in scope | Non-goals, Rollout and Rollback |
| Use a dedicated readability validator as the owner script composed by other validators where needed. | in scope | Recommended Direction, Testing and Verification Strategy, Decision Log |
| Enforce README and `VISION.md` semantic source-line checks immediately for changed sections only. | in scope | Architecture Impact, Testing and Verification Strategy, Decision Log |
| Exclude manual-proof contracts from this proposal. | in scope | Non-goals, Scope Budget, Testing and Verification Strategy, Decision Log |
| Use canonical generated-region markers with `surface`, `source`, and optional `generator` metadata. | in scope | Recommended Direction, Testing and Verification Strategy, Decision Log |
| Encourage diagrams when they reduce cognitive load but never require them. | in scope | Recommended Direction, Risks and Mitigations, Decision Log |
| Keep long-line and dense-paragraph warnings audit-only unless narrow fixture-backed checks mature. | in scope | Testing and Verification Strategy, Decision Log |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Markdown readability contract | core to this proposal | This proposal establishes the decision direction and boundaries. |
| Semantic source-line guidance | core to this proposal | Repeated README and `VISION.md` issues show arbitrary hard wrapping is the recurring failure. |
| Artifact-class readability rules | core to this proposal | Generated Markdown classes need different rules for prose, tables, commands, generated regions, reviews, specs, learn sessions, and release evidence. |
| Status and result block conventions | first-slice candidate | Lifecycle and review artifacts benefit immediately from skim-first metadata, but exact fields should be settled in the downstream spec. |
| Skeleton and repeated-asset alignment | same-slice dependency | Skills should generate the structures reviewers enforce. |
| Command ledger and proof-bearing command ownership | same-slice dependency | Proof-bearing commands need IDs, owners, failure behavior, and evidence paths. |
| Manual-proof contracts | out of scope | The owner decision is to exclude manual-proof contracts from this readability proposal. |
| Generated-region marker ownership | first-slice candidate | Source-owner markers reduce hidden manual-maintenance risk; exact marker syntax and enforcement need specification. |
| Deterministic readability validator | same-slice dependency | Validation is needed for known hard-wrap, placeholder, marker, table, command, and proof-structure failures. |
| Audit-only prose warnings | deferable follow-up | Ambiguous readability can start as review guidance or warnings before blocking validation. |
| Representative generated-doc cold read | same-slice dependency | The proposal's value depends on reviewers finding status, blockers, commands, evidence, and next action quickly. |
| Historical Markdown migration | out of scope | Broad reflow would create noisy diffs and should require a separate migration decision. |
| Formatter or markdownlint max-line-length policy | rejected option | Fixed-width prose wrapping recreates the known failure mode. |

## Context

Learn sessions already record the recurring issue:

- `docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md` identifies source readability as the problem and recommends semantic line breaks for adopter-facing prose.
- `docs/learn/sessions/2026-06-23-semantic-markdown-line-breaks.md` records that long semantic source lines can be correct and that arbitrary hard wrapping can make review text less natural.
- `docs/learn/sessions/2026-06-24-readme-prose-hard-wrap-recurrence.md` records a recurrence where the first fix addressed a command line but missed mechanically wrapped prose.

Those learn sessions deliberately did not create authoritative workflow, spec, validator, or skill policy.
This proposal is the route for turning the repeated lesson into an approved contract.

The related `docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md` shows the same pattern in a narrower artifact class:
authors should start from the same command-ledger and proof-map structure that reviewers enforce.
This proposal generalizes that readability and proof-structure principle across generated RigorLoop Markdown.

## Options Considered

### Option 1: Rely on human review only

Pros:

- Flexible.
- Avoids false-positive validator risk.
- Requires no new scripts, skeletons, or fixtures.

Cons:

- The same hard-wrap and proof-structure issues have recurred.
- Reviewers spend time finding avoidable source-format and structure problems.
- Learn sessions remain historical context instead of live authoring policy.

Rejected as insufficient.

### Option 2: Add a fixed Markdown line-length rule

Pros:

- Easy to understand.
- Easy to enforce with existing lint patterns.

Cons:

- Recreates the hard-wrap problem.
- Penalizes correct long semantic lines.
- Misclassifies tables, commands, URLs, generated markers, and lifecycle chains.

Rejected.

### Option 3: Auto-format all Markdown

Pros:

- Produces mechanically consistent output.
- Reduces some whitespace variance.

Cons:

- Can change meaning-bearing prose.
- Can hand-edit generated projections.
- Can create noisy diffs.
- Does not understand RigorLoop proof structures or artifact ownership.

Rejected for the first slice.

### Option 4: Define a readability contract, skeletons, and bounded validation

Pros:

- Addresses both source review and rendered readability.
- Keeps rules artifact-aware.
- Avoids broad historical churn.
- Makes generated docs easier to skim, diff, validate, and trust.
- Leaves ambiguous prose style to human review.

Cons:

- Requires coordinated skill, skeleton, validator, fixture, and representative-output updates.

Recommended.

## Recommended Direction

Choose Option 4: adopt a Markdown readability contract with four layers.

| Layer | Direction | Purpose |
| --- | --- | --- |
| Source-line readability | Use semantic line breaks for review-critical prose. | Preserve meaning in source diffs. |
| Structural readability | Use skeletons, status/result blocks, tables, and repeated-row assets. | Make generated documents predictable and skim-first. |
| Evidence readability | Use stable IDs, command ledgers, milestone maps, and direct evidence paths. | Keep proof claims auditable. |
| Validation | Fail deterministic structure and known readability defects; warn or route review judgment for ambiguous prose. | Prevent recurring defects without pretending style is fully mechanical. |

For human-facing generated prose, use these source-line rules:

```text
- one complete sentence per source line when practical;
- one natural clause per line for long sentences;
- one complete list item per bullet;
- one complete table row per row;
- one complete command per code line or fenced block;
- keep paired phrases together;
- avoid splitting lifecycle chains;
- use lists, tables, or diagrams instead of mid-sentence wrapping.
```

Every substantial generated artifact should have a skeleton or template asset.
Skeletons should define metadata, status or result shape, required sections, repeated blocks, placeholder removal, and handoff wording.
Skeletons should own output shape, while policy remains in the skill, spec, or workflow contract.

Lifecycle and review artifacts should start with a concise result or status block.
Review artifacts should identify skill, status, material findings, recording status, next stage, and stop condition when applicable.
Non-review generated documents should identify artifact status, scope, owner skill, last update, and related artifacts when applicable.

Use tables for requirement coverage, command ledgers, milestone proof maps, review findings, release surfaces, risk matrices, and decision logs.
Use stable IDs such as `R1`, `AC-001`, `T1`, `CMD1`, `M1`, review IDs, and finding IDs instead of vague references like "the command above" or "the second milestone."

Proof-bearing commands should be copyable and owned.
A command ledger should include command ID, command string, owner, when required, failure behavior, evidence artifact, and safe-mode boundary.

Generated regions should use source-owner markers and should not be hand-edited.
The canonical marker shape is:

```md
<!-- rigorloop:generated:start surface=<surface-id> source=<canonical-source> generator=<generator-id> -->
...
<!-- rigorloop:generated:end surface=<surface-id> -->
```

The downstream spec should define field validation details, path selection, parser behavior, and validator integration mechanics.
The `generator` field is optional only when no generator script exists yet.
The `surface` value should be stable and unique within the file, and start/end `surface` values should match.

Diagrams should be encouraged for workflow order, state transitions, artifact ownership, data flow, runtime flow, and boundary-heavy architecture when they reduce cognitive load.
Diagrams should not be required when a table or ordered list is clearer, and each diagram node should map to a real artifact, stage, component, actor, or state.

Historical docs should remain stable.
New generated documents and changed current documents should follow the contract.
Historical documents should be audit-only unless a migration is separately approved.

## Expected Behavior Changes

- Future generated Markdown preserves semantic source lines for review-critical prose.
- Future generated Markdown uses structure instead of dense paragraphs for chains, decisions, commands, mappings, and proof.
- High-value artifact classes use skeletons or required structures rather than depending on agent memory.
- Review and lifecycle artifacts expose status, blockers, evidence, and next action near the top.
- Proof-bearing commands become easier to copy and easier to audit.
- Generated regions are marked with source ownership so maintainers update canonical sources or generators.
- Validators catch deterministic readability failures while review still owns ambiguous prose clarity.
- Historical Markdown is not mass-reflowed by default.

## Architecture Impact

| Surface | Expected impact |
| --- | --- |
| `specs/` | Add a contract-level spec for generated Markdown readability, artifact classes, validation scope, and rollout boundaries. |
| `skills/` | Update affected stage skills so generated artifacts follow source-line, skeleton, status/result, ID, command, proof, and generated-region guidance. |
| Skill assets | Add or revise skeletons and repeated-row or repeated-block assets for high-value artifact classes. |
| `scripts/` | Add or extend repository-owned validation for deterministic readability and generated-region checks. |
| `templates/` | Add or update reusable scaffolds only when the artifact class is template-owned. |
| `docs/workflows.md` | Update workflow summary only if the downstream spec changes workflow-level guidance or artifact-location expectations. |
| README and `VISION.md` projections | Enforce changed-section semantic source-line checks without mass-reflowing historical text. |
| Generated adapter output | Regenerate or validate from canonical `skills/`; do not hand-edit generated public adapter bodies. |
| Historical documents | Audit-only in the first slice. |

Architecture or ADR work may be needed if the downstream spec introduces a shared generated-region ownership model, validator architecture, or cross-artifact generator boundary.

## Testing and Verification Strategy

Validation should start with deterministic checks:

| Check ID | What is verified |
| --- | --- |
| `MDREAD-001` | README and `VISION.md` hard-wrap regression fixtures fail. |
| `MDREAD-002` | Long complete semantic lines pass. |
| `MDREAD-003` | Code fences, tables, HTML blocks, and link reference definitions are excluded from prose-line checks. |
| `MDREAD-004` | Generated-region markers pair correctly. |
| `MDREAD-005` | Unfilled placeholders fail in generated documents. |
| `MDREAD-006` | Review records contain result blocks and finding IDs when required. |
| `MDREAD-007` | Test specs with named commands require a command ledger. |
| `MDREAD-008` | Manual-proof contracts are not enforced by this proposal. |
| `MDREAD-009` | Milestone-based test specs require milestone proof maps where the downstream spec requires them. |
| `MDREAD-010` | Commands are fenced or table-owned where command proof applies. |
| `MDREAD-011` | Historical docs are audit-only in the first slice. |
| `MDREAD-012` | Generated projections are not hand-edited when source-owner markers apply. |
| `MDREAD-013` | Representative generated docs pass a source-form cold read. |

Audit-only checks should report without failing on long source lines, possible semantic-line ambiguity, dense paragraphs, and prose chains that could become tables.
They should graduate to failures only when the check is narrow, deterministic, fixture-backed, and low-noise across tables, code fences, links, generated regions, and historical evidence.
Generic long-line checks should remain audit-only because long semantic source lines can be correct.

Repository-owned readability validation should be owned by a dedicated script:

```bash
python scripts/validate-markdown-readability.py
```

Existing guide, skill, artifact, or release validators should compose that owner script only for their relevant paths.
The downstream spec, test spec, and plan should define field validation details, path selection, parser behavior, and integration mechanics without moving policy ownership into those composed validators.

Representative generated-doc proof should include a source-form cold read where a reviewer can quickly find:

```text
status
blockers
commands
evidence
next stage
```

## Rollout and Rollback

Roll out the contract in slices while preserving one coherent external behavior.
Do not ship a half-updated state where skills require sections that skeletons lack, validators enforce fields that generators do not produce, generated docs contain markers without ownership rules, or readability rules exist only in learn topics.

Apply the first slice to new generated documents and changed current documents.
Keep historical documents audit-only unless a later migration proposal approves broader reflow.

Rollback should revert the contract spec, skill and skeleton changes, validator checks, fixtures, and generated-output proof together.
Because the first slice avoids historical migration and does not change runtime application behavior, rollback risk is mainly limited to authoring, validation, and generated-document surfaces.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Validator becomes a subjective prose judge | Fail only deterministic cases; keep ambiguous prose as warnings or review guidance. |
| Long-line fear returns | Explicitly reject fixed-width line limits and permit complete semantic source lines. |
| Generated docs become too verbose | Use tables, summaries, repeated blocks, and links to evidence instead of transcripts. |
| Skeletons become policy owners | Keep policy in skills, specs, or workflow guidance; skeletons own shape. |
| Historical files create noise | Audit history only in the first slice. |
| False positives in tables, code, links, or generated regions | Parse or recognize Markdown block types before prose checks. |
| Agents overuse diagrams | Require diagrams to reduce cognitive load and map nodes to real artifacts, stages, components, or actors. |
| Source and rendered readability conflict | Prefer structure such as bullets, tables, fenced commands, and diagrams over awkward prose. |
| Generated regions become hidden manual-maintenance surfaces | Add source-owner markers and validate marker pairing or projection consistency. |
| Public skill output drifts from canonical authored skills | Regenerate or validate from `skills/` and avoid hand-edited adapter bodies. |

## Open Questions

None.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-04 | Propose optimizing Markdown for both source and rendered readability. | RigorLoop artifacts are reviewed in Git and rendered form. | Render-only readability. |
| 2026-07-04 | Reject fixed-width prose wrapping. | Hard wrapping caused repeated README and `VISION.md` readability defects. | 80-, 88-, 100-, or 120-character Markdown limits. |
| 2026-07-04 | Prefer semantic source lines for prose. | Source lines should preserve complete sentences, natural clauses, list items, table rows, and commands. | Mechanical reflow by column width. |
| 2026-07-04 | Use skeletons and tables for generated artifacts. | Predictable structure improves scanning, validation, and reviewer handoff. | Free-form generated prose. |
| 2026-07-04 | Validate deterministic readability only in the first slice. | Prose clarity has subjective cases. | Full grammar or style checker. |
| 2026-07-04 | Avoid historical migration. | Broad reflow would create noise and risk. | Mass rewrite all Markdown. |
| 2026-07-04 | Use a dedicated Markdown readability validator script composed by existing validators where needed. | Readability cuts across artifact families and needs one policy owner. | Bury readability checks separately inside guide and skill validators. |
| 2026-07-04 | Enforce README and `VISION.md` semantic source-line checks immediately for changed sections only. | Recurrence evidence is strong, but historical reflow should stay out of scope. | Full-file README and `VISION.md` migration. |
| 2026-07-04 | Exclude manual-proof contracts from this proposal. | Owner decision is no manual-proof contracts in this readability change. | First-slice manual-proof enforcement. |
| 2026-07-04 | Use paired generated-region markers with `surface`, `source`, and optional `generator` metadata. | Stable source ownership is needed for generated regions to stay auditable. | Free-form `generated` comments. |
| 2026-07-04 | Encourage diagrams only when they reduce cognitive load. | Tables or lists are often clearer, and diagrams should map to real workflow or system nodes. | Require diagrams for workflow or state-machine topics. |
| 2026-07-04 | Keep long-line and dense-paragraph warnings audit-only unless narrow fixture-backed checks mature. | Long semantic lines can be correct, and subjective prose clarity should remain review-owned. | Generic long-line failure or subjective paragraph-density gate. |

## Next Artifacts

```text
proposal-review
spec: markdown readability contract for generated artifacts
spec-review
architecture or ADR if the spec introduces shared generated-region or validator architecture
plan
plan-review
test-spec
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on Artifacts

- Proposal review R1: `docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md`
- Proposal review R2: `docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md`

## Readiness

Accepted after clean `proposal-review-r2`; ready for `spec`.
