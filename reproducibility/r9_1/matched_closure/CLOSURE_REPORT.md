# CSA R9.1 Matched Four-Layer Closure Report

**Date:** 2026-09-25  
**Branch:** `csa-r9.1-matched-closure-search`  
**Preregistered protocol:** `reproducibility/r9_1/matched_closure/PROTOCOL.md`

## Closure statement

The preregistered search is closed with a **negative end-to-end result**: none of the four frozen candidates satisfies all eight admission gates required for a `FULL_CLOSE` on one independently tracked physical carrier.

This is not equivalent to “no useful systems were found.” The four candidates fail for different, physically meaningful reasons:

1. **CO/Cu(001):** nearest empirical case, but condition matching and quantitative carrier-to-saddle projection remain incomplete.
2. **Co2(CO)8:** the native reaction-coordinate friction and basin-frequency parameters used in the Kramers analysis are outcome-calibrated rather than independently measured.
3. **HONO/Kr:** the pumped OH-stretch population loss is entangled with IVR and reaction, while the actual reactive architecture is multimode and matrix-assisted.
4. **Photoinduced electron transfer:** the native solvent-polarization dynamics require a non-Markovian memory kernel, so reduction to a single local scalar damping ratio is not licensed.

The search therefore supports the manuscript's layered architecture while refusing to manufacture a fused predictor.

## Gate summary

| Candidate | G1 conditions | G2 scalar license | G3 carrier identity | G4 modal/path | G5 independent barrier | G6 native transmission/friction | G7 outcome independence | G8 provenance | Final class |
|---|---|---|---|---|---|---|---|---|---|
| CO/Cu(001) | FAIL/PARTIAL | PASS within each measured regime | PASS qualitatively | FAIL/PARTIAL | PASS | PASS | PASS for independent linewidth + PES; fitted spin-echo friction excluded | PASS/PARTIAL | **NEAR_MISS** |
| Co2(CO)8 | PASS for 2DIR series | FAIL for true reactive carrier | FAIL/PARTIAL | PARTIAL | PASS if computed PES is used | PARTIAL | **FAIL** | PASS | **REFUSED** |
| HONO/Kr | PASS within matrix studies | **FAIL** | **FAIL** | PASS as multimode architecture | PARTIAL due gas/matrix mismatch | PASS only in multimode native description | **FAIL** | PASS | **REFUSED** |
| Angulo photo-ET GLE | PASS | **FAIL by model class** | PASS | PASS in extended state space | PASS for independently constructed FES | PASS as non-Markovian GLE | PASS | PASS | **REFUSED** |

## Candidate 1: CO/Cu(001)

### What succeeds

The lateral frustrated translation of isolated CO on Cu(001) is experimentally assigned at (3.94\pm0.07\) meV by helium atom scattering and isotope shifts (Ellis, Toennies & Witte, 1995, DOI 10.1063/1.469555).

At dilute coverage, Graham, Hofmann & Toennies report an intrinsic zero-temperature-extrapolated linewidth of (85\pm5\) micro-eV, corresponding to a quoted lifetime of (8\pm1\) ps (1996, DOI 10.1063/1.471260). Under the CSA population-lifetime convention this gives

\[
\chi_0 = \frac{\hbar}{2E_{\mathrm{FT}}T_1} \approx 0.0104,
\]

with the width-based estimate (85\,\mu\mathrm{eV}/(2\times3.94\,\mathrm{meV})\approx0.0108).

Independent periodic DFT places the adsorption minimum atop Cu and the diffusion saddle at the bridge site, with barriers of approximately (95\pm30\) and (125\pm30\) meV depending on GGA (Fouquet, Olsen & Baerends, 2003, DOI 10.1063/1.1578054). Later (^{3}\)He spin-echo work observes activated microscopic hopping and a barrier near 0.12 eV (Alexandrowicz et al., 2004, DOI 10.1103/PhysRevLett.93.156103).

A separate half-monolayer pump-probe experiment at roughly 100 K reports a characteristic FT damping time of (2.3\pm0.4\) ps. Lewis & Rappe's independent lattice-coupling calculation at the same half-monolayer model gives a 3.0 ps harmonic FT decay time and identifies resonant mixing with Cu phonons as the dominant mechanism (DOI 10.1103/PhysRevLett.77.5241). If converted only within that high-coverage regime, the measured 2.3 ps value and roughly 32 cm(^{-1}) FT frequency correspond to an illustrative (\chi\approx0.036\), while the 3.0 ps calculation gives about 0.028.

### Why it still fails strict closure

The half-monolayer damping experiment is not the low-coverage diffusion experiment. The dilute HAS linewidth is independently measured but its numerically recovered value is the 0 K extrapolate rather than a tabulated lifetime at the diffusion temperatures. Coverage is scientifically material because the FT becomes collective/dispersive as coverage rises.

The FT is also not a pure rigid translation. Isotope shifts show rotational admixture, especially larger oxygen motion, so its quantitative overlap with the bridge-saddle diffusion direction cannot be set to one by nomenclature alone.

The later spin-echo analysis contains a fitted friction used to reproduce the diffusion data. That fitted friction is excluded by G7 and is not recycled as an independent lowercase-chi input.

**Final status: NEAR_MISS.** A new modal calculation could close G4 but would not close G1. The missing same-condition independent damping measurement is the decisive blocker.

## Candidate 2: Co2(CO)8

### What succeeds

Ultrafast 2D-IR directly observes bridged/nonbridged equilibrium exchange on picosecond timescales, with forward and reverse rates measured across linear alkane solvents (Anna, Ross & Kubarych, 2009, DOI 10.1021/jp903112c; Anna & Kubarych, 2010, DOI 10.1063/1.3492724). Independent electronic-structure calculations provide isomer and transition-state energetics. The exchange outcome itself is therefore real and well observed.

The 2010 study also identifies the isomerization coordinate as predominantly rotational/bridge-opening motion rather than a terminal CO stretch reporter.

### Decisive failure

The native Kramers analysis does not independently measure the required reactive-coordinate damping and reactant-well frequency. In the published fit, the geometric/friction mapping parameter and the basin frequency are allowed to vary against the observed reaction-rate series. Thus using those same fitted parameters to construct

\[
\chi = \frac{\beta}{2\omega_a}
\]

and then treating (\chi\) as an independent test of those rates would violate G7.

The visible CO-stretch population lifetime is not a rescue. It is a spectroscopic reporter lifetime, not the damping of the bridge-opening/rotational reaction coordinate.

A targeted literature search found structures, vibrational spectra, and later memory-kernel methodology for other isomerizing molecules, but no independently measured or computed Co2(CO)8 reaction-coordinate friction kernel under the 2D-IR solvent conditions.

**Final status: REFUSED.** Static quantum chemistry could improve the TS and Hessian, but cannot supply the missing independent solvent reaction-coordinate friction.

## Candidate 3: HONO in solid Kr

### What succeeds

Direct OH-stretch excitation of cis-HONO produces cis-trans isomerization in the same low-temperature Kr matrix experiment. Schanz, Botan & Hamm report about a 20 ps decay of the initially excited cis state and a roughly 10% fast isomerization yield on that timescale (2005, DOI 10.1063/1.1834567). Later work resolves a slower approximately 2 ns reaction channel and approximately 20 ns final cooling (Botan, Schanz & Hamm, 2006, DOI 10.1063/1.2204914).

Temperature-dependent experiments show that the OH-stretch lifetime and final cooling change little from roughly 30 to 15 K while the cis-to-trans yield increases strongly, reaching approximately 50-70% at lower temperature (Botan & Hamm, 2008, DOI 10.1063/1.2978386). Two-color spectroscopy directly follows IVR through other modes (DOI 10.1063/1.2996355).

Full-dimensional calculations and the matrix model show that the reactive path involves torsional/delocalized intramolecular states together with translational motion in the Kr cage, rather than a single OH-stretch coordinate.

### Decisive failure

The disappearance of the pumped OH-stretch population cannot be treated as an independent bath-only damping constant. On the same timescale, population is being transferred by IVR and lost into the reactive branch:

\[
k_{\mathrm{observed\ decay}}
=
k_{\mathrm{bath}}
+
k_{\mathrm{IVR}}
+
k_{\mathrm{reaction}}
+\cdots
\]

Using that total decay as (\gamma) and then testing it against the isomerization outcome would leak the outcome into the predictor and violate G7. The carrier-identity gate also fails because the pumped OH stretch prepares the system, but the reactive architecture subsequently routes through other modes and the matrix cage.

The strong temperature dependence of quantum yield despite weak temperature dependence of the OH-stretch lifetime is itself evidence against a one-scalar OH-damping interpretation.

**Final status: REFUSED.** The failure is mechanistic, not a missing-geometry problem.

## Candidate 4: Angulo et al. photoinduced electron transfer

### What succeeds

Angulo et al. define a solvent-polarization reaction coordinate and use an inertial generalized Langevin equation with independently constructed free-energy surface and solvent dynamics (2017, DOI 10.1063/1.4990044). The FES is obtained from stationary spectroscopy, while the non-Markovian friction is calibrated from the nonreacting probe Coumarin 153 rather than from the target PeDMA dynamics.

The friction has the form

\[
\eta(t)
=
\omega_L^2\gamma\delta(t)
+
\omega_L^2\sum_i k_i e^{-\lambda_i t}.
\]

The paper also rewrites the GLE as a higher-dimensional Markovian system with auxiliary variables, preserving the memory information.

### Decisive refusal

The memory terms are part of the physical model, not optional decoration. A memoryless overdamped Smoluchowski test with constant asymptotic diffusion does not reproduce the observations adequately, and the generalized reduced treatment departs increasingly from the full GLE as dynamics slow.

Therefore the coefficient multiplying the delta term cannot by itself be promoted to a complete local scalar stability coordinate for the reaction. Auxiliary-variable Markovian embedding changes the representation of the non-Markovian process but does not collapse the extended state to one physically sufficient damping ratio.

**Final status: REFUSED.** This is a successful model-class refusal and directly demonstrates why the scalar gate is necessary.

## Failure taxonomy

The four candidates separate into four failure mechanisms:

| Failure type | Candidate | Meaning |
|---|---|---|
| Condition/provenance closure | CO/Cu(001) | Right carrier and physics exist, but the independent damping record is not matched to the independent diffusion record closely enough to satisfy G1. |
| Outcome-calibrated dynamics | Co2(CO)8 | Reactive-coordinate friction/basin frequency are adjusted against the rate series, so they cannot independently validate that series. |
| Reaction-contaminated decay and carrier migration | HONO/Kr | The observed pumped-mode loss contains IVR/reaction, and the reactive carrier changes into a multimode/matrix-assisted architecture. |
| Non-Markovian model-class refusal | Photo-ET GLE | The native dynamics require memory; a single local scalar loses essential state information. |

## Compute stop-rule adjudication

No new Rowan calculation is scientifically capable of converting any current candidate to `FULL_CLOSE` by itself:

- **CO/Cu(001):** a new surface Hessian/path calculation could quantify G4, but the candidate would still fail G1 because the missing item is a same-condition independent damping measurement. Independent PES/barrier calculations already exist.
- **Co2(CO)8:** a new TS/Hessian calculation could improve G4/G5, but the decisive missing item is an independent solvent reaction-coordinate friction/memory kernel. Routine static quantum chemistry cannot provide it.
- **HONO/Kr:** another gas-phase/matrix-free PES calculation cannot separate bath damping from IVR/reaction in the measured OH-stretch decay or turn that preparation mode into the unique reactive carrier.
- **Photo-ET GLE:** no computation is needed to repair a deliberate model-class refusal; the source-native memory kernel is the correct representation.

Accordingly, running additional static calculations would create more numbers without removing the admission failures and is prohibited by the preregistered stop rule.

## Final scientific conclusion

The investigation is closed honestly with **zero FULL_CLOSE systems among the four preregistered candidates**. The nearest system, CO/Cu(001), misses strict closure for concrete condition/projection reasons rather than for lack of relevant physics. The other three demonstrate three different reasons that a scalar (chi) should be withheld.

The result strengthens rather than weakens the architecture: the framework does not force chemically distinct damping, modal, barrier, and kinetic observables into a single coordinate when independence or model class does not support that reduction.

A future positive closure requires new evidence, not reinterpretation of the present literature. The cleanest empirical target would be a same-condition measurement of a licensed reaction-coordinate (T_1)/damping rate, its mode/path geometry, an independently established barrier/native transmission model, and an independently observed kinetic outcome.
