# H/Ru(0001) Dissipation-Coordinate Literature Audit v0.2

**Date:** 14 September 2026  
**Status:** LIMIT MAP UPDATED / QUANTITATIVE DIFFUSION FRICTION STILL NOT ESTABLISHED  
**Supersedes for current literature state:** v0.1  
**Program authority:** SymC General Operations Manual v0.8.0

## Question frozen for this audit

Is there a published, physically matched **quantitative damping/friction coordinate for adsorbed atomic H diffusion on Ru(0001)** that can be paired with the corresponding H diffusion mode/reaction coordinate without changing system, phase, process, or dynamical meaning?

This is narrower than asking whether electronic friction has ever been calculated for any hydrogen/Ru(0001) process.

## Result

`QUANTITATIVE_H_ADATOM_DIFFUSION_FRICTION = NOT_ESTABLISHED`

`QUALITATIVE_LOW_FRICTION_CONSTRAINT = SUPPORTED`

The new search finds useful H/Ru(0001)-specific dissipation evidence, but the directly retrieved quantitative friction models concern H2 dissociative adsorption/scattering or associative desorption rather than the adsorbed-H fcc↔hcp diffusion coordinate. They therefore do not satisfy the coordinate-matching contract for a numerical diffusion damping coefficient.

## Direct diffusion evidence

### McIntosh et al., J. Phys. Chem. Lett. 2013, DOI 10.1021/jz400622v

This combined helium spin-echo and ab initio path-integral study measures atomic H diffusion on Ru(0001) from 75 to 250 K. It reports a low-temperature tunneling-dominated rate of approximately 1.9 x 10^9 s^-1, with quantum effects visible up to about 200 K. Its DFT description finds fcc as the most stable site, hcp higher by about 50 meV, and a lowest-energy bridge pathway with a classical barrier near 150 meV, reduced to roughly 120 meV with harmonic zero-point correction.

Most relevant here, the paper interprets observed multiple jumps as evidence of **low adsorbate-substrate friction** relative to systems such as H/Pt(111). That is a real H/Ru(0001) diffusion constraint, but it is not a reported numerical friction coefficient or projected damping tensor for the fcc↔hcp diffusion coordinate.

**Admission for dissipation:** qualitative/inequality-like Limit Map information only.  
**Not admitted as:** numerical gamma, friction tensor element, or direct ChemSA damping coordinate.

Open/full-text identity also exists through PubMed Central (PMCID PMC4047567).

## H/Ru(0001)-specific electronic-friction studies that do not match the diffusion coordinate

### Fuechsel, Schimka, and Saalfrank, J. Phys. Chem. A 2013, DOI 10.1021/jp403860p

The study performs classical molecular dynamics with electronic friction for **H2 dissociative sticking and inelastic scattering at Ru(0001)**. Electronic friction is represented through atomic friction coefficients from an embedded-atom/free-electron-gas model with DFT embedding densities.

This establishes that an explicit friction model has been applied to hydrogen/Ru(0001), but the governed process is an incoming H2 molecule on a six-dimensional dissociation/scattering PES. It is not the equilibrium adsorbed-H diffusion coordinate between fcc and hcp sites.

**Admission:** methodological/process-adjacent evidence.  
**Coordinate match to adatom diffusion:** FAIL.

### Femtosecond-laser associative H2 desorption from Ru(0001), J. Chem. Phys. 2006, DOI 10.1063/1.2206588

A first-principles dynamical model of laser-induced **associative H2 desorption** from H-covered Ru(0001) uses a DFT potential-energy surface and electronic-friction tensor, including molecular separation, molecule-surface distance, and a phonon coordinate. It reproduces several experimental observables semiquantitatively without adjustable parameters in that comparison.

This is strong evidence that friction tensors are physically meaningful for H/Ru(0001) femtochemistry, but the dynamical object is associative desorption under hot-electron excitation, not thermal/tunneling fcc↔hcp adatom diffusion.

**Admission:** Ru/H dissipation mechanism evidence.  
**Coordinate match to adatom diffusion:** FAIL.

## Ru(0001)-specific tensor methodology with a different adsorbate

### N2/Ru(0001) orbital-dependent electronic friction, J. Phys. Chem. Lett. 2019, DOI 10.1021/acs.jpclett.9b00523

This work computes full orbital-dependent electronic-friction tensors from density-functional perturbation theory for N2 on Ru(0001), using Quantum ESPRESSO and a converged Ru slab/k-mesh/friction-broadening setup. It demonstrates that first-principles tensorial friction on Ru(0001) is computationally feasible and that orbital dependence can materially alter reactive-scattering dynamics.

It cannot supply H-adatom diffusion friction because both the adsorbate and reaction coordinate differ.

**Admission:** implementation precedent for a future Ru-surface friction calculation.  
**Coordinate match to H diffusion:** FAIL.

## General first-principles friction methodology

Tensorial electronic-friction methods based on DFT/nonadiabatic couplings have been developed for adsorbates on metals and can predict vibrational relaxation and mode coupling. These methods show that friction is generally tensorial and coordinate dependent, reinforcing rather than weakening the need for a projected, mode-matched quantity.

A 2024/2025 line of work on non-Markovian electronic friction plus quantum rate theory for H diffusion on Cu(111) further warns that a single Markovian scalar can miss memory effects in quantum surface diffusion. That result is not final evidence for H/Ru(0001), but it is a useful design warning for any future first-principles dissipation tier.

## Updated Function Map

Established:

- atomic H diffusion rates on Ru(0001) from HeSE;
- quantum/tunneling importance and an experimentally observed low-temperature rate plateau;
- fcc/hcp/bridge diffusion topology in the published DFT/PIMD study;
- qualitative evidence for relatively low adsorbate-substrate friction from multiple jumps;
- H/Ru(0001)-specific electronic-friction modeling for H2 dissociation/scattering and associative desorption;
- feasibility of first-principles tensorial electronic-friction calculations on Ru(0001) from N2/Ru work.

Not established:

- a numerical friction coefficient explicitly projected onto the adsorbed-H fcc↔hcp diffusion coordinate;
- a frequency-dependent memory kernel for that H/Ru diffusion coordinate;
- a validated Markovian reduction of such a kernel;
- a mechanical damping ratio for the diffusion coordinate;
- a licensed `chi` derived from the HeSE jump rate alone.

## Consequence for System 3

The dissipation claim ceiling remains unchanged:

1. HeSE rates may validate or challenge a future diffusion-rate calculation.
2. The HeSE multiple-jump observation may be used as **qualitative low-friction evidence**.
3. H2/Ru electronic-friction models may motivate or benchmark methodology but may not be numerically transplanted to H-adatom diffusion.
4. A future first-principles friction calculation should compute the full or appropriately reduced friction object on the same H/Ru(0001) substrate/coverage/coordinate, then project it onto a validated diffusion/reaction mode before any scalar damping quantity is considered.
5. Memory dependence should be tested rather than assumed negligible if the quantitative claim depends on a Markovian scalar.

## Preferred closure path

The cleanest computational path available without a new physical experiment is:

- finish the native H/Ru PES and validated diffusion path first;
- identify the relevant reaction-coordinate tangent/mode along that path;
- compute a first-principles electronic-friction tensor or kernel for the same H/Ru states using a method with explicit convergence controls;
- project the friction onto the validated coordinate;
- test Markovian versus frequency-dependent/memory-sensitive descriptions where feasible;
- compare the resulting dynamics against the independent HeSE diffusion-rate curve and its multiple-jump/low-friction signature.

Until that chain exists, `DISSIPATION_NOT_ESTABLISHED` remains the correct quantitative status.

## Sources checked in this refresh

- McIntosh et al., "Quantum Effects in the Diffusion of Hydrogen on Ru(0001)," J. Phys. Chem. Lett. 2013, DOI: 10.1021/jz400622v, open-access full text/PMC available.
- Fuechsel, Schimka, Saalfrank, "On the Role of Electronic Friction for Dissociative Adsorption and Scattering of Hydrogen Molecules at a Ru(0001) Surface," J. Phys. Chem. A 2013, DOI: 10.1021/jp403860p.
- "Femtosecond laser induced associative desorption of H2 from Ru(0001): comparison of first principles theory with experiment," J. Chem. Phys. 2006, DOI: 10.1063/1.2206588.
- "Orbital-Dependent Electronic Friction Significantly Affects the Description of Reactive Scattering of N2 from Ru(0001)," J. Phys. Chem. Lett. 2019, DOI: 10.1021/acs.jpclett.9b00523, open full text available through PMC.
- Maurer et al., "Ab-initio tensorial electronic friction for molecules on metal surfaces: nonadiabatic vibrational relaxation," methodological reference, arXiv:1607.02650 / associated peer-reviewed work.

No source retrieved in this refresh numerically reports the matched adsorbed-H fcc↔hcp diffusion friction required by the frozen question.
