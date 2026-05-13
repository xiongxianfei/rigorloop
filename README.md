# RigorLoop

<!-- vision:start -->
RigorLoop is a rigorous software engineering workflow for AI coding agents. It turns product intent into traceable proposals, requirements, tests, architecture, plans, implementation, validation evidence, and review decisions so humans can understand agent-produced changes with confidence.

What makes it different: Most AI coding tools optimize for faster output. RigorLoop optimizes for trustworthy change delivery by keeping source of truth, rationale, tests, design intent, validation evidence, and review concerns in durable project artifacts.

Who it is for: RigorLoop is for individual contributors, maintainers, and teams that want AI agents to participate in serious software delivery without weakening engineering discipline.

See [VISION.md](VISION.md) for goals, non-goals, and falsifiability.
<!-- vision:end -->

*Rigorous workflow for AI-assisted software delivery with explicit artifacts, review gates, and durable change history.*

RigorLoop helps individual contributors turn AI-assisted ideas into reviewable changes with proposals, specs, plans, tests, review gates, verification, and explainable change history. That gives contributors clearer review scope, explicit artifact history, and traceable change rationale from idea to PR. It also helps maintainers and small teams keep AI-assisted delivery explicit and auditable without replacing Git, pull requests, CI, or human review.

## When to use / When not to use

Use RigorLoop when:

- you want AI-assisted work to stay reviewable, traceable, and grounded in explicit proposals, specs, plans, tests, and verification
- you need a repository-local workflow that leaves durable change history instead of burying decisions in chat
- you want a workflow that makes the path from idea to reviewed change visible and auditable

Do not use RigorLoop when:

- you want agents to bypass pull requests, CI, or human review
- you need a hosted orchestration platform or centralized control plane
- you want a zero-process scratchpad with no explicit artifacts or review gates

## Quick Start

1. Read the [short workflow summary](docs/workflows.md).
2. Read the [normative workflow contract](specs/rigorloop-workflow.md).
3. Inspect the [shipped proof-of-value example](docs/changes/0001-skill-validator/).
4. If the approach fits, start from the lifecycle artifacts under [docs/](docs/), [specs/](specs/), and [skills/](skills/).

## Vision and README Ownership

`VISION.md` is the canonical project-vision artifact. Proposals created or substantively revised after this spec is adopted include `Vision fit`.

README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`. README front-matter is not the source of truth when it conflicts with `VISION.md`.

## Adapter Packages

RigorLoop ships generated adapter packages for Codex, Claude Code, and opencode as GitHub release archives. The active install contract is in `dist/adapters/README.md`.

| Tool | Archive pattern | Skill directory |
| --- | --- | --- |
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |
| opencode | `rigorloop-adapter-opencode-<version>.zip` | `.opencode/skills/` |

The current support matrix is tracked in `dist/adapters/manifest.yaml`; it records adapter support and generated opencode command aliases under `command_aliases.opencode`.

`skills/` is the only authored skill source. `.codex/skills/` is ignored local Codex runtime state; keep it untracked if you copy installed Codex adapter skills there for local runtime use.

For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`. Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window while introducing release archives.

Adapter compatibility claims are versioned. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

Ordinary contributors do not need all supported tools installed locally to run non-smoke validation. Maintainer smoke for Codex, Claude Code, and opencode is recorded in `docs/releases/<version>/release.yaml` before a stable release.

### Using Adapter Skills

Claude Code uses native skill slash commands after the Claude adapter is installed. TUI examples:

```text
/proposal Evaluate whether this change should be specified.
/spec Define the observable behavior for this change.
/implement Build the approved milestone with tests first.
/code-review Review the current diff against the approved artifacts.
/pr Prepare the verified change for pull request review.
```

OpenCode uses generated command aliases for the curated lifecycle stages. All included portable skills remain reusable under `.opencode/skills/`; thin command aliases live under `.opencode/commands/`. TUI examples:

```text
/proposal Evaluate whether this change should be specified.
/spec Define the observable behavior for this change.
/implement Build the approved milestone with tests first.
/code-review Review the current diff against the approved artifacts.
/pr Prepare the verified change for pull request review.
```

OpenCode command aliases are generated only for `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, and `pr`. Other portable skills remain available as skills but do not receive command aliases.

OpenCode one-shot example:

```text
opencode run --command proposal "Draft a proposal for the requested change."
```

Do not use Codex `$skill` syntax for Claude Code or OpenCode. Claude Code one-shot CLI examples are intentionally omitted because no Claude one-shot form has been smoke-tested for this release.

## Learn More / Contribute

- Workflow detail: [docs/workflows.md](docs/workflows.md) and [specs/rigorloop-workflow.md](specs/rigorloop-workflow.md)
- Artifact and skill docs: [specs/README.md](specs/README.md) and [skills/](skills/)
- Report problems or feature ideas: [bug report template](.github/ISSUE_TEMPLATE/bug.yml) and [feature request template](.github/ISSUE_TEMPLATE/feature.yml)
- Review PR expectations before contributing: [.github/pull_request_template.md](.github/pull_request_template.md)

## Workflow At A Glance

RigorLoop recommends one standard workflow for complete AI-assisted delivery:

- Standing artifacts: `VISION.md` and `CONSTITUTION.md`
- Living references: `docs/project-map.md` when repository shape is not obvious enough for safe reliance
- Workflow infrastructure: specs, workflow summaries, affected root guidance, affected skills, and generated outputs
- On-demand support: `explore` and `research`
- Per-change chain: `proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review -> plan -> plan-review -> test-spec -> implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`
- Periodic learning: `learn`

`explore` and `research` run only when ambiguity, options, or current external facts matter. `learn` is periodic or explicitly invoked, not a final stage for every change. `ci-maintenance` means updating hosted workflow automation or related CI infrastructure; validation execution belongs to `verify`.

Do not rely on `docs/project-map.md` when it is absent, stale, contradicted, or missing the relied-on area; refresh it or record a no-map rationale first.

Users may manually invoke individual skills for focused output. A manual skill invocation is isolated by default and does not imply that the full workflow is complete.

The normative contract lives in [specs/rigorloop-workflow.md](specs/rigorloop-workflow.md). The short operational summary lives in [docs/workflows.md](docs/workflows.md).

## What This Repository Contains

- one recommended standard workflow for complete AI-assisted delivery
- isolated manual skill invocation for focused skill output
- standing artifacts, living references, on-demand support, a per-change chain, and periodic learning as distinct lifecycle categories
- canonical workflow sources in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`
- ignored local Codex runtime state in `.codex/skills/`
- generated public adapter packages in `dist/adapters/`
- a change-local artifact pattern under `docs/changes/<change-id>/` for the shipped example and later non-trivial work

## Change-Local Artifact Packs

- Manual skill invocations may omit `docs/changes/<change-id>/` when they are not used to claim complete workflow delivery.
- Ordinary non-trivial work uses the baseline pack: `docs/changes/<change-id>/change.yaml` plus `docs/changes/<change-id>/explain-change.md`.
- `review-resolution.md` and `verify-report.md` stay conditional and are added only when their governing workflow triggers apply.
- Approved legacy top-level explain artifacts under `docs/explain/` remain valid until migrated or retired.
- `docs/changes/0001-skill-validator/` is a rich reference example, not the minimum required pack for every non-trivial change.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated public adapter packages. Use `dist/adapters/README.md` for public adapter installation.
- `skills/` is the only authored skill source. `.codex/skills/` is ignored local Codex runtime state; keep it untracked when copying installed Codex adapter skills there for local runtime use, and edit canonical skills under `skills/`.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface.
- Public-surface token-cost benchmarks must identify generated public adapter output or release archive output, not repository-local `.codex/skills/`.
- Execution plans follow:
  - `docs/examples/plans/example-plan.md`

## Validation Commands

Before PR, run the same structural checks that CI runs:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>`
- `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3`

Use `bash scripts/ci.sh` to run the same checks through the repository-owned CI wrapper.

## Repository Layout

```text
.
├── AGENTS.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   ├── plan.md
│   ├── proposals/
│   ├── roadmap.md
│   ├── workflows.md
│   ├── changes/
│   │   └── 0001-skill-validator/
│   ├── examples/
│   │   └── plans/
│   │       └── example-plan.md
│   ├── plans/
│   ├── architecture/
│   └── adr/
├── .codex/
│   └── skills/
├── dist/
│   └── adapters/
├── scripts/
├── skills/
├── schemas/
└── specs/
```

The first shipped change-local artifact pack is `docs/changes/0001-skill-validator/`, and it should be read as a rich example rather than the universal minimum pack for every non-trivial change.

## License

This repository currently ships with the MIT license.
