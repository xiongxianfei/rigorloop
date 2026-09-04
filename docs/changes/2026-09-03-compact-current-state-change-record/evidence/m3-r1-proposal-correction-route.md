# M3 R1 proposal correction route

Change ID: 2026-09-03-compact-current-state-change-record
Source stage: implement
Destination artifact: proposal
Reason: upstream-contract-gap
Finding IDs: CCSR-M3-CR1
Return stage: implement
Milestone: M3
Lifecycle revision: sha256:f7603df7372fed25943b9247252531cad6e3204d6bf55fd61ead13b0e875a35f

Code Review M3 R1 found that a caller-supplied authority field cannot authenticate the process invoking a local CLI. The active M3 implementation therefore routes the trust-boundary correction to Proposal. Return requires the refined proposal to be registered and independently accepted; downstream Design, Delivery, and affected implementation judgments must then be refreshed before M3 continues.
