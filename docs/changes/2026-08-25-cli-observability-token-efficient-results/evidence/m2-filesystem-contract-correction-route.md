# M2 Filesystem Contract Correction Route

Change ID: 2026-08-25-cli-observability-token-efficient-results
Source stage: code-review
Destination artifact: spec
Reason: upstream-contract-gap
Finding IDs: CLIOBS-M2-R4-F1, M2-L1B-F2
Return stage: code-review
Lifecycle revision: sha256:0478e6a286b6ed75c1c2b372a3e010f9195c4b947c6d8bd0a3c15d28bc3cc505

The approved contract requires pathname operations to remain beneath a resolved root but does not state whether concurrent hostile replacement by another same-user process is inside the threat model. Portable Node built-ins cannot bind `rename` and `unlink` to a previously opened directory handle on all supported platforms. The specification owner must define the supported actor boundary before M2 can implement and prove the requirement honestly.
