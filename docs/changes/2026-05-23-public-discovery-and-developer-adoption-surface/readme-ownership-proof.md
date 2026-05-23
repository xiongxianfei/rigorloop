# README Ownership Proof

## Purpose

Record README generated-region boundaries and safe edit zones before the README
adoption-surface implementation milestone.

## Generated or owned regions inspected

- File: `README.md`
- Generated marker start: `<!-- vision:start -->`
- Generated marker end: `<!-- vision:end -->`
- Evidence command: `rg -n "<!-- vision:start -->|<!-- vision:end -->|^# |^## |@xiongxianfei/rigorloop@|source of truth|Source of Truth|When to use / When not to use" README.md`
- Evidence result:
  - `README.md:3`: `<!-- vision:start -->`
  - `README.md:11`: `<!-- vision:end -->`
  - `README.md:17`: `## When to use / When not to use`
  - `README.md:31`: `## Quick Start`
  - `README.md:119`: `## Vision and README Ownership`
  - `README.md:222`: `## Source Of Truth`

## Ownership decision

- The region from `README.md:3` through `README.md:11` is generated from `VISION.md`.
- M2 must not hand-edit generated vision content unless it updates the owning source or generator.
- Current M2 first-contact edits should target direct README-owned regions outside the generated block unless a later owner decision changes `VISION.md`.
- Quick Start examples at `README.md:42` and `README.md:87` are outside the generated block and may be updated directly in M2.

## Validation

- Command: `python scripts/validate-readme.py README.md --vision-markers`
- Result:
  - `README validation passed: README.md`
  - `Vision marker validation passed: one standalone marker block present`

## Contradiction checks

- `VISION.md` remains the canonical project-vision artifact.
- README front-matter is not the source of truth when it conflicts with `VISION.md`.
- `specs/readme-user-value-positioning.md` remains the approved README ordering contract.
- M1 did not edit `README.md`, so no generated-region contradiction was introduced in this milestone.

## Follow-up for M2

M2 must update README adoption-surface content outside the generated region or
update the owning source if generated content needs to change. M2 must preserve
the near-top `When to use / When not to use` value-first ordering before
mechanics/reference content.

## M2 ownership result

- Edited file: `README.md`
- Edited regions:
  - Direct README-owned Quick Start and npm usage examples outside
    `<!-- vision:start -->` through `<!-- vision:end -->`.
  - Direct README-owned near-top link group after Quick Start.
  - Direct README-owned `Lifecycle At A Glance` Mermaid section.
  - Direct README-owned `Learn More / Contribute` link list.
- Generated-region edits: none.
- Owning source updates required: none.
- Contradiction result:
  - The generated vision block remains unchanged.
  - The first audience-facing direct README sentence still names individual
    contributors first.
  - `When to use / When not to use` remains before Quick Start, npm usage, and
    mechanics/reference content.
  - The lifecycle caption preserves the manual skill invocation boundary from
    `CONSTITUTION.md`.
- M2 validation command: `python scripts/validate-readme.py README.md --vision-markers`
- M2 validation result: passed.
