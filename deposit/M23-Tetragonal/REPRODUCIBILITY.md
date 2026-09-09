# Reproducibility guide

## Environment

Python 3.10 or later is recommended. SymPy 1.14.0 is pinned in `requirements.txt`. The tested environment appears in `ENVIRONMENT.md`.

```sh
python -m pip install -r requirements.txt
```

## C1-C7: tetragonal and corroborating suites

```sh
./RUN_FAST_CERTIFICATES.sh
```

Expected marker:

```text
M23_TETRAGONAL_FAST_SUITE_PASS
```

The fast suite checks the local inputs at 31, specialization units, finite-field tables, the q-pair frame, the seven-band lattice and exact adjoints, the six-slice kernel, the exact frame transition, ramification bookkeeping, virgin-prime and out-of-window adversarial checks, and the strict height-reduction arithmetic check.  It runs independent checkers in isolated parallel workers, requires a zero exit status and each checker's terminal PASS marker, and accepts `M23_FAST_WORKERS` as an optional positive worker-count override.

```sh
./RUN_EXACT_TETRAGONAL.sh
```

Expected marker:

```text
M23_EXACT_TETRAGONAL_SUITE_PASS
```

The exact suite runs the exhaustive compactified fiber comparison at all 1013 base values and the 971-point characteristic-zero remainder identity, followed by the degree-970 metadata check. The identity evaluator defaults to four workers and can be changed with `M23_IDENTITY_WORKERS`. The compactified-fiber sweep accepts `M23_FIBER_WORKERS`; the default is eight, capped by the available CPU count.

## C8: global height minimality

```sh
./RUN_GLOBAL_HEIGHT_MINIMALITY.sh
```

Expected final marker:

```text
M23_GLOBAL_PGL2Q_HEIGHT_MINIMALITY_PASS
```

This exact verifier proves the unique translate minimum, the global integral-unimodular minimum, the determinant cutoff `|det M| in {1,2}`, and the determinant-2 exhaustion. No floating-point approximation determines a retained pass/fail decision.

## C9: bounded diagnostic

```sh
./RUN_BOUNDED_HEIGHT_SEARCH.sh
```

This independently checks 37,296 normalized degree-23 transforms with matrix sup-norm at most 8. It is not used to prove the global theorem.

## Complete run

The aggregate runner executes the four suites sequentially and accepts `M23_ALL_SUITE_TIMEOUT` as an optional per-suite timeout in seconds.

```sh
./RUN_ALL_CERTIFICATES.sh
```

Expected final marker:

```text
M23_TETRAGONAL_CERTIFICATE_SUITE_PASS
```

## Discovery, proof, and corroboration

- C2: the 15-prime q-pair CRT and 42-prime kernel CRT discover candidates.
- C4: the degree bound and 971 exact remainders prove the arithmetic relation over `Q`.
- C5: the characteristic-zero principal-part calculation proves the frame transition.
- C6-C7: finite-field, fresh-prime, and out-of-window calculations corroborate the exact results.
- C8: exact interval, determinant/content, and finite enumeration calculations prove the global height statements.
- C9: the bounded matrix search is diagnostic only.

## Magma sources

The archive supplies the finite-field Riemann-Roch and characteristic-polynomial generators as Magma sources together with recorded outputs. Magma is not required for the final Python exact identity and height proofs; reviewers with Magma can replay the generation sources independently.

## Integrity

```sh
./VERIFY_CHECKSUMS.sh
```

`SHA256SUMS` covers every payload file except itself and `MANIFEST.tsv`. The manifest records every payload file except those two self-referential index files. The script also verifies exact manifest membership.
