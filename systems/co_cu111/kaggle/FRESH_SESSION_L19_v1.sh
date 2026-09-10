#!/usr/bin/env bash
set -euo pipefail
REPO_URL="https://github.com/SymCUniverse/Chemistry.git"
BRANCH="personal-free-compute"
REPO="/kaggle/working/Chemistry"
ORCH="$REPO/systems/co_cu111/kaggle/kaggle_l19_resilient_v2.py"
POINTERS="/kaggle/working/SYMC_L19_STORAGE_POINTERS.txt"

printf '\n===== SYMC CO/Cu(111) L19 FRESH-SESSION BOOTSTRAP =====\n'
[[ -d /kaggle/working ]] || { echo 'MECHANICAL_HOLD: run inside Kaggle'; exit 2; }
mkdir -p /kaggle/tmp
if pgrep -af '[p]w\.x' >/dev/null 2>&1; then
  echo 'MECHANICAL_HOLD: pw.x is already running in this Kaggle session; use a separate Kaggle notebook/session for the parallel L19 lane.'
  pgrep -af '[p]w\.x' || true
  exit 3
fi
if [[ ! -d "$REPO/.git" ]]; then
  rm -rf "$REPO"
  git clone --depth 1 --single-branch --branch "$BRANCH" "$REPO_URL" "$REPO"
else
  if ! git -C "$REPO" diff --quiet || ! git -C "$REPO" diff --cached --quiet; then
    echo 'MECHANICAL_HOLD: repository has local changes'; git -C "$REPO" status --short; exit 4
  fi
  git -C "$REPO" fetch origin "$BRANCH"
  git -C "$REPO" checkout -B "$BRANCH" "origin/$BRANCH"
fi
[[ -f "$ORCH" ]] || { echo "MECHANICAL_HOLD: missing $ORCH"; exit 5; }
commit=$(git -C "$REPO" rev-parse HEAD)
cat > "$POINTERS" <<TXT
SYMC CO/Cu(111) L19 STORAGE POINTERS
=====================================
AUTHORITATIVE DURABLE CHECKPOINTS
  private dataset A: symcuniverse/symc-co-cu111-l19-checkpoint-a
  private dataset B: symcuniverse/symc-co-cu111-l19-checkpoint-b
  metadata: L19_CHECKPOINT_META.json
  archive: symc_l19_checkpoint.qebin
SESSION WORKSPACE
  repo: /kaggle/working/Chemistry
  rolling state: /kaggle/working/symc_l19_current
  small history: /kaggle/working/symc_l19_history
  persistence receipt: /kaggle/working/KAGGLE_L19_PERSISTENCE_STATUS.json
  final result: /kaggle/working/L19_CONVERGENCE_RESULT.json
  scratch/bootstrap: /kaggle/tmp/symc_l19_bootstrap
IMPORTANT
  /kaggle/working and /kaggle/tmp are disposable.
  The two private datasets are the durable restart store.
  This launcher restores only a size/SHA/route/protocol verified checkpoint.
REPOSITORY
  branch=$BRANCH
  commit=$commit
TXT
cat "$POINTERS"
exec python3 "$ORCH"
