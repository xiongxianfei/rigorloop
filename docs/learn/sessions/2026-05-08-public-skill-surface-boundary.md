# Learn Session: Public Skill Surface Boundary

## Frame

- Date: 2026-05-08
- Status: session-recorded-follow-up-recommended
- Trigger: contributor observed that repository skills are used by end users, so skill files are a published interface and should not expose repository development details.
- Trigger type: explicit contributor observation.
- Scope: boundary between public skill guidance and repository-internal contributor, generation, validation, and routing details.
- Session path: `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`

## Evidence Reviewed

- Contributor examples from the invoked `learn` skill:
  - `For full routing rules, follow specs/rigorloop-workflow.md`.
  - `Generated-output handling` section naming canonical skill source, generated mirrors, adapter paths, selector validation, drift checks, and shared-block implementation details.
- Bounded scan of matching text in:
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - generated `.codex/skills/*/SKILL.md` mirrors
  - generated `dist/adapters/*` skill copies
  - `docs/workflows.md`
  - `specs/skill-contract.md`
- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-08-verify-explain-change-order.md`

## Exclusions

- This session does not change skills, specs, workflow docs, validators, shared blocks, generated output, or adapter output.
- This session does not update a curated topic file because the requested behavior would change the public skill contract and belongs in an authoritative artifact.
- This session does not claim branch readiness, PR readiness, CI status, or generated-output sync.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-08-verify-explain-change-order.md`

The prior session shows the same routing pattern: when an observation would change workflow or skill behavior, learn records the issue and routes it to proposal/spec work instead of directly making policy.

## Observations

### O1: Current first-slice skills expose repository-internal development surfaces

The first-slice skills include guidance that is useful to repository maintainers but not appropriate for an end-user-facing skill package. Examples include references to `specs/rigorloop-workflow.md`, canonical source paths under `skills/<skill>/SKILL.md`, generated mirrors under `.codex/skills/`, public adapter package paths under `dist/adapters/`, selector validation path constraints, drift checks, and shared-block implementation details.

Evidence:

- The contributor cited the `learn` skill as a direct example of public-surface leakage.
- A bounded scan found the same `For full routing rules` and `Generated-output handling` wording across the canonical first-slice skills and generated public adapter copies.

### O2: The same information still belongs somewhere

Repository-internal maintenance rules are necessary for contributors and automation. The problem is not that these rules exist; the problem is that they are copied into skill files that users consume as the published agent interface.

Evidence:

- `AGENTS.md`, `docs/workflows.md`, and `specs/skill-contract.md` already contain repository maintenance guidance about canonical skill source, generated mirrors, adapters, and validation boundaries.
- The contributor specifically framed the issue as "do not show to users", not "remove repository maintenance rules entirely".

### O3: The public skill contract needs an explicit audience boundary

The skill contract should distinguish:

- public skill text shipped to users;
- contributor-facing repository maintenance instructions;
- generated-output and adapter validation rules;
- internal source-of-truth pointers.

Without this boundary, future skill optimization can keep making skills smaller while still leaking maintainer-only details into user-facing instructions.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | direction | direction | Candidate proposal/spec update | Contributor observation with direct skill examples | Removing internal repository details from published skills changes the skill contract and should be decided in authoritative artifacts. |
| O2 | observation | observation | Context for candidate proposal | Bounded evidence in repository guidance surfaces | The maintenance rules remain valid, but their audience and placement need separation. |
| O3 | direction | direction | Candidate proposal/spec update | Contributor observation | The public/internal audience split is reusable, but it requires proposal/spec work before changing skills and validators. |

Contributor confirmation status: confirmed for recording this learn session and treating the issue as follow-up direction. Not confirmed for editing authoritative specs, skills, validators, shared blocks, generated output, or adapter output in this session.

## Routing Results

- Session record: created.
- Topic update: not routed.
- Action-owning artifact update: not routed.
- Recommended follow-up: create a proposal to define the public skill surface boundary, then update `specs/skill-contract.md`, `docs/workflows.md`, `AGENTS.md`, canonical skills, shared blocks, validators, and generated output as needed.

## Best Practice Direction

Skills shipped to users should describe how to operate the skill, not how this repository authors, validates, generates, or packages that skill.

Keep repository-internal details in contributor and governance surfaces, such as `AGENTS.md`, `docs/workflows.md`, specs, validators, templates, and release tooling. Public skills can point to user-available workflow concepts, but should avoid repository-local paths, generated-output implementation details, selector-validation mechanics, and maintainer-only build instructions unless the skill is explicitly a contributor or packaging skill.

## No-Durable-Route Rationale

This session records a contributor-confirmed direction with concrete examples, but it does not update curated topic guidance or authoritative workflow policy. The fix changes the public skill contract and generated packaging expectations, so it belongs in proposal/spec/skill work rather than a learn topic.
