# Validated Substrate Inheritance Contract v0.2

**Status:** current architectural contract  
**Effective date:** 2026-09-11  
**Supersedes for current architecture:** `VALIDATED_SUBSTRATE_INHERITANCE_CONTRACT_v0.1.md`  
**Historical v0.1 remains preserved.**

## 1. Scope

Substrate inheritance is a bounded reuse rule for a **qualified substrate representation**. It is not inheritance of a chemical conclusion, rate, mechanism, damping object, stability class, or universal material property.

A substrate certificate is issued only to the exact System Model version that passes the numerical and reproduction gates required for the substrate claim. A failed or still-qualifying version has no certificate merely because a nearby version, deeper slab, denser grid, or different material behaved well.

## 2. What may be inherited

After a clean-surface representation has passed its required qualification, downstream calculations that preserve the certified substrate-defining assumptions may reuse the conclusion that the finite substrate representation is numerically adequate within that qualified scope.

Depending on the certificate, inheritable fields may include:

- substrate material and facet;
- qualified slab thickness or depth rule;
- vacuum/electrostatic treatment;
- reciprocal-space resolution rule;
- bulk chemical-potential/reference construction;
- exchange-correlation treatment;
- pseudopotential family/valence definition;
- spin/relativistic treatment where material;
- surface-cell convention;
- permitted clean-surface relaxation convention;
- exact Engine/runtime/provenance identities required by the certificate.

What is inherited is the **qualification certificate plus provenance**, not a frozen set of atomic positions for all future chemistry. Downstream protocols may relax the substrate degrees of freedom they explicitly permit.

## 3. P0-Q successor rule

Under General Protocol v0.7.1A, a failed qualification may inform a versioned P0-Q successor representation. If that successor later passes its required qualification, the successor may receive a new substrate certificate.

The certificate must retain lineage to:

1. the failed parent qualification;
2. the evidence that informed the successor;
3. the exact change from parent to successor;
4. the unchanged or separately justified acceptance rule;
5. the new qualification and reproduction evidence.

A successor PASS does not convert the parent HOLD into PASS and does not make the reused qualification evidence untouched P1 confirmation.

## 4. Function Map and Limit Map inheritance

The certificate may carry both a Function Map and a Limit Map.

The Function Map records the numerical/physical region in which the substrate representation has demonstrated adequacy. The Limit Map records observed boundaries, failed grids, finite-size sensitivity, regime changes, or other states where reuse is not licensed.

Inheritance is allowed only inside the demonstrated scope. A downstream calculation that approaches or crosses a mapped limit triggers a typed HOLD or targeted requalification rather than silent extrapolation.

## 5. Cases that do not inherit automatically

A clean-surface certificate does not automatically transfer to:

- another material;
- another facet, step, terrace, defect, reconstruction, alloy, oxide, or morphology;
- a materially strained or high-coverage state outside the qualified surface representation;
- a changed exchange-correlation functional, pseudopotential family, valence treatment, dispersion model, spin model, relativistic treatment, or other material Hamiltonian change;
- a changed electrostatic model, charge state, applied field/electrode potential, explicit solvent, dipole/ESM treatment, or other boundary condition that changes the modeled surface response;
- lateral supercell or coverage convergence;
- an adsorbate-specific k-point claim merely by copying the clean primitive-cell integer mesh instead of preserving or requalifying appropriate reciprocal resolution;
- adsorption-site ordering or adsorption energy;
- reaction-path, NEB-image, saddle-force, or barrier convergence;
- Hessians, vibrational frequencies, transmission coefficients, nuclear-quantum convergence, friction, damping, rate constants, or ChemSA eligibility;
- a different temperature/pressure/coverage/phase regime that materially changes the physical substrate state.

These exclusions are not administrative caution. They follow from the limited claim actually established by clean-surface convergence.

## 6. Adsorbate perturbation rule

Adding an adsorbate does not automatically invalidate a clean-substrate certificate, but the downstream protocol must test the numerical dimensions that the adsorbate can materially perturb.

For example, a clean-slab depth certificate does not itself establish that:

- the adsorbate is noninteracting with lateral periodic images;
- the clean-surface k-mesh remains sufficient for adsorption-energy differences or barriers;
- the permitted relaxation depth remains adequate around the adsorbate;
- dipoles, charge transfer, reconstruction, or subsurface penetration leave the certified physical state unchanged.

If downstream evidence exposes a substrate-defining perturbation outside the certificate, only the affected dimension is requalified where scientifically defensible. Unaffected, hash-verified evidence may remain reusable.

## 7. Relation to the Independent Atlas

Substrate inheritance is System Model infrastructure. It does not write a chemical conclusion into the Independent Atlas and it does not allow the Atlas to tune the substrate model.

A downstream barrier/rate record may cite a substrate certificate as provenance while still carrying independent fields for barrier, prefactor, reaction-coordinate validation, dissipation, experimental comparison, and ChemSA eligibility.

Atlas admission cannot repair a failed substrate gate.

## 8. Current system-specific certificate states

### CO/Cu(111)

`CERTIFICATE_STATE = NOT_YET_ISSUED`

The repository contains authorized P0-Q depth-continuation routes, but live Kaggle execution is not established from repository state alone. Historical numerical HOLDs remain part of the Limit Map. Any eventual certificate belongs to the exact successor surface version that satisfies its required frozen numerical and reproduction gates.

### H/Ru(0001)

`CERTIFICATE_STATE = NOT_YET_ISSUED`

The L15/L17/L19 depth extension passed with L17 selected against L19, but the required coupled endpoint recheck returned `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD` on the k-mesh axis. Therefore no Ru(0001) clean-surface certificate exists yet and relaxation cannot be used to rescue the failed fixed-grid version.

The active K20/K24/K28 work is P0-Q Function/Limit mapping. If it supports a versioned successor grid, that successor must pass its own required qualification before a Ru(0001) certificate can be issued.

### Na/Cu(001)

Any reusable certificate must be tied to the final documented Na/Cu(001) qualification state and exact model scope rather than inferred from its role as the development pilot. This contract does not create a certificate where the system-specific evidence record has not explicitly issued one.

## 9. Claim-specific reuse and stopping

Once a valid substrate certificate covers the numerical substrate claim needed by a downstream calculation, the entire clean-surface convergence campaign need not be repeated for every compatible adsorbate or reaction.

Additional deeper or denser clean-surface runs may continue as robustness or Function/Limit evidence. They do not silently expand the certificate. If they reveal a material contradiction with the certified region, the conflict is preserved and the affected certificate scope is reopened.

## 10. Fail-closed rule

When it is unclear whether a downstream state remains inside the qualified substrate scope, inheritance is **held**, not assumed.

The guiding question is not simply whether the element and Miller index are the same. It is whether the evidence that supported the substrate certificate still applies to the physical and computational state used by the downstream claim.
