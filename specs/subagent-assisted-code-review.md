# Subagent-Assisted Code Review

## Status

approved

## Related proposal

- [Subagent-Assisted Code Review](../docs/proposals/2026-07-06-subagent-assisted-code-review.md), accepted.
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-07-06-subagent-assisted-code-review/reviews/proposal-review-r1.md), approved with no material findings.

## Goal and context

RigorLoop code review remains a single canonical lifecycle review, but broad changes can require specialist evidence across generated output, release packaging, security, compatibility, test evidence, performance, workflow state, and documentation.

This spec defines the contract for subagent-assisted code review.
Subagents may widen review coverage by returning bounded advisory packets.
The `code-review` skill remains reviewer of record, verifies any evidence before promotion, and records one canonical review artifact.

The first implementation of this contract records summarized subagent coverage inside the canonical code-review record.
It does not require persistent raw packet files, target-native Claude subagent packaging, mandatory Codex review, parallel execution, or auto-fix behavior.

## Glossary

- `subagent`: A specialist reviewer context that inspects a bounded review packet and returns structured advisory output.
- `reviewer of record`: The canonical `code-review` skill invocation that owns final review status, material findings, review-log entries, and downstream routing.
- `coordinator`: The `code-review` behavior that classifies changed surfaces, selects specialists, prepares bounded inputs, and collects subagent packets.
- `aggregator`: The `code-review` behavior that validates packets, verifies evidence, deduplicates comments, resolves conflicts, and decides what becomes a canonical material finding.
- `subagent review packet`: A structured advisory output from a selected specialist reviewer.
- `subagent input packet`: The bounded context and instructions given to one selected specialist reviewer.
- `changed surface`: A changed path, artifact type, behavior class, or risk class used for specialist selection.
- `specialist role`: A closed vocabulary value identifying a subagent review focus.
- `advisory status`: A subagent packet status of `findings`, `no-findings`, or `inconclusive`.
- `canonical review status`: A `code-review` result status owned by the reviewer of record.

## Examples first

### Example E1: direct code review without subagents still works

Given a small docs-only change has no specialist trigger beyond ordinary review
When `code-review` runs without selecting subagents
Then it records the canonical review using the existing review artifact contract.

### Example E2: generated-output change selects specialists

Given a change touches adapter archive generation and validation fixtures
When `code-review` classifies changed surfaces
Then it selects generated-output, release/package, correctness, and test/evidence review coverage unless a bounded cap requires a recorded omission rationale.

### Example E3: a security finding does not need consensus

Given `security-privacy-reviewer` returns an evidenced finding about unsafe token exposure
And other subagents return `no-findings`
When the aggregator verifies the evidence and materiality
Then the canonical review can record a material finding without subagent consensus.

### Example E4: low-evidence suggestion is not promoted

Given a subagent returns a readability suggestion without evidence of contract, security, release, workflow, or maintainability impact
When the aggregator evaluates the packet
Then the suggestion is not promoted to a material finding.

### Example E5: malformed required packet blocks review completion

Given a required specialist packet is malformed or missing
When the aggregator cannot safely reconstruct the reviewed scope and status
Then canonical code review records `blocked` or `inconclusive` instead of treating the missing packet as a clean result.

### Example E6: Codex PR review remains advisory

Given a Codex GitHub review comment stream exists for the PR
When RigorLoop code-review consumes that output
Then it may summarize the output as advisory evidence, but only the canonical `code-review` artifact owns lifecycle review status.

### Example E7: subagent-assisted mode records coverage

Given subagent-assisted review runs for a broad workflow change
When the canonical review is recorded
Then the review artifact lists selected subagents, status, reviewed scope, accepted findings, rejected or downgraded comments when relevant, and limitations.

## Requirements

R1. The `code-review` skill MUST remain the reviewer of record for formal RigorLoop code review.

R1a. Subagents MUST NOT approve, block, close, or mark milestones directly.

R1b. Subagents MUST NOT write canonical review records, review-log entries, review-resolution entries, verify results, or PR readiness claims directly.

R1c. Subagent output MUST be advisory until the aggregator verifies and promotes it into the canonical review record.

R2. Subagent-assisted code review MUST preserve direct code review without subagents.

R2a. The absence of selected subagents MUST NOT by itself make a review incomplete when no selection trigger applies.

R2b. Direct review output MUST continue to use the existing formal review recording and material-finding contract.

R3. The specialist role vocabulary MUST be closed.

R3a. The initial role vocabulary MUST include:

| Role | Review focus |
|---|---|
| `correctness-reviewer` | Contract compliance, algorithms, validators, and workflow logic. |
| `test-evidence-reviewer` | Test coverage, test specs, validation commands, fixtures, and evidence ownership. |
| `security-privacy-reviewer` | Secrets, auth, authorization, trust boundaries, external services, publication, and unsafe inputs. |
| `generated-output-reviewer` | Generated skills, adapter output, archives, release artifacts, and source-derived parity. |
| `migration-compatibility-reviewer` | Schemas, storage, public APIs, CLI behavior, release/package compatibility, and migration expectations. |
| `performance-concurrency-reviewer` | Hot paths, parallelism, caching, async behavior, subprocess behavior, cost, and determinism. |
| `docs-ops-reviewer` | README, docs, release notes, guides, runbooks, user-facing commands, and operational accuracy. |

R3b. Unknown specialist role values MUST fail closed before selection, packet validation, or aggregation continues.

R4. Subagent selection MUST be derived from changed surfaces and risk markers.

R4a. The coordinator MUST record selected specialists and the changed surfaces or risk markers that triggered them.

R4b. The coordinator MUST record non-selected high-value specialists with omission rationale when their omission could otherwise look like under-review.

R4c. The coordinator MUST support a bounded default specialist count.

R4d. When more specialists are triggered than the default cap permits, the coordinator MUST record which specialists ran, which specialists were omitted or folded into another review, and why the resulting coverage remains acceptable or incomplete.

R4e. A manual full-specialist mode MAY run more specialists than the default cap only when the review record says full-specialist mode was used.

R5. Selection rules MUST cover common changed surfaces.

R5a. Changes to validators, algorithms, workflow logic, or production behavior MUST select `correctness-reviewer`.

R5b. Changes to tests, test specs, fixtures, validation commands, or evidence records MUST select `test-evidence-reviewer`.

R5c. Changes involving secrets, authentication, authorization, permissions, file-system trust boundaries, external services, network behavior, package publication, or unsafe external input MUST select `security-privacy-reviewer`.

R5d. Changes to generated skills, adapters, archives, release artifacts, or generated-output validation MUST select `generated-output-reviewer`.

R5e. Changes to schemas, storage, public APIs, CLI behavior, release/package compatibility, or migrations MUST select `migration-compatibility-reviewer`.

R5f. Changes to hot paths, parallel execution, caching, async behavior, subprocess orchestration, or deterministic aggregation MUST select `performance-concurrency-reviewer`.

R5g. Changes to README, docs, release notes, guides, or operational runbooks MUST select `docs-ops-reviewer`.

R6. Subagent input packets MUST be bounded.

R6a. Each input packet MUST identify review ID, change ID when present, milestone when present, specialist role, changed files or review scope, governing artifacts, must-check items, must-not actions, and expected output format.

R6b. Each input packet MUST exclude secrets, credentials, private keys, and unrelated private data.

R6c. Each input packet MUST tell the specialist not to edit files, approve milestones, claim verify readiness, claim PR readiness, or review unrelated code.

R6d. Each input packet SHOULD include known non-goals and relevant open questions when they affect review judgment.

R7. Review subagents MUST be read-only by default.

R7a. Default allowed operations are reading files, searching files, inspecting diffs, inspecting validation logs, and running explicitly allowed safe read-only diagnostics.

R7b. Default disallowed operations include editing files, writing review records, committing, pushing, publishing, modifying generated outputs, running destructive commands, running publication commands, accessing secrets, or using external network access.

R7c. Any environment-specific tool permission model MUST preserve the read-only review boundary or record that subagent-assisted mode is unavailable in that environment.

R8. Subagent review packets MUST be structured.

R8a. Packet schema version MUST be `subagent-review-packet-v1` for this spec's first implementation.

R8b. Each packet MUST include review ID, subagent role, advisory status, reviewed scope, checked coverage, not-checked coverage, findings, no-finding rationale when status is `no-findings`, and limitations.

R8c. Advisory status MUST be one of `findings`, `no-findings`, or `inconclusive`.

R8d. Unknown packet schema versions, unknown roles, unknown statuses, missing required fields, malformed findings, or unverifiable reviewed scope MUST fail closed.

R9. Subagent findings MUST be evidence-bearing before promotion.

R9a. Each subagent finding MUST include title, severity recommendation, location or review surface, evidence, required outcome, safe resolution path or needs-decision rationale, and confidence.

R9b. The aggregator MUST verify evidence paths and claims before promoting a subagent finding to a canonical material finding.

R9c. The aggregator MUST NOT promote a low-confidence suggestion to a material finding without independent inspectable evidence.

R9d. A finding MAY become canonical without consensus when one specialist provides verified material evidence.

R10. The aggregator MUST own deduplication, conflict handling, severity, and promotion.

R10a. The aggregator MUST reject malformed packets.

R10b. The aggregator MUST deduplicate overlapping findings before recording canonical material findings.

R10c. The aggregator MUST resolve conflicting subagent conclusions by inspecting evidence rather than counting votes.

R10d. The aggregator MUST decide final canonical severity under the existing material-finding contract.

R10e. The aggregator MUST record conflict, evidence inspected, final decision, and reason when a material subagent conflict affects review outcome.

R11. Canonical review records MUST record subagent coverage when subagent-assisted mode runs.

R11a. The review record MUST list selected subagents, advisory status, reviewed scope, accepted findings count, rejected or downgraded comments count when relevant, and limitations.

R11b. The review record MUST identify missing or inconclusive required specialist coverage when it affects canonical review status.

R11c. The review record SHOULD summarize rejected or downgraded subagent comments only when doing so helps later reviewers understand materiality decisions.

R11d. Raw subagent transcripts SHOULD NOT be embedded in canonical review records unless needed as evidence.

R12. Missing or inconclusive required specialist coverage MUST affect canonical review status.

R12a. A missing required packet MUST cause canonical code review to return `blocked` or `inconclusive` unless the coordinator records a safe substitute coverage rationale.

R12b. An inconclusive required packet MUST cause canonical code review to return `blocked` or `inconclusive` when the missing coverage is material to the changed surface.

R12c. A malformed required packet MUST be rejected and treated as missing coverage until rerun or replaced by recorded safe substitute coverage.

R13. Subagent-assisted review MUST preserve existing lifecycle gates.

R13a. Material findings MUST still use the standard evidence, required outcome, and safe resolution path or needs-decision rationale.

R13b. Material findings MUST still trigger review-resolution according to the existing workflow contract.

R13c. Subagent output MUST NOT claim branch readiness, verify readiness, PR-body readiness, or PR-open readiness.

R13d. Verify and PR readiness MUST NOT be inferred from subagent output alone.

R14. External review output MUST be advisory unless imported into the canonical review record.

R14a. Codex GitHub review output MAY be summarized as advisory review evidence.

R14b. GitHub comment streams, Codex review comments, Claude subagent output, or other target-native review output MUST NOT replace the canonical RigorLoop code-review artifact.

R14c. Imported advisory output MUST identify source, scope, limitations, and any findings promoted or rejected by the aggregator.

R15. Target-native subagent configuration is optional in the first implementation.

R15a. The first implementation MUST NOT require packaged Claude custom subagents for every reviewer role.

R15b. If Claude custom subagent configs are shipped, review roles MUST use read-only permissions and preserve the same packet contract.

R15c. If target-native configs are not shipped, the vendor-neutral packet and review-record contracts MUST still be usable.

R16. Persistent separate packet files are not required in the first implementation.

R16a. The first implementation MAY record summarized subagent coverage only in the canonical review artifact.

R16b. If later work stores packet files separately, packet paths, retention behavior, and privacy boundaries MUST be specified before implementation.

R17. Parallel subagent execution is not required in the first implementation.

R17a. Subagents MAY run sequentially.

R17b. Parallel execution MAY be added only after packet validation, read-only tool boundaries, and deterministic aggregation behavior are specified and covered by tests.

R18. Subagent-assisted review MUST not add new dependencies unless justified by a follow-on spec or architecture artifact.

R18a. Existing repository scripts, skill guidance, validators, and standard runtime SHOULD be preferred for packet validation and review-record validation.

## Inputs and outputs

Inputs:

- changed files, staged diff, commit range, PR diff, or other review surface;
- accepted proposal, approved spec, active test spec, active plan, architecture records, review-resolution records, validation evidence, and other governing artifacts when present;
- configured specialist selection rules;
- optional target-native advisory review output.

Outputs:

- canonical code-review record;
- review-log entry;
- review-resolution record when material findings or blocking outcomes require it;
- subagent coverage section when subagent-assisted mode runs;
- optional summarized advisory import notes.

## State and invariants

- The canonical `code-review` result remains the only lifecycle review result.
- Subagent status is advisory and cannot close or block lifecycle state by itself.
- Unknown specialist roles and unknown packet statuses fail closed.
- A single verified specialist finding can become a canonical material finding.
- Missing required specialist coverage is not silently treated as a clean review.
- Direct review without subagents remains a supported path.

## Error and boundary behavior

- Unknown role: reject selection or packet and return blocked or inconclusive when required coverage is affected.
- Unknown status: reject packet and return blocked or inconclusive when required coverage is affected.
- Missing required packet: block or mark inconclusive unless safe substitute coverage is recorded.
- Malformed packet: reject packet and rerun or record safe substitute coverage before clean review.
- Low-evidence comment: do not promote; optionally summarize as non-material if useful.
- Conflicting packets: inspect evidence and record final aggregation decision when material.
- External advisory review unavailable: continue direct review unless an explicit future contract makes that advisory source required.

## Compatibility and migration

Existing direct code-review workflows remain valid.
Existing review records without subagent coverage remain valid historical records.

The first implementation should update `skills/code-review/SKILL.md`, related code-review assets if needed, validators, fixtures, workflow guidance when affected, and generated adapter packaging through the existing release process.
Generated public adapter skill bodies must not be hand-edited.

The change is compatibility-sensitive because it affects public review behavior, workflow guidance, validation, and potentially generated adapter output.
Rollback should disable subagent-assisted mode while preserving direct code review and historical coverage summaries.

## Observability

Canonical review records must expose:

- selected specialists;
- changed surfaces or risk markers that drove selection;
- missing or omitted specialists and rationale when relevant;
- packet advisory statuses;
- accepted findings;
- rejected or downgraded comments when relevant;
- limitations;
- conflict decisions when material.

Validation output should identify malformed packets, unknown role values, unknown status values, missing required coverage, duplicate finding collapse, and coverage-section shape errors.

## Security and privacy

Subagent input packets must exclude secrets, credentials, private keys, unrelated private data, and unnecessary external context.

Subagents are read-only by default.
Network, publication, secret access, destructive commands, repository writes, commits, pushes, and generated-output mutation are outside the default review boundary.

External advisory review output can be consumed only as imported evidence and must not become the lifecycle source of truth.

## Accessibility and UX

Not applicable to end-user UI.

Reviewer-facing records must remain concise enough to scan.
Subagent coverage tables should summarize coverage and limitations without embedding raw transcripts by default.

## Performance expectations

The default selection model should avoid running every specialist for every review.

Implementations should support a bounded default specialist count and bounded packet output size.
Parallel execution is not required for the first implementation.

## Edge cases

EC1. Direct review runs on a small change with no specialist triggers.

EC2. A changed surface triggers more specialists than the default cap.

EC3. A required specialist packet is missing.

EC4. A required specialist packet is malformed.

EC5. A subagent uses an unknown role.

EC6. A subagent uses an unknown advisory status.

EC7. Two subagents report the same underlying finding.

EC8. One subagent reports a material security finding while others report no findings.

EC9. A subagent reports a low-evidence style suggestion.

EC10. A target-native Codex or GitHub review exists but is not imported into the canonical review.

EC11. Claude custom subagent configs are absent.

EC12. Persistent packet files are absent.

EC13. A docs-only change defines commands or contracts that need docs/ops review but no production-code specialist.

EC14. A generated-output change also affects release-package compatibility.

## Non-goals

- Replacing the canonical `code-review` skill.
- Letting subagents independently approve, block, or close milestones.
- Making subagent consensus a substitute for evidence.
- Requiring subagents for every review.
- Allowing review subagents to edit files or review records.
- Auto-applying code-review findings.
- Requiring live GitHub PR review for local RigorLoop closeout.
- Requiring Claude, Codex, or any single vendor.
- Introducing background asynchronous review.
- Requiring persistent raw packet files in the first implementation.
- Requiring parallel subagent execution in the first implementation.
- Hand-editing generated adapter output.

## Acceptance criteria

AC1. Direct code review without subagents remains supported.

AC2. The reviewer of record remains canonical `code-review`.

AC3. A closed specialist role vocabulary exists and unknown role values fail closed.

AC4. Changed-surface selection records selected specialists and omission rationale when relevant.

AC5. Subagent input packets are bounded and read-only by default.

AC6. Subagent review packets use `subagent-review-packet-v1` and unknown statuses fail closed.

AC7. Malformed, missing, or inconclusive required packets block or mark canonical review incomplete unless safe substitute coverage is recorded.

AC8. The aggregator verifies evidence before promoting subagent findings.

AC9. Duplicate subagent findings are deduplicated before canonical recording.

AC10. One evidenced specialist finding can become a material finding without consensus.

AC11. Low-evidence suggestions are not promoted to material findings without independent evidence.

AC12. Review records list selected subagents, coverage, accepted findings, relevant rejected comments, and limitations.

AC13. Subagent findings do not claim verify or PR readiness.

AC14. Codex or GitHub review output remains advisory unless imported and summarized by the canonical review.

AC15. Claude custom configs, if shipped, preserve read-only permissions and the packet contract.

AC16. Existing review-resolution, verify, and PR readiness boundaries remain unchanged.

## Open questions

None.

The proposal's candidate answers are settled in this spec:

- separate packet files are not required initially;
- Claude custom subagent configs are not required for every role initially;
- Codex review is optional advisory input;
- model routing is environment-specific;
- parallel subagent execution is deferred.

## Next artifacts

- `spec-review`
- Architecture assessment
- `plan`
- `plan-review`
- `test-spec`
- `test-spec-review`
- Implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

## Follow-on artifacts

- Spec review R1: `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md`

## Readiness

Approved and ready for architecture assessment.
