# Publication-facing certificate paths

This directory contains stable, version-neutral aliases and orchestration tools for the certificate sources and data cited in Section 10 of the article. The claim-to-certificate mapping and logical roles appear in `../../CERTIFICATE_INDEX.md`. Provenance copies remain in their source directories.

## Orchestration

- `run_python_checker.py` executes an individual checker in an isolated interpreter while preserving exit status and output.
- `run_fast_suite.py` runs the fast certificate components in isolated parallel workers and requires each terminal PASS marker.
- `run_all_suites.py` executes the four top-level suites sequentially and verifies the terminal marker from each suite.
- `exact_tetragonal/verify_compactified_fibers_parallel.py` performs the exact compactified-fiber comparison at all 1013 base values with an adjustable worker count.

## Stable proof and corroboration aliases

- `p31_checks/` and `regression_p31/`: C1 local inputs.
- `band_law/` and `exact_closure/`: C3 support and exact-adjoint checks.
- `exact_tetragonal/`: C4 exact data plus the resource-stable 1013-fiber runner used in C5.
- `frame_transition/`: C5 exact frame matrix and symmetric coefficient table.
- `ramification/`: C6 finite-field corroboration.
- `virgin_prime_spotcheck/` and `out_of_window_spotcheck/`: C7 adversarial corroboration.
