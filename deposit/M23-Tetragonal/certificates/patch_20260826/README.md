# Integrated 2026-08-26 patch certificates

This directory incorporates the useful computational parts of `M23_patch_bundle_2026-08-26.zip`.
The original uploaded bundle is retained verbatim under `provenance/`.

Integrated status boundaries:

- `verify_ramification_structure.py` certifies modular factorization and ramification patterns across the 21 training primes plus held-out p=1013. The even degree-124 discriminant residual is recorded as a genus-4 consistency check. The script does not promote a finite set of modular identities to characteristic-zero identities by itself.
- The exact characteristic-zero identity `w(P)t(P)=1` is proved in the article directly from the symmetric first-jet normalization. The 22-prime audit independently confirms its reductions.
- `branch_locus_reconstruction.py` is a certified negative reconstruction attempt at the current modulus: 0/29 coefficients survive p=1013. The LLL denominator scale is diagnostic, not a rigorous lower bound for the true coefficient height.
- `verify_null_model.py` supplies a statistical baseline for Wang rational-reconstruction candidate counts.
- `verify_specialization_units.py` verifies the unit, split-prime, integrality, and determinant data used in the article's good-reduction argument. The scheme-theoretic specialization step is supplied in the article using the tame good-reduction model at p=31.
- `verify_heldout_p1013_v2.py` parses the held-out table from the recorded Magma log and cross-checks the original validator.

Run from the package root:

```sh
python certificates/patch_20260826/scripts/verify_specialization_units.py
python certificates/patch_20260826/scripts/verify_ramification_structure.py
python certificates/patch_20260826/scripts/branch_locus_reconstruction.py
python certificates/patch_20260826/scripts/verify_null_model.py
python certificates/patch_20260826/scripts/verify_heldout_p1013_v2.py
```
