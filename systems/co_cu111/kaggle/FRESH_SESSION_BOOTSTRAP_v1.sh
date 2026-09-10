#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/SymCUniverse/Chemistry.git"
BRANCH="personal-free-compute"
REPO="/kaggle/working/Chemistry"
POINTERS="/kaggle/working/SYMC_STORAGE_POINTERS.txt"
ORCH="$REPO/systems/co_cu111/kaggle/kaggle_l15_l17_resilient_v3.py"

printf '\n===== SYMC L15/L17 FRESH-SESSION BOOTSTRAP =====\n'

if [ ! -d /kaggle/working ]; then
  echo "MECHANICAL_HOLD: /kaggle/working does not exist. Run this inside a Kaggle notebook session."
  exit 2
fi
mkdir -p /kaggle/tmp

if pgrep -af '[p]w\.x' >/dev/null 2>&1; then
  echo "MECHANICAL_HOLD: a pw.x process is already running in this Kaggle session. Refusing duplicate QE compute."
  pgrep -af '[p]w\.x' || true
  exit 3
fi

if [ ! -d "$REPO/.git" ]; then
  echo "FRESH_SESSION: repository clone is absent; reconstructing it now."
  rm -rf "$REPO"
  git clone --depth 1 --single-branch --branch "$BRANCH" "$REPO_URL" "$REPO"
else
  echo "EXISTING_SESSION: repository clone found; verifying it before update."
  if ! git -C "$REPO" diff --quiet || ! git -C "$REPO" diff --cached --quiet; then
    echo "MECHANICAL_HOLD: local repository has uncommitted changes. Refusing to overwrite them."
    git -C "$REPO" status --short || true
    exit 4
  fi
  current_branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
  if [ "$current_branch" != "$BRANCH" ]; then
    git -C "$REPO" fetch origin "$BRANCH"
    git -C "$REPO" checkout -B "$BRANCH" "origin/$BRANCH"
  fi
  git -C "$REPO" pull --ff-only origin "$BRANCH"
fi

current_branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
current_commit="$(git -C "$REPO" rev-parse HEAD)"
if [ "$current_branch" != "$BRANCH" ]; then
  echo "MECHANICAL_HOLD: expected branch $BRANCH but found $current_branch"
  exit 5
fi
if [ ! -f "$ORCH" ]; then
  echo "MECHANICAL_HOLD: resilient orchestrator is missing at $ORCH"
  exit 6
fi

cat > "$POINTERS" <<EOF
SYMC CO/Cu(111) L15/L17 STORAGE POINTERS
=========================================

AUTHORITATIVE DURABLE CHECKPOINTS
  Kaggle private dataset A:
    symcuniverse/symc-co-cu111-l15-l17-checkpoint-a
  Kaggle private dataset B:
    symcuniverse/symc-co-cu111-l15-l17-checkpoint-b
  Durable metadata filename:
    CHECKPOINT_META.json
  Durable archive filename:
    symc_checkpoint.qebin

SESSION-LOCAL WORKSPACE
  Repository:
    /kaggle/working/Chemistry
  Small result tree:
    /kaggle/working/symc_l15_l17_results
  Preflight record:
    /kaggle/working/KAGGLE_L15_L17_PREFLIGHT.json
  Latest remote-persistence receipt:
    /kaggle/working/KAGGLE_L15_L17_PERSISTENCE_STATUS.json
  Large active QE checkpoint:
    /kaggle/tmp/symc_l15_l17_active
  Next-segment staging:
    /kaggle/tmp/symc_l15_l17_next
  Restore staging:
    /kaggle/tmp/symc_l15_l17_restore
  Persistence staging:
    /kaggle/tmp/symc_l15_l17_persist_stage
  Engine/bootstrap extraction:
    /kaggle/tmp/symc_l15_l17_resilient_bootstrap

IMPORTANT
  /kaggle/working and /kaggle/tmp are disposable session workspaces.
  The private dataset A/B pair is the durable restart store.
  The orchestrator restores the newest slot only after metadata/hash/manifest verification.

REPOSITORY IDENTITY
  branch=$current_branch
  commit=$current_commit
EOF

cat "$POINTERS"

python3 - <<'PY'
try:
    import kagglehub
except Exception as exc:
    raise SystemExit(f"MECHANICAL_HOLD: kagglehub is unavailable: {exc}")
try:
    who = kagglehub.whoami()
except Exception as exc:
    raise SystemExit(f"MECHANICAL_HOLD: Kaggle native authentication failed: {exc}")
print(f"KAGGLE_NATIVE_IDENTITY={who}")
PY

printf '\n===== DISK SNAPSHOT =====\n'
df -h /kaggle/working /kaggle/tmp || true

printf '\n===== LAUNCHING HASH-VERIFIED RESUME =====\n'
echo "The orchestrator will inspect both private checkpoint slots and restore the newest verified serial before new QE compute."
exec python3 "$ORCH"
