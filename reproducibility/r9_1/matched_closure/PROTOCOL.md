# CSA R9.1 Matched Four-Layer Closure Protocol

Status: PREREGISTERED BEFORE candidate promotion or new calculation.
Branch: `csa-r9.1-matched-closure-search`
Parent: R9.1 reproducibility commit `4a00fbbb708d2eec42c74850c1b857e9d5d1a96d`

## Question

Can at least one real chemical reaction, isomerization, conformational transition, or surface-diffusion process be represented on the same tracked physical carrier with all four CSA layers independently supported?

1. licensed local temporal carrier dynamics, including `omega0`, `gamma`, and lowercase `chi = gamma/(2 omega0)`;
2. Capital-Chi modal/path organization for that same carrier;
3. an independently measured or computed barrier plus the native transmission/friction representation required by the system;
4. an observed kinetic or selectivity outcome not used to construct the damping, barrier, or modal quantity being evaluated.

A negative result is acceptable and will be retained.

## Irreducible admission gates

### G1. Same-system / condition gate
The four layers must refer to the same chemical system and to matched conditions or to a quantitatively justified condition transfer. A condition mismatch is not silently ignored.

### G2. Scalar-license gate
Lowercase `chi` is admitted only for a carrier that supports the manuscript's second-order mechanical interpretation. A coherence time `T2`, bulk viscosity, solvent dielectric relaxation time, electronic hybridization width, reaction-population decay, or generic spectral width is not substituted for mechanical amplitude/population damping without a source-native derivation.

For spectroscopic population relaxation the current CSA convention is `gamma = 1/T1`, but a source-specific linewidth/lifetime convention must be re-derived before numerical admission.

### G3. Carrier identity gate
The exact carrier used for `chi` must be identifiable in the modal record. A spectroscopic reporter does not become a reaction coordinate by assertion. Low or zero reaction-coordinate participation is an admissible result.

### G4. Modal/path gate
Capital Chi must preserve basis/subspace information needed to relate the reactant carrier to the relevant reaction/diffusion direction. Acceptable evidence includes source-reported projection matrices or independently computed mass-weighted Hessian/subspace overlaps. Target-driven mode permutation is prohibited.

### G5. Barrier-independence gate
A barrier reconstructed from the target rate cannot independently validate that rate. Prefer source-independent electronic-structure/PES barriers or direct energetic measurements. Eyring barriers inferred from the same target rate are outcome summaries, not independent barrier evidence.

### G6. Native transmission/friction gate
Use the native dynamical treatment. Markovian Kramers, Grote-Hynes/non-Markovian friction, tunneling, surface diffusion, or other transmission physics is retained where required. Reactant-well `chi` is never substituted for this layer.

### G7. Outcome-independence gate
The observed rate, diffusion coefficient/broadening, branching ratio, sticking probability, or selectivity outcome must not have been used to fit the scalar damping, modal mapping, independent barrier, or baseline transmission model being tested.

### G8. Provenance gate
Every numerical value carries source, access tier, condition, unit, and extraction route. Figure-only values remain provisional until calibrated or independently tabulated.

## Outcome classes

- `FULL_CLOSE`: all gates G1-G8 pass.
- `CONDITIONAL_CLOSE`: all physics gates pass but one explicitly quantified condition transfer remains.
- `NEAR_MISS`: scientifically relevant but at least one required layer is genuinely unavailable.
- `REFUSED`: a required layer would need an unlicensed substitution, circular reconstruction, or unresolved identity mapping.
- `FAILED_MECHANICAL`: acquisition/computation/reproduction failed without yet implying scientific failure.
- `FAILED_SCIENTIFIC`: the candidate was tested and the required physical relation/identity does not hold.

Every failure is retained and investigated for root cause: isolated/outlier, distributional, reproducible/systematic, source/provenance, implementation/infrastructure, or genuine model/data behavior.

## Frozen candidate order

The first-pass order is fixed before final adjudication:

1. CO/Cu(001) frustrated-translation surface diffusion.
2. Co2(CO)8 bridged/nonbridged equilibrium isomerization.
3. HONO/Kr IR-driven cis-trans isomerization.
4. Angulo et al. photoinduced electron transfer GLE as a deliberate scalar-refusal control.

No candidate will be promoted because it gives a favorable numerical relationship.

## Candidate-specific first tests

### CO/Cu(001)
Re-derive the source linewidth/lifetime convention before computing `chi`. Seek finite-temperature linewidths matching the >100 K diffusion measurements. Build or source an independent PES/barrier and compute the mass-weighted reactant frustrated-translation overlap with the diffusion saddle direction. Do not equate the QHAS activation energy with the adiabatic PES barrier.

### Co2(CO)8
Recover exact isomer-specific carbonyl frequencies and population lifetimes from 2D-IR evidence; identify whether the damped mode can be tracked to the isomerization saddle. Use an independent electronic-structure barrier rather than the Eyring barrier reconstructed from the exchange rate.

### HONO/Kr
Treat the observed excited-state/reaction-population decays separately from a genuine mode-specific population lifetime. Refuse lowercase `chi` unless an independently measured `T1` for the tracked OH-stretch carrier is recovered.

### Photoinduced electron transfer GLE
Retain the source-native non-Markovian kernel on the solvent-polarization reaction coordinate. This candidate is a control against forcing a scalar Markovian `chi`; a scalar refusal is a successful protocol outcome, not a failure.

## Stop rule

Stop the search only after:
1. every frozen candidate has been adjudicated through the available evidence;
2. obvious open-source citation trails have been exhausted for the missing measurements;
3. affordable independent computation capable of closing a missing modal/barrier layer has either been run or shown not to resolve the actual blocker.

If no candidate reaches `FULL_CLOSE`, the manuscript will report the preregistered search and the exact missing layer(s), rather than merely state that no matched case was found.
