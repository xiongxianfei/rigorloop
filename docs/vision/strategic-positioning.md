# Strategic Positioning

`VISION.md` is the canonical project-vision artifact. This file is supporting rationale for how the current project vision was derived. If this rationale conflicts with `VISION.md`, update this rationale or revise `VISION.md` through a substantive vision update; do not treat this file as independently authoritative.

## Category

A rigorous software engineering workflow for AI coding agents.

## Primary User

Individual contributors, maintainers, and teams that want AI agents to participate in serious software delivery without weakening engineering discipline.

## Primary Pain

AI agents can produce code faster than reviewers can safely understand the purpose, governing requirements, design constraints, tests, validation evidence, and review concerns behind the change.

## Primary Promise

RigorLoop makes AI-assisted changes reviewable, traceable, and reproducible enough that humans can approve, challenge, or maintain them with confidence.

## Core Mechanism

The workflow turns product intent into explicit proposals, requirements, test specifications, architecture decisions, execution plans, implementation, validation evidence, review records, and change explanations.

## Alternatives

Teams would otherwise rely on ordinary AI coding chats, ad hoc PR descriptions, generic project-management process, or tool-specific agent runtimes that optimize for output speed without durable engineering rationale.

## Tradeoff

RigorLoop accepts more explicit artifacts and review gates in exchange for stronger confidence that agent-produced changes match human-approved intent.

## Compatibility Surfaces

Git, CI, pull requests, repository-local artifacts, generated adapter packages, and common agent runtimes are compatibility surfaces. They support the workflow but are not the project category.

## Refusals

RigorLoop refuses to become a generic project-management suite, hosted control plane, vendor-specific agent runtime, replacement for engineers or reviewers, or a system that rewards code volume without evidence.

## Falsifiability

The vision is wrong if reviewers cannot reconstruct a representative change's purpose, requirements, design constraints, tests, validation evidence, and review concerns from tracked artifacts without chat history. It is also wrong if teams routinely ignore the artifacts because they slow delivery without improving review quality, or if useful adoption requires a platform migration.
