# Barrier-Height/Rate Atlas v0.9 GOM v0.8.0 Migration Audit v0.1

**Date:** 14 September 2026  
**Atlas state:** FROZEN RELEASE  
**Program authority:** SymC General Operations Manual v0.8.0  
**Migration decision:** PRESERVE v0.9 UNCHANGED; any changed evidence product is a separately versioned successor.

## 1. Frozen release identity verified from the v0.9 release records

The retained v0.9 verification and process reports identify:

- 61 physical coordinates;
- 26 reaction families;
- all 18/18 operational classes represented;
- 67 sources;
- 11 Grade A, 30 Grade B, and 20 Grade C coordinates;
- 80 replicates;
- 27 held/refused candidates;
- zero ChemSA source modifications.

Physical-environment depth is:

- gas: 20;
- aqueous solution: 15;
- organic solution: 7;
- enzyme active site: 5;
- surface: 7;
- solid state: 5.

The two cross-phase records remain comparison architectures and are explicitly excluded from physical-environment padding.

## 2. Preserved validation state

The frozen verification report records:

- v0.3 through v0.7 release regressions: PASS;
- v0.8 semantic inheritance: PASS;
- v0.9 release validator: PASS with zero failures;
- dependency-free adversarial checks: 131/131;
- Atlas pytest suite: 113/113;
- focused ChemSA boundary suite: 138/138;
- workbook verification: PASS;
- 228 formulas across 11 workbook sheets;
- zero cached formula errors.

This migration audit does not relabel those historical executions as new September 2026 executions. It preserves the verification claims exactly at the scope reported by v0.9.

## 3. GOM migration-integrity mapping

### Independent Atlas architecture

v0.9 remains an **Independent Atlas**, not a writable state table for a confirmatory System Model/Engine. A confirmatory or predictive engine may read a frozen Atlas under an explicitly licensed comparison but may not write, retune, regrade, or select upstream model settings using Atlas agreement.

### Evidence classes and non-inflation

The existing A/B/C evidence grading, proxy/reconstruction labels, held/refused candidates, source lineages, and independence ceilings remain project-local Atlas semantics. They are not removed merely because v0.8.0 is domain-neutral.

The GOM migration therefore preserves the following v0.9 refusals:

- primary-source retrieval alone cannot promote a retrospective row to prospective confirmation;
- same-study hydride rows cannot be treated as independent cross-publication closure;
- the TEMPO PCET calibration anchor cannot validate the relation calibrated on itself;
- rate-derived enzyme energies cannot be recycled as independent barriers;
- reconstructed surface point rates cannot be relabelled raw measurements;
- collective conductivity proxies cannot be converted into molecular rates or promoted above their earned Grade C role;
- cross-phase comparison rows cannot pad physical-environment counts;
- target-calibrated theory cannot be counted as independent validation of the same target.

### Function Map and Limit Map

The Atlas is not required to make every family agree. Large residuals remain evidence. Examples intentionally retained by v0.9 include the 4-OT underprediction, large Au/Cu formate reconstruction residuals, and solid-state conductivity-proxy discrepancies. These are Function/Limit information, not rows to tune away.

### Native-semantics firewall

Barrier height, barrier-top frequency, reaction rate, friction regime, transmission coefficient, tunneling correction, well-side damping morphology, and exceptional-point structure remain distinct native quantities. The Atlas does not manufacture canonical mechanical `chi` from a barrier frequency, nor does it infer a barrier-top `chi=1` boundary where the native inverted mode lacks one.

## 4. What v0.9 may be used for now

v0.9 may be used as:

- a frozen retrospective evidence map;
- a source/provenance map;
- a Function/Limit Map across environments and mechanism families;
- an independent read-only comparator where the tested System Model did not use the relevant Atlas target for tuning;
- a candidate-discovery resource for a future prospectively frozen v0.10 or separate extension.

It is **not**, by itself:

- untouched P1 confirmation of a rule learned from the same data;
- a predictive-tool certification;
- permission to tune an engine until it agrees;
- permission to collapse Grade C proxies into direct kinetics;
- permission to merge environments or families without the matching contract.

## 5. Successor policy

Any work that does one or more of the following creates a new version or explicitly separate extension rather than mutating v0.9:

- adds/removes a physical coordinate;
- changes an evidence grade or source lineage;
- changes an independence classification;
- adds a new mechanistic family or operational class definition;
- changes a reconstruction/proxy method;
- adds new prospective results;
- changes the Atlas schema, validators, or admission logic.

The frozen v0.9 workbook, source records, environment-depth table, independence backfill, validator outputs, refusals, and release reports remain untouched.

## 6. Recommended v0.10 work, if opened

A future v0.10 should begin from a new prospectively versioned protocol and should prioritize added information rather than round-number expansion. High-value targets include:

1. deeper direct/raw surface kinetics to reduce dependence on Grade C Arrhenius reconstructions;
2. direct molecular or mode-resolved solid-state kinetics where possible, rather than conductivity proxies alone;
3. independent cross-publication replication of families currently constrained by same-study dependence;
4. prospectively separated theory/experiment rows not used to learn the tested relation;
5. explicit friction/dissipation coordinates only where the native source genuinely reports or derives them;
6. retained refusals where public evidence cannot support the requested coordinate.

No requirement is imposed to reach a larger row count if the evidence is not available.

## 7. Migration result

`V0_9_FROZEN = true`

`MIGRATION_IN_PLACE_ALLOWED = false`

`GOM_V0_8_0_LOCAL_SAFEGUARDS_PRESERVED = true`

`ATLAS_WRITE_ACCESS_FROM_CONFIRMATORY_ENGINE = false`

`SCIENTIFIC_RESULTS_CHANGED_BY_THIS_AUDIT = false`

`NEXT_CHANGED_ATLAS_REQUIRES_NEW_VERSION = true`
