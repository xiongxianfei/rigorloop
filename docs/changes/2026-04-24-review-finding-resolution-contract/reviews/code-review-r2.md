# Code Review R2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: `de66569`
Status: changes-requested

## Scope

This first-pass implementation review covered the M3 workflow guidance and generated output alignment commit.

## Findings

### CR2-F1: Workflow contract weakens first-pass review timing

Finding ID: CR2-F1

Evidence: `specs/review-finding-resolution-contract.md` requirement `R2m` says material review findings MUST be recorded before fixes begin, with `R2m-exception` defining reconstructed records when that timing was missed. The M3 update to `specs/rigorloop-workflow.md` introduced `R12ab` as "Material review findings SHOULD be recorded before review-driven fixes begin", which weakens the approved timing rule.

Required outcome: The general workflow contract must preserve the approved `MUST` timing rule for material review findings while keeping the reconstructed-record recovery path.

Suggested resolution: Change `specs/rigorloop-workflow.md` `R12ab` from `SHOULD` to `MUST` and rerun focused review-artifact, metadata, lifecycle, and diff validation.
