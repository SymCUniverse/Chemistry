# Chemistry GOM v0.8.0 Migration Integrity Checklist

Version: 0.1
Date: 14 September 2026
Status: PREPARED, NON-EXECUTING
Scope: governance migration only
Active compute touched: no

## Purpose

Implement the GOM v0.8.0 migration-integrity rule for `SymCUniverse/Chemistry`: project-specific safeguards may move out of the program-wide manual, but they may not disappear merely because the GOM has become more domain-neutral.

This checklist is not a scientific re-adjudication and does not modify the active H/Ru(0001) calculation, the ChemSA scientific core, Barrier Atlas contents, historical HOLDs, or frozen acceptance thresholds.

## Authority chain

1. Program authority: SymC General Operations Manual v0.8.0, Definitive Active Baseline, 14 September 2026.
2. Prepared Chemistry authority: `governance/CHEMISTRY_PROJECT_PROTOCOL_v0.2.md`.
3. Historical Chemistry protocol retained for lineage: `governance/CHEMISTRY_PROJECT_PROTOCOL_v0.1.md`.
4. Existing project change control remains binding: `governance/SCIENTIFIC_CHANGE_CONTROL_PROTOCOL_v1.1.json`.
5. Historical GP adoption mappings remain preserved for provenance and are not active program authority after GOM adoption.

## Migration-integrity audit

| Chemistry-specific safeguard | Local destination | Status |
| --- | --- | --- |
| Generator-first interpretation and finite-precision EP discipline | Project Protocol v0.2 Sections 2 and 14 | RETAINED |
| Stable-well `omega_0` versus barrier-top `omega_b` firewall | Project Protocol v0.2 Section 3 | RETAINED |
| Stable-well chi does not establish barrier crossing/rate/yield/selectivity | Project Protocol v0.2 Section 3 | RETAINED |
| Estimator-equivalence and width-convention safeguards | Project Protocol v0.2 Section 4 | RETAINED |
| Native-timescale Markov/memory test | Project Protocol v0.2 Section 5 | RETAINED |
| Engine/Barrier Atlas independence | Project Protocol v0.2 Section 6 | RETAINED |
| Literature condition matching and evidence-tier provenance | Project Protocol v0.2 Section 7 | RETAINED |
| Source/family/pathway independence | Project Protocol v0.2 Section 8 | RETAINED |
| Post-result representative-selection firewall | Project Protocol v0.2 Section 9 | RETAINED |
| Coequal Function Map and Limit Map | Project Protocol v0.2 Section 10 | RETAINED |
| Local versus embedded dynamics and no scalar averaging shortcut | Project Protocol v0.2 Section 11 | RETAINED |
| Active-run identity, checkpoint, stale-execution, and HOLD safeguards | Project Protocol v0.2 Section 12 | RETAINED |
| Separate R1/R2/R3 reproducibility claims | Project Protocol v0.2 Section 13 | RETAINED |
| Classification does not imply chemical prediction; native comparator discipline | Project Protocol v0.2 Section 14 | RETAINED |
| Historical HOLDs, failures, refusals, discrepancies, and immutable Atlas lineage | Project Protocol v0.2 Sections 6 and 15 | RETAINED |
| Governance migration cannot alter frozen scientific settings or active execution | Project Protocol v0.2 Sections 15 and 16 | RETAINED |

No project-specific safeguard reviewed above is intentionally retired by GOM v0.8.0 adoption.

## Change-control compatibility

The existing Chemistry change-control record uses a deliberately strict local mechanical-versus-scientific firewall. GOM v0.8.0 adds finer program-level distinctions. They are mapped without weakening the local rule:

- **Mechanical:** may be handled as local mechanical only when equations, acceptance logic, scientific settings, evidence meaning, and frozen interpretation are unchanged.
- **Science-adjacent:** requires an explicit equivalence check. If equivalence is not demonstrated, classify it under the local scientific path.
- **Scientific / science-breaking:** requires the applicable explicit authorization, versioning, and revalidation. A change that might be scientific is treated as scientific.

This mapping does not grant new authority to alter the active computation.

## Active-run firewall

At preparation time, the live H/Ru(0001) L21 contingency computation is on `personal-free-compute`; this GOM migration is isolated on `gom-v0.8.0-chemistry-adoption-prep`.

Until the active run reaches a valid terminal state or is explicitly dispositioned:

- do not merge governance changes into the active execution branch solely for GOM adoption;
- do not restart, duplicate, replace, or cancel the live computation as part of this migration;
- do not change scientific thresholds, numerical settings, checkpoint semantics, or acceptance logic;
- do not rewrite a pending scientific outcome as PASS, FAIL, HOLD, or robustness support before its evidence is complete.

## Adoption gate

Before GOM migration is promoted into an execution-bearing branch, confirm all of the following:

- active-run terminal/disposition state is known from the live repository;
- current branch/run/checkpoint identities have been re-read rather than inherited from a stale handoff;
- no frozen scientific rule changed;
- no project-specific safeguard disappeared;
- current project-state records are synchronized;
- stale or superseded workflows cannot consume expensive compute;
- capability descriptions are synchronized after adoption;
- this checklist and the prepared Project Protocol v0.2 remain documentation/governance changes only.

Disposition: `MIGRATION_PREPARED_NOT_YET_ADOPTED`.
