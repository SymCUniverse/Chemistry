#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-/kaggle/working/Chemistry}"
WORK_ROOT="${KAGGLE_WORK_ROOT:-/kaggle/working}"
TMP_ROOT="${KAGGLE_TMP_ROOT:-/kaggle/tmp}"
BOOT="$TMP_ROOT/symc_l15_l17_probe_bootstrap"
PROBE="$TMP_ROOT/symc_l15_l17_probe"
RESULT="$WORK_ROOT/KAGGLE_L15_L17_RESOURCE_PROBE.json"
ZIP="systems/co_cu111/personal_bootstrap/co-cu111-l15-l17-site-depth-inputs-v2.zip"
ZIP_SHA="babc1533a8c894420762c734e853a5009497cada508441573f8cef552e6ca257"
PW_SHA="2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855"

fail() { echo "$1" >&2; exit "${2:-2}"; }

[[ -d "$REPO/.git" ]] || fail "MECHANICAL_HOLD: repository not found at $REPO"
mkdir -p "$TMP_ROOT"
cd "$REPO"

branch=$(git rev-parse --abbrev-ref HEAD)
[[ "$branch" == "personal-free-compute" ]] || fail "MECHANICAL_HOLD: expected personal-free-compute branch, got $branch"

# This is intentionally NON-ADMISSIBLE. It tests only whether the exact frozen
# L15/top 2x2 workload can remain alive for 300 seconds on this Kaggle CPU VM.
python3 systems/co_cu111/test_pbe_l15_l17_site_depth_diagnostic_v2.py -v
python3 systems/co_cu111/pbe_l15_l17_site_depth_diagnostic_v2.py self-test \
  --protocol systems/co_cu111/SYSTEM2_PBE_L15_L17_SITE_DEPTH_DIAGNOSTIC_v0.2.json

# The exact frozen runtime bundle is repository-local and hash pinned.
echo "$ZIP_SHA  $ZIP" | sha256sum -c -
rm -rf "$BOOT" "$PROBE"
mkdir -p "$BOOT" "$PROBE"
unzip -q "$ZIP" -d "$BOOT"
(cd "$BOOT" && sha256sum -c engine/meta/STAGE_A_ENGINE.sha256)
chmod +x "$BOOT/engine/bin/pw.x"
actual_pw=$(sha256sum "$BOOT/engine/bin/pw.x" | awk '{print $1}')
[[ "$actual_pw" == "$PW_SHA" ]] || fail "MECHANICAL_HOLD: exact pw.x hash mismatch"

if ! command -v /usr/bin/time >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq time >/dev/null
fi

# Build the real frozen v0.2 L15/top 2x2 input. The helper labels all resulting
# output/checkpoint material as resource-probe-only and scientifically inadmissible.
python3 systems/co_cu111/personal_standard_resource_probe_v2.py \
  "$BOOT/engine/pseudos" "$PROBE"

ram_bytes=$(awk '/MemTotal:/ {print $2*1024}' /proc/meminfo | awk '{printf "%.0f",$1}')
logical_cpus=$(getconf _NPROCESSORS_ONLN)
tmp_free_before=$(df -B1 "$TMP_ROOT" | awk 'NR==2 {print $4}')
work_free_before=$(df -B1 "$WORK_ROOT" | awk 'NR==2 {print $4}')

# Confirm the scientific-admissibility firewall before QE is launched.
python3 - <<PY
import json
p=json.load(open("$PROBE/probe_input_metadata.json"))
assert p["scientific_admissibility"] == "NONE_RESOURCE_PROBE_ONLY"
assert p["checkpoint_evidence_admitted"] is False
assert p["scientific_result_admitted"] is False
assert p["depth"] == "L15" and p["site"] == "top"
assert p["supercell"] == [2, 2] and int(p["kmesh"]) == 8
print("NON_ADMISSIBLE_RESOURCE_PROBE_FIREWALL_PASS")
PY

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
start_epoch=$(date +%s)
set +e
/usr/bin/time -v -o "$PROBE/time.txt" \
  timeout --signal=TERM --kill-after=120s 300s \
  "$BOOT/engine/bin/pw.x" \
  < "$PROBE/site_scf.in" \
  > "$PROBE/site_scf.out" 2>&1
rc=$?
set -e
end_epoch=$(date +%s)
elapsed=$((end_epoch-start_epoch))

max_rss_kb=$(awk -F: '/Maximum resident set size/ {gsub(/^[ \t]+/,"",$2); print $2}' "$PROBE/time.txt" | tail -n1)
max_rss_kb=${max_rss_kb:-0}
output_tail=$(tail -n 25 "$PROBE/site_scf.out" 2>/dev/null || true)

pass=false
reason=""
if [[ "$rc" -eq 124 && "$elapsed" -ge 295 ]]; then
  pass=true
  reason="SURVIVED_CONTROLLED_300_SECOND_TIMEOUT"
elif [[ "$rc" -eq 0 ]]; then
  if grep -qi 'JOB DONE' "$PROBE/site_scf.out" && ! grep -qiE 'Error in routine|MPI_ABORT' "$PROBE/site_scf.out"; then
    pass=true
    reason="QE_COMPLETED_BEFORE_300_SECONDS"
  else
    reason="QE_EXITED_ZERO_WITHOUT_VERIFIED_JOB_DONE"
  fi
else
  reason="QE_OR_VM_TERMINATED_BEFORE_CONTROLLED_TIMEOUT"
fi

python3 - <<PY
import json, pathlib
row={
  "schema":"symc-kaggle-l15-l17-resource-probe-v0.1",
  "status":"PASS" if "$pass" == "true" else "FAIL",
  "scientific_admissibility":"NONE_RESOURCE_PROBE_ONLY",
  "scientific_result_admitted":False,
  "checkpoint_evidence_admitted":False,
  "depth":"L15",
  "site":"top",
  "supercell":[2,2],
  "kmesh":8,
  "controlled_probe_seconds":300,
  "elapsed_seconds_wall":int("$elapsed"),
  "process_returncode":int("$rc"),
  "maximum_resident_set_kb":int("$max_rss_kb"),
  "ram_bytes":int("$ram_bytes"),
  "logical_cpus":int("$logical_cpus"),
  "working_free_bytes_before":int("$work_free_before"),
  "tmp_free_bytes_before":int("$tmp_free_before"),
  "reason":"$reason",
  "exact_pw_sha256":"$PW_SHA",
  "bootstrap_zip_sha256":"$ZIP_SHA",
  "scientific_settings_changed":False,
  "thresholds_changed":False,
  "paid_compute_used":False
}
pathlib.Path("$RESULT").write_text(json.dumps(row,indent=2,sort_keys=True)+"\n")
print(json.dumps(row,indent=2,sort_keys=True))
PY

# The probe checkpoint and raw output are intentionally destroyed. Only the
# small resource-classification JSON survives in /kaggle/working.
rm -rf "$PROBE" "$BOOT"

if [[ "$pass" == "true" ]]; then
  echo 'KAGGLE_L15_L17_300_SECOND_RESOURCE_PROBE_PASS'
else
  echo "KAGGLE_L15_L17_RESOURCE_PROBE_FAIL: $reason" >&2
  printf '%s\n' "$output_tail" >&2
  exit 40
fi
