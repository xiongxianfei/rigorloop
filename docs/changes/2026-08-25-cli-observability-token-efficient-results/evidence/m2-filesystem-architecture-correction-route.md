# M2 Filesystem Architecture Correction Route

Change ID: 2026-08-25-cli-observability-token-efficient-results
Source stage: code-review
Destination artifact: adr-cli-observability
Reason: upstream-contract-gap
Finding IDs: CLIOBS-M2-R4-F1, M2-L1B-F2
Return stage: code-review
Lifecycle revision: sha256:32022c5c177ca2f06f426c5915440d2f94d6f71446728a64db5b17ff54c7fa93

The accepted ADR describes revalidation but does not delimit the guarantees available from portable Node pathname APIs. It must align its mechanism, consequences, and threat model with approved specification `sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba`.
