# Design Review R8 specification correction route

Change ID: 2026-09-03-compact-current-state-change-record
Source stage: design-review
Destination artifact: spec
Reason: upstream-contract-gap
Finding IDs: CCSR-DR8-1
Return stage: design-review
Lifecycle revision: sha256:4eae0c68f983809932f49fa5ef0f93da0090d98e10cf1a6381532fe242654baa

Design Review R8 requires the transient semantic correction input to be separated from the durable correction record so callers cannot supply evaluator-owned kind or status fields.
