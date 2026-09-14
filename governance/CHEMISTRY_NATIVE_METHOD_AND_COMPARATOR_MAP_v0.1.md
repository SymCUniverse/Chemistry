# Chemistry Native-Method and Comparator Map v0.1

**Date:** 14 September 2026  
**Status:** ACTIVE CLAIM-DESIGN MAP  
**Program authority:** SymC General Operations Manual v0.8.0

## Purpose

A SymC/ChemSA analysis earns value only relative to the native scientific toolkit that already answers the same question. This map prevents two opposite errors: replacing established chemistry with a stability coordinate, and demanding irrelevant comparator calculations that do not answer the frozen inferential question.

`NO_NATIVE_COMPARATOR` is used only after a good-faith search fails to identify a native method answering the same question. It does not mean no chemistry method exists in the surrounding field.

## Claim-by-claim map

| Frozen question | Native method / reference standard | Independent evidence or comparator | What ChemSA may add | What ChemSA may not replace |
|---|---|---|---|---|
| Is the clean bulk/surface numerical model converged? | DFT convergence in cutoffs, k-space, cell/vacuum, slab depth, force/energy criteria | higher-resolution endpoint calculations; experimental surface structure only after numerical choices are frozen | Function/Limit mapping of where inherited numerical representations remain stable | ordinary convergence testing |
| Is the relaxed clean-surface geometry physical? | DFT ionic relaxation under a predeclared force criterion | LEED-IV / surface X-ray diffraction / known interlayer relaxations | dependency/inheritance map across local and embedded substrate states | structural experiment or force convergence |
| Which adsorption site is lowest? | DFT adsorption-energy comparison after unbiased relaxation from candidate sites | LEED/HREELS/diffraction/site-sensitive experiment after calculation is frozen | stability/modal description of the computed minima; substrate-inheritance limits | adsorption energy or site ordering |
| Is an adsorbed structure a local minimum? | Hessian / vibrational normal-mode calculation with no unstable adsorbate mode in the intended constrained space | HREELS/IR/Raman/INS where available | mode-resolved scalar/modal architecture where the native second-order reduction is licensed | the Hessian or vibrational-stability criterion |
| What is the minimum-energy reaction/diffusion path? | NEB / climbing-image NEB, dimer or equivalent saddle search; QE `neb.x` is a standard implementation | path sensitivity, alternate initialization, experimental mechanism only as external validation | Function/Limit mapping of modal structure along a path; detect where a local reduction changes character | path optimization |
| Is the transition state a first-order saddle? | saddle Hessian / one unstable mode aligned with the path; converged saddle force | alternate saddle method or local finite-difference verification | generator/mode classification with explicit saddle semantics | the one-negative-mode saddle criterion |
| What is the classical activated rate baseline? | harmonic transition-state theory / Eyring-type native rate theory on a verified minimum/saddle, with recrossing caveats | direct dynamics/reactive-flux correction or experimental rate | compare stability architecture with rate residuals without using rate to tune the architecture | TST rate formula, barrier, partition functions |
| Are recrossing/friction effects important? | Kramers, Grote-Hynes, reactive-flux, generalized Langevin or direct dynamical treatment appropriate to the bath | trajectory-based transmission coefficient; matched experimental correlation functions | test whether native damping/friction objects align with a licensed stability boundary in their own governing dynamics | barrier-top frequency, transmission coefficient, or friction kernel |
| What is the quantum-nuclear rate? | PIMD-QTST, ring-polymer instanton, RPMD-based rate theory, or other justified quantum method with bead/path convergence | isotope effect and independent rate curve; method cross-check where genuinely comparable | examine mode/system stability structure after method/coordinate choices are frozen | tunneling calculation or bead convergence |
| What is the adsorbate electronic-friction object? | first-principles electronic-friction tensor/kernel from TDPT/DFPT/nonadiabatic-coupling methods, or a separately justified lower-level model | vibrational lifetime, scattering/desorption energy loss, HeSE/memory-sensitive diffusion observables | project a validated friction object onto a validated mode/reaction coordinate, then ask whether a scalar/modal description is licensed | friction calculation itself; linewidth/rate as a friction surrogate |
| Is a measured linewidth mechanical damping? | spectroscopy decomposition: homogeneous vs inhomogeneous broadening, lifetime vs pure dephasing and other relaxation channels | independent T1/time-domain/echo/orientational information | compute mechanical chi only from a licensed lifetime damping term and corresponding mode frequency | raw linewidth-to-damping conversion |
| Is a repeated root an exceptional point? | algebraic vs geometric multiplicity / defective generator analysis, with structural or parameter-continuation support for high-order claims | perturbation response, Puiseux behavior, condition number, Jordan-chain evidence | executable refusal-aware EP classification and provenance scoping | eigenvalue coincidence alone |
| Does local spectral architecture predict a reaction rate? | Native kinetics/PES and global barrier dynamics | constructive counterexample and independent rate data | generally: no direct rate prediction from local architecture; any added-value relation must be separately demonstrated | reaction-rate prediction from local chi alone |
| Does a substrate certificate transfer downstream? | numerical substrate qualification plus clean relaxation/reproduction and explicit scope | targeted adsorbate perturbation/requalification tests | bounded hierarchical inheritance and reopening rules | adsorbate-specific convergence, coverage, path, barrier, rate, or dissipation gates |

## System-3 H/Ru(0001) concrete comparator ladder

### Clean substrate

- Native computation: fresh DFT fixed-grid convergence, then BFGS clean-surface relaxation/reproduction.
- External comparator: published LEED-IV / surface X-ray diffraction interlayer relaxation.
- Current ChemSA role: governance/inheritance and later mode-resolved interpretation only.

### Adsorption

- Native computation: unbiased top/bridge/fcc/hcp relaxations plus H2 reference, lateral-cell sensitivity, reciprocal-resolution sensitivity, and local vibrational stability.
- External comparator: published H/D HREELS frequencies/dispersion and site/coverage evidence.
- ChemSA does not select the site.

### Diffusion path and rate

- Native computation: computed fcc/hcp minima, bridge/other path search, NEB/CI-NEB, verified saddle, classical TST baseline, quantum-nuclear method.
- External comparator: HeSE temperature-dependent H diffusion curve and fcc-hcp asymmetry.
- Published HeSE data are held out from upstream model selection.

### Dissipation

- Native computation: matched electronic-friction tensor/kernel and projection to the computed H diffusion coordinate; test memory dependence where material.
- External comparator: HeSE multiple-jump/low-friction signature and any future matched isotope/memory experiment.
- H2 dissociation/desorption friction literature is method-adjacent, not coordinate-equivalent.

## Comparator decision rules

1. Freeze the **inferential question** before choosing a comparator.
2. A method is a comparator only if it estimates/tests the same quantity or decision at a meaningful scale.
3. A more sophisticated method answering a different question is not automatically a better comparator.
4. Agreement with a method used to calibrate the candidate does not count as independent validation.
5. Experimental data used to choose a path, threshold, site, or parameter are discovery/qualification data for that decision, not untouched confirmation.
6. A failed or unavailable native comparator is reported as a Limit Map result rather than replaced by a convenient surrogate.
7. ChemSA added value must be stated explicitly: refusal, cross-representation bookkeeping, defectiveness/provenance classification, hierarchical inheritance, Function/Limit mapping, or a separately demonstrated new predictive relation.

## Current source anchors

- Quantum ESPRESSO current documentation provides standard PWscf structural optimization and `neb.x` NEB machinery; current NEB docs identify QE 7.5 while the QE release page lists 7.6 as the latest release.
- i-PI currently documents QE as an out-of-the-box force client and provides PIMD/advanced nuclear-dynamics infrastructure.
- McIntosh et al., J. Phys. Chem. Lett. 2013, DOI 10.1021/jz400622v, supplies the strongest direct H/Ru(0001) diffusion-rate comparator identified for System 3.
- Published H/D HREELS on Ru(0001) supplies a native vibrational/coverage comparator.
- Published H/Ru and N2/Ru electronic-friction work establishes process-specific and methodological precedents but not a numerical H-adatom diffusion friction coordinate.

This map is prospective claim design, not evidence that every listed method has already been executed in this repository.
