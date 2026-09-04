# M3 R3 proposal correction route

Change ID: 2026-09-03-compact-current-state-change-record
Source stage: implement
Destination artifact: proposal
Reason: upstream-contract-gap
Finding IDs: CCSR-M3-CR2
Return stage: implement
Milestone: M3
Lifecycle revision: sha256:918a914c555e83fdd93b85228ef36247240df0929cb3376bf1f00f3badd926c1

Code Review M3 R3 found that the approved design allowed callers to construct
derived lifecycle state and did not fully define evidence dependency resolution
or direct subject freshness without Git. The correction routes those decisions
to Proposal. Return requires a newly registered and independently accepted
proposal; the affected Design, Delivery, and implementation packages must then
be refreshed before M3 can continue.
