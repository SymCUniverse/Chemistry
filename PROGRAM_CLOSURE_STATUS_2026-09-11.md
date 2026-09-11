# Chemistry program closure status

**Snapshot:** 2026-09-11 America/Chicago  
**Branch:** `personal-free-compute`  
**Supersedes for current state:** `PROGRAM_CLOSURE_STATUS_2026-09-04.md`  
**Historical snapshots remain preserved.**

## Program-level governance

General Protocol v0.7.1 plus the v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum is now mapped explicitly into chemistry governance by `governance/CHEMISTRY_GENERAL_PROTOCOL_v0.7.1A_ADOPTION_v0.1.json`.

Current numerical-development work is classified as P0-Q qualification where appropriate. Qualification evidence may inform versioned successor System Models or Engine components, but a prior frozen failure remains a historical failure and qualification-informed evidence is not represented as untouched P1 confirmation.

The program uses both Function Maps and Limit Maps. Claim-specific closure does not require an infinite computational ladder; additional calculations may continue as robustness or mapping evidence and can reopen interpretation if they reveal a material contradiction.

## System 3: H/Ru(0001)

**Current status:** `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD / P0-Q KMESH DIAGNOSTIC ACTIVE`

The deeper odd-layer extension completed and passed its frozen suffix rule:

- L15 = 1.092107489992486 eV/surface atom
- L17 = 1.091078831559571 eV/surface atom
- L19 = 1.090771478953684 eV/surface atom
- |L17-L19| = 0.0003073526058869902 eV/surface atom
- selected non-terminal layer = L17

The lineage-preserving coupled recheck required before relaxation then completed in run `34535678952` and returned `CLEAN_SURFACE_COUPLED_CONVERGENCE_HOLD`:

- K16 to K20 delta = 0.0024786851754470263 eV/surface atom: FAIL
- V15 to V25 delta = 0.0000029932525649201125 eV/surface atom: PASS
- L17 to L19 delta = 0.0003073526058869902 eV/surface atom: PASS
- frozen tolerance = 0.001 eV/surface atom

The failed axis is therefore specifically surface k-mesh. Relaxation remains unauthorized.

A separately frozen P0-Q K20/K24/K28 diagnostic is active in workflow run `34560002560`. It preserves the original K16 coupled HOLD, does not retune the 1 meV criterion, and cannot itself emit `CLEAN_SURFACE_FIXED_GRID_PASS`.

## H/Ru pre-reconciliation work now closed

The following work no longer waits on K24/K28:

- current state ledger and evidence lineage;
- General Protocol v0.7.1A phase/function-limit mapping;
- manuscript integration through the coupled HOLD;
- reproducibility package preflight and evidence-role inventory;
- append-only governance decisions for P0-Q successor logic and claim-specific closure;
- initial public H/Ru dissipation/coordinate-matching literature audit;
- quantum QE/i-PI architecture readiness audit;
- preservation of historical numerical HOLDs;
- explicit separation of repository readiness from verified live Kaggle execution.

The consolidated record is `systems/h_ru0001/SYSTEM3_PRE_RECONCILIATION_CLOSEOUT_v0.1.md`.

## H/Ru dissipation boundary

Current state: `DISSIPATION_NOT_ESTABLISHED`.

The initial public-source audit found no qualified independent coordinate-matched projected friction for lateral atomic-H diffusion on Ru(0001). HeSE dephasing is not automatically reaction-coordinate friction. A later explicit H/Ru friction parameter identified in theory is fitted against H/Ru hopping-rate data and therefore is not independent validation evidence. H2/Ru electronic-friction work involves different coordinates/state points.

This limits claims requiring `DISSIPATION_READY` or ChemSA eligibility. It does not invalidate upstream surface, adsorption, reaction-path, classical, or quantum work.

## H/Ru quantum implementation boundary

Quantum ESPRESSO plus i-PI remains a supported planned architecture for the nuclear-quantum tier. Production is not yet authorized. Exact software versions, interface convention, socket operation, bead/client topology, restart behavior, and memory/runtime scaling must be qualified in a non-admissible pilot before evidentiary PIMD.

## System 2: CO/Cu(111)

**Repository status:** READY for the authorized checkpointed Kaggle continuation routes.

The audited launchers remain:

- L15/L17: `systems/co_cu111/kaggle/FRESH_SESSION_BOOTSTRAP_v1.sh`
- L19: `systems/co_cu111/kaggle/FRESH_SESSION_L19_v1.sh`

GitHub repository readiness does not establish that either Kaggle session is currently executing. No live Kaggle status is claimed here.

Historical CO/Cu numerical HOLDs remain preserved and may inform P0-Q successor qualification without being rewritten.

## Barrier Height/Rate Atlas v0.9

Atlas v0.9 remains frozen as a reproducible retrospective independent evidence product. It is not rewritten by System 2 or System 3 calculations and its current publication/archival closure does not depend on resolving H/Ru or CO/Cu surface computation.

Protocol-compatibility improvements belong to a versioned future Atlas release rather than silent mutation of v0.9.

## Remaining critical path

For the current H/Ru clean-surface problem, the only immediate scientific dependency is the K20/K24/K28 diagnostic and what it shows about the dense-k operating region. If a usable region is established, a versioned successor fixed-grid qualification must be frozen, executed, and independently coupled-rechecked before relaxation. If no usable region is established, the diagnostic result is preserved and the next bounded P0-Q map is designed without relaxing the threshold.

Everything else listed in the pre-reconciliation closeout has been removed from the current waiting backlog.
