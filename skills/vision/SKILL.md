---
name: vision
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Produce or update the project vision and matching README front-matter at project genesis or when current vision no longer reflects the project. This skill is upstream of the per-change workflow.
argument-hint: [project idea, update vision, or sync README]
---

# Project vision

Define project identity, audience, commitments, refusals, and falsifiability—not specifications, architecture, roadmaps, or trackers.

## Workflow role

- role_name: vision
- stage: authoring
- upstream: explicit owner intent, repository state, and applicable project evidence
- downstream: none automatically
- summary: Establish or revise canonical project vision and keep derived README front-matter aligned.
- ownership: Write only authorized `VISION.md`, supporting strategic rationale, README marker-bounded content, and required same-change evidence.
- must_not_claim: proposal, specification, architecture, plan, implementation, review, verification, branch, PR, release, or deployment completion

## Workflow Fit

This upstream skill does not hand off automatically. Use it at project genesis or for a surfaced vision-level conflict.

## Inputs To Read

Start with compact project inputs: `CONSTITUTION.md`, `AGENTS.md`, root `VISION.md`, README content between `<!-- vision:start -->` and `<!-- vision:end -->`, relevant proposals, and useful project-map evidence. Retired root `vision.md` is an ordinary file only when explicitly requested.

Use summary and stable-ID first reasoning with check IDs, requirement IDs, proposal IDs, section names, file paths, counts, and line citations. Expand only for insufficient or conflicting evidence.

## Edit Authorization

`CONSTITUTION.md` outranks `VISION.md`; `VISION.md` is canonical; `VISION.md` outranks README front-matter. Root `VISION.md` is the only supported project-vision artifact. existing visions are not overwritten without clear update intent.

Do not ask users to choose `create`, `revise`, or `mirror` modes. Legacy words are intent hints only. Loading a reference or copying an asset never grants establishment, revision, insertion, skip, lifecycle, routing, review, or continuation authority.

## State-Based Behavior

This state-based behavior resolves ordinary user intent to exactly `establish-vision`, `revise-vision`, or `sync-readme`; ordinary read-only questions are outside this vocabulary.

- If the user explicitly asks to establish project vision, create root `VISION.md` only when it is absent. Existing vision routes to explicit revision. Do not create the initial `VISION.md` just because this skill is installed or invoked for ordinary README maintenance.
- `revise-vision` requires existing `VISION.md` and exact update intent. Absent vision routes to establishment. Update only requested or necessarily related sections and explain required cascades.
- `sync-readme` requires existing `VISION.md`, leaves it unchanged, and changes only authorized README front-matter.

For revision, ask or confirm whether the change is `substantive` or `editorial` before finalizing. Internally classify exactly `editorial`, `substantive-nonmaterial`, or `material-repositioning`. Scope, audience, commitment, refusal, proposal-fit, or falsifiability changes are substantive absent owner rationale. Governed work uses the existing or required change-local pack and records causal links in `change.yaml` and `explain-change.md`.

If the user asks this skill to read, edit, merge, delete, or migrate retired root `vision.md` as project vision, stop and explain that root `VISION.md` is the only supported project-vision artifact unless the owner gives a separate non-vision-file instruction.

## Resource classification

Independently classify `strategic_authoring_context` as `false|true` and `readme_sync_context` as `required|skipped`. Pre-resolved skip needs one exact current owner instruction before marker inspection; late skip retains README procedure.

| Assembly | Strategic reference | README reference |
| --- | --- | --- |
| `VA0-readme-sync` | no | yes |
| `VA0S-readme-skip` | no | no |
| `VA1-editorial-sync` | no | yes |
| `VA1S-editorial-skip` | no | no |
| `VA2-strategic-sync` | yes | yes |
| `VA2S-strategic-skip` | yes | no |

Initial establishment uses `VA2-strategic-sync`. Editorial work uses VA1 unless uncertainty, changed assumptions, or conflict requires late strategic loading. Substantive work loads strategic procedure before final judgment or mutation. Explicit README sync uses VA0. `blocked` is a result, not an assembly.

## Secondary actions and assets

Classify positioning action exactly as `unchanged`, `create`, `update`, `full-rewrite`, or `blocked`, and README action as `synchronize-existing`, `insert-and-synchronize`, `skip`, or `blocked`. Classify both independently from public significance.

Establishment creates positioning rationale. Unaffected editorial or substantive-nonmaterial revision leaves it unchanged. Changed assumptions or authorized conflict correction update it; unresolved choice blocks. Material repositioning updates, creates when required, or uses authorized full rewrite. Never adopt unrelated rationale.

Both asset contexts are exactly `not-required|create-or-full-rewrite`. Copy the vision asset only for establishment or authorized full canonical rewrite; copy the positioning asset only for creation or full rewrite. Narrow historical revisions preserve structure. Assets own structure only, never policy or authority.

## Operation manifest and recovery

Before any write or final skip, resolve one exact operation manifest. Each target records path, role, action, prior identity or absence, intended identity, and evidence state. Governed work persists the complete manifest in authorized change-local authoring evidence before its first target write when that evidence model supports the contract. Zero-write sync skip records unchanged canonical vision and skipped README targets with equal prior and intended identities, plus `marker_state: not-evaluated-under-exact-skip`.

Validate operation, significance, actions, paths, authority, content, privacy, provenance, baselines, intended identities, and marker evidence, then reread targets. Write source-first: canonical `VISION.md`, positioning rationale, derived README. Immediately before README action, revalidate canonical and README identities, inspected markers, authority, and manifest. Completion requires read-back of every required target.

Result is exactly `complete`, `partial-retry-required`, or `blocked-before-write`. Blocked mutates nothing. Zero-write skip has no changed files and claims neither synchronization nor marker validity. Partial results name committed and pending targets, identities, manifest, and retry without claiming synchronization. Exact retry binds the same operation, manifest, targets, inputs, identities, actions, and authority, completing matching pending work only. Never adopt or overwrite unrelated, stale, ambiguous, lost, or concurrent state. Portable cross-session recovery stops without its manifest.

## Security And Research Boundaries

Vision and generated README text must not include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication. Omit sensitive input or request explicit confirmation. The skill must not fetch external information unless the user explicitly requests research or workflow supplies research-backed authority; distinguish researched facts from project assumptions.

## Stop conditions and claims

Stop before dependent work for unclear intent, invalid state, unresolved authority, unsafe content, missing identities, partial conflict, or a missing, unreadable, escaped, stale, contradictory, or mixed-version required resource. Do not reconstruct procedure or structure from memory.

Do not claim review approval, downstream readiness, implementation, validation, verification, branch readiness, PR readiness, publication, release, or deployment. This skill never opens a PR, pushes, or starts another lifecycle stage.

## When full-file read is required

Use full-file reads when creating or replacing root `VISION.md`, when the whole file is the review target, when surrounding context controls an edit, when bounded searches disagree, when README placement depends on complete structure, or when a behavior-changing edit depends on the whole source-of-truth artifact.

## Resource map

- READ `references/strategic-vision-authoring.md` when `strategic_authoring_context` is true. It owns strategic positioning, vision content, drafting, word-limit, and quality procedure.
- READ `references/readme-vision-sync.md` when `readme_sync_context` is required or marker evidence must be inspected. It owns marker parsing, authorized insertion mechanics, derivation, bounded replacement, idempotence, and README result procedure.
- COPY `assets/vision-skeleton.md` when vision asset context is `create-or-full-rewrite`.
- COPY `assets/strategic-positioning-skeleton.md` when positioning asset context is `create-or-full-rewrite`.

Confirm required resources are readable, contained, and from one package version before dependent work.

## Output skeleton

```md
COPY applicable structural asset for creation or authorized full rewrite.
Fill <every applicable field> and remove insertion markers and placeholders.
Preserve <existing structure> for narrow revision.
```

## Expected output

Report `Files changed:`, `README front-matter:`, operation, assembly, manifest, target results, blockers, and claims. Establishment adds `Assumptions:`, open questions, positioning summary, and rationale path. Revision adds `Sections changed:`, significance, and whether the required causal link was recorded or not required. README-only sync adds ``VISION.md` unchanged:`.
