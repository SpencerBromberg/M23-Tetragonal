#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"

sha256sum -c SHA256SUMS
python - <<'PY'
from pathlib import Path
root = Path('.')
excluded = {'SHA256SUMS', 'MANIFEST.tsv'}
actual = sorted(p.as_posix() for p in root.rglob('*') if p.is_file() and p.as_posix() not in excluded)
manifest = []
for line in Path('MANIFEST.tsv').read_text().splitlines():
    if not line.strip():
        continue
    parts = line.split('\t')
    manifest.append(parts[-1])
if actual != manifest:
    missing = sorted(set(actual) - set(manifest))
    extra = sorted(set(manifest) - set(actual))
    raise SystemExit(f'MANIFEST_MISMATCH missing={missing} extra={extra}')
print(f'MANIFEST_PAYLOAD_FILES={len(actual)}')
print('MANIFEST_EXACT_MATCH=PASS')
PY
printf 'M23_TETRAGONAL_CHECKSUMS_PASS\n'
