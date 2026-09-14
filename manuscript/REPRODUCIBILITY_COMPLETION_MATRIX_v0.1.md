# Chemistry Reproducibility Completion Matrix

Version: 0.1
Status: ACTIVE

The Chemistry manuscript will report reproducibility at three distinct levels rather than using a single undifferentiated reproducibility label.

## R1 — release integrity and regeneration

Required closure items:
- canonical repository commit identified;
- immutable archive generated from the canonical commit;
- SHA-256 recorded;
- dependency lock or exact environment specification preserved;
- test suite and validator counts reported without mixing real scientific tests and drift/integrity checks;
- clean-room extraction verified;
- generated artifacts regenerated where the release claims regeneration;
- stale release references removed from manuscript and supplement.

Current state: PARTIALLY SUPPORTED BY HISTORICAL RELEASE WORK; FINAL MANUSCRIPT RELEASE NOT YET FROZEN.

## R2 — recomputation of scientific quantities

Required closure items:
- raw or licensed input identity preserved;
- exact system configuration and scientific parameters preserved;
- deterministic preprocessing/calculation steps documented;
- computational outputs recomputable from preserved parent inputs;
- checkpoint lineage retained for long-running workflows;
- manual transformations eliminated or explicitly scripted/audited;
- numerical tolerances and acceptance gates versioned;
- independent rerun or recomputation performed for the quantities used in the final manuscript where feasible.

Current state: PENDING TERMINAL COMPUTATIONAL EVIDENCE FOR ACTIVE SYSTEMS.

## R3 — reconstruction of primary evidence and provenance

Required closure items:
- source identity and retrieval pathway recorded for literature-derived values;
- exact table/equation/text location recorded where available;
- units and transformations preserved;
- same-system/phase/temperature/medium/reaction-event matching auditable;
- source-family dependence recorded;
- FULL/ABSTRACT/SNIPPET/BLOCKED evidence tier retained;
- blocked or inaccessible sources do not silently become verified evidence;
- Atlas and Engine provenance remain independent.

Current state: ACTIVE; FINAL ATLAS PROVENANCE AUDIT PENDING.

## Manuscript release gate

The final manuscript may say only what the closed R-levels justify. For example, a clean-room test of a frozen output package is an R1 statement unless it actually recomputes the scientific quantity from its declared parent inputs, in which case it may also support R2. Bibliographic traceability is not automatically R3 unless the numerical source and transformation can be reconstructed.
