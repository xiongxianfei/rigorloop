# RigorLoop

<!-- vision:start -->
RigorLoop is a rigorous software engineering workflow for AI coding agents. It turns AI work into durable project artifacts so humans can trace, review, trust, and continue what the AI did.

What makes it different: AI coding agents produce output quickly, but the reasoning often disappears. RigorLoop keeps decisions, requirements, tests, current reviews, validation evidence, and verified outcomes in durable project artifacts instead of lost chat logs. The governed lifecycle ends at final verification; external handoff is optional.

Who it is for: RigorLoop is for individual contributors, maintainers, and teams that want AI-assisted software work to remain traceable, resumable, and reviewable without depending on a particular version-control or hosting service.

See [VISION.md](VISION.md) for goals, non-goals, and falsifiability.
<!-- vision:end -->

RigorLoop makes AI-assisted delivery inspectable after the chat ends.
The chain runs from request and Requirement Analysis through reviewed design, delivery planning, implementation, review, and final verification. PR handoff is an optional external integration after compact lifecycle completion.

It is for contributors and maintainers who want AI agents to help with serious software work without losing the reasoning, proof, and review trail that make a change safe to continue.

## Quick Start

Try the CLI without installing anything:

```bash
npx @xiongxianfei/rigorloop@latest --help
```

Install support for the agent you actually use:

```bash
npx @xiongxianfei/rigorloop@latest init codex
```

Use `init claude` for Claude Code.

Pin the package version anywhere reproducibility matters:

```bash
npx @xiongxianfei/rigorloop@0.3.4 init codex
```

For a project-local dev dependency, install once and run through `npx`:

```bash
npm install --save-dev @xiongxianfei/rigorloop
npx rigorloop --help
```

Recommended first pass:

1. Run `init` for one agent adapter.
2. For an existing Change, run `npx rigorloop change context --root . --change CHANGE` to inspect its current handoff.
3. Start your first real change with `requirement-analysis`; use `route` to coordinate authorized continuation.
4. Move through review gates only when the durable artifacts are current.

Read the [normative workflow contract](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) when you need to customize the lifecycle or resolve a process question.

Key paths: [workflow contract](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) · [contribute](CONTRIBUTING.md) · [bug report](.github/ISSUE_TEMPLATE/bug.yml) · [feature request](.github/ISSUE_TEMPLATE/feature.yml) · [security](SECURITY.md)

## Recommended Use

Use the [standard workflow](#workflow-at-a-glance) and current engineering owners. Start Requirement Analysis from the caller's request, reuse existing needs where adequate, and keep requirements, logical behavior and architecture distinct. Plan reviewed work into bounded milestones with required checks, then obtain one independent whole-change Code Review and distinct final Verify.

Keep the current handoff useful for the next engineer: goal and authority, governing basis, progress, open issues, relevant evidence, review standing and next action. Preserve older detail selectively where it still supports a decision. A direct skill invocation performs its authorized scope without silently starting the full workflow.

## Starting a new repository

Use `init` to install agent support.
It does not replace the standing governance and orientation artifacts that make a repository understandable.

```bash
npx @xiongxianfei/rigorloop@latest init codex
```

For a new repository, use this order:

1. Install the adapter for your agent: `init codex` or `init claude`.
2. Bootstrap standing repository guidance:
   - `vision` creates or updates `VISION.md` for project direction and fit checks.
   - `constitution` creates or updates `CONSTITUTION.md` for source-of-truth and governance rules.
   - `project-map` creates or updates `docs/project-map.md` when repository orientation is needed.
   - `route` uses `rigorloop change context --root . --change CHANGE` for deterministic project-local workflow information and retains semantic routing judgment.
   - `docs/plan.md` starts as the small active/blocked/recent-work index.
3. Start the first real change with the per-change lifecycle described above.

For an existing repository, do the same bootstrap only for missing or stale standing guidance.
Do not rewrite durable guides just for symmetry.

## Where to go next

| Need | Read |
| --- | --- |
| Understand project direction | [VISION.md](VISION.md) |
| Understand governance and source-of-truth order | [CONSTITUTION.md](CONSTITUTION.md) |
| Find workflow stages and artifact paths | Run `rigorloop change context --root . --change CHANGE`; read [the workflow contract](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) for policy |
| Orient to repository structure | [docs/project-map.md](docs/project-map.md) |
| See active, blocked, and recent work | [docs/plan.md](docs/plan.md) |
| Use one lifecycle stage | [skills/](skills/) |

## Workflow At A Glance

```mermaid
flowchart LR
  A[Request / RR] --> B[Requirement analysis]
  B --> C[Requirement review]
  C --> D[System design and Architecture design]
  D --> E[Integrated Design review]
  E --> F[Plan]
  F --> G[Delivery review]
  G --> H[Implementation and required checks]
  H --> I[Whole-change Code review]
  I --> J[Final Verify]
  J -. authorized external handoff .-> K[PR]
```

Requirement Analysis reuses, refines or creates obligations as needed. Milestones organize implementation and proof; optional interim advice does not add approval gates. Corrections return to their responsible owner, with affected reassessment before renewed reliance. One independent whole-change Code Review gate precedes distinct final Verify.

Individual skills can perform isolated authorized work. `route` coordinates the current handoff and authority; it does not approve work or invent judgments. Humans and agents supply engineering decisions and evidence; the CLI validates and persists explicit submissions. A save or passing schema check is not approval.

## Authorized continuation

A caller can authorize continuation toward an outcome such as final Verify or PR submission. Record the scope and limits in the current Change. Continue eligible work across milestones, stop affected work at missing authority or unresolved blockers, and obtain the required independent reviews. PR submission, merge and release are distinct actions; authorize each applicable external boundary explicitly.

Resume with `rigorloop change context --root . --change CHANGE`. Use the current command contract and packaged skill guidance for supported recording operations. Historical automation profiles and filesystem records retain their original meaning; they do not activate a successor workflow.

## Worked Example

| Information | Current owner and location |
| --- | --- |
| Request and authorized goal | Current Change handoff through the CLI |
| Obligations and use | `design/requirements/`: IR, SR, AR and Scenarios |
| Logical behavior | `design/system/`: Features and Functions |
| Responsibility and realization | `design/architecture/`: Modules, Interfaces and subordinate detail |
| Reusable methods | `rem/` |
| Stable delivery plan | `docs/plans/<change>.md` |
| Review judgments, findings and selected evidence | CLI-managed local operational records in SQLite |
| Bulky supporting evidence | Local artifact store, retained selectively |
| Successful completion | Compact final acceptance account, with distinct final Verify |
| Optional PR | Authorized external handoff linked from the Change |

This is RigorLoop's repository layout. Customer projects select their own canonical model locations and explicitly adopt applicable contracts; installation alone does not adopt governance or migrate records.

## When to use / When not to use

Use RigorLoop when:

- you want AI-assisted work to stay reviewable, traceable, and grounded in explicit requirements, designs, plans, tests, and verification
- you need a repository-local workflow that leaves durable change history instead of burying decisions in chat
- you want a workflow that makes the path from idea to reviewed change visible and auditable

Do not use RigorLoop when:

- you want agents to bypass required review, validation, ownership, or release judgment
- you need a hosted orchestration platform or centralized control plane
- you want a zero-process scratchpad with no explicit artifacts or review gates

## Why RigorLoop Is Built This Way

- **Reviewable artifacts.** Important decisions become files in your repository, not lost chat logs.
- **Human-understandable AI work.** Reviewers can see what changed, why it changed, and what evidence supports it.
- **Resumable across sessions and agents.** Work can continue because current authoritative state lives in durable project artifacts, not one model session.
- **Traceable from idea to verified change.** A change has a visible chain from request through final verification; external handoff is optional.
- **Durable lessons.** Mistakes become reusable guidance and checks, improving reliability over time.

## npm Usage

The npm package is:

```text
@xiongxianfei/rigorloop
```

It exposes one binary:

```text
rigorloop
```

### Run directly with `npx`

You do not need to install RigorLoop before trying it:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@latest init codex --dry-run --json
```

Use `@latest` for quick manual trials. Use a pinned version for automation, CI, onboarding docs, and repeatable agent setup:

```bash
npx @xiongxianfei/rigorloop@0.3.4 init codex --json
```

### Run after project-local install

```bash
npm install --save-dev @xiongxianfei/rigorloop
npx rigorloop --help
npx rigorloop init codex
```

### Run after global install

```bash
npm install --global @xiongxianfei/rigorloop
rigorloop --help
rigorloop init codex
```

The current CLI candidate supports:

- `rigorloop --help`
- `rigorloop version`
- `rigorloop init codex|claude [--force] [--dry-run] [--json]`
- `rigorloop change create --root PATH --input - --format json`
- `rigorloop change context --root . --change CHANGE --format json`

`init codex` installs verified Codex support into `.agents/skills/`. The CLI uses package-bundled official metadata, downloads the official GitHub release archive, verifies archive SHA-256 and installed tree hash, and leaves `rigorloop.yaml` / `rigorloop.lock` untouched without reading or writing them.

`change create` creates a current Change through the v2 interface from an explicit targeted request. It does not replace requirement, design, review, Verify or PR judgment. See [CLI recording usage](packages/rigorloop/README.md).

The npm package is a delivery channel for the CLI. It is not the canonical source for workflow rules, skills, schemas, templates, or adapter archives. Canonical source remains in this repository, and adapter archives remain verified GitHub release artifacts.

## Vision and README Ownership

`VISION.md` is the canonical project-vision artifact. Proposals created or substantively revised after this spec is adopted include `Vision fit`.

README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`. README front-matter is not the source of truth when it conflicts with `VISION.md`.

## Adapter Packages

RigorLoop ships generated adapter packages for Codex and Claude Code as GitHub release archives. The active install contract is in `dist/adapters/README.md`.

| Tool | Archive pattern | Skill directory |
| --- | --- | --- |
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |

The current support matrix is tracked in `dist/adapters/manifest.yaml`; it records support for the two current targets.

`skills/` is the only authored skill source. `.codex/skills/` is ignored local Codex runtime state; keep it untracked if you copy installed Codex adapter skills there for local runtime use.

For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`. Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window while introducing release archives.

Adapter compatibility claims are versioned. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

Ordinary contributors do not need all supported tools installed locally to run non-smoke validation. Maintainer smoke for Codex and Claude Code is recorded in `docs/releases/<version>/release.yaml` before a stable release.

### Using Adapter Skills

Claude Code uses native skill slash commands after the Claude adapter is installed. TUI examples:

```text
/requirement-analysis Analyze this request against the existing requirements.
/system-design Define the required logical behavior.
/architecture-design Allocate responsibilities and realization.
/implement Build the approved milestone with tests first.
/code-review Review the current diff against the approved artifacts.
/pr Prepare the verified change for pull request review.
```

Existing destination skills conflict even when identical. Use `--force` for complete replacement; local changes inside replaced skill directories leave the active installation, with originals retained outside discovery for inspection. Unrelated skills and state files stay untouched. OpenCode and `--write-state` are no longer supported.

## Learn More / Contribute

- Workflow detail: [Workflow](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md); inspect project facts with `rigorloop change context --root . --change CHANGE`
- Artifact and skill docs: [System](design/architecture/composition.md) and [skills/](skills/)
- Report problems or feature ideas: [bug report template](.github/ISSUE_TEMPLATE/bug.yml) and [feature request template](.github/ISSUE_TEMPLATE/feature.yml)
- Review PR expectations before contributing: [.github/pull_request_template.md](.github/pull_request_template.md)
- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)

## Workflow Categories

RigorLoop recommends one standard workflow for complete AI-assisted delivery:

- Standing artifacts: `VISION.md` and `CONSTITUTION.md`
- Living references: `docs/project-map.md` when repository shape is not obvious enough for safe reliance
- Workflow infrastructure: Designs, CLI workflow context, affected root guidance, affected skills, and generated outputs
- On-demand support: `explore` and `research`
- Compact per-change chain: `requirement-analysis -> requirement-review -> system-design / architecture-design -> design-review -> plan -> delivery-review -> implement -> code-review -> verify`. PR is an optional external handoff after lifecycle completion.
- Periodic learning: `learn`

Explore (`explore`) expands a materially unclear decision space; Research (`research`) reduces bounded uncertainty about facts that can change a decision. Use both when the option comparison depends on unanswered research questions, and neither when direction and relevant facts are already clear. They are optional supporting skills: an explicit invocation writes a standalone artifact under `docs/explorations/` or `docs/research/`, and the owning stage must adopt any conclusion that affects its decision. Neither skill approves a direction or advances the lifecycle. `learn` is periodic or explicitly invoked, not a final stage for every change. `ci-maintenance` means updating hosted workflow automation or related CI infrastructure; validation execution belongs to `verify`.

Do not rely on `docs/project-map.md` when it is absent, stale, contradicted, or missing the relied-on area; refresh it or record a no-map rationale first.

Users may manually invoke individual skills for focused output. A manual skill invocation is isolated by default and does not imply that the full workflow is complete.

The normative contract lives in [Workflow](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md). Deterministic project-local workflow facts come from `rigorloop change context --root . --change CHANGE`; semantic routing belongs to `route`.

## What This Repository Contains

- one recommended standard workflow for complete AI-assisted delivery
- isolated manual skill invocation for focused skill output
- standing artifacts, living references, on-demand support, a per-change chain, and periodic learning as distinct lifecycle categories
- a repository orientation map at `docs/project-map.md`
- canonical engineering definitions in `design/`, reusable methods in `rem/`, and instructions/tooling in `skills/`, `schemas/` and `scripts/`
- ignored local Codex runtime state in `.codex/skills/`
- generated public adapter packages in `dist/adapters/`
- a current local Change handoff through the CLI for coordinated engineering work

## Current operational records

Current operations use the v2 public interface and v4 semantic records in SQLite. The CLI owns persistence; skills supply explicit inputs and never write SQL. The handoff preserves unresolved obligations, attributed judgments and useful evidence without recording every action. Completion retains a compact historical acceptance account.

Engineering definitions remain Git-held model sources. Historical filesystem records and synthetic examples retain their original contracts; explicit import preserves required original identities and does not silently adopt old judgments as current approval. See [Work record storage](design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md) for the full contract.

## Source Of Truth

- Edit canonical workflow content in:
  - `design/` and `rem/`
  - `docs/` for usage and contributor guidance
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated public adapter packages. Use `dist/adapters/README.md` for public adapter installation.
- `skills/` is the only authored skill source. `.codex/skills/` is ignored local Codex runtime state; keep it untracked when copying installed Codex adapter skills there for local runtime use, and edit canonical skills under `skills/`.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface.
- Execution plans use the packaged `skills/plan/assets/plan-skeleton.md` scaffold.

## Validation Commands

Run the repository-owned selector and required checks for your change:

```bash
bash scripts/ci.sh --mode local
```

[Contributing](CONTRIBUTING.md#validation-scope) explains scoped and PR-range checks. Packaging changes also use `python scripts/build-adapters.py --check`; release qualification follows the actual prepared-candidate procedure in [Release](design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md).

## Repository Layout

```text
.
├── AGENTS.md
├── CONSTITUTION.md
├── VISION.md
├── .github/
├── design/                    Current engineering definitions
├── rem/                       Reusable engineering methods
├── docs/
│   ├── changes/
│   ├── plans/
│   ├── proposals/
│   ├── releases/
│   ├── plan.md
│   └── project-map.md
├── packages/rigorloop/
├── dist/adapters/
├── scripts/
├── skills/
├── schemas/
├── templates/
└── tests/
```

## License

This repository currently ships with the MIT license.

The unified authoring skill replaces `spec` and `architecture` with `design`. Existing retired entries require [separate inspection and reconciliation](packages/rigorloop/README.md#upgrading-retired-authoring-skills); installation does not manage project state or automatically migrate those entries. The selected [Design](design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md) and [System](design/architecture/composition.md) own the bounded method/composition migration. The three main models are [Skill](design/architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md), [CLI](design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) and [Engineering](design/support/development.md). Engineering [Packaging](design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md) owns artifact production; CLI [Installation](design/architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md) owns trusted acquisition and destination writes. Current responsibilities are self-contained in these models; retired source provenance and removal evidence are recorded in the cleanup change (historical operational reference; original assessment unavailable in the current tree).
