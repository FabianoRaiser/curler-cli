#!/usr/bin/env bash
# beforeShellExecution: bloqueia comandos destrutivos por política do projeto.
# Exit 0 = permite. Exit 2 = nega.
set -euo pipefail

payload="$(cat)"
command="$(printf '%s' "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('command', ''))
" 2>/dev/null || true)"

if printf '%s' "$command" | grep -Eq 'rm[[:space:]]+-rf|git[[:space:]]+push.*--force'; then
  echo "Comando bloqueado pela política do projeto: $command" >&2
  exit 2
fi

exit 0
