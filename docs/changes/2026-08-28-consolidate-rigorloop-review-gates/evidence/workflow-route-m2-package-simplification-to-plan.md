# Workflow route: M2 package simplification to plan

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Source stage: code-review
Destination artifact: plan
Reason: upstream-contract-gap
Finding IDs: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
Return stage: code-review
Lifecycle revision: sha256:44c3b5a2c2472e77bcd021e6f008ddacb39ce8b1255a29c573542206002c35c7

The approved specification and architecture remove aggregate package identity. The M2 plan must replace its aggregate and hash proof obligations with visible member maps, governed invalidation, non-approved blockers, and finding-owner mapping before implementation resumes.
