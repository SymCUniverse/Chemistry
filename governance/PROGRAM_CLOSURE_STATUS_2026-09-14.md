# Chemistry Program Closure Status — 14 September 2026

**Program authority:** SymC General Operations Manual v0.8.0  
**Branch:** `personal-free-compute`  
**Purpose:** one current checkpoint for what is scientifically closed, what is implementation-ready, what is actively running, and what remains genuinely evidence-gated.

## Top-line state

Chemistry is no longer waiting on broad architecture or governance work. The principal H/Ru(0001) clean-surface numerical gate has passed on a fresh versioned successor, the complete clean-surface relaxation/reproduction route is implemented and mechanically prequalified, the substrate/adsorption downstream structures are prepared, the living manuscript is in the repository and compiling, and the GOM v0.8.0 migration is explicit.

The remaining immediate H/Ru scientific hinge is narrow: the prospectively frozen **L21 layer-depth robustness challenge**. Its outcome determines whether L17 is inherited into production relaxation. No other currently identified non-compute preparation must be invented after that result arrives.

## H/Ru(0001)

### Closed / banked

- PBE bulk candidate: PASS.
- Historical L15/L17/L19 layer extension: PASS with L17 selected under that version's rule.
- Original L17/V15/K16 coupled gate: HOLD on k-mesh, permanently preserved.
- Post-HOLD K20/K24/K28 diagnostic: completed as P0-Q Function/Limit evidence; K24 nominated by the predeclared successor rule.
- Fresh L17/V15/K24 four-case successor qualification: `CLEAN_SURFACE_FIXED_GRID_PASS`.
- Fresh endpoint deltas under unchanged 1 meV/surface-atom criterion:
  - L17 to L19: 0.164765 meV;
  - K24 to K28: 0.307761 meV;
  - V15 to V25: 0.002041 meV.
- Fixed-grid PASS evidence committed with run/artifact provenance.
- Deterministic L17/L19/L21 robustness adjudicator qualified on known-good, known-bad, and invalid-input tests.
- Clean-surface relaxation implementation self-test: PASS.
- BFGS fresh-runner native checkpoint handoff qualification: QUALIFIED, mechanical/non-evidentiary only.
- Production relaxation/reproduction workflow: WIRED, manual-only, fail-closed on committed `ROBUSTNESS_SUPPORTED` plus the BFGS qualification.
- Substrate-inheritance contract updated; certificate template prepared but not issued.
- Adsorption-screen evidence architecture prepared but not frozen for execution.
- Reproducibility preflight updated through the fresh fixed-grid PASS.
- Manuscript integration record updated through the fresh fixed-grid PASS and active robustness hold.

### Actively running

- L21/V15/K24 foundational layer-depth challenge, GitHub run `34798425393`, segment 3 in progress at this status snapshot.
- QE 7.6 / i-PI 3.3.0 non-evidentiary socket smoke test, run `34845931092`, environment prequalification only.

### Held by evidence

- Production clean-surface relaxation: held only by the unresolved L21 foundational interlock.
- H/Ru substrate certificate: requires `ROBUSTNESS_SUPPORTED` plus `CLEAN_SURFACE_RELAX_PASS` with independent reproduction.
- Adsorption execution: requires an issued substrate certificate and a separately frozen execution protocol with justified H reference/lateral-cell/reciprocal-resolution/electrostatic choices.
- Path/barrier/rate work: downstream of adsorption and its own gates.
- Quantitative H-adatom diffusion friction: not established.
- H/Ru mechanical chi: not licensed.
- Production PIMD: not authorized.

## H/Ru external validation and opportunity map

Existing literature substantially covers several validation experiments that the project otherwise might need to perform:

- clean Ru(0001) interlayer relaxation: LEED-IV / surface X-ray diffraction;
- H/D adsorbate vibrational structure and lateral coupling: high-resolution HREELS;
- atomic H diffusion from 75–250 K: HeSE with tunneling plateau and fcc/hcp information;
- process-specific H/Ru electronic friction: H2 dissociation/scattering and associative desorption.

The strongest unresolved experimental opportunity identified is a **quantitative dissipative object matched to the same adsorbed-H diffusion coordinate**, ideally with memory sensitivity and a matched D diffusion experiment.

## Dissipation state

Current literature conclusion:

- quantitative projected H-adatom fcc↔hcp diffusion friction: **NOT ESTABLISHED**;
- qualitative low-friction signature from HeSE multiple jumps: **SUPPORTED**;
- H2/Ru electronic-friction studies: physically relevant but wrong coordinate for numerical transplantation;
- Ru(0001) tensorial-friction methodology: computationally plausible from other adsorbates, not substitute evidence.

The preferred closure path is to compute the native H/Ru PES/path first, then a matched tensor/kernel, project it onto the validated coordinate, test memory/Markovian reduction where material, and compare only afterward with independent HeSE behavior.

## Quantum-nuclear environment

A current-version correction has been made:

- QE candidate: 7.6, frozen tag commit `9f93ddec427d2b9a45bb72d828c6d324f62fcabd`;
- i-PI candidate: **3.3.0**, commit `bf64b65ef2711638a5c9fad1fbd5dffc73b7c008`;
- i-PI 3.2.0 is superseded as the previously stated latest version.

A non-evidentiary QE `--ipi` socket smoke test has been opened. Even a successful smoke test does not authorize H/Ru PIMD; multi-client topology, restart semantics, force repeatability, resources, and scientific bead/method convergence remain separate gates.

## CO/Cu(111)

- GOM v0.8.0 migration audit: complete.
- L15/L17 and L19 zero-paid resumable routes: WIRED.
- Live external Kaggle execution: NOT VERIFIED from repository evidence.
- Historical HOLDs: preserved.
- Reconciliation routes for consistent, conflicting, incomplete, and failed future evidence: prospectively recorded.
- Substrate certificate: NOT_YET_ISSUED.

No H/Ru or Atlas result may select or rescue CO/Cu numerical settings.

## Barrier-Height/Rate Atlas

v0.9 remains a frozen retrospective independent evidence product:

- 61 physical coordinates;
- 26 families;
- 18/18 operational classes;
- 67 sources;
- 11 Grade A / 30 Grade B / 20 Grade C;
- 80 replicates;
- 27 held/refused candidates.

The GOM migration audit preserves its evidence grades, refusals, independence ceilings, source relations, Function/Limit Map, and read-only relationship to confirmatory engines. v0.9 is not mutated in place.

A v0.10 prospectus exists, but `V0_10_RELEASE_OPEN = false`. Opening a changed Atlas requires a separately frozen successor protocol.

## Living manuscript

Canonical working entry point:

`manuscript/working/CHEMSA_LIVING_MAIN.tex`

The manuscript workspace:

- is explicitly WORKING / NOT RELEASE / NOT SUBMISSION-READY;
- is bound to the user-supplied seed `ChemSA_Combined_Main (9).tex`, SHA-256 `2e44a44b52872f471a202486c155eb86465b8545c2c7f2184b1cd1fffb17fc61`;
- has the complete seed text modularized through the bibliography;
- preserves a separate H/Ru evidence-to-prose staging note;
- compiles successfully under GitHub Actions, run `34845313047`;
- uses an explicit nonpublication placeholder for `linewidth_hierarchy.png` until the real generated figure is staged.

This is now the canonical place to edit the evolving Chemistry manuscript. A release/submission candidate requires a separate explicit freeze and clean-room synchronization.

## Governance/documentation

Completed:

- GOM v0.8.0 adoption and hash binding;
- Chemistry-local safeguard migration;
- living-document/current-state audit;
- capability-description index;
- native-method/comparator map;
- active-dependency monitor-coverage audit;
- current implementation registry v1.3;
- synchronized root README.

Known administrative mismatch retained transparently: the external GitHub repository description still uses an obsolete broad single-ratio/near-critical-optimum description. The current connector cannot administer that repository metadata, so the mismatch is recorded rather than falsely claimed fixed.

## Exact next routing

### If L21 returns `ROBUSTNESS_SUPPORTED`

1. bank the final L21 evidence and deterministic robustness adjudication;
2. commit `SYSTEM3_L17_FOUNDATIONAL_ROBUSTNESS_RESULT_v0.1.json`;
3. dispatch the already-wired production clean-surface relaxation/reproduction workflow;
4. if `CLEAN_SURFACE_RELAX_PASS`, assemble and issue the exact-scope substrate certificate;
5. freeze the adsorption execution protocol before any adsorption result is inspected.

### If L21 returns `FOUNDATION_REOPENED`

- do not dispatch L17 relaxation;
- preserve the fresh fixed-grid PASS as the true result of its minimum gate;
- reopen only the layer-depth foundation;
- use L19/L21 behavior to design the next version without threshold retuning.

### If L21 is invalid/mechanically incomplete

- keep the foundational hold;
- repair only the bounded challenge's mechanics/provenance;
- do not change the 1 meV scientific criterion.

## Bottom line

All identified work that can be advanced without the unresolved L21 scientific result has either been completed, prepared, or opened as an independent non-evidentiary qualification. The H/Ru clean-surface program is therefore no longer blocked by missing governance, missing manuscript tracking, missing relaxation code, missing restart qualification, or missing downstream protocol architecture. It is waiting on an actual scientific result rather than unfinished scaffolding.
