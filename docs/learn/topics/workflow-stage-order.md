# Workflow stage order

[Workflow](../../design/skill/workflow.md) owns the current stage order. Allocate verification in the delivery plan after the affected Design is settled; implementation and its proof precede independent review, then distinct final Verify. PR handoff is optional and separately authorized.

The durable lesson from [plan-before-proof framing](../sessions/2026-05-25-plan-before-test-spec-public-framing.md) is to express dependencies accurately. Its old spec/test-spec stage names are historical; current public guidance uses the owning Workflow model.
