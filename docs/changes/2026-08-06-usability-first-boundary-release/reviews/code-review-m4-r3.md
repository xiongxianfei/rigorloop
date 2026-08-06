# Usability-First Boundary-First v0.4.0 Code Review M4 R3

Review ID: code-review-m4-r3
Stage: code-review
Round: 3
Reviewer: Codex independent blind-first code-review peer
Target: 692ec7366b664c79d41adeb505a3d572b39b5190..c570b557b447f0f9420a8ea53da7fd88f092a813
Reviewed artifact: commit c570b557b447f0f9420a8ea53da7fd88f092a813
Reviewed milestone: M4 final holistic evidence correction
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m4-r2-count-correction
Reviewer context ID: m4-r3-fresh-independent-final-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: review-resolution-cardinality; final-holistic-evidence-consistency; lifecycle-closeout
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: docs/changes/2026-08-06-usability-first-boundary-release/change.yaml; docs/changes/2026-08-06-usability-first-boundary-release/review-log.md; docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md; docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r2.md; specs/formal-review-recording.md; specs/review-finding-resolution-contract.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@c570b557#sha256:92b720e9d1db8efd1bec1b423263ea2e0f2798b7c8a780fb74b67ae4afd7fb1d; docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md@c570b557#sha256:e69f6de719c406cb156b04c056246483ac34ac2b3303bfd29fc1eadb416e9cf1; docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r2.md@c570b557#sha256:d5453b729b572af0af7434bb33e8b3d1a70bdbfcb63397d4964d3bbd2f3e3270; range:692ec7366b664c79d41adeb505a3d572b39b5190..c570b557.diff@c570b557#sha256:91930091229c3ce716992673570ab099bcd7896e5ed51eff132652afe06430a4; range:d215c045..c570b557.diff@c570b557#sha256:bdc9380310e58024600adcde8dd3b9157a844f427fe1d76e62a12e935aa2e38e
Prompt template version: code-review-v1
Initial packet hash: sha256:91930091229c3ce716992673570ab099bcd7896e5ed51eff132652afe06430a4
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: durable review finding cardinality and final holistic closeout evidence
Highest-impact failure modes: wrong row count; duplicate or omitted findings; stale sibling count; changed implementation conclusion; premature explain-change handoff
Changed boundaries: review-resolution summary; parseable resolution rows; final review receipt; change-local routing
Evidence expected: exact one-line diff; independent overview/detail parse; stale-count search; review-artifact validation; change-metadata validation
Areas requiring direct inspection: resolution overview; Finding ID detail blocks; M4 R2 receipt; review log; change state
Areas intentionally out of scope: implementation behavior; activation derivation; release execution; explain-change; verify; PR; tag; publication; push; merge
Risk classes considered: requirement-fidelity=applicable; review-recording=applicable; lifecycle-closeout=applicable; implementation-behavior=not-applicable:unchanged-one-line-evidence-correction; live-publication=not-applicable:forbidden-lifecycle-action; external-mutation=not-applicable:forbidden-lifecycle-action
Falsifiable review questions: Do exactly 26 unique parseable overview rows match 26 unique detail IDs? Does any live final-review surface still claim 22 findings? Does the numeric correction preserve the clean implementation conclusion?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m4-r3.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md; docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r2.md
Requirement-fidelity matched path triggers: docs/changes/**/reviews/; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: review-recording contracts; material-finding schemas; workflow routing contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > recording contract > correction diff > resolution rows > detail IDs > sibling review receipt > validators
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M4-CR3-001
Material findings: UBR-M4-CR3-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M4-CR3-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M4-CR3-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r3.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-m4-r3`
- Reviewed milestone: M4 final holistic evidence correction
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 evidence correction
- Required review-resolution: yes
- Finding IDs: UBR-M4-CR3-001
- Verify readiness: not-claimed

## Finding UBR-M4-CR3-001

Finding ID: UBR-M4-CR3-001
Severity: major
Location: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r2.md:90`
Evidence: The one-line correction accurately changes `Findings resolved` from 22 to 26. Independent parsing finds 26 unique resolution-overview rows, all `accepted` and `resolved`, exactly matching 26 unique `Finding ID:` detail blocks. However, the governing M4 R2 final holistic receipt still says “All 22 material findings,” so the durable final-review surfaces disagree after the correction. Repository review-artifact validation reports 26 findings but does not reject the stale prose count.
Required outcome: Every live final-holistic and review-resolution count claim states 26 while preserving the clean M4 R2 implementation conclusion and `explain-change`-before-`verify` routing.
Safe resolution path: Change only the stale `All 22 material findings` phrase in `code-review-m4-r2.md` to `All 26 material findings`; rerun the independent overview/detail parse, stale-count search, review-artifact validator, change-metadata validator, and diff check; then request M4 R4.
needs-decision rationale: none
auto_fix_class: mechanical

## Review evidence

- Correction diff: exactly one line in `review-resolution.md`, changing 22 to 26; no implementation, spec, test, architecture, release, or routing code changed.
- Independent overview parse: 26 rows, 26 unique IDs, 26 `accepted` dispositions, and 26 `resolved` statuses.
- Independent detail parse: 26 `Finding ID:` records, 26 unique IDs, exactly the same set as the overview rows.
- Stale-count search: `review-resolution.md` now says 26, but `code-review-m4-r2.md:90` still says 22.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-06-usability-first-boundary-release/` passes and reports 26 findings, demonstrating that the structural validator alone does not prove prose-count coherence.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` passes.
- `git diff --check 692ec7366b664c79d41adeb505a3d572b39b5190..c570b557` passes.

## Checklist coverage

- Spec alignment: block; formal review evidence must remain internally consistent.
- Test coverage: concern; structural validation passes despite the stale sibling numeric claim, so independent count comparison is required.
- Edge cases: pass; duplicates, missing rows, non-final dispositions, and overview/detail set drift were checked directly.
- Error handling: not applicable; the correction is static review evidence.
- Architecture boundaries: pass; no implementation or release authority changed.
- Compatibility: pass; implementation and downstream contract conclusions are unchanged.
- Security/privacy: pass; no private or external data is involved.
- Derived artifact currency: block for durable review evidence only; the summary and final receipt disagree.
- Unrelated changes: pass; the target commit is exactly one line.
- Validation evidence: block; repository validators pass, but the required independent semantic count check exposes stale evidence.

## Prior and final-holistic reconciliation

- UBR-M4-CR1-001 remains resolved; selector, activation, release, rollback, and package conclusions are unaffected.
- M4 R2's substantive implementation conclusion remains valid. This R3 finding is limited to its stale numeric review-evidence claim.
- Final holistic approval cannot remain the active clean handoff while its durable receipt disagrees with the corrected parseable finding inventory.

## Handoff

Record and resolve UBR-M4-CR3-001 through the one-line M4 R2 receipt correction, then request independent M4 R4. `explain-change` and `verify` remain blocked until the review evidence is coherent and a clean final holistic rereview closes the finding.
