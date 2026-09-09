# Exact Tetragonal Coordinates for the Genus-4 M23 Quotient

**DOI:** `10.5281/zenodo.22117162`

## Article

- `article/M23_exact_tetragonal_coordinates.pdf`
- `article/M23_exact_tetragonal_coordinates.tex`

The article gives exact degree-4 coordinates on the genus-4 quotient in the regular M23 construction of Huang, Jackson, Lee, Poonen, Pries, and Zhang. It constructs a symmetric principal-part coordinate, a compact arithmetic coordinate, a primitive bidegree-(4,23) equation, an exact rational frame transition, and the seven-band support theorem governing the adjoint plane. The support-polygon corollary extracts the corresponding prime-degree mechanism.

Appendix A is logically separate. It proves that the translated Example 3.7 polynomial uniquely minimizes ordinary height among all integral translates and globally minimizes height over the full rational fractional-linear `PGL_2(Q)` orbit. Arbitrary primitive generators outside that orbit remain outside the claim.

## Main results

- `V=L(div(dt)-b'-c')` has dimension 2, is base-point free, and every basis ratio has degree 4.
- The normalization over `Z_31` is smooth and proper; the two ramified sections and the relative parameters `pi_+`, `pi_-` extend integrally.
- The symmetric coordinate satisfies `w(P)t(P)=1` at both conjugate totally ramified points.
- The map `(t,w)` has bidegree `(4,23)`.
- The ceiling `m_j >= ceil((397-19j)/23)` forces a `q^18` factor, seven support bands, and a 15-slot forbidden odd triangle.
- Primitive integer adjoints `H1,H2` define `z=H1/H2` and a primitive 120-term equation `R(T,Z)` of bidegree `(4,23)`.
- A degree-970 remainder bound and 971 exact evaluations prove `R(t,z)=0` over `Q`.
- An exact matrix with 148-150 digit entries gives `w=(Az+B)/(Cz+D)` and the primitive symmetric equation.
- All 120 transformed coefficients agree projectively at all 22 finite-field primes; the held-out prime 1013 supplies independent inverse-frame and compactified-fiber checks.
- Appendix A proves the global translate, unimodular, determinant-cutoff, and full rational fractional-linear height statements.

## Certificate organization

Section 10 of the article and `CERTIFICATE_INDEX.md` use identifiers C1-C9. Each computation is classified as proof-bearing, corroborative, discovery-only, or diagnostic. Mathematical proofs contain the mathematical argument; implementation paths and success markers are collected in the certificate map.

## Reviewer entry points

- `REVIEWER_GUIDE.md` - recommended reading order and logical boundaries.
- `CERTIFICATE_INDEX.md` - C1-C9 claim-to-certificate map.
- `CLAIM_STATUS.md` - exact scope of each headline claim.
- `REPRODUCIBILITY.md` and `ENVIRONMENT.md` - execution details.
- `PUBLICATION_REVIEW.md` and `FINAL_AUDIT.md` - final critical assessment and package audit.
- `LICENSES.md` - mixed-license scope.
- `GPL-3.0-only.txt`, `CC-BY-NC-ND-4.0.txt`, `CC-BY-NC-4.0.txt` - full license texts.

## Verification

Install the pinned Python dependency:

```sh
python -m pip install -r requirements.txt
```

Run the principal suites. The fast and exact runners use isolated resource-stable workers; `REPRODUCIBILITY.md` documents the optional worker-count controls:

```sh
./RUN_FAST_CERTIFICATES.sh
./RUN_EXACT_TETRAGONAL.sh
./RUN_GLOBAL_HEIGHT_MINIMALITY.sh
```

Run the independent bounded diagnostic:

```sh
./RUN_BOUNDED_HEIGHT_SEARCH.sh
```

Run every suite:

```sh
./RUN_ALL_CERTIFICATES.sh
```

Verify archive integrity:

```sh
./VERIFY_CHECKSUMS.sh
```
