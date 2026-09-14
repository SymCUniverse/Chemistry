# Validated Substrate Inheritance Contract v0.3

**Status:** current architectural contract  
**Effective date:** 2026-09-14  
**Supersedes for current architecture:** `VALIDATED_SUBSTRATE_INHERITANCE_CONTRACT_v0.2.md`  
**Historical v0.1 and v0.2 remain preserved.**  
**Program authority:** SymC General Operations Manual v0.8.0

v0.3 preserves the scientific scope and fail-closed semantics of v0.2. It updates the program-governance pointer, the H/Ru(0001) current state, and the explicit foundational-robustness interlock. It does not issue a substrate certificate or relax a prior requirement.

## 1. Scope

Substrate inheritance is a bounded reuse rule for a **qualified substrate representation**. It is not inheritance of a chemical conclusion, rate, mechanism, damping object, stability class, or universal material property.

A substrate certificate is issued only to the exact System Model version that passes the numerical and reproduction gates required for the substrate claim. A failed or still-qualifying version has no certificate merely because a nearby version, deeper slab, denser grid, or different material behaved well.

Where the substrate is a material upstream dependency for substantial downstream work, GOM Section 11.3 also applies: a bounded prospectively specified robustness challenge may govern whether a minimum-gate PASS is inherited as settled foundation. Such a challenge does not rewrite the minimum gate.

## 2. What may be inherited

After a clean-surface representation has passed its required qualification, reproduction, and any active foundational-dependency interlock, downstream calculations that preserve the certified substrate-defining assumptions may reuse the conclusion that the finite substrate representation is numerically adequate within that qualified scope.

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

Under the GOM P0-Q structure, a failed qualification may inform a versioned successor representation. If that successor later passes its required qualification, reproduction, and applicable dependency interlocks, the successor may receive a new substrate certificate.

The certificate must retain lineage to:

1. the failed parent qualification;
2. the evidence that informed the successor;
3. the exact change from parent to successor;
4. the unchanged or separately justified acceptance rule;
5. the new qualification and reproduction evidence;
6. any bounded foundational robustness challenge that materially governed downstream inheritance.

A successor PASS does not convert the parent HOLD into PASS and does not make reused qualification evidence untouched P1 confirmation.

## 4. Function Map and Limit Map inheritance

The certificate may carry both a Function Map and a Limit Map.

The Function Map records the numerical/physical region in which the substrate representation has demonstrated adequacy. The Limit Map records observed boundaries, failed grids, finite-size sensitivity, regime changes, or other states where reuse is not licensed.

Inheritance is allowed only inside the demonstrated scope. A downstream calculation that approaches or crosses a mapped limit triggers a typed HOLD or targeted requalification rather than silent extrapolation.

A later robustness contradiction reopens the materially affected certificate scope. A successful bounded challenge does not silently expand the certificate beyond the tested region.

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

These exclusions follow from the limited claim actually established by clean-surface convergence.

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

Atlas admission cannot repair a failed substrate gate or a failed foundational robustness challenge.

## 8. Current system-specific certificate states

### CO/Cu(111)

`CERTIFICATE_STATE = NOT_YET_ISSUED`

The repository contains authorized P0-Q depth-continuation routes, but live Kaggle execution is not established from repository state alone. Historical numerical HOLDs remain part of the Limit Map. Any eventual certificate belongs to the exact successor surface version that satisfies its required frozen numerical, reproduction, and applicable dependency gates.

### H/Ru(0001)

`CERTIFICATE_STATE = NOT_YET_ISSUED`

The historical L15/L17/L19 extension and original K16 coupled recheck remain preserved, including `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD` on the K16-to-K20 k-mesh axis.

A versioned P0-Q successor has now passed a fresh four-case fixed-grid qualification at **L17 / 15 A total vacuum / K24x24x1**. Source run `34769372617` returned `CLEAN_SURFACE_FIXED_GRID_PASS` with unchanged tolerance 0.001 eV/surface atom and fresh endpoint deltas:

- L17 to L19 at K24: 0.0001647649442020338 eV/surface atom;
- K24 to K28 at L17: 0.0003077607798331883 eV/surface atom;
- V15 to V25 at L17/K24: 0.0000020408515410963446 eV/surface atom.

This establishes the minimum fixed-grid gate for the successor but **does not yet issue the Ru(0001) substrate certificate**. Two further controls remain:

1. the user-authorized GOM Section 11.3 foundational robustness hold must resolve the already-running fresh L21/V15/K24 challenge under `SYSTEM3_L17_FOUNDATIONAL_ROBUSTNESS_HOLD_v0.1.json`; and
2. the clean-surface relaxation and independent reproduction gate in `SYSTEM3_CLEAN_RU0001_RELAXATION_PROTOCOL_v0.1.json` must pass.

If the L21 challenge contradicts the selected L17 foundation, the affected layer-depth conclusion is reopened and relaxation remains held. If robustness is supported, the previously earned fixed-grid PASS may enter the frozen relaxation/reproduction gate. The certificate is issued only after that gate passes and the exact certificate scope/provenance is recorded.

### Na/Cu(001)

Any reusable certificate must be tied to the final documented Na/Cu(001) qualification state and exact model scope rather than inferred from its role as the development pilot. This contract does not create a certificate where the system-specific evidence record has not explicitly issued one.

## 9. Claim-specific reuse and stopping

Once a valid substrate certificate covers the numerical substrate claim needed by a downstream calculation, the entire clean-surface convergence campaign need not be repeated for every compatible adsorbate or reaction.

Additional deeper or denser clean-surface runs may continue as robustness or Function/Limit evidence. They do not silently expand the certificate. If they reveal a material contradiction with the certified region, the conflict is preserved and the affected certificate scope is reopened.

A prospectively completed robustness challenge does not create an automatic infinite ladder. Further escalation requires a new scientific reason.

## 10. Fail-closed rule

When it is unclear whether a downstream state remains inside the qualified substrate scope, inheritance is **held**, not assumed.

The guiding question is not simply whether the element and Miller index are the same. It is whether the evidence that supported the substrate certificate still applies to the physical and computational state used by the downstream claim.
