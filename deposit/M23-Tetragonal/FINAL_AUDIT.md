# Final mathematical, publication, and archive audit

## Mathematical claims

The manuscript establishes the following claims with the proof structure stated in the article and the C1-C9 certificate map.

- The genus-4 quotient carries an optimal degree-4 pencil over Q. The degree-1, degree-2, and degree-3 alternatives are excluded separately; the published HJLPPZ canonical-model and ruling-descent results are cited at the points where they enter.
- The normalization over `Z_31` is smooth and proper. The proof treats the vertical generic point by finite etaleness, the complement of the branch sections by purity, and the branch sections by tame local form. The two ramified points extend to disjoint sections with integral relative parameters.
- Cohomology and base change plus the invertible first-jet map produce the symmetric principal-part frame.
- The local valuations force the `q^18` factor, seven support bands, the 86-slot carrier, and the 15-slot forbidden odd triangle.
- A weighted-degree bound of 970 and 971 exact evaluations prove the primitive bidegree-(4,23) arithmetic relation in characteristic zero. A six-slice rank-119 calculation independently proves uniqueness.
- The local first-jet calculation derives the exact constant `PGL_2(Q)` transition and the primitive symmetric equation.
- The ramified-adjoint ceiling law and support-polygon corollary isolate the general mechanism behind the seven-band calculation.
- Appendix A proves global ordinary-height minimality for the Example 3.7 generator under all integer translates and the full rational fractional-linear orbit. The determinant/content argument reduces every height-competitive primitive matrix to determinant magnitude 1 or 2; Hutz-Stoll reduction handles determinant 1, and exact enumeration handles determinant 2.

The article does not claim a global minimum over arbitrary primitive generators outside the rational fractional-linear orbit, and the finite-field ramification audit does not claim a complete classification of every plane singularity.

## Computational logic

Section 10 separates computation from the mathematical body and assigns every retained calculation one of four roles:

- proof-bearing: C1, C3, C4, the characteristic-zero part of C5, and C8;
- discovery and validation: C2;
- corroborative: the modular parts of C5, C6, and C7;
- diagnostic: C9.

No modular agreement is used as a substitute for a characteristic-zero identity. The 15-prime and 42-prime calculations discover candidates; C4 proves the relation over Q. The 22-prime coefficient comparison, the exhaustive 1013-fiber sweep, the two virgin-prime tests, and the out-of-window evaluations are independent corroboration.

## Fresh execution results

The final source tree was tested with the publication-facing runners:

- `RUN_FAST_CERTIFICATES.sh`: PASS, including all 18 component markers;
- `RUN_EXACT_TETRAGONAL.sh`: PASS, including 971/971 exact zeros and 1013/1013 compactified-fiber matches;
- `RUN_GLOBAL_HEIGHT_MINIMALITY.sh`: PASS, including the global translate, unimodular, determinant-cutoff, and determinant-2 checks;
- `RUN_BOUNDED_HEIGHT_SEARCH.sh`: PASS, 37,296/37,296 diagnostic transforms;
- `VERIFY_CHECKSUMS.sh`: rerun after final manifest construction.

The optional Magma sources remain available for independent finite-field Riemann-Roch and table-generation replays. The publication claims are tied to the exact data, recorded outputs, and independently executable Python checks listed in `CERTIFICATE_INDEX.md`.

## Manuscript quality

- 21 pages; two-pass pdfTeX compilation with no warnings, unresolved references, overfull boxes, or underfull boxes.
- All labels are unique and every reference resolves.
- All 21 archive paths cited in the manuscript resolve.
- The article contains no internal filing-version label, draft marker, release-history narrative, first-person author narrative, or British spelling variant found by the final scans.
- Certificate paths and implementation mechanics appear only in Sections 10-11, outside the mathematical proofs.
- Running headers are absent; footers contain page numbers only; links and headings render in black.
- All fonts are embedded. Poppler and PDFium both render all 21 pages; visual inspection found no clipping, overlap, malformed glyph, or abnormal page break.

## Archive quality

The final archive inventory, checksum count, syntax checks, nested-ZIP checks, and clean-room results are recorded in `PACKAGE_QA.log`. Mixed-license scope is stated in `LICENSES.md`; the minted DOI and companion reference appear in `CITATION.cff` and `ZENODO_METADATA.json`.
