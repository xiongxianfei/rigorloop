# Workflow Correction Route: Milestone Deadlock Architecture

Change ID: 2026-08-24-governed-lifecycle-cli
Source stage: verify
Destination artifact: architecture
Reason: upstream-ownership-gap
Finding IDs: RLCLI-DEADLOCK-CR1
Return stage: verify
Lifecycle revision: sha256:b7fd1632d0f3d4e9e8ec17478546e0af77c115508cf64e7a8fc12f95bf3f3d61

The approved specification now separates milestone completion from workflow-selected start and requires a durable, evidence-complete replay identity. Architecture must define the smallest persistence and component boundary needed to implement those requirements without granting the CLI workflow-selection authority.
