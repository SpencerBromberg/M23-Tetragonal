# Scheme-theoretic good reduction at p=31

This note records the construction used in the manuscript's lemma **Smooth proper model at 31**.  It closes the specialization argument at the level of the normalized integral curve rather than treating good reduction as a black box.

## Construction

Let `R = Z_31`, `K = Q_31`, and `L = K(X)`.  Choose the Hensel lift `s in R` of `15 mod 31`, so `s^2 = -23`.  The three true branch values `0,+s,-s` define disjoint sections of `P^1_R`, because their pairwise differences are 31-adic units.

Define `X_R` as the normalization of `P^1_R` in `L`.  Since `P^1_R` is excellent, the normalization is finite, hence proper.  Its generic fiber is the given smooth projective curve `X_K`.

### No vertical ramification

Let `eta_31` be the generic point of the special fiber and `A0 = O_{P^1_R,eta_31}`.  This is a DVR with uniformizer `31` and residue field `F_31(t)`.  At `eta_31`, `q=t^2+23` is a unit, so `u=qv` is an invertible change of generator.  The integral `u`-equation is monic of degree 23, hence gives a finite free rank-23 `A0`-algebra `B0`.

The archive verifies irreducibility directly: at `t=7`, the reduction `G(7,U)` is irreducible of degree 23 over `F_31`.  If the monic polynomial `G` factored over `F_31(t)`, Gauss's lemma would give a factorization into monic positive-degree polynomials in `F_31[t][U]`; specializing `t=7` would preserve both positive `U`-degrees and contradict irreducibility.  Thus `G` is irreducible over `F_31(t)`.  Because `31` does not divide `23`, an irreducible polynomial of degree 23 in characteristic 31 cannot be inseparable; hence `B0/31B0` is a separable field of degree 23.  The verifier separately checks `gcd(G(7,U),dG(7,U)/dU)=1` as a specialization sanity check.  The reduction of `G_u` is nonzero in this field and therefore a unit; Nakayama makes `G_u` a unit in `B0`.  Consequently `B0/A0` is finite etale.  Since its fraction field is the degree-23 field `L`, `B0` is the integral closure of `A0` in `L`, proving that the normalization has no vertical ramification.  HJLPPZ Proposition 3.5 independently certifies the stronger arithmetic-monodromy statement `G_arith,31=M23` and tameness.

### Etale away from the true branch divisor

On the generic fiber the only branch values are `0,+s,-s`.  Hence every horizontal codimension-one point away from those sections is unramified, and the preceding paragraph handles the vertical codimension-one point.  The normalization is normal and the base is regular, so purity of the branch locus (Stacks Project, Tag `0BMB`) makes the normalization finite etale over the complement of the three branch sections.

The degree-84 factor occurring in the discriminant of the published plane equation does not create branch points of the normalized cover; HJLPPZ explicitly identify that factor with singularities of the plane presentation.  Purity therefore removes those apparent punctures automatically.

### Smoothness at the branch sections

The actual ramification indices are `2` over `t=0` and `23` over `t=+s,-s`, together with unramified points above `t=0`.  All indices are prime to 31.  Abhyankar's lemma for a regular divisor (Stacks Project, Tag `0EYG`) gives, etale locally on `P^1_R`, the standard form

`A[r]/(r^e - tau)`, with `e in {1,2,23}`,

where `tau` is a relative parameter cutting out the branch section.  Since the branch section is etale over `R`, `A` is etale over `R[tau]`; therefore the standard tame cover is etale over `R[r]` and hence smooth over `R`.  This proves that the normalization `X_R` is smooth and proper.

### The two ramified sections and the explicit uniformizers

Properness extends the two `K`-points above `t=+s,-s` uniquely to sections.  Their reductions are disjoint because `2s` is a unit.  In a tame local parameter `r_+` or `r_-`,

` t -/+ s = unit * r^23`.

The characteristic-zero model and the p=31 regression both give `ord(u)=19`; exact order 19 after reduction rules out a vertical factor in `u/r^19`, so

`u = unit * r^19`.

Therefore

`u^17/(t -/+ s)^14 = unit * r^(17*19 - 14*23) = unit * r`, 

and the manuscript's `pi_+`, `pi_-` are integral relative parameters with unit reductions.

## Cohomology/base change

For the smooth proper morphism `rho : X_R -> Spec R`, note first that `rho` is projective because `X_R -> P^1_R` is finite.  Set

`Lcal = omega_{X_R/R}(-P_+ - P_-)`.

The divisor formed by the two disjoint sections is relative effective Cartier, so `Lcal` is invertible and `R`-flat.  The generic fiber has `h^0=2`.  The p=31 differential computation gives canonical dimension 4 and two independent zeroth principal-part conditions, hence special-fiber `h^0=2`.  Hartshorne III.12.11 (constant-dimension cohomology and base change) therefore identifies `rho_* Lcal` with a free rank-2 `R`-module whose generic and special fibers are the desired Riemann-Roch spaces.  The first-jet map reduces to the recorded matrix with determinant `28 != 0 mod 31`; Nakayama then makes the integral first-jet map an isomorphism, and hence the characteristic-zero map is an isomorphism.

## Machine-checkable inputs

Run:

```sh
python certificates/good_reduction_p31/verify_good_reduction_inputs.py
```

The script checks Hensel splitting, branch-section separation, tameness, the Bezout exponent, binding to the exact p=31 Magma source by SHA256, the irreducible/separable `t=7` specialization, the `23/19` valuation assertions, the four-dimensional canonical computation, the two-dimensional twisted kernel, and the first-jet determinant.  The static record `good_reduction_p31_certificate.json` stores the source hash, specialized coefficient vector, and numerical invariants checked by the verifier.  It directly certifies vertical irreducibility/separability from the bundled equation by the irreducible specialization `t=7`; HJLPPZ Proposition 3.5 is retained as an independent stronger monodromy/tameness check rather than a load-bearing vertical-étaleness assumption.
