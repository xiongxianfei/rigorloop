# <PROJECT_NAME>

Replace this README with a project-specific introduction as soon as the repository has a real public purpose.

## Why this template exists

This template is designed for repositories that use Codex regularly and want less repeated setup work. It gives you:

- one place for durable repo instructions (`AGENTS.md`)
- a lightweight planning + spec structure for behavior-changing work
- GitHub community files so new repos start contributor-friendly
- CI and release workflows that are easy to adapt
- repo-local Codex skills for verification and release preparation

## First 15 minutes after creating a repo from this template

1. Rename the project and replace placeholder text.
2. Update `AGENTS.md` with the actual build, test, lint, and release commands.
3. Update `LICENSE`, `SECURITY.md`, and maintainer contact details.
4. Edit `docs/workflows.md` so it matches how your team actually works.
5. Replace `scripts/ci.sh` and `scripts/release-verify.sh` with repo-specific commands if needed.
6. Enable branch protection or rulesets for `main` and require the CI job from `.github/workflows/ci.yml`.
7. Delete any files you do not actually want to maintain.

## Template layout

```text
.
├── AGENTS.md
├── .codex/PLANS.md
├── .agents/skills/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   ├── plan.md
│   ├── roadmap.md
│   ├── workflows.md
│   └── plans/
├── scripts/
└── specs/
```

## Suggested repository settings

- default branch: `main`
- require pull requests before merge
- require the `ci` status check
- require one approval for external-facing changes
- disable force pushes to protected branches
- use squash merge unless your project has a strong reason not to

## Suggested follow-up for organizations

If you own many repositories, also create a public `.github` repository with default community health files and workflow templates, then keep only repo-specific differences here.

## License

This template ships with the MIT license text as a placeholder. Change it if your project needs a different license.
