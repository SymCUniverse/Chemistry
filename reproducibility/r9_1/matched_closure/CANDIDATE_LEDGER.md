# CSA R9.1 Matched-Closure Candidate Ledger

This ledger is evidence, not a results ranking. Statuses can only change after the corresponding gate evidence is recorded.

| Candidate | Lowercase chi | Modal/path | Independent barrier | Outcome | Current status | Immediate blocker |
|---|---|---|---|---|---|---|
| CO/Cu(001) frustrated translation / surface diffusion | PENDING-CONVENTION | PENDING-COMPUTE | PARTIAL-AVAILABLE | AVAILABLE | INVESTIGATE-FIRST | linewidth-to-damping convention; matched-T linewidth; quantitative mode-to-saddle overlap |
| Co2(CO)8 bridged/nonbridged isomerization | PENDING-SOURCE | PENDING-COMPUTE | AVAILABLE-IN-LITERATURE | AVAILABLE | INVESTIGATE | exact same-isomer T1/frequency extraction and carrier-to-TS mapping |
| HONO/Kr cis-trans | REFUSED-PENDING-T1 | PARTIAL-AVAILABLE | CONDITION-MISMATCH | AVAILABLE | NEAR-MISS | reaction decay is not automatically mode T1; matrix-matched barrier/transmission |
| Photoinduced ET GLE | REFUSED-NONMARKOVIAN-SCALAR | AVAILABLE-NATIVE-GLE | AVAILABLE-INDEPENDENT-FES | AVAILABLE | CONTROL-REFUSAL | scalar chi would violate the native memory-kernel description |

## Frozen literature anchors

- Graham, Hofmann & Toennies (1996), J. Chem. Phys., DOI 10.1063/1.471260: CO/Cu(001) frustrated-translation linewidth and lifetime.
- Graham et al. (1998), J. Chem. Phys., DOI 10.1063/1.476219: CO/Cu(001) vibrational/PES information and quasielastic diffusion barrier.
- Anna, Ross & Kubarych (2009), J. Phys. Chem. A, DOI 10.1021/jp903112c: Co2(CO)8 2D-IR exchange and temperature-dependent barrier analysis.
- Anna & Kubarych (2010), J. Chem. Phys., DOI 10.1063/1.3492724: Co2(CO)8 solvent-friction barrier-crossing test.
- Schanz, Botan & Hamm (2005), J. Chem. Phys., DOI 10.1063/1.1834567: HONO/Kr ultrafast IR-driven isomerization.
- Richter et al. (2004), J. Chem. Phys., DOI 10.1063/1.1632471: HONO six-dimensional ab initio isomerization surface.
- Angulo et al. (2017), J. Chem. Phys., DOI 10.1063/1.4990044: independently constructed FES plus non-Markovian friction for photoinduced electron transfer.

## Initial evidence notes

### CO/Cu(001)
Published low-coverage HAS gives the frustrated-translation loss near 3.94 +/- 0.07 meV. The 1996 study reports a zero-temperature extrapolated intrinsic broadening of 85 +/- 5 micro-eV and a quoted vibrational lifetime of 8 +/- 1 ps. The 1998 study reports diffusion-related quasielastic broadening above about 100 K and an activation energy of 31 +/- 10 meV. Independent PES calculations in later literature place the atop site minimum and bridge diffusion saddle on the same lateral coordinate, but the static PES barrier is not interchangeable with the QHAS activation energy.

### Co2(CO)8
2D-IR exchange directly observes bridged/nonbridged interconversion on the picosecond scale, and temperature-dependent rates exist. Separate quantum-chemical structures/barriers exist. Preliminary literature evidence also indicates carbonyl vibrational lifetimes substantially longer than exchange, but exact isomer/mode-specific T1 and a carrier-to-saddle modal overlap must be recovered before scalar/modal closure.

### HONO/Kr
OH-stretch pumping produces mode-selective isomerization with measured quantum yields and picosecond/nanosecond channels. A six-dimensional gas-phase surface exists. The published population decays cannot be relabeled as the mechanical damping T1 of the tracked mode without further evidence.

### Photoinduced ET GLE
The source explicitly uses an inertial GLE with a non-Markovian friction kernel projected onto a solvent-polarization coordinate. The FES is obtained from stationary spectroscopy and the friction from an independent Coumarin-153 calibration rather than target reaction fitting. This is strong end-to-end native dynamics, but it is intentionally retained as a negative control because collapsing the kernel to a local scalar damping ratio would violate CSA's scalar-admission rule.
