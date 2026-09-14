# System 3 H/Ru(0001) Quantum Environment Prequalification v0.3

**Date:** 14 September 2026  
**Status:** `CURRENT_VERSION_PAIR_IDENTIFIED_SOCKET_SMOKE_TEST_OPENED`  
**Phase:** P0-Q implementation/readiness  
**Supersedes for current environment-planning state:** `SYSTEM3_QUANTUM_ENVIRONMENT_PREQUALIFICATION_v0.2.md`  
**Production PIMD authorized:** **NO**

## Correction to v0.2

v0.2 recorded i-PI 3.2.0 as the latest release. A fresh check of the authoritative i-PI GitHub releases shows that **i-PI v3.3.0** was released on 30 June 2026. The v3.2.0 statement is therefore superseded. v0.2 remains preserved as historical audit lineage rather than silently rewritten.

The current candidate pair for a new environment qualification is:

- **Quantum ESPRESSO 7.6**, tag `qe-7.6`, annotated tag resolving to commit `9f93ddec427d2b9a45bb72d828c6d324f62fcabd`;
- **i-PI 3.3.0**, tag `v3.3.0`, commit `bf64b65ef2711638a5c9fad1fbd5dffc73b7c008`.

The official i-PI v3.3.0 wheel asset is `ipi-3.3.0-py3-none-any.whl` with published SHA-256 `a76886600559d536b80797a2051fc5f23664ba0db7d032edb1246605857dc2da`.

## Current upstream interface documentation

Quantum ESPRESSO's current PWscf user guide documents the native i-PI socket client as:

`pw.x --ipi localhost:PORT -in pw.input`

with a standard single-point `calculation='scf'` input. The same documentation recommends a UNIX socket when server and client share a machine.

i-PI's current getting-started/manual pages also show a Quantum ESPRESSO-side `calculation='driver'` / `srvaddress=...` convention. Because these two public descriptions are not textually identical, this project will not choose between them from documentation alone.

The first empirical smoke test is frozen to the **QE-native documented `--ipi` route** using the exact QE 7.6 / i-PI 3.3.0 pair. If that route fails for an interface-specific reason, the failure is preserved and a separately versioned test of the i-PI-documented driver syntax may follow. A failed socket test is not a reason to change H/Ru physics or PIMD convergence rules.

## Non-evidentiary socket smoke test

The smoke test uses the H2O Quantum ESPRESSO client example distributed in the i-PI v3.3.0 source tree, reduced to one bead and a very small number of integration steps solely to prove force/position/cell communication.

It must verify:

1. exact QE and i-PI release identities;
2. exact i-PI wheel hash;
3. successful build of `pw.x` from QE 7.6 source;
4. i-PI server startup;
5. QE connection through the documented socket interface;
6. at least one completed i-PI force exchange / trajectory step;
7. clean server/client termination or an explicitly understood stop after the requested smoke-test steps;
8. preservation of logs, input identities, version output, and build/runtime hashes.

The smoke-test H2O energies, forces, geometry, and trajectory are **not Chemistry evidence** and may not enter H/Ru calculations or claims.

## Qualification ladder after socket communication

A successful socket smoke test closes only the communication portion of QENV-2. It does not close:

- H/Ru pseudopotential/runtime compatibility under the new QE version;
- multi-client/bead topology;
- PIMD restart state;
- stochastic/thermostat restart semantics;
- electronic-force repeatability under the H/Ru production settings;
- resource feasibility for 16/32/64 beads;
- free-energy or rate convergence.

Those remain separately testable implementation/scientific gates.

## Scientific rules unchanged

This version correction changes no System-3 scientific rule:

- PIMD/quantum production remains unauthorized;
- bead ladder remains 16/32/64 unless separately amended before decisive evidence;
- bead convergence remains a free-energy-barrier change of <=0.005 eV on doubling;
- experimental rate agreement may not select bead count or quantum method;
- the reaction coordinate comes from the independently computed new PES/path;
- the HeSE H/Ru rate curve remains external validation rather than tuning evidence;
- changing the software version does not permit retrospective changes to classical surface evidence already computed with its frozen runtime.

## Current state

`QE_CURRENT_RELEASE = 7.6`

`IPI_CURRENT_RELEASE = 3.3.0`

`QE76_TAG_COMMIT = 9f93ddec427d2b9a45bb72d828c6d324f62fcabd`

`IPI330_TAG_COMMIT = bf64b65ef2711638a5c9fad1fbd5dffc73b7c008`

`SOCKET_SMOKE_TEST = OPENED_NOT_YET_ADJUDICATED`

`PRODUCTION_PIMD_AUTHORIZED = false`
