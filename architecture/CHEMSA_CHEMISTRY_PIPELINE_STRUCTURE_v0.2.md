# ChemSA Chemistry Pipeline Structure v0.2

**Status:** current architecture  
**Effective date:** 2026-09-11  
**Supersedes for current architecture:** `CHEMSA_CHEMISTRY_PIPELINE_STRUCTURE_v0.1.md`  
**Historical v0.1 remains preserved.**

## 1. Governing architecture

The chemistry program uses the General Protocol distinction:

**System Model -> implemented by Engine**

A **System Model** is the scientific representation: state variables, equations, physical assumptions, reduction rules, admissible observables, boundary conditions, and claim limits for the system under study.

An **Engine** is the tested computational implementation of that System Model or one of its components. Engine success does not by itself establish physical validity, and a physical HOLD is not a software defect merely because the Engine executed correctly.

A separate **Independent Atlas** stores evidence and provenance. The System Model and Engine may read qualified Atlas evidence under explicit rules, but they may not rewrite or retune the Atlas to improve agreement.

For chemistry:

- **System Model + Engine** gives a reproducible computational representation.
- **System Model + Independent Atlas** may support a Tool when the relationship is scientifically licensed.
- **Validated System Model + Independent Atlas + prospective validation** is required before calling the result a Predictive Tool.

The present program is not assumed to have reached Predictive Tool status.

## 2. Phase discipline

### P0-D: discovery and mapping

Used to explore response landscapes, numerical behavior, candidate coordinates, mechanism structure, failure modes, and possible representations. Previously observed results may inform exploration. P0-D evidence is not presented as untouched confirmation.

### P0-Q: controlled qualification

Used to test and improve candidate System Models and Engines. Qualification failures may inform a versioned successor model or implementation, provided:

- the original failure remains preserved;
- the reason for the successor change is explicit;
- frozen thresholds are not loosened merely to obtain PASS;
- reused qualification evidence is not later represented as untouched P1 confirmation;
- evidence firewalls remain explicit.

The current H/Ru(0001) dense-k investigation and current CO/Cu(111) continuation are P0-Q activities.

### P1: confirmatory claim testing

A P1 claim requires claim-specific frozen assumptions, acceptance rules, relevant MFR-14 controls, and evidence not used to learn the rule being tested. Independence is assessed pathway by pathway rather than as one binary label.

### P2: prospective external validation

Reserved for genuinely prospective testing of a validated representation or prediction on evidence not used to develop or qualify the tested rule.

## 3. Computational Reaction-Path System Model and Engine

**Scientific job:** establish the static, structural, harmonic, and pathway quantities licensed by the chosen electronic-structure representation.

Typical outputs include:

- qualified substrate geometry and numerical settings;
- adsorbate geometries and adsorption-site ordering;
- minimum-energy paths;
- saddle geometry and barrier height;
- Hessian, force-grid, or mode information;
- harmonic or separately qualified approximate prefactors;
- conventional rate-model inputs where physically licensed.

The Engine does not infer a damping coefficient from a Hessian and does not assign a ChemSA stability class merely because an oscillatory frequency or barrier exists.

A numerical surface qualification HOLD is preserved as a limit of that version of the System Model. P0-Q may build a successor version from the observed qualification evidence without rewriting the earlier HOLD.

## 4. Reaction-Coordinate Consistency Validator

**Scientific job:** determine whether proposed quantities refer to the same physical coordinate and compatible state conditions.

Checks include, where applicable:

- adsorbate/substrate identity and surface state;
- translational, rotational, internal, collective, or reaction-coordinate identity;
- projection of well modes onto the barrier-crossing coordinate;
- whether damping evidence addresses the same coordinate rather than an orthogonal process;
- temperature, coverage, pressure, solvent, charge state, structural phase, and preparation compatibility;
- coordinate conventions for local frequency, barrier, and saddle quantities;
- explicit reproducibility of any multidimensional-to-reduced projection.

Possible outcomes include `PASS`, typed HOLDs, `INDETERMINATE`, `UNRESOLVED`, `NOT_APPLICABLE`, or `REFUSED` where the evidence cannot support the requested mapping.

The validator does not decide source independence or provenance adequacy. That is a separate pathway.

## 5. Dissipation Provenance and Independence Validator

**Scientific job:** determine what a proposed damping/dissipation quantity physically represents, whether it maps to the validated coordinate, and whether its evidentiary pathway is independent enough for the claim being made.

Objects that must remain distinguishable include:

- population lifetime T1;
- homogeneous dephasing T2 or decomposed linewidth;
- pure dephasing;
- inhomogeneous broadening;
- phonon coupling;
- electronic friction;
- projected friction-tensor components;
- generalized-Langevin memory kernels;
- rate-fitted Langevin friction;
- model-resolved coupling parameters.

Independence is recorded separately for relevant pathways such as data, outcome, tuning, method, Atlas, literature/source, system/cohort, and temporal independence.

A fitted diffusion friction cannot be used as independent validation of the same diffusion-rate data used to fit it. HeSE dephasing is not automatically reaction-coordinate friction. A friction tensor calculated for a different reaction coordinate is not silently projected onto the target coordinate.

A legitimate result may be `DISSIPATION_NOT_ESTABLISHED`. That limits dissipation-dependent claims without invalidating upstream chemistry.

## 6. ChemSA stability representation

A ChemSA classifier operates only on a dynamical object whose physical semantics are already licensed.

It may receive, for example:

- a validated quadratic pencil;
- a first-order generator;
- a licensed reduced second-order mode;
- another explicitly derived generator representation.

Any scalar chi is a compressed coordinate, not the whole stability architecture. Modal/vector structure and conglomerate/system organization provide additional views, and those views are themselves not assumed to exhaust the higher-order stability architecture.

The classifier may not:

- invent missing dissipation;
- treat unrelated observables as equivalent;
- use kinetic agreement to repair an upstream HOLD;
- treat chi = 1 as a universal physical boundary without a domain-specific semantic derivation;
- infer a common mechanism from scalar similarity alone.

## 7. Independent Barrier-Height/Rate Atlas

The Barrier-Height/Rate Atlas is an evidence system, not an Engine output cache and not a tuning surface for the System Model.

Barrier Atlas v0.9 remains a frozen, reproducible retrospective parent. Future releases are versioned extensions and protocol-compatibility upgrades rather than silent edits to v0.9.

Atlas records may contain valid chemistry even when ChemSA classification is unavailable. A first-principles barrier with no admissible dissipation can remain a useful barrier/rate coordinate while carrying `dissipation_tier = NONE` and `chemsa_eligibility = false`.

Future Atlas releases should distinguish evidence quality from independence and should retain blocked, disputed, superseded, excluded, provisional, verified, and locked states rather than forcing all rows into one success scale.

## 8. Function Map and Limit Map

Every major chemistry component should preferentially retain both:

**Function Map:** how the representation behaves where it is adequate.

**Limit Map:** where it degrades, changes regime, becomes non-identifiable, violates a convergence criterion, or refuses a scalar/reduced description.

Examples include:

- layer-depth, vacuum, and k-mesh convergence trajectories;
- adsorption-site energy landscapes;
- barrier/path sensitivity surfaces;
- bead-convergence trajectories;
- friction-regime maps;
- regions where coordinate matching or scalar reduction is not licensed.

A HOLD is therefore not merely an obstacle to a PASS. It may be a scientifically useful boundary in the Limit Map.

## 9. Claim-specific closure

A system does not need every conceivable calculation to finish every narrower claim.

For each reported claim, identify the exact upstream gates logically required for that claim. When those gates are satisfied or the claim is honestly bounded by a preserved HOLD, that component may be closed at the corresponding claim ceiling.

Additional deeper, denser, longer, or broader computation may continue as robustness, Function Map, or Limit Map evidence. It is not silently made a prerequisite after the fact. If additional evidence materially contradicts an earlier interpretation, the contradiction is preserved and the interpretation is reopened.

## 10. Default scientific route

The default route is:

`source / experiment / first-principles calculation`

-> **System-specific scientific representation**

-> **Computational Reaction-Path Engine qualification**

-> **Reaction-Coordinate Consistency Validation**

-> **Dissipation Provenance and Independence Validation**

-> **licensed scalar/modal/system stability representation, if available**

-> **Independent Atlas admission and cross-system analysis under explicit read-only rules**

A system may stop at any layer. The stop must be typed scientifically rather than hidden as missing data or mislabeled as software failure.

## 11. Current system roles

- **System 1: Na/Cu(001):** development pilot and regression anchor for the reaction-path Engine and audit machinery.
- **System 2: CO/Cu(111):** independently selected chemistry target currently undergoing P0-Q qualification/continuation. Historical failures remain failures even if a successor model later qualifies.
- **System 3: H/Ru(0001):** difficult-limit contrast target currently in P0-Q clean-surface qualification. Its role includes exposing where the numerical and physical representation works and where it refuses promotion.

Neither System 2 nor System 3 is described as untouched P1 confirmation merely because it was selected prospectively before some calculations. Evidence used during qualification is labelled accordingly.

## 12. Non-substitution rule

No layer silently performs another layer's job.

- A Hessian is not a damping matrix.
- A linewidth is not automatically reaction-coordinate friction.
- A fitted rate parameter is not independent validation of the same rate.
- A rate-derived activation energy is not automatically an independent barrier.
- A numerical convergence PASS is not a kinetic validation.
- A ChemSA classification cannot promote weak provenance.
- Atlas admission cannot repair a failed physical-consistency gate.
- Relaxation cannot rescue an unconverged fixed-grid representation.

## 13. Refactor and release rule

Do not physically relocate working legacy paths while active workflows or reproducibility records depend on them. Generic reusable code may be extracted only with regression tests demonstrating preservation of the historical output and with explicit version lineage.

Scientific model changes, mechanical implementation repairs, evidence-record changes, and documentation-only changes remain separately typed so that a green CI status cannot be mistaken for a scientific PASS.
