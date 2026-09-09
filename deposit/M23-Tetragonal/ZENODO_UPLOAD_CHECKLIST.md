# Zenodo upload checklist

## Upload exactly three top-level artifacts

1. `M23_exact_tetragonal_coordinates_v111.pdf` - primary readable manuscript.
2. `M23_exact_tetragonal_coordinates_v111.tex` - standalone manuscript source.
3. `M23_exact_tetragonal_coordinates_v111_2026-08-26.zip` - complete reproducibility archive.

The filename tag is retained only for local filing. The manuscript and Zenodo metadata contain no internal release-version label; the filenames may be changed immediately before deposit.

## Metadata

**Title:** Exact Tetragonal Coordinates for the Genus-4 M23 Quotient

**Description first line:** Symmetric Principal Parts, Exact Arithmetic Closure, and the Seven-Band Support Law

**Creators:** Spencer Harkness Bromberg; Alexander Xavier Bromberg

**Publication date:** 2026-08-26

**Resource type:** Publication / preprint

**DOI:** 10.5281/zenodo.22117162

**Record-level Version:** `1.0` (Zenodo metadata/UI only; the manuscript remains version-free)

**Referenced companion record:** 10.5281/zenodo.22010546 (`references`)

## License fields

Select all three applicable licenses explicitly:

- `CC-BY-NC-ND-4.0` - article and original documentation;
- `GPL-3.0-only` - executable source;
- `CC-BY-NC-4.0` - original computational data and outputs.

`provenance/` retains the license status of the underlying materials; see `LICENSES.md`.

## Final deposit checks

- Confirm creator spelling and order.
- Upload the TeX, PDF, and ZIP from the same final build.
- Preserve the DOI in `CITATION.cff` under root-level `identifiers:`.
- Preserve the companion DOI in the CFF `references:` list and Zenodo related identifiers.
- Add the final `SHA256(SHA256SUMS)` value supplied with the release handoff to the Zenodo description. The digest is intentionally kept outside the checksummed archive to avoid self-reference.
