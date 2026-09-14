# Chemistry GOM v0.8.0 Migration Audit v0.1

**Date:** 14 September 2026  
**Status:** ACTIVE MIGRATION AUDIT  
**Current program authority:** SymC General Operations Manual v0.8.0, Definitive Active Baseline  
**Comparison baseline:** General Cross-Project Research Protocol v0.7.7 as the last program version explicitly loaded in this Chemistry thread before v0.8.0 review

## 1. Audit conclusion

The v0.8.0 transition changes governance organization and local-responsibility boundaries more than it changes Chemistry science. No current Chemistry numerical threshold, physical model, evidence grade, prior HOLD, or P0-Q/P1 distinction is weakened by the migration.

The material repository defect found by this audit was a stale program-authority pointer: `CHEMISTRY_GENERAL_PROTOCOL_v0.7.1A_ADOPTION_v0.1.json` remained the only explicit Chemistry adoption artifact even though later program baselines had superseded it. That file is retained as historical lineage. Current prospective authority is now recorded in `CHEMISTRY_GOM_v0.8.0_ADOPTION_AND_MIGRATION_v0.1.json`.

The second material issue was migration integrity. v0.8.0 deliberately removes project-specific equations, named examples, thresholds, and implementation detail from the program manual. Chemistry-specific safeguards therefore cannot be left implicit. Their active local destination is now `CHEMISTRY_PROJECT_GUARDRAILS_v0.1.md`, supplemented by existing frozen system and Atlas records.

## 2. Verbatim-semantic change classes relevant to Chemistry

### v0.7.7 controls retained

The following controls remain active without intentional weakening:

- truth over continuity;
- MFR-14 confirmatory floor;
- native-model-first construction;
- explicit chi/omega/gamma semantics;
- degeneracy versus exceptional-point firewall;
- P0-D / P0-Q / P1 / P2 separation;
- promotion debt;
- refusal capability;
- preservation of failures and residuals;
- source-of-record verification rather than AI recall;
- semantic validation in addition to hashes;
- System Model / Engine / Atlas / Tool separation;
- Function Map and Limit Map;
- relational stability and hierarchical closure;
- foundational dependency and bounded robustness;
- active-run monitoring/recovery/circuit breaking;
- new-chat protocol bootstrap;
- reader-first communication.

### v0.7.8 consolidation affecting Chemistry

v0.7.8 moved project-specific architecture and examples out of the program-level document and retained domain-neutral safeguards. Chemistry must therefore keep local rules for barrier kinetics, Atlas semantics, DFT convergence, substrate inheritance, dissipation coordinates, quantum execution readiness, and project-specific claim ceilings.

It also reduced prescriptive operational schemas to the minimum needed for auditability. Chemistry may remain stricter where its long DFT runs, checkpoint sizes, evidence independence, or publication requirements justify stricter local controls.

### v0.8.0 additions affecting Chemistry

1. The program document is now the **SymC General Operations Manual (GOM)**. Historical GP references remain aliases only when history is being discussed.
2. Numbered program releases become authoritative only by explicit user promotion. Review candidates do not silently become active baselines.
3. **Migration integrity is explicit:** a safeguard removed from the GOM is not safely relocated until a project-local destination is identified or created.
4. `NO_NATIVE_COMPARATOR` is clarified as a good-faith exclusion result, not an obligation to run irrelevant methods.
5. Program-level interpretive safeguards are consolidated; Chemistry-specific implementations remain local.

## 3. Chemistry-specific safeguard destinations

| Safeguard | Local destination | Audit status |
|---|---|---|
| P0-D/P0-Q/P1/P2 Chemistry mapping and historical HOLD preservation | historical v0.7.1A adoption + current project guardrails | PRESERVED |
| Barrier-top `omega_b` versus restoring `omega_0` distinction | `CHEMISTRY_PROJECT_GUARDRAILS_v0.1.md` | PRESERVED |
| No canonical barrier-saddle `chi=1`/EP by notation alone | `CHEMISTRY_PROJECT_GUARDRAILS_v0.1.md` | PRESERVED |
| DFT settings selected by native convergence, never chi/rate agreement | project guardrails + frozen H/Ru protocols | PRESERVED |
| Barrier Height/Rate Atlas v0.9 immutable/read-only evidence role | project guardrails + frozen v0.9 release | PRESERVED |
| Dissipation coordinate must be independently established | project guardrails + H/Ru dissipation audit | PRESERVED |
| QE+i-PI/PIMD readiness does not equal production qualification | project guardrails + quantum-readiness audit | PRESERVED |
| Substrate inheritance requires separate earned certification | project guardrails + substrate-inheritance contract | PRESERVED |
| Foundational robustness before heavy downstream inheritance | H/Ru L17 robustness hold record | ACTIVE |

## 4. Current H/Ru consequence

The fresh successor fixed-grid qualification has now passed at L17/V15/K24 under the unchanged 1 meV/surface-atom criterion. The original K16 coupled HOLD remains preserved. The fresh endpoint deltas are:

- L17 to L19: 0.164764944 meV/surface atom;
- K24 to K28: 0.307760780 meV/surface atom;
- V15 to V25: 0.002040852 meV/surface atom.

The original successor adjudicator therefore correctly records `CLEAN_SURFACE_FIXED_GRID_PASS` and `relaxation_authorized=true` for the minimum gate it was written to judge.

A stronger user-authorized GOM Section 11.3 robustness dependency is also active. It is a separate governance layer and does not rewrite the PASS. Because substantial downstream H/Ru work will inherit the slab, operational progression into relaxation is held until the already-running fresh L21/V15/K24 challenge resolves both prospectively frozen checks:

- `abs(gamma_L21 - gamma_L17) <= 0.001 eV/surface atom`; and
- `abs(gamma_L21 - gamma_L19) <= 0.001 eV/surface atom`.

If both survive, robustness is supported and the layer-depth ladder stops unless a new scientific reason appears. If either fails, the foundation is reopened without erasing the minimum-gate PASS or historical K16 HOLD.

## 5. Non-compute migration closures

Completed by this audit:

- current GOM v0.8.0 adoption/migration record created;
- historical v0.7.1A adoption preserved rather than overwritten;
- project-local Chemistry guardrails created;
- H/Ru L17 foundational robustness hold frozen before the L21 result;
- current-state registries identified as stale and scheduled for successor records;
- monitor/recovery coverage identified as a separate audit surface rather than inferred from workflow existence.

Still appropriate without waiting for current scientific computations:

- issue an updated implementation-status registry and H/Ru state ledger;
- audit active-dependency monitoring and recovery coverage;
- audit manuscript/reproducibility prose for stale protocol names, stale H/Ru status, or capabilities that changed;
- preflight the exact post-robustness relaxation/reproduction route without starting relaxation;
- preflight the substrate-inheritance certificate requirements without issuing the certificate;
- audit CO/Cu current evidence/run readiness against GOM v0.8.0 while preserving its historical HOLDs;
- audit Barrier Atlas v0.9 migration integrity and define any v0.10 work as a separate successor rather than mutating v0.9;
- continue literature-only dissipation/friction and experimental-opportunity work where new evidence can be added without contaminating frozen computation.

## 6. No-change declaration

This migration audit changes no frozen Chemistry scientific setting, numerical threshold, evidence grade, Atlas coordinate, historical failure, or claim status by itself. It changes governance pointers, makes local safeguards explicit, and synchronizes project control with the authoritative GOM.
