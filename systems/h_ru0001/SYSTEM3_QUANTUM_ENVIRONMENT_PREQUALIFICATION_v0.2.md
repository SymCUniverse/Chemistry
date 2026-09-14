# System 3 H/Ru(0001) Quantum Environment Prequalification v0.2

**Date:** 14 September 2026  
**Status:** `CANDIDATE_VERSION_PAIR_IDENTIFIED_SMOKE_TEST_STILL_REQUIRED`  
**Phase:** P0-Q implementation/readiness  
**Supersedes for current environment-planning state:** `SYSTEM3_QUANTUM_IMPLEMENTATION_READINESS_AUDIT_v0.1.md`  
**Production PIMD authorized:** **NO**

## 1. Current upstream software state checked

### Quantum ESPRESSO

The Quantum ESPRESSO Foundation release page currently lists **Quantum ESPRESSO v7.6** as the latest release, released approximately July 2026. QE 7.5 is now marked as a historical release.

The public PWscf documentation continues to document:

- `max_seconds` as the supported way to stop long jobs for later restart;
- `restart_mode` as the intended companion for split jobs;
- `forc_conv_thr` and `etot_conv_thr` for ionic minimization;
- `disk_io` controls;
- a direct i-PI socket interface in the PWscf user guide.

The current public NEB input documentation identifies itself as QE **7.5**, which demonstrates that documentation pages may lag the newest release label. Therefore version labels in web documentation are not sufficient to qualify the exact production binary.

### i-PI

The official i-PI GitHub release page currently lists **v3.2.0** as the latest release. Current documentation lists Quantum ESPRESSO as an out-of-the-box client and documents the client-server architecture in which i-PI propagates nuclear coordinates and an external electronic-structure code supplies energies/forces/virials.

Current i-PI documentation also includes newer transport options such as shared-memory and MPI communication in addition to conventional UNIX/INET sockets. These are implementation options, not scientific reasons to alter the planned nuclear-quantum method.

## 2. Candidate production-version pair

For a new qualification performed today, the default candidate pair is:

- **Quantum ESPRESSO 7.6**, exact source/binary hash to be frozen after build or retrieval;
- **i-PI 3.2.0**, exact release/commit and Python environment lock to be frozen.

This is a candidate pair, not an authorized production environment.

The already-used frozen QE executable elsewhere in the Chemistry repository remains the authority for the current classical surface lane. This prequalification does **not** silently replace that binary or recompute current surface evidence with QE 7.6.

## 3. Interface ambiguity that still requires an empirical smoke test

Current documentation exposes two descriptions of the QE/i-PI connection:

1. the QE PWscf user guide documents launching PWscf with `pw.x --ipi <address>:<port>` (or a UNIX-socket equivalent) while the PW input is essentially a single-point SCF setup;
2. i-PI documentation shows a Quantum Espresso input-side convention using `calculation='driver'` and `srvaddress=...`.

These descriptions establish architectural support but do not prove that both syntaxes are interchangeable for the chosen QE 7.6/i-PI 3.2.0 pair.

**Required resolution:** build/install the exact pair and run a non-evidentiary socket smoke test. Freeze the syntax that actually works for those exact versions. Do not choose by documentation preference.

## 4. Pre-production qualification ladder

### QENV-1: immutable environment identity

Freeze:

- QE 7.6 source tag/commit;
- compiled `pw.x` SHA-256;
- compiler and linked-library versions;
- i-PI 3.2.0 package/commit identity;
- Python version and locked dependency set;
- pseudopotential identities inherited from the qualified System-3 electronic-structure lane where scientifically applicable.

### QENV-2: communication smoke test

Use a deliberately non-evidentiary toy/small system to prove:

- i-PI server starts;
- one QE client connects with the selected UNIX/INET syntax;
- cell and positions are received correctly;
- QE returns energy, forces, and virial/stress in the expected units/convention;
- controlled disconnect/restart is understood;
- logs contain enough information to diagnose a failed handshake.

No H/Ru rate agreement is inspected during this step.

### QENV-3: replica/client topology test

For representative bead counts, verify:

- number of clients and ranks per bead;
- whether clients are persistent or relaunched;
- memory per client;
- filesystem pressure and wavefunction reuse policy;
- socket/shared-memory/MPI transport only as an execution optimization after functional correctness is established.

### QENV-4: restart/reproducibility test

Demonstrate that an interrupted path-integral run can be restarted without silently changing:

- bead positions/momenta;
- thermostat/barostat state where applicable;
- random-number state where deterministic continuation is claimed;
- force-client electronic settings;
- temperature and bead count;
- estimator definitions.

Restart agreement must be defined in terms appropriate to stochastic/thermostatted sampling, not byte-identical trajectories where chaos/stochasticity makes that meaningless.

### QENV-5: electronic-force consistency

Before ab initio bead convergence is interpreted, establish that individual QE force calls at a small set of fixed bead geometries reproduce under fresh clients to the frozen electronic tolerance.

### QENV-6: resource pilot

Measure wall time, RAM, artifact/checkpoint volume, and client-launch overhead at a small bead count. The pilot decides feasibility and execution architecture, not scientific bead convergence.

## 5. Scientific nuclear-quantum rules retained from the earlier protocol

This environment update changes **none** of the previously frozen scientific rules:

- full H/Ru rate validation retains a nuclear-quantum tier;
- prospective bead ladder remains **16 / 32 / 64** unless a separately justified amendment is frozen before decisive bead evidence;
- bead convergence remains a free-energy-barrier change of **<= 0.005 eV** on doubling the bead count;
- rate agreement may not select bead count;
- reaction coordinate is derived from the newly computed adjacent-site MEP, not imported from the published H/Ru labels;
- a nonrepresentative centroid coordinate produces `QUANTUM_REACTION_COORDINATE_HOLD` rather than an after-the-fact method switch;
- published HeSE rate agreement is validation evidence only after the computational method/path/convergence choices are frozen.

## 6. Method choice after environment qualification

The 2013 H/Ru literature used ab initio PIMD-based quantum transition-state theory and an instanton comparison, demonstrating that such methods are physically relevant to this exact system. That prior use does not force the present implementation to reproduce every historical algorithmic detail, but any alternative must answer the same frozen question and carry its own convergence/error analysis.

A future choice among PIMD-QTST, ring-polymer instanton, RPMD-based rate theory, or another quantum-rate method should be made from native method suitability to the temperature/barrier regime, not from which method happens to agree best with the HeSE curve.

## 7. Current closure state

`QE_LATEST_RELEASE_IDENTIFIED = 7.6`

`IPI_LATEST_RELEASE_IDENTIFIED = 3.2.0`

`QE_IPI_ARCHITECTURE_SUPPORTED = true`

`CANDIDATE_VERSION_PAIR_IDENTIFIED = true`

`EXACT_SOCKET_SYNTAX_QUALIFIED_FOR_PAIR = false`

`RESTART_TOPOLOGY_QUALIFIED = false`

`RESOURCE_PILOT_COMPLETE = false`

`PRODUCTION_PIMD_AUTHORIZED = false`

No quantum result should be reported until QENV-1 through the claim-relevant qualification stages are completed.

## Documentation consulted

- Quantum ESPRESSO Foundation release page, current listing including QE v7.6.
- Quantum ESPRESSO PWscf input/user documentation for `max_seconds`, restart, structural optimization, and i-PI socket interface.
- Quantum ESPRESSO NEB input documentation, currently labelled version 7.5.
- i-PI official documentation for installation, client-server communication, Quantum ESPRESSO client support, sockets/shared-memory/MPI transports.
- i-PI GitHub releases, current latest release v3.2.0.
