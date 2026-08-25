# Plan Validation Scope Correction Route

Change ID: 2026-08-25-workflow-routed-upstream-corrections
Source stage: implement
Destination artifact: plan
Reason: upstream-planning-gap
Finding IDs: none
Return stage: implement
Lifecycle revision: sha256:e7990fe4ae72b31e1b07e47707dede0254ae0c76796eb92b18ab0894fcb8746d

The M3 validation selected the release-tag gate for a feature branch. Feature verification must use the repository CI wrapper and leave the immutable published-release checks to a release checkpoint.
