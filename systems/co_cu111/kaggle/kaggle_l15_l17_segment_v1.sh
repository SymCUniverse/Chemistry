#!/usr/bin/env bash
set -euo pipefail

REPO="${KAGGLE_REPO:-/kaggle/working/Chemistry}"
WORK_ROOT="${KAGGLE_WORK_ROOT:-/kaggle/working}"
TMP_ROOT="${KAGGLE_TMP_ROOT:-/kaggle/tmp}"
ACTIVE="$WORK_ROOT/symc_l15_l17_active"
RESULTS="$WORK_ROOT/symc_l15_l17_results"
BOOT="$TMP_ROOT/symc_l15_l17_prod_bootstrap"
RUN="$TMP_ROOT/symc_l15_l17_prod_run"
ROUTE="systems/co_cu111/KAGGLE_L15_L17_EXECUTION_ROUTE_v0.1.json"
PROTOCOL="systems/co_cu111/SYSTEM2_PBE_L15_L17_SITE_DEPTH_DIAGNOSTIC_v0.2.json"
RUNNER="systems/co_cu111/pbe_l15_l17_site_depth_diagnostic_v2.py"
ZIP="systems/co_cu111/personal_bootstrap/co-cu111-l15-l17-site-depth-inputs-v2.zip"
ZIP_SHA="babc1533a8c894420762c734e853a5009497cada508441573f8cef552e6ca257"
PW_SHA="2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855"
PERSIST_CEILING=19000000000

fail() { echo "$1" >&2; exit "${2:-2}"; }

DEPTH="${1:-}"
SITE="${2:-}"
SEGMENT="${3:-}"
[[ "$DEPTH" == "L15" || "$DEPTH" == "L17" ]] || fail "USAGE: $0 L15|L17 top|bridge|fcc_hollow|hcp_hollow SEGMENT"
case "$SITE" in top|bridge|fcc_hollow|hcp_hollow) ;; *) fail "USAGE: invalid site $SITE" ;; esac
[[ "$SEGMENT" =~ ^[1-6]$ ]] || fail "USAGE: segment must be 1..6"

[[ -d "$REPO/.git" ]] || fail "MECHANICAL_HOLD: repository not found at $REPO"
mkdir -p "$TMP_ROOT" "$RESULTS"
cd "$REPO"
[[ "$(git rev-parse --abbrev-ref HEAD)" == "personal-free-compute" ]] || fail "MECHANICAL_HOLD: wrong repository branch"

python3 - <<PY
import json
p=json.load(open("$ROUTE"))
assert p["status"] == "FROZEN_AFTER_RESOURCE_PROBE_BEFORE_SCIENTIFIC_RESULTS"
assert p["resource_probe"]["status"] == "PASS"
assert p["runtime_identity"]["exact_pw_sha256"] == "$PW_SHA"
assert p["runtime_identity"]["execution_mode"] == "DIRECT_ONE_RANK"
assert p["runtime_identity"]["mpi_ranks"] == 1
assert p["runtime_identity"]["qe_max_seconds_per_segment"] == 16200
fw=p["frozen_science_firewall"]
for k in ("scientific_settings_changed","thresholds_changed","coverage_changed","geometry_changed","kmesh_changed","execution_rank_changed","paid_compute_used","automatic_paid_escalation"):
    assert fw[k] is False
assert fw["original_l17_hold_preserved"] is True
print("KAGGLE_L15_L17_EXECUTION_ROUTE_FIREWALL_PASS")
PY

python3 systems/co_cu111/test_pbe_l15_l17_site_depth_diagnostic_v2.py -v
python3 "$RUNNER" self-test --protocol "$PROTOCOL"
echo "$ZIP_SHA  $ZIP" | sha256sum -c -

rm -rf "$BOOT" "$RUN"
mkdir -p "$BOOT" "$RUN"
unzip -q "$ZIP" -d "$BOOT"
(cd "$BOOT" && sha256sum -c engine/meta/STAGE_A_ENGINE.sha256)
chmod +x "$BOOT/engine/bin/pw.x"
[[ "$(sha256sum "$BOOT/engine/bin/pw.x" | awk '{print $1}')" == "$PW_SHA" ]] || fail "MECHANICAL_HOLD: exact pw.x hash mismatch"

python3 "$RUNNER" preflight \
  --protocol "$PROTOCOL" \
  --l15-root "$BOOT/source_l15/l15_audit" \
  --l17-root "$BOOT/source_l17_relax" \
  --out "$RUN/PREFLIGHT.json"

if [[ "$SEGMENT" -eq 1 ]]; then
  if [[ -f "$ACTIVE/L15_L17_SITE_SCF_STATE.json" ]]; then
    python3 - <<PY
import json
p=json.load(open("$ACTIVE/L15_L17_SITE_SCF_STATE.json"))
if p.get("depth") != "$DEPTH" or p.get("site") != "$SITE":
    raise SystemExit("MECHANICAL_HOLD: another case already owns the active checkpoint")
if int(p.get("segment",-1)) >= 1:
    raise SystemExit("MECHANICAL_HOLD: this case already has an active segment; resume it instead of restarting segment 1")
PY
  fi
else
  [[ -f "$ACTIVE/L15_L17_SITE_SCF_STATE.json" ]] || fail "MECHANICAL_HOLD: no persisted active checkpoint for segment $SEGMENT"
  python3 - <<PY
import json
p=json.load(open("$ACTIVE/L15_L17_SITE_SCF_STATE.json"))
assert p["depth"] == "$DEPTH" and p["site"] == "$SITE"
assert int(p["segment"]) == int("$SEGMENT")-1
assert p["status"] == "CHECKPOINT"
print("PRIOR_EXACT_CHECKPOINT_SEQUENCE_PASS")
PY
fi

OUT="$RUN/out"
mkdir -p "$OUT"
ARGS=(
  scf-segment
  --protocol "$PROTOCOL"
  --surface-protocol systems/co_cu111/SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json
  --stage-a-result "$BOOT/stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json"
  --bundle systems/co_cu111/PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json
  --pseudo-dir "$BOOT/engine/pseudos"
  --pw "$BOOT/engine/bin/pw.x"
  --l15-root "$BOOT/source_l15/l15_audit"
  --l17-root "$BOOT/source_l17_relax"
  --depth "$DEPTH"
  --site "$SITE"
  --out "$OUT"
  --segment "$SEGMENT"
)
if [[ "$SEGMENT" -gt 1 ]]; then
  ARGS+=(--prior-root "$ACTIVE")
fi

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/usr/bin/time -v -o "$RUN/RESOURCE_USAGE.txt" python3 "$RUNNER" "${ARGS[@]}"
cp "$RUN/RESOURCE_USAGE.txt" "$OUT/RESOURCE_USAGE.txt"
cp "$RUN/PREFLIGHT.json" "$OUT/PREFLIGHT.json"

STATE="$OUT/L15_L17_SITE_SCF_STATE.json"
[[ -f "$STATE" ]] || fail "MECHANICAL_HOLD: production segment returned without state"
STATUS=$(python3 - <<PY
import json
p=json.load(open("$STATE"))
assert p["depth"] == "$DEPTH" and p["site"] == "$SITE" and int(p["segment"]) == int("$SEGMENT")
assert p["checkpoint_semantics"] == "QE_CLEAN_MAX_SECONDS_EXACT_RESTART"
assert p["scientific_settings_changed"] is False
assert p["original_l17_hold_preserved"] is True
assert p["absolute_clean_surface_pass_claimed"] is False
print(p["status"])
PY
)

if [[ "$STATUS" == "CHECKPOINT" ]]; then
  python3 - <<PY
import importlib.util, json, pathlib
runner=pathlib.Path("$RUNNER").resolve()
spec=importlib.util.spec_from_file_location("m",runner); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p=json.load(open("$STATE"))
m.verify_checkpoint_manifest(pathlib.Path("$OUT"),p["checkpoint_manifest_sha256"])
print("NEW_EXACT_CHECKPOINT_MANIFEST_PASS")
PY
  BYTES=$(du -sb "$OUT" | awk '{print $1}')
  if (( BYTES > PERSIST_CEILING )); then
    python3 - <<PY
import json, pathlib
row={
 "schema":"symc-kaggle-l15-l17-storage-hold-v0.1",
 "status":"OVERSIZE_CHECKPOINT_LIVE_SCRATCH_ONLY",
 "depth":"$DEPTH","site":"$SITE","segment":int("$SEGMENT"),
 "checkpoint_root":"$OUT","checkpoint_bytes":int("$BYTES"),
 "persistent_soft_ceiling_bytes":int("$PERSIST_CEILING"),
 "scientific_settings_changed":False,"thresholds_changed":False,
 "exact_restart_required":True,"paid_compute_used":False
}
pathlib.Path("$WORK_ROOT/KAGGLE_L15_L17_STORAGE_HOLD.json").write_text(json.dumps(row,indent=2,sort_keys=True)+"\n")
print(json.dumps(row,indent=2,sort_keys=True))
PY
    echo "KAGGLE_L15_L17_OVERSIZE_CHECKPOINT_LIVE_SCRATCH: $DEPTH $SITE segment $SEGMENT"
    exit 42
  fi

  FREE=$(df -B1 "$WORK_ROOT" | awk 'NR==2 {print $4}')
  if (( FREE < BYTES + 500000000 )) && [[ -d "$ACTIVE" ]]; then
    echo "Persistent space requires retiring the verified prior checkpoint before copying the verified new checkpoint."
    rm -rf "$ACTIVE"
    FREE=$(df -B1 "$WORK_ROOT" | awk 'NR==2 {print $4}')
  fi
  (( FREE >= BYTES + 500000000 )) || fail "MECHANICAL_HOLD: insufficient persistent space for verified checkpoint; scratch copy retained" 43

  NEXT="$WORK_ROOT/symc_l15_l17_active_next"
  rm -rf "$NEXT"
  cp -a "$OUT" "$NEXT"
  python3 - <<PY
import importlib.util, json, pathlib
runner=pathlib.Path("$RUNNER").resolve()
spec=importlib.util.spec_from_file_location("m",runner); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r=pathlib.Path("$NEXT"); p=json.load(open(r/"L15_L17_SITE_SCF_STATE.json"))
m.verify_checkpoint_manifest(r,p["checkpoint_manifest_sha256"])
print("PERSISTED_EXACT_CHECKPOINT_MANIFEST_PASS")
PY
  rm -rf "$ACTIVE"
  mv "$NEXT" "$ACTIVE"
  rm -rf "$RUN" "$BOOT"
  echo "KAGGLE_L15_L17_CHECKPOINT_PERSISTED: $DEPTH $SITE segment $SEGMENT"
  exit 0
fi

[[ "$STATUS" == "COMPLETE" ]] || fail "MECHANICAL_HOLD: unexpected segment state $STATUS"
CASE_ROOT="$RESULTS/$DEPTH/$SITE"
mkdir -p "$CASE_ROOT"
FINAL_SEG_ROOT="$CASE_ROOT/segment$SEGMENT"
rm -rf "$FINAL_SEG_ROOT"
cp -a "$OUT" "$FINAL_SEG_ROOT"

PRIOR="$FINAL_SEG_ROOT"
if (( SEGMENT < 6 )); then
  for N in $(seq $((SEGMENT+1)) 6); do
    CARRY="$CASE_ROOT/segment$N"
    rm -rf "$CARRY"
    python3 "$RUNNER" scf-segment \
      --protocol "$PROTOCOL" \
      --surface-protocol systems/co_cu111/SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json \
      --stage-a-result "$BOOT/stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json" \
      --bundle systems/co_cu111/PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json \
      --pseudo-dir "$BOOT/engine/pseudos" \
      --pw "$BOOT/engine/bin/pw.x" \
      --l15-root "$BOOT/source_l15/l15_audit" \
      --l17-root "$BOOT/source_l17_relax" \
      --depth "$DEPTH" --site "$SITE" --out "$CARRY" --segment "$N" --prior-root "$PRIOR"
    PRIOR="$CARRY"
  done
fi

rm -rf "$ACTIVE"
python3 - <<PY
import json, pathlib
order=["L15:top","L15:bridge","L15:fcc_hollow","L15:hcp_hollow","L17:top","L17:bridge","L17:fcc_hollow","L17:hcp_hollow"]
cur="$DEPTH:$SITE"; i=order.index(cur); nxt=order[i+1] if i+1<len(order) else None
row={
 "schema":"symc-kaggle-l15-l17-progress-v0.1",
 "status":"CASE_COMPLETE" if nxt else "ALL_EIGHT_CASES_COMPLETE_READY_FOR_ADJUDICATION",
 "completed_case":cur,"completed_at_segment":int("$SEGMENT"),"next_case":nxt,
 "scientific_settings_changed":False,"thresholds_changed":False,"original_l17_hold_preserved":True
}
pathlib.Path("$WORK_ROOT/KAGGLE_L15_L17_PROGRESS.json").write_text(json.dumps(row,indent=2,sort_keys=True)+"\n")
print(json.dumps(row,indent=2,sort_keys=True))
PY
rm -rf "$RUN" "$BOOT"
echo "KAGGLE_L15_L17_CASE_COMPLETE: $DEPTH $SITE"
