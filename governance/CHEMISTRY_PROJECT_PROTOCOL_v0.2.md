# Chemistry Project Protocol

Version: 0.2
Status: PREPARED FOR GOM v0.8.0 ADOPTION
Date: 14 September 2026
Applies to: SymCUniverse/Chemistry
Governing program manual: SymC General Operations Manual v0.8.0, Definitive Active Baseline
Supersedes on adoption: `governance/CHEMISTRY_PROJECT_PROTOCOL_v0.1.md`
Migration class: governance/documentation only
Scientific settings changed: no
Active execution changed: no

## 1. Purpose

This project protocol keeps Chemistry-specific scientific and implementation safeguards local under the SymC General Operations Manual v0.8.0. It extends the GOM and may be stricter, but it may not weaken MFR-14, native-model-first reasoning, epistemic classification, anti-circularity, refusal, reproducibility, Function Map/Limit Map, foundational-dependency safeguards, or the GOM migration-integrity rule.

Version 0.2 is a governance successor to Chemistry Project Protocol v0.1. It changes the governing authority from the historical General Protocol naming to the active GOM naming and preserves the Chemistry-specific scientific content of v0.1. Adoption changes no frozen scientific setting, threshold, historical outcome, Atlas entry, or active computation.

## 2. Chemistry System Model and Engine

The ChemSA System Model remains generator-first and the ChemSA Engine is its executable implementation.

Start with the actual governing dynamical generator and determine its eigenstructure before deciding whether a scalar chi is licensed. Numerical eigenvalue proximity, repeated roots, at-tolerance defectiveness, and structural exceptional-point certification are distinct claims.

Finite-precision classifications follow GOM Sections 18.1 and 40.3. For higher-order exceptional-point candidates, a single finite-precision instance cannot certify exact defectiveness. Parameter continuation or structural/symbolic proof is required for structural certification.

Vocabulary in manuscripts, reports, figures, metadata, and tool output must match the exact classification earned by the validated Engine or derivation.

## 3. Stable-well chi and barrier-crossing firewall

For a licensed stable second-order factor, canonical mechanical chi uses the restoring natural frequency `omega_0` and the corresponding damping convention under GOM Section 2.2.

Barrier-top `omega_b` is the magnitude of unstable barrier curvature used by barrier-crossing theories. It is not `omega_0` and may not be substituted into canonical mechanical chi to create a critical-damping interpretation. At a true barrier top the local fixed point is a saddle and the canonical restoring-system critical-damping boundary does not exist.

A stable-well damping coordinate, local chi, repeated-root result, or near-critical stable-well condition does not by itself establish reaction commitment, barrier crossing, first-passage probability, transmission coefficient, reaction rate, yield, selectivity, or catalytic optimality. Those are separate chemistry-native claims requiring the corresponding stochastic/dynamical model and evidence.

## 4. Estimator-equivalence safeguard

Different operational routes may estimate friction, damping, relaxation, or widths only under their own native validity conditions. Spectroscopic linewidths, solvent relaxation times, electronic-friction calculations, memory kernels, lifetimes, and related observables are not assumed to represent the same physical quantity merely because each can be placed into a dimensionless ratio.

Two estimator routes may be treated as interchangeable only after a derivation, calibration, or benchmark establishes that they recover the same native target quantity within a stated regime and uncertainty. Otherwise they remain distinct operational estimators or proxies with distinct epistemic classes.

Width conventions must state amplitude versus energy decay, full versus half width, angular versus ordinary frequency, and rate versus wavenumber. Pure dephasing, inhomogeneous broadening, orientation, instrumental broadening, and other non-dissipative contributions are separated or bounded before a width is interpreted as damping.

## 5. Memory and Markov safeguard

A Markovian or memoryless reduction is licensed only by comparison of the bath/environment memory timescale to the native local dynamical timescale relevant to the reduction. An unrelated global waiting time, overall reaction time, or remote observational timescale may not be used to justify local Markovianity.

Where memory is material, use the native non-Markovian or generalized-friction description, or lower the claim ceiling.

## 6. Barrier Height / Rate Atlas independence

The Barrier Height / Rate Atlas remains an independent evidence structure and is not folded into the ChemSA Engine unless a later science-breaking decision explicitly justifies integration.

The Engine may not use Atlas outcomes, favored residuals, observed rates, desired chi regions, or post-result agreement to tune its coordinate definitions, thresholds, estimators, or admission rules. The Atlas may interpret Engine outputs only after the coordinate is independently derived.

`Barrier_Height_Rate_Atlas_v0.9` remains immutable unless a separately versioned Atlas release is created. Historical grades, refusals, HOLDs, discrepancies, and provenance states are preserved.

## 7. Literature pairing and evidence tiers

For a literature-derived barrier/rate coordinate, all paired quantities must refer to the same chemical system, phase, temperature, medium, and reaction event unless the record explicitly demonstrates why a narrower equivalence is valid.

Both the rate and the barrier/frequency/friction quantities required for the coordinate must be numerically supported by the source record. Barrier or free-energy type must be explicit. Bounds are not central values. Figure-only extraction does not support a verified or locked coordinate unless a separately qualified measurement protocol permits it.

Evidence tiers follow GOM Section 18.2. Locked references require FULL evidence unless a stricter project rule applies. ABSTRACT evidence may support a verified value only when every condition needed for the intended pairing is explicitly present. SNIPPET and BLOCKED remain provisional.

Each literature record should preserve, where applicable: publication identity, exact source location, equation/table/sentence, extracted symbols and units, transformation/calculation used, retrieval date, source lineage, condition match, and independence pathway.

## 8. Source and family independence

Bibliographic records are not automatically independent evidence units. Track, where material, publication identity, source-record identity, underlying data origin, lineage, mechanistic family, and whether multiple rows share the same experiment, fitted model, simulation, or source table.

Multiple temperatures, pressures, or closely related conditions from one underlying source family do not automatically establish multi-family generality.

Independence is pathway-specific under GOM Section 12.3. Shared information that could force the tested agreement weakens or refuses the corresponding independence claim.

## 9. Representative-selection firewall

Evidence strength and model agreement remain distinct. A coordinate selected after observing the smallest residual, closest agreement, most favorable chi, or most visually compelling behavior is a post-result discovery/diagnostic representative unless its selection rule was frozen independently of the outcome.

A post-result representative may be studied, but it may not summarize confirmatory predictive performance. The full underlying family/distribution remains available and promotion debt is recorded under GOM Section 9.2.

## 10. Function Map and Limit Map for chemistry

Where native chemistry supports them, the project maps both:

- Function Map: how rates, modes, friction/memory behavior, coupling, environmental response, and local/system organization behave across supported regimes;
- Limit Map: where scalar reduction, estimator equivalence, Markovianity, inheritance, mode separation, barrier representation, or Engine admission ceases to hold.

A model limitation or refusal is not automatically a physical transition in nature. If a method-validity limit suggests a physical transition, that becomes a separate system-behavior hypothesis requiring its own MFR-14 record and untouched test.

## 11. Local versus embedded chemistry dynamics

A local molecular, adsorbate, phonon, solvent, or reaction-coordinate identity is distinct from its realized behavior after embedding in a surface, solvent, lattice, catalyst, network, or larger coupled environment.

Do not infer a whole-system scalar by averaging local chi values. Participation, observability, identifiability, coupling, feedback, modal reorganization, and hierarchical closure are audited separately. A system-level scalar must be separately derived and qualified.

## 12. Active computational evidence chains

Long-running first-principles and numerical workflows preserve exact scientific configuration, execution identity, checkpoint lineage, process-completion status, and scientific-completion status.

Mechanical recovery may resume from verified checkpoints without changing frozen physics. Unchanged deterministic failures are not rerun. A stale or superseded execution must refuse expensive continuation. Scientific/numerical HOLDs exit automatic recovery.

For active surface-convergence and substrate-inheritance work, layer depth, vacuum, k-mesh, pseudopotentials, cutoffs, relaxation constraints, force gates, reproduction gates, and other frozen settings remain project-local scientific commitments and are not modified by GOM adoption.

A governance migration must not restart, duplicate, invalidate, supersede, or reinterpret an in-flight computation. Before resuming or launching dependent work, the live branch, run identity, checkpoint lineage, active interlocks, and supersession state must be rechecked.

## 13. Reproducibility

Report R1, R2, and R3 separately:

- R1: release integrity/regeneration;
- R2: recomputation of scientific quantities from preserved inputs;
- R3: reconstruction of primary evidence and provenance.

A clean-room check of frozen outputs is not represented as calculation regeneration unless it actually rebuilds the declared outputs from the documented parent/source inputs.

## 14. Prediction and claim discipline

Classification success does not automatically establish predictive success for rate, yield, selectivity, catalysis, transfer, commitment, or another chemical outcome.

Any confirmatory chemistry prediction must satisfy MFR-14 and identify the strongest relevant native comparator, or record `NO_NATIVE_COMPARATOR` under the GOM when a good-faith frozen search establishes that no native method answers the same frozen task. Candidate comparators include only those scientifically appropriate to the question, such as Kramers/Grote-Hynes, transition-state/rate theory, direct dynamics, reactive flux, electronic-friction theory, Marcus-family theory, or another native method.

A SymC result that reproduces an established native result without prespecified incremental utility is EQUIVALENT, not ADDS.

## 15. GOM migration integrity and change control

All Chemistry-specific safeguards carried by Project Protocol v0.1 remain binding in v0.2 unless an explicit later project version retires or changes them with a documented reason. Removal of a project-specific rule from the program-wide GOM does not retire that Chemistry rule.

Change classification follows GOM Section 24. Mechanical changes may proceed only when scientific meaning is untouched. A science-adjacent change requires an explicit equivalence check and must be treated as scientific when equivalence is uncertain. A science-breaking change requires explicit authorization, versioning, and revalidation. The existing stricter Chemistry scientific-change controls remain in force and are not weakened by this mapping.

The Barrier Atlas, ChemSA scientific core, historical HOLDs/failures, and frozen system-specific convergence or acceptance settings are not altered by this governance migration.

## 16. Adoption gate

This protocol is prepared on the isolated branch `gom-v0.8.0-chemistry-adoption-prep` while the current frozen H/Ru(0001) L21 contingency computation remains active. It must not alter that execution, its configuration, its scientific interpretation, or its evidence lineage.

Before adoption to an execution-bearing branch, verify:

- the active computation has reached a valid terminal state or has been explicitly dispositioned;
- no scientific setting, threshold, Atlas content, historical HOLD, or frozen claim changed through the migration;
- Chemistry-specific safeguards remain at least as strict as the safeguards they replace or inherit;
- project control records are synchronized to the live computational state;
- stale or superseded execution paths are refused before expensive work;
- repository descriptions are re-synchronized with the adopted capability and authority naming.
