# Bounded workflow automation

## Load condition

Read this procedure for an explicit `$workflow auto: <argument>` command or a valid active or resumable automation run. `<argument>` is a supported target stage, `status`, or `off`.

Automation is one target-driven `bounded-review-fix` mechanism under `workflow.automation`. The requested target is the complete automation boundary. Do not add a second authorization, selector, capability, or inferred continuation parameter.

Supported targets are `proposal-review`, `architecture`, `spec`, `design-review`, `plan`, `test-spec`, `delivery-review`, `implement`, `code-review`, and `verify`.

## Command classification

An explicit target command creates `automation_command_context`; it does not by itself create `armed_automation_context`. Durable automation must be bound to the exact governed change identity, target, occurrence when a stage repeats, canonical position source, and current authorization.

`$workflow auto: status` is read-only. `$workflow auto: off` durably cancels an existing unified run and preserves transition evidence. When neither a governed record nor a matching run exists, `status` and `off` return `no-active-run`; this creates no governed or automation state.

Direct review invocations do not activate, resume, or advance automation. Manual skill invocations stay isolated unless an authorized workflow-managed context invokes them.

## Automation bootstrap

For a new target command without an existing governed record, use this exact order:

1. Recognize the explicit target command and enter transient bootstrap state.
2. Load bounded workflow automation procedure for bootstrap semantics.
3. Resolve or create governed change identity under existing workflow authority.
4. Validate the governed record and exact change identity.
5. Reclassify as governed context.
6. Load governed lifecycle procedure.
7. Only then persist authorization, target, occurrence, and run state.

Bootstrap is transient and is never persisted as an armed run. If identity creation or validation fails, stop without partial automation state. Active or resumable automation without a valid governed identity is invalid.

## Target and occurrence

Reaching a target stops at that exact stage occurrence. Repeated `implement` and `code-review` targets bind the unique current plan milestone before persistence and never silently rebind on resume.

Resume uses tracked artifact and review evidence. Do not rerun completed artifacts or clean reviews. Do not infer completion from file existence. Pause when the authoritative position or occurrence is ambiguous.

The mechanism never opens a PR, pushes, publishes, releases, deploys, merges, performs destructive Git operations, accesses credentials, or mutates an external system.

## Authoring and review gates

Authoring follows the governed stage order. Every formal review is recorded before automation-driven downstream action. Automated review must reset context to the reviewed artifact, governing requirements, review criteria, and relevant recorded findings rather than rely on hidden authoring reasoning.

Workflow-managed automated `code-review` uses the independent adversarial review gate. The orchestrator creates the neutral review invocation manifest and initial packet. It must withhold validation-result summaries, evidence menus, implementation notes, and prior finding content until the required phase receipts allow release.

Workflow-managed automated `code-review` uses the requirement-fidelity gate when deterministic applicability is `applicable`. The requirement-fidelity gate is additive with the independent adversarial review gate; both receipts must pass when both contracts apply. Requirement-fidelity review starts from the relevant spec clause, then decomposition, expected surfaces, implementation diff, validator assertions, validation evidence, and prior findings.

A first-pass material result must be recorded before any review-driven fix. `blocked`, `inconclusive`, owner decisions, or open `needs-decision` stop. A clean automated review may advance only after the normalized `review_gate_outcome`, independence manifest, phase receipts, clean receipt, risk-tier gates, unresolved-finding check, and second-review policy all pass.

Before `explain-change` or `verify`, require final holistic code-review evidence covering the complete final diff and cross-milestone interactions.

## Bounded correction

Only reviewer-declared eligible corrections may enter a bounded correction cycle. Track finding identity, allowed surfaces, correction count, validation, and rereview evidence. Stop on new findings, scope expansion, a non-shrinking loop, exhausted budget, ambiguous ownership, or a correction that is no longer mechanical or declared safe.

Implementation and review remain separate stage owners. Correction never changes upstream requirements, architecture, or stable plan intent.

## Promotion and pause

Automation asks governed lifecycle procedure for each next valid transition. It must not redefine stage order, architecture applicability, settlement, milestone closeout, or final holistic-review requirements.

Pause on missing promotion evidence, unrelated dirty state that prevents attribution, stale identity, owner decisions, target non-applicability, verify failure, resource failure, transition-budget exhaustion, user pause/cancellation, or any attempt to cross the PR boundary.

Every result reports target, occurrence when applicable, canonical position source, stage outcome, review and clean-gate state, transitions, corrections, decisions, artifacts, stop reason, and next action.
