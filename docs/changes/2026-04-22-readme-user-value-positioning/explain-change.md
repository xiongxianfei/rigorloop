# README user-value positioning

## Why this change exists

The public repository entrypoint was accurate but mechanics-first. It explained lifecycle structure before it clearly told a new visitor what RigorLoop does, why it is useful, who it is for, and how to evaluate fit.

This change implements the approved positioning contract by making `README.md` a value-first overview for first-time visitors while keeping workflow rules and validation requirements unchanged.

## What changed

- Rewrote the top of `README.md` so it now opens with:
  - the project title and a short value-focused tagline
  - an overview paragraph that names individual contributors first, keeps maintainers and small teams secondary, and states that RigorLoop does not replace Git, pull requests, CI, or human review
  - an exact `When to use / When not to use` section
  - a quick-start path that links to the workflow summary, normative workflow spec, and shipped proof-of-value example
  - a concise `Learn More / Contribute` section that points to truthful workflow, artifact/skill, and issue/PR surfaces
- Removed the stale `Current Focus` block and replaced rollout-era framing with durable shipped-state references.
- Added the baseline change-local metadata required for this non-trivial documentation slice.

## Scope control

- No workflow rules changed.
- No validation requirements changed.
- No source-of-truth ordering changed.
- No new standalone `CONTRIBUTING.md` was invented.
- The placeholder security contact under `.github/ISSUE_TEMPLATE/config.yml` was intentionally not surfaced as a README help path.

## Evidence and verification plan

The active plan and test spec require manual contract review plus focused repository checks over README headings, required links, stale wording removal, lifecycle validation, patch hygiene, and `bash scripts/ci.sh`.

Validation results and review/verify outcomes will be appended here and in `change.yaml` as the initiative moves through downstream stages.
