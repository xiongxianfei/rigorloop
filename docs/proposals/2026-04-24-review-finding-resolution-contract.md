# Review Finding Resolution Contract

## Status

- accepted

## Problem

RigorLoop already requires review feedback to be resolved, rejected, or deferred with rationale, and it already supports standalone `review-resolution.md` when durable review memory is needed.

The remaining gap is that a review finding can still be too incomplete to drive safe action. A finding may identify a concern without naming the supporting evidence, the required outcome, or a safe resolution path. That creates three downstream problems:

- implementers can guess at the intended fix;
- `review-resolution` can record a disposition without proving what was actually done;
- PR bodies can become overloaded with detailed finding text because the durable review artifacts are not consistently structured.

The workflow needs a clearer contract from review finding to resolution decision to verification proof to concise PR summary.

## Goals

- Make each material review finding actionable before it enters a fix or decision loop.
- Separate review suggestions from final resolution decisions.
- Make accepted fixes verifiable through explicit proof rather than chat memory.
- Keep PR bodies concise by summarizing review disposition counts and linking durable artifacts.
- Provide a predictable change-local layout for non-trivial changes that receive review feedback.
- Preserve the existing split between `review`, `review-resolution`, `verify`, `explain-change`, and `pr` ownership.

## Non-goals

- Replacing human reviewer judgment with a rigid form.
- Requiring a standalone resolution file for a clean review with no findings.
- Duplicating every review comment in the PR body.
- Replacing `explain-change.md` as the final concise rationale surface.
- Reopening the broader code-review independence or autoprogression decisions.
- Changing implementation behavior outside review artifact structure and stage guidance.
- Capturing maintainer PR review comments into `reviews/` in the current version.
- Automating semantic review-quality judgment in the first implementation slice.

## Context

- `CONSTITUTION.md` already says each material review item must be resolved, rejected, or deferred with rationale when review feedback exists.
- `specs/rigorloop-workflow.md` already defines `review-resolution` as enforced when review comments exist and requires each review item disposition to be recorded.
- The current workflow contract names `accepted`, `rejected`, and `deferred` as disposition values. This proposal intentionally expands that vocabulary with `partially-accepted` and `needs-decision`.
- `specs/rigorloop-workflow.md` currently allows review resolution to live in the PR body, `explain-change.md`, or standalone `review-resolution.md`, with standalone use required only for durable-memory triggers.
- `docs/workflows.md` says standalone `review-resolution.md` remains conditional and PR text remains the reviewer-facing summary surface.
- `skills/code-review/SKILL.md` already requires independent-review mode, evidence-backed findings, and first-pass review records.
- `skills/pr/SKILL.md` currently provides a broad PR body template but does not define a compact review-resolution summary section.
- Public adapter packages under `dist/adapters/` are generated from canonical skill guidance. Any canonical skill change used by public adapters must keep `.codex/skills/`, `dist/adapters/`, and `dist/adapters/manifest.yaml` in sync.
- Recent workflow use has shown a practical need to keep detailed suggestions in durable review artifacts while keeping PR text focused on the final review package.

## Options considered

### Option 1: Keep the current conditional review-resolution policy unchanged

- Advantages:
  - no new artifact shape to maintain
  - ordinary changes remain lightweight
  - existing workflow rules already require dispositions when feedback exists
- Disadvantages:
  - findings can remain under-specified
  - implementers may still infer fixes from incomplete review text
  - PR bodies can become the easiest place to store detailed review decisions
  - verification has no consistent way to prove accepted review fixes by item

### Option 2: Require a full review artifact pack for every non-trivial change

- Advantages:
  - maximum consistency
  - reviewers always know where to find review logs, resolutions, and final summary
  - easy to validate structurally
- Disadvantages:
  - too heavy for non-trivial changes with clean reviews
  - conflicts with the current proportional artifact policy
  - risks cargo-cult review files with no useful content

### Option 3: Require complete review findings and a standalone resolution chain when material findings exist

- Advantages:
  - addresses the real failure mode: incomplete findings and ambiguous fix ownership
  - keeps clean non-trivial changes lighter
  - makes PR bodies concise without losing traceability
  - aligns with the existing conditional artifact model while tightening the trigger
  - gives `verify` a concrete item-by-item proof surface for accepted fixes
- Disadvantages:
  - requires clearer finding IDs and disposition references
  - adds artifact work for review-heavy changes
  - needs updates across specs, stage skills, examples, and validation guidance

### Option 4: Keep detailed review and resolution entirely in the PR body

- Advantages:
  - familiar to GitHub-centric reviewers
  - fewer repository files
  - low tooling cost
- Disadvantages:
  - weakens durable change-local history
  - mixes suggestions, decisions, and final summary in one surface
  - makes later verification and explanation harder to audit from the repository alone

## Recommended direction

Choose Option 3.

RigorLoop should formalize a review finding completeness contract and a durable resolution chain for non-trivial changes that receive material review findings.

The proposed chain is:

- review record: finding plus suggested solution;
- `review-resolution.md`: final disposition decision plus final action;
- `verify`: proof that accepted fixes worked;
- `explain-change.md`: concise final summary of what changed and why;
- PR body: summary counts plus links, not duplicated finding detail.

A material review finding should be incomplete until it states:

- the evidence supporting the finding, such as a file reference, requirement, test gap, command output, or artifact inconsistency;
- the outcome required to satisfy the review gate;
- at least one safe way to resolve it, or a clear statement that a product, spec, architecture, scope, or maintainer decision is needed first.

The recommended change-local layout for non-trivial changes with review findings is:

```text
docs/changes/<change-id>/
|-- change.yaml
|-- review-log.md
|-- review-resolution.md
|-- explain-change.md
`-- reviews/
    |-- spec-review-r1.md
    |-- plan-review-r1.md
    `-- code-review-r1.md
```

`review-log.md` should act as a compact index of review rounds and outcomes. Individual files under `reviews/` should preserve the detailed review records. `review-resolution.md` should record the disposition and final action for each material finding. `explain-change.md` should summarize the final diff and refer to review resolution only at the level needed to understand why the final change looks the way it does.

If `reviews/` exists, `review-log.md` should be required even when there is only one detailed review record. That keeps the index rule simple and prevents single-review changes from becoming a special case.

PR bodies should include a compact section such as:

```md
## Review resolution summary
- Accepted 3 findings
- Rejected 1 finding with rationale
- Deferred 1 advisory follow-up
- Review-resolution: `docs/changes/<change-id>/review-resolution.md`
```

The PR body should not duplicate every finding, suggestion, and resolution detail when the durable artifacts already contain them.

The first implementation slice should include minimal structural validation only:

- if `reviews/` exists, `review-log.md` exists;
- every `reviews/*.md` file has a Review ID;
- every Review ID appears in `review-log.md`;
- every detailed review file has a stage, round, target, and status;
- finding IDs are unique within the change;
- findings referenced in `review-resolution.md` exist;
- `review-resolution.md` dispositions use approved values.

Approved disposition values should be:

- `accepted`;
- `rejected`;
- `deferred`;
- `partially-accepted`;
- `needs-decision`.

This expands the current workflow contract. Before `verify`, `explain-change`, or `pr`, every finding must have a final disposition.

Allowed final dispositions are:

- `accepted`;
- `rejected`;
- `deferred`;
- `partially-accepted`.

`needs-decision` is not a final disposition. It is an unresolved stop state and blocks `verify`, `explain-change`, and `pr` until resolved or explicitly deferred by an authorized owner.

`partially-accepted` is final only when the accepted part has an action and validation evidence, and the rejected or deferred part has rationale.

| Disposition | Meaning | Final for PR handoff? | Required record |
| --- | --- | --- | --- |
| `accepted` | The finding is valid and will be fixed in this change. | Yes, after fix and validation. | Chosen action plus validation evidence. |
| `rejected` | The finding will not be acted on because it is incorrect, out of scope, or already satisfied. | Yes. | Rationale. |
| `deferred` | The finding is valid or useful, but intentionally moved out of the current change. | Yes, only with rationale and follow-up owner or explicit no-follow-up reason. | Deferral reason plus follow-up. |
| `partially-accepted` | Part of the finding is accepted; part is rejected or deferred. | Yes, only after sub-decisions are recorded. | Accepted portion, rejected or deferred portion, rationale, and validation for accepted part. |
| `needs-decision` | A required owner decision is missing. | No. Blocks `verify`, `explain-change`, and `pr`. | Decision owner, decision needed, and owning stage. |

Semantic review-quality automation should be deferred. The validator should not try to decide whether the evidence is persuasive, whether the suggested solution is best, or whether the final action is substantively correct.

## Expected behavior changes

- Review records become more actionable because material findings include evidence, required outcome, and a safe resolution path or decision-needed rationale.
- Review-heavy non-trivial changes get a predictable durable artifact chain from finding to disposition to verification proof.
- Any change that creates `reviews/` also creates `review-log.md`, including one-review changes.
- `review-resolution.md` becomes the normal durable decision surface when material review findings exist, instead of relying on PR body detail for those decisions.
- `verify` checks accepted review fixes against recorded findings and resolution actions.
- `needs-decision` blocks `verify`, `explain-change`, and `pr` until an authorized owner resolves or explicitly defers the finding.
- `partially-accepted` can close a finding only when accepted and non-accepted portions each have the required record.
- `explain-change.md` remains concise and final-state oriented rather than becoming a review transcript.
- PR bodies summarize review resolution counts and link the durable resolution record.
- Repository-owned validation catches missing review IDs, missing log references, missing disposition links, duplicate finding IDs, and unsupported disposition values without judging review quality.
- Canonical skill changes keep `.codex/skills/` and generated public adapters synchronized.

## Architecture impact

This is a workflow-contract and artifact-shape change. It does not require a runtime service, new storage backend, or new generated adapter package layout.

Likely touched surfaces:

- `specs/rigorloop-workflow.md` for normative review finding completeness, resolution, verification, and PR-summary behavior.
- `docs/workflows.md` for concise contributor-facing guidance.
- `CONSTITUTION.md` and `AGENTS.md` if their review and change-local artifact summaries need alignment.
- `skills/code-review/SKILL.md` for finding completeness.
- `skills/workflow/SKILL.md` for stage routing and review-resolution loop language.
- `skills/verify/SKILL.md` for accepted-fix proof expectations.
- `skills/explain-change/SKILL.md` for concise final summary expectations.
- `skills/pr/SKILL.md` for the PR review-resolution summary section.
- `schemas/` or validation scripts for minimal structural validation of review IDs, review-log references, finding links, and disposition values.
- generated `.codex/skills/` output after canonical skills change.
- generated public adapter output after canonical skills change:
  - `dist/adapters/codex/`;
  - `dist/adapters/claude/`;
  - `dist/adapters/opencode/`;
  - `dist/adapters/manifest.yaml`.

The implementation must not update only `.codex/skills/` while leaving public adapter output stale.

## Testing and verification strategy

- Write a focused spec for the review finding resolution contract.
- Update the matching workflow or focused test spec so it covers:
  - incomplete findings without evidence;
  - incomplete findings without required outcome;
  - incomplete findings without safe resolution or decision-needed rationale;
  - accepted findings requiring final action and verification proof;
  - rejected and deferred findings requiring rationale;
  - `partially-accepted` and `needs-decision` dispositions using approved values;
  - `needs-decision` blocking `verify`, `explain-change`, and `pr` until resolved or explicitly deferred by an authorized owner;
  - `partially-accepted` requiring accepted-part action and validation plus rationale for the rejected or deferred part;
  - `reviews/` requiring `review-log.md` even when there is only one review record;
  - every detailed review file carrying Review ID, stage, round, target, and status;
  - review-log references covering every detailed Review ID;
  - finding IDs being unique within a change;
  - review-resolution references pointing only to existing finding IDs;
  - PR bodies using summary counts plus a link instead of duplicating detailed suggestions;
  - clean reviews not creating empty resolution boilerplate.
- Add repository-owned structural validation for review IDs, review-log references, finding ID uniqueness, review-resolution disposition links, and approved disposition values.
- Defer semantic review-quality automation.
- Run skill validation, generated skill drift checks, adapter generation drift checks, and adapter validation when canonical skill text changes.
- Run artifact lifecycle validation on the new proposal, follow-on spec, test spec, plan, and change-local artifacts.

## Rollout and rollback

Rollout:

- settle this proposal through `proposal-review`;
- write a focused spec and test spec;
- update workflow docs and affected stage skills;
- update examples or templates only where they teach the new artifact split;
- add minimal structural validation for review IDs, review-log references, finding references, and approved disposition values;
- regenerate generated Codex skill output and public adapter output if canonical skills change;
- validate `.codex/skills/`, `dist/adapters/codex/`, `dist/adapters/claude/`, `dist/adapters/opencode/`, and `dist/adapters/manifest.yaml` for sync;
- use the next review-heavy change to validate the artifact flow in practice.

Rollback:

- keep the existing workflow rule that review items need accepted, rejected, or deferred dispositions;
- revert only the stricter finding-completeness and artifact-layout guidance if it proves too heavy;
- preserve PR-body summary guidance if it improves review readability without blocking adoption.

## Risks and mitigations

- Risk: the artifact layout becomes universal boilerplate even for clean reviews.
  - Mitigation: scope the full layout to non-trivial changes with material review findings and keep clean-review handling lightweight.
- Risk: reviewers write formulaic findings that satisfy headings but not substance.
  - Mitigation: require concrete evidence, required outcome, and safe resolution content rather than just section names.
- Risk: `review-resolution.md` duplicates `explain-change.md`.
  - Mitigation: keep `review-resolution.md` focused on finding dispositions and final actions, while `explain-change.md` explains the final diff.
- Risk: PR bodies become too terse for reviewers.
  - Mitigation: include counts, disposition categories, and a direct link to the durable resolution artifact.
- Risk: implementation starts with overly strict validation before the writing contract is proven.
  - Mitigation: start with spec, skill, and template guidance; add machine validation only for fields that are stable and cheap to check.
- Risk: this conflicts with the current conditional standalone review-resolution policy.
  - Mitigation: frame the new policy as a narrower trigger: standalone resolution becomes expected when material review findings exist, while clean reviews still do not need empty resolution artifacts.
- Risk: structural validation is mistaken for semantic review assurance.
  - Mitigation: explicitly defer semantic review-quality automation and limit validation to stable links, IDs, required fields, and approved disposition values.
- Risk: `needs-decision` is treated as a final closeout state.
  - Mitigation: define it as an unresolved stop state that blocks `verify`, `explain-change`, and `pr` until resolved or explicitly deferred by an authorized owner.
- Risk: generated public adapters drift after canonical skill changes.
  - Mitigation: include `.codex/skills/`, all public adapter directories, and `dist/adapters/manifest.yaml` in generation and validation scope.

## Open questions

- None.

## Decision log

- 2026-04-24: Rejected leaving the current policy unchanged as the preferred direction. Reason: disposition requirements exist, but finding completeness and PR-summary boundaries remain under-specified.
- 2026-04-24: Rejected a universal full review pack for every non-trivial change. Reason: it would conflict with proportional artifact policy and create empty boilerplate for clean reviews.
- 2026-04-24: Chose a stricter finding-completeness and resolution chain for non-trivial changes with material review findings. Reason: it improves traceability where review feedback actually exists while preserving lightweight clean-review flow.
- 2026-04-24: Rejected storing detailed review resolution primarily in PR bodies. Reason: PR text is a summary surface, while durable repository artifacts should carry reusable review decisions.
- 2026-04-24: Decided that any change with `reviews/` must also have `review-log.md`, even for a single review record. Reason: a universal index rule is easier to apply and validate than a one-review exception.
- 2026-04-24: Deferred maintainer PR review comment capture from the current version. Reason: lifecycle review records are enough for the first slice, and PR comment ingestion would broaden scope.
- 2026-04-24: Chose minimal structural validation for review IDs, review-log references, finding references, and approved disposition values. Reason: stable structure is cheap to validate, while semantic review-quality automation should wait until the writing contract is proven.
- 2026-04-24: Expanded disposition vocabulary with `partially-accepted` and `needs-decision`. Reason: real review outcomes sometimes split a finding or require an owner decision before resolution.
- 2026-04-24: Classified `needs-decision` as an unresolved stop state rather than a final disposition. Reason: downstream stages cannot safely rely on unresolved review findings.
- 2026-04-24: Required generated public adapter sync when canonical adapter-shipped skills change. Reason: `.codex/skills/` is not the only generated consumer of canonical skill guidance.

## Next artifacts

- `proposal-review`
- focused spec for review finding resolution contract
- spec-review
- architecture only if the follow-up adds machine validation, schemas, or generated artifact behavior
- plan
- test-spec

## Follow-on artifacts

- `specs/review-finding-resolution-contract.md`
- `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
- `docs/plans/2026-04-25-review-finding-resolution-contract.md`
- `specs/review-finding-resolution-contract.test.md`

## Readiness

- Proposal-review approved this direction.
- The downstream spec and architecture are approved.
- The execution plan passed plan-review, and the test spec is active. The active plan and test spec now govern the execution lane.
- The main direction is settled: stricter finding completeness, required review-log when `reviews/` exists, expanded disposition vocabulary with final closeout rules, minimal structural validation, generated adapter sync, verification proof for accepted fixes, concise explain-change summary, and PR-body summary links.
