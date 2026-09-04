# M1 R1 specification correction route

Change ID: 2026-09-03-compact-current-state-change-record
Source stage: implement
Destination artifact: spec
Reason: upstream-contract-gap
Finding IDs: CCSR-M1-CR1
Return stage: implement
Milestone: M1
Lifecycle revision: sha256:27f0562b7cc4e0434928bd70efd8d32db071faefbaafdb0a8276f43b52496e23

Code Review M1 R1 found that SR-21 requires change identity, lifecycle-contract identity, and lifecycle revision in a skill-context projection while the exact closed Projection schema omits and therefore forbids those fields. The active M1 Implementation stage routes that upstream contract gap to the specification owner and requires return to Implementation before the milestone can close.
