# Governed test-spec authoring

Load only for `governed_test_spec_candidate_context`. The parent owns proof quality; this reference owns governed authoring registration.

## CLI-bound authoring

Run `rigorloop lifecycle context test-spec --change <change-id> --format json`. Require settled spec, plan, and applicable architecture; exact target or unambiguous creation path; legal authority; and no blocker. Capture the target digest before revision.

If context returns `RL_WORKFLOW_ROUTE_REQUIRED`, do not author or mutate state. Return its route facts to workflow and resume only after context makes `record-artifact-revision` immediately available.

Write only the test specification and evidence containing `Artifact path`, `Artifact identity`, and `Authoring result: complete`. Creation requires no competing primary. Revision requires exact prior identity plus a current finding, upstream change, or reopen authority. Preserve prior evidence and route implementation reliance, partial unknown content, or unsafe recovery to workflow.

After validating proof coverage and evidence, refresh context and submit `record-artifact-revision` with the returned lifecycle revision, exact artifact ID, `artifact_kind: test-spec`, role, path, evidence path, `stage_authority: test-spec`, and prior digest for revision. The CLI derives `review-required` and invalidates registrations tied to the replaced identity. Never edit lifecycle, review, workflow, routing, or automation fields directly.

`already-recorded` is success for an identical request. Stale context, changed basis, path or identity mismatch, competing content, rejected registration, or ambiguous restart stops without adoption.

## Result

Report operation, identities, validation, CLI result, blockers, and `test-spec-review` handoff without authorizing implementation.
