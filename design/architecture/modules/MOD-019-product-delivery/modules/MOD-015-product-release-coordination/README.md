# Release coordination

Responsibility and allocation are defined in [module.json](module.json). The [Release contract](release.md) owns qualification, workflow-start authority, publication and recovery for the implemented CLI and Codex/Claude packages.

## How to publish

Start with the [publication procedure](release.md#publication-procedure). It explains selecting the right merged source, initiating the selected release, qualifying and retaining packages, publishing automatically and checking the public outcome.

## Architecture views

| Question | Owning explanation |
| --- | --- |
| Who cooperates during successful publication? | [Process: publication sequence](#publication-flow) |
| What happens after failure or uncertain publication? | [Process: recovery flow](#publication-recovery) |
| How is the release code organized? | [Development: workflow and helper dependencies](#release-code) |
| Where does it run, and where are artifacts and evidence stored? | [Physical: jobs, execution boundary and providers](#release-placement) |

The D2 diagrams below are registered in `browser-views.toml` and rendered into the existing architecture browser. This README owns the diagram source; `release.md` owns the detailed publication contract and procedure. Observed source structure does not establish candidate qualification, remote configuration or publication success. Proposed customer-browser delivery remains separately scoped in the Module model.

These views describe the checked-in workflow and helpers: authorized workflow initiation followed by automatic publication after checks, with no second human approval. They do not establish deployed configuration or a successful public release; remote setup must satisfy the [Adoption boundary](release.md#adoption-boundary). This refinement retains existing release evidence persistence; simplifying that storage is separate pending design work.

## Publication flow

A permitted push to protected `main` initiates and authorizes the selected release for its exact event source and established configuration. The workflow prepares and qualifies packages before publication. No later maintainer confirmation is requested. A local or PR validation run has no publication authority. [Release contract](release.md#runtime-view) defines binding, failure and retry rules.

Preparation and execution remain separate jobs. Prepared packages means retained workflow artifacts, not a new service. Release status and evidence uses the existing durable reporting ref until its separate simplification is designed. GitHub/npm groups destinations for readability; publication is not an atomic transaction across them.

<!-- architecture-diagram: publication-flow -->
```d2
shape: sequence_diagram
prepare: "Preparation"
maintainer: "Maintainer"
executor: "Executor"
artifacts: "Prepared packages"
providers: "GitHub / npm"
evidence: "Release status and evidence"
maintainer -> prepare: "Initiate release through\nauthorized main push"
prepare -> prepare: "Bind event source;\nbuild and check packages"
prepare -> artifacts: "Retain candidate\nand check results"
artifacts -> prepare: "Return retained\nartifact binding"
prepare -> executor: "Continue automatically\nafter required checks pass"
executor -> artifacts: "Retrieve bound\noriginal candidate"
artifacts -> executor: "Return exact artifacts\nand source bundle"
executor -> executor: "Validate inputs,\nbinding and authority"
executor -> evidence: "Record initiating run\nand candidate binding"
evidence -> executor: "Confirm durable save"
executor -> providers: "Inspect next\npublication boundary"
providers -> executor: "Return observed\npublic state"
executor -> executor: "Classify missing work\nand check authority"
executor -> evidence: "Record write intent"
evidence -> executor: "Confirm durable save"
executor -> providers: "Publish retained bytes\nfor this boundary"
providers -> executor: "Return post-write\nidentity facts"
executor -> executor: "Confirm exact\npublic match"
executor -> evidence: "Record boundary\noutcome before advancing"
executor -> executor: "After all boundaries,\nrun fresh install smoke"
executor -> providers: "Read public packages,\nassets and identities"
providers -> executor: "Return public artifacts\nand identity facts"
executor -> executor: "Assess smoke and\nrechecked identities"
executor -> evidence: "Record completed\nacceptance and outcome"
evidence -> executor: "Confirm durable closeout"
executor -> maintainer: "Report actual outcome\nand limitations"
```

The publication-boundary portion applies in the implemented order: **tag → GitHub assets → npm**. Before each write, the executor revalidates exact inputs and initiating authority, inspects current public state and persists write intent. It records the observed result before advancing. The sequence compresses that repeated portion once; it does not show a single combined provider write or skip intermediate evidence. Final public smoke and identity rechecks follow all required matching boundaries. Optional evidence mirroring is supplementary to durable closeout, not a new permission or publication of changed product bytes.

A failed check, missing initiating authority, existing matching publication, uncertain response, partial publication or reporting failure leaves this successful path and follows [Publication recovery](#publication-recovery). Successful command return alone does not establish a public result.

## Publication recovery

This flow selects the next safe action from the actual state. It does not automatically retry an unsuccessful publication command. Qualification, candidate identity, authority and durable support remain prerequisites for every affected action. Detailed rules: [Publication procedure](release.md#publication-procedure).

<!-- architecture-diagram: publication-recovery -->
```d2
direction: down
problem: "Failed check, interruption\nor uncertain outcome"
basis: "Can the original candidate\nand authority still be relied on?" {
  shape: diamond
}
inspect: "Inspect retained evidence\nand actual public state"
state: "Observed publication state" {
  shape: diamond
}
missing: "Persist intent; perform only\nconfirmed authorized missing work"
checks: "Repeat affected public checks\nand reconcile reporting"
stop: "Stop affected work\nRetain facts and required correction"
done: "Record confirmed outcome\nand actual limitations"
problem -> basis
basis -> stop: "Unauthorized start, failed qualification,\nchanged binding or unavailable original"
basis -> inspect: "Same qualified candidate\nand applicable authority"
inspect -> state
state -> missing: "Absent or supported incomplete state;\nmissing write confirmed and authorized"
missing -> inspect: "Observe actual result\nbefore continuing"
state -> checks: "Existing product publication matches"
state -> stop: "Conflicting identity or\nstate remains unknown/unavailable"
checks -> done: "Required checks and\ndurable closeout succeed"
checks -> stop: "Checks or required reporting fail"
```

Before any public write, preparation or authority failure returns to its responsible owner; a corrected material basis needs a new authorized workflow start and qualified candidate. After a write may have occurred, preserve the original candidate and inspect each destination separately. Matching earlier stages stay intact; only confirmed missing, still-authorized work can continue. Delayed visibility permits bounded observation, not blind republishing. A conflict or uncertainty that cannot be resolved stops affected work with an incomplete result.

When product publication already matches but smoke or reporting fails, repeat the affected checks or repair reporting against that same candidate. Do not republish product bytes to fix evidence, overwrite conflicting public identity, or describe a cancelled run as undoing a write. If durable reporting is unavailable, preserve the private observation artifact and report the gap; completion cannot be claimed until required closeout is reconciled. A queued run retains its event source; newer source cannot replace its packages. Cancelling a run requires applicable authority and does not undo completed writes.

## Release code

Development: release code and dependencies. Detailed rules: [Release contract](release.md#building-block-view).

<!-- architecture-diagram: release-code -->
```d2
direction: down
workflow: ".github/workflows/release.yml\nJob ordering and permissions"
entry: "scripts/release-coordinator.py\nHosted command entry"
coordination: "scripts/lib/release/release_coordination.py\nSetup, candidate and initiation binding"
candidate: "release_candidate.py\nIsolated build, checks and sealing"
execution: "release_execution.py\nPublication, observation and evidence"
transaction: "release_transaction.py\nProfile, preflight and closeout helpers"
packaging: "Packaging helpers and validators\nMOD-013 production and MOD-014 install proof"
workflow -> entry: "prepare / execute"
entry -> coordination: "Dispatch operation"
coordination -> candidate: "Prepare and seal exact candidate"
coordination -> execution: "Restore, execute and recover"
candidate -> transaction: "Derive and check intent"
candidate -> packaging: "Build archives, metadata and packed CLI"
execution -> candidate: "Verify retained identity"
execution -> transaction: "Validate public closeout"
```

## Release placement

Release job placement and destinations declared by the workflow, without a second approval gate. Detailed rules: [Release contract](release.md#deployment-view).

<!-- architecture-diagram: release-placement -->
```d2
direction: down
github: "GitHub Actions" {
  prepare: "Prepare runner\nRead-only provider access"
  artifacts: "Retained candidate\nArtifacts and checks"
  execute: "Execute runner\nWrite and OIDC permissions"
  recovery: "Recovery artifact\nObserved outcome"
}
source: "Protected main\nExact event commit"
maintainer: "Maintainer"
releases: "GitHub tag\nand release assets"
npm: "npm registry\nTrusted publishing"
evidence: "Durable evidence\nSeparate Git ref"
source -> github.prepare: "Read selected commit"
github.prepare -> github.artifacts: "Upload once\nReuse on retry"
maintainer -> source: "Initiate authorized\nrelease through main push"
github.artifacts -> github.execute: "Retrieve and verify\nexact binding"
github.prepare -> github.execute: "Checks pass; proceed\nwithout another approval"
github.execute -> releases: "Publish and\nobserve"
github.execute -> npm: "Publish and\nobserve"
github.execute -> evidence: "Persist actual\noutcomes"
github.execute -> github.recovery: "Retain recovery\nobservations"
```
