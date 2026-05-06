---
name: vision
description: >
  Produce or update the project vision and matching README front-matter. Use at project genesis, or when accumulated proposals reveal that the current vision no longer reflects what the project is becoming. This skill is upstream of the per-change workflow and is not a normal lifecycle stage.
---

# Project Vision

You are producing the document people read first when they encounter this project.

A vision answers: what is this, who is it for, what does it commit to, what does it refuse to become, and how should future proposals be checked for fit.

This is not a proposal, spec, architecture document, roadmap, task tracker, or README maintenance pass. It describes project identity and scope. It does not describe how the project is built.

## Workflow Fit

This skill is upstream of the normal per-change workflow. It does not hand off to another stage on completion.

Use it at project genesis, or when proposal review or learn surfaces a vision-level conflict. Do not run it just because a feature was added, an architecture changed, or README needs ordinary setup instructions.

Future proposals should be checked against `VISION.md` when it exists, but proposal requirements still belong in proposals and specs.

## Inputs To Read

Start with compact project inputs when available:

- `CONSTITUTION.md`
- `AGENTS.md`
- README front-matter between `<!-- vision:start -->` and `<!-- vision:end -->`
- existing root `VISION.md`
- retired root `vision.md`, only as an ordinary repository file when the user explicitly asks about that path
- recent proposal summaries, especially proposals that touch scope or direction
- `docs/project-map.md` when it helps project framing
- prior research or exploration artifacts when the workflow already produced them

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, proposal IDs, section names, file paths, counts, and line citations when comparing project direction or repeated artifact scans.

Escalate from compact inputs to broader reads or full-file reads only when compact inputs are missing, conflicting, or insufficient to decide project-level framing.

## Edit Authorization

`CONSTITUTION.md` outranks `VISION.md`.

`VISION.md` is canonical for project-vision content.

`VISION.md` outranks README front-matter. README front-matter is generated from `VISION.md` and is not independently authoritative.

The skill follows state-based behavior from repository state and ordinary user intent. Do not ask users to choose `create`, `revise`, or `mirror` modes.

Do not create the initial `VISION.md` just because this skill is installed or invoked for ordinary README maintenance.

Do not edit README front-matter directly to express a vision change. Edit `VISION.md`, then synchronize README from it.

Ensure existing visions are not overwritten without clear update intent; keep the current file unchanged and ask for clarification before editing.

Root `VISION.md` is the only supported project-vision artifact.

If the user asks this skill to read, edit, merge, delete, or migrate retired root `vision.md` as project vision, stop and explain that root `VISION.md` is the only supported project-vision artifact unless the owner gives a separate non-vision-file instruction.

## State-Based Behavior

Interpret legacy words such as `create`, `revise`, or `mirror` only as natural-language hints about user intent. Apply the state-based rules below and do not report those words as operating modes.

If no root `VISION.md` exists:

- If neither root vision file exists and the user explicitly asks to establish project vision, create root `VISION.md`, generate README front-matter, insert README vision markers when missing using deterministic placement, and report assumptions plus open vision-level questions.
- If the user did not clearly ask to establish project vision, stop and ask whether to create `VISION.md`. Do not edit README while that intent is unclear.

If root `VISION.md` exists and the user asks to update vision:

- Update only the requested section or clearly related sections.
- If a requested change necessarily cascades across sections, state why before finalizing.
- If the section or update intent is unclear, stop and ask for clarification before editing.
- Always ask or confirm whether the change is `substantive` or `editorial` before finalizing, even when the user proposes the classification.
- Treat changes to project scope, target users, commitments, refusals, proposal-fit framing, or falsifiability as substantive unless an owner records a contrary rationale.
- For substantive changes tied to an existing or required change-local pack, require the causal link in `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing.
- Update README front-matter only inside an existing valid marker block.
- When updating an existing `VISION.md` or syncing README, missing or malformed markers stop the skill unless the user explicitly authorizes marker insertion or skipping README synchronization.

If root `VISION.md` exists and the user asks to sync README:

- Leave `VISION.md` unchanged.
- Update README front-matter only inside an existing valid marker block.
- If README front-matter already matches, report that no content changed.
- If README markers are missing, malformed, nested, or duplicated, stop unless the user explicitly authorizes marker insertion.

Editorial updates and README-only synchronization do not require a new change-local pack solely because this skill ran.

## Vision Content

Root `VISION.md` should normally stay at or under 750 words.

For methodology, protocol, workflow, or operating-model projects, root `VISION.md` may exceed 750 words only when the owner explicitly allows the extra length and the additional content is needed to explain the project category, methodology pillars, tradeoff, refusals, or falsifiability.

Generated or revised `VISION.md` MUST NOT exceed 900 words. A draft over 900 words is invalid and must be shortened before completion.

Use plain language. Do not use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary in generated or revised vision text.

Do not include feature lists, implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, or priority columns.

Use plain Markdown. `VISION.md` must not require rendered tables, diagrams, HTML layout, or generated assets to be understood.

Include sections, in this order, with plain-language headings:

1. Pitch
2. What makes this different
3. Who it is for
4. Who it is not for
5. What it commits to
6. What it refuses to be
7. What would prove this wrong
8. Open questions, only when vision-level uncertainty remains

Concrete and verifiable language beats abstract claims. Scope refusals should be real enough to guide future proposal decisions.

## Strategic Positioning

Before drafting the initial `VISION.md` or materially repositioning an existing one, perform a strategic-positioning pass. Identify:

- project category
- primary user
- primary pain
- primary promise
- core mechanism
- alternatives
- tradeoff
- compatibility surfaces
- refusals
- falsifiability

For initial visions and material repositioning, write this pass to `docs/vision/strategic-positioning.md` as supporting rationale. `VISION.md` remains canonical; the rationale explains how the vision was derived and does not independently override it. If `docs/vision/strategic-positioning.md` conflicts with `VISION.md`, update the rationale or revise `VISION.md` through a substantive vision update.

For editorial updates, README-only sync, or narrow section edits, keep the strategic-positioning pass internal and do not update `docs/vision/strategic-positioning.md` unless strategic assumptions changed or a conflict is found.

For substantive repositioning in a repository that uses a change-local pack, require `docs/changes/<change-id>/explain-change.md` to summarize the positioning delta and link to `docs/vision/strategic-positioning.md`.

Treat repository layout, Git, CI, pull requests, runtime, package format, hosting platform, language, and template mechanics as compatibility surfaces unless the owner explicitly chooses one as the project category or the substrate is genuinely the product.

When the project itself is a methodology, workflow, protocol, or operating model, use methodology-as-product framing: the methodology pillars or operating loop are part of project identity rather than implementation detail.

For methodology, workflow, protocol, or operating-model projects, you may add one optional methodology-oriented section only when available inputs identify concrete methodology pillars or an operating loop. If the owner has not supplied enough detail, keep the standard sections and report an open vision-level question instead of inventing methodology structure.

Use fixture-style checks when evaluating category quality:

- RigorLoop-style inputs should lead with an AI-agent software engineering workflow or methodology category, treat Git and CI as compatibility surfaces, include methodology pillars as the core mechanism, and avoid making `Git-first starter kit` the category.
- A Windows-native file manager should lead with the file-manager product category; WinUI, MSIX, and Shell APIs appear only when they materially affect the differentiator.
- A Git extension may lead with Git because Git is the actual product category.

Before reporting completion, check that the first sentence names the highest-level category, the differentiator includes a tradeoff, the core mechanism appears when essential, compatibility surfaces are not the main identity, audience non-fit is visible, commitments are checkable, refusals block tempting scope creep, falsifiability is observable, and the vision can guide proposal-fit review without chat history.

For initial visions and materially repositioned visions, final output reports a concise strategic-positioning summary and rationale path. For editorial updates, README sync, or narrow section edits, keep the positioning pass internal unless it changes assumptions or reveals a conflict.

## Drafting Heuristics

Use these as authoring questions or checks, not additional `VISION.md` sections:

- Differentiator: what alternative class or specific tool is this different from, and what tradeoff does this project make?
- Pain points: are the project pain points embedded in the differentiator instead of presented as an unrelated complaint list?
- Commitments: is each commitment concrete and checkable by a future reviewer?
- Falsifiability: are the failure conditions observable from behavior or artifacts?
- Audience: does the audience statement rule out at least one plausible non-fit?
- Refusals: are scope refusals concrete enough to block misaligned proposals?
- Category: is a lower-level compatibility surface being mistaken for the project category?

The differentiator comparison may name an alternative class or a specific tool. It does not require naming a specific competitor.

## README Front-Matter

README front-matter is bounded by this exact marker pair:

```markdown
<!-- vision:start -->
<!-- vision:end -->
```

Generated README front-matter includes only:

- the pitch
- the differentiator
- the target audience
- a link to `VISION.md` for goals, non-goals, and falsifiability

The front-matter must be derived from `VISION.md`, not independently authored.

Automatic marker insertion is allowed only when creating the initial `VISION.md`.

If README already contains one valid marker block, replace only content inside the marker block and preserve all content outside it.

During initial `VISION.md` creation, if README has no marker block and contains a Markdown H1, insert the marker block immediately after the first H1 block. The first H1 block is the first line matching `# <title>` plus any immediately following badge/image lines or blank lines directly attached to that heading.

During initial `VISION.md` creation, if README has no H1, insert the marker block at the start of the file and preserve existing content after it.

When updating an existing `VISION.md` or syncing README, missing or malformed markers stop the skill before file modification unless the user explicitly authorizes marker insertion or skipping README synchronization.

This is the same gate as existing guidance that says the user explicitly authorizes marker insertion or skipping README mirroring.

If README has malformed, nested, or multiple vision marker pairs, stop and request explicit handling instead of rewriting README broadly.

Do not edit README content outside the marker block except to insert the marker block when initial vision creation or explicit owner authorization allows insertion.

## Security And Research Boundaries

`VISION.md` and generated README front-matter must not include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication.

If sensitive or private content is present in inputs, omit it or ask for explicit confirmation before including it.

The skill must not fetch external information unless the user explicitly requests research or the workflow invokes a research-backed mode before vision drafting.

If external research is used, distinguish researched facts from project assumptions.

## Rules

- Do not create or update `VISION.md` unless repository state and user intent authorize that edit.
- Do not insert generated README vision front-matter during update or sync unless the user explicitly authorizes marker insertion.
- Do not add a README synchronization helper script as part of this skill.
- Do not make `vision` a normal lifecycle stage.
- Do not silently redefine project vision through README edits.
- Do not let generated or revised `VISION.md` exceed 900 words.
- Do not include implementation detail or architecture content.
- Do not rewrite legacy proposals solely to add `Vision fit` or update historical `vision.md` references.

## Evidence Collection Efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, proposal IDs, section names, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Full-file reads are required when creating or replacing root `VISION.md`, when the whole file is the review target, when the relevant section cannot be isolated safely, when surrounding context can change the conclusion, when compact inputs are missing or conflicting, when bounded searches disagree or produce incomplete evidence, when README marker placement depends on the whole README structure, or when a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Report:

- Files changed:
- README front-matter: created, replaced, unchanged, skipped, blocked, or not applicable
- Assumptions: required when establishing the initial vision
- Sections changed: required when updating vision
- Revision classification: `substantive` or `editorial`, required when updating vision
- `VISION.md` unchanged: required when syncing README only
- Strategic-positioning summary: required for initial visions and materially repositioned visions
- Positioning rationale path: required when `docs/vision/strategic-positioning.md` is created or updated
- For substantive updates: whether the required causal link was recorded or not required
- open questions suitable for human review before treating the vision as current
