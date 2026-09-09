# Exact Tetragonal Coordinates for the Genus-4 M23 Quotient

[![Replay certificates](https://github.com/SpencerBromberg/M23-Tetragonal/actions/workflows/replay.yml/badge.svg)](https://github.com/SpencerBromberg/M23-Tetragonal/actions/workflows/replay.yml)

Spencer Harkness Bromberg and Alexander Xavier Bromberg

**Version of record:** Zenodo, DOI [10.5281/zenodo.22117162](https://doi.org/10.5281/zenodo.22117162)

This repository is a convenience mirror. `deposit/M23-Tetragonal/` is a byte-identical copy of the Zenodo deposit: the article, its LaTeX source, the certificate suite, and the recorded provenance and release history. Nothing in that directory is edited here; changes are made on Zenodo and then mirrored. The deposit was updated on 2026-09-09, so that replaying the certificate suite no longer alters any checksummed file, and to include the full license texts. Certificate results and article are unchanged; see the deposit's `CHANGELOG.md`.

A companion repository, [M23-Hurwitz](https://github.com/SpencerBromberg/M23-Hurwitz), mirrors the positive-dimensional paper (DOI [10.5281/zenodo.22010546](https://doi.org/10.5281/zenodo.22010546)).

| Git tag | Zenodo version |
|---|---|
| `zenodo-v1` | Version 1 (2026-08-26; files corrected 2026-09-09) |

## Verify the mirror against the deposit

```bash
cd deposit/M23-Tetragonal
sh VERIFY_CHECKSUMS.sh
```

This checks every file against `SHA256SUMS` and confirms the payload matches `MANIFEST.tsv` exactly, so an added or missing file is caught as well as a modified one.

## Replay the certificates

```bash
cd deposit/M23-Tetragonal
pip install -r requirements.txt
sh RUN_ALL_CERTIFICATES.sh
```

SymPy is the only dependency. The Magma and PARI/GP sources under `certificates/` are recorded inputs bound by SHA256, not executed, so no proprietary software is needed to replay the suite. Toolchain details are in `ENVIRONMENT.md`; the reviewer's route through the certificates is in `REVIEWER_GUIDE.md` and `CERTIFICATE_INDEX.md`.

Replaying does not modify the deposit, so `VERIFY_CHECKSUMS.sh` passes both before and after a run.

CI runs verification and then the full replay on every push (see the badge above).

## Citation

Use the DOI above, or the "Cite this repository" button (`CITATION.cff`).

## Licenses

- Article and original explanatory, review, and metadata documents: CC-BY-NC-ND-4.0
- Source code and executable scripts in `certificates/`, the top-level `RUN_*.sh`, and `VERIFY_CHECKSUMS.sh`: GPL-3.0-only
- Original computational data and recorded outputs: CC-BY-NC-4.0
- Files under `provenance/` (this project's own earlier release bundles, changelogs, and run logs) keep whatever license they carried when they were first released, rather than being relicensed by this deposit

No single license applies to every file. Full scope in `LICENSE.md`; license texts in `LICENSES/` and at the deposit root.

The third-party paper this work builds on (Huang, Jackson, Lee, Poonen, Pries, and Zhang, arXiv:2608.08538) is cited but not redistributed.
