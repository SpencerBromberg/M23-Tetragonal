#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
python3 certificates/global_fractional_linear_height/verify_global_fractional_linear_height.py
