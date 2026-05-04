# Learn Artifact Namespace

This directory is the canonical namespace for learn artifacts.

## Surfaces

- `docs/learn/sessions/YYYY-MM-DD-<slug>.md` holds raw historical session records. The session record is the primary output of any learn invocation that reaches Frame, including empty sessions and sessions with no durable lesson.
- `docs/learn/topics/<topic>.md` holds curated durable topic guidance. A topic file exists only when at least one contributor-confirmed durable lesson justifies it.

## Sessions

Session records preserve the historical thread for a learn run. They record trigger, trigger type, scope, evidence reviewed, exclusions, prior learnings, observations, classification decisions, routing results, derivative artifact links, and no-learn rationale when applicable.

## Topics

Topic files are curated guidance, not authoritative workflow, product, architecture, validation, skill, implementation, or decision contracts.

They may summarize confirmed durable lessons and point to the session record and action-owning artifacts that explain the source. They must not override higher-priority artifacts such as `CONSTITUTION.md`, approved specs, ADRs, architecture docs, workflow docs, skill files, accepted proposals, active plans, or the artifact that owns a behavior change.

Topic entries may be added, superseded, removed, revised, or absorbed into an authoritative artifact. When curation must remove, revise, or absorb an entry, preserve traceability through a session link, authoritative-artifact link, topic-file rationale, or explain-change rationale.

## Actions

Lessons that change behavior, workflow, validation, architecture, skill behavior, examples, or decisions belong in the action-owning artifact. The session record links to the change. A topic entry may summarize it for discovery, but it is not the source of truth.

## Initial Structure

No templates are defined here. No empty topic taxonomy is pre-created. Create session records and topic files only when a learn session produces them under the approved workflow.
