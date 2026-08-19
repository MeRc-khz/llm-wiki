#!/usr/bin/env bash
# llm-wiki server-side sync: commit all changes and push to origin so the
# desktop (Obsidian Git plugin) receives server-side edits. Usage:
#   ./scripts/sync-push.sh "optional commit message"
set -euo pipefail
cd /srv/projects/llm-wiki
MSG="${1:-vault sync: $(date -u +%Y-%m-%dT%H:%M:%SZ)}"

git add -A
# Nothing to commit -> done.
if git diff --cached --quiet; then
  echo "[sync-push] nothing to commit."
  exit 0
fi

git commit -q -m "$MSG"
git push origin main && echo "[sync-push] pushed: $MSG"
