# Critical publication review

## Grade

**A+++ — ready for Zenodo publication and external mathematical peer review.**

This is a publication-readiness grade, not a substitute for independent journal refereeing.

## Referee assessment

The central theorem chain is coherent and appropriately attributed. The published HJLPPZ model supplies the coordinates and the cited gonality inputs. The manuscript then gives an independent exact construction of the tetragonal pencil, proves the seven-band support law from local valuations, proves the arithmetic equation in characteristic zero, derives the symmetric frame transition locally, and records modular computations only in their proper discovery or corroborative roles.

The scheme-theoretic argument at 31 is complete at the level expected in a research article: the model is explicitly constructed by normalization; vertical etaleness, purity, tame local structure, section separation, relative parameters, cohomology/base change, and the first-jet Nakayama argument are all stated. The exact-relation proof has a transparent polynomial degree bound and enough exact specializations to force the remainder to vanish. The degree and field-generation arguments are explicit.

Appendix A is logically independent of the tetragonal theorem and makes a genuine global statement. The Hutz-Stoll hypotheses are supplied by exact root disks and interval bounds; the determinant/content proof explains why only determinants 1 and 2 can compete; and the remaining matrices are enumerated exactly. The appendix also states the natural scope boundary for arbitrary primitive field generators.

## Adversarial checks

The audit attempted to break the argument at the following interfaces:

- good reduction versus a singular affine presentation at 31;
- modular reconstruction versus characteristic-zero proof;
- degree-970 remainder bound versus proof-window fitting;
- arithmetic versus symmetric coordinates at fresh primes;
- compactification at fibers meeting `W=infinity`;
- local content at the exceptional primes 2 and 23;
- determinant-2 column signs, nonprimitive columns, and primitive-part normalization;
- theorem numbering, archive paths, and certificate-role attribution.

No counterexample, unsupported inference, or hidden dependence was found. The finite-field singularity statements remain deliberately limited to the factorization and discriminant data actually certified.

## Presentation and reproducibility

The mathematical body is free of implementation paths and release-history commentary. Section 10 maps C1-C9 to the exact theorem or proposition supported and identifies each calculation as proof-bearing, discovery, corroborative, or diagnostic. Section 11 gives the executable entry points and archive-integrity procedure.

The resource-stable runners isolate symbolic computations, preserve exit status, require terminal PASS markers, and expose worker-count controls. Every constituent top-level suite passed freshly against the final source tree. The final PDF is typographically clean and the archive is self-contained.

## Recommendation

Submit without further mathematical expansion. Additional work on arbitrary primitive field generators would constitute a separate project rather than a necessary completion of this paper.
