# Vision Skill

## Status

- accepted

## Problem

RigorLoop has a clear workflow contract, a public README, and a growing set of lifecycle skills, but it does not yet have a compact canonical vision document that answers what the project is, who it is for, what it refuses to become, and how future proposals should be checked for fit.

That leaves three recurring risks:

- users landing on the repository must infer the project direction from workflow details;
- contributors can propose work that is locally reasonable but misaligned with the project identity;
- project-scope decisions can drift into proposals, specs, architecture documents, or README prose without one short source of truth.

The repository also lacks a dedicated skill for safely creating or revising that vision. Without a skill, an agent may treat README positioning as ordinary documentation editing, overwrite durable authorial judgment, or make a vision-level change without preserving the causal link to the proposal, incident, or learning that triggered it.

## Goals

- Add a `vision` skill for creating and revising the project vision.
- Establish `vision.md` at the repository root as the canonical project vision.
- Establish the README front-matter between `<!-- vision:start -->` and `<!-- vision:end -->` as generated from `vision.md`.
- Keep the vision concise, plain-language, and user-facing.
- Make proposal review easier by giving proposals a stable project-fit reference.
- Distinguish vision work from proposals, specs, architecture, plans, and README maintenance.
- Support three modes: create, revise, and mirror.
- Protect an existing `vision.md` from unclear regeneration requests.
- Make `Vision fit` visible in future proposals when `vision.md` exists.
- Teach `proposal-review` to classify proposal-versus-vision conflicts.
- Keep substantive vision revisions traceable through change-local artifacts when a proposal, incident, or learning caused the revision.
- Refresh generated `.codex/skills/` and `dist/adapters/` output only through the existing generators when canonical skill guidance changes.

## Non-goals

- Adding the `vision` stage to the normal per-change workflow chain.
- Turning the vision into a requirements document, architecture document, roadmap, or marketing page.
- Replacing the README, workflow spec, constitution, proposal process, or architecture package.
- Adding feature lists, implementation details, stakeholder tables, priority columns, status fields, or decision logs to `vision.md`.
- Requiring every feature addition or README edit to revise the vision.
- Creating the initial `vision.md` as a side effect of adding the skill.
- Creating validator enforcement for vision content in the first slice.
- Adding a helper script for README front-matter mirroring in the first slice.
- Hand-editing generated `.codex/skills/` or `dist/adapters/` output.

## Context

`CONSTITUTION.md` defines RigorLoop as a Git-first starter kit for AI-assisted software delivery that optimizes for reviewability, traceability, and trustworthy automation. `README.md` currently explains that direction to users, but it is not generated from a canonical vision and does not use bounded vision markers.

The existing workflow already treats `proposal` as the default stage for choosing direction. A vision document would sit upstream of that lifecycle rather than inside the normal per-change chain. It gives proposal authors and reviewers a short, stable surface for project fit, while proposals and specs continue to own change-specific direction and requirements.

The source-of-truth boundary is important:

- `vision.md` should be canonical authored content at the repository root.
- `README.md` should contain a generated front-matter subset bounded by comments.
- `skills/vision/SKILL.md` should be the canonical authored skill source.
- `.codex/skills/vision/SKILL.md` and `dist/adapters/*` should remain generated output refreshed by the existing scripts.

The requested skill guidance is intentionally strict about length and voice: `vision.md` should stay under 500 words, use plain language, avoid requirements vocabulary, and state scope refusals plainly enough to guide future decisions.

There is no root `vision.md` in the repository yet. This proposal therefore creates the skill and routing contract first; the initial project vision should be authored later through an explicit `vision create` invocation after the skill itself is accepted.

## Options considered

### Option 1: Keep README as the only project-positioning surface

Advantages:

- no new artifact;
- users already read README first;
- no generated README front-matter boundary is needed.

Disadvantages:

- README must serve setup, usage, contribution, adapter, validation, and positioning needs at once;
- project-fit reasoning can drift across README sections;
- agents may edit public positioning directly without a canonical source;
- proposals have no short vision reference for scope fit.

### Option 2: Add `vision.md` without a skill

Advantages:

- creates a dedicated source of truth quickly;
- avoids adding another skill to the adapter packages;
- lets humans author the first version freely.

Disadvantages:

- no consistent create/revise/mirror workflow;
- no guardrail against overwriting existing vision content;
- no standard README marker regeneration behavior;
- no guidance for substantive versus editorial revisions;
- future agents may still treat the vision as ordinary docs prose.

### Option 3: Add a full `vision` skill with README mirroring

Advantages:

- creates a repeatable process for project genesis, substantive revisions, and README mirroring;
- makes `vision.md` canonical and README front-matter generated;
- gives proposal authors and reviewers a stable project-fit reference;
- preserves the distinction between vision, proposals, specs, architecture, and plans;
- protects existing vision content by requiring explicit revise or mirror mode;
- supports change-local traceability for substantive revisions.

Disadvantages:

- adds another skill to maintain and distribute;
- requires careful README marker introduction;
- may require workflow and proposal guidance updates so the skill is used at the right time and not as a routine stage;
- generated skill and adapter output must be refreshed and validated.

### Option 4: Add a full vision workflow stage

Advantages:

- makes project-fit checks highly visible;
- could require every proposal to cite or update the vision;
- creates strong lifecycle consistency.

Disadvantages:

- overfits ordinary changes;
- conflicts with the requested model that vision is upstream of the per-change workflow;
- risks turning a concise project identity document into a routine process artifact;
- increases workflow weight without proportional value.

## Recommended direction

Choose Option 3.

Add a `vision` skill that produces or updates the root `vision.md` and regenerates only the bounded README front-matter section. The skill should have three modes:

- `create`: no `vision.md` exists; create `vision.md` and insert or regenerate README front-matter.
- `revise`: `vision.md` exists and a named section needs substantive change; update only that section unless the change cascades, then regenerate README front-matter.
- `mirror`: `vision.md` exists and remains current; regenerate README front-matter only.

The skill should refuse unclear requests when `vision.md` already exists. It should ask for the intended mode rather than silently overwriting the document.

The first implementation should add:

- `skills/vision/SKILL.md`;
- generated `.codex/skills/vision/SKILL.md` via `scripts/build-skills.py`;
- generated adapter skill copies and manifest updates via `scripts/build-adapters.py`;
- README marker behavior in the skill contract;
- workflow and proposal guidance that says vision is upstream of the per-change lifecycle and referenced by proposals, not a normal stage in the chain;
- `skills/proposal/SKILL.md` guidance requiring a short `Vision fit` section when `vision.md` exists;
- `skills/proposal-review/SKILL.md` guidance requiring reviewers to check `Vision fit`.

The first implementation should not create the initial `vision.md`. Creating the project vision is a separate invocation of the accepted skill because the content is project-level authorial judgment, not a generated side effect of adding the skill. After the skill is accepted, run the `vision` skill in `create` mode to produce `vision.md` and the README front-matter, then review that artifact before treating it as current.

Future proposal guidance should say that if `vision.md` exists, every proposal includes a short `Vision fit` section using one of these values:

- `fits the current vision`;
- `may conflict with the current vision`;
- `intentionally proposes a vision revision`;
- `no vision exists yet`.

A proposal must not silently redefine project vision. If a proposal conflicts with `vision.md`, `proposal-review` should classify the outcome as one of:

- revise proposal;
- revise vision;
- record explicit exception.

The skill should keep the user-provided document rules: `vision.md` stays under 500 words, uses plain language, avoids requirements vocabulary, and includes plain headings for pitch, differentiator, audience, non-audience, commitments, refusals, falsifiability, and optional open questions. The README generated subset should include only the pitch, differentiator, audience, and a link back to `vision.md`.

README marker insertion is governed by the `vision` skill instructions in the first slice. A helper script is deferred until mirror drift or repeated README-front-matter edits show that deterministic automation is needed. The v1 contract is:

- the skill may edit only between `<!-- vision:start -->` and `<!-- vision:end -->`;
- content outside the markers remains author-owned;
- missing or malformed markers require explicit handling, not broad README rewrite.

## Vision fit

- no vision exists yet.

This proposal defines the mechanism that will make future project-fit checks explicit. Proposal-review should still check the scope risk that vision work could drift toward general project-management behavior; if reviewers decide that risk conflicts with current project positioning in `README.md` or `CONSTITUTION.md`, they should request a narrower proposal before spec work.

## Expected behavior changes

- Contributors can invoke `vision` to create a project vision at genesis, revise a specific vision section, or mirror the README front-matter from `vision.md`.
- `vision.md` becomes the canonical project-vision artifact at the repository root.
- README gains a bounded generated front-matter section that can be regenerated without touching the rest of the file.
- Future proposals can be reviewed against vision commitments and refusals.
- Future proposals include a visible `Vision fit` section when `vision.md` exists.
- Proposal review distinguishes revise-proposal, revise-vision, and explicit-exception outcomes for vision conflicts.
- Substantive vision revisions caused by a proposal, incident, or learning record their reason in the matching change-local pack.
- Editorial mirror-only updates can rely on version control history without a change-local record.

## Architecture impact

This change affects the skill and documentation surface, not the runtime architecture.

Expected touched surfaces:

- `skills/vision/SKILL.md` as the canonical authored skill;
- `.codex/skills/vision/SKILL.md` as generated local Codex output;
- `dist/adapters/*` generated adapter skill output and manifest entries;
- `README.md` marker conventions for generated vision front-matter;
- `docs/workflows.md` and `specs/rigorloop-workflow.md` only where needed to clarify that vision is upstream and not part of the per-change chain;
- `skills/proposal/SKILL.md` so proposals check against `vision.md`;
- `skills/proposal-review/SKILL.md` so proposal-review checks `Vision fit`.

No new service, data store, deployment boundary, or architecture package is expected.

## Testing and verification strategy

Verification should focus on skill validity, generated-output drift, README marker safety, and workflow wording consistency.

Likely proof commands:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/select-validation.py --mode explicit --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md
bash scripts/ci.sh --mode explicit --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md
```

The first slice should validate README marker behavior by review because marker insertion is governed by the skill instructions rather than a helper script. If a later implementation adds README marker logic to a script, add focused tests for:

- creating markers when absent;
- replacing only content between markers;
- refusing to edit README content outside the markers;
- mirroring from `vision.md` without changing the canonical vision.

## Rollout and rollback

Rollout:

- add the canonical `vision` skill under `skills/`;
- update workflow/proposal guidance only enough to route vision work correctly;
- generate `.codex/skills/` and `dist/adapters/` output through the existing generators;
- after the skill is accepted, invoke `vision create` separately to create the initial `vision.md` and README front-matter;
- review the initial `vision.md` before treating it as current.

Rollback:

- remove `skills/vision/` and regenerate `.codex/skills/` and `dist/adapters/`;
- remove or revert workflow/proposal references to the vision skill;
- if a later `vision create` invocation created `vision.md`, either keep it as an ordinary manually maintained document or remove it in the same rollback change;
- restore README front-matter to the previous hand-authored form if the generated section is rolled back.

## Risks and mitigations

- Risk: the vision becomes another heavy workflow artifact.
  - Mitigation: keep it under 500 words, status-free, and outside the normal per-change chain.

- Risk: agents overwrite project identity prose too casually.
  - Mitigation: require explicit create, revise, or mirror mode and refuse unclear regeneration when `vision.md` exists.

- Risk: README generated front-matter conflicts with hand-authored README content.
  - Mitigation: use `<!-- vision:start -->` and `<!-- vision:end -->` markers and edit only inside them.

- Risk: proposals treat the vision as a requirements spec.
  - Mitigation: proposal guidance should use the vision for fit checks while keeping requirements in specs.

- Risk: adding vision fit checks moves RigorLoop toward general project management.
  - Mitigation: keep the vision skill upstream, narrow, status-free, and limited to project identity rather than task tracking or portfolio management.

- Risk: generated skill or adapter output drifts from canonical `skills/vision/SKILL.md`.
  - Mitigation: refresh through existing generators and validate generated output with the current skill and adapter checks.

## Open questions

- None.

## Decision log

- 2026-04-29: Drafted proposal to add a dedicated `vision` skill rather than treating vision as ordinary README editing.
- 2026-04-29: Recommended `vision.md` as canonical and README front-matter as generated from it.
- 2026-04-29: Rejected adding vision as a normal workflow stage because the requested model places it upstream of the per-change chain.
- 2026-04-29: Decided the first implementation will not create the initial `vision.md`; initial vision authoring is a separate `vision create` invocation after the skill is accepted.
- 2026-04-29: Decided future proposals should include `Vision fit` when `vision.md` exists, and proposal-review should classify conflicts as revise proposal, revise vision, or explicit exception.
- 2026-04-29: Deferred README mirror helper automation until repeated marker drift shows it is needed.

## Next artifacts

- `proposal-review`
- focused spec for the `vision` skill contract
- test spec covering skill validation, generated-output refresh, README marker behavior, and workflow wording
- execution plan if the accepted spec spans multiple surfaces

## Follow-on artifacts

- [Vision Skill spec](../../specs/vision-skill.md)

## Readiness

This proposal is accepted. The focused spec is the current downstream contract surface for the `vision` skill, README front-matter ownership, and generated-output refresh expectations.
