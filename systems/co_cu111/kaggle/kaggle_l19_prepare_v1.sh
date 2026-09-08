#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-/kaggle/working/Chemistry}"
WORK_ROOT="${KAGGLE_WORK_ROOT:-/kaggle/working}"
TMP_ROOT="${KAGGLE_TMP_ROOT:-/kaggle/tmp}"
BOOT="$TMP_ROOT/symc_l19_bootstrap"
ENV_JSON="$WORK_ROOT/KAGGLE_L19_ENVIRONMENT.json"
PREFLIGHT_JSON="$WORK_ROOT/KAGGLE_L19_PREFLIGHT.json"

fail() { echo "$1" >&2; exit "${2:-2}"; }

[[ -d "$REPO/.git" ]] || fail "MECHANICAL_HOLD: repository not found at $REPO"
mkdir -p "$TMP_ROOT"

ram_bytes=$(awk '/MemTotal:/ {print $2*1024}' /proc/meminfo | awk '{printf "%.0f",$1}')
work_free=$(df -B1 "$WORK_ROOT" | awk 'NR==2 {print $4}')
tmp_free=$(df -B1 "$TMP_ROOT" | awk 'NR==2 {print $4}')
logical_cpus=$(getconf _NPROCESSORS_ONLN)

# L19 already proved viable on a ~15 GiB standard runner. Require a substantial
# margin before a long Kaggle run, without changing any scientific setting.
[[ "$ram_bytes" -ge 24000000000 ]] || fail "MECHANICAL_RESOURCE_HOLD: Kaggle RAM below 24 GB safety floor" 20
[[ "$work_free" -ge 14000000000 ]] || fail "MECHANICAL_RESOURCE_HOLD: less than 14 GB free persistent output space" 21
[[ "$tmp_free" -ge 24000000000 ]] || fail "MECHANICAL_RESOURCE_HOLD: less than 24 GB scratch space" 22

cd "$REPO"
branch=$(git rev-parse --abbrev-ref HEAD)
[[ "$branch" == "personal-free-compute" ]] || fail "MECHANICAL_HOLD: expected personal-free-compute branch, got $branch"

sha_check() {
  expected="$1"; path="$2"
  [[ -f "$path" ]] || fail "MECHANICAL_HOLD: missing $path"
  actual=$(sha256sum "$path" | awk '{print $1}')
  [[ "$actual" == "$expected" ]] || fail "MECHANICAL_HOLD: SHA256 mismatch for $path"
}

sha_check db0ff7ea1e85c4c709548a81351030d90d1db95b2df7d99659e362aba79a0b4f systems/co_cu111/SYSTEM2_PBE_SURFACE_DEPTH_STACKING_POLICY_v0.1.json
sha_check f27ecf8ee22776e695b92549c1f2a8a8818df57d8f8f24033d0cd2c49f5f361e systems/co_cu111/SYSTEM2_PBE_SURFACE_CONVERGENCE_L19_v0.1.json
sha_check 0cd11a12c5f031197e4cc11880e5b0dd963ee83e5b223b1eae308d5bec9e0401 systems/co_cu111/pbe_surface_depth_stack_v1.py
sha_check 7dc5f5cbd5592ee9535b471732bfd2c2e459a4221c8b6d1a1fd6b27c8ed1ba6f systems/co_cu111/test_pbe_surface_depth_stack_v1.py
sha_check babc1533a8c894420762c734e853a5009497cada508441573f8cef552e6ca257 systems/co_cu111/personal_bootstrap/co-cu111-l15-l17-site-depth-inputs-v2.zip
sha_check e8b99f660762724922a9be153b374ccf9fc7f269744570b978d5d2e2b15de0a4 systems/co_cu111/personal_bootstrap/RANK_SELECTION_RESULT.json

python3 -m py_compile systems/co_cu111/pbe_surface_depth_stack_v1.py systems/co_cu111/test_pbe_surface_depth_stack_v1.py
python3 systems/co_cu111/test_pbe_surface_depth_stack_v1.py -v
python3 systems/co_cu111/pbe_surface_depth_stack_v1.py self-test --protocol systems/co_cu111/SYSTEM2_PBE_SURFACE_CONVERGENCE_L19_v0.1.json

# Install only runtime libraries needed by the already-frozen pw.x binary.
if command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libopenblas-dev liblapack-dev libfftw3-dev libopenmpi-dev openmpi-bin >/dev/null
else
  fail "MECHANICAL_HOLD: apt-get unavailable for unchanged QE runtime libraries"
fi

rm -rf "$BOOT"
mkdir -p "$BOOT"
unzip -q systems/co_cu111/personal_bootstrap/co-cu111-l15-l17-site-depth-inputs-v2.zip -d "$BOOT"
(cd "$BOOT" && sha256sum -c engine/meta/STAGE_A_ENGINE.sha256)
chmod +x "$BOOT/engine/bin/pw.x"
sha_check_local() {
  expected="$1"; path="$2"
  actual=$(sha256sum "$path" | awk '{print $1}')
  [[ "$actual" == "$expected" ]] || fail "MECHANICAL_HOLD: bootstrap SHA256 mismatch for $path"
}
sha_check_local 2b1ede22d276b1d4dab3e31212f306e88ae57e00f33ce6b532b849493a457855 "$BOOT/engine/bin/pw.x"
sha_check_local 3aaf41c304c4238da5804d095c5724f810ff06f67060dccecb3277efa46a1d15 "$BOOT/source_l17_relax/L17_RESTART_STATE.json"
sha_check_local 45eb9c31a954d736f799e70964508c22a2cfb8781e11f171801ad4b4a3681b2d "$BOOT/source_l17_result/L17_CONVERGENCE_RESULT.json"
sha_check_local 2f77135848bbfb90904cbbf54eeb3ef4e8de3629f5ddcc0b7157a26c6f31fff3 "$BOOT/stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json"

ldd "$BOOT/engine/bin/pw.x" | tee "$WORK_ROOT/KAGGLE_L19_PW_LDD.txt"
if ldd "$BOOT/engine/bin/pw.x" | grep -q 'not found'; then
  fail "MECHANICAL_HOLD: frozen pw.x still has unresolved shared libraries" 23
fi

python3 systems/co_cu111/pbe_surface_depth_stack_v1.py preflight \
  --protocol systems/co_cu111/SYSTEM2_PBE_SURFACE_CONVERGENCE_L19_v0.1.json \
  --source-relax-root "$BOOT/source_l17_relax" \
  --source-result-root "$BOOT/source_l17_result" \
  --out "$PREFLIGHT_JSON" \
  --surface-protocol systems/co_cu111/SYSTEM2_PBE_SURFACE_SITE_ORDERING_PROTOCOL_v0.1.json \
  --stage-a-result "$BOOT/stage_a_decision/PBE_STAGE_A_NUMERICAL_EXTENSION_RESULT.json" \
  --bundle systems/co_cu111/PBE_PSEUDOPOTENTIAL_BUNDLE_v0.1.json \
  --pseudo-dir "$BOOT/engine/pseudos" \
  --pw "$BOOT/engine/bin/pw.x" \
  --selection systems/co_cu111/personal_bootstrap/RANK_SELECTION_RESULT.json

python3 - <<PY
import json, os, platform, pathlib
row = {
  "schema": "symc-kaggle-l19-environment-v0.1",
  "status": "PASS_KAGGLE_L19_ENVIRONMENT_AND_PREFLIGHT",
  "ram_bytes": int("$ram_bytes"),
  "logical_cpus": int("$logical_cpus"),
  "working_free_bytes_at_preflight": int("$work_free"),
  "tmp_free_bytes_at_preflight": int("$tmp_free"),
  "repository_branch": "$branch",
  "scientific_settings_changed": False,
  "thresholds_changed": False,
  "paid_compute_used": False,
  "platform": platform.platform(),
}
pathlib.Path("$ENV_JSON").write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
print(json.dumps(row, indent=2, sort_keys=True))
PY

echo 'KAGGLE_L19_READY_FOR_RELAX_SEGMENT_1'
