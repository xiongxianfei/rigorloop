---
name: project-map
version: "0.0.0-test"
schema-version: skill-readability-v1
description: >
  Build, refresh, or audit a current-state repository orientation map with
  cited evidence, bounded inference, known gaps, and durable root or area scope.
argument-hint: [repository, area, orientation question, or refresh scope]
---

# Project map contract fixture

## Workflow role

- role_name: project-map
- stage: support
- upstream: current repository state, project-local guidance, and the user's orientation question
- downstream: explore, proposal, architecture, or workflow routing
- summary: Creates, refreshes, or audits a current-state repository orientation map.

## Operating modes

- `create`
- `refresh`
- `area`
- `audit`

## Map metadata and freshness

Required metadata fields:

- Map status
- Scope
- Baseline
- Last reviewed
- Coverage
- Exclusions
- Parent map
- Known gaps

Allowed map statuses:

- current
- partial
- stale

## Evidence and confidence

Evidence classes:

- observed
- inferred
- unknown

Material claim example: a claim that identifies an entry point, trusted boundary,
runtime flow, data flow, test surface, CI surface, or downstream reliance point
must cite a repository path.

Incidental statement example: a sentence that only names the map purpose or
scope does not need a citation.

## Root and area maps

Every area map must be registered from the root map.

| Area | Map | Scope | Baseline | Freshness | Known gaps |
| --- | --- | --- | --- | --- | --- |
| <area> | <path> | <scope> | <baseline> | <freshness> | <known gaps> |

## Required output structure

- Map metadata
- Purpose and scope
- System overview
- Repository layout
- Runtime flow
- Data flow
- External boundaries
- Test map
- CI and release map
- Architecture rules observed
- Risk areas
- Open questions
- Area maps

## Resource map

- COPY `assets/project-map-skeleton.md` when creating a new root or area project map.
  Fill: metadata fields, applicable sections, evidence paths, known gaps, and area registration fields.
  Do not emit unfilled placeholders.

## Expected output

- Project map contract fixture diagnostics.

## Output skeleton

```md
- Skill: project-map
- Status: <created|updated|audited|blocked>
- Mode: <create|refresh|area|audit>
- Map scope: <repository|area:slug>
```
