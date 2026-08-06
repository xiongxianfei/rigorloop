# Usability-First Boundary-First v0.4.0 Release

## Owning change record

`docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-06-usability-first-boundary-release.md`

## Goal and context

Publish `boundary-first-v1` as automatic, concise behavior in the related lifecycle skills.
Users should receive the correctness benefit without naming the method and without routine work expanding into an exhaustive scenario catalog.

The same change prepares stable release `v0.4.0` through the existing routine release workflow.
Checked-revision activation and public release are separate claims: files in the currently checked repository revision can prove that the behavior is active before a release tag exists, while public availability still requires the immutable tag and ordinary publication evidence.

This specification replaces the custom candidate-validation and atomic-publication design with the smallest contract that preserves user-facing behavior, package parity, release integrity, and rollback.

## Glossary

- `automatic boundary coverage`: considering material correctness boundaries as part of normal skill behavior without requiring a method name or special prompt.
- `material boundary`: an admitted input, state, authority, composition, timing, recovery, compatibility, or environment condition whose outcome can change correctness for the task at hand.
- `concise default`: covering each material boundary once at the artifact's natural level while omitting inapplicable dimensions and speculative scenarios that have no governing requirement, observed interface, or named failure consequence.
- `deeper analysis`: expanded partitions, interactions, or explanation required by the task, its governing contract, a material risk, or an explicit user request.
- `checked-revision activation`: validation of boundary-first behavior using only files in the currently checked repository revision, without requiring Git history, remote state, release tags, or network access; it is not a claim that a version is publicly available.
- `grandfathering baseline provenance`: the exact full reviewed pending-revision commit identity supplied explicitly to activation preparation and used once to derive the frozen grandfathered-spec inventory; it need not be a release tag, the active record's parent, or reachable during later checked-revision validation.
- `frozen grandfathered-spec inventory`: the sorted path inventory derived during activation preparation and thereafter used directly to preserve historical accepted specifications.
- `routine release workflow`: the existing release-profile, preparation, preflight, full verification, trusted tag publication, and public closeout flow.

## Examples first

Example E1: a RigorLoop specification gets boundary coverage without a keyword
Given a user asks for a specification of the existing `python scripts/validate-boundary-first.py --check` behavior
And the user does not mention boundary-first
When the `spec` skill authors the contract
Then it covers coherent pending and active snapshots, missing, malformed, additional, mixed, and unknown state, and compatibility with the existing checked-revision validator
And it does not invent release-tag, network, publication, or Git-transition-history scenarios for that local validation.

Example E2: code inspection stays concise
Given a user asks to inspect the activation-record loader used by `python scripts/validate-boundary-first.py --check`
When a related implementation or review skill examines that loader and its public CLI caller
Then it covers missing, additional, malformed, and unknown fields, coherent pending and active snapshots, frozen-inventory handling, and public-call behavior
And it does not introduce GitHub, npm, publication, or provider-outage analysis.

Example E3: a RigorLoop code review covers the exact cleanup boundary
Given a diff removes the custom candidate and publisher experiment while retaining focused `--check` validation and the routine release workflow
When the `code-review` skill evaluates the diff
Then it covers removed helpers, options, tests, and selector paths plus retained checked-revision validation, routine release, and rollback behavior
And it does not introduce atomic-ref races or custom-publisher recovery because those unpublished mechanisms are being removed.

E1 through E3 are semantic proof fixtures for automatic boundary selection.
They do not define product behavior for RigorLoop or require exact prose, output length, or a fixed global scenario count.

Example E4: the checked revision is active before publication
Given the activation record is active and canonical and generated skill resources agree
And `v0.4.0` has not been tagged or published
When checked-revision boundary validation runs
Then activation validation passes without claiming that `v0.4.0` is publicly released.

Example E5: the routine release publishes one coherent package
Given the reviewed `v0.4.0` tree passes routine preparation, preflight, full release verification, package parity, and packed installation smoke
When a maintainer tags the exact reviewed commit and the trusted release workflow runs
Then Codex, Claude, opencode, GitHub release archives, and npm expose the coherent `v0.4.0` capability and public closeout records the result.

Example E6: publication fails after one public surface changes
Given the immutable `v0.4.0` tag exists and one publication surface succeeds while another fails
When release closeout observes the partial state
Then it remains open with the failed phase and uses the existing rerunnable closeout or a later patch; it never rewrites `v0.4.0`, and `v0.3.6` remains selectable as rollback.

## Requirements

UBR-R001. The ten governed skills `workflow`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `test-spec-review`, `implement`, `code-review`, and `verify` MUST apply their stage-owned `boundary-first-v1` responsibility automatically when the task admits behavior boundaries; users MUST NOT need to name the method, version, or reference file.

UBR-R002. Default skill behavior MUST cover every material boundary admitted by the task's governing requirements and observed interfaces, and MUST omit a dimension or scenario that has no governing requirement, observed interface, or named correctness consequence.

UBR-R003. A related skill MUST expand beyond the concise default when the governing contract requires additional partitions or interactions, a material risk makes them necessary for the stage-owned conclusion, or the user explicitly requests deeper analysis.

UBR-R004. Automatic boundary coverage MUST preserve stage ownership: feature specs own normative boundaries, test specs own proof mapping, plans own sequencing, implementation owns the approved slice, and review or verification skills judge only their assigned gate.

UBR-R005. Formal feature specs and test specs governed by `boundary-first-v1` MUST retain the normalized boundary and proof records required by the standing proof-model contract; informal inspection and review responses MUST NOT be required to create a separate boundary artifact solely because the method was applied.

UBR-R006. The boundary-first activation record MUST describe behavior in the currently checked repository revision and MUST support exactly two independently valid checked-revision snapshots, `pending` and `active`, without using public tag existence or prior-revision history as the state discriminator. `pending` uses `-` for activating release, rollback release, and grandfathering baseline and uses an empty grandfathered-spec inventory. `active` uses `v0.4.0` as release intent, `v0.3.6` as rollback, one frozen grandfathering baseline provenance revision, and the frozen sorted grandfathered-spec inventory derived during activation preparation.

UBR-R007. Activation preparation MUST take the exact full reviewed pending-revision commit identity as an explicit input, derive the complete sorted grandfathered-spec inventory from that revision once, and record both values in one declarative active snapshot. Checked-revision activation validation MUST require the exact state fields from UBR-R006, one coherent `boundary-first-v1` contract version, canonical reference and resource identities, the ten-skill inventory, generated projection identity, adapter package set, and rollback metadata. It MUST reject missing, additional, stale, malformed, mixed, or divergent values, but MUST NOT require baseline reachability, prior-revision history, an activating tag, or network access to accept an active checked revision.

UBR-R008. Checked-revision activation success MUST identify the checked snapshot and release intent without reporting the release as tagged, published, publicly available, or publicly verified.

UBR-R009. The prepared release MUST use Git tag `v0.4.0`, npm package version `0.4.0`, npm dist-tag `latest`, and the existing routine release profile as the release identity authority.

UBR-R010. The `v0.4.0` canonical skills, generated Codex package, generated Claude package, generated opencode package, adapter archives, and npm package MUST contain equivalent mapped boundary resources and behavior.

UBR-R011. Routine release preparation, preflight, and full release verification MUST retain version consistency, generated drift detection, archive integrity, package-content validation, adapter metadata validation, packed installation and target initialization smoke, secret scanning, release-note validation, and rollback metadata checks.

UBR-R012. Public release MUST continue to use the existing routine release preparation, preflight, full verification, trusted tag workflow, and rerunnable public closeout, including GitHub asset validation, npm registry validation, and fresh public `npx` smoke for version and all three target initializers. Checked-revision activation MUST NOT retire, replace, or bypass this standard release-step mechanism.

UBR-R013. The unpublished custom activation-release experiment MUST be retired according to the following closed inventory. Candidate-only activation mode, candidate-result protocol, first-parent publication identity choreography, custom publication readiness, and custom atomic main-and-tag publication MUST NOT remain supported or selectable. The standing checked-revision structural validator, ordinary changed-path selection, and routine release mechanism in UBR-R011 and UBR-R012 MUST remain supported.

| Surface | Required disposition | Retained behavior |
| --- | --- | --- |
| `scripts/boundary_activation_release.py` | delete | None; the routine release mechanism owns release steps. |
| `scripts/publish-boundary-activation.py` | delete | None; the trusted tag workflow owns publication. |
| `scripts/test-boundary-activation-release.py` | delete | None; tests move to checked-revision activation and routine release owners. |
| `scripts/boundary_first_validation.py` | remove candidate and publication-readiness behavior | Structural records, canonical resources, projections, active checked-revision state, and rollback validation. |
| `scripts/validate-boundary-first.py` | remove candidate/publication CLI options | Focused local `--check` validation. |
| `scripts/test-boundary-first-validation.py` | remove candidate/publication-readiness cases and add checked-revision active-state cases | Structural, parity, privacy, grandfathering, and rollback regressions. |
| `scripts/validation_selection.py` | remove custom activation-release check and path dependencies | Ordinary boundary-first and routine release check selection. |
| `scripts/test-select-validation.py` | replace custom-path selection fixtures | Ordinary boundary-first and release selection regressions. |

UBR-R014. Lifecycle authoring, review, implementation, and verification MUST NOT create or push a public tag, publish GitHub or npm artifacts, merge a branch, or claim public availability; those actions remain explicit post-merge maintainer operations.

UBR-R015. The immutable `v0.3.6` release MUST remain the rollback selection and MUST retain complete passing adapter artifact metadata for Codex, Claude, and opencode.

UBR-R016. A failure before public tag publication MUST leave public release state unchanged; a failure after immutable publication begins MUST be recorded by phase and recovered through the existing rerunnable closeout, dist-tag correction or deprecation when applicable, or a later patch release, never by rewriting `v0.4.0`.

UBR-R017. Validation and release evidence MUST NOT expose credentials, tokens, OTPs, private environment values, usernames, hostnames, or machine-local temporary paths.

UBR-R018. Tests for concise default behavior MUST use representative specification, code-inspection, and code-review journeys and semantic assertions; they MUST NOT enforce exact prose, exact word counts, a fixed number of bullets, or the presence of the method name in user-facing output.

UBR-R019. Historical accepted feature specs MUST remain valid without migration. The frozen active grandfathered-spec inventory MUST remain the authority for historical exemption. After active checked-revision activation, new or substantively revised behavior specs outside that inventory MUST continue to adopt the standing normalized boundary record.

UBR-R020. An immutable `v0.4.0` tag MUST identify the exact reviewed release commit, and local or public checks MUST fail rather than treat a mismatched, rewritten, incomplete, or mixed-version release identity as success.

## Inputs and outputs

Inputs:

- the user's task, requested depth, and applicable project-local governing artifacts;
- the `boundary-first-v1` shared method, activation record, canonical resources, and ten governed skills;
- generated target packages and adapter archive metadata;
- the routine `v0.4.0` release profile, package metadata, release notes, pending evidence, and immutable `v0.3.6` rollback metadata;
- the exact reviewed release commit and, after explicit publication, public GitHub and npm evidence.

Outputs:

- concise stage-owned specifications, plans, implementation work, inspections, and reviews that cover material boundaries automatically;
- expanded analysis when required or requested;
- a checked-revision activation result that does not imply public publication;
- one coherent generated `v0.4.0` release package and routine validation evidence;
- post-publication closeout or phase-specific recovery evidence.

## State and invariants

- Each checked repository revision contains exactly one coherent `pending` or `active` activation snapshot, independently of public tag existence.
- The record is declarative rather than transactional: checked-revision validation makes no claim about the activation snapshot in any previous or future repository revision. Additional activation states and mixed field tuples are unsupported.
- `active` means the checked canonical and generated package surfaces agree on `boundary-first-v1`, the release-intent and rollback tuple is `v0.4.0`/`v0.3.6`, and the frozen grandfathering inventory is present; it does not mean publicly released.
- Public `v0.4.0` availability requires the immutable tag, trusted publication workflow, registry and asset evidence, and public closeout.
- The ten governed skills share one versioned method while retaining distinct stage responsibilities.
- Concision changes presentation and selection of applicable hazards; it never permits omission of a material correctness boundary.
- All published targets carry the same release version and mapped skill resources.
- `v0.3.6` and `v0.4.0` are immutable release identities.

## Error and boundary behavior

- A task with no admitted behavior boundary does not trigger invented scenarios or a boundary artifact.
- A material boundary that cannot be owned by a governing requirement blocks the stage and routes the gap upstream.
- A user request for deeper analysis expands applicable coverage but does not authorize unrelated scope.
- Missing, additional, stale, or divergent canonical, generated, adapter, version, or rollback surfaces fail validation with the affected surface identified.
- An active checked revision without `v0.4.0` may pass checked-revision activation validation but cannot pass a public-release claim.
- An active record with reachable or unreachable baseline provenance is judged from its frozen inventory and checked-revision identities; local validation does not inspect prior revisions or reconstruct a Git transition chain.
- A missing or mismatched release tag blocks release verification and publication.
- Unavailable public evidence keeps closeout open; it is not converted into success.
- Partial publication follows UBR-R016 and preserves immutable artifacts.

## Compatibility and migration

After this specification is approved and its lifecycle settlement is recorded, it supersedes `specs/boundary-first-v1-v0-3-7-activation-release.md`.
The matching `specs/boundary-first-v1-v0-3-7-activation-release.test.md`, `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`, and `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md` remain historical records of the cancelled design and are not release authority.

UBR-R013 is the normative and closed custom-experiment retirement inventory.
This cleanup does not retire or replace any routine release step named by UBR-R011 or UBR-R012.
If architecture discovers another surface that makes the unpublished custom experiment supported or selectable, that discovery routes to spec revision rather than silently expanding the retirement inventory.

The standing `specs/boundary-first-proof-model.md` contract remains authoritative with these exact activation-subject dispositions:

| Standing requirement subjects | Disposition in this specification |
| --- | --- |
| `PBF-R005`, `PBF-R005a` | Replaced for capability state by UBR-R006 through UBR-R008. Existing manifest identity fields remain, but `activating_release` is release intent and tag existence is not local activation proof. |
| `PBF-R005b` | Retained: architecture continues to own the activation-manifest path. |
| `PBF-R005c` | Replaced only for ongoing derivation: activation preparation receives the exact reviewed pending revision explicitly, derives and freezes the complete inventory once, and records both; later checked-revision checks use the frozen inventory without requiring Git reachability or transition-parent identity. |
| `PBF-R006` | Its complete coherent skill/resource/package precondition is retained by UBR-R007; its tag and transition-history activation preconditions are replaced. |
| `PBF-R007`, `PBF-R049a`, `PBF-R049b` | Retained using checked-revision state and the frozen grandfathered-spec inventory. |
| `PBF-R052` through `PBF-R056` | Retained for prospective adoption and historical compatibility, with `active` interpreted by UBR-R006 through UBR-R008. |
| `PBF-R057`, `PBF-R058` | Retained for exact `v0.3.6` rollback metadata and read-only package selection. |

The standing routine release transaction contract remains authoritative for release preparation, verification, publication, closeout, and historical immutability.

## Observability

Normal skill output identifies the material boundary or blocked outcome in plain language and remains summary-first.
Deeper detail is visible when the task or user requests it.

Checked-revision activation diagnostics identify the pending or active snapshot, contract version, release intent, affected resource or target on failure, and the corrective action.
They do not emit public-release success.

Routine release evidence identifies release and package versions, target parity, archive and package results, rollback release, validation phase, and public closeout state using the standing release evidence formats.

## Security and privacy

Ordinary boundary guidance requires no network access or credentials.
Checked-revision activation validation is read-only and local.
Trusted publication and public closeout use their existing credential boundaries, and committed evidence is limited by UBR-R017.

## Accessibility and UX

No graphical interface is introduced.
Users can request the work normally without learning the method name.
Default prose is concise and task-oriented; failures name the blocked outcome and corrective action; explicit requests for deeper analysis are honored.

## Performance expectations

Automatic boundary coverage MUST NOT add a separate user-visible workflow stage or network call to ordinary skill use.
Checked-revision activation validation MUST remain a focused local check and MUST NOT run publication or public smoke.
Routine preflight and full release verification retain their standing performance and timing-evidence contracts.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: UBR-R001, UBR-R002, UBR-R003, UBR-R004, UBR-R005, UBR-R006, UBR-R007, UBR-R008, UBR-R009, UBR-R010, UBR-R011, UBR-R012, UBR-R013, UBR-R014, UBR-R015, UBR-R016, UBR-R017, UBR-R018, UBR-R019, UBR-R020

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | UBR-R001, UBR-R002, UBR-R003, UBR-R018 | BND-INPUT-001 | - |
| state-lifecycle | applicable | UBR-R006, UBR-R007, UBR-R008, UBR-R014, UBR-R016, UBR-R019 | BND-STATE-001 | - |
| identity-authority | applicable | UBR-R009, UBR-R020 | BND-AUTH-001 | - |
| composition-path | applicable | UBR-R004, UBR-R005, UBR-R010, UBR-R011, UBR-R012, UBR-R013 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | UBR-R012, UBR-R016, UBR-R020 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | UBR-R015, UBR-R016 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | UBR-R006, UBR-R007, UBR-R013, UBR-R015, UBR-R019 | BND-COMPAT-001 | - |
| external-environment | applicable | UBR-R007, UBR-R012, UBR-R014, UBR-R017 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | UBR-R001, UBR-R002, UBR-R003, UBR-R018 | ordinary request; explicit deeper request; contract-required depth; no admitted behavior boundary | Material boundaries are covered once at the owning layer; depth does not invent scope. | Concise coverage, justified expansion, or no boundary-specific output; missing ownership blocks. | UBR-R002 |
| BND-STATE-001 | state-lifecycle | UBR-R006, UBR-R007, UBR-R008, UBR-R014, UBR-R016, UBR-R019 | coherent pending snapshot; coherent active/unpublished snapshot; malformed or mixed snapshot; tagged/publishing; published/closeout pending; closed | An active checked revision has one coherent release-intent, rollback, resource, projection, and frozen-inventory tuple; local validation makes no claim about prior or future revisions, never claims public availability, and lifecycle work never performs publication. | A coherent pending or active snapshot validates locally; a malformed or mixed snapshot stops; publication advances only under the routine release owner; partial publication remains open. | UBR-R006 |
| BND-AUTH-001 | identity-authority | UBR-R009, UBR-R020 | reviewed commit; local tag; immutable public tag; profile/package identity | The profile owns routine release values and the immutable tag names the exact reviewed release commit. | Exact identities pass; missing, rewritten, mismatched, or mixed identities stop. | UBR-R020 |
| BND-COMPOSE-001 | composition-path | UBR-R004, UBR-R005, UBR-R010, UBR-R011, UBR-R012, UBR-R013 | ten stage-owned skills; canonical and three generated packages; routine preparation, verification, trusted publication, closeout; retired custom path | No stage substitutes for another; all targets agree; only the routine release path is authoritative. | Complete paths produce coherent behavior and release evidence; bypass, drift, or custom-path reliance fails. | UBR-R013 |
| BND-TEMPORAL-001 | temporal-retry | UBR-R012, UBR-R016, UBR-R020 | pre-tag retry; immutable tag; delayed public evidence; rerun closeout; later patch | Pre-tag work is reversible; published identities are immutable; closeout is rerunnable. | Retry before publication, keep partial state open, or fix forward after publication; never rewrite the release. | UBR-R016 |
| BND-RECOVERY-001 | failure-recovery | UBR-R015, UBR-R016 | validation failure; publication unavailable; partial publication; runtime rollback | Failed validation cannot publish; recovery preserves immutable versions and uses one coherent package version. | Correct and retry, rerun closeout, issue a patch, or select exact v0.3.6 rollback. | UBR-R016 |
| BND-COMPAT-001 | compatibility-migration | UBR-R006, UBR-R007, UBR-R013, UBR-R015, UBR-R019 | pending snapshot; active frozen inventory; historical accepted specs; new or substantively revised specs; retired custom activation-release experiment; retained routine release mechanism; v0.3.6 rollback | Historical contracts remain valid; active checked-revision adoption uses the frozen inventory; the custom experiment is absent; the routine release mechanism remains authoritative. | Existing specs remain usable; new work adopts automatically; stale custom dependencies fail; routine release proceeds unchanged; rollback selects v0.3.6. | UBR-R019 |
| BND-ENV-001 | external-environment | UBR-R007, UBR-R012, UBR-R014, UBR-R017 | local checked revision; trusted GitHub workflow; GitHub assets; npm registry; public npx; unavailable external evidence | Checked-revision activation needs no network; public claims require public evidence; private values never enter evidence. | Local proof can pass independently; external unavailability blocks only its owned public claim or keeps closeout open. | UBR-R012 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | UBR-R002, UBR-R003, UBR-R004, UBR-R005 | BND-INPUT-001, BND-COMPOSE-001 | Automatic coverage becomes either superficial or an exhaustive repeated checklist across stages. | Each stage covers its owned material boundaries once; required depth expands only the applicable part. |
| INT-002 | UBR-R006, UBR-R008, UBR-R009, UBR-R012, UBR-R014, UBR-R020 | BND-STATE-001, BND-AUTH-001, BND-ENV-001 | An active checked revision is mistaken for a publicly released version. | Checked-revision activation may pass without a tag, but only the exact immutable tag and public evidence support the public-release claim. |
| INT-003 | UBR-R010, UBR-R011, UBR-R012, UBR-R013, UBR-R015, UBR-R016 | BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001 | Removing the custom experiment also removes or replaces the original routine release mechanism, parity, verification, or rollback protection. | Only the custom experiment is retired; the original routine release steps, parity, verification, immutable recovery, and exact v0.3.6 rollback remain mandatory. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | regression | UBR-R001, UBR-R002 | BND-INPUT-001 | REG-UBR-001 | - |
| E2 | illustration | UBR-R001, UBR-R002 | BND-INPUT-001 | - | - |
| E3 | illustration | UBR-R003 | BND-INPUT-001 | - | - |
| E4 | regression | UBR-R006, UBR-R008 | BND-STATE-001 | REG-UBR-002 | - |
| E5 | illustration | UBR-R010, UBR-R011, UBR-R012 | BND-COMPOSE-001 | - | - |
| E6 | regression | UBR-R015, UBR-R016 | BND-RECOVERY-001 | REG-UBR-003 | - |

## Edge cases

EC1. A trivial wording or non-behavior task admits no material boundary; the skill completes without a synthetic matrix.

EC2. A contract requires a boundary the user did not mention; the skill covers it because governing requirements outrank default brevity.

EC3. The user asks for deep analysis of one risk; that risk expands without expanding unrelated dimensions.

EC4. A formal spec has all eight dimensions but only two are applicable; the other six use concise requirement-grounded non-applicability rationales.

EC5. Canonical skills are active but one generated target is stale; checked-revision activation fails and identifies the stale target.

EC6. The active checked revision has no `v0.4.0` tag; checked-revision activation passes, while release verification and public-release claims remain blocked.

EC7. A local or public `v0.4.0` tag points anywhere except the exact reviewed release commit; release validation fails.

EC8. Public GitHub assets exist but npm or one target's public smoke is unavailable; closeout remains open and rerunnable.

EC9. A retired custom helper remains, a candidate-only option is still accepted, or a selector still selects the custom experiment; AC-UBR-008 fails until the exact UBR-R013 disposition is satisfied.

EC10. Checked-revision activation is implemented by replacing or bypassing routine release preparation, preflight, verification, trusted publication, or closeout; validation fails because UBR-R012 preserves those original release steps.

## Non-goals

- No redesign of the eight-dimension `boundary-first-v1` proof model.
- No mandate to enumerate every dimension as prose in informal user-facing responses.
- No semantic completeness claim from deterministic structural validation.
- No exact word-count, wording-snapshot, or fixed-scenario-count checker.
- No second release mode, custom activation publisher, atomic main-and-tag protocol, or generalized pre-tag candidate protocol.
- No weakening of the existing routine release gate, package parity, installation smoke, secret controls, public closeout, or immutable rollback.
- No automatic merge, tag, push, GitHub release, npm publication, or rollback action.
- No rewrite of historical accepted specs or immutable release evidence.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-UBR-001 | The E1 specification and E2 inspection journeys cover coherent pending and active snapshots, their named missing, additional, malformed, mixed, unknown, frozen-inventory, compatibility, and public-call boundaries without requiring the method name. |
| AC-UBR-002 | E1 and E2 omit tag, network, publication, and provider-outage analysis from checked-revision validation, while E3 proves the exact custom-experiment surfaces are removed and checked-revision validation, routine release, and rollback behavior remain. |
| AC-UBR-003 | Formal adopting specs retain valid normalized boundary records, and informal journeys are not forced to emit a separate record. |
| AC-UBR-004 | An active checked revision with the exact UBR-R006 snapshot tuple, explicit baseline provenance and frozen inventory from UBR-R007, and coherent checked-revision identities passes local activation validation without a `v0.4.0` tag, baseline reachability, network access, prior-revision proof, or a public-release claim. |
| AC-UBR-005 | Missing, stale, additional, or divergent canonical, governed-skill, generated-target, adapter, version, or rollback surfaces fail with bounded diagnostics. |
| AC-UBR-006 | The routine `v0.4.0` profile, package, notes, pending evidence, and generated packages agree on `v0.4.0`/`0.4.0`, `latest`, and Codex, Claude, and opencode support. |
| AC-UBR-007 | The original routine preparation, preflight, full release verification, packed installation, archive/package integrity, trusted publication, public smoke, and rerunnable closeout gates remain present and effective. |
| AC-UBR-008 | Every UBR-R013 `delete` surface is absent, every `remove` surface rejects or omits candidate/publication behavior, retained checked-revision behavior still passes, and ordinary selection cannot select the custom experiment. |
| AC-UBR-009 | `v0.3.6` remains an exact complete rollback package, and partial or failed `v0.4.0` publication follows immutable fix-forward recovery. |
| AC-UBR-010 | No lifecycle stage before explicit post-merge release action mutates external publication state or claims public availability. |
| AC-UBR-011 | Concision tests use semantic representative journeys and do not enforce exact prose, word count, bullet count, or method-name output. |
| AC-UBR-012 | Every UBR-R001 through UBR-R020 requirement and every selected boundary interaction has direct proof in the matching test specification. |

## Open questions

None.

## Next artifacts

- Spec review.
- Architecture assessment and architecture review, including retirement of the custom publication ADR and its implementation surfaces.
- A small execution plan and plan review.
- A focused test specification and test-spec review.
- Implementation, milestone code review, explanation, verification, and PR handoff.
- Explicit post-merge routine release publication and public closeout.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.
Implementation is not yet allowed.
