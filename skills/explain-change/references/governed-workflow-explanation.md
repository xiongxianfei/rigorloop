# Governed workflow explanation

This reference supplies governed eligibility, basis, closeout, staleness, and handback. The parent owns classification, writes, stops, and claims.

## Eligibility and placement

Resolve one current change root, `change.yaml`, target, stage, and authority. Governed work uses `docs/changes/<change-id>/explain-change.md` unless current authority names approved legacy placement. Invalid identity stops.

Inspect `review-log.md`. `Closeout status: open` or `needs-decision` blocks; `Closeout status: closed` requires final dispositions and evidence. A stage-owned non-approval outcome requires a same-stage later review round or explicit reviewer or owner closeout; `review-resolution.md` alone is not a silent substitute. no-material detailed records need `review-log.md` but not an empty `review-resolution.md`. Also require closed milestones, clean final holistic code review, and current promotion evidence.

## Reviewed-change basis

Bind change, repository, base revision, reviewed-subject revision, base-to-subject diff identity, final holistic code-review ID and subject identity, governing artifact identities, review-resolution basis, validation-evidence cutoff, explanation path, and prior identity.

Final reviewed diff means base to reviewed-subject. Content identity, recording revision, and handoff revision remain separate; no self-referential commit identity.

Handoff equals the reviewed subject or one direct-child explain-change-owned evidence commit containing only the explanation artifact. It excludes product code, tests, specifications, architecture, plans, dependencies, configuration, generated output, unrelated documentation, change-record mutation, and other-stage evidence.

A non-direct child, broader or multiple tail, or changed basis requires new final review. Later verify evidence alone does not stale unchanged explanation evidence and cutoff.

## Governed result and handback

Durable output records `Stage: explain-change`, `Status: current` or `blocked`, `Final diff identity`, `Final review identity`, and its basis. Governed inline reports the same facts.

For `Workflow handback`, report `Explanation status`, `Explanation basis`, `Validation-evidence cutoff`, `Open explain-change blockers`, `Control returned to workflow`, and `Next-stage decision owner: workflow`. Never use or imply `verify-ready`, `verification-passed`, `branch-ready`, `pr-body-ready`, `pr-open-ready`, `release-ready`, or `lifecycle-complete`. Workflow alone selects the next stage; isolated invocation stops.
