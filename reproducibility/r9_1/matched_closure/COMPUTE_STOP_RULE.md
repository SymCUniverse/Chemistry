# Matched-Closure Compute Decision

## Decision

Do **not** launch additional Rowan jobs for this closure campaign.

## Reason

The unresolved gates are not static electronic-structure quantities that the available workflows can repair.

### CO/Cu(001)
A new Hessian or path projection could quantify the rotational admixture of the frustrated translation against the bridge saddle. That would improve G4. It would not create the missing independent damping record at the same temperature and coverage as the diffusion measurement. Since G1 would remain failed, new compute cannot yield `FULL_CLOSE`.

### Co2(CO)8
A TS search/frequency/IRC workflow could independently reproduce the bridge-opening pathway and basin frequency. The decisive missing evidence is an independently obtained solvent reaction-coordinate friction or memory kernel under the 2D-IR conditions. The published Kramers mapping varies dynamical parameters against the target rate series. Static QM does not repair G7.

A proper rescue would require a new explicit-solvent equilibrium-dynamics campaign with a predefined reaction coordinate and memory-kernel extraction, independent of the measured exchange rates. That is a new scientific experiment/simulation campaign rather than a mechanical continuation of the current paper.

### HONO/Kr
The problem is experimental channel decomposition. The measured OH-stretch population loss shares timescales with IVR and reactive transfer. A new isolated-molecule PES cannot make the measured decay an independent bath-only damping constant.

### Angulo photo-ET
The source-native non-Markovian GLE is already the appropriate model. Additional computation to force a one-number damping ratio would violate the scalar-license gate.

## Stop-rule result

The preregistered requirement that affordable computation be run **or shown unable to resolve the actual blocker** is satisfied. No compute was withheld that could by itself change a candidate from its final class to `FULL_CLOSE`.
