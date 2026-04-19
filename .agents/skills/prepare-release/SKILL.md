---
name: prepare-release
description: Prepare a release for a repository that already has a defined release process. Use when the user asks to get a repo release-ready, draft release notes, verify release readiness, or clean up release tasks. Do not use to invent a release process from scratch when the repository already documents one.
---

Follow this workflow:

1. Read `AGENTS.md`, `docs/workflows.md`, and any release-specific docs first.
2. Inspect `.github/workflows/` and release scripts to find the real release path.
3. Summarize the release contract before changing files.
4. Verify readiness with the smallest relevant checks first.
5. Update release notes, docs, or version metadata only when the documented process requires it.
6. State exactly what was verified and what remains manual.

Keep release preparation separate from feature work whenever possible.
