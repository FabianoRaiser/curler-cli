#!/usr/bin/env bash
# afterFileEdit: formata arquivos Python editados pelo agente.
set -euo pipefail

payload="$(cat)"
file_path="$(printf '%s' "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('file_path', data.get('path', '')))
" 2>/dev/null || true)"

if [[ -z "$file_path" ]] || [[ "$file_path" != *.py ]]; then
  exit 0
fi

if command -v ruff >/dev/null 2>&1; then
  ruff format "$file_path" 2>/dev/null || true
fi

exit 0
