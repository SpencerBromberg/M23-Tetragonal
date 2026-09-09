#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
printf 'M23_BOUNDED_HEIGHT_SEARCH_BEGIN\n'
python certificates/lower_height_specialization/extracted/M23_better_polynomial_certificate/search_pgl2_height.py -B 8
printf 'M23_BOUNDED_HEIGHT_SEARCH_PASS\n'
