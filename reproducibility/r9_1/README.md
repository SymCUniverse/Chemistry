# CSA R9.1 reviewer reproducibility snapshot

This branch provides the executable reviewer-facing verification layer for **Stability Architecture of Chemical Dynamics: Generator-First Classification, Spectroscopic Dissipation, and Barrier-Rate Evidence (R9.1)**.

It is intentionally separate from the working manuscript source. The private working manuscript is not required to execute the numerical checks below.

## Materialize the snapshot

From this directory:

```bash
python bootstrap_repro.py
```

The bootstrap verifies `payload.b64` against SHA-256 `c6959a485564eecdbe14fe1347bb53622463c59ce7838bf34acd80e8fd79f59c` and extracts `r9_1_repro/`.

## Environment

```bash
python -m venv .venv
. .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r r9_1_repro/engine/requirements.txt
```

## Reviewer checks

Frozen-engine targeted regressions:

```bash
cd r9_1_repro/engine
python -m pytest -q test_pass_table.py test_biorthogonal.py test_linewidth_hierarchy.py test_provenance_gate.py
python test_randomized.py
cd ..
```

Expected: **139 passing pytest checks**, followed by randomized verification with **0 false EP classifications in 500 semisimple twins, 0 misses in 500 defective critical systems, OVERALL: PASS**.

Reader-facing summary checks:

```bash
python verify_scalar_summary.py
python verify_barrier_summary.py
python verify_modal_benchmark.py
```

Expected headline results:

- scalar records: 30; recomputation 30/30; PASS;
- barrier atlas: 61 total comparative coordinates, comprising 59 physical-environment coordinates plus 2 cross-phase comparison-architecture coordinates; grades A/B/C = 11/30/20; 55 paired predicted/observed rates; no reactant-well chi used as a rate input; PASS;
- controlled reactive-mode benchmark: 7 orientations; table match PASS; Hessian/Grote-Hynes eigenvalue identity PASS.

## Provenance and scope

The snapshot is a compact extraction from the frozen ChemSA Release 38 computational layer and frozen Barrier-Height/Rate Atlas v0.9 records, plus the self-contained controlled modal benchmark. File identities inside the extracted snapshot are recorded in `r9_1_repro/SHA256SUMS.txt`.

`r9_1_repro/engine/RELEASE_RESULTS.json` preserves the historical Release 38 release-audit counts. This compact reviewer snapshot does **not** claim a fresh execution of the complete 442-test Release 38 tree, does not rebuild the manuscript PDFs, and does not expose the private working manuscript. Its purpose is to let a reviewer independently execute the numerical checks tied directly to R9.1's reader-facing claims.

The atlas verification record is included as `r9_1_repro/atlas/V0.9_VERIFICATION_REPORT.md`; the authoritative coordinate records used by the R9.1 barrier summary are under `r9_1_repro/atlas/data/`.


## Matched four-layer closure audit

The prospectively frozen end-to-end closure adjudication is in `matched_closure/`. Start with `matched_closure/README.md`, then `PROTOCOL.md` and `CLOSURE_REPORT.md`. The final result is 0 FULL_CLOSE, 1 NEAR_MISS, and 3 REFUSED cases; the negative result and compute stop decision are preserved as reproducibility evidence.
