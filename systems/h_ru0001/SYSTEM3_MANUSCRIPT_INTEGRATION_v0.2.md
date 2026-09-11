# System 3 H/Ru(0001) manuscript integration record v0.2

**Status:** CURRENT EVIDENCE INTEGRATION / P0-Q QUALIFICATION.  
**Supersedes for current state:** `SYSTEM3_MANUSCRIPT_INTEGRATION_v0.1.md`.  
**Historical files remain preserved.**

## Role of System 3

H/Ru(0001) remains a difficult-limit system for the ChemSA computational methodology. Its role is not to establish universality and not to force a scalar stability description. The purpose is to determine how far an evidence-gated chemistry workflow can progress while preserving failures, identifying the operating region of each representation, and refusing unsupported promotion.

Under General Protocol v0.7.1 plus Addendum v0.7.1A, the present clean-surface work is **P0-Q controlled qualification**. Qualification failures may inform a versioned successor model, but they may not be rewritten as untouched confirmation.

## Language and claim rule

Conventional chemical and numerical terminology controls each statement. Exceptional point, critical damping, phase boundary, kinetic crossover, stability boundary, adsorption minimum, transition state, and related terms are used only when the governing equations and evidence license them. The symbol chi is not itself a license to rename a physical boundary.

A claim attaches only to the gate needed for that claim. Additional deeper or denser calculations may continue as robustness, Function Map, or Limit Map evidence after a claim-specific stopping condition is met, but they are not silently promoted into the original selection rule.

## Current evidence state

### Ru bulk candidate: ADJUDICATED PASS

The PBE/SSSP Ru bulk candidate passed the frozen numerical and structural gates. Selected settings remain 70/280 Ry and 16x16x10, with fitted hcp Ru lattice constants a = 2.725291573 A and c = 4.294686729 A. This establishes the bulk-level method prerequisite only. It does not establish a qualified Ru(0001) surface, H adsorption ordering, diffusion path, rate, dissipation coordinate, chi, or ChemSA eligibility.

### Clean Ru(0001) layer extension: ADJUDICATED PASS

The prospectively frozen deeper odd-layer extension produced:

- L15 surface excess = 1.092107489992486 eV/surface atom
- L17 surface excess = 1.091078831559571 eV/surface atom
- L19 surface excess = 1.090771478953684 eV/surface atom
- |L17 - L19| = 0.0003073526058869902 eV/surface atom

Under the frozen suffix rule, L17 is the selected non-terminal layer candidate and the L15/L17/L19 extension is `CLEAN_SURFACE_LAYER_EXTENSION_PASS`.

This layer PASS did not authorize relaxation. The lineage guard frozen in commit `807b71eab1c44d400d72f08bc3f789fc894122e5` required the original coupled endpoint recheck before any `CLEAN_SURFACE_FIXED_GRID_PASS` could be emitted.

### Coupled endpoint recheck: ADJUDICATED HOLD

Run `34535678952` completed the independent one-axis endpoint substitutions at the selected L17 base point. Relative to L17/V15/K16:

- K20 delta = 0.0024786851754470263 eV/surface atom: **outside** the frozen 0.001 tolerance
- V25 delta = 0.0000029932525649201125 eV/surface atom: **inside** tolerance
- L19 delta = 0.0003073526058869902 eV/surface atom: **inside** tolerance

The adjudicated result is `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD`, failed specifically on the k-mesh axis. This is a scientific numerical HOLD, not a mechanical failure. It cannot be rescued by relaxation, later rate agreement, chi, or another system's outcome.

### Post-HOLD dense-k qualification diagnostic: ACTIVE P0-Q

The K16-to-K20 failure is now being used as qualification evidence to map the k-mesh operating region. A separately frozen diagnostic continues the original +4 cadence through K20/K24/K28 at fixed L17/V15 and unchanged electronic settings and 0.001 eV/surface-atom tolerance.

This diagnostic serves both a **Function Map** and a **Limit Map** role:

- Function Map: identify any dense-k region in which surface excess becomes numerically stable.
- Limit Map: preserve the observed breakdown of the original K16 production candidate against K20.

The diagnostic cannot retroactively convert the original coupled HOLD into PASS and cannot directly authorize relaxation. Any production promotion requires a versioned successor fixed-grid qualification followed by its required coupled recheck.

### Downstream sections: NOT YET PROMOTED

H adsorption, local H vibrational stability, reaction path, classical rate baseline, nuclear-quantum rate tier, projected dissipation, and any scalar/modal/system stability representation remain downstream of their own readiness gates. Literature and coordinate-matching work that does not depend on the final surface numerical selection may be prepared in parallel, but no downstream result may back-justify the present surface model.

## Prospective result structure

When licensed by evidence, System 3 will be reported in this order:

1. Ru bulk method qualification;
2. clean-surface layer/vacuum/k-mesh Function and Limit Map, including preserved HOLDs;
3. versioned fixed-grid surface qualification and independent reproduction;
4. unbiased top/bridge/fcc/hcp adsorption screen plus required numerical sensitivity;
5. local H vibrational stability of the computed adsorption minimum;
6. ordinary NEB, CI-NEB, and saddle-mode verification for the path selected from the computed PES;
7. classical harmonic baseline;
8. quantum-nuclear free-energy/rate tier under its frozen bead and coordinate rules;
9. independently matched dissipation evidence;
10. only then, any licensed scalar, modal/vector, conglomerate/system, or higher-order stability representation.

## Interpretation firewall

The original K16 coupled HOLD remains part of the published scientific record even if a later successor grid qualifies. A later successor version may demonstrate that a denser grid is adequate; it may not claim that the original K16 candidate passed. Similarity to CO/Cu(111), Na/Cu(001), published H/Ru behavior, or a desired ChemSA interpretation cannot select the successor grid or erase disagreement.
