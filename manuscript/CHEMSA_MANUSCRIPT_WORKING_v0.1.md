# Working Manuscript: Chemistry Stability Architecture

Version: 0.1
Status: ACTIVE DRAFT, NOT FOR SUBMISSION
Date: 14 September 2026
Governing authority: SymC General Operations Manual v0.8.0 + Chemistry Project Protocol v0.2 (prepared)

> **Draft-control note.** This manuscript is intentionally incomplete. Sections that depend on unfinished computations or unresolved source work are marked explicitly. No placeholder constitutes a result.

## Proposed title

**Stability Architecture in Chemical Dynamics: Generator-First Coordinates, Substrate Inheritance, and Independent Barrier-Rate Evidence**

Title status: WORKING. Final title should follow the actual evidence ceiling reached by the completed study.

## Abstract

Chemical dynamics span local vibrational relaxation, environment-coupled modes, barrier crossing, surface interactions, and system-level organization. A central difficulty is that a compact stability coordinate can be informative only when it is derived from the native dynamics and kept distinct from chemically different quantities that merely share similar dimensions or mathematical forms. Here we develop a generator-first Stability Architecture workflow for chemistry. The framework begins with the native dynamical generator, resolves mode structure before scalar reduction, and treats local scalar stability coordinates, modal structure, and embedded system organization as complementary rather than interchangeable descriptions. We impose explicit firewalls between stable-well dynamics and barrier-top kinetics, between independent and inherited evidence, and between classification and prediction. The computational program then tests how local dynamical structure changes with substrate or environmental embedding across multiple chemical systems, while an independent Barrier Height / Rate Atlas evaluates rate and barrier evidence without tuning the Engine. 

**PENDING_COMPUTATION:** The final abstract must be rewritten after the current convergence and substrate-inheritance computations are closed. Numerical claims, system counts, predictive comparisons, and any statement of cross-system transfer are intentionally absent here.

## 1. Introduction

Chemical systems rarely live in isolation. A molecular coordinate may be embedded in a solvent, lattice, catalytic surface, phonon bath, electronic environment, or larger reaction network. Once embedded, the behavior actually realized by the system can differ from the identity inferred from the isolated component. This creates a recurring interpretive problem: a local dynamical descriptor can be physically meaningful without being a complete descriptor of reaction outcome, system function, or whole-system stability.

The present work addresses that problem through a Stability Architecture approach. The starting point is not a preferred scalar but the native generator of the dynamics. Modal structure is resolved first where the model supports it. Scalar coordinates are admitted only when their derivation and units are licensed by that native model. System-level interpretation is then treated as a separate layer that must account for coupling, participation, observability, and embedding rather than averaging local scalar values.

This distinction matters especially in chemistry because several mathematically adjacent quantities are physically non-equivalent. A stable-well restoring frequency is not a barrier-top unstable curvature. A linewidth is not automatically a mechanical damping constant. A solvent relaxation time is not automatically interchangeable with an electronic-friction estimate. A repeated root or near-degeneracy is not automatically a structurally certified exceptional point. A local damping coordinate is not automatically a reaction rate, yield, transmission coefficient, or catalytic optimum.

The study therefore has two coupled but independent goals. First, the ChemSA Engine tests local and embedded dynamical structure under controlled computational changes, including substrate or environment inheritance. Second, an independent Barrier Height / Rate Atlas evaluates literature-derived kinetic and barrier coordinates under strict provenance and pairing rules. The two evidence streams may later be compared, but the Atlas does not tune the Engine and Engine outcomes do not determine Atlas admission.

## 2. Conceptual architecture

### 2.1 Three complementary views

The fullest working description of chemical stability architecture combines three views:

1. **Modal structure.** The mode-resolved spectrum, eigenvectors, couplings, repeated-root structure, and generator behavior.
2. **Scalar stability coordinates.** Compressed coordinates such as a licensed local chi when the native reduction supports one.
3. **Conglomerate or embedded organization.** The behavior of the coupled system after the local component is embedded in a surface, solvent, lattice, network, or other larger environment.

These are not competing descriptions. The scalar is a compression, the modal structure resolves what the compression hides, and the conglomerate description addresses organization that is not recoverable by scalar averaging alone.

### 2.2 Native-model-first rule

The governing equation or generator is identified before assigning a scalar coordinate. If a second-order stable restoring factor is genuinely present, a canonical damping-like coordinate may be defined using the corresponding restoring natural frequency and damping convention. If the system is not of that form, the scalar is not imported by analogy.

### 2.3 Stable-well versus barrier-top firewall

For a stable restoring coordinate, the natural frequency `omega_0` belongs to a local minimum. For barrier crossing, `omega_b` represents the magnitude of unstable barrier curvature. These are physically different objects. Substituting `omega_b` into a stable-well critical-damping formula would manufacture a critical boundary where the local barrier-top dynamics are actually saddle-like. Accordingly, barrier-rate analysis is handled separately using the appropriate native kinetic theory.

### 2.4 Classification versus prediction

A correct classification of dynamical structure does not by itself predict a chemical rate, yield, selectivity, or catalytic outcome. Any predictive claim must identify the outcome, the native comparator, the frozen test, and the untouched evaluation pathway. This manuscript will distinguish descriptive structure, mechanistic interpretation, and predictive utility throughout.

## 3. Methods

### 3.1 ChemSA System Model and Engine

The ChemSA System Model is generator-first. The executable Engine evaluates the native system representation, identifies eigenstructure, and applies finite-precision classifications only at the strength justified by the evidence. Numerical eigenvalue proximity, repeated roots, defectiveness at tolerance, and structural exceptional-point certification are not collapsed into a single label.

For higher-order candidates, structural certification requires parameter continuation, symbolic/structural reasoning, or another test that distinguishes a genuine structural feature from a finite-precision coincidence.

**PENDING_AUDIT:** Insert exact current Engine version, repository commit, environment, test count, and frozen configuration after the final pre-submission software audit.

### 3.2 Local and embedded calculations

The computational program evaluates a local chemical or adsorbate system and then examines behavior under controlled embedding or substrate changes. The key scientific question is not whether a single scalar remains numerically identical, but how the modal structure, licensed scalar coordinates, and system-level organization transform together.

Frozen numerical settings are system specific and include the applicable layer depth, vacuum, k-point mesh, pseudopotentials, cutoffs, relaxation constraints, force gates, reproduction gates, and convergence criteria. Governance changes do not alter these settings.

**PENDING_COMPUTATION:** Insert the final systems table after the active surface-convergence and substrate-inheritance computations terminate and pass audit.

### 3.3 Estimator-equivalence checks

Operational estimates of damping, friction, relaxation, or spectral width are treated as distinct unless a derivation or benchmark demonstrates equivalence in the regime studied. When spectral widths are used, the manuscript will state whether the quantity is an amplitude or energy decay, full width or half width, angular or ordinary frequency, and whether non-dissipative contributions such as pure dephasing or inhomogeneous broadening are separated or bounded.

### 3.4 Memory and Markov tests

Any Markovian reduction is justified by comparing the bath or environmental memory timescale with the native local dynamical timescale relevant to the reduction. A global reaction waiting time or unrelated observational timescale is not used as a substitute for this test.

### 3.5 Independent Barrier Height / Rate Atlas

The Barrier Height / Rate Atlas is maintained independently from the ChemSA Engine. A literature coordinate is admitted only when the paired quantities refer to the same chemical system, phase, temperature, medium, and reaction event, unless a narrower equivalence is explicitly justified. Both the kinetic quantity and the barrier/frequency/friction quantity required for the coordinate must be numerically supported by the source.

Evidence is classified by source access and provenance. FULL evidence is preferred for locked coordinates. ABSTRACT evidence is used only where every condition necessary for the intended pairing is explicit. SNIPPET and BLOCKED states remain provisional. Figure-only extraction is not treated as a locked numerical value unless a separately qualified measurement protocol permits it.

The Atlas remains independent of the Engine. Atlas outcomes are not used to tune Engine coordinates, thresholds, estimators, or admission rules.

### 3.6 Function Map and Limit Map

The study records both where the method works and where it stops being licensed. The Function Map will describe behavior across supported dynamical regimes. The Limit Map will identify failure of scalar reduction, estimator equivalence, Markovianity, mode separation, inheritance assumptions, identifiability, or barrier representation. A method limit is not automatically interpreted as a physical transition in nature.

## 4. Results

### 4.1 Engine verification and software integrity

**PENDING_AUDIT.** This section will report the final software release identity, test suite, clean-room regeneration status, and R1/R2/R3 reproducibility state. Historical release and regression milestones are retained in the repository but will not be copied into the final paper until reconciled against the release actually used for the manuscript.

### 4.2 System 1

**PENDING_RECONCILIATION.** Insert the first completed physical-system result from the current evidence lineage, including the exact native model, modal structure, licensed scalar coordinates, uncertainty, and failure/refusal conditions. Do not backfill from an obsolete manuscript.

### 4.3 System 2: CO/Cu surface program

**PENDING_COMPUTATION / PENDING_AUDIT.** Insert only after the current CO/Cu computational lineage is reconciled to a terminal, reproducible state. Required outputs include the frozen structural model, convergence evidence, modal/eigenstructure result, local versus embedded comparison, uncertainty or sensitivity analysis, and any refusal where the scalar reduction is not licensed.

### 4.4 System 3: H/Ru(0001) surface program

The H/Ru(0001) branch is used as an independent chemical-system test of the same general architecture rather than as a parameter-retuning exercise.

**PENDING_COMPUTATION.** The active L21 contingency computation remains unresolved at this manuscript version. No scientific outcome is inferred from its being active, long-running, mechanically difficult, or computationally expensive. Final text will be written from the terminal evidence only.

### 4.5 Cross-system substrate inheritance

**PENDING_COMPUTATION.** This section will ask whether embedding changes are consistent across systems at the level of modal structure, scalar coordinate behavior, and whole-system organization. A cross-system claim requires more than one successful example and will be bounded by the actual independence and diversity of the systems tested.

### 4.6 Barrier Height / Rate Atlas

**PENDING_ATLAS_CLOSURE.** The final paper will report the independently curated barrier/rate coordinates by phase and mechanistic family, including refusals and incomplete records. The primary analysis will preserve source-family dependence and will not treat multiple rows from one underlying experimental or simulation family as independent replications.

### 4.7 Native-comparator analysis

**PENDING_COMPARATOR_FREEZE.** Where the manuscript makes a predictive claim, the corresponding strongest scientifically appropriate native comparator will be specified and frozen before confirmatory evaluation. Reproducing a native result without incremental utility will be classified as equivalence rather than added predictive value.

## 5. Discussion

### 5.1 What a chemical stability coordinate can and cannot mean

The central interpretive result of this program is expected to be architectural rather than merely scalar. A scalar coordinate can provide a useful compressed location within a licensed dynamical reduction, but it does not replace mode-resolved structure and does not automatically survive embedding as a whole-system descriptor. The scientific object of interest is therefore the relation among local dynamics, modal reorganization, scalar compression, and embedded organization.

### 5.2 Substrate inheritance as a testable question

The substrate-inheritance program asks whether a local component carries a recognizable stability identity into a larger environment, whether the environment systematically transforms that identity, or whether the embedded dynamics become qualitatively different enough that the local scalar ceases to be a useful summary. These possibilities are experimentally and computationally distinguishable and should not be forced into a single inheritance narrative.

### 5.3 Relationship to barrier crossing

Stable-well dynamics may influence the environment in which barrier crossing occurs, but they are not themselves a barrier-crossing theory. The independent Atlas is therefore used to examine whether any relationship exists without defining that relationship into the coordinate. If a relationship appears, it must survive source-family controls, native comparator testing, and untouched evaluation before it is treated as predictive.

### 5.4 Limits

The final limitation section will include at minimum: system-count limits, family dependence, finite-size and convergence limits, estimator non-equivalence, non-Markovian regimes, failures of scalar reduction, observational identifiability, source-family dependence in the Atlas, and the difference between computational embedding and laboratory perturbation.

## 6. Experimental opportunities

The computational architecture generates laboratory questions rather than replacing them. Candidate experiments should be designed first from the scientific uncertainty, then checked against the literature to determine which questions are genuinely unanswered.

Priority experiment classes for later closure include:

- controlled changes of substrate, coverage, isotopic mass, or adsorbate environment while tracking vibrational modes and linewidth/relaxation observables;
- temperature- or pressure-dependent perturbations that separate intrinsic mode changes from bath/friction changes;
- pump-probe or time-resolved measurements capable of distinguishing population relaxation from dephasing where the relevant timescales are accessible;
- paired kinetic and spectroscopic measurements on the same system and conditions to test whether a stable-well coordinate has any independent relationship to barrier-crossing observables;
- deliberately non-Markovian environments where the memory safeguard predicts failure of the simpler reduction.

**PENDING_LITERATURE:** Each candidate class requires a structured novelty collision against existing experiments before being promoted as a proposed new experiment.

## 7. Reproducibility and data availability

The release will report reproducibility at three levels: R1 release integrity/regeneration, R2 recomputation of scientific quantities from preserved inputs, and R3 reconstruction of primary evidence/provenance. These levels will not be merged into a single reproducibility claim.

Code, frozen configuration, system inputs, derived tables, provenance records, and the manuscript evidence ledger will be versioned in the repository or release package according to license and storage constraints.

**PENDING_RELEASE:** Insert archive identity, commit SHA, environment lock, data locations, checksums, and clean-room verification results.

## 8. Conclusion

This work develops a chemistry-specific Stability Architecture in which the native generator, modal structure, scalar coordinates, and embedded organization are kept physically distinct while remaining mathematically connected. The study is designed so that negative results are informative: a failed scalar reduction, absent inheritance pattern, non-Markovian regime, or lack of predictive relationship to kinetics constrains the architecture rather than being hidden as a failed fit.

**PENDING_FINAL_EVIDENCE:** The final conclusion will state only the cross-system and predictive claims actually supported after the active computations, Atlas closure, native-comparator analysis, and reproducibility audit are complete.
