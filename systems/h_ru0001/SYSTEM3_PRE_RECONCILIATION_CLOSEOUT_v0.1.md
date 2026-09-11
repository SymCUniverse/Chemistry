# System 3 H/Ru(0001) pre-reconciliation closeout v0.1

**Date:** 2026-09-11  
**Status:** `NON_COMPUTE_PRE_RECONCILIATION_WORK_CLOSED`  
**Current scientific phase:** P0-Q  
**Critical-path compute:** post-HOLD K20/K24/K28 dense-k diagnostic, run `34560002560`

## Purpose

This record separates work that can be completed without the remaining clean-surface numerical result from work that genuinely depends on that result. It prevents documentation, governance, literature admissibility, provenance, and implementation planning from being deferred until the computational reconciliation finishes.

## Closed before reconciliation

### General Protocol adoption

The chemistry program now has an explicit v0.7.1A mapping in `governance/CHEMISTRY_GENERAL_PROTOCOL_v0.7.1A_ADOPTION_v0.1.json`.

The current H/Ru k-mesh investigation is P0-Q qualification and Function/Limit mapping. A successor version may learn from qualification evidence without erasing the original failure or representing the reused evidence as untouched P1 confirmation.

### Current H/Ru state lineage

`SYSTEM3_STATE_LEDGER_v0.2.json` supersedes the stale current-state use of v0.1 while preserving v0.1 historically. It records:

- Ru bulk prerequisite: adjudicated PASS;
- L15/L17/L19 layer extension: adjudicated PASS;
- selected non-terminal depth: L17;
- coupled endpoint recheck: adjudicated scientific HOLD;
- failed axis: k-mesh;
- K20/K24/K28 post-HOLD diagnostic: active P0-Q;
- relaxation: blocked until a versioned successor fixed-grid qualification and required coupled PASS.

### Historical HOLD preservation

`SYSTEM3_POST_EXTENSION_COUPLED_HOLD_RECORD_v0.1.json` permanently preserves the K16-to-K20 coupled failure. Any successor grid may establish a new qualified model but cannot retroactively relabel the original candidate.

### Manuscript integration

`SYSTEM3_MANUSCRIPT_INTEGRATION_v0.2.md` now contains the actual present evidence rather than the old pre-computation placeholder. It already includes the Ru bulk PASS, layer-extension PASS, coupled k-mesh HOLD, P0-Q Function/Limit interpretation, claim fence, and downstream promotion firewall.

Final numerical values from the current K24/K28 diagnostic can be inserted later without having to redesign the manuscript logic.

### Reproducibility preflight

`SYSTEM3_REPRODUCIBILITY_PREFLIGHT_v0.1.json` has already bound the current run IDs, commits, artifact identities/digests, evidence roles, package requirements, and final-assembly firewalls. The package structure therefore no longer waits on reconciliation design.

### Dissipation-source admissibility

`SYSTEM3_DISSIPATION_COORDINATE_LITERATURE_AUDIT_v0.1.md` closes the obvious public-source audit at the current evidence state.

Current conclusion: `DISSIPATION_NOT_ESTABLISHED`.

No currently identified public source supplies an independent, coordinate-matched projected friction for lateral atomic-H diffusion on Ru(0001). HeSE dephasing is not automatically reaction-coordinate friction, the explicit H/Ru fitted friction found in later theory is outcome/tuning-linked to the hopping-rate comparator, and H2/Ru electronic-friction calculations use different reaction coordinates/state points.

This is a legitimate claim limit, not missing bookkeeping. It does not block upstream surface/path/quantum science, but it blocks any claim requiring independent H/Ru dissipation or chi until that evidence exists.

### Quantum implementation readiness

`SYSTEM3_QUANTUM_IMPLEMENTATION_READINESS_AUDIT_v0.1.md` closes the architecture question before reconciliation.

Quantum ESPRESSO plus i-PI remains a documented viable architecture. Exact interface conventions are version-dependent, so future production must freeze exact QE/i-PI versions and pass a socket smoke test plus resource-scaling/environment qualification. Production PIMD is not yet authorized, but there is no unresolved architectural question that needs to wait for the clean-surface result.

### Barrier Atlas relationship

Barrier Height/Rate Atlas v0.9 remains a separate frozen retrospective evidence product. Current System 2/System 3 compute cannot silently rewrite it. Atlas expansion is not a prerequisite for closing the present H/Ru clean-surface claim.

### CO/Cu execution readiness

The repository-side L15/L17 and L19 Kaggle launchers remain the audited routes. Their readiness does not establish that Kaggle is currently executing. Live runtime state remains unverified unless direct Kaggle evidence is obtained.

### Claim-specific stopping rule

The project no longer treats every possible deeper layer, denser mesh, or longer run as automatically required for submission. Once a stated claim is adequately qualified or honestly bounded, additional calculations may continue as robustness, Function Map, or Limit Map evidence. Material contradictions discovered by such runs must still be preserved and investigated.

## What genuinely remains compute-dependent for clean-surface reconciliation

1. Complete K24 and K28 at fixed L17/V15 under the frozen diagnostic and adjudicate K20/K24/K28 against terminal K28 using the unchanged 0.001 eV/surface-atom rule.
2. If the diagnostic identifies a usable dense-k region, create a versioned P0-Q successor fixed-grid protocol that explicitly states it was informed by the preserved qualification evidence.
3. Qualify that successor fixed-grid model under its required independent checks, including the coupled endpoint recheck appropriate to the successor.
4. Only after `CLEAN_SURFACE_FIXED_GRID_PASS`, execute the already separated clean-surface relaxation and independent reproduction gate.
5. If the dense-k diagnostic does not identify a stable region, preserve that result and decide the next bounded P0-Q map from the observed numerical behavior. Do not loosen the 1 meV threshold merely to obtain PASS.

## Work after SURFACE_READY that is not part of current reconciliation

These remain real scientific stages, but none needs to delay the current numerical reconciliation bookkeeping:

- unbiased H adsorption-site screen and numerical sensitivity;
- local vibrational stability at the computed minimum;
- ordinary NEB, CI-NEB, and saddle-mode verification;
- classical harmonic baseline;
- exact-version quantum compute-environment qualification and PIMD/QTST tier;
- any future reopening of the dissipation search if genuinely new coordinate-matched evidence becomes available;
- stability/chi representation only after its semantic and evidence gates are satisfied.

## Finish-line definition for this waiting period

The non-compute pre-reconciliation backlog is considered **closed**. From this point, the clean-surface critical path is driven by new numerical evidence rather than missing governance, manuscript architecture, provenance planning, or obvious literature-admissibility work.
