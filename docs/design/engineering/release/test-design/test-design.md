# Release test design

Owner: [Release](../release.md#test-design), model ID `release`.

Release supports occasional publication of this repository's skills and CLI. Its design protects four outcomes: prepare the intended release, qualify the actual artifacts, publish only with exact approval, and report or recover honestly. The [catalog](test-cases.json) owns concrete scenarios; [System](../../../test-design/rules.md#start-from-supported-outcomes) owns shared test-quality and maintenance rules.

## JSON case-design draft

The catalog contains **42 scenarios**: 39 automated-test designs and three review procedures. They cover the 24 recurring Release requirements through seven existing behavior groups. REL-SR-20/21 retain their original scoped source-consolidation obligations in the owner; this catalog neither retires those rows nor adds perpetual replay cases for them. Several executable methods may realize one scenario at different observation boundaries. Native discovery owns the executable inventory; complete method-to-case mapping is not a catalog requirement.

There are 23 `existing`, 13 `partial` and six `proposed` scenarios. Three proposed scenarios describe missing automated protection; three describe assessments of actual release authority or incidents. The latter are procedures to apply when relevant, not three additional mandatory reviews on every release. The known gaps in the contributing designs remain explicit after consolidation. These classifications describe realization, not passing execution or independent approval.

Each scenario states defining conditions, actions, independently expected observations and its realization links. For example, `REL-IN-001` groups profile-admission variations, `REL-TC-001` observes correct generated values and honest pending evidence, and `REL-AR-010` distinguishes unknown public state, bounded visibility and safe retry. Field-by-field parser mutations and mandatory-row enumeration remain in the linked executable tests; they do not need individual permanent design entries.

`format_version: 2` remains the provisional representation. The index explicitly names the seven group files. JSON owns scenario intent, this companion owns strategy, and scripts own executable setup and assertions. Results remain in evidence associated with exact subjects. This package neither supplies a runner nor changes test selection.

## Catalog contract

This section defines the provisional Release representation for author checks and validation. The index records covered behavior and evidence limits; case realization records pending proof. Preserve IDs and protection when editing. Unknown structural fields and closed values reject; free-form scenario prose, fixture facts and variant parameters are descriptive data rather than executable code.

| Object | Required fields and constraints | Optional fields |
| --- | --- | --- |
| Index | `format` = `release-test-catalog-draft`; integer `format_version` = 2; `owner`, `scope`, `fixture_rules`, nonempty `groups`. | None. |
| Owner | Nonempty `model`, `design`, `test_design`; here model is `release` and paths identify its main document and this companion. Every group repeats the identical owner. | None. |
| Index scope | Nonempty strings `model`, `boundary`, `entrypoint`, `coverage_claim`. Boundary names covered behavior; coverage claim states the extent and limits of the evidence. | None. |
| Fixture rules | Nonempty strings `isolation`, `independent_expectations`, `negative_setup`, `version_roles`, `resource_boundary`. Rules apply to every indexed group. | None. |
| Group index entry | Nonempty `id`, `title`, `path`; IDs and paths are unique. Paths explicitly identify JSON under this package's `cases/`. | None. |
| Group file | `format` = `release-test-cases-draft`; integer `format_version` = 2; `owner`, `scope`, nonempty `fixtures` and `cases`. | None. |
| Group scope | Nonempty `group`, `title`, `boundary`; identity/title agree with the index entry. Boundary explains the group's proof limits. | None. |
| Fixture | Nonempty local `id` and nonempty string array `initial_state`. IDs are unique within the group. | `builder` callable reference; `profile` repository file reference; `facts` nonempty descriptive object; `expected_changed_paths` nonempty fixture-relative path array; `extends` group-local base fixture ID; `reference_test` exact source reference illustrating setup; `limitation` nonempty explanation of proof limits. Omit absent fields; no null builder. |
| Case | Nonempty `id`, `title`, `risk`; nonempty unique `requirements` array; `technique`, `method`, `boundary`, `target`, `given`, nonempty string arrays `when` and `then`, and `realization`. | Nonempty `variants` array. |
| Given | Local `fixture` ID and nonempty string array `conditions`. Defining mutations are visible here or in variants. | None. |
| Variant | Nonempty case-local `id`, unique within its case; nonempty `parameters` object of descriptive JSON values. Parameters supply named inputs/faults/expected diagnostics used by the shared case. | None. |
| Callable/test reference | Nonempty repository-relative `path` and exact nonempty `symbol`; Python methods use `Class.method`. Linked references exist in current source. | None. |
| Review target | Nonempty repository-relative `path` and exact Markdown `section`; no `symbol`. | None. |
| Realization | `state`; `tests` array of unique callable references; `gaps` array of nonempty strings. Empty arrays are meaningful under the state rules below. | None. |

JSON strings must contain non-whitespace content. IDs use ASCII letters/digits/hyphens, begin with a letter, and retain case; group/fixture/variant IDs use lowercase. Paths use normalized repository-relative POSIX spelling, without absolute prefixes, `.`/`..` segments or symlink traversal. `expected_changed_paths` instead name files within the private fixture root. Variant parameters and fixture facts may contain strings, finite numbers, booleans, null, arrays and objects; their values have no dispatch authority. Reject duplicate JSON keys anywhere, even inside descriptive data.

`method` is `automated-test` or `independent-review`. `boundary` is `contract`, `public-command`, `composition` or `review`. A review case uses the review target and boundary, has `method=independent-review`, and its realization has no executable test links. Automated cases use callable targets and the other boundaries. Review execution results remain outside this catalog; performing a review does not turn its empty test list into `existing` automated coverage.

`technique` is `equivalence-partition`, `boundary-values`, `decision-table`, `state-transition`, `property`, `fault-injection` or `walkthrough`. It identifies the primary derivation method. Boundary and technique are independent: a property may be observed at a command or through composition. Walkthrough identifies the review procedures in this draft. More detail belongs in the concrete conditions/outcomes, without adding arbitrary vocabulary values.

`realization.state` is `existing`, `partial` or `proposed`. Existing requires at least one test and no gaps. Partial requires at least one test and at least one named gap. Proposed requires no linked tests and at least one gap, including a required real-subject assessment for a review procedure. These are author claims to inspect, never inferred passing results. A method link alone cannot justify existing status.

Requirements resolve to the owning model's current requirement table. Fixtures are group-local. Optional `extends` references a setup basis in the same group and must be acyclic; it does not implicitly override or merge JSON fields, execute a builder or introduce test-class inheritance. Case IDs are unique across the complete model catalog; variant identity is `(case ID, variant ID)`. Moving a case or variant preserves its ID. Retiring an obligation removes its exclusive cases only after resolving current consumers, with history retained in Git. Do not reuse retired IDs for unrelated behavior. Native discovery accounts for linked tests, including imported/generated cases and meaningful subtest variants; method count equality is insufficient semantic proof.

## Scope and evidence boundary

The recurring population is the current stable package and Codex/Claude Code targets under [Release's support transition](../release.md#distribution-support-transition). The catalog covers the following outcomes. The group files remain at their existing paths because their fixtures and observation boundaries remain useful.

| Outcome | Groups and scenario count | Why the protection is needed |
| --- | --- | --- |
| Prepare the intended release | [Profile/input](cases/profile-input.json): 4; [preparation](cases/preparation.json): 9; [preflight](cases/preflight.json): 4 | Wrong intent, corrupted human content, fabricated readiness or unobserved prerequisites can produce an invalid candidate. |
| Qualify the actual artifacts | [Candidate identity](cases/candidate-identity.json): 6 | Checked source, package bytes, bundled metadata and installed artifacts must describe the same candidate. |
| Publish only with exact approval | [Approval/recovery](cases/approval-recovery.json): 12 | Wrong authority, conflicting identity, partial writes and lost observations can cause irreversible or duplicate publication. |
| Report and recover honestly | [Evidence/closeout](cases/evidence-closeout.json): 4 | Public installation, failure history and durable evidence must reflect what happened. |
| Assess authority when relevant | [Policy review](cases/maintenance-review.json): 3 | Engineering judgment, exceptional permission and incident correction cannot be proved by parser checks. |

The three review procedures qualify the four outcomes. `REL-MR-001` assesses the engineering/version authority already needed for routine eligibility; it creates no extra release-time engineering lifecycle. `REL-MR-002` applies to a requested exception, and `REL-MR-005` to an actual bad-publication incident. A valid synthetic exception record establishes no real authorization.

One-time source-consolidation acceptance belongs to its governing change. Test adequacy uses System’s shared rules and the existing assessment process; discovery checks remain with Validation. Neither is a recurring Release operation requiring its own case. The [focused change](../../../../changes/2026-09-17-model-test-design/change.json) records the executable-test refinement and its retained protection. It does not transfer source-consolidation duties or retarget prior judgments.

Local provider fixtures prove decisions, serialization and recovery. They cannot establish remote protection configuration, a real public publication or fresh public installation. Packaging and Installation own their detailed behavior; `REL-CI-013` proves their integration with the actual Release candidate rather than copying their complete suites. Historical evidence is an immutable input only where the current reader contract requires it, not a historical release-execution matrix. Prerelease or exceptional policy does not create routine tooling support.

## Requirement accounting and proof limits

Use [System's complete selection procedure](../../../test-design/rules.md#select-requirements-and-proof) before changing the cases. The following groups account for the current requirement population without another per-method ledger. The catalog remains the sole concrete scenario owner; its defining inputs, actions, expected observations and unresolved gaps are not duplicated here.

| Current requirement group | Primary catalog coverage or scoped proof | Why the selected boundary is necessary |
| --- | --- | --- |
| REL-SR-01, REL-SR-02, REL-SR-03, REL-SR-22 — supported intent and routine eligibility | Profile/input, preparation and policy-review groups; especially REL-IN-001/010 and REL-MR-001. | A valid profile cannot independently establish approved engineering intent. Use input partitions for supported values and an independent actual-subject walkthrough for version/authority judgments. |
| REL-SR-04, REL-SR-05, REL-SR-07 — generated surfaces and preservation | Preparation plus REL-IN-006/008 and REL-PF-002. | Independently inspect actual changed bytes and forbidden side-effect boundaries; a returned change list or empty external-action tuple cannot prove preservation. Keep malformed markers, interruption and rerun distinct from ordinary idempotence. |
| REL-SR-06, REL-SR-09 — cheap preflight and complete qualification | Preflight group, REL-CI-001/010/013/022 and REL-AR-034. | Command reachability and actual candidate composition expose bypasses that isolated parsers cannot; real Git and controlled remote observations preserve the preflight environment boundary. |
| REL-SR-08, REL-SR-12, REL-SR-23, REL-SR-25 — exact candidate and publication authority | Candidate-identity and approval/recovery groups; REL-AR-036 retains the between-boundary revocation gap. | Authority before the first write, changed authority between writes and altered artifact identity have distinct irreversible effects. Observe the real coordinator with provider write histories, not a policy helper alone. |
| REL-SR-10, REL-SR-13, REL-SR-14, REL-SR-15, REL-SR-24, REL-SR-26 — public facts, durable evidence and safe recovery | Evidence/closeout, approval/recovery and current-candidate admission; REL-EC-001, REL-AR-010/011/016/019 and REL-MR-005. | Lost publication responses, partial assets, failed smoke, identity drift during smoke and failed report persistence require separate observations. Local fixtures establish decisions and persistence; required actual public observations remain release-scoped. |
| REL-SR-11, REL-SR-16, REL-SR-17 — authentication, exceptions and privacy | REL-AR-028/030/034, REL-EC-009 and REL-MR-002/005. | A controlled provider can expose unsafe execution or leaks; it cannot grant emergency permission or assess an actual fix-forward decision. Review the exact authority/evidence when that situation occurs, without inventing an extra routine gate. |
| REL-SR-18, REL-SR-19 — diagnostic timing and closed representations | REL-EC-024 plus profile/input, marker, literal and candidate shape scenarios. | Unknown values must reject before consistency; unavailable timing cannot supply a correctness result or suppress an otherwise valid release. [Validation's case costs](../../validation.md#execution-cost-reporting) remain separate observations from operational phase/job telemetry. |
| REL-SR-20, REL-SR-21 — selected source-consolidation acceptance | Independent inspection of the original exact source/obligation disposition, current reader/resource closure and retained protective proof under the owning change and [Engineering retirement policy](../../engineering.md#repository-retirement). | These are bounded migration duties, not a recurring supported-release input class. Assess transferred meaning and actual consumers; record unresolved current reliance with its owner. Do not replay completed releases, rewrite historical judgments or promote document removal into implementation success. |

The existing catalog's 13 partial and six proposed scenarios remain explicit. Their missing assertions, faults and command observations are required alignment work; the three actual-authority/incident review procedures remain conditional on those events. A future authorized release or incident is not performed solely to call this suite complete or obtain a duration. Conversely, applicability does not waive missing deterministic automated proof. Delivery must allocate the catalog gaps, actual fixture/source audit and appropriate semantic assessments, and limit completion claims where applicable proof is unavailable.

The supporting architecture is unchanged: preparation, candidate qualification, approval, execution, public observation and durable reporting retain their existing owners and edges. This method selects proof at those existing boundaries without changing routine support, adding a historical release matrix or changing the seven-file catalog contract.

## Selecting a scenario

Start with a supported outcome and a plausible material violation. Use representative input partitions for admission, decision tables for eligibility/approval, state transitions for publication/recovery, properties for preservation and identity, and controlled faults for uncertain writes. Apply boundary values to real limits, such as the bounded visibility observations in `REL-AR-010`.

Keep scenarios separate when the required observation changes: rejected approval before the first write, revoked approval between writes, partial asset publication, failed public smoke, and lost evidence after publication expose different failures. Within a scenario, related malformed fields or required rows can share a decision table in code. A new helper, serialized field, version literal or test method alone does not justify a catalog entry. There is no case-count target.

Combine scenario entries only after retaining the relevant conditions, observations, realization links and unresolved gaps. Retain existing IDs for continuing scenarios; record any future merged-ID disposition once in its owning change, without aliases or a second live inventory. A shorter catalog is a reduction in documentation, not evidence that executable tests are redundant. Removing a test still requires a retired obligation or demonstrated replacement protection under System’s shared rules.

## Preparation and preflight

Use independent synthetic previous/target versions, private real files and snapshots. `REL-TC-001` checks actual package identity and the expected generated path set rather than trusting a reported changed-file list. `REL-TC-005` compares human/history bytes; `REL-TC-008` observes successful and failing check mode through the real CLI. Pending and finalized evidence have different starting states and expected consequences.

Keep `REL-TC-027` for absence of external operations and `REL-TC-029` for a write interruption followed by inspection and repair. Neither is established by a returned success flag. `REL-TC-030` covers malformed markers before writes; missing nesting/unknown-surface protection remains an implementation gap. Preflight uses actual Git discovery and controlled remote observations while retaining its cheap, side-effect-limited contract.

## Candidate and publication

`REL-CI-001` covers authored source and loaded runtime identity; `REL-CI-004` covers the artifact seal. Both retain their missing baseline/restoration assertions. `REL-CI-013` uses the real builders and packed CLI to establish artifact composition. Other admission and tag-entrypoint cases prevent old reports, failed prepared checks or conflicting refs from supplying authority.

Use the real approval policy, executor and coordinator with controlled external observations, write histories and faults. `REL-AR-034` spans preparation, build, one fixture approval, publication and reporting through actual dispatch. Smaller scenarios isolate authority, persistence, concurrency, public conflicts and partial publication without repeating the full build for each malformed field. Links to one composed method do not require duplicate execution or create independent passing results.

`REL-AR-010` preserves unknown-before-write versus uncertain-after-write and exact visibility limits: six post-write observations for tag/GitHub, 121 for npm, no wait after the final observation. Exhaustion and recovery remain incomplete proof. `REL-AR-036` retains authority revocation between boundaries; `REL-AR-011` retains the gap for changed public identity during smoke. These risks remain meaningful even with infrequent releases.

## Evidence and recovery

`REL-EC-001` consumes independently varied provider facts, preserves pending/unrelated evidence on failure, and retains missing no-write and negative-baseline assertions. `REL-EC-009` distinguishes complete, failed and legitimately deferred duties without assigning one design entry to every required row. `REL-EC-018` binds pending-gate admission to exact CI proof. The current historical reader remains distinct from admission of a new current profile.

`REL-EC-024` protects the consequence of diagnostic timing: unavailable or malformed telemetry cannot alone suppress otherwise successful publication, and tolerance cannot admit an invalid release profile. Individual timing-field checks remain in executable tests. No extra release gates, duration targets or timing scenarios are introduced.

## Fixtures, scripts and maintenance

Each scenario or variant owns its mutable files, mappings, provider log and Git state. Reuse small fixture operations while keeping the defining fault visible. Expected values come from the contract; preservation snapshots precede mutation, and negative tests first establish a valid baseline. Actual candidate tests use selected real bytes. Additional synthetic versions require a distinct outcome rather than a new release number.

The [existing suite entrypoint](../../../../../tests/engineering/release/test-release-transaction.py) retains discovery and filtering. Behavior modules, framework test classes and fixture functions remain implementation choices; no object hierarchy, per-function quota or file-length threshold follows from this catalog. Existing lower-level tests can remain useful without separate catalog entries. A lost import or undiscoverable linked method remains a defect.

Review the owner, strategy, index and affected groups together. Author audits check parsing, IDs, containment, references, discoverability and retained gaps; independent review assesses scope, scenarios and assertion adequacy. [Validation](../../validation.md#release-test-design-admission-contract) owns repository admission. Current implementation allocation, evidence and tooling limitations belong to the owning change rather than this living strategy. Account for native cases, generated registrations, named subtest observations, fixtures and direct callers when aligning this catalog with the executable suite. Use Validation's [execution-cost reporting](../../validation.md#execution-cost-reporting) for before/after measurements with the same relevant execution conditions; a case's process cost includes its setup/cleanup and does not isolate provider latency or its test body. Preserve required real artifact and recovery observations before reducing repeated setup.
