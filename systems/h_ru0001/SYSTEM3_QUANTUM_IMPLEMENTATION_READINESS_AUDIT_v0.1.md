# System 3 H/Ru(0001) quantum implementation readiness audit v0.1

**Date:** 2026-09-11  
**Status:** `QUANTUM_IMPLEMENTATION_ROUTE_SUPPORTED_ENVIRONMENT_NOT_YET_QUALIFIED`  
**Phase:** P0-Q implementation/readiness audit  
**Scope:** Work that can be closed before final clean-surface computational reconciliation. This record does not authorize production PIMD.

## Question

Is the previously frozen open implementation concept, i-PI for nuclear dynamics with Quantum ESPRESSO PWscf as the force client, technically supported strongly enough to remain the planned System 3 quantum route, and what still has to be qualified before any evidentiary PIMD run?

## Documentation findings

### Quantum ESPRESSO

Current Quantum ESPRESSO PWscf documentation explicitly describes a socket interface with i-PI. In that documentation, i-PI acts as the server and PWscf acts as a force/stress client. The documented current command-line form includes `pw.x --ipi <address>:<port>` (or a UNIX-socket form), while the PWscf input is prepared as a single-point `calculation='scf'` initialization.

### i-PI

Current i-PI documentation lists Quantum ESPRESSO among out-of-the-box client codes and describes the same client-server architecture. Its current Getting Started material also contains a Quantum-Espresso example using an input-side `calculation='driver'` plus `srvaddress=...` convention.

## Implementation interpretation

The two projects independently document a supported QE/i-PI coupling route, so the architectural choice remains technically defensible.

However, the exact invocation convention is not treated as universal or frozen by this audit. The current documentation exposes at least two interface conventions: a QE command-line `--ipi`/SCF route and an i-PI-documented input-side `driver`/`srvaddress` route. This is classified as an **implementation-version/interface ambiguity**, not a scientific discrepancy.

Production must therefore be tied to exact tested software versions rather than copying a syntax example from whichever manual is open at the time.

## Pre-production qualification contract

Before any H/Ru quantum calculation can be evidentiary, a future compute-environment qualification must freeze and verify all of the following:

1. exact Quantum ESPRESSO version and executable SHA-256;
2. exact i-PI version/commit and package hash or immutable environment specification;
3. the exact QE/i-PI socket invocation convention used by those versions;
4. a non-admissible connection smoke test proving that positions/cell are received and forces/stress are returned correctly;
5. bead/client launch topology and processor allocation;
6. deterministic or bounded restart/checkpoint behavior appropriate to the chosen versions;
7. memory and wall-clock scaling from a non-admissible pilot before production bead calculations;
8. confirmation that the pilot did not inspect or optimize against held-out H/Ru rate agreement;
9. exact pseudopotential and electronic-structure settings inherited only from the qualified upstream System 3 model;
10. a preserved failure state if the intended environment cannot sustain the required bead/client topology.

## What remains frozen from the scientific protocol

- The nuclear-quantum tier remains required for a full H/Ru rate comparison under the existing System 3 protocol.
- The prospective bead grid remains 16/32/64 unless a separately justified amendment is frozen before decisive bead evidence.
- The bead-convergence criterion remains a free-energy-barrier change of <= 0.005 eV upon doubling P.
- Rate agreement may not select the bead count.
- The reaction coordinate must derive from the newly computed adjacent-site MEP rather than being imposed from published labels.
- A demonstrably nonrepresentative centroid coordinate returns `QUANTUM_REACTION_COORDINATE_HOLD`; it does not trigger an after-the-fact method switch.
- The standard GitHub runner is not promoted by this audit to a qualified production ab initio PIMD environment.

## Closure result

`QE_IPI_ARCHITECTURE_ROUTE = SUPPORTED`

`EXACT_INTERFACE_IMPLEMENTATION = VERSION_DEPENDENT_AND_MUST_BE_QUALIFIED`

`QUANTUM_COMPUTE_ENVIRONMENT = NOT_YET_QUALIFIED`

`PRODUCTION_PIMD_AUTHORIZED = false`

This removes uncertainty about whether QE/i-PI is a viable planned architecture while preserving the future environment/smoke-test/resource qualification as a genuine gate. None of this depends on the outcome of the current K24/K28 clean-surface diagnostic.
