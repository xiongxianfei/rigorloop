# Subagent-Assisted Code Review

## Status

accepted

## Problem

RigorLoop code review is artifact-first and evidence-bound.
A formal review records review status, material findings, evidence, required outcomes, safe resolution paths, review records, review logs, review-resolution routing, milestone closeout state, remaining milestones, and readiness boundaries.

That single-reviewer model preserves accountability, but broad changes can span validators, generated outputs, release tooling, workflow specs, adapters, public packaging, security-sensitive surfaces, and lifecycle state.
One reviewer pass can miss specialized risks when the changed surface is wide.

The current safe fallback is for one reviewer to inspect every dimension manually.
That preserves a single reviewer of record, but it raises review cost and can reduce coverage on generated-output, release, security, compatibility, test-evidence, and workflow-state risks.

Modern agent platforms support a more focused review pattern.
Specialist subagents can inspect bounded surfaces and return structured evidence, while the main `code-review` skill remains the reviewer of record.
The missing RigorLoop decision is how to use subagents without fragmenting review authority or weakening lifecycle evidence.

## Goals

- Improve code-review coverage for broad or high-risk changes.
- Keep `code-review` as the single reviewer of record.
- Use subagents as read-only, bounded specialist reviewers.
- Select subagents from changed surfaces and risk classes, rather than running every possible reviewer every time.
- Require each selected subagent to return a structured review packet.
- Require the main reviewer to verify, deduplicate, classify, and record findings before they become canonical.
- Preserve the existing material-finding schema and review-resolution, re-review, milestone closeout, verify, and PR boundaries.
- Avoid letting subagents mutate code, apply fixes, or claim approval.
- Support Claude, Codex, and target-native agent environments without making one vendor-specific behavior authoritative.
- Add validation and fixture coverage for packet shape, aggregation, conflicts, missing required coverage, and advisory import behavior.

## Non-goals

- Do not replace the canonical `code-review` skill.
- Do not let subagents independently approve, block, or close a milestone.
- Do not use subagent consensus as a substitute for evidence.
- Do not require every code review to spawn multiple subagents.
- Do not let review subagents edit code, documentation, generated output, or review records.
- Do not auto-apply code-review findings as part of this proposal.
- Do not weaken existing code-review, review-resolution, verify, or PR gates.
- Do not send secrets, credentials, or private data to external services.
- Do not require live GitHub PR review for local RigorLoop code review.
- Do not make code review depend on Claude, Codex, or any single model vendor.
- Do not introduce background asynchronous review as part of the first contract.
- Do not hand-edit generated adapter output.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted work traceable, resumable, and reviewable in Git.
Subagent-assisted review fits that vision only if it improves coverage while keeping the final review result inspectable, evidence-bound, and owned by one canonical review artifact.

The proposal would conflict with the vision if subagents became independent approvers, bypassed material-finding evidence, created noisy unverified suggestion streams, or allowed verify or PR readiness to be inferred from subagent output alone.

## Context

This proposal builds on RigorLoop's existing review contract.
The code-review stage already focuses on material findings, evidence, required outcomes, safe resolution paths, and lifecycle-aware routing.
Formal review evidence remains durable and change-local when required.

The external process evidence supports bounded specialist review rather than unaggregated approval.
Claude Code documents subagents as specialized assistants with independent context, focused prompts, tool restrictions, permission controls, and model routing.
Codex GitHub review is positioned as a high-signal PR-diff review that follows repository guidance and focuses on serious issues.
Open-source review guidance emphasizes long-term code health, maintainability, testability, security, clear reviewer expectations, and explicit blocking rationale.

Sources consulted:

- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks-guide>
- Codex GitHub review integration: <https://developers.openai.com/codex/integrations/github>
- Codex GitHub review use case: <https://developers.openai.com/codex/use-cases/github-code-reviews>
- Google Engineering Practices code review standard: <https://google.github.io/eng-practices/review/reviewer/standard.html>
- GitLab code review guidelines: <https://docs.gitlab.com/development/code_review/>
- Rust compiler review policy: <https://forge.rust-lang.org/compiler/reviews.html>
- Kubernetes PR review guidance: <https://kubernetes.io/docs/contribute/review/reviewing-prs/>

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Use subagents as specialist evidence collectors rather than final approvers. | in scope | Recommended Direction |
| Keep the main code-review skill as reviewer of record. | in scope | Goals, Recommended Direction |
| Add an aggregator that verifies, deduplicates, and records final material findings. | in scope | Recommended Direction, Expected Behavior Changes |
| Select subagents based on changed surfaces and risk classes. | in scope | Recommended Direction, Scope Budget |
| Require structured subagent review packets. | in scope | Expected Behavior Changes, Testing and Verification Strategy |
| Preserve review-resolution, verify, and PR boundaries. | in scope | Goals, Non-goals |
| Keep subagents read-only by default. | in scope | Recommended Direction, Risks and Mitigations |
| Support Claude, Codex, and target-native environments without vendor lock-in. | in scope | Architecture Impact, Open Questions |
| Add validation and fixture coverage for packet aggregation behavior. | in scope | Testing and Verification Strategy |
| Decide whether packets are stored separately, whether Claude configs are packaged, and whether Codex review is required. | open question | Open Questions |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Core subagent-assisted review contract | core to this proposal | This is the central direction and ownership decision. |
| Specialist role vocabulary and selection rules | core to this proposal | Review coverage cannot be auditable without a bounded role and selection model. |
| Subagent review packet shape | core to this proposal | Aggregation depends on structured input rather than raw transcripts. |
| Aggregation and conflict rules | core to this proposal | The main reviewer needs an explicit method for promoting or rejecting subagent findings. |
| Code-review skill guidance update | same-slice dependency | The behavior belongs in the canonical review skill before implementation can rely on it. |
| Validation and fixture coverage | same-slice dependency | The closed packet and role model needs regression coverage. |
| Claude custom subagent configs | first-slice candidate | They may be useful, but the vendor-neutral contract should land first. |
| Codex/GitHub advisory import guidance | first-slice candidate | Advisory import should be specified without making GitHub review required. |
| Persistent packet file storage | deferable follow-up | The first version can record summarized coverage in the canonical review artifact. |
| Parallel subagent execution | deferable follow-up | Parallelism is an execution optimization after packet and aggregation behavior is stable. |
| Auto-applying fixes from review findings | out of scope | This would change the review role from judging to mutating. |

## Options Considered

### Option 1: Keep one monolithic code-review pass

This keeps the current review model simple and preserves a single reviewer of record.
It avoids packet schemas, subagent selection, and aggregation complexity.

The drawback is weaker specialist coverage on broad changes.
Generated-output, release, security, compatibility, and lifecycle-state issues can be easy to miss when one reviewer must inspect every dimension.

### Option 2: Let subagents directly write code-review findings

This would create fast fan-out and reduce aggregation work.
It also creates duplicated findings, inconsistent severity, unclear review status, and weak lifecycle accountability.

This option is rejected because it fragments review authority and makes the canonical review record harder to trust.

### Option 3: Require consensus among subagents

Consensus can reduce some false positives, but it is a poor fit for specialist review.
A security, release, or generated-output defect can be material even when other reviewers found nothing.

This option is rejected because evidence should decide materiality, not vote count.

### Option 4: Use subagents as specialist evidence packets with one canonical aggregator

This improves coverage while preserving one reviewer of record.
Subagents inspect bounded surfaces, return structured packets, and the main reviewer verifies evidence before accepting findings.

This is the recommended direction.

## Recommended Direction

Adopt subagent-assisted code review with one invariant:

```text
Subagents produce specialist review packets.
The code-review skill remains the only reviewer of record.
```

The main `code-review` skill should classify changed surfaces, select required specialists, provide bounded review packets, collect structured responses, reject malformed packets, verify evidence, remove duplicates, resolve conflicts, decide final severity, and record one canonical review artifact.

Subagents should have advisory statuses only:

- `findings`
- `no-findings`
- `inconclusive`

The canonical `code-review` skill remains responsible for review status such as `approved`, `changes-requested`, `blocked`, or `inconclusive`, according to the existing review contract.

Specialist roles should be selected from changed surfaces and risk markers.
Candidate recurring roles include:

| Subagent | Use when changed surface includes |
|---|---|
| `correctness-reviewer` | production code, validators, algorithms, or workflow logic |
| `test-evidence-reviewer` | tests, test specs, validation commands, or review evidence |
| `security-privacy-reviewer` | auth, secrets, network, file system trust boundaries, external services, or publication |
| `generated-output-reviewer` | generated skills, adapters, archives, or release artifacts |
| `migration-compatibility-reviewer` | schemas, storage, public APIs, CLI, or release/package behavior |
| `performance-concurrency-reviewer` | hot paths, parallelism, caching, async behavior, or subprocess orchestration |
| `docs-ops-reviewer` | README, docs, release notes, guides, or operational runbooks |

Subagents should be read-only by default.
Allowed operations should focus on reading files, searching files, inspecting diffs, inspecting validation logs, and running safe read-only diagnostics when explicitly permitted.
Editing, committing, pushing, publishing, modifying generated outputs, accessing secrets, or writing review records should stay outside the default subagent boundary.

The review artifact should record subagent selection, coverage, accepted findings, rejected or downgraded comments when relevant, and limitations.
Raw subagent transcripts should not be included unless needed as evidence.

## Expected Behavior Changes

- Code review can select specialist subagents for broad or risky changes.
- Subagents return structured review packets rather than free-form final approvals.
- The main code-review skill records one canonical review result.
- Review artifacts show which specialists ran, what they covered, what they did not cover, and which findings were accepted.
- One evidenced specialist finding can become a material finding without consensus from other subagents.
- Low-evidence suggestions are not promoted to material findings without independent confirmation.
- Direct code review without subagents remains supported.
- Claude and Codex outputs can be used as target-native advisory inputs, but the canonical RigorLoop artifact remains the lifecycle review record.

## Architecture Impact

Expected touched surfaces include:

| Surface | Expected impact |
|---|---|
| `skills/code-review/SKILL.md` | Add subagent-assisted review mode, selection rules, packet expectations, aggregation rules, and conflict handling. |
| `skills/code-review/assets/` | Add packet or coverage skeletons if the existing asset model supports them. |
| Review artifact validation | Validate role vocabulary, packet shape, coverage records, and malformed or missing required packet behavior. |
| Workflow guide | Summarize when subagent-assisted review is used and preserve direct review behavior. |
| Change metadata | Optionally record selected subagents and packet paths if persistent packet files are introduced. |
| Target adapters | Package updated public code-review skill guidance through the existing adapter release process. |
| Claude target | Optionally document or package custom read-only subagent configs for recurring roles. |
| Codex target | Optionally document advisory import or summarization guidance for PR-diff review output. |

An architecture assessment is recommended if implementation introduces a reusable orchestrator, persistent packet storage, target-specific subagent configuration generation, or new adapter packaging behavior.

## Testing and Verification Strategy

The spec and test spec should cover at least these proof points:

| Check ID | What is verified |
|---|---|
| `SUBCR-001` | Direct code review still works without subagents. |
| `SUBCR-002` | Release or package surfaces select generated-output and release/package specialists. |
| `SUBCR-003` | Security-sensitive surfaces select the security/privacy specialist. |
| `SUBCR-004` | Review subagents are read-only by default. |
| `SUBCR-005` | Malformed subagent packets are rejected. |
| `SUBCR-006` | Missing required specialist packets block or mark review incomplete. |
| `SUBCR-007` | The aggregator deduplicates overlapping findings. |
| `SUBCR-008` | One evidenced specialist finding can become a material finding without consensus. |
| `SUBCR-009` | Low-evidence suggestions are not promoted to material findings. |
| `SUBCR-010` | Review records list selected subagents, coverage, and limitations. |
| `SUBCR-011` | Subagent findings do not claim verify or PR readiness. |
| `SUBCR-012` | Codex or GitHub review output can be summarized as advisory evidence without replacing canonical review. |
| `SUBCR-013` | Claude subagent configs, if generated, use read-only permissions for review roles. |
| `SUBCR-014` | Existing review-resolution and code-review lifecycle validation remains green. |

Validation should include fixtures for valid packets, malformed packets, missing required coverage, duplicate findings, conflicting packets, no-finding packets, and advisory external review summaries.

## Rollout and Rollback

Rollout should start with the vendor-neutral review contract, packet schema, role vocabulary, and code-review skill guidance.
Direct code review remains available throughout the rollout.

The first implementation should record summarized subagent coverage in the canonical review artifact.
Separate packet files can be deferred unless audit volume or review readability makes them necessary.

Rollback is straightforward if direct review remains intact:

- Disable subagent-assisted mode.
- Preserve existing review records and coverage summaries as historical evidence.
- Remove packet-producing or packet-validating behavior only after no active workflow depends on it.
- Keep historical role names understandable for older review records.
- Do not weaken material-finding validation during rollback.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Subagents produce noisy comments. | The aggregator promotes only evidence-bound material findings and can summarize non-material observations separately. |
| Subagents disagree. | Evidence-based conflict resolution decides; a material risk with evidence can outweigh silence from other reviewers. |
| Review cost grows. | Select specialists by changed surface, cap default specialist count, and allow full specialist mode only by explicit request. |
| Subagents mutate files. | Keep review subagents read-only by default and prevent them from writing review records directly. |
| Lifecycle accountability blurs. | Keep `code-review` as reviewer of record and keep subagent statuses advisory. |
| Vendor lock-in grows. | Define a vendor-neutral packet contract; treat Claude and Codex as adapter-specific inputs. |
| Findings lose context. | Give each subagent bounded input with changed files, governing artifacts, non-goals, and review questions. |
| Security data leaks. | Exclude secrets and avoid external network or publication commands unless explicitly approved by a future contract. |
| Human reviewers overtrust agents. | Review records should show limitations and make clear that aggregation, not subagent output alone, owns materiality. |

## Open Questions

1. Should subagent packets be stored as separate files?
   Candidate answer: not initially.
   Record summarized subagent coverage in the canonical review artifact and add separate packet files only if packet volume or audit needs justify them.

2. Should Claude custom subagents be packaged for every reviewer role?
   Candidate answer: not initially.
   Add target-native configs only for high-value recurring roles after the vendor-neutral contract is stable.

3. Should Codex review be required for every PR?
   Candidate answer: no.
   Treat Codex review as optional advisory input or PR-surface enhancement, not a local workflow closeout requirement.

4. Should the same model run every specialist?
   Candidate answer: no requirement.
   Use the environment's available model routing while preserving packet shape and reviewer accountability.

5. Should subagents run in parallel?
   Candidate answer: allowed later.
   Parallelism is an execution optimization after packet schema, read-only boundaries, and aggregation behavior are stable.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-07-06 | Propose subagents as specialist evidence collectors. | This can improve coverage while preserving canonical review accountability. | Subagents independently approving reviews. |
| 2026-07-06 | Keep `code-review` as reviewer of record. | RigorLoop lifecycle evidence depends on one durable canonical review artifact. | Distributed unaggregated review comments. |
| 2026-07-06 | Make review subagents read-only by default. | Code review should judge the change, not mutate it. | Letting subagents patch code during review. |
| 2026-07-06 | Select specialists by changed surface and risk class. | This controls cost and noise while keeping coverage explainable. | Running every specialist every time. |
| 2026-07-06 | Treat Claude and Codex outputs as adapter-specific advisory inputs. | This avoids vendor lock-in and preserves the RigorLoop review contract. | Making one platform's review output authoritative. |

## Next Artifacts

- `proposal-review`
- `spec: subagent-assisted code-review`
- `spec-review`
- Architecture assessment if target-native subagent packaging, persistent packet storage, or reusable orchestration is introduced.
- `plan`
- `plan-review`
- `test-spec`
- `test-spec-review`
- Implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

## Follow-on Artifacts

- Proposal review R1: `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md`

## Readiness

Accepted and ready for `spec` by separate workflow or user request.

The open questions have candidate answers and did not block proposal review.
They should be settled in the follow-on spec before implementation.
