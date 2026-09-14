# Barrier-Height/Rate Atlas v0.10 Prospectus v0.1

**Date:** 14 September 2026  
**Status:** PROSPECTUS ONLY / NO v0.10 RELEASE OPENED  
**Parent:** Barrier-Height/Rate Atlas v0.9, frozen and immutable  
**Program authority:** SymC General Operations Manual v0.8.0

## Purpose

This document defines how any future changed Barrier-Height/Rate Atlas must begin so that v0.9 remains a fixed evidence product. It does not add, delete, regrade, or reinterpret a v0.9 coordinate and is not itself an Atlas release.

## Version boundary

A v0.10 or separately named successor is required before any of the following can enter the evidence product:

- a new physical coordinate;
- removal or replacement of an existing physical coordinate;
- a changed evidence grade;
- a changed source/provenance relation;
- a changed independence classification;
- a changed proxy/reconstruction method;
- a changed operational-class definition;
- a changed validator/admission rule;
- a genuinely prospective new computation or experiment.

None of those changes are made in place to v0.9.

## Candidate objectives, ordered by information value

### 1. Surface depth with less reconstruction dependence

Target direct numeric surface rates/barriers and condition-matched friction information where the public literature provides them. The goal is not simply more surface rows; it is to reduce the current dependence on Grade C Arrhenius reconstruction/proxy evidence.

### 2. Solid-state molecular/mode-resolved kinetics

Prefer directly resolved hopping or mode-specific kinetic quantities over bulk conductivity proxies when the literature makes that possible. Collective conductivity remains useful evidence but should not be upgraded into a molecular rate by reinterpretation.

### 3. Independent family replication

Prioritize families whose current depth is limited by same-study or same-source dependence. New coordinates are most valuable when they create a new evidentiary pathway rather than another replicate under the same hidden assumptions.

### 4. Prospective theory/experiment separation

Where new computation is performed by this project, freeze the model/method/thresholds before the held-out experimental target is inspected for validation. The Atlas should make the discovery/qualification/holdout role machine-readable.

### 5. Native friction/dissipation fields

Admit friction, memory kernels, transmission coefficients, or damping objects only when the source/model actually defines the native quantity for the same system, phase, temperature, medium, and reaction coordinate. A barrier frequency or measured rate cannot be used as a surrogate friction merely to complete a coordinate.

### 6. Refusal-preserving literature search

If a target family lacks public numeric evidence that satisfies the matching contract, retain the candidate as held/refused rather than weakening the contract or relying on figure-only values. Repository-hosted author copies and ResearchGate/institutional copies are acceptable when publication identity is independently verified; unpublished preprints are not final evidence.

## Prospective v0.10 entry contract to freeze before data promotion

A future v0.10 protocol should make explicit, before promoted new rows are inspected:

1. target families/environments and why they add information;
2. allowed source classes and free-access retrieval rules;
3. exact condition-matching fields;
4. independence dimensions and promotion ceilings;
5. direct/reconstructed/proxy labels;
6. barrier-type and rate-type compatibility;
7. friction/transmission semantics where used;
8. figure-only numeric refusal rule;
9. calibration versus validation separation;
10. stopping rule based on information gain rather than a required row count;
11. clean-room release/manifest/validator requirements;
12. explicit statement that v0.9 remains untouched.

## Relation to the user's existing phase-depth objective

The historical target of roughly 7--10 barrier-rate coordinates per physical phase remains a useful design aspiration **only where the literature supports it without weakening evidence rules**. It is not a quota. A smaller direct, independent set outranks a larger set padded with proxies or nonmatched conditions.

The preferred growth order remains from simpler reactions to more complex mechanisms:

- gas-phase atom transfer / abstraction / isomerization;
- solution substitution / association / electron-transfer / PCET;
- surface diffusion/reaction with direct kinetic observables;
- condensed conformational or lattice processes with reactive-flux/memory information where possible.

## v0.10 launch gate

`V0_10_RELEASE_OPEN = false`

Opening v0.10 requires a separately frozen versioned protocol that implements the entry contract above. This prospectus alone does not authorize data migration or code changes to the frozen v0.9 release.

## No-change declaration

`V0_9_MUTATED = false`

`V0_9_EVIDENCE_GRADES_CHANGED = false`

`V0_9_VALIDATORS_CHANGED = false`

`V0_9_COORDINATES_CHANGED = false`

`SCIENTIFIC_RESULT_CREATED_BY_THIS_PROSPECTUS = false`
