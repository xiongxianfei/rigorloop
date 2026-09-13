# Skill Contract: retained specialist obligations

Owning change: [change.json](../docs/changes/2026-09-08-skill-model-proposal-family-pilot/change.json).

## Current owner and retained boundary

[Skill](../docs/design/skill/skill.md) defines common published skill structure, metadata, invocation descriptions, role summaries, vocabulary presentation, readable procedure, portability, resource maps/integrity, output assets and truthful claims. Its [retained-contract table](../docs/design/skill/skill.md#common-contract-details-retained-by-consolidation) states actual requirements, populations and approved equivalents. Its [source-qualified displacement map](../docs/design/skill/skill.md#source-qualified-displacement-map) dispositions every selected numbered/unnumbered responsibility and acceptance intent. A generic preservation reference is not a replacement rule.

Transfer takes effect only with reviewed coherent implementation and successful Verify of the owning change. Before that boundary this is staged displacement, not partial adoption. After adoption the mapped common definitions here are superseded, not independently maintained. [Original bytes and related historical navigation](../docs/archive/skill-model/2026-09-08/README.md) remain directly readable. The readability, customer-portability and resource-integrity ADR originals retained at source paths are non-current history after this same adoption boundary.

This current source retains R37–R45's plan-specific asset structure, metadata/fingerprint and preservation obligations, and R56–R63's boundary-method obligations under their existing owners and later adopted amendments. Initial pilot scopes, budgets, old entrypoint inventories and completed rollout constraints remain historical, not a new adoption condition. The retained examples below explain those responsibilities in their original contract era. No retired skill or stored-record format becomes executable through this retention.

[Published-skill-first R26](published-skill-first-repository-simplification.md) supersedes R43d, R44a, R44e, R45 and R45a–d, R52/a/b, the installed-target-tree part of R55a and R59b as prospective runtime/corpus proof requirements, alongside the other clauses it explicitly names. Deterministic structure, resource, transformation and byte-parity protection remains with Skill and Gate A/B. Retained historical wording below does not reactivate a superseded proof requirement.

[Design](../docs/design/skill/authoring/design.md) owns model authoring; [Workflow](../docs/design/skill/workflow.md) owns coordination; [Review and Closeout](../docs/design/skill/assessment.md) owns assessment policy; [Validation](../docs/design/engineering/validation.md) owns shared test criteria; [Record Format](../docs/design/cli/records.md) and [CLI](../docs/design/cli/cli.md) own v2 representation/mechanics. Installation does not adopt project governance. Specialist proposal content and judgment remain at their existing owners. Operational manifests, templates and packaged methods keep their existing paths.

## Retained requirements

### Assets-first plan pilot (R37-R45)

R37. The assets-first plan pilot MUST be a follow-on packaged-resource pilot and MUST NOT change the current published-skill design pilot scope unless this spec is explicitly amended and approved.

R37a. Implementation MUST NOT begin while `plan` is part of another active or unresolved skill-contract change unless the active plan or change-local evidence records why the overlap is safe.

R37b. The assets-first plan pilot MUST modify `plan` as the only skill in its asset pilot implementation slice.

R37c. The assets-first plan pilot MUST NOT modify `proposal`, `proposal-review`, `spec`, `spec-review`, `code-review`, `verify`, or `pr`.

R37d. The assets-first plan pilot MUST NOT introduce packaged `references/`, packaged `scripts/`, build-time partials, adapter install-root changes, lockfile changes, or CLI behavior changes.

R38. The assets-first plan pilot MUST ship exactly these three normative assets under `skills/plan/assets/`:
- `plan-skeleton.md`;
- `milestone.md`;
- `decision-log-row.md`.

R38a. The assets-first plan pilot MUST NOT ship optional, example, deprecated, or fourth asset files unless this spec is amended.

R38b. The three normative assets MUST contain structural templates copied and filled by the agent, not paragraph-length workflow procedure, filled example narratives, hidden trigger logic, or policy text that belongs in `SKILL.md` or governing specs.

R38c. The three normative assets MUST NOT require repository-root internal paths as normal customer-project dependencies.

R39. `skills/plan/SKILL.md` MUST include a `Resource map` for the three normative assets.

R39a. Each assets-first plan pilot resource-map entry MUST use the literal verb `COPY`.

R39b. Each assets-first plan pilot resource-map entry MUST name the asset path, state the trigger condition, and name the fields or structures the agent must fill.

R39c. `COPY` is the only allowed verb for `assets/` in this pilot. `READ` is reserved for future `references/`, and `RUN` is reserved for future `scripts/`.

R39d. The `Resource map` MUST instruct the agent not to emit unfilled placeholders.

R40. `assets/plan-skeleton.md` MUST be the reviewed equivalent full output template for the `plan` artifact in the assets-first plan pilot.

R40a. `assets/plan-skeleton.md` MUST own canonical plan section order, headers, and placeholders.

R40b. `skills/plan/SKILL.md` MUST retain a compact output expectation summary that names the expected output shape and points to `assets/plan-skeleton.md` through the `Resource map`.

R40c. `skills/plan/SKILL.md` and `assets/plan-skeleton.md` MUST NOT duplicate the full plan section layout.

R41. The Current Handoff Summary in `assets/plan-skeleton.md` MUST contain only one stable pointer to the owning change record.

R41a. The Current Handoff Summary MUST NOT define lifecycle status values, next-stage transition rules, claim ownership, branch-ready semantics, PR-ready semantics, or validation requirements.

R41b. `skills/plan/SKILL.md` MUST retain the rule that mutable workflow and milestone state lives only in the owning change record.

R41c. The assets-first plan pilot MUST NOT ship a separate `assets/current-handoff-summary.md` file.

R41d. `skills/plan/SKILL.md` MUST instruct plan authors to write `docs/plan.md` and `docs/plan-archive.md` plan references as clickable Markdown links relative to the index file, such as `[Title](plans/YYYY-MM-DD-slug.md)`, instead of bare repository-root plan paths.

R42. Every assets-first plan pilot asset MUST include metadata comments for template name and version, skill name, template status, structural fingerprint, and maintained-alongside path.

R42a. Asset template status MUST use one of: `normative`, `optional`, `example`, `deprecated`.

R42b. The assets-first plan pilot assets MUST use `normative` status.

R42c. Static validation MUST recompute the structural fingerprint for each normative asset and fail when the recomputed fingerprint differs from the recorded fingerprint without a template-version update.

R42d. Static validation MUST compare the section set for normative assets against the section set referenced by `skills/plan/SKILL.md` resource-map and operating-procedure text when the asset is a full-artifact skeleton.

R42e. Drift MUST be resolved by reverting the structural change or bumping the template version and updating the recorded fingerprint.

R43. Assets-first plan pilot validation MUST be deterministic.

R43a. Static validation MAY check asset count, approved asset paths, required metadata comments, matching `Resource map` entries, literal `COPY`, fields-to-fill wording, visible placeholders, forbidden repository-root required paths, structural fingerprints, section-set parity, and generated adapter asset presence.

R43b. Static validation MUST NOT use broad semantic scoring to decide whether asset prose is too explanatory.

R43c. Prose-heavy asset review MUST use a bounded heuristic declared in the spec, test spec, or plan, or code-review judgment.

R43d. Behavior parity MUST be fixture-based or review-recorded and MUST NOT rely on an unbounded claim that the new plan is similar enough.

R44. The assets-first plan pilot MUST prove both no regression and demonstrated improvement.

R44a. The no-regression gate MUST include behavior-parity evidence showing that required plan sections, milestone shape, decision log shape, current handoff summary, validation evidence, implementation and review handoff, claim boundaries, and recording discipline are not weakened.

R44b. The demonstrated-improvement gate MUST show that `skills/plan/SKILL.md` common-path body token count decreases by at least 15 percent compared with the pre-pilot baseline.

R44c. Total packaged skill content, measured as `skills/plan/SKILL.md` plus assets, MAY grow by up to 5 percent with recorded rationale.

R44d. Total packaged skill content growth above 10 percent MUST block rollout unless this spec is amended.

R44e. The assets-first plan pilot MUST record supporting evidence that `assets/milestone.md` is used once per milestone across the behavior-parity reference corpus.

R45. The assets-first plan pilot behavior-parity corpus MUST separate contract-era reference plans from historical plans.

R45a. The reference corpus MUST include at least three contract-era, contract-compliant plans and MUST use strict structural parity.

R45b. The reference corpus SHOULD include `docs/plans/2026-05-18-skill-readability-self-containment.md`, `docs/plans/2026-05-19-published-skill-design-spec-family.md`, and `docs/plans/2026-05-19-published-skill-design-plan-family.md`.

R45c. The historical corpus MUST include 3 to 5 pre-contract-era plans and MUST use coverage parity, not strict structural parity.

R45d. Historical corpus gaps MUST be recorded in change-local evidence such as `docs/changes/<change-id>/historical-coverage.md`.

R45e. Follow-on packaged-resource proposals MUST choose resource patterns by skill type: constructive skills SHOULD treat `assets/` as the primary pattern for repeated structures, while deliberative skills SHOULD treat `references/` as the primary pattern for rule-heavy judgment guidance.

### Portable boundary-first capability (R56-R63)

R56. The portable boundary-first method MUST conform to `specs/boundary-first-proof-model.md`.

R56a. The governed published skills MUST be exactly `route`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `test-spec-review`, `implement`, `code-review`, and `verify`.

R57. Every governed skill MUST package and map `references/boundary-first-method-v1.md`.

R57a. Each resource-map entry MUST use the literal verb `READ`.

R57b. Each resource-map entry MUST state the stage-specific condition under which the method is loaded.

R57c. A governed skill MUST stop with a package-integrity blocker when the reference is required for the current invocation but is missing.

R58. All governed skill-local references MUST be deterministic projections of one declared canonical source.

R58a. Projected copies MUST NOT be hand-edited.

R58b. Projection metadata MUST identify the method version and canonical owner in a repository-maintainer surface that is not shipped as stage policy.

R59. The canonical source, governed skill-local projections, generated skill output, locally packed adapter output, and installed target skill trees MUST preserve the same skill-root-relative path and raw-byte SHA-256.

R59a. Byte drift or a missing governed projection MUST fail before adapter publication.

R59b. Clean-install proof MUST inspect Codex, Claude Code, and opencode target skill trees from locally packed release candidates.

R60. The shared reference MAY own only the closed dimension vocabulary, feature and proof record fields, identifier grammar, example classification, interaction-selection method, and portable worked examples.

R60a. Stage-specific stop conditions, formal review approval semantics, artifact placement, lifecycle routing, mutation authority, and readiness claims MUST remain in the governing skill or workflow contract.

R61. Published governed skills MUST describe the method with project-portable language and MUST NOT require the RigorLoop repository's canonical source, projection script, validators, adapter paths, or package internals in customer projects.

R62. Deterministic skill and package validation MUST check mapped-resource existence, allowed verb and class, containment, governed-skill coverage, projection identity, generated parity, packed parity, and installed parity.

R62a. Deterministic validation MUST NOT claim that the method was applied semantically or completely.

R63. Boundary-first activation MUST be atomic across all governed skills and supported adapter packages.

R63a. Existing accepted historical skill packages and feature artifacts remain valid according to the compatibility rules in `specs/boundary-first-proof-model.md`.

R63b. Package activation evidence MUST bind the canonical reference identity, all governed projections, generated output, locally packed output, installed target output, and the durable feature-spec grandfathering baseline.


## Retained contract-era examples

### Example E13: plan asset resource map copies templates

Given the assets-first plan pilot ships `assets/milestone.md` When `skills/plan/SKILL.md` includes a `Resource map` Then the resource map uses the literal verb `COPY` And it states when to copy `assets/milestone.md` And it names the fields the agent must fill.

### Example E14: plan skeleton owns section layout

Given `assets/plan-skeleton.md` is normative When `skills/plan/SKILL.md` describes expected output Then `SKILL.md` includes only a compact output expectation summary And `assets/plan-skeleton.md` owns canonical section order, headers, and placeholders And the full section layout is not duplicated in both files.

### Example E15: the plan skeleton carries only a stable handoff pointer

Given the assets-first plan pilot ships `assets/plan-skeleton.md` When an agent fills its Current Handoff Summary Then that section contains only the stable owning change-record pointer And lifecycle status values, transition rules, claim ownership, readiness semantics, and validation requirements remain in `change.yaml`, `SKILL.md`, or governing workflow artifacts.

### Example E16: historical plans are coverage evidence only

Given a historical plan was written before the published-skill design contract era When the assets-first plan pilot uses it as evidence Then strict structural parity is not required And gap analysis records whether the new `plan` skill can cover the same planning concerns.

### Example E23: governed skills share one packaged method

Given the boundary-first contract is active When a user installs any supported adapter Then each governed skill maps `references/boundary-first-method-v1.md` with `READ` And every mapped copy has the same raw bytes And each skill retains its own stage-specific stop, review, handoff, and claim rules outside the shared reference.
