# Certificate index

The manuscript separates mathematical arguments from implementation details. The identifiers C1-C9 match Section 10 of the article. Each entry states the logical role of the computation, the manuscript result it supports, the principal executable, and the expected success marker.

| ID | Role | Manuscript result | Principal executable or data | Expected marker / recorded output |
|---|---|---|---|---|
| C1 | Proof-bearing | Lemma 3.1 (smooth proper model at 31) and Proposition 3.3 (nondegenerate first-jet frame) | `certificates/good_reduction_p31/verify_good_reduction_inputs.py`; `certificates/publication/p31_checks/verify_specialization_units.py`; Magma source in `certificates/publication/regression_p31/` | `M23_P31_GOOD_REDUCTION_INPUTS_PASS`; `M23_SPECIALIZATION_UNITS_VERIFY_PASS`; `P31_SCHEME_CLOSURE_EXECUTION.log` |
| C2 | Discovery and finite-field validation | Section 4 and the arithmetic-frame candidate construction | `certificates/current_21prime/verify_symmetric_crt21.py`; `certificates/heldout_p1013/verify_heldout_p1013.py`; `certificates/common_denominator_133/verify_common_denominator_133.py`; `certificates/qpair_goodframe_v93/verify_qpair_goodframe_v93.py` | `M23_SYMMETRIC_CRT21_VERIFY_PASS`; `M23_HELDOUT_P1013_VERIFY_PASS`; `M23_COMMON_DENOMINATOR_133_VERIFY_PASS`; `M23_QPAIR_GOODFRAME_V93_PASS` |
| C3 | Proof-bearing | Proposition 7.1 and Corollary 7.3 (seven-band support and exact support plane) | `certificates/publication/band_law/verify_band_law_ceiling.py`; `certificates/publication/exact_closure/cert1_forbidden_triangle_lattice.py`; `certificates/publication/exact_closure/cert2_exact_adjoints_band_law.py` | `M23_BAND_LAW_NUMERIC_PASS`; `M23_PATCH_CERT1_PASS`; `M23_PATCH_CERT2_PASS` |
| C4 | Proof-bearing, with independent uniqueness check | Theorem 8.1 and Proposition 8.4 (exact arithmetic relation and six-slice uniqueness) | `RUN_EXACT_TETRAGONAL.sh`; `certificates/exact_tetragonal_v93/verify_global_identity_parallel_v96.py`; `certificates/exact_tetragonal_v93/verify_global_identity_metadata_v93.py`; `certificates/exact_tetragonal_v93/M23_tetragonal_exact_kernel_certificate_v92.py` | `M23_EXACT_TETRAGONAL_SUITE_PASS`; `M23_TETRAGONAL_GLOBAL_IDENTITY_V96_PASS`; `M23_TETRAGONAL_GLOBAL_IDENTITY_METADATA_V93_PASS`; `M23_TETRAGONAL_EXACT_KERNEL_V92_PASS` |
| C5 | Proof-bearing frame calculation; corroborative reductions | Proposition 3.5 and Theorem 8.2 (two-point values and exact frame transition) | `certificates/publication/frame_transition/verify_exact_frame_transition.py`; `certificates/frame_transition_v95/cert6_frame_transition_p1013.py`; `certificates/publication/exact_tetragonal/verify_compactified_fibers_parallel.py` | `M23_EXACT_FRAME_TRANSITION_V94_PASS`; `M23_PATCH_CERT6_PASS`; compactified-fiber runner marker `M23_PATCH_CERT5_PASS` |
| C6 | Corroborative only | Proposition 3.5 and Theorem 3.6 (two-point normalization, branch profile, and geometric bidegree) | `certificates/publication/ramification/verify_ramification_structure.py` | `M23_RAMIFICATION_STRUCTURE_VERIFY_PASS`; recorded JSON in `certificates/publication/json/` |
| C7 | Adversarial corroboration only | Theorems 8.1 and 8.2 | `certificates/publication/virgin_prime_spotcheck/verify_virgin_prime_spotcheck.py`; `certificates/publication/out_of_window_spotcheck/verify_out_of_window_spotcheck.py` | `M23_VIRGIN_PRIME_SPOTCHECK_PASS`; `M23_OUT_OF_WINDOW_SPOTCHECK_PASS` |
| C8 | Proof-bearing | Proposition A.1, Theorem A.2, Lemma A.3, and Theorem A.4 (global translate, unimodular, determinant-cutoff, and rational fractional-linear minima) | `certificates/global_height_minimality/verify_global_height_minimality.py`; `certificates/global_fractional_linear_height/verify_global_fractional_linear_height.py`; top-level `RUN_GLOBAL_HEIGHT_MINIMALITY.sh` | `M23_TRANSLATE_GLOBAL_PASS`; `M23_GL2Z_GLOBAL_HEIGHT_PASS`; `M23_GLOBAL_PGL2Q_HEIGHT_MINIMALITY_PASS` |
| C9 | Diagnostic only | Height-search context for Appendix A | `RUN_BOUNDED_HEIGHT_SEARCH.sh`; `certificates/lower_height_specialization/extracted/M23_better_polynomial_certificate/search_pgl2_height.py` | `PGL2 SEARCH CERTIFICATE: PASS`; `M23_BOUNDED_HEIGHT_SEARCH_PASS` |

## Corroborating outputs

- The exact frame transition reproduces all 120 transformed coefficients projectively at all 22 finite-field primes.
- The held-out prime 1013 recovers the inverse map `z=(546w+938)/(283w+1)` with projective ratio 732.
- The compactified degree-23 fiber comparison agrees at all 1013 base values over `F_1013`.
- The virgin-prime test uses split primes 1511 and 1531, absent from the reconstruction set, and passes 12/12 end-to-end checks.
- The out-of-window test passes 9/9 reductions at three large base values and three fresh primes.

These corroborating calculations do not replace the characteristic-zero arguments identified in C4 and C5.

## Orchestration

- `RUN_FAST_CERTIFICATES.sh` runs C1-C3, C5-C7, the six-slice check in C4, and the strict height-reduction arithmetic check.
- `RUN_EXACT_TETRAGONAL.sh` runs the 971-point characteristic-zero identity and the exhaustive 1013-fiber comparison in C4/C5.
- `RUN_GLOBAL_HEIGHT_MINIMALITY.sh` runs C8.
- `RUN_BOUNDED_HEIGHT_SEARCH.sh` runs C9.
- `RUN_ALL_CERTIFICATES.sh` runs all four suites sequentially with explicit exit-status and terminal-marker checks.
- `VERIFY_CHECKSUMS.sh` verifies every payload checksum and exact manifest membership.

## Resource-stable publication runners

- `certificates/publication/run_python_checker.py` executes one checker in an isolated interpreter and preserves its exit status.
- `certificates/publication/run_fast_suite.py` runs the fast components in isolated parallel workers and verifies every terminal marker.
- `certificates/publication/exact_tetragonal/verify_compactified_fibers_parallel.py` performs the exact 1013-fiber sweep with an adjustable worker count.
- `certificates/publication/run_all_suites.py` composes the four top-level suites and verifies the terminal marker from each suite.
