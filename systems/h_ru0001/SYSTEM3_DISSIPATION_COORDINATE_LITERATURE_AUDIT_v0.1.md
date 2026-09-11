# System 3 H/Ru(0001) dissipation-coordinate literature audit v0.1

**Date:** 2026-09-11  
**Status:** `DISSIPATION_NOT_ESTABLISHED`  
**Phase:** P0-Q / evidence-admissibility audit  
**Purpose:** Determine whether public literature presently supplies an independently sourced, coordinate-matched friction or damping quantity that can license the H/Ru(0001) diffusion dissipation tier without circularity.

## Admission rule

A dissipation source is not admitted merely because it contains a decay rate, a fitted friction, a Ru(0001) friction calculation, or qualitative low-friction language. For `DISSIPATION_READY`, the quantity must be physically matched to the atomic-H surface-diffusion coordinate and compatible state point, and it must be sufficiently independent of the held-out H/Ru rate data that it cannot force the downstream agreement being tested.

HeSE dephasing, population relaxation, fitted Langevin friction, electronic friction tensors for different processes, and phenomenological rate-fit parameters remain distinct evidence channels.

## Source audit

### 1. McIntosh et al., 2013

**Citation:** E. M. McIntosh, K. Thor Wikfeldt, J. Ellis, A. Michaelides, W. Allison, *Quantum Effects in the Diffusion of Hydrogen on Ru(0001)*, J. Phys. Chem. Lett. 4, 1565-1569 (2013). DOI: `10.1021/jz400622v`. Open access / CC-BY.

**What it supplies:**

- He-3 spin-echo measurements of atomic H motion on Ru(0001) over 75-250 K.
- Intermediate-scattering-function exponential decay constants/dephasing rates alpha(DeltaK).
- A multiple-jump signature interpreted as low adsorbate-substrate friction.
- Experimental hopping-rate behavior and an ab initio PIMD/QTST comparator.

**Admissibility:** `QUALITATIVE_FRICTION_REGIME_ONLY`.

The measured dephasing rate is not automatically a scalar reaction-coordinate friction coefficient. The multiple-jump signature supports the statement that the adsorbate-substrate friction is relatively low, but it does not by itself provide the independent projected gamma required by the System 3 dissipation gate.

### 2. Pollak, 2026

**Citation:** E. Pollak, *Semiclassical second order vibrational perturbation theory for hopping rates of H and D atoms on Pt(111) and H on Ru(0001)*, Phys. Chem. Chem. Phys. 28, 2054-2060 (2026). DOI: `10.1039/D5CP03122B`. Open access.

**What it supplies for H/Ru(0001):**

- a one-dimensional generalized-Langevin dissipative-tunneling model;
- fitted H/Ru parameters including hbar*omega_barrier = 130 meV, barrier height = 231 meV, and hbar*gamma = 2.5 meV;
- a fit to the experimental H/Ru hopping-rate data.

**Admissibility:** `NON_INDEPENDENT_RATE_FIT_DISSIPATION_COMPARATOR`.

This paper is scientifically relevant because it provides an explicit dissipative model for the same H/Ru hopping process. It is not admissible as the independent dissipation quantity required to validate a later rate/stability comparison, because gamma is a fitted parameter in a model adjusted against the same experimental hopping-rate behavior that is reserved as the downstream comparator. Using that fitted gamma to claim independent agreement would create a tuning/outcome-independence leak.

The source may be retained as a post-qualification theory comparator and as evidence that a generalized-Langevin description is physically plausible for this process, but not as an independent dissipation validator.

### 3. Luntz et al., 2006 and related Ru(0001) electronic-friction work

**Representative citation:** *Femtosecond laser induced associative desorption of H2 from Ru(0001): comparison of first principles theory with experiment*, J. Chem. Phys. (2006). DOI: `10.1063/1.2206588`.

**What it supplies:** first-principles electronic-friction tensors/dynamics for laser-induced associative H2 desorption from hydrogen-covered Ru(0001).

**Admissibility:** `PROCESS_AND_COORDINATE_MISMATCH`.

The reaction coordinates involve H-H separation, center-of-mass motion normal to the surface, and phonon coordinates under laser-heated conditions. These are not the lateral atomic-H fcc/hcp surface-diffusion coordinate and equilibrium state points required by System 3.

### 4. Fuchsel et al., 2011 and related H2/Ru(0001) MDEF studies

**Representative citation:** *Dissipative dynamics within the electronic friction approach: the femtosecond laser desorption of H2/D2 from Ru(0001)*, Phys. Chem. Chem. Phys. (2011), DOI associated with article `C0CP02086A`.

**Admissibility:** `PROCESS_AND_STATE_POINT_MISMATCH`.

These calculations are useful background on friction modelling at Ru surfaces but do not independently determine the projected friction for lateral atomic-H diffusion under the System 3 measurement conditions.

### 5. Trenins and Rossi, 2025

**Citation:** G. Trenins and M. Rossi, *Non-Markovian Effects in Quantum Rate Calculations of Hydrogen Diffusion with Electronic Friction*, Phys. Rev. Lett. 134, 226201 (2025). DOI: `10.1103/PhysRevLett.134.226201`.

**What it supplies:** a generalized-Langevin/ring-polymer framework incorporating spatially dependent and non-Markovian electronic friction for hydrogen diffusion on Cu(111).

**Admissibility for H/Ru:** `METHOD_RELEVANT_SUBSTRATE_MISMATCH`.

It is useful for future Engine/method design but cannot supply the H/Ru-specific independent dissipation quantity.

## Audit conclusion

`NO_QUALIFIED_INDEPENDENT_COORDINATE_MATCHED_H_RU0001_DIFFUSION_FRICTION_SOURCE_IDENTIFIED_IN_CURRENT_PUBLIC_SEARCH`.

Therefore:

- `DISSIPATION_READY = false`.
- `CHEMSA_ELIGIBLE = false` until an admissible dissipation pathway and domain-specific semantic license are established.
- McIntosh HeSE dephasing must not be relabelled as reaction-coordinate gamma.
- Pollak's fitted hbar*gamma = 2.5 meV must not be used as an independent validation input or upstream selector.
- H2/Ru electronic-friction tensors must not be projected onto atomic-H lateral diffusion without a separately justified coordinate-matching derivation.
- The negative literature result is a valid Limit Map outcome rather than missing or failed bookkeeping.

## What is closed by this audit

The initial public-literature search and admissibility classification are complete enough that final computational reconciliation does not need to pause to decide whether the obvious existing H/Ru friction candidates are independently usable. None of the identified candidates currently licenses `DISSIPATION_READY`.

A future newly located or newly published source may reopen the audit, but absence of such a source does not invalidate the classical/quantum reaction-path work. It limits only claims that require independently established dissipation or chi.
