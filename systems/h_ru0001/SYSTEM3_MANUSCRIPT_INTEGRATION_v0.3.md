# System 3 H/Ru(0001) manuscript integration record v0.3

**Status:** CURRENT EVIDENCE INTEGRATION / P0-Q QUALIFICATION WITH FOUNDATIONAL ROBUSTNESS HOLD  
**Supersedes for current state:** `SYSTEM3_MANUSCRIPT_INTEGRATION_v0.2.md`  
**Historical files remain preserved.**  
**Program authority:** SymC General Operations Manual v0.8.0

## Role of System 3

H/Ru(0001) remains a difficult-limit system for the ChemSA computational methodology. Its role is not to establish universality and not to force a scalar stability description. The purpose is to determine how far an evidence-gated chemistry workflow can progress while preserving failures, identifying the operating region of each representation, and refusing unsupported promotion.

The present clean-surface work is **P0-Q controlled qualification**. Qualification failures may inform a versioned successor model, but they may not be rewritten as untouched confirmation.

## Language and claim rule

Conventional chemical and numerical terminology controls each statement. Exceptional point, critical damping, phase boundary, kinetic crossover, stability boundary, adsorption minimum, transition state, and related terms are used only when the governing equations and evidence license them. The symbol chi is not itself a license to rename a physical boundary.

A claim attaches only to the gate needed for that claim. Additional deeper or denser calculations may continue as bounded robustness, Function Map, or Limit Map evidence after a minimum stopping condition is met. A material robustness contradiction may reopen the affected foundation, but successful robustness does not create an automatic infinite compute ladder.

## Current evidence state

### Ru bulk candidate: ADJUDICATED PASS

The PBE/SSSP Ru bulk candidate passed the frozen numerical and structural gates. Selected settings remain 70/280 Ry and 16x16x10, with fitted hcp Ru lattice constants a = 2.725291573 A and c = 4.294686729 A. This establishes the bulk-level method prerequisite only. It does not establish H adsorption ordering, diffusion path, rate, dissipation coordinate, chi, or ChemSA eligibility.

### Historical clean-surface layer extension: ADJUDICATED PASS

The prospectively frozen deeper odd-layer extension produced:

- L15 surface excess = 1.092107489992486 eV/surface atom
- L17 surface excess = 1.091078831559571 eV/surface atom
- L19 surface excess = 1.090771478953684 eV/surface atom
- |L17 - L19| = 0.0003073526058869902 eV/surface atom

Under the frozen suffix rule, L17 was selected as the first non-terminal layer candidate in that model version.

### Original coupled endpoint recheck: ADJUDICATED HOLD, PRESERVED

Run `34535678952` tested the original L17/V15/K16 base and returned:

- K16 to K20 delta = 0.0024786851754470263 eV/surface atom: outside 0.001;
- V15 to V25 delta = 0.0000029932525649201125 eV/surface atom: inside 0.001;
- L17 to L19 delta = 0.0003073526058869902 eV/surface atom: inside 0.001.

The result `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD` remains part of the scientific record. It failed specifically on k-mesh and is not rewritten by later success.

### Dense-k P0-Q mapping: COMPLETED AS QUALIFICATION/FUNCTION-LIMIT EVIDENCE

The post-HOLD K20/K24/K28 work mapped the dense-k region without authorizing production by itself. K20 remained outside the frozen 1 meV criterion relative to K28, while K24 was inside. Under the prospectively frozen successor-selection rule this nominated K24 for a new fresh fixed-grid qualification. The diagnostic remains P0-Q evidence and not untouched P1 confirmation.

### Fresh successor fixed-grid qualification: ADJUDICATED PASS

Run `34769372617` completed the required fresh successor requalification at the proposed base **L17 / V15 / K24**. All four cases were fresh for the successor qualification; diagnostic energies were not reused as PASS evidence.

Surface-excess energies:

- base L17/V15/K24 = 1.0945347456436139 eV/surface atom;
- layer endpoint L19/V15/K24 = 1.094699510587816 eV/surface atom;
- k-mesh endpoint L17/V15/K28 = 1.094842506423447 eV/surface atom;
- vacuum endpoint L17/V25/K24 = 1.0945327047920728 eV/surface atom.

Absolute differences from the base:

- L17 to L19 = 0.0001647649442020338 eV/surface atom = **0.164765 meV/surface atom**;
- K24 to K28 = 0.0003077607798331883 eV/surface atom = **0.307761 meV/surface atom**;
- V15 to V25 = 0.0000020408515410963446 eV/surface atom = **0.002041 meV/surface atom**.

All are below the unchanged 0.001 eV/surface-atom threshold. The adjudicated result is therefore:

`CLEAN_SURFACE_FIXED_GRID_PASS`

This PASS is P0-Q qualification informed by the preserved dense-k diagnostic. It is not untouched P1 confirmation and it does not rewrite the original K16 HOLD.

### Foundational layer-depth robustness: ACTIVE HOLD BEFORE DOWNSTREAM INHERITANCE

The fixed-grid PASS satisfies the minimum frozen gate it was designed to judge. Because the clean Ru substrate will be inherited by substantial downstream H/Ru work, the user prospectively chose a stronger GOM Section 11.3 robustness challenge before entering relaxation.

`SYSTEM3_L17_FOUNDATIONAL_ROBUSTNESS_HOLD_v0.1.json` therefore holds operational progression while a fresh **L21/V15/K24** calculation runs under `SYSTEM3_L19_CONTINGENCY_LAYER_SUFFICIENCY_PROTOCOL_v0.1.json`.

The robustness challenge requires both:

- |L21 - L17| <= 0.001 eV/surface atom; and
- |L21 - L19| <= 0.001 eV/surface atom.

This is not a rescue calculation. The original PASS remains a PASS. If both checks survive, the result strengthens the inheritance of L17 and the layer-depth challenge stops. If either fails, the layer-depth foundation is reopened before relaxation. No automatic L23/L25 ladder is licensed by a successful result.

### Clean-surface relaxation/reproduction: FROZEN, NOT YET EXECUTED

`SYSTEM3_CLEAN_RU0001_RELAXATION_PROTOCOL_v0.1.json` remains the next production gate after the foundational robustness interlock. It requires checkpoint-protected BFGS relaxation of the permitted outer Ru layers followed by a fresh independent SCF reproduction at the emitted relaxed geometry. Passing the numerical fixed-grid gate alone does not issue a substrate-inheritance certificate.

### Dissipation coordinate: LIMIT MAP / NOT ESTABLISHED

The public-source audit remains `DISSIPATION_NOT_ESTABLISHED`. No qualified independent H/Ru(0001) diffusion-friction coordinate has yet been matched. This blocks quantitative dissipation/chi promotion that requires such a coordinate, but it does not invalidate the independently qualified bulk or clean-surface electronic-structure work.

### Quantum implementation: ARCHITECTURE READY, PRODUCTION NOT AUTHORIZED

The QE plus i-PI architecture remains a feasible future route, but the exact production interface/environment has not been qualified. No PIMD or other quantum-nuclear production result is implied by architecture readiness.

### Downstream sections: NOT YET PROMOTED

H adsorption, local H vibrational stability, reaction path, classical rate baseline, nuclear-quantum rate tier, projected dissipation, and any scalar/modal/system stability representation remain downstream of their own readiness gates. Literature and coordinate-matching work that does not depend on the final relaxed substrate may progress in parallel, but no downstream result may back-justify the substrate model.

## Prospective result structure

When licensed by evidence, System 3 will be reported in this order:

1. Ru bulk method qualification;
2. clean-surface layer/vacuum/k-mesh Function and Limit Map, including preserved HOLDs;
3. fresh successor fixed-grid qualification and bounded foundational robustness;
4. clean-surface relaxation and independent reproduction;
5. substrate-inheritance certificate at the exact earned scope;
6. unbiased top/bridge/fcc/hcp adsorption screen plus required numerical sensitivity;
7. local H vibrational stability of the computed adsorption minimum;
8. ordinary NEB, CI-NEB, and saddle-mode verification for the path selected from the computed PES;
9. classical harmonic baseline;
10. quantum-nuclear free-energy/rate tier under its frozen execution and convergence rules;
11. independently matched dissipation evidence where a claim requires it;
12. only then, any licensed scalar, modal/vector, conglomerate/system, or higher-order stability representation.

## Interpretation firewall

The original K16 coupled HOLD remains part of the published scientific record. The later K24 successor demonstrates that a denser version can satisfy the frozen numerical standard; it does not claim that K16 passed.

Similarity to CO/Cu(111), Na/Cu(001), published H/Ru behavior, a desired rate, a desired chi, or a preferred ChemSA interpretation cannot select or rescue numerical settings. Barrier-top frequencies, electronic broadening, friction, damping, and canonical restoring frequencies retain their native meanings and are not interchanged to manufacture a critical boundary.
