#!/usr/bin/env python3
"""Build the real frozen L15/top 2x2 QE input for a NON-SCIENTIFIC resource probe.

This helper intentionally bypasses the frozen pw.x identity check because its
only purpose is to test whether a standard public GitHub runner survives the
actual L15/top workload long enough to justify a no-cost execution route.
No energy, convergence state, or checkpoint produced by this helper is
scientifically admissible.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import pbe_l15_l17_site_depth_diagnostic_v2 as v2  # type: ignore


def main() -> None:
    repo = HERE.parent.parent
    protocol_path = HERE / "SYSTEM2_PBE_L15_L17_SITE_DEPTH_DIAGNOSTIC_v0.2.json"
    surface_path = HERE / "SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json"
    bundle_path = HERE / "PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json"
    source_path = HERE / "personal_bootstrap" / "L15_AUDIT_SUMMARY_ORIGINAL.json"
    pseudo_dir = Path(sys.argv[1]).resolve()
    out_root = Path(sys.argv[2]).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    qe_tmp = out_root / "qe_tmp"
    qe_tmp.mkdir(parents=True, exist_ok=True)

    p = v2.load_protocol_v2(protocol_path)
    source = json.loads(source_path.read_text())
    src = p["source_l15"]
    assert source["case_id"] == src["case_id"]
    assert int(source["layers"]) == int(src["layers"]) == 15
    assert float(source["vacuum_angstrom"]) == float(src["vacuum_angstrom"]) == 32.0
    assert int(source["kmesh"]) == int(src["kmesh"]) == 28
    assert source["mechanical_pass"] is True
    assert len(source["final_atoms"]) == 15

    cell, atoms, evidence = v2.matched_geometry_v2(source, "L15", "top", p)
    base = v2.v1.import_base()
    surface = base.load_json(surface_path)
    bundle = base.load_json(bundle_path)
    text = base.qe_input(
        calculation="scf",
        prefix="co_cu111_l15_top_personal_resource_probe",
        cell=cell,
        atoms=atoms,
        kmesh=int(p["matched_site_screen"]["kmesh"]),
        protocol=surface,
        bundle=bundle,
        pseudo_dir=pseudo_dir,
        outdir=qe_tmp,
    )
    inp = out_root / "site_scf.in"
    inp.write_text(text)
    meta = {
        "schema": "co-cu111-personal-standard-runner-resource-probe-v0.2",
        "scientific_admissibility": "NONE_RESOURCE_PROBE_ONLY",
        "checkpoint_evidence_admitted": False,
        "scientific_result_admitted": False,
        "depth": "L15",
        "site": "top",
        "supercell": [2, 2],
        "kmesh": int(p["matched_site_screen"]["kmesh"]),
        "nat": len(atoms),
        "layers": 15,
        "nominal_coverage_ML": 0.25,
        "ecutwfc_ry": surface["inherited_stage_a_settings"]["ecutwfc_ry"],
        "ecutrho_ry": surface["inherited_stage_a_settings"]["ecutrho_ry"],
        "esm_bc": "bc1",
        "geometry_evidence": evidence,
        "source_original_artifact_id": 9993915792,
        "source_original_artifact_zip_sha256": "babc1533a8c894420762c734e853a5009497cada508441573f8cef552e6ca257",
        "source_original_summary_sha256": "34b0290260dc6f59a596f34a15ef75f5af48674a9bf33f8f686a47618b379e2e",
        "runtime_identity_scientifically_admitted": False,
    }
    (out_root / "probe_input_metadata.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps(meta, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
