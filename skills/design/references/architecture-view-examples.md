# Architecture views by responsibility

These two synthetic examples are excerpts illustrating overview boundaries, view selection and reference ownership. They are not complete model documents, proposed components, executable services or an exhaustive test list. A real model supplies its own requirements, decisions and acceptance scenarios. Use the structure only when it fits the project's responsibility; do not copy these component names into unrelated systems.

## Composed example: document validation

Assume a project validates documents against an existing product contract. The author owns document corrections; an independent assessor judges whether the results justify acceptance. Validation owns check selection and execution but cannot grant acceptance.

```mermaid
flowchart TB
    Contract["Product contract<br/>What must be protected"]
    Request["Requested verification scope"]
    subgraph Validation["Document validation"]
        Criteria["Proof criteria<br/>Useful checks and independence"]
        Catalog["Check catalog<br/>IDs, commands and constraints"]
        Selection["Selection<br/>Required IDs and reasons"]
        Executor["Executor<br/>Dependencies and bounded parallel work"]
        Results["Results<br/>Outcomes, diagnostics and incomplete work"]
        Criteria -.->|"guides authors maintaining checks"| Catalog
        Catalog -->|"available checks"| Selection
        Catalog -->|"trusted commands and constraints"| Executor
        Selection -->|"required checks"| Executor
        Executor -->|"actual outcomes"| Results
    end
    Contract -->|"required behavior"| Criteria
    Request -->|"scope"| Selection
    Results -->|"evidence and limitations"| Assessor["Independent assessment"]
```

The [context detail](#context-detail) owns inputs and consumers. The [building blocks](#building-block-detail) own local responsibilities; [runtime detail](#runtime-detail) owns ordered cooperation. The overview summarizes those subjects and keeps the independent assessor outside the validation boundary. Dashed guidance is distinct from executable data flow. The boxes need not become separate models or processes.

| Supporting view | Necessary and why | Owning detail |
| --- | --- | --- |
| Context | Yes: scope, behavioral authority and assessment belong to distinct external owners. | [Context detail](#context-detail) |
| Building Block | Yes: trusted catalog, selection and execution have distinct responsibilities. | [Building-block detail](#building-block-detail) |
| Runtime | Yes: failure must leave dependent work visibly incomplete. | [Runtime detail](#runtime-detail) |
| Deployment | No for this excerpt's abstract method: no executable placement or environment is selected. An actual process implementation must reassess resource and deployment boundaries. | This explicit limit; no deployment correctness claim. |

### Context detail

```mermaid
flowchart LR
    Contract["Product contract owner"] -->|"required behavior"| Validation["Document validation"]
    Caller["Caller"] -->|"documents and scope"| Validation
    Validation -->|"outcomes and limitations"| Assessor["Independent assessor"]
```

The caller supplies documents and scope; the product owner defines the accepted behavior. The assessor consumes results and owns the acceptance decision. Validation neither edits the documents nor assumes a passing command grants approval.

### Building-block detail

```mermaid
flowchart LR
    Criteria["Proof criteria"] -.->|"maintenance guidance"| Catalog["Catalog"]
    Catalog -->|"available identities"| Selection["Selection"]
    Catalog -->|"commands and constraints"| Executor["Executor"]
    Selection -->|"selected identities and reasons"| Executor
    Executor -->|"actual observations"| Results["Results"]
```

The catalog owns check identity and command constraints; selection owns requested scope, and execution consumes both. Results own the factual account, including missing work. Criteria guide authors and reviewers instead of automatically judging adequacy.

### Runtime detail

```mermaid
flowchart TB
    Select["Select required checks"] --> Preflight["Validate inputs and dependencies"]
    Preflight --> Gate{"Valid and ready?"}
    Gate -->|"yes"| Run["Run ready checks within budget"]
    Gate -->|"no"| Stop["Report rejection without launching work"]
    Run --> Depend{"Prerequisite passed?"}
    Depend -->|"yes"| Continue["Run dependent checks"]
    Depend -->|"no"| Incomplete["Report dependent work not started"]
    Continue --> Report["Report actual outcomes"]
    Incomplete --> Report
```

Selection is not execution evidence. A failed prerequisite prevents dependent execution and remains visible in the aggregate result. Independent assessment consumes the resulting account under its own criteria.

## Leaf example: label normalization

Assume a pure function trims leading/trailing ASCII spaces, preserves interior characters, rejects non-string input and touches no external state. Its single responsibility does not justify additional submodels.

```mermaid
flowchart LR
    Caller["Caller"] -->|"label value"| Input["Input boundary"]
    subgraph Normalization["Label normalization"]
        Input -->|"string"| Trim["Trim outer ASCII spaces"]
        Input -->|"non-string"| Reject["Reject invalid input"]
    end
    Trim -->|"normalized string"| Caller
    Reject -->|"input error"| Caller
```

The input, transformation and error relationships are owned by the behavior stated in this excerpt. The caller owns any storage, authorization or presentation. No persistent artifact or deployed component is implied.

| Supporting view | Necessary and why | Owning detail |
| --- | --- | --- |
| Context | No separate view: the only external relationship is one synchronous caller, fully specified by the function boundary above. | The stated input/output contract. |
| Building Block | No separate view: this leaf has no material internal decomposition beyond the single pure transformation. | The stated normalization behavior. |
| Runtime | No separate view: no interacting components, state transition, retry or concurrency protocol exists. | Deterministic return/error behavior above. |
| Deployment | No: placement and storage belong to the caller, and this function has no environment-sensitive behavior. | Caller responsibility above. |

This is a necessity assessment, not a size exemption. Adding locale dependence, shared state or an asynchronous caller protocol would require reassessment.

## Counterexamples for review

- A validation diagram puts “approve change” inside the executor: reject the abstraction because evidence production has taken the assessor's decision authority.
- The overview adds a store or service that has no owning contract: identify the missing owner or remove the unsupported element before accepting the design.
- Runtime is declared necessary because checks have prerequisites, but only the overview is drawn: require the missing runtime view and its failure behavior.
- Context and runtime disagree about who may initiate publication: reconcile the actual authority owner rather than merely relabeling arrows.
- Every child repeats the parent's detailed rules: keep one owner and reference it; a second diagram cannot become a competing contract.
- A leaf has four empty diagrams solely to fill the template: reassess necessity and keep reasoned dispositions, while retaining its required overview.
