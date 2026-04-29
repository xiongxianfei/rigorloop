---
name: vision
description: >
  Produce or update the project vision and matching README front-matter. Use at project genesis, or when accumulated proposals reveal that the current vision no longer reflects what the project is becoming. This skill is upstream of the per-change workflow and is not a normal lifecycle stage.
---

# Project Vision

You are producing the document people read first when they encounter this project.

A vision answers: what is this, who is it for, what does it commit to, what does it refuse to become, and how should future proposals be checked for fit.

This is not a proposal, spec, architecture document, roadmap, task tracker, or README maintenance pass. It describes project identity and scope. It does not describe how the project is built.

## Inputs To Read

Start with compact project inputs when available:

- `CONSTITUTION.md`
- `AGENTS.md`
- README front-matter between `<!-- vision:start -->` and `<!-- vision:end -->`
- existing root `vision.md`
- recent proposal summaries, especially proposals that touch scope or direction
- `docs/project-map.md` when it helps project framing
- prior research or exploration artifacts when the workflow already produced them

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, proposal IDs, section names, file paths, counts, and line citations when comparing project direction or repeated artifact scans.

Escalate from compact inputs to broader reads or full-file reads only when compact inputs are missing, conflicting, or insufficient to decide project-level framing.

## Source Of Truth

`CONSTITUTION.md` outranks `vision.md`.

`vision.md` is canonical for project vision and proposal-fit reasoning. README front-matter is generated from `vision.md` and is not independently authoritative.

Do not edit README front-matter directly to express a vision change. Edit `vision.md`, then run this skill in `mirror` mode.

Do not create the initial `vision.md` just because this skill is installed. The first `vision.md` is created only by an explicit create-mode invocation.

## Modes

Use exactly one mode.

### create

Use create mode when no root `vision.md` exists and the user clearly asks to produce the project vision.

Create:

- root `vision.md`
- README front-matter at the deterministic marker location

Report assumptions and open vision-level questions.

### revise

Use revise mode when root `vision.md` exists and the user names a section or project-level change to revise.

Update only the named section unless the change necessarily cascades to another section. If it cascades, say why. Regenerate README front-matter after the vision edit.

Before finalizing, classify the revision as substantive or editorial. A substantive revision is caused by a proposal, incident, learning, or project-direction drift. When a change-local pack exists, remind the contributor to record the causal link in:

```text
docs/changes/<change-id>/change.yaml
docs/changes/<change-id>/explain-change.md
```

Editorial revisions and mirror-only changes do not require a new change-local pack solely because this skill ran.

If the user asks to revise an unnamed section, ask which section is being revised before editing.

### mirror

Use mirror mode when root `vision.md` exists and remains current.

Leave `vision.md` unchanged and regenerate README front-matter from it. If README front-matter already matches, report that no content changed.

If root `vision.md` is missing, stop because there is no canonical source to mirror.

## Existing Vision Protection

If root `vision.md` exists and the user's request does not clearly specify `revise` or `mirror`, stop and ask which mode applies before editing. Do not silently overwrite authorial judgment.

## Vision Content

Root `vision.md` stays at or under 500 words.

Use plain language. Do not use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary in generated or revised vision text.

Do not include feature lists, implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, or priority columns.

Use plain Markdown. `vision.md` must not require rendered tables, diagrams, HTML layout, or generated assets to be understood.

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
- a link to `vision.md` for goals, non-goals, and falsifiability

The front-matter must be derived from `vision.md`, not independently authored.

Automatic marker insertion is allowed only in `create` mode.

If README already contains one valid marker block, replace only content inside the marker block and preserve all content outside it.

In `create` mode, if README has no marker block and contains a Markdown H1, insert the marker block immediately after the first H1 block. The first H1 block is the first line matching `# <title>` plus any immediately following badge/image lines or blank lines directly attached to that heading.

In `create` mode, if README has no H1, insert the marker block at the start of the file and preserve existing content after it.

In `mirror` or `revise`, missing or malformed markers stop the skill before file modification unless the user explicitly authorizes marker insertion or skipping README mirroring.

If README has malformed, nested, or multiple vision marker pairs, stop and request explicit handling instead of rewriting README broadly.

Do not edit README content outside the marker block except to insert the marker block in create mode when it is missing.

## Security And Research Boundaries

`vision.md` and generated README front-matter must not include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication.

If sensitive or private content is present in inputs, omit it or ask for explicit confirmation before including it.

The skill must not fetch external information unless the user explicitly requests research or the workflow invokes a research-backed mode before vision drafting.

If external research is used, distinguish researched facts from project assumptions.

## Workflow Fit

This skill is upstream of the normal per-change workflow. It does not hand off to another stage on completion.

Use it at project genesis, or when proposal review or learn surfaces a vision-level conflict. Do not run it just because a feature was added, an architecture changed, or README needs ordinary setup instructions.

Future proposals should be checked against `vision.md` when it exists, but proposal requirements still belong in proposals and specs.

## Rules

- Do not create or revise `vision.md` unless the mode authorizes that edit.
- Do not insert generated README vision front-matter outside create, revise, or mirror behavior.
- Do not add a README mirror helper script as part of this skill.
- Do not make `vision` a normal lifecycle stage.
- Do not silently redefine project vision through README edits.
- Do not let the vision exceed 500 words.
- Do not include implementation detail or architecture content.
- Do not rewrite legacy proposals solely to add `Vision fit`.

## Evidence Collection Efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, proposal IDs, section names, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Full-file reads are required when creating or replacing root `vision.md`, when the whole file is the review target, when the relevant section cannot be isolated safely, when surrounding context can change the conclusion, when compact inputs are missing or conflicting, when bounded searches disagree or produce incomplete evidence, when README marker placement depends on the whole README structure, or when a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Report:

- Mode used: `create`, `revise`, or `mirror`
- Files changed:
- README front-matter: created, replaced, unchanged, or not applicable
- Assumptions: required in create mode
- Sections changed: required in revise mode
- `vision.md` unchanged: required in mirror mode
- open questions suitable for human review before treating the vision as current
