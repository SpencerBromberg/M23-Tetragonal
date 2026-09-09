# Lower-height polynomial for the HJLPPZ Example 3.7 M23 field

This supplement records a strict coefficient-height improvement of the second explicit degree-23 polynomial in Huang-Jackson-Lee-Poonen-Pries-Zhang, *The Mathieu group M23 is a Galois group over Q* (arXiv:2608.08538v1, Example 3.7).

Let `f2` denote their Example 3.7 polynomial and put `g(x)=f2(x+1)`. Equivalently, if `alpha` is a root of `f2`, use the generator `beta=alpha-1`. Then `alpha=beta+1`, so the degree-23 fields and their splitting fields are exactly equal. The published Magma certification of the splitting field of `f2` as an M23-extension therefore transfers immediately to `g`.

The improved polynomial is

```
x^23 + 23*x^22 + 299*x^21 + 2139*x^20 + 8234*x^19 - 8510*x^18
- 280094*x^17 - 1592842*x^16 - 3657782*x^15 + 3526406*x^14
+ 44362906*x^13 + 63064206*x^12 - 221821982*x^11 - 727073654*x^10
+ 229352458*x^9 + 1938799398*x^8 - 1207282236*x^7 - 435568756*x^6
+ 1165914252*x^5 + 727883760*x^4 - 482357150*x^3 - 983586582*x^2
+ 60455178*x + 242325562.
```

Using ordinary polynomial height `H(h)=max_i |a_i|`,

- `H(f2) = 67,357,061,907`
- `H(g)  = 1,938,799,398`
- reduction factor: about `34.741635455676`.

The exact Python verifier additionally proves that `g` is the best integer translate `f2(x+k)` for `-100 <= k <= 100`, is irreducible modulo 29, and factors modulo 5 into distinct irreducibles of degrees `3,5,15`. The bounded PGL2 search checks every primitive integer linear-fractional generator with matrix sup-norm at most 8 (37,296 degree-23 transforms) and finds the same `beta=alpha-1` transform as the minimum by coefficient height.

This is **not** a claim of global minimality among all defining polynomials for the number field. It is a certified strict improvement and a bounded optimality statement. Separately, Remark 3.4 of the HJLPPZ paper explains that their regular two-variable model can in principle be reconstructed using a degree-4 rational function instead of degree 8; that is a different and potentially stronger optimization problem.

## Run

```bash
python3 verify_better_m23_polynomial.py
python3 search_pgl2_height.py --bound 8
```

Optional independent systems:

```bash
gp -q better_m23_polynomial.gp
magma verify_magma.m
```

`verify_magma.m` follows the same `GaloisGroup` + `GaloisProof` certification pattern used by the authors' public `verify.m`. The Magma computation can be memory intensive; the field-equivalence certificate itself does not require rerunning it because `g(x)=f2(x+1)` is an exact invertible change of generator.

## Source

Huang, Jackson, Lee, Poonen, Pries, Zhang, arXiv:2608.08538v1 (2026), especially Remark 3.4 and Example 3.7. Public code: `shaowuz/m23isgalois` on GitHub.
