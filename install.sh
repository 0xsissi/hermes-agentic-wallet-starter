#!/bin/sh
set -eu
task_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v node >/dev/null 2>&1; then
  echo 'Install Node.js 24 LTS from https://nodejs.org/ first, then reopen your terminal.' >&2
  exit 1
fi
exec node "$task_dir/starter.mjs" install "$@"
