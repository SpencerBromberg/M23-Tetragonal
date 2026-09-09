#!/bin/sh
set -u

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export M23_IDENTITY_WORKERS=${M23_IDENTITY_WORKERS:-4}

TMPDIR_EXACT=$(mktemp -d "${TMPDIR:-/tmp}/m23-exact.XXXXXX")
trap 'rm -rf "$TMPDIR_EXACT"' EXIT HUP INT TERM

printf 'M23_EXACT_TETRAGONAL_SUITE_BEGIN\n'

# These exact checks are independent and run concurrently.  The identity
# worker count defaults to four and can be overridden by M23_IDENTITY_WORKERS.
(
  trap - EXIT HUP INT TERM
  python -u certificates/publication/exact_tetragonal/verify_compactified_fibers_parallel.py
) >"$TMPDIR_EXACT/fibers.log" 2>&1 &
PID_FIBERS=$!

(
  trap - EXIT HUP INT TERM
  cd certificates/exact_tetragonal_v93
  python verify_global_identity_parallel_v96.py
  python verify_global_identity_metadata_v93.py
) >"$TMPDIR_EXACT/identity.log" 2>&1 &
PID_IDENTITY=$!

STATUS=0
wait "$PID_FIBERS" || STATUS=1
wait "$PID_IDENTITY" || STATUS=1

printf '\n===== exhaustive compactified p=1013 fiber comparison =====\n'
cat "$TMPDIR_EXACT/fibers.log"
printf '\n===== 971-point exact characteristic-zero identity =====\n'
cat "$TMPDIR_EXACT/identity.log"

if [ "$STATUS" -ne 0 ]; then
  printf '\nM23_EXACT_TETRAGONAL_SUITE_FAIL\n' >&2
  exit 1
fi

printf '\nM23_EXACT_TETRAGONAL_SUITE_PASS\n'
