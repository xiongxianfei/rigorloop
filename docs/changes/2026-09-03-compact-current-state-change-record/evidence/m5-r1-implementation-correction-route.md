# M5 R1 implementation correction route

Change ID: 2026-09-03-compact-current-state-change-record
Source stage: code-review
Destination artifact: implement
Reason: upstream-proof-gap
Finding IDs: CCSR-M5-CR1
Return stage: code-review
Lifecycle revision: sha256:0d3e6258f7db50b71e1c7f819f8be6e1a60c2fbd911f0e3457c99af12d5377fe

The correction is limited to making both exact-change and project-level `workflow-context` use the complete bounded compact reader and adding the corresponding public regressions.
