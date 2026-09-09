# AGENTS.md

## Skill ownership

For this repository's selected Skill-model initiative, [Skill](docs/design/skill/skill.md) owns the mapped common skill contract with its existing applicability; new procedure improvements apply only to `proposal` and `proposal-review`. The exact transfer takes effect through reviewed coherent implementation and successful Verify, not Design approval or package availability alone. [Skill Contract](specs/skill-contract.md) retains only its explicitly bounded plan/boundary-method authority. [Archive navigation](docs/archive/skill-model/2026-09-08/README.md) identifies historical originals and their replacements; source-retained old judgments do not govern new work after adoption. Specialist policy, distribution, installation and release retain their owners. Remaining adoption stays in named follow-ups, not an inventory-wide conformance claim.

## Design and System ownership

For this repository’s explicitly selected design-authoring and model-composition responsibility, [Design](docs/design/design/design.md) owns living model conventions, reconciled behavioral/technical authoring, decision preservation and validation mapping. [System](docs/design/system/system.md) owns the selected composition view and shared-owner relationships. The normal public author is `design`; `design-review` remains independent and selects the exact affected models, retained legacy contracts, examples and interactions. Workflow coordinates and consumes the mapping. Unmigrated responsibilities retain their declared owners and formats; installation does not adopt customer governance. The exact transfer is bounded by the models’ displacement maps and takes effect only with reviewed implementation and successful Verify. Historical IDs and approvals retain their original meaning.

## Test criteria ownership

For this repository's explicitly adopted model work, [Test](docs/design/test/test.md) owns shared derivation, protective-value and maintenance criteria (TEST-SR-01–13). Specialist reviewers and Verify judge actual plans, tests and evidence; Review and Closeout retains assessment authority policy, applicability and closeout consequences. Workflow retains coordination. Canonical consumers apply the criteria through selective quality and maintenance resources; those resources are application guidance, not another policy owner. This initiative's coordinated consumer adoption preserves historical contracts, required negative/regression proof and separately owned execution permissions. Installation does not adopt customer policy. Internal requirement mappings and package mechanics remain in contributor/governance surfaces rather than published skills.

This repository uses Codex to help maintain a public open source project.

Optimize for correctness, explicitness, small reviewable diffs, and alignment with the documented contract over speculative improvements.

Detailed governance lives in `CONSTITUTION.md`. `AGENTS.md` stays concise and points to the governing artifacts.

## Review and Closeout ownership

For explicitly adopted model work, [Review and Closeout](docs/design/review-closeout/review-closeout.md) owns shared assessment and final-closeout policy within Workflow (RC-SR-01–18). Workflow retains coordination; Record Format and CLI retain representation and mechanics. This change adopts that ownership for this repository's explicitly selected initiative; installation and distribution do not activate customer projects. The model's clause-level map identifies replacement ownership, while historical contracts and their stable IDs, judgments and stored procedures below retain their exact meaning. Specialized skills apply the owner through selectively packaged guidance; they do not define competing policy. Existing separately authorized release, PR, publication and destructive-action boundaries remain in force.

## Instruction precedence

When instructions conflict, follow this order:

1. Direct user request
2. `CONSTITUTION.md`
3. Approved owning Design for adopted responsibilities, or approved feature spec in `specs/` for unmigrated responsibilities
4. Approved architecture or ADR docs when relevant
5. Active execution plan file in `docs/plans/`
6. Matching test spec in `specs/`
7. This file

Do not silently blend conflicting higher-priority instructions. Call out the conflict, explain the impact, and follow the highest-priority source that already implies the answer.

## Repository defaults

- Prefer the smallest change that fully satisfies the request.
- Do not add unrelated refactors while implementing a scoped task.
- Preserve user changes unless explicitly asked to revert them.
- When behavior changes, update the relevant spec, test spec, docs, or examples in the same change when this repository uses them.
- Reuse existing scripts and workflows before inventing new commands or processes.
- Edit canonical workflow content in `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and `templates/`.
- Keep architecture and ADR scaffolds under `templates/`; do not place template-like files under `docs/architecture/` or `docs/adr/`.
- `skills/` is the only authored skill source.
- For public adapter installation, use `dist/adapters/README.md`; for `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`.
- Keep `.codex/skills/` untracked when copying installed Codex adapter skills there for local runtime use, and edit canonical skills under `skills/`.
- Do not hand-edit generated public adapter package output. `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface.
- Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window.
- Follow `docs/design/skill/skill.md` for the adopted common skill contract; `specs/skill-contract.md` retains its explicitly unmigrated plan/boundary obligations.
- Treat shipped skill text as user-facing. Keep repository-maintainer details about canonical source paths, generated mirrors, adapter paths, selector path constraints, drift checks, and shared-block implementation mechanics in contributor or governance surfaces, not in published skills.
- Do not create a new skill for one-off behavior; update an existing skill unless the new skill owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.
- `VISION.md` is the canonical project-vision artifact. Routine vision alignment is Proposal Review evidence, not a required proposal section. Material vision issues remain proposal-level decisions.
- README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`; README front-matter is not the source of truth when it conflicts with `VISION.md`.
- Validator closed-vocabulary checks must fail closed before consistency checks. For constants such as `*_OUTCOMES`, `*_FIELDS`, `*_KINDS`, and similar closed sets, unknown values must produce an explicit validation error unless the code documents why fall-through is intentional. The pattern `if value in CONSTANT: check_consistency(value)` is a defect when unknown values can pass silently. Every new closed-vocabulary validator constant should have an unknown-value regression test, preferably with `unknown_value` or `not_in_vocabulary` in the test name.
- Keep `AGENTS.md` practical. Keep workflow contracts in `specs/`, deterministic project-local workflow facts behind `rigorloop workflow-context`, and feature-specific detail in the matching spec.

## Planning and workflow

For explicitly adopted RigorLoop Record Format work, follow docs/design/cli/cli.md, docs/design/workflow/workflow.md and docs/design/record-format/record-format.md. Use primary status/context/show to read the exact record_contract and revision, subject inspect for the declared basis, and purpose-specific commands or batch for targeted recording. Only rigorloop-records-v2 is supported at runtime. Retired inputs reject safely; discovery excludes unrelated archival legacy records without running their validators and does not hide malformed current stores. Record-store is advanced inspection/replacement/recovery, not the normal skill path. Do not convert historical roots, reconstruct complete files routinely, or invoke historical eligibility before recording. Installation and model validation grant neither adoption nor workflow approval. Legacy work is owner-confirmed complete. Preserve historical record bytes and identities without migration, temporary continuation or a permanent legacy reader.

Use a plan first for work that is multi-file, risky, ambiguous, architecture-affecting, migration-heavy, or large enough that it should be split into reviewable milestones.

For the lifecycle contract, follow `specs/rigorloop-workflow.md`.

Use `rigorloop workflow-context` for deterministic project-local workflow information. Use the `route` skill for semantic routing decisions.

The `vision` skill is upstream of the per-change workflow, not a normal lifecycle stage. Use it at project genesis or when proposal review or learning surfaces a vision-level conflict.

`docs/project-map.md`, when present, is a living reference. Do not rely on it when it is absent, known-stale, contradicted, or missing the relied-on area unless you refresh it or record a no-map rationale.

Use Explore (`explore`) to expand a materially unclear decision space and Research (`research`) to reduce bounded decision-relevant uncertainty. Use both when Explore exposes factual questions that could change the option comparison, and neither when direction and relevant facts are sufficiently clear. Both are optional: an explicit invocation creates a standalone artifact under `docs/explorations/` or `docs/research/`, while a small incidental check does not. Neither approves or mutates the owning stage; Proposal, Design, Delivery, Implementation, Verify, or another named owner must adopt any conclusion that changes its decision. `learn` is periodic or explicitly invoked; after Frame it records a tracked session under `docs/learn/sessions/`, while pre-session trigger closeout may schedule a follow-up, defer capture, or record an explicit no-learn rationale in a tracked or review-visible surface.

Once proposal, spec, and architecture are already settled, execution usually proceeds through:

`plan -> delivery-review -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> verify`

After all implementation milestones and required corrections, require fresh independent whole-change Code Review of the complete final diff and cross-milestone interactions before distinct final Verify. Only successful Verify owns the final explanation and closeout assessment. PR is an optional external integration.

The consolidated pre-implementation gates are `proposal-review`, `design-review`, and `delivery-review`. Design Review approves the exact affected models, retained legacy contracts, examples and interactions as one package; Delivery Review approves the plan and its verification allocation. Earlier package shapes remain historical evidence, not current progression routes.

For milestone-based plans, repeat implementation and code-review for each in-scope implementation milestone. A clean non-final milestone review routes to the next implementation milestone; final closeout follows only after all in-scope implementation milestones are closed and required review-resolution is closed.

For planned initiatives, `docs/changes/<change-id>/change.json` owns the current milestone, milestone state, review status, remaining in-scope implementation milestones, next stage, and final closeout readiness. Plans carry stable execution intent, while stage-owned artifacts provide scoped evidence. Every state-changing handoff checks the change-local state and affected evidence before downstream readiness is claimed.

In workflow-managed completion flows, continue automatically into the next mandatory or triggered downstream stage when the approved autoprogression contract says to do so. Do not wait for redundant user confirmation to enter a known review or PR gate. Review-only and manual individual-skill invocations stay isolated by default, direct `pr` still opens the PR when readiness passes, and bugfix skill invocations remain explicit-step unless a higher-priority artifact broadens them.

Use `bugfix` for bugs, `ci-maintenance` when GitHub Actions or related automation for a material risk is missing, stale, or wrong, and `pr` only when the branch is already ready for review.

For an already-open PR, a user-authorized bounded CI repair may inspect the exact failure, make the smallest correction, run existing focused and PR checks, push under existing authority, and observe the replacement check. Preserve current review and verification evidence only when the correction restores approved behavior without changing their decision basis; otherwise return to the earliest affected owning stage.

## Plan file policy

- `docs/plan.md` is a navigation index to plan bodies and owning change records. It does not own active, blocked, milestone, review, or next-stage state.
- `docs/plan-archive.md` stores older historical plan references. Do not infer current lifecycle state from it.
- Concrete plan files under `docs/plans/` are the plan bodies that carry initiative detail.
- Plan bodies carry stable scope, milestones, dependencies, validation strategy, and recovery intent. They do not carry mutable lifecycle status, current milestone progress, blockers, or next-stage state.
- Every approved initiative gets its own living plan file under `docs/plans/YYYY-MM-DD-slug.md`.
- Never overwrite an older plan when starting a new initiative.
- If a new plan replaces an older one, preserve the older plan as historical intent and record replacement lifecycle state in the owning change record.
- Execution plans should use `skills/plan/assets/plan-skeleton.md`; do not maintain a second plan scaffold under documentation, templates, or local runtime output.

## Required reading before implementation

Before implementing behavior-changing work, follow the source-of-truth order from `CONSTITUTION.md`. In practice, read in this order when the files exist:

1. `CONSTITUTION.md`
2. the relevant feature spec in `specs/<feature>.md`
3. approved architecture or ADR docs when they are relevant to the change
4. `docs/plan.md`, then the active plan file in `docs/plans/`
5. the matching test spec in `specs/<feature>.test.md` only when independently applicable to the current approved contract
6. authoritative CLI workflow context when the task touches an existing governed flow or release process
7. the files you expect to modify

If the work changes externally observable behavior and no relevant spec exists, create or request the missing spec before coding the contract into the implementation.

## Spec and test conventions

- `specs/<feature>.md` defines the contract: requirements, examples, edge cases, non-goals, compatibility expectations, and acceptance criteria.
- A v2 plan maps requirements and edge cases to verification groups, concrete checks, and evidence expectations.
- Every `MUST` in a spec should map to planned verification.
- Historical v1 test specs remain subordinate to their feature specs.

## Artifact lifecycle defaults

- Mutable proposal, spec, test-spec, architecture, ADR, and plan lifecycle state lives in the owning `docs/changes/<change-id>/change.json`.
- Governed artifacts contain one stable pointer to their owning change record and keep stable intent, planning history, and explicitly historical evidence.
- Authoring skills may change only their own governed content and matching authoring-state transition. The sole narrow exception is that `plan` initializes missing v2 work entries exactly once from an approved Delivery Review package containing that primary plan; it never initializes an unreviewed draft or replaces or updates existing planned work. Review peers may change only their own review evidence and the matching package or artifact settlement transition.
- Route owns semantic routing and uses the stable workflow authority for lifecycle mutations. Downstream and support skills treat upstream governed artifacts and lifecycle state as read-only and route corrections to the owning stage.
- Keep `Next artifacts` as planning history while an artifact is active. Use `Follow-on artifacts` or `Closeout` for actual downstream artifacts or final disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- A superseded artifact's change-local state and owning closeout evidence must identify its replacement.
- `verify` blocks on stale touched, referenced, generated, or authoritative lifecycle-managed artifacts and warns on unrelated stale baseline debt.

## Implementation rules

- Keep diffs scoped.
- Write or update tests first when feasible.
- Run the smallest relevant verification scope first, then expand only as needed.
- If validation fails, stop and fix the failure before moving to the next milestone.
- During execution, `implement` writes implementation, tests, and stage-owned execution evidence. It does not update the plan body or artifact lifecycle and routing state.
- If a spec gap blocks safe implementation, state it explicitly instead of silently guessing.

## Verification expectations

- Until the repository-wide validation scripts are fully implemented, use the exact validation commands named in the active plan and any independently applicable test spec.
- When repo-owned validation scripts exist, run those named commands before PR instead of inventing substitute checks.
- For adapter package work, ordinary contributors do not need all supported tools installed locally; non-smoke validation is repository-owned through adapter generation, adapter validation, release metadata validation, and `scripts/release-verify.sh`.
- Release automation must use tracked release notes under `docs/releases/<tag>/release-notes.md`; do not rely on generated release notes for adapter compatibility claims.
- For planned initiatives, final lifecycle closeout updates change-local state and stage-owned evidence. Merge is not a routine trigger for later lifecycle closeout. `verify` treats mutable lifecycle or routing state in a governed artifact or plan as blocking PR readiness.
- Do not report success without naming the commands actually run.

## Change management

- Do not rewrite plan, spec, or workflow files unless the task requires it.
- Remove or challenge stale instructions when they no longer match reality.
- If a request conflicts with the current spec, ask whether the spec should change or the implementation should intentionally diverge only when the higher-priority sources do not already imply the answer.

## Definition of done

A task is not done unless all of the following are true:

- the implementation matches the current contract
- relevant verification was run, or any inability to run it is stated clearly
- named edge cases and failure paths are handled or explicitly deferred
- the user-visible scope does not silently exceed what was agreed
- the owning change record and stage-owned evidence reflect what actually happened when a plan was used
- meaningful assumptions and open questions are called out in the final response
