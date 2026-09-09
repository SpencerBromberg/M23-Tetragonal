# Reviewer guide

## Reading path

1. Sections 2-3: the published model, the optimal degree-4 pencil, the smooth model at 31, and the symmetric principal-part normalization.
2. Sections 6-7: adjoint slot arithmetic and the geometric seven-band theorem.
3. Section 8: exact arithmetic closure, six-slice uniqueness, and the exact transition to the symmetric frame.
4. Section 9: the general ramified-adjoint ceiling and support-polygon corollary.
5. Section 10: the C1-C9 certificate map and the logical role of every computation.
6. Section 11: reproducibility and archive integrity.
7. Appendix A: global height minimality for all integral translates and the full rational fractional-linear `PGL_2(Q)` orbit.

## Logical spine

- HJLPPZ supplies the published genus-4 degree-23 model and the gonality lower bound used for optimality.
- At 31, the normalization of `P^1_{Z_31}` in `Q_31(X)` is smooth and proper: vertical finite etaleness handles the special-fiber generic point, purity handles the complement of the branch sections, and tame Abhyankar local form handles the branch sections.
- Cohomology and base change plus the nonzero special-fiber first-jet determinant gives the symmetric principal-part frame.
- Local valuations prove the seven-band support restriction before coefficient reconstruction.
- The 15-prime and 42-prime CRT calculations discover compact exact candidates.
- Characteristic-zero division and 971 exact evaluations prove the relation; a six-slice rank computation independently proves uniqueness after existence.
- A local characteristic-zero calculation derives the exact `PGL_2(Q)` frame transition.
- Appendix A combines Hutz-Stoll reduction theory, exact root and interval bounds, a local determinant/content argument, and finite enumeration to prove global height minimality over the rational fractional-linear orbit.

## Computation boundaries

- Modular agreement does not establish a characteristic-zero identity. C4 supplies the exact identity; C2 is discovery and validation.
- The 22-prime coefficient comparison, the 1013-fiber sweep, the virgin-prime test, and the out-of-window test are corroborative; they do not replace C4 or C5.
- The ramification audit verifies the recorded finite-field factorization and genus-consistency checks. It does not classify every singularity of every plane reduction.
- The bounded 37,296-matrix search is diagnostic C9. The global theorem rests on C8.
- The published HJLPPZ plane model, canonical model, gonality statement, and characteristic-zero branch data remain explicit external inputs.
- Global minimum height among arbitrary primitive field generators outside the rational fractional-linear orbit is not claimed.

## Commands

```sh
./RUN_FAST_CERTIFICATES.sh
./RUN_EXACT_TETRAGONAL.sh
./RUN_GLOBAL_HEIGHT_MINIMALITY.sh
./RUN_BOUNDED_HEIGHT_SEARCH.sh
./VERIFY_CHECKSUMS.sh
```

The exact identity runner defaults to four workers; set `M23_IDENTITY_WORKERS` to another positive integer when appropriate. See `CERTIFICATE_INDEX.md` for exact paths and success markers.
