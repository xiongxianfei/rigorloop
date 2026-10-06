# Development View

## Development View

The Development View answers:

> How is the architecture realized in the static organization of software used for development, build, testing, and maintenance?

Prefer these semantic inputs:

- Module software realization;
- implementation/source/package mappings;
- applications, libraries, services, workers, adapters, jobs, or other software units when material;
- build/package dependencies that matter architecturally;
- concrete Interface implementation/binding relationships where useful;
- test groups and the responsibilities or contracts they assess;
- test observation boundaries, including material substitutions and their limits;
- fixtures, test helpers, selection catalogs, runners, entrypoints, and build or installed artifacts required by those groups.

The Development View MUST NOT redefine Module boundaries or parent-child containment from current package or source layout.
It shows how hierarchical logical responsibility is realized by software organization, including deliberate many-to-many mappings when they exist.
Its component names may match the Logical technical structure, but its relationships explain source units, package dependencies, builds and maintenance. A component-and-contract overview belongs to Logical; source organization is more than a filename inventory and can be designed before files exist. Keep these projections attributable to one technical design instead of maintaining competing component definitions.

Development describes intended software organization independently of implementation progress. Its design can be authored and reviewed before source files, builds or tests exist. Keep software units, material dependencies, build/resource relationships and test architecture grounded in the governing requirements and architectural decisions. Existing source mappings and observed behavior provide supporting traceability and conformance information; they do not automatically define or approve the intended design. Preserve their qualification and any divergence. A design-oriented presentation should lead with the design and rationale, with implementation references available separately; missing references do not invalidate a design, and references alone do not fill a design gap. This design/observation distinction applies across all five views.

### Test architecture

The Development View SHOULD explain the static organization of the test system when it is material to understanding or maintaining the architecture. Show coherent behavior groups and their dependencies, rather than an inventory of every test case. Make it possible to find the assessed responsibility, governing coverage contract, test sources, fixture/support sources, and execution entrypoints.

A test group **assesses** a responsibility; it does not thereby **implement** that responsibility. Keep the owner of the protected behavior, the owner of shared test execution tooling, and the owner of evidence assessment distinct. Recording tests alongside a Module's realization provides subject context without assigning all referenced fixtures, runners, or CI infrastructure to that Module. Shared dependencies should be referenced where used and described at their authoritative owner. A missing architectural allocation for execution tooling remains an explicit gap until responsibility analysis resolves it.

Record observation boundaries and material limits, including substituted dependencies and required artifacts. A direct source test, a public command test, and an installed-product test observe different boundaries. A source path, test catalog entry, or coverage mapping alone establishes neither adequate coverage nor passing execution.

Use the other concerns for complementary information: Process explains material scheduling, concurrency, isolation, timeouts and cleanup; Physical explains execution environments and infrastructure. Verification defines the assessment, Evidence records actual observations, and the resulting judgment retains its scope. Static test dependency arrows must not imply runtime order, requirement satisfaction, or an executed test result.
