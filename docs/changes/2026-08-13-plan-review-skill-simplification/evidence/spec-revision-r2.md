# Spec Revision R2 Evidence

- Owner: `spec`
- Trigger: deterministic boundary validation during test-spec review preparation
- Finding: the approved spec omitted the required top-level activation marker, which had prevented deterministic validation from exposing over-broad example ownership rows; one proof row also included two requirements not governed by its cited state boundary
- Change: added `boundary_contract: boundary-first-v1`, narrowed each multi-boundary example row to requirements governed by every cited boundary, and narrowed `PRF-002` to the state boundary's approved requirement set
- Semantic effect: none; the examples remain illustrations, and the proof cases continue covering all requirements while their ownership metadata now follows the approved boundary contract
- Required next stage: formal `spec-review` of the corrected revision before test-spec review resumes
