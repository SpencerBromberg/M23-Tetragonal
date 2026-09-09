# Global translate and unimodular height-minimality certificate

This directory certifies two appendix claims for the HJLPPZ Example 3.7 polynomial `f` and `g(x)=f(x+1)`.

## 1. All integer translates

The `x^20` coefficient of `f(x+k)` is

`C3(k) = 1771 k^3 + 966 k - 598`.

Its derivative is `5313 k^2 + 966 > 0`.  Exact endpoint evaluation excludes every `|k| >= 104`, and exact coefficient-height evaluation for `-104 <= k <= 104` gives the unique minimum

`H(g) = 1938799398`

at `k=1`.

## 2. Entire integral unimodular orbit

Let `Phi(X,Y)=Y^23 f(X/Y)` and `Gamma(X,Y)=Y^23 g(X/Y)`.
The proof uses Hutz--Stoll, *Acta Arith.* 189 (2019), Theorem 4.7, Proposition 4.3, and Remark 4.9 (DOI `10.4064/aa180618-9-12`).  Their maximum-norm bound gives a finite hyperbolic search region once lower bounds for the Julia invariant and root-direction separation are known.

The verifier establishes those inputs without floating-point decisions:

1. Twenty-three rational centers are supplied in `root_centers.json`.  Exact Taylor/Rouche inequalities on disks of radius `10^-10` prove that each disk contains exactly one root of `g`.  The disks are disjoint and certify `|alpha_i|<9` and pairwise separation `|alpha_i-alpha_j|>1/10`.
2. Exact rational interval arithmetic evaluates the gradient of `log R(Gamma,t+ui)` on a 64-piece subdivision of each side of `[-1,0] x [2,3]`.  Opposite components have strict opposite signs.  Poincare--Miranda gives a stationary point in the rectangle; uniqueness of the Julia covariant point identifies it with `z(Gamma)`.  Thus `-1<t<0` and `2<u<3`.
3. Pair separation gives `theta(Gamma)>20^-23`: at most one root lies within `1/20` of any horizontal coordinate, so simultaneously `R>=u^23` and `R>=400^-22 u^-21`; the maximum is minimized at `u=1/20`.
4. In normalized coordinates, the sphere half-angle formula plus the root and Julia-point bounds gives `eta>1/594050`, hence Proposition 4.3 allows `epsilon>1/(2*594050^22)`.
5. Remark 4.9 uses `||F|| <= (n+1) H_infty(F)^2 = 24 H_infty(F)^2`.  The exact integer inequality

   `(600000000)^21 > 2^23 * 24 * B^2 * 594050^22 * 20^23`

   makes `600000000` a valid Hutz--Stoll `cosh(distance)` cutoff for every transform with height at most `B`.
6. For `gamma=[[a,b],[c,d]]`,

   `cosh d(gamma^-1 z,i) = (|dz-b|^2+|a-cz|^2)/(2u) >= c^2+d^2`

   because `u>2`.  Therefore `|c|,|d|<=24494`.
7. `Gamma=Phi*T` with `T=[[1,1],[0,1]]`, and left multiplication by `T` leaves the bottom row unchanged.  Exact Sturm isolation of the seven real roots and six real critical points of `f` reduces the column inequalities `|Phi(a,c)|<=B` through denominator `24494` to four primitive columns up to simultaneous sign:

   `(1,0), (0,1), (1,1), (2,1)`.

8. Exact substitution of all 40 signed determinant `+/-1` column pairs finds no height below `B`.  Modulo overall sign, equality gives exactly four forms generated from `Gamma` by `X -> -X` and `X <-> Y`.

Matrices of determinant `-1` reduce to determinant `1` by a coordinate reflection, which preserves coefficient height.  Thus the result covers `GL_2(Z)` with determinant `+/-1`.

## Scope boundary

This certificate closes all integer translates and the full integral unimodular orbit.  The companion certificate in `certificates/global_fractional_linear_height/` extends the result to the full rational fractional-linear orbit.  Arbitrary primitive generators of the number field remain outside the claim.

Run:

```sh
python3 verify_global_height_minimality.py
```

Success markers:

- `M23_TRANSLATE_GLOBAL_PASS`
- `M23_SL2_GLOBAL_HEIGHT_PASS`
- `M23_GL2Z_GLOBAL_HEIGHT_PASS`
