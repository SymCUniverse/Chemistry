#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:-}"
SEGMENT="${2:-}"
REPO="${3:-/kaggle/working/Chemistry}"
WORK_ROOT="${KAGGLE_WORK_ROOT:-/kaggle/working}"
TMP_ROOT="${KAGGLE_TMP_ROOT:-/kaggle/tmp}"
BOOT="$TMP_ROOT/symc_l19_bootstrap"
CURRENT="$WORK_ROOT/symc_l19_current"
NEXT="$TMP_ROOT/symc_l19_next"
HISTORY="$WORK_ROOT/symc_l19_history"

fail() { echo "$1" >&2; exit "${2:-2}"; }
[[ "$STAGE" == "relax" || "$STAGE" == "scf" ]] || fail "usage: kaggle_l19_segment_v1.sh <relax|scf> <segment> [repo]"
[[ "$SEGMENT" =~ ^[0-9]+$ ]] || fail "MECHANICAL_HOLD: segment must be integer"
[[ -d "$REPO/.git" ]] || fail "MECHANICAL_HOLD: repository missing"
[[ -d "$BOOT" ]] || fail "MECHANICAL_HOLD: Kaggle bootstrap missing; rerun kaggle_l19_prepare_v1.sh in this session"
mkdir -p "$TMP_ROOT" "$HISTORY"

cd "$REPO"
PROTOCOL=systems/co_cu111/SYSTEM2_PBE_SURFACE_CONVERGENCE_L19_v0.1.json
RUNNER=systems/co_cu111/pbe_surface_depth_stack_v1.py
SURFACE=systems/co_cu111/SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json
BUNDLE=systems/co_cu111/PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json
SELECTION=systems/co_cu111/personal_bootstrap/RANK_SELECTION_RESULT.json
PW="$BOOT/engine/bin/pw.x"
PSEUDO="$BOOT/engine/pseudos"
STAGE_A="$BOOT/stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json"
SOURCE_RELAX="$BOOT/source_l17_relax"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1

rm -rf "$NEXT"
mkdir -p "$NEXT"

common=(--protocol "$PROTOCOL" --segment "$SEGMENT" --out "$NEXT" --surface-protocol "$SURFACE" --stage-a-result "$STAGE_A" --bundle "$BUNDLE" --pseudo-dir "$PSEUDO" --pw "$PW" --selection "$SELECTION")

if [[ "$STAGE" == "relax" ]]; then
  if [[ "$SEGMENT" -eq 1 ]]; then
    python3 "$RUNNER" relax-segment "${common[@]}" --source-relax-root "$SOURCE_RELAX"
  else
    [[ -f "$CURRENT/SURFACE_DEPTH_RESTART_STATE.json" ]] || fail "MECHANICAL_HOLD: prior persistent relaxation state missing"
    python3 - <<PY
import json
p=json.load(open("$CURRENT/SURFACE_DEPTH_RESTART_STATE.json"))
assert p["stage"]=="relax" and int(p["segment"])==int("$SEGMENT")-1, p
assert p["scientific_settings_changed"] is False and p["thresholds_changed"] is False
print("PRIOR_RELAX_STATE_IDENTITY_PASS")
PY
    python3 "$RUNNER" relax-segment "${common[@]}" --source-relax-root "$SOURCE_RELAX" --prior-root "$CURRENT"
  fi
else
  if [[ "$SEGMENT" -eq 1 ]]; then
    [[ -f "$CURRENT/SURFACE_DEPTH_RESTART_STATE.json" ]] || fail "MECHANICAL_HOLD: final relaxation state missing"
    python3 - <<PY
import json
p=json.load(open("$CURRENT/SURFACE_DEPTH_RESTART_STATE.json"))
assert p["stage"]=="relax" and int(p["segment"])==6 and p["status"]=="COMPLETE", p
assert p["scientific_settings_changed"] is False and p["thresholds_changed"] is False
print("FINAL_RELAX_STATE_IDENTITY_PASS")
PY
    python3 "$RUNNER" scf-segment "${common[@]}" --relax-root "$CURRENT"
  else
    [[ -f "$CURRENT/SURFACE_DEPTH_RESTART_STATE.json" ]] || fail "MECHANICAL_HOLD: prior persistent SCF state missing"
    python3 - <<PY
import json
p=json.load(open("$CURRENT/SURFACE_DEPTH_RESTART_STATE.json"))
assert p["stage"]=="scf" and int(p["segment"])==int("$SEGMENT")-1, p
assert p["scientific_settings_changed"] is False and p["thresholds_changed"] is False
print("PRIOR_SCF_STATE_IDENTITY_PASS")
PY
    python3 "$RUNNER" scf-segment "${common[@]}" --prior-root "$CURRENT"
  fi
fi

[[ -f "$NEXT/SURFACE_DEPTH_RESTART_STATE.json" ]] || fail "MECHANICAL_HOLD: segment produced no state JSON"
status=$(python3 - <<PY
import json
p=json.load(open("$NEXT/SURFACE_DEPTH_RESTART_STATE.json"))
assert p["stage"]=="$STAGE" and int(p["segment"])==int("$SEGMENT"), p
assert p["status"] in {"CHECKPOINT","COMPLETE"}, p
assert p["scientific_settings_changed"] is False and p["thresholds_changed"] is False
print(p["status"])
PY
)

# Preserve small provenance before replacing the large rolling state.
stamp="${STAGE}_segment_${SEGMENT}"
mkdir -p "$HISTORY/$stamp"
cp "$NEXT/SURFACE_DEPTH_RESTART_STATE.json" "$HISTORY/$stamp/"
for f in QE_CHECKPOINT_MANIFEST.sha256 relax.in relax.out scf.in scf.out; do
  if [[ -f "$NEXT/$f" ]]; then
    if [[ "$f" == *.out ]]; then gzip -c "$NEXT/$f" > "$HISTORY/$stamp/$f.gz"; else cp "$NEXT/$f" "$HISTORY/$stamp/$f"; fi
  fi
done

# A COMPLETE state no longer needs the multi-GB QE outdir for downstream logic.
if [[ "$status" == "COMPLETE" ]]; then
  rm -rf "$NEXT/qe_checkpoint"
  rm -f "$NEXT/QE_CHECKPOINT_MANIFEST.sha256"
fi

next_bytes=$(du -sb "$NEXT" | awk '{print $1}')
if [[ "$status" == "CHECKPOINT" && "$next_bytes" -ge 19000000000 ]]; then
  fail "MECHANICAL_RESOURCE_HOLD: exact checkpoint approaches Kaggle 20 GB persisted-output ceiling" 30
fi

# Replace only after the new state has passed all identity checks. NEXT remains
# in scratch until this point, so a failed calculation never destroys CURRENT.
rm -rf "$CURRENT"
if mv "$NEXT" "$CURRENT" 2>/dev/null; then
  :
else
  cp -a "$NEXT" "$CURRENT"
  rm -rf "$NEXT"
fi

current_bytes=$(du -sb "$CURRENT" | awk '{print $1}')
work_free=$(df -B1 "$WORK_ROOT" | awk 'NR==2 {print $4}')
python3 - <<PY
import json, pathlib
row=json.load(open("$CURRENT/SURFACE_DEPTH_RESTART_STATE.json"))
summary={
  "schema":"symc-kaggle-l19-segment-persistence-v0.1",
  "stage":row["stage"],
  "segment":row["segment"],
  "status":row["status"],
  "persistent_state_bytes":int("$current_bytes"),
  "working_free_bytes_after_persist":int("$work_free"),
  "checkpoint_manifest_sha256":row.get("checkpoint_manifest_sha256"),
  "scientific_settings_changed":False,
  "thresholds_changed":False,
  "paid_compute_used":False,
}
pathlib.Path("$WORK_ROOT/KAGGLE_L19_LAST_SEGMENT.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
print(json.dumps(summary,indent=2,sort_keys=True))
PY

echo "KAGGLE_L19_${STAGE^^}_SEGMENT_${SEGMENT}_${status}_PERSISTED"
