#!/usr/bin/env bash
# llm-wiki server-side sync: pull latest from origin so desktop edits (via
# Obsidian Git plugin) show up here. Runs on a cron. Safe to run manually.
set -euo pipefail
cd /srv/projects/llm-wiki

# Abort if there are uncommitted local changes (don't clobber server edits).
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[sync-pull] local changes present, skipping pull (commit them first)."
  exit 0
fi

git fetch --quiet origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse '@{u}' 2>/dev/null || echo "")

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "[sync-pull] already up to date."
  exit 0
fi

# Fast-forward only — never silently merge/rebase server work away.
git merge --ff-only origin/main && echo "[sync-pull] pulled $(git rev-parse --short HEAD)."
