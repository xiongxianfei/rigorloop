# Architecture assessment

Stage: architecture-assessment
Applicability: required
Route: architecture-required
Spec identity: sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029
Assessment mode: workflow-managed
Authoring action: canonical-update-with-adr

The feature changes the CLI package's cross-command result boundary, adds machine-local persistence and cross-process rotation, and introduces a compatibility-gated default migration. The smallest sufficient package is a focused canonical architecture update plus one ADR. No C4 diagram changes are required because the affected components remain inside the existing CLI package container.
