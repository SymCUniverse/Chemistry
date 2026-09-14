# ChemSA: Generator-First Stability Analysis in Chemistry

This repository contains the current ChemSA chemistry program, its reproducibility assets, the Barrier-Height/Rate Atlas, prospective computational system tests, and a living working manuscript.

**Current program authority:** SymC General Operations Manual (GOM) v0.8.0, 14 September 2026. Chemistry-specific safeguards that no longer belong in the domain-neutral GOM are maintained explicitly in `governance/CHEMISTRY_PROJECT_GUARDRAILS_v0.1.md`.

**Living manuscript:** `manuscript/working/CHEMSA_LIVING_MAIN.tex`. The `manuscript/working/` tree is deliberately mutable and is **not** a release or submission-ready product. It exists so the scientific text, evidence state, and code/provenance can evolve together in the repository rather than in an untracked local copy.

The present scientific scope is **generator first**. A scalar stability coordinate is reported only when the physical and mathematical reduction that licenses it has been established. Scalar quantities remain attached to the mode, reaction coordinate, subspace, or generator from which they are derived.

## Current core

For an identified stable second-order damped mode,

```math
\chi = \frac{\Gamma}{2\Omega}
```

is a legitimate mechanical damping ratio. In that restricted setting, `chi < 1`, `chi = 1`, and `chi > 1` describe underdamped, repeated-root/critical, and overdamped modal morphology.

ChemSA does **not** treat this scalar as a universal reaction-rate coordinate or a system-wide stability number. For a general first-order or coupled generator, the engine withholds mechanical `chi` unless the required scalar or proportionally damped modal reduction is independently licensed.

The classifier instead preserves the relevant spectral and modal structure, including multiplicity, defectiveness at tolerance, conditioning, provenance, and response geometry.

## Exceptional-point classification

A repeated eigenvalue is not automatically an exceptional point. A semisimple degeneracy retains independent eigenvectors, whereas an exceptional point is defective.

ChemSA therefore distinguishes eigenvalue coincidence from eigenvector deficiency and scopes every exceptional-point interpretation to the declared provenance of the supplied equation. Crowded or numerically unresolved neighborhoods are returned as unresolved rather than promoted.

## Scalar-modal-system reporting discipline

Promoted chemistry stability results preserve complementary views rather than forcing one scalar to carry the whole system:

- governing generator, Hessian/dynamical object, response operator, or justified reduced model;
- licensed scalar coordinate set and applicable competing margins;
- modal/eigenvector/reaction-coordinate/subspace geometry;
- explicit scalar-to-mode or scalar-to-subspace assignment;
- conglomerate/system organization and inter-channel relation where applicable;
- uncertainty, conditioning, provenance, admissibility, and refusal state.

Scalar, modal/vector, and conglomerate/system views are starting representation components, not an exhaustive decomposition of stability architecture. A scalar is not selected because it happens to lie near a preferred value, and a mode is not selected after inspecting the desired outcome.

The frozen inheritance contract is:

`systems/CHEMISTRY_STABILITY_ARC_INHERITANCE_v0.1.json`

## Barrier crossing is a separate dynamical question

A stable well mode and an inverted transition-state mode are not governed by the same critical-damping geometry.

For an isolated scalar inverted barrier coordinate,

```math
q'' + \gamma q' - \omega_b^2 q = 0,
```

the discriminant is

```math
\frac{\gamma^2}{4} + \omega_b^2,
```

which does not vanish for real damping and nonzero barrier frequency. There is therefore no mechanical critical-damping boundary at the saddle analogous to `chi = 1` for a stable well.

Barrier-top `omega_b` is a native barrier-kinetics quantity and must not be silently substituted for the restoring `omega_0` of the canonical damped oscillator. Barrier transmission is handled with the appropriate reactive-pole or transmission description. The current engine does not infer a reaction rate from local spectral architecture alone.

## Barrier-Height/Rate Atlas

Barrier-Height/Rate Atlas v0.9 is a **frozen retrospective independent evidence product**. It contains 61 physical coordinates across 26 families and all 18 operational classes in the current atlas taxonomy. It remains read-only relative to confirmatory System Model/Engine logic and is not mutated in place by later research.

Any future extension that changes the evidence product is separately versioned, for example as v0.10 or an explicitly separate extension.

The validation rules explicitly forbid substituting well-side ChemSA `chi` for barrier-local friction. Barrier height, reaction rate, damping morphology, transmission, friction regime, and exceptional-point proximity remain distinct quantities unless a separately frozen comparison establishes a relation.

## Current prospective computational systems

### System 2: CO/Cu(111)

The CO/Cu(111) program is a frozen, staged first-principles qualification lane. Numerical convergence, clean-surface validation, adsorption-site ordering, reaction-path construction, and later dissipation validation are separated so kinetic outcomes cannot tune upstream electronic-structure choices.

Repository launch routes for the L15/L17 and L19 continuation are wired, but current live Kaggle execution is **not established from repository evidence**. Historical numerical HOLDs remain part of its Limit Map, and no substrate-inheritance certificate is presently issued.

### System 3: H/Ru(0001)

H/Ru(0001) is the selected contrast/limit system and is currently in **P0-Q controlled qualification**.

The historical L17/V15/K16 coupled gate remains `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD` because the K16-to-K20 k-mesh substitution changed the clean-surface excess by about 2.479 meV/surface atom, outside the unchanged 1 meV criterion.

A versioned successor at **L17 / 15 A total vacuum / K24x24x1** has now earned a fresh four-case `CLEAN_SURFACE_FIXED_GRID_PASS`. The fresh endpoint changes are:

- L17 to L19 at K24: **0.164765 meV/surface atom**;
- K24 to K28 at L17: **0.307761 meV/surface atom**;
- V15 to V25 at L17/K24: **0.002041 meV/surface atom**.

All are inside the unchanged 1.000 meV/surface-atom criterion. The original K16 HOLD is preserved, and the successor result remains P0-Q rather than untouched P1 confirmation.

Before substantial downstream chemistry inherits L17 as settled substrate foundation, a prospectively frozen **L21/V15/K24 foundational robustness challenge** is being completed under `systems/h_ru0001/SYSTEM3_L17_FOUNDATIONAL_ROBUSTNESS_HOLD_v0.1.json`. Both L17-to-L21 and L19-to-L21 must remain within the same 1 meV criterion. A successful challenge stops the automatic layer ladder; a contradictory challenge reopens the affected layer-depth foundation.

Clean-surface relaxation/reproduction is therefore prepared but operationally held. The substrate certificate is `NOT_YET_ISSUED`. H adsorption, paths, barriers, quantum-nuclear rates, and stability interpretation remain downstream of their own gates.

No H/Ru ChemSA `chi` is assigned until a physically matched projected damping/friction quantity and the corresponding mode or reaction coordinate pass their validators. The current public-source dissipation audit remains `DISSIPATION_NOT_ESTABLISHED`.

## Reproducibility

Repository code and deposited data are the canonical computational sources for numerical results. Published figures and tables should be reproducible from preserved scripts and source data, with hashes and validation records retained where material.

Historical failures, refusals, numerical HOLDs, superseded mechanical execution routes, and qualification-informed successor paths remain part of the provenance record and are not rewritten as successes.

For H/Ru(0001), the current clean-surface reproducibility state is tracked in `systems/h_ru0001/SYSTEM3_REPRODUCIBILITY_PREFLIGHT_v0.2.json` and `systems/h_ru0001/SYSTEM3_STATE_LEDGER_v0.3.json`.

## Scope and nonclaims

The current program does not claim that:

- one scalar describes every chemical stability problem;
- `chi = 1` is a universal reaction-rate optimum;
- `chi = 1` is a barrier-top critical point;
- a linewidth by itself is a mechanical damping coefficient;
- a repeated eigenvalue by itself establishes an exceptional point;
- local spectral architecture determines reaction rate, yield, selectivity, or commitment probability;
- quantities from different physical modes, generator classes, temperatures, media, or coordinate definitions may be pooled without an explicit matching contract.

Refusal, unresolved status, or nonidentifiability is a valid result when the required reduction, comparator, numerical qualification, or provenance is absent.

## Repository contents

The repository includes current and historical manuscript assets, the living manuscript workspace, reproducibility packages, Barrier Atlas data and validation tools, governance/migration records, and prospective computational workflows for chemistry systems under test.

Historical files are preserved as lineage. Current-state documents explicitly supersede them rather than silently rewriting them. See each protocol, state ledger, validation record, and reproducibility file for the exact scientific contract that applies to that object.
