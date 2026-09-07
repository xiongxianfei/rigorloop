# Record Format and targeted recording Design rereview

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: `workflow` = `docs/design/workflow.md`; `cli` = `docs/design/cli.md`; `record-format` = `docs/design/record-format.md`. Each is one combined requirements/architecture model; no separate ADR member applies.
- Upstream review ID: `proposal-review-r1`, at `docs/changes/2026-09-07-targeted-recording-primary-cli-review-recording/reviews/proposal-review-r1.md`.
- Review ID and round: `record-format-design-rereview`, first review of this exact three-model revision.
- Material findings: RF-DR-001.
- Correction targets: `cli`, Design authoring.
- Recording status: recorded, advisory-durable.
- Settlement status: withheld.
- Open blockers: RF-DR-001; formal settlement also lacks a selected governed change and exact package settlement context.
- Immediate next stage: isolated stop; the CLI Design author owns the identified correction.
- Claim limitations: independent substantive review of the exact three-model package only. No lifecycle settlement, Delivery eligibility, implementation authorization, runtime verification, activation or release readiness is established.

## Finding RF-DR-001

- Finding ID: RF-DR-001
- Severity: medium
- Location: `docs/design/cli.md`, Primary result schema, diagnostics and preview (line 258), and Bounded storage receipt and diagnostic detail (lines 274–278).
- Evidence: The observation identity hashes exactly `{schema_version: 1, revision, observations}`. The returned diagnostic contains code, safe message and applicable locations; neither its required fields nor its fixed safe message template must include the actual observed subject identity. Nevertheless, line 278 promises that a changed observed external subject produces conflict. Consider a retained subject identity A, with actual bytes having identity B during the first diagnostic scan. Before continuation, an external edit changes those bytes to C, also different from A. The registered record revision is unchanged. Both scans may correctly return the same `subject-drift` code, location and fixed message that the recorded subject differs from current content. All explicitly defined hash inputs are then identical, so the expected observation identity still matches and continuation can succeed despite the promised conflict. This is a missing identity input, not a cryptographic collision or an unsupported edit during publication. The edit occurs between diagnostic reads.
- Required outcome: Make the exact digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves diagnostic category, location and message. Preserve the bounded receipt and safe diagnostic representation; do not require diagnostic detail as a write prerequisite.
- Safe resolution path: The CLI Design author should bind the observation identity to a precisely defined, deterministically ordered set of observed external path/identity pairs, including explicit absence, or require an equivalent identity-bearing diagnostic representation. Specify how the same basis is reconstructed by candidate scans and current reads, and add an acceptance case where an already-drifted subject changes again while the registered revision stays constant. Alternatively, explicitly narrow the promise to diagnostic-content stability and document that changed subject bytes can retain the same diagnostic identity; that is a Design decision and must reconcile CLI-SR-14/20 and the temporal acceptance wording. Independently rereview the exact package after correction.
- needs-decision rationale: none for preserving the currently promised external-basis freshness; narrowing that promise would need an explicit Design decision.
- Finding scope: artifact-local
- Affected artifact IDs: cli
- Owning stages: Design authoring.

## Package assessment

The primary v2 creation rule and retained v1 compatibility now have distinct scopes. Primary new-root creation explicitly selects v2 after coordinated activation; existing v1 roots retain compatible operations, and advanced v1 creation remains a separately identified compatibility facility. Workflow explicitly requires reviewed governance, runtime, schemas, skills and adapter changes before activation. The current executable v1 guidance is therefore not evidence that the prospective v2 creation policy contradicts its adoption boundary.

The newly added `record_contract` field supports the requested first-write interaction. Status, context and change-scoped show report the manifest discriminator alongside the revision from the same snapshot, even for no selected entries or a continuation page. Absent roots return null contract/revision and invalid stores do not synthesize a value. The actor can submit those returned values with its explicit decision and separately inspected subject basis. Freshness is rechecked at mutation time.

The receipt design separates a bounded storage result from diagnostic detail. Its finite changed-target/count representation fits the stated reserve, optional expansion can be explicitly omitted, and successful publication cannot become a false rejection because stdout delivery failed. Advanced recording receives a corresponding bounded aggregate fallback without a new v1 diagnostic enum. RF-DR-001 concerns the retrieval freshness guarantee, not the core decision to prevent diagnostic volume from blocking correction.

Normal `verify show`, `decisions show` and their full context selectors expose complete narratives with identities and applicability. Unregistered, registered-missing and malformed records have distinct outcomes. These reads avoid unrelated record bodies and do not claim renewed verification. Review-context omission of findings remains explicit; full review show retains them.

Record Format now owns the complete durable layouts and common types, while Workflow owns decisions and CLI owns construction and publication. Immutable concern origin retains the original reporter, subjects, evidence, required outcome and rationale, with an explicitly absent or embedded supporting judgment. Later current assessments preserve it; advanced replacement and recovery share preservation obligations. This supports understanding an unresolved concern without prior review rounds or chat while preserving the need to inspect current engineering subjects before disposition.

The purpose-specific catalogue, batch final-candidate validation, source-span preservation, revision checks before no-op recognition, declared decision basis and exact-byte recovery form a coherent recording architecture. Findings and change-level blockers retain distinct targets and reporter/correction responsibilities. A failed Verify and new blocker can be recorded after completed work, with Route acting in a later transaction. No additional material finding was identified in these boundaries. The earlier TR-DR-001 query-shape issue remains addressed in this revision.

All eight dimensions are allocated in each model. Delivery still must prove preservation, concurrency/recovery, closed-schema rejection, supported consumer adoption and complete-interaction token effects. These are explicit downstream proof obligations, not runtime claims established by this document review. A few residual phrases still call shared types “Workflow types” or refer to the earlier v1 placement description; the authoritative model-boundary and adoption clauses resolve their scope, so these are editorial cleanup rather than additional material findings.

## Basis, independence and authority

The exact reviewed basis is commit `a50358185e5fd4d4eae8c83a18db3e57db22afb1`. `git diff HEAD --exit-code -- docs/design/workflow.md docs/design/cli.md docs/design/record-format.md` confirmed all three reviewed members were unmodified. This Git reference identifies the advisory document revision; it does not infer workflow state or substitute for a formal stored package identity. No manual model hashes or aggregate revisions were calculated.

Reviewer `/root/record_format_rereview` is a separately delegated agent that authored none of the reviewed package. Contributors are the user and author `/root`. The reviewer read all three complete models, the proposal, Proposal Review, both previous Design Review records, relevant governance, and the Design Review method, feature-authoring, requirement-tracing, recording and result/finding assets. The one-file-per-model package follows the explicit user scope and Constitution rather than fabricating separate specification and architecture members. The reviewer changed only this review evidence.

Recording mode is `advisory-durable`; settlement is `none`. Current workflow context again reports `RL_CONTEXT_CHANGE_INVALID` for unrelated historical change `2026-04-24-multi-agent-adapters-first-public-release`, with no selected change. No new root, lifecycle record, reviewer settlement or routing decision was fabricated. The substantive changes-requested outcome stands independently of that formal recording limitation. Previous advisory approval of the older two-model revision does not approve the extracted Record Format model or this revised package.

## Validation

- `node packages/rigorloop/dist/bin/rigorloop.js workflow-context --format json`: exited 2, blocked by the historical change error above.
- `git diff HEAD --exit-code -- docs/design/workflow.md docs/design/cli.md docs/design/record-format.md`: passed; reviewed members unchanged.
- Parent-run `python scripts/validate-boundary-first.py --check --path docs/design/cli.md --path docs/design/workflow.md --path docs/design/record-format.md`: passed, structure-and-references-only.
- Parent-run `python scripts/validate-markdown-readability.py docs/design/cli.md docs/design/workflow.md docs/design/record-format.md`: passed with 226 audit-only MDREAD-002 warnings.
- Parent-run `git diff --check`: passed before review recording.
- `python scripts/validate-markdown-readability.py docs/reviews/2026-09-07-record-format-design-rereview.md`: passed with 24 audit-only MDREAD-002 warnings.
- `git diff --no-index --check /dev/null docs/reviews/2026-09-07-record-format-design-rereview.md`: no whitespace diagnostics; exit 1 denotes the new-file comparison.

These document checks do not establish semantic adequacy or runtime correctness. No runtime implementation test was performed; RF-DR-001 is demonstrated from the explicit design inputs and required outcome.
