# Retire standalone architecture and ADR authoring from Design

## Challenge

The Design skill supports living Designs and also carries a separate path for creating, rebuilding and amending standalone architecture documents and ADRs. Its legacy templates, technical procedure and required package checks keep that older authoring contract active. The preceding simplification retained compatibility by scope, without establishing a current project need for it.

## Goals

Make living Designs the skill's supported architecture and decision authoring output. Reduce the extra guidance and package obligations while preserving applicable requirements, decision rationale and historical meaning in existing project documents.

## Scope and non-goals

| Work | Treatment | Bound |
| --- | --- | --- |
| Retire standalone architecture/ADR authoring and its two skill-local scaffolds | core to this proposal | Remove the old-format create/rebuild/amend path; existing documents remain inspectable inputs. |
| Reconcile owning Designs, skill guidance, reviewer/author consumers, repository template copies, tests and package checks | same-slice dependency | Remove exclusive support and prevent dangling dependencies; preserve independently useful concerns and diagram styles. |
| Preserve source authority and decision history during scoped adoption into living Designs | core to this proposal | Require explicit authority and obligation reconciliation; no automatic conversion, deletion or retargeted approval. |
| Retire customer feature-spec/proof contracts, old records or unrelated skill capabilities | out of scope | These are separate supported responsibilities; this change targets standalone architecture/ADR authoring. |
| Migrate user repositories, release, install or publish | out of scope | Package qualification does not authorize external changes. |

## Governing principle

Preserve the engineering meaning without maintaining an unnecessary authoring format.

## Proposed direction

Use the existing living-Design authoring method for architecture and decisions. Read older architecture documents and ADRs as source material and historical evidence, preserving their current authority until an authorized scoped adoption reconciles the affected responsibility. A project that requires old-format output receives a clear unsupported-output explanation and an owner decision, rather than silent conversion or a reconstructed legacy method.

Remove the legacy authoring instructions and scaffolds together with their exclusive consumers. Keep useful technical concerns in their living-Design owner and preserve decision context, alternatives, consequences and provenance. Existing project documents and old review judgments are not cleanup targets. Reconcile any duplicate repository template aids according to actual dependencies. Detailed requirement changes, resource selection and proof allocation belong to Design and Delivery.

## Feasibility

Feasible within the current skill architecture. `skills/design/SKILL.md` explicitly maps the two scaffolds and `legacy-technical-authoring.md`; the Design model defines their contract, while named validator resources and skill tests enforce their presence. Living-model technical guidance and a design skeleton already provide the replacement authoring method. No known dependency prevents Design work, but the dependency audit must distinguish exclusive legacy support from feature-spec support, reusable technical obligations and historical assessment evidence.

## Impact and major trade-offs

This intentionally removes a supported output path. Projects still requiring standalone architecture/ADR edits cannot use the refined skill for that output without first choosing an authorized scoped adoption or another authoring tool. We have not established that no such external project exists; the decision trades that compatibility for a simpler supported method. Installation alone must never change a project's contracts or documents.

## Decision requested

Approve retiring standalone architecture/ADR authoring while retaining source interpretation and explicit, obligation-preserving adoption into living Designs. Preserve the separate customer feature-spec contract and reconcile the affected guidance, templates and validation in one reviewed change.
