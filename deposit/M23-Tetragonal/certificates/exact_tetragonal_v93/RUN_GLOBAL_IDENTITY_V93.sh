#!/bin/sh
set -eu
python verify_global_identity_chunk_v93.py -485 -364
python verify_global_identity_chunk_v93.py -364 -243
python verify_global_identity_chunk_v93.py -243 -122
python verify_global_identity_chunk_v93.py -122 -1
python verify_global_identity_chunk_v93.py -1 120
python verify_global_identity_chunk_v93.py 120 242
python verify_global_identity_chunk_v93.py 242 364
python verify_global_identity_chunk_v93.py 364 486
python verify_global_identity_metadata_v93.py
printf '%s\n' 'EXACT_ZERO_COUNT = 971'
printf '%s\n' 'GLOBAL_REMAINDER_IDENTICALLY_ZERO = true'
printf '%s\n' 'M23_TETRAGONAL_GLOBAL_IDENTITY_V93_PASS'
