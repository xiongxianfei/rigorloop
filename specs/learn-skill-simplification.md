<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Learn Skill Simplification

## Owning change record

`docs/changes/2026-08-16-learn-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Learn Skill Simplification](../docs/proposals/2026-08-16-learn-skill-simplification.md)
- Approved [proposal-review R3](../docs/changes/2026-08-16-learn-skill-simplification/reviews/proposal-review-r3.md)

## Goal and context

This specification defines a shorter published `learn` skill without weakening trigger safety, evidence quality, contributor confirmation, sensitive-data handling, durable session recording, topic ownership, derivative routing, or claim boundaries.

The universal skill owns operation selection, authority, stops, and claims. One conditional session-method reference owns the detailed `Frame -> Observe -> Classify -> Route` session method. Learn owns session records, confirmed topic guidance, and exact owner-result backlinks; it never gains authority to mutate a proposal, specification, ADR, plan, workflow guide, skill, issue, tracker, or external system merely because a learning classification recommends that work.

This specification is a focused amendment to `specs/learn-artifact-model.md`. Where its prospective operation, route identity, or route-settlement rules are more specific, this specification governs the simplified package and new session records. Historical learn artifacts remain evidence under their original format.

## Glossary

- `run-learn-session`: the full recorded learning operation using the four-phase session method.
- `record-learn-route-result`: the bounded operation that links one exact owner-produced result to one existing route in one completed learn session.
- `session attempt`: one exact trigger, normalized scope, evidence basis, and session path selected for a learning session.
- `stable route ID`: a session-local identifier in the form `ROUTE-NNN`, beginning at `ROUTE-001` and increasing without reuse.
- `owner result`: an artifact, durable follow-up, or other result created by the destination owner under its own authority and review gates.
- `route completion`: learn has recorded one exact qualifying owner-result identity against the route; it does not assert that the destination is approved, accepted, implemented, released, or otherwise settled.
- `historical session`: a session created before the stable-route contract or otherwise lacking the route identity required for bounded result recording.

## Examples first

### Example E1: ordinary session disclosure

Given an explicit `$learn` invocation with a valid trigger and writable session location, when operation selection completes, then `run-learn-session` loads the session-method reference before `Frame` begins.

### Example E2: same-day collision

Given `docs/learn/sessions/2026-08-17-example.md` and `...-2.md` already exist, when a new session with the same normalized slug begins, then the new path is `...-3.md` and no existing file is overwritten.

### Example E3: partial prior session

Given an occupied session path contains incomplete or ambiguous content, when a later invocation encounters it, then learn does not resume, repair, adopt, or overwrite it and selects a new unique path or stops if safe creation is impossible.

### Example E4: contributor confirmation

Given observation suggests a durable lesson whose classification requires contributor confirmation, when confirmation is absent, then the session records the pending decision and performs no topic update or derivative-route commitment.

### Example E5: owner-bound route

Given a confirmed classification requires a specification amendment, when routing completes, then the session records `ROUTE-001` as `pending-owner-action` and learn does not edit the specification.

### Example E6: owner-result backlink

Given `ROUTE-001` names the `spec` owner and an exact owner-produced specification revision is supplied, when `record-learn-route-result` validates it, then only the route backlink becomes `complete`; no destination lifecycle claim or mutation occurs.

### Example E7: idempotent backlink

Given the same route already records the same owner-result identity, when result recording repeats, then it returns idempotent success without another session, topic write, route, or destination mutation.

### Example E8: conflicting backlink

Given a route already records one owner result, when a different destination identity is supplied, then result recording stops rather than replacing or reinterpreting the settled backlink.

### Example E9: historical route

Given a historical session lacks stable route IDs, when route-result recording is requested, then the session remains readable but is not implicitly rewritten and the operation blocks.

### Example E10: no durable lesson

Given `Frame` has begun but observation yields no reusable lesson, when the session ends, then the durable session records that outcome rather than disappearing or manufacturing topic or derivative work.

### Example E11: missing method resource

Given `run-learn-session` is selected and the mapped session-method reference is missing or unreadable, when loading occurs, then the operation stops before creating a session record.

### Example E12: trigger-owner closeout

Given a review, incident, release, cadence, or maintainer process decides not to start learn, when that owner closes its trigger, then it records the deferral, follow-up, or no-learn rationale on its own surface and does not invoke a separate learn assessment operation.

## Requirements

### Package and universal ownership

R1. The canonical package MUST contain `skills/learn/SKILL.md` and `skills/learn/references/session-method.md` and MUST add no template, asset, script, executable engine, or additional reference in this change.

R2. `SKILL.md` MUST remain self-sufficient for purpose, operation classification, trigger sufficiency, durable-evidence sufficiency, single-event versus systemic-gap boundaries, contributor confirmation, sensitive-data handling, write ownership, canonical paths, resource selection, missing-resource behavior, stops, claims, and handoff limits.

R3. `session-method.md` MUST load exactly for `run-learn-session` and MUST own the detailed `Frame -> Observe -> Classify -> Route` method, topic curation, derivative classification, route construction, incident evidence selection, and cadence evidence selection.

R4. The reference MUST NOT own operation selection, trigger authority, confirmation authority, destination write authority, sensitive-data policy, workflow routing, or downstream settlement.

R5. The resource map MUST use `READ` with the exact contained relative path and one closed positive trigger, and the reference MUST load at most once per invocation.

R6. A missing, unreadable, escaped, stale, contradictory, or mixed-version required reference MUST stop before session creation or dependent judgment without reconstructing its procedure from memory.

### Operations and trigger ownership

R7. Public learn operations MUST be exactly `run-learn-session` and `record-learn-route-result`; unknown, missing, combined, or ambiguous operations MUST stop before writes.

R8. An explicit direct `$learn` invocation MUST select `run-learn-session` unless the request explicitly identifies one existing session, one stable route ID, and one owner result for `record-learn-route-result`.

R9. `learn` MUST NOT expose `assess-learn-trigger`; the trigger-owning review, incident, release, cadence, workflow, or maintainer process MUST decide whether learn is invoked and MUST own any deferral, scheduled follow-up, or no-learn rationale.

R10. Trigger-owner closeout MUST NOT create a learn session, topic update, route, or claim that learn executed.

### Session identity, creation, and interruption

R11. Before `Frame`, `run-learn-session` MUST resolve one trigger identity, closed existing trigger type, normalized scope, initial evidence-basis identity, canonical session directory, and deterministic candidate path.

R12. Session paths MUST use `docs/learn/sessions/YYYY-MM-DD-<normalized-slug>.md`; when occupied, the writer MUST select the lowest available suffix beginning with `-2` and MUST recheck absence immediately before creation.

R13. Concurrent creation, ambiguous path ownership, unsafe path normalization, or inability to prove absence MUST stop or recompute a new absent candidate without overwriting or adopting existing bytes.

R14. The new session file MUST record its session identity, trigger, scope, evidence basis, and complete `Frame` content in the first successful creation write.

R15. Once `Frame` begins, the invocation MUST leave a durable session outcome, including when observation finds no reusable lesson, evidence is insufficient, confirmation is withheld, or routing is not required.

R16. Learn MUST NOT automatically resume, repair, overwrite, or infer phase completion from an incomplete, ambiguous, or competing session file.

R17. A retry of an explicitly identified already-complete session with the same identity MAY return idempotent recorded success but MUST NOT repeat observation, classification, confirmation, topic effects, or route creation.

R18. A changed trigger, normalized scope, evidence basis, or session identity MUST create a new unique session rather than rebinding a prior session attempt.

### Observation, confirmation, classification, and topic ownership

R19. Session observation MUST distinguish recorded evidence, bounded inference, unknowns, and sensitive or excluded evidence and MUST NOT claim access to unavailable transcripts, runtime state, or external systems.

R20. Contributor confirmation MUST settle only the learning classification and MUST NOT authorize destination mutation, lifecycle transition, issue creation, tracker update, publication, or workflow continuation.

R21. When the governing learn method requires contributor confirmation, learn MUST record `pending`, `confirmed`, or `rejected` and MUST perform no confirmation-dependent topic or route write while status is `pending` or `rejected`.

R22. Classification MUST preserve the accepted distinctions among no durable lesson, confirmed topic guidance, and owner-bound derivative action; unknown classifications MUST fail closed.

R23. Learn MAY create or update confirmed topic guidance under `docs/learn/topics/` only after required confirmation, with an exact session backlink and without presenting topic guidance as authoritative proposal, specification, architecture, workflow, or skill policy.

R24. Repeating the same topic effect for the same session and content identity MUST be idempotent; conflicting or ambiguous topic content MUST stop without overwrite.

### Derivative routes and owner-result recording

R25. Every owner-bound derivative route in a new session MUST have one stable session-local ID `ROUTE-NNN`, assigned in ascending order from `ROUTE-001` without duplication, renumbering, or reuse.

R26. Every route MUST record its source observation, confirmed classification and requested action, exact destination kind and path or external identity, owning skill or process, evidence-basis identity, settlement value, optional owner-result identity, and optional blocker.

R27. Route settlement MUST be exactly `pending-owner-action`, `complete`, or `blocked`; unknown values MUST fail closed before consistency checks.

R28. `pending-owner-action` MUST mean that learn recorded the route but has no exact qualifying owner result, and it MUST NOT imply that the destination owner was invoked or accepted the work.

R29. `complete` MUST mean only that learn recorded one exact qualifying owner-result identity against the route; it MUST NOT imply destination approval, acceptance, implementation, release, workflow completion, or correctness beyond the recorded identity.

R30. `blocked` MUST record a concrete route-specific blocker and MUST NOT silently convert the route to a different classification, owner, destination, or requested action.

R31. `record-learn-route-result` MUST require one exact current session path and identity, one stable route ID, one matching destination owner and route basis, and one exact owner-result identity produced under the destination owner's authority.

R32. Result recording MUST update only the matching route's owner-result backlink, settlement value, and route-specific blocker field when applicable; it MUST NOT create a session, repeat classification, change confirmation, update topic guidance, discover or poll owner work, mutate the destination, change workflow state, or create another route.

R33. A matching existing backlink MUST return idempotent success; a changed session identity, route identity, route basis, destination, owner, or existing different owner-result identity MUST stop without adoption or replacement.

R34. A durable scheduled follow-up MAY qualify as an owner result only when the route explicitly permits that completion kind and the exact follow-up identity is supplied; a chat-only recommendation or unowned note MUST NOT qualify.

R35. Same-turn owner execution MUST finish and record the learn classification, invoke the destination owner under its own contract and review gates, and then use `record-learn-route-result`; learn MUST NOT perform the destination mutation itself.

### Compatibility, output, measurement, and proof

R36. Stable route IDs and route-result recording MUST apply prospectively to sessions created under this specification; historical sessions MUST remain readable and unchanged and MUST NOT become result-recording targets without an explicit separately governed migration.

R37. The compact result MUST distinguish operation, session identity and path, trigger and scope, confirmation result, session recording result, topic effects, route IDs and settlements, owner-result identities, blockers, next owner or handoff, and claim limitations.

R38. Every behaviorally significant current rule and duplicate cluster MUST receive one owner and disposition in a change-local semantic-rule ledger.

R39. Every compatibility-sensitive heading, path, resource verb, operation value, classification, route label, settlement value, and consumed phrase MUST receive one classification and disposition in a separate literal-compatibility ledger.

R40. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have an unknown-value regression test.

R41. Measurement MUST use canonical authored files, LF normalization, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedural resource once in `SKILL.md`, then `session-method.md` order.

R42. Measurement MUST report `LR0-route-result`, `LR1-session`, each resource, and total package size separately; `LR1-session` MUST decrease strictly from the recorded baseline of 1,712 words and 12,375 UTF-8 bytes without semantic loss.

R43. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode resources MUST retain required inventory and raw-byte parity through existing repository tooling.

R44. Acceptance MUST use deterministic contract, fixture, validator, lifecycle, package, and parity proof and MUST NOT execute a target-agent runtime, grade transcripts, add a learning engine, add a tokenizer dependency, or add a separate manual semantic-review acceptance gate.

R45. Published skill text MUST remain project-portable and MUST keep repository-maintainer source, package, release, adapter, selector, and validation mechanics in contributor or governing surfaces rather than shipped procedure.

R46. The bounded architecture assessment MUST return `architecture-required` if safe implementation requires transaction-grade phase recovery, a new persistent route or session schema owner, a polling or coordination service, an external integration, or a new cross-owner mutation authority.

## Inputs and outputs

Inputs are the accepted proposal and review, current `learn` skill, approved learn artifact model, workflow and skill-package contracts, current session and topic artifacts, repository trigger callers, package consumers, validators, and fixtures.

Outputs are the simplified canonical skill, one conditional reference, directly coupled contract and fixture updates, prospective session and route structure, semantic and literal ledgers, profile measurements, package parity evidence, and stage-owned lifecycle evidence.

## State and invariants

- `skills/` remains the sole authored skill source.
- Every actual learning session loads the complete session method.
- Trigger-owner closeout remains outside learn and creates no artificial learn-assessment surface.
- Contributor confirmation grants classification authority only.
- Learn owns session records, confirmed topic guidance, and exact route backlinks only.
- Destination owners retain mutation, review, acceptance, and lifecycle authority.
- Historical sessions remain historical and are not rewritten prospectively.
- Route completion is a backlink fact, not a destination-lifecycle claim.
- Workflow remains the only lifecycle-routing owner.

## Error and boundary behavior

Every unknown vocabulary, ambiguous operation, unsafe path, unresolved trigger or session identity, missing required reference, pending confirmation, conflicting topic effect, malformed route, stale route basis, mismatched destination, unqualified owner result, historical session without stable route identity, concurrent edit, package drift, or unsafe claim fails closed with a concrete blocker. Failure before session creation leaves no session artifact. Failure after `Frame` leaves a durable session outcome but grants no destination authority.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R7, R8, R11, R21, R22, R25, R27, R31, R34 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R9, R10, R14, R15, R16, R17, R18, R21, R23, R24, R27, R28, R29, R30, R32, R33, R36 | BND-STATE-001 | - |
| identity-authority | applicable | R8, R9, R10, R11, R18, R20, R21, R23, R25, R26, R31, R32, R33, R34, R35 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R12, R13, R23, R36, R37, R38, R39, R43, R45 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R12, R13, R16, R17, R18, R24, R25, R32, R33, R36 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R6, R13, R15, R16, R17, R21, R24, R30, R32, R33, R46 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R36, R38, R39, R40, R41, R42, R43, R45 | BND-COMPAT-001 | - |
| external-environment | applicable | R6, R11, R12, R13, R19, R23, R31, R34, R43, R44 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R7, R8, R11, R21, R22, R25, R27, R31, R34 | two operations, current trigger types, confirmation values, classification outcomes, route IDs, settlement values, and completion kinds | unknown or mixed values fail before consistency checks | one valid operation proceeds; invalid input stops | R7 |
| BND-STATE-001 | state-lifecycle | R9, R10, R14, R15, R16, R17, R18, R21, R23, R24, R27, R28, R29, R30, R32, R33, R36 | no session, framed session, completed session, pending confirmation, topic effect, pending route, complete backlink, blocked route, or historical session | recorded state never grants destination authority or rewrites historical evidence | bounded learn-owned state advances or remains unchanged with a blocker | R32 |
| BND-AUTH-001 | identity-authority | R8, R9, R10, R11, R18, R20, R21, R23, R25, R26, R31, R32, R33, R34, R35 | trigger owner, contributor, learn-owned session/topic, destination owner, exact owner result, and workflow router | confirmation and route recording never broaden mutation authority | exact authority permits its own write; absent or stale authority stops | R20 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R12, R13, R23, R36, R37, R38, R39, R43, R45 | universal skill, one reference, session namespace, topic namespace, historical artifacts, and derived packages | one owner per rule, safe contained paths, and byte parity remain mandatory | valid composition loads and writes safely; drift or escape blocks | R1 |
| BND-TEMPORAL-001 | temporal-retry | R12, R13, R16, R17, R18, R24, R25, R32, R33, R36 | first creation, same-day collision, complete rerun, partial prior file, same backlink, conflicting backlink, or changed basis | no automatic partial resume, identity reuse, duplicate effect, or backlink replacement | unique creation or exact idempotent no-op succeeds; unsafe retry stops | R16 |
| BND-RECOVERY-001 | failure-recovery | R6, R13, R15, R16, R17, R21, R24, R30, R32, R33, R46 | failure before Frame, durable incomplete outcome after Frame, complete session, missing method, conflicting topic, or unsafe backlink | recovery never reconstructs missing method or adopts ambiguous bytes | durable bounded outcome is preserved; unsupported recovery blocks | R16 |
| BND-COMPAT-001 | compatibility-migration | R36, R38, R39, R40, R41, R42, R43, R45 | new route-aware session, historical session, normative rule, parser-sensitive literal, incidental prose, canonical source, or derived resource | prospective structure does not rewrite history and packaging remains exact | classified atomic migration passes or blocks | R36 |
| BND-ENV-001 | external-environment | R6, R11, R12, R13, R19, R23, R31, R34, R43, R44 | available local evidence, sensitive evidence, unavailable resource, filesystem collision, owner-produced destination, package build, or clean install | claims match available evidence and no external mutation is inferred | repository-owned proof succeeds or dependent operation blocks | R44 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R8, R9, R10, R11 | BND-INPUT-001, BND-AUTH-001 | an ordinary question or owner closeout manufactures a formal learn assessment or session | only explicit session or exact result-recording requests select learn operations |
| INT-002 | R12, R13, R14, R16, R18 | BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | a same-day collision or partial file is overwritten or silently resumed | deterministic absent path selection creates new content; ambiguous prior bytes remain untouched |
| INT-003 | R20, R21, R23, R25, R26, R31, R32, R35 | BND-STATE-001, BND-AUTH-001 | contributor confirmation or same-turn convenience grants cross-owner mutation | learn records classification and routes; the destination owner performs its own authorized work |
| INT-004 | R27, R28, R29, R31, R32, R33, R36 | BND-STATE-001, BND-TEMPORAL-001, BND-COMPAT-001 | route completion overclaims destination state or rewrites historical sessions | only exact prospective route backlinks become complete and their claim remains narrow |
| INT-005 | R3, R5, R6, R38, R39, R42, R43, R45 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | procedure relocation hides semantic loss or produces package drift | rule and literal ledgers, real-profile reduction, and package parity remain mandatory |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R3 | BND-COMPOSE-001 | - | - |
| E2 | regression | R12, R13 | BND-COMPOSE-001, BND-TEMPORAL-001 | LRNSIM-PR2 | - |
| E3 | regression | R16 | BND-TEMPORAL-001, BND-RECOVERY-001 | LRNSIM-PR2 | - |
| E4 | illustration | R21 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | regression | R32 | BND-STATE-001, BND-AUTH-001 | LRNSIM-PR3 | - |
| E6 | regression | R32 | BND-STATE-001, BND-AUTH-001 | LRNSIM-PR3 | - |
| E7 | illustration | R33 | BND-TEMPORAL-001 | - | - |
| E8 | illustration | R33 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E9 | regression | R36 | BND-COMPAT-001 | LRNSIM-PR6 | - |
| E10 | illustration | R15 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E11 | illustration | R6 | BND-COMPOSE-001, BND-RECOVERY-001 | - | - |
| E12 | regression | R9, R10 | BND-AUTH-001 | LRNSIM-PR4 | - |

## Compatibility and migration

The migration is prospective. New learn sessions use stable route IDs and the bounded route-result operation. Historical sessions and topic files remain readable and unchanged; their absent route IDs are not inferred. The canonical skill, new reference, focused learn contract, directly coupled callers, validators, fixtures, and package metadata migrate atomically. Rollback restores the previous flat skill and coupled expectations and removes the new reference without rewriting historical sessions.

## Observability

The change is observable through operation results, session paths and identities, confirmation status, topic-effect identities, per-route settlement and backlinks, blockers, semantic and literal ledgers, loaded-profile measurements, deterministic scenarios, lifecycle validation, and canonical-through-installed package parity. Reports distinguish configured commands from executed commands and relocated procedure from removed behavior.

## Security and privacy

Existing sensitive-data handling remains universal. Session and topic records must exclude secrets, credentials, unnecessary personal data, unsafe transcript excerpts, and inaccessible evidence. Paths must remain within the approved learn namespaces. Owner-result recording reads only supplied or repository-resolvable identities and grants no external-system mutation.

## Accessibility and UX

Not applicable to end-user interface accessibility. Published Markdown must remain readable, keep complete prose sentences intact, use stable route IDs, and emit no unfilled placeholders.

## Performance expectations

`LR1-session` must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than its 1,712-word and 12,375-byte baseline. `LR0-route-result`, both resources, and total package size are reported separately. No runtime latency, polling, or service-level contract is introduced.

## Edge cases

EC1. The direct request names a route but no session: operation selection blocks.

EC2. A session candidate becomes occupied between resolution and creation: the writer recomputes an absent suffix or stops without overwrite.

EC3. `Frame` completes and later evidence is insufficient: the session records the bounded incomplete outcome and creates no derivative route.

EC4. Confirmation is rejected: no confirmation-dependent topic or route effect occurs.

EC5. Two routes request different owners: each receives its own ascending route ID and independent settlement.

EC6. An owner result exists at the expected path but its identity is not supplied or resolvable exactly: the route remains pending or blocks.

EC7. A scheduled follow-up is supplied for a route that requires an authoritative artifact update: it does not complete the route.

EC8. A historical session resembles the new route table but lacks stable IDs: result recording does not infer or insert them.

EC9. The reference exists in canonical source but is absent from one packaged adapter: package validation blocks acceptance.

EC10. Total package size increases while `LR1-session` decreases: the increase is reported and does not substitute for the required real-profile reduction.

## Non-goals

- Redesigning the accepted four-phase learning method, learn artifact model, trigger cadence, or confirmation policy.
- Adding pre-session trigger assessment, automatic transcript grading, polling, destination discovery, cross-owner orchestration, or an executable learning engine.
- Adding templates, scripts, a route registry, a persistent transaction schema, phase-resume state, external integration, or new lifecycle owner.
- Migrating or rewriting historical learn sessions or topic guidance.
- Treating topic guidance as authoritative project policy or route completion as destination approval.
- Optimizing another skill except for directly coupled contract and caller compatibility.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every R-clause maps to deterministic proof in the test specification. |
| AC2 | The package contains one universal skill and exactly one mapped session-method reference with no asset, template, or script. |
| AC3 | Direct sessions and exact route-result requests select only their defined operations; no trigger-assessment operation remains. |
| AC4 | Same-day collisions, incomplete files, changed bases, complete reruns, and concurrent creation receive one fail-closed or idempotent result. |
| AC5 | Contributor confirmation never grants destination mutation authority. |
| AC6 | New owner-bound routes have stable IDs, complete fields, closed settlement values, and independently reconcilable backlinks. |
| AC7 | Route completion records only an exact owner result and makes no destination approval, implementation, release, or workflow claim. |
| AC8 | Historical sessions remain readable and unchanged and are not implicit route-result targets. |
| AC9 | Semantic and literal ledgers give every current rule and compatibility dependency one disposition. |
| AC10 | `LR1-session` decreases in words and bytes while `LR0-route-result`, resources, and total package remain visible. |
| AC11 | Canonical-through-installed resource inventories and raw bytes match. |
| AC12 | Acceptance executes no target-agent runtime and introduces no separate manual semantic-review gate. |
| AC13 | Architecture assessment returns `architecture-required` if implementation needs persistent phase recovery, polling, external integration, or new cross-owner authority. |

## Open questions

None. Exact Markdown labels for route rows and result fields may vary while preserving R25 through R33 and must be settled by planning and the test specification.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after required review settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture settlement, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
