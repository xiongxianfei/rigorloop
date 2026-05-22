# Change-Record Catalog Registration and Bounded Read Model

## Status

accepted

## Problem

RigorLoop's change-record mechanism has become stronger at writing evidence and storing validation metadata, but it still lacks two contracts that now matter repeatedly:

```text
1. A registration contract:
   what change-local evidence files may exist and how tooling routes them.

2. A read contract:
   how agents and tools answer common change-record questions without loading
   the whole change record.
```

Two recent learn sessions exposed the same root issue from opposite sides. The selector-routing session showed that useful new evidence files can block CI because the changed-path selector does not know how to route them. The reading-scope session showed that agents may read a large `change.yaml` to answer a narrow one-slice question because no bounded read/query model exists. Both symptoms point to the same missing mechanism: the change record is being treated like an append-only transcript rather than a queried catalog.

The first principle should be:

```text
A change record is a queried catalog, not a transcript.

Every evidence file it can contain should be registered so tooling can route it,
and every common question it answers should have a bounded read path so consumers
do not load the whole record to answer a slice question.
```

Recent work has repeatedly found the same pattern: a surface is correct in one dimension but lacks structural enforcement in the dimension that eventually fails. Here, compact metadata improved storage, and evidence files improved proof quality, but the mechanism still does not define how new evidence is routed or how common reads are bounded.

## Goals

- Treat the change record as a catalog with registered evidence classes and queryable slices.
- Define a registration contract for change-local evidence files.
- Define reusable filename patterns for recurring evidence classes, instead of one-off selector additions for every new file.
- Require deterministic changed-path selector routing for registered evidence classes.
- Surface `manual-routing-required` earlier than verify when deterministic in-repo evidence is added.
- Define a bounded read model for common change-record questions.
- Add or specify a query helper that reads only the metadata slice needed for a stage-owned question.
- Add stage-skill reading guidance so skills name which change-record slice they read and why.
- Preserve full forensic reconstructability when a full change record is genuinely needed.
- Keep immediate CI-maintenance fixes separate from the durable mechanism proposal.

## Non-goals

- Do not weaken changed-path selector safety.
- Do not make unregistered evidence files silently pass.
- Do not make `manual-routing-required` a permanent workaround for deterministic in-repo evidence.
- Do not require agents to read the whole `change.yaml` for stage-local questions.
- Do not replace authoritative state owners such as the active plan, review log, review resolution, or explain-change.
- Do not make `change.yaml` the default state oracle for questions better answered elsewhere.
- Do not remove existing validation, review, or lifecycle evidence.
- Do not bulk-migrate every historical change record in the first slice.
- Do not change the semantics of compact validation metadata unless required by the read/query contract.
- Do not change workflow stage order, review status meanings, milestone state values, or branch/PR readiness semantics.

## Vision fit

fits the current vision

RigorLoop's artifact-first workflow depends on durable records that are easy to inspect, validate, and maintain. A change record should help contributors find the right evidence quickly without relying on chat memory, broad reads, or selector guesswork.

This proposal is falsified if any of the following happens:

```text
- a deterministic change-local evidence file reaches verify with
  manual-routing-required;
- a new recurring evidence filename requires a one-off selector patch despite
  matching a registered evidence class;
- a stage still needs the whole change.yaml to answer a common stage-owned
  question;
- the query helper hides failures, blockers, or validation evidence;
- stage skills keep saying only "read change.yaml" without naming a bounded
  slice;
- full forensic reconstruction becomes harder when it is actually needed.
```

## Context

The uploaded analysis frames the two learn sessions as two halves of one missing contract. The selector session found an open write model meeting a closed routing model: contributors can create useful evidence files, but deterministic changed-path routing may not know them. The reading-scope session found that `change.yaml` does many jobs, but stages often need only one slice.

The same analysis recommends a unified proposal with two separated work items:

```text
registration contract:
  evidence classes, filename patterns, deterministic selector routes;

read contract:
  query helper, stage-by-stage read guidance, bounded metadata slices.
```

This should proceed through the lifecycle because it changes workflow and skill behavior. The learn session correctly diagnosed and routed the durable gap rather than unilaterally changing skills or workflow guidance.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Treat the two learn sessions as one underlying mechanism problem | in scope | Problem, Context |
| Add a registration contract for evidence files | in scope | Goals, Evidence registration contract |
| Prefer filename patterns for recurring evidence classes | in scope | Evidence class registry, Filename-pattern policy |
| Validate changed-path routing before verify | in scope | Selector-routing policy |
| Treat `manual-routing-required` as CI-maintenance debt | in scope | `manual-routing-required` policy |
| Add a read/query model for `change.yaml` and change records | in scope | Bounded read/query model |
| Read from the right state owner, not always `change.yaml` | in scope | Read contract |
| Add stage-skill reading guidance | in scope | Stage-skill reading guidance |
| Avoid legislating from a learn session | in scope | Rollout, Next artifacts |
| Current concrete selector blocker | deferred follow-up | Scope budget, Next artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Evidence class registry | core to this proposal | New evidence files need deterministic selector routes. |
| Filename-pattern routing | core to this proposal | Recurring evidence classes should not require one selector patch per exact filename. |
| Changed-path routing validation before verify | core to this proposal | Routing gaps should surface where files are introduced, not at branch readiness. |
| `manual-routing-required` handling | core to this proposal | Deterministic in-repo evidence should route or be explicitly unsupported before verify. |
| Change-record read contract | core to this proposal | Common questions need bounded read paths. |
| Query helper | separate implementation slice | Structural enforcement is stronger than relying on agent discipline, but it has different rollback and correctness risks than selector routing. |
| Stage-skill read guidance | separate implementation slice | Skills should name the slice they need after query-helper commands are stable. |
| Compact metadata schema changes | separate implementation slice | Include only if existing compact metadata cannot expose required query slices. |
| Current selector CI-maintenance blocker | separate implementation slice | Concrete blocker should be resolved directly in the active change, not wait for durable contract work. |
| Bulk migration of historical change records | separate proposal | Larger migration and compatibility risk. |

## Options Considered

### Option 1: Do nothing

Continue adding evidence files and reading `change.yaml` ad hoc.

Pros:

- No new contract or validator work.
- Existing workflows remain familiar.

Cons:

- New evidence files keep risking `manual-routing-required`.
- Verify remains the first changed-path routing check for some files.
- Agents continue broad-reading large change records for narrow questions.
- Repeated learn-session advice remains discipline-based, not mechanism-enforced.

### Option 2: Only add selector routes for the current blocker

Patch the currently failing evidence filenames.

Pros:

- Fastest way to unblock the active change.
- Low scope.

Cons:

- Fixes one instance, not the mechanism.
- Future evidence files can fail the same way.
- Does not address bounded reads.

This belongs as immediate CI-maintenance, not as the durable solution.

### Option 3: Only add a read/query helper

Build the bounded read model, but leave evidence registration unchanged.

Pros:

- Reduces unnecessary `change.yaml` reads.
- Improves stage-skill behavior.

Cons:

- New evidence files can still break changed-path routing.
- The write/routing side remains uncontracted.
- Only solves half the root cause.

### Option 4: Only add evidence registration

Create filename patterns and selector routing, but leave reads to agent discipline.

Pros:

- Reduces verify-stage selector failures.
- Makes change-local evidence classes more maintainable.

Cons:

- Agents still read the whole record for narrow questions.
- Stage skills remain vague about which fields to consult.
- The storage/read mismatch remains.

### Option 5: Unified change-record mechanism proposal with separated work items

Define both the registration contract and read contract, but execute them in separate workstreams and proof surfaces.

Pros:

- Solves the shared root cause.
- Keeps write-side selector risk and read-side skill behavior risk separated.
- Lets each half have its own falsifier and validation.
- Aligns with the catalog-not-transcript model.

Cons:

- Larger than either half alone.
- Requires careful staging so selector/CI changes and skill guidance changes do not blur.

## Recommended Direction

Choose Option 5.

Create a durable change-record mechanism contract with two explicitly separated workstreams:

```text
Workstream A: evidence registration and selector routing
Workstream B: bounded read/query model and stage-skill guidance
```

The two workstreams belong in one proposal because they govern the same mechanism: how change records are cataloged, routed, and queried. They should remain separate in spec, test-spec, plan, and implementation because the risks differ.

## Evidence registration contract

Create an evidence class registry for change-local files.

Each registered evidence class should define:

| Field | Meaning |
| --- | --- |
| Evidence class ID | Stable identifier such as `behavior-preservation`, `identity-proof`, `audit`, `baseline`, `token-cost`. |
| Filename pattern | Bounded glob or regex pattern. |
| Allowed directory | Usually `docs/changes/<change-id>/`. |
| Selector route | Deterministic changed-path route. |
| Required validator | Which validation command handles the file. |
| Lifecycle stage | When the file is expected or allowed. |
| Required when | Conditions that make the file mandatory. |
| Optional when | Conditions that make it allowed but not mandatory. |
| Forbidden when | Conditions where the file should not appear. |

Example registry entries:

```yaml
evidence_classes:
  audit:
    patterns:
      - "*-audit.md"
    selector_routes:
      - artifact.lifecycle
      - change.metadata
    validator: validate-artifact-lifecycle
    allowed_root: docs/changes/{change_id}/

  identity:
    patterns:
      - "*-identity.txt"
      - "*-commands-*.txt"
      - "*-tests-*.txt"
    selector_routes:
      - artifact.lifecycle
      - selector.regression
    validator: validate-artifact-lifecycle

  preservation:
    patterns:
      - "*-preservation.md"
      - "behavior-preservation.md"
    selector_routes:
      - artifact.lifecycle
      - review.artifacts
    validator: validate-artifact-lifecycle

  baseline:
    patterns:
      - "baseline.md"
      - "*-baseline.txt"
    selector_routes:
      - artifact.lifecycle
      - change.metadata
    validator: validate-artifact-lifecycle
```

The exact registry should be specified in the feature spec or selector spec.

## Filename-pattern policy

Prefer bounded filename patterns over one-off names for recurring evidence classes.

```text
Good:
  *-audit.md
  *-identity.txt
  *-preservation.md
  baseline.md
  token-cost.md

Less desirable:
  exact one-off filename for every new evidence artifact
```

Rules to evaluate in the spec:

```text
- Pattern registration is for recurring evidence classes.
- Exact filename registration is for genuinely novel classes.
- Broad catch-all patterns such as *.md under docs/changes/<id>/ are not allowed.
- A new deterministic evidence class should either match a registered pattern or
  add a registry entry in the same change.
```

## Selector-routing policy

Creating a new change-local evidence file is a two-part action:

```text
1. create the evidence file;
2. ensure changed-path selector routing recognizes it.
```

The file is not complete until both are true.

Selector routing should be validated against the actual changed-path set, not only explicit paths hand-picked by the milestone.

Required policy direction:

```text
- Implementation and code-review stages that add new evidence files should run
  changed-path selector routing over the change's actual changed paths before
  verify.
- Changed-set fixtures may supplement actual changed-path routing for selector
  unit tests, but should not substitute for routing the change's own changed
  paths.
- Explicit-path validation may supplement but should not replace actual
  changed-path routing when a new evidence class appears.
- Verify should not be the first stage to discover that a deterministic
  evidence file has no selector route.
```

## `manual-routing-required` policy

`manual-routing-required` is a valid diagnostic, not a durable workaround.

Rules to evaluate in the spec:

```text
- For deterministic in-repo evidence, manual-routing-required creates
  registration debt.
- Registration debt should be resolved before verify unless an owner records
  that the evidence class is intentionally unsupported.
- Milestone-local explicit-path validation may be used only as a temporary
  measure and should be recorded.
- The plan should track any unresolved manual-routing-required path as a
  blocker or CI-maintenance item.
```

## Bounded read/query model

`change.yaml` is a catalog, not the default source for every question.

Common questions should map to the smallest authoritative surface:

| Question | Authoritative source |
| --- | --- |
| Current live workflow state | Active plan `Current Handoff Summary` |
| Durable rationale | `explain-change.md` |
| Review finding status | `review-log.md` and `review-resolution.md` |
| Validation command/result inventory | `change.yaml` |
| Final validation state | `change.yaml.validation_summary` or compact equivalent |
| Forensic command detail | Validation events or transcript references |
| Owning artifact paths | `change.yaml` artifact/path index or query helper |
| Current active plan list | `docs/plan.md`, not historical change metadata |

The anti-pattern is using full `change.yaml` as the default first read for questions another artifact owns better.

## Query helper

Add or specify a repository-owned query helper.

Candidate command shape:

```bash
python scripts/query-change-record.py <change-id> summary
python scripts/query-change-record.py <change-id> artifacts
python scripts/query-change-record.py <change-id> review
python scripts/query-change-record.py <change-id> validation --latest
python scripts/query-change-record.py <change-id> validation --stage <stage>
python scripts/query-change-record.py <change-id> blockers
python scripts/query-change-record.py <change-id> forensic --stage <stage>
```

Candidate outputs:

```text
metadata summary:
  change id
  artifact paths
  current review status
  latest validation status
  open blockers
  detail pointers

metadata artifacts:
  canonical artifact paths only

metadata review:
  review records
  finding counts
  open finding IDs
  review-resolution status

metadata validation --latest:
  latest stage
  bundles
  result
  counts
  blockers
  transcript pointer if any

metadata validation --stage X:
  that stage's bundles/events/results only
```

The helper should make bounded reading easier than full-file reading.

## Common-read block ordering

For compact metadata, common-read fields should physically appear before historical detail.

Recommended top order:

```text
change identity
artifact paths
review state
latest validation summary
open blockers
detail pointers
validation events / history
```

Historical event detail remains available but is not the first-read surface.

## Stage-skill reading guidance

Stage skills should say which slice to read for which claim.

Examples:

```text
proposal-review:
  read proposal under review;
  read user intent;
  read review-log/review-resolution only when checking prior findings.

code-review:
  read changed files;
  read the reviewed milestone evidence;
  read review-resolution for the finding being checked;
  do not read all prior validation events unless reviewing validation history.

verify:
  read artifact paths, review closeout, validation_summary, and blockers;
  expand to validation events only when reconstructing command history or
  disputing evidence.

pr:
  read artifact paths, final validation summary, review counts, explain-change,
  and remaining blockers;
  do not broad-read every milestone event by default.
```

This turns bounded reads into part of the skill contract rather than optional advice.

## Full-read escalation rules

Full `change.yaml` or full change-record reads remain valid when needed.

Escalate to full read when:

```text
- reconstructing validation command history;
- investigating summary inconsistency;
- checking disputed evidence;
- debugging selector routing;
- validating migration between legacy and compact metadata;
- the query helper reports an ambiguous or unsupported shape;
- the whole change record is the review target.
```

Bounded reads are the default, not a hard prohibition.

## Expected Behavior Changes

- New evidence files are routed by registered class or pattern.
- Changed-path routing gaps surface earlier than verify.
- `manual-routing-required` for deterministic in-repo evidence becomes a tracked debt item, not a workaround.
- Stage skills consult bounded change-record slices rather than broad-reading full `change.yaml`.
- A query helper gives contributors a stable way to answer common change-record questions.
- Full forensic detail remains available when needed.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| Changed-path selector | Adds evidence-class registry or pattern routing. |
| Selector tests | Add fixtures for registered/unregistered evidence files. |
| `scripts/validate-change-metadata.py` | May expose or validate queryable slices, depending on implementation. |
| New query helper | Possible new `scripts/query-change-record.py` or equivalent. |
| Stage skills | Update guidance to name exact read slices. |
| Compact metadata spec | May need amendment if current schema lacks query-slice fields. |
| `docs/changes/<id>/` | Evidence files should match registered patterns or add registry entries. |
| `docs/workflows.md` or workflow spec | May document change-record catalog/read contract. |
| Generated adapters | Changed only if stage skill text changes; generated-output validation required if so. |

## Testing and Verification Strategy

This proposal likely requires a feature spec and focused test spec.

Recommended proof route:

```text
proposal-review
spec: change-record catalog registration and read model
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

A separate spec amendment may be needed for compact metadata if the existing compact shape cannot support query slices. A selector/test-spec amendment is likely required for evidence-class routing.

Implementation should not begin until the plan names one approved route:

```text
1. new feature spec plus focused test spec are sufficient;
2. feature spec plus compact-metadata/selector spec amendments are approved;
3. split into registration-only and read-model proposals if ownership boundaries
   are judged too different.
```

Recommended route:

```text
one proposal, one feature spec, two implementation workstreams.
```

The implementation workstreams should be sequenced rather than co-shipped:

```text
Slice 1: Workstream A, evidence registration and selector routing.
Slice 2: Workstream B, bounded read/query model and stage-skill guidance.
```

Likely checks:

| Check ID | What is verified |
| --- | --- |
| `CRM-001` | Evidence class registry exists and has bounded filename patterns. |
| `CRM-002` | Registered evidence file routes through changed-path selector. |
| `CRM-003` | Unregistered deterministic evidence file produces `manual-routing-required`. |
| `CRM-004` | `manual-routing-required` is tracked before verify for deterministic evidence. |
| `CRM-005` | Exact filename registration works for genuinely novel evidence classes. |
| `CRM-006` | Broad catch-all patterns are rejected. |
| `CRM-007` | Changed-path selector routing runs against the change's actual changed paths in implementation/code-review proof. |
| `CRM-008` | Query helper `summary` reads only the common-read slice. |
| `CRM-009` | Query helper `validation --latest` returns latest validation without full history. |
| `CRM-010` | Query helper `validation --stage X` returns only that stage's validation events. |
| `CRM-011` | Query helper `artifacts` returns canonical paths only. |
| `CRM-012` | Query helper escalates or errors on unsupported/ambiguous change-record shapes. |
| `CRM-013` | Stage skills name exact slices instead of saying only "read `change.yaml`." |
| `CRM-014` | Full-read escalation remains available for forensic tasks. |
| `CRM-015` | Legacy change metadata remains supported during migration. |
| `CRM-016` | Generated stage-skill adapters reflect skill guidance changes when skills are edited. |

Suggested validation commands:

```bash
python scripts/test-select-validation.py
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/changes/<change-id>/review-log.md \
  --path docs/changes/<change-id>/review-resolution.md
git diff --check --
```

If a query helper is added:

```bash
python scripts/query-change-record.py <change-id> summary
python scripts/query-change-record.py <change-id> artifacts
python scripts/query-change-record.py <change-id> validation --latest
python scripts/query-change-record.py <change-id> validation --stage <stage>
```

If selector routing changes:

```bash
bash scripts/ci.sh --mode explicit --path docs/changes/<change-id>/<new-evidence-file>
bash scripts/ci.sh --mode selected
```

Use the repository's actual changed-path selector command names in the test spec and plan.

## Behavior-preservation proof

Create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| Existing registered evidence routes | selector output before change | selector output after change | unchanged |
| New evidence pattern routing | `manual-routing-required` or absent route | registered deterministic route | improved |
| Validation command selection | selected checks list/hash | selected checks list/hash | unchanged except intended selector additions |
| Legacy `change.yaml` read | current validator/query behavior | post-change behavior | still supported |
| Query summary | full-file manual extraction | helper output | same answer, bounded read |
| Query validation latest | full validation history read | helper output | same latest result |
| Stage-skill read guidance | broad read wording | slice-specific wording | behavior narrowed without losing required evidence |

## Rollout and Rollback

Rollout:

1. Approve proposal.
2. Write feature spec covering registration and read contracts.
3. Write test spec with selector fixtures and query-helper fixtures.
4. Plan separate implementation workstreams for evidence registry and selector routing, changed-path routing validation and manual-routing debt handling, query helper / bounded read model, and stage-skill read guidance with generated adapter proof if skills change.
5. Implement Workstream A first so selector routing and registration debt are stable before read-model guidance depends on the catalog shape.
6. Code-review each workstream separately.
7. Verify changed-path routing no longer defers deterministic evidence gaps to verify.
8. Verify query helper answers common questions without full reads.
9. Explain change and prepare PR.

Rollback:

- Revert selector routing registry changes if changed-path classification regresses.
- Revert query helper without deleting evidence files.
- Revert skill guidance changes and rebuild generated adapters if needed.
- Preserve explicit routes added for currently blocking evidence classes if still correct and independently useful.
- Do not invalidate existing change records.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Registry patterns become too broad. | Forbid catch-all patterns and require evidence-class-specific tests. |
| New evidence files still fail at verify. | Run changed-path routing earlier and require registration debt tracking. |
| Query helper hides important failure history. | Full-read escalation remains required for forensic and disputed-evidence cases. |
| Skills over-narrow reads and miss context. | Add escalation conditions and require full read when the whole record is the review target. |
| `change.yaml` becomes under-specified for queries. | Amend compact metadata schema only where needed. |
| Selector routing and read model are too much in one implementation. | Separate workstreams and allow split if spec review finds ownership conflict. |
| Generated adapters drift after skill guidance changes. | Rebuild or validate generated adapters from canonical skills. |
| Existing evidence filenames become invalid. | Use legacy compatibility and transition rules; do not bulk-break current changes. |

## First-slice boundary

First implementation slice should include Workstream A only:

```text
evidence class registry for recurring change-local evidence files
selector routing for registered filename patterns
actual changed-path routing validation before verify
changed-set routing fixtures as supplemental selector tests
manual-routing-required debt handling
```

Out of scope for first slice:

```text
query helper for summary, artifacts, validation --latest, validation --stage
stage-skill guidance updates for the most affected stages
generated adapter proof for skill guidance changes
bulk migration of historical evidence filenames
full replacement of validate-change-metadata.py
new transcript schema
new workflow stage semantics
new review status meanings
automated evidence-file creation scaffolding
```

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-CRM-001` | Registered evidence classes have bounded filename patterns and deterministic selector routes. |
| `AC-CRM-002` | A newly added evidence file matching a registered pattern routes without `manual-routing-required`. |
| `AC-CRM-003` | A deterministic unregistered evidence file produces `manual-routing-required` and a stable diagnostic. |
| `AC-CRM-004` | `manual-routing-required` for deterministic in-repo evidence is tracked as registration debt before verify. |
| `AC-CRM-005` | Changed-path routing is validated against the change's actual changed paths before verify; changed-set fixtures may supplement but do not substitute for this proof. |
| `AC-CRM-006` | Query helper `summary` returns change ID, artifact paths, review state, latest validation state, blockers, and detail pointers without loading full validation history. |
| `AC-CRM-007` | Query helper `validation --latest` returns only the latest validation result, bundles, counts, blockers, and transcript pointer. |
| `AC-CRM-008` | Query helper `validation --stage <stage>` returns only the requested stage's validation evidence. |
| `AC-CRM-009` | Query helper `artifacts` returns canonical artifact paths only. |
| `AC-CRM-010` | Query helper supports legacy and compact metadata shapes, or reports a stable unsupported-shape diagnostic. |
| `AC-CRM-011` | Stage-skill guidance names exact change-record slices for stage-owned questions. |
| `AC-CRM-012` | Full change-record reads remain required for forensic reconstruction, disputed evidence, unsupported shapes, and whole-record review. |
| `AC-CRM-013` | Existing change records remain valid during migration. |
| `AC-CRM-014` | Generated adapter output reflects any changed skill guidance. |
| `AC-CRM-015` | No validation selection, review status, lifecycle state, or final readiness semantics change. |

## Open Questions

None. The proposal's initial open questions are resolved:

| Question | Resolution |
| --- | --- |
| Should the registration and read contracts live in one new spec, or amend existing selector and compact-metadata specs separately? | Use one feature spec with explicit dependency references, unless spec review finds ownership conflict. |
| Should the query helper be a new script or a subcommand of `validate-change-metadata.py`? | Add a new script, because query and validation have different purposes. |
| Should stage-skill guidance be updated in the same slice as the query helper or after the query helper exists? | Update only after query helper commands are stable, within Workstream B. |
| Should `manual-routing-required` be allowed at all for deterministic in-repo evidence after this proposal? | Allow it as a temporary diagnostic, but not at verify without owner-approved deferral. |
| Should filename patterns be centralized in one registry file? | Yes, if the selector architecture supports it; otherwise keep a table in the selector with fixture-backed tests. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-22 | Treat change record as a queried catalog, not a transcript. | Both selector routing and reading-scope failures come from missing catalog contracts. | Continue ad hoc file creation and broad reads. |
| 2026-05-22 | Bundle registration and read model in one proposal. | They govern the same change-record mechanism. | Two unrelated proposals. |
| 2026-05-22 | Separate registration and read model into workstreams. | Selector/CI risk and skill/read behavior risk differ. | One blurred implementation milestone. |
| 2026-05-22 | Prefer filename patterns for recurring evidence classes. | Avoids one-off selector churn for every useful evidence file. | Exact filename registration for all files. |
| 2026-05-22 | Add query helper rather than relying only on agent discipline. | Bounded reads should be the easy default. | Skills merely say "read less." |
| 2026-05-22 | Keep immediate selector blockers as CI-maintenance. | Current blockers should be fixed directly; durable behavior goes through proposal/spec. | Wait for this proposal before fixing current CI. |
| 2026-05-22 | Sequence Workstream A before Workstream B. | Selector/CI routing risk and read-helper/skill guidance risk need separate rollback surfaces. | Co-ship registration, query helper, and skill guidance in one first slice. |
| 2026-05-22 | Use one feature spec with explicit dependency references. | Registration and read contracts govern one mechanism, while dependency references preserve selector and compact-metadata ownership. | Separate selector and compact-metadata amendments as the default route. |
| 2026-05-22 | Add a new query helper script. | Querying and validation have different purposes and should not blur command semantics. | Make query behavior a subcommand of `validate-change-metadata.py`. |
| 2026-05-22 | Update stage-skill guidance only after query helper commands are stable within Workstream B. | Skill guidance should point to stable command surfaces. | Update skill guidance before the helper interface settles. |
| 2026-05-22 | Treat `manual-routing-required` as temporary diagnostic only. | Deterministic in-repo evidence needs a registered route or owner-approved deferral before verify. | Allow `manual-routing-required` as a durable verify-stage workaround. |
| 2026-05-22 | Prefer a centralized filename-pattern registry when selector architecture supports it. | A central registry is easier to validate and reason about; selector-backed tables remain acceptable when architecture requires them. | Require a registry file regardless of selector architecture. |

## Next Artifacts

```text
proposal-review
spec: change-record catalog registration and bounded read model
spec-review
test-spec
plan
plan-review
implementation workstreams
code-review
explain-change
verify
pr
```

Potential later proposals after this artifact is settled:

- Automated scaffolding of registered evidence files.
- Bulk migration of historical evidence filenames.
- Compact validation transcript query support if the first helper only exposes summaries.
- Shared evidence registry file if the first implementation embeds the registry in selector code.
- Broader workflow-skill read-model conventions beyond change records.

## Follow-on Artifacts

None yet

## Readiness

Proposal review approved with observations. Ready for `spec`.

## Core invariant

```text
A change record is a queried catalog, not a transcript.

Every deterministic change-local evidence file should have a registered selector
route when it is created, and every common stage-owned question should have a
bounded read path from the right state owner.

The mechanism should enforce good routing and good reading behavior instead of
relying on each agent or reviewer to remember the discipline.
```
