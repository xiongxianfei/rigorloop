# Skill parent test design

Owner: [Skill](../skill.md), model ID `skill`. Shared test-quality rules belong to [System](../../test-design/rules.md#start-from-supported-outcomes).

This package covers recurring capability and resource contracts, recording paths, implementation authority and cross-capability handoffs. The [case index](test-cases.json) declares five JSON groups. The [model inventory](../skill.md#context-and-scope) supplies responsibility boundaries. Select scenarios for a distinct observable failure; a parent requirement or discovered method does not need its own catalog row.

## Coverage and proof dependencies

Derive scenarios from current requirements and plausible failures, then inspect the actual assertions. A method that checks instruction wording proves that wording or structure. It cannot establish that an agent makes the correct decision, respects authority or produces useful work. Keep those outcomes in explicit review procedures with concrete inputs, counterexamples and expected decisions.

SKL-AR-004 relies on [Authoring's composition cases](../authoring/test-design/test-cases.json) for internal refinement and handoffs. SKL-AR-006 checks the boundary between [Assessment's Verify](../assessment.md) and [Delivery Handoff](../delivery-handoff.md). SKL-RC-010 interprets [Packaging's resource-identity evidence](../../engineering/packaging.md). SKL-RX-008 compares recording outcomes with the supported [CLI](../../cli/cli.md) and [Records](../../cli/records.md) contracts. These references support specific observations in the catalog.

The standing scenarios reference 28 parent requirements within their existing applicability. SKL-SR-19/21/22/23/30/32/33 remain scoped rollout, source-transfer, improvement and inventory-acceptance duties under their original owners and initiative references in [Skill](../skill.md#requirements). This focused catalog does not transfer, settle or execute those duties; they are outside its recurring coverage. No requirement is retired. References establish a bounded account, not complete coverage or an executed assessment. System's shared maintenance rules and Authoring's current move/handoff scenarios retain their own responsibilities.

## Case groups and proof limits

| Group | Cases | Distinct protection |
| --- | ---: | --- |
| [Capability contract](cases/capability-contract.json) | 10 | Shared entry structure, actual description-length edge, canonical-source selection, validator tool independence, capability choice and safe sufficient evidence. |
| [Resource contract](cases/resource-contract.json) | 9 | Mapped verbs, inventory agreement in both directions, containment, source-copy identity and the distinction between runtime loading, package validity and authority. |
| [Recording composition](cases/recording-composition.json) | 8 | Entry classification reaches the exact complete reference; portable and governed paths, late triggers and recording results remain distinct. |
| [Implementation handoffs](cases/implementation-handoffs.json) | 7 | Current CI declaration grammar and Implement handoff; separate Bugfix write authority and original-proof identity; separate CI admission, concurrent replacement and partial recovery. |
| [Capability composition](cases/capability-composition.json) | 3 | Support inputs retain their decision owner; verified PR handoff retains current identity and external authority; current presentation preserves specialist meanings and stops. |

The draft contains **37 cases**: 19 automated-test designs and 18 independent-review procedures. The automated population links **33 distinct existing methods**: 15 cases are `existing` at their stated observation boundary and four are `partial`. The 18 review procedures are `proposed`; that describes their authored realization, not 18 missing executable tests or a claim that no prior reviews occurred. Actual results and exact reviewed identities belong in evidence.

The [native Skill entrypoint](../../../../tests/skill/test-skill-validator.py) also discovers specialist tests outside this parent scope. Do not require its total method count to equal the parent links. Check that every linked method is actually discoverable and report a required outcome with unresolved ownership as a gap. An unlinked method alone does not justify deleting a regression or claiming its coverage elsewhere.

## Derivation and observation

Use equivalence partitions for valid, missing, wrong-class, escaped and unreadable inputs. Use decision tables for declaration precedence and authority combinations; state transitions for missing/matching/drifted copies and late invocation triggers. Apply boundary values to real limits such as the 1024-character description boundary. Properties cover absence of target-agent execution and preservation of authority through handoff. A walkthrough needs explicit starting facts, a decision or artifact to inspect, a counterexample and an independently expected outcome.

Keep the smallest useful observation boundary and retain composition where it exposes additional failures. SKL-RX-003 protects selection of the named reference even when correct words exist elsewhere; generic resource existence does not establish that property. SKL-CC-007 exercises the real command with target-tool traps; importing a helper cannot establish command independence. SKL-RX-006/007 examine the complete invocation path; phrase-presence tests cannot establish those decisions.

SKL-IH-001's unknown CI assembly competes with missing and duplicate known entries. Its expected single unknown-value diagnostic is stronger than a generic rejection. SKL-RC-007 requires exactly the unknown-consumer diagnostic and guards resource reads for both policy validators; its linked tests now establish those observations.

Resource-map absence, an unlisted present file and a listed missing file are named variations of one inventory-agreement boundary in SKL-RC-002; the linked scenario retains each specific diagnostic and establishes an accepted private baseline before each omission. Bugfix write authority and original-proof identity remain separate in SKL-IH-003/007. CI admission, a target changed before commit, and interruption after one valid write remain separate in SKL-IH-004/005/006 because they observe different authority and persistence states. SKL-AR-004 checks support-input consumption; SKL-AR-006 separately checks verified external handoff. Consolidation does not authorize deleting executable tests or hiding distinct failure mechanisms.

## Review fixture basis

Every review packet identifies the actual current owner and selected canonical body, triggered references/assets and project authority. The case supplies concrete starting facts and a deliberately incorrect candidate decision or artifact alongside its compliant control. Inspect those candidates against the governing outcome; matching case wording or document headings cannot establish the result. Variants use fresh independent packets, not successive mutations that depend on an earlier review.

| Fixture fact | Interpretation and observation |
| --- | --- |
| Proposed action and artifact | Describe permitted writes and the exact output/decision to inspect. A negative candidate changes one material fact or claim; preserve the remaining valid setup. |
| Synthetic identity labels | F0 is the inspected CI file, F1 its prepared replacement and F2 a concurrent replacement. G0/G1/G2 play the same roles for the second target. S0/S1 identify differing verification subjects. Labels assert only equality or difference within the fictional packet; actual evidence records actual inspected identities. |
| CI operation | The case explicitly supplies review/revise authority, required privilege choices and available commit primitives. Check proposed preserved bytes and reported effects without writing a real workflow or contacting hosted CI. |
| Cross-capability input | The packet includes producer identity, evidence limits, receiving owner and actual authority. A finding, project map, lesson or Verify result contributes only what its owner established. |
| Evidence/privacy counterexample | E_CONFIG, timeout_seconds and TOKEN_PLACEHOLDER are fictional report fields, not a real diagnostic vocabulary or credential. Inspect whether the proposed evidence request retains relevant safe facts and excludes unnecessary private data. |

Record the exact inspected packet, candidate, expected difference and observed decision through the existing evidence owner when a review is performed. These are proposed walkthroughs; they do not run an agent, prove target-agent compliance, create record-store examples or authorize external actions.

## Fixtures and script organization

Executable sources remain under `tests/skill/`, with the current aggregate entrypoint and cohesive behavior files. [Fixture helpers](../../../../tests/skill/skill_fixture_helpers.py) own setup operations; [recording fixtures](../../../../tests/skill/skill_contract_tests.py) independently declare the selected profiles. Existing authored fixture directories are read-only inputs. New mutation-based implementations should use a fresh temporary root, establish a valid baseline, change the named field and assert its exact outcome. Do not derive expected values or supported names from validator registries.

Use ordinary test functions or framework groups; `unittest.TestCase` supplies framework grouping, not a required domain-object hierarchy. A small context manager or resource object is useful when it owns one coherent lifetime. Keep the defining mutation, expected diagnostic and authority observation visible in the case. Share setup, not a helper that computes the expected answer with production logic. Split files by responsibility and setup cohesion when that improves navigation; line count alone is not a split rule.

Use real filesystem paths for containment and byte-copy claims. Substitute target tools with observable traps only when testing their prohibited invocation. Review fixtures use synthetic requests and proposed outcomes against exact current package subjects. A reading-path walkthrough does not run an agent, mutate production, write workflow records or contact an external provider. If future work needs runtime-agent evaluation, its environment, authority, repeatability and limits need an explicit design and evidence allocation.

## Inspected gaps

The four partial cases retain existing protection and state the additional intended observation. SKL-CC-002/004 use separate malformed fixtures without demonstrating the same accepted baseline before mutation. SKL-CC-003 lacks the competing-inconsistency precedence observation. SKL-CC-005 lacks the just-below and at-limit description cases. SKL-RC-001–004 now use accepted private packages and visible mutations; SKL-RC-007 observes exclusive unknown-consumer diagnostics without resource reads. These are bounded executable observations, not independent review approval.

Semantic review remains necessary for usable output, appropriate evidence selection, resource-trigger decisions, specialist mutation boundaries, independent handoffs and useful simplification. Existing canonical text checks remain valuable bounded regression evidence, but linking them would not justify marking those larger claims `existing`.

## Catalog contract

This Skill draft has its own owner and format names. `format_version: 2` identifies the provisional representation defined below. The index records covered behavior and evidence limits; case realization records pending proof.

| Object | Required fields | Optional fields and constraints |
| --- | --- | --- |
| Index | `format` = `skill-test-catalog-draft`; integer `format_version` = 2; `owner`, `scope`, `fixture_rules`, nonempty `groups`. | No other fields. |
| Owner | Nonempty `model`, `design`, `test_design`. | Model is `skill`; paths identify the parent and this strategy. Identical in every group. |
| Index scope | Nonempty strings `model`, `boundary`, `entrypoint`, `coverage_claim`. | No other fields. Boundary names covered behavior; coverage claim states the extent and limits of the evidence. |
| Fixture rules | Nonempty strings `isolation`, `independent_expectations`, `negative_setup`, `version_roles`, `resource_boundary`. | No other fields. |
| Index group | Nonempty `id`, `title`, `path`. | IDs and paths are unique; paths name files inside this package's `cases/`. |
| Group file | `format` = `skill-test-cases-draft`; integer `format_version` = 2; `owner`, `scope`, nonempty `fixtures`, nonempty `cases`. | No other fields. |
| Group scope | Nonempty `group`, `title`, `boundary`. | Group and title agree with the index. |
| Fixture | Nonempty local `id`; nonempty string array `initial_state`. | Callable `builder`; exact `reference_test`; string file `profile`; nonempty object `facts`; nonempty fixture-relative path array `expected_changed_paths`; string `limitation`; group-local `extends` ID. Omit absent fields. |
| Case | Nonempty `id`, `title`, `risk`; nonempty unique requirement-ID array `requirements`; `technique`, `method`, `boundary`, `target`, `given`, nonempty string arrays `when` and `then`, `realization`. | Nonempty `variants` array. |
| Given | Local fixture ID `fixture`; nonempty string array `conditions`. | No other fields. |
| Variant | Nonempty case-local `id`; nonempty descriptive object `parameters`. | Variant IDs are unique within a case. |
| Callable/test reference | Nonempty repository-relative `path` and exact `symbol`. | Python methods use `Class.method`; source and symbol must exist. |
| Review target | Nonempty repository-relative `path` and exact Markdown `section`. | No callable symbol or invented executable test. |
| Realization | `state`, array `tests` of unique exact test references, string array `gaps`. | Empty arrays follow the state rules below. |

Reject duplicate JSON keys, unknown structural fields and unknown closed values before reference/consistency checks. All nonempty strings contain non-whitespace content. IDs begin with an ASCII letter and otherwise contain letters, digits and hyphens; group, fixture and variant IDs use lowercase. Case IDs are unique across the entire parent catalog and survive wording/group moves. Variant identity is `(case ID, variant ID)`. Do not reuse retired IDs.

`method` is `automated-test` or `independent-review`. `boundary` is `contract`, `public-command`, `composition` or `review`. Automated targets are callable references with a non-review boundary; review targets use exact document sections and the review boundary. `technique` is `equivalence-partition`, `boundary-values`, `decision-table`, `state-transition`, `property`, `fault-injection` or `walkthrough`. These vocabularies separate execution method, observation boundary and derivation technique.

`realization.state` is `existing`, `partial` or `proposed`. Existing requires tests and no gaps; partial requires tests and gaps; proposed requires no tests and at least one explicit gap or pending real-subject review. Independent-review cases have no executable test links and remain proposed procedures regardless of prior run results. These states never report pass/fail or independent approval.

Repository references use normalized POSIX relative paths without absolute prefixes, `.`/`..` components or symlink traversal. Referenced files must be contained readable regular files. Fixture-relative paths are a separate private-root namespace. Facts and variant parameters are descriptive JSON values, with finite numbers; they cannot dispatch commands. Optional `extends` refers to an acyclic group-local setup basis, with no implicit field merge, execution or class inheritance. Requirement references resolve to the Skill parent's current requirement table.

## Validation and maintenance

Author checks parse the exact index and five groups, validate shape/vocabularies/IDs/paths/fixtures, resolve source and section references, and confirm native discovery of the selected test links. Run applicable parent/prose checks and the referenced native tests. Those checks establish structure and bounded existing observations; independent review assesses whether conditions and expected outcomes expose the intended defect.

[Validation's Skill admission contract](../../engineering/validation.md#skill-parent-test-design-admission-contract) defines package admission. A passing main-model check does not establish catalog admission. Implementation allocation and observed tooling limitations are recorded in the [owning change](../../../changes/2026-09-17-model-test-design/change.json).

Update the account when behavior, source paths, fixtures, discovery or responsibility ownership changes. Keep each scenario with its primary owner, preserve stable IDs and reconcile affected current links. A later child catalog owns its detailed requirements and references parent interactions; it does not copy these 37 cases. Record deliberate case consolidation, splits and scope transfers once in the owning change; keep no live aliases and never reuse retired case IDs. Remove exclusive obsolete tests only after their owner retires the obligation or establishes adequate replacement protection and reconciles consumers; an unlinked test or absent case is not removal permission. Delivery allocates future executable changes and commands; actual outcomes remain in evidence bound to exact subjects.

Feature-format withdrawal relies on Authoring AUTH-SH-005 for unsupported-output and authorized-adoption meaning. Skill retains package-resource and capability-composition observations: current declared methods must be present and contained, while retired feature/proof resources cannot remain as transitive dependencies. Existing catalog groups remain the parent observation boundaries; removing resource entries does not retire package integrity.
