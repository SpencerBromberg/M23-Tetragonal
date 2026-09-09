#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
TERM=${TERM:-xterm}
export TERM
exec python certificates/publication/run_fast_suite.py
