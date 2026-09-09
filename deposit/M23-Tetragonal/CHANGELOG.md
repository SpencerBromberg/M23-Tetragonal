# Publication changelog

This filing increment prepares the submission candidate without placing version language in the article.

- Separated all implementation paths and certificate mechanics from the mathematical body.
- Added Section 10, a C1-C9 map distinguishing proof-bearing, corroborative, discovery, and diagnostic computations and linking each family to the relevant result.
- Added Section 11 for reproducibility and archive integrity.
- Removed revision-history and supersession language from the article prose.
- Clarified the local Smith/content argument at 2 and 23 and the determinant-2 independent-sign enumeration.
- Recorded Zenodo record-level Version `1.0` in the deposit metadata while keeping the article version-free.
- Made the exact identity runner resource-stable with a four-worker default and an environment-variable override.
- Rebuilt and visually reviewed the article and reran the complete proof, corroboration, diagnostic, metadata, and checksum audits.

Numbered filing history remains under `provenance/release_history/`.

## Post-publication correction (2026-09-09)

- Removed the wall-clock `lll_seconds` field from `certificates/common_denominator_133/common_denominator_133.json` and the timing call in `certificates/common_denominator_133/verify_common_denominator_133.py` that produced it, so replaying the suite no longer rewrites a checksummed artifact and the deposit re-verifies after a replay. Recorded stdout, mathematical content, and every certificate outcome are unchanged.
- Added the full CC BY-NC-ND 4.0 and CC BY-NC 4.0 license texts at the package root alongside the GPL text; `LICENSES.md` and `README.md` now point to them.
- Clarified in `LICENSES.md` that `provenance/` holds this project's own earlier release bundles, changelogs, and run logs.
- Regenerated `SHA256SUMS` and `MANIFEST.tsv`.
