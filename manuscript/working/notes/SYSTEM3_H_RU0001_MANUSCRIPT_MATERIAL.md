# System 3 H/Ru(0001): evidence-to-prose note

**Status:** WORKING MANUSCRIPT NOTE / NOT YET PROMOTED INTO MAIN TEXT  
**Program authority:** SymC General Operations Manual v0.8.0

This file is the staging area for H/Ru(0001) manuscript material. It deliberately separates current evidence from publication-ready prose while the System-3 gates continue to resolve.

## Current evidence that may be described now

### Preserved historical numerical failure

The original selected L17/V15/K16 clean-surface representation failed its prospectively required coupled endpoint recheck on the k-mesh axis. The K16-to-K20 change in surface excess was about 2.478685 meV/surface atom, outside the unchanged 1.000 meV criterion. The layer and vacuum axes were inside tolerance.

Publication-safe interpretation:

> The original K16 surface representation was rejected by its coupled numerical gate. That HOLD remains part of the Limit Map and was not relaxed or retrospectively reclassified.

### P0-Q dense-k qualification

A separately frozen K20/K24/K28 diagnostic mapped the dense-k region. K20 was outside the terminal K28 tolerance while K24 was inside. The diagnostic did not authorize production directly; under the predeclared selection rule it nominated K24 for a fresh successor qualification.

Publication-safe interpretation:

> The failed K16 representation informed a versioned P0-Q successor search rather than a threshold change. Diagnostic evidence was used to choose the successor candidate but was not reused as its fresh PASS evidence.

### Fresh successor fixed-grid PASS

Run `34769372617` produced a fresh four-case qualification at L17/V15/K24:

| Case | Surface excess, eV/surface atom | Difference from base, meV/surface atom |
|---|---:|---:|
| L17 / V15 / K24 base | 1.0945347456436139 | 0 |
| L19 / V15 / K24 | 1.094699510587816 | 0.164764944 |
| L17 / V15 / K28 | 1.094842506423447 | 0.307760780 |
| L17 / V25 / K24 | 1.0945327047920728 | 0.002040852 |

All endpoint differences are inside the unchanged 1.000 meV/surface-atom criterion. The adjudicated status is `CLEAN_SURFACE_FIXED_GRID_PASS`.

Important claim ceiling:

- phase = P0-Q;
- all four cases are fresh for the successor gate;
- diagnostic energies were not reused as PASS evidence;
- original K16 HOLD is preserved;
- this is not untouched P1 confirmation.

### Foundational robustness challenge

Before the fixed-grid PASS is inherited by substantial downstream H/Ru work, a fresh L21/V15/K24 challenge is being completed. The prospectively frozen stronger test requires BOTH:

- |gamma_L21 - gamma_L17| <= 0.001 eV/surface atom;
- |gamma_L21 - gamma_L19| <= 0.001 eV/surface atom.

If both survive, the layer-depth robustness challenge closes without an automatic L23/L25 ladder. If either fails, the affected foundation is reopened while the historical minimum-gate PASS remains a true record of what that earlier gate decided.

**Do not write in the main manuscript yet:** that L17 is the final inherited substrate. That depends on the unresolved L21 result and the subsequent relaxation/reproduction gate.

## External validation evidence already identified

### Clean Ru(0001) structure

Published LEED-IV and surface X-ray diffraction studies report roughly 2% outermost interlayer contraction for clean Ru(0001), with hydrogen contamination/coverage explicitly investigated. These should become an external validation comparison after our relaxation is complete, not a target used to tune the relaxation.

### H/D vibrational structure

Published high-resolution HREELS has mapped H and D perpendicular/parallel modes, coverage dependence, lateral coupling, and dispersion on Ru(0001). This is a strong future validation target for computed local vibrational modes.

### H diffusion

McIntosh et al. (J. Phys. Chem. Lett. 2013, DOI 10.1021/jz400622v) provide open-access HeSE H/Ru(0001) diffusion data from 75-250 K. The study reports:

- quantum effects visible to about 200 K;
- low-temperature tunneling plateau around 1.9 x 10^9 s^-1;
- fitted fcc-hcp site-energy difference 22.2 +/- 0.6 meV at 250 K;
- DFT fcc-hcp difference about 50 meV in that study;
- DFT bridge diffusion barrier about 150 meV, reduced to about 120 meV with harmonic ZPE;
- multiple jumps interpreted as relatively low adsorbate-substrate friction.

These values are **external comparators**, not inputs for selecting our adsorption site, path, barrier, bead count, or friction model.

## Dissipation state

The refreshed literature audit remains:

`QUANTITATIVE_H_ADATOM_DIFFUSION_FRICTION = NOT_ESTABLISHED`

but adds:

`QUALITATIVE_LOW_FRICTION_CONSTRAINT = SUPPORTED`

H/Ru electronic-friction models exist for H2 dissociation/scattering and associative desorption, and tensorial friction calculations exist for other adsorbates on Ru(0001). Those establish methodology/process relevance but are not coordinate-matched numerical friction for thermal/tunneling H-adatom fcc-hcp diffusion.

Main-manuscript consequence:

- acceptable: discuss low-friction HeSE signature as an external qualitative constraint;
- unacceptable: turn that signature or the jump rate into a numerical damping coefficient;
- unacceptable: transplant H2 desorption/scattering friction to H-adatom diffusion;
- future route: compute a matched friction tensor/kernel and project it onto our independently validated diffusion coordinate.

## Quantum implementation state

Current environment planning identifies QE 7.6 and i-PI 3.2.0 as the present candidate version pair for a new qualification. Production PIMD remains unauthorized until socket syntax, force exchange, restart, client topology, resources, and electronic-force reproducibility are qualified for exact versions.

The scientific bead ladder and convergence rule remain unchanged from the existing System-3 protocol. Agreement with the HeSE rate curve may not choose bead count or quantum method.

## Prospective manuscript insertion point

If the L21 challenge and clean-surface relaxation/reproduction both pass, a System-3 subsection can be inserted after the engine/Atlas foundations and before broad interpretation, with this structure:

1. why H/Ru(0001) is a difficult-limit test;
2. preserved K16 numerical failure;
3. P0-Q successor selection without threshold retuning;
4. fresh K24 fixed-grid PASS;
5. bounded L21 foundational robustness;
6. clean-surface relaxation/reproduction and experimental structure comparison;
7. unbiased adsorption/PES/path construction;
8. classical and quantum rate hierarchy;
9. independently matched dissipation or explicit refusal;
10. only then any licensed scalar/modal/system stability interpretation.

## Claims explicitly withheld today

- final inherited L17 substrate;
- `SURFACE_READY`;
- issued H/Ru substrate certificate;
- computed adsorption-site ordering from the new System-3 pipeline;
- new H/Ru diffusion barrier;
- new classical or quantum rate;
- numerical H-adatom friction/damping;
- H/Ru mechanical chi;
- exceptional point associated with H/Ru diffusion;
- predictive validation of ChemSA from System 3.

This note should be updated as each gate adjudicates. Main-text promotion should occur only when a statement no longer depends on an unresolved upstream gate.
