# Pending Result Inserts

Version: 0.1
Status: ACTIVE

This file is the bridge between long-running computations and the living manuscript. It records exactly what must be inserted when evidence closes, so the manuscript can advance without inventing results while computations are still active.

## PRI-01 — software/release audit

Target manuscript section: 4.1 Engine verification and software integrity.

Insert only after final audit:
- exact Engine/release identity;
- commit SHA and immutable archive/checksum;
- dependency/environment lock;
- real test count and validator/drift test count, separately stated;
- R1/R2/R3 reproducibility classification;
- clean-room result and what it actually regenerated;
- unresolved reproducibility debt, if any.

## PRI-02 — System 1 reconciliation

Target manuscript section: 4.2.

Before drafting results:
- identify the canonical System 1 evidence lineage;
- reconcile old manuscript wording against current files;
- retain negative/HOLD findings rather than silently dropping them;
- state the native dynamical model;
- state modal result, scalar coordinate if licensed, uncertainty, and refusal conditions;
- state whether the result is discovery, verification, or confirmatory.

## PRI-03 — CO/Cu terminal result

Target manuscript section: 4.3.

Required evidence:
- terminal workflow identity and frozen configuration;
- numerical convergence and force gates;
- structural model and surface setup;
- modal/eigenstructure output;
- local versus embedded comparison;
- sensitivity/robustness result;
- failure or refusal states;
- exact claim class that survives audit.

## PRI-04 — H/Ru(0001) L21 terminal result

Target manuscript section: 4.4.

Required evidence:
- terminal L21 run identity and branch;
- checkpoint lineage and supersession check;
- scientific completion status distinct from process completion;
- convergence evidence;
- final dissipation-coordinate literature disposition;
- modal/eigenstructure result;
- local versus embedded result;
- sensitivity/robustness result;
- any HOLD and its reason.

No manuscript inference is allowed from run duration, repeated mechanical failure, or the fact that contingency recovery was needed.

## PRI-05 — cross-system inheritance test

Target manuscript section: 4.5.

Required before any generalization:
- freeze the cross-system comparison rule before reading the combined outcome;
- define which quantities are being compared: modal, scalar, conglomerate/system organization;
- define uncertainty and admissible missingness/refusal;
- identify shared methodology that limits independence;
- separate common architecture from system-specific behavior;
- report discordant systems, not only concordant ones.

## PRI-06 — Barrier Height / Rate Atlas closure

Target manuscript section: 4.6.

Required:
- final version identity of the independent Atlas;
- counts by phase, mechanistic family, evidence tier, and source family;
- refused/HOLD/BLOCKED counts;
- source-family clustering/dependence analysis;
- exact transformations and units;
- sensitivity to inclusion/exclusion rules;
- no retroactive tuning from Engine outcomes.

## PRI-07 — native comparator freeze

Target manuscript section: 4.7.

For every predictive claim:
- freeze target and metric;
- specify strongest scientifically appropriate native comparator;
- if none exists, document the frozen good-faith search and `NO_NATIVE_COMPARATOR` rationale;
- preserve untouched test data/evidence;
- classify result as FAILS, EQUIVALENT, or ADDS rather than treating agreement alone as added value.

## PRI-08 — final abstract/conclusion

Target manuscript sections: Abstract and Conclusion.

Rewrite only after PRI-01 through PRI-07 are dispositioned. The abstract and conclusion must be generated from the closed claim ledger, not from the hoped-for narrative.
