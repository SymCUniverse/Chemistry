# CO/Cu(111) GOM v0.8.0 Migration Audit v0.1

**Date:** 14 September 2026  
**Status:** NON-COMPUTE GOVERNANCE/READINESS AUDIT  
**Program authority:** SymC General Operations Manual v0.8.0

## Executive result

The existing CO/Cu(111) continuation architecture is compatible with the GOM v0.8.0 scientific core. No threshold or scientific parameter should be changed merely because the program manual was consolidated. The main current limitation is evidentiary rather than architectural: repository routes are wired and frozen, but live external Kaggle execution is not established from repository state, so the lane must not be described as actively computing without independent runtime evidence.

No substrate-inheritance certificate is issued by this audit.

## Existing route review

### L15/L17 diagnostic continuation

`KAGGLE_L15_L17_RESILIENT_CHECKPOINT_ROUTE_v0.2.json` is frozen before its first scientific L15/L17 production result. It preserves the existing scientific protocol and explicitly treats the microcheckpoint cadence as execution bookkeeping rather than a scientific parameter.

Its current safeguards are GOM-compatible:

- exact scientific protocol remains unchanged;
- original L17 HOLD remains preserved;
- threshold, cutoffs, geometry, coverage, k-mesh, ESM, pseudopotential, binary, and rank are not changed by the recovery route;
- no absolute clean-surface PASS is claimed from the route itself;
- direct one-rank execution remains fixed;
- remote advancement occurs only after checkpoint metadata verification;
- old safe checkpoint state is not discarded before a newer state is verified;
- zero-paid route is explicit.

The 900 s clean-stop request cadence is execution risk control, not a claim that durable persistence occurs every 900 s. The existing caveat correctly states that QE writes only at safe points and persistence adds latency.

### L19 continuation

`KAGGLE_L19_RESILIENT_ROUTE_v0.2.json` is frozen before the Kaggle L19 result and preserves the pre-existing `L19-V40-K36-extension-audit` scientific protocol.

Its GOM-compatible controls include:

- no change to layer count, vacuum, k-mesh, cutoffs, pseudopotential, binary, execution rank, force gate, reproduction gate, or surface-excess gate;
- preservation of the original L17 HOLD;
- independent L15/L17 and L19 execution lanes;
- scientific reconciliation only after both results exist;
- exact remote checkpoint hash verification before slot advancement;
- no paid-compute escalation.

## GOM v0.8.0 mapping

| GOM control | CO/Cu state |
|---|---|
| Truth over continuity | Historical HOLDs preserved; no route file converts them into PASS. |
| P0-Q controlled qualification | Current depth work remains qualification/iteration, not untouched confirmation. |
| Function Map + Limit Map | Existing failures/resource boundaries and depth continuation should be retained alongside any eventual usable region. |
| Foundational dependency | A future surface PASS should receive bounded robustness proportional to the downstream work that will inherit it; no automatic infinite depth ladder is implied. |
| Recovery without retuning | Current Kaggle routes alter persistence/execution bookkeeping while explicitly freezing science. |
| Active-run monitoring | Applies only after a live Kaggle run is independently verified. A wired launcher is not an active process. |
| Refusal | Resource failure, unresolved depth sensitivity, or missing live provenance remain legitimate HOLD outcomes. |
| Migration integrity | CO/Cu-specific numerical protocols remain project-local; their details are not expected to live in the domain-neutral GOM. |
| Substrate inheritance | Certificate remains NOT_YET_ISSUED until the exact successor model satisfies its required numerical/reproduction gates. |

## Current claim ceiling

The strongest repository-supported current statement is:

> CO/Cu(111) has versioned, zero-paid, resumable P0-Q continuation routes for the frozen L15/L17 diagnostic and the frozen L19 depth extension, with historical HOLDs preserved. Repository readiness does not establish that either route is presently executing or that a clean-surface substrate certificate has been earned.

Do not claim from repository state alone:

- live Kaggle execution;
- final L15/L17 or L19 scientific outcomes;
- converged substrate depth;
- issued substrate certificate;
- adsorption-site ordering newly established by these continuation routes;
- reaction barrier/rate/dissipation/chi validation.

## Work that can proceed without live compute

1. Maintain exact launcher/driver hashes and freeze checks.
2. Prepare a current-state ledger that distinguishes WIRED, LIVE, VALID, and ADJUDICATED rather than using one word such as active.
3. Predefine how L15/L17 and L19 evidence will reconcile if they agree, disagree, or one remains incomplete.
4. Predefine the bounded foundational robustness question that would apply after any minimum clean-surface PASS.
5. Prepare the substrate-certificate template without issuing it.
6. Audit manuscript text so CO/Cu historical results and current continuation are not conflated.
7. Add live-run monitor coverage only after independent evidence that a Kaggle session is actually running.

## Migration decision

`GOM_V0_8_0_COMPATIBLE_WITH_LOCAL_CONTROLS = true`

`SCIENTIFIC_SETTINGS_CHANGED = false`

`THRESHOLDS_CHANGED = false`

`HISTORICAL_HOLDS_PRESERVED = true`

`LIVE_KAGGLE_EXECUTION_VERIFIED = false`

`SUBSTRATE_CERTIFICATE_STATE = NOT_YET_ISSUED`
