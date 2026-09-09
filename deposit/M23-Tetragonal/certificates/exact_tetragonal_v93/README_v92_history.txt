M23 exact tetragonal coefficient closure, v92

WHY V91 TIMED OUT
V91 reached H1_DEG_V=H2_DEG_V=21 and then entered Magma MinimalPolynomial(zeta) in a degree-23 function field. That general-purpose operation is the bottleneck.

V92 RECONSTRUCTION
The exact good-frame adjoints define a bidegree-(4,23) relation with 120 coefficients. For each finite-field prime, six ordinary t-specializations give 138 linear constraints on those 120 projective coefficients. The modular constraint matrix has rank 119, hence one projective relation.

Using 42 primes near 10^9, the CRT modulus reaches 379 decimal digits. Classical rational reconstruction recovers all 120 normalized coefficients. The reconstructed vector passes independent held-out reductions at p=1000003, p=1008001, and p=1013. Clearing denominators gives a primitive integer coefficient vector with gcd 1, all 120 entries nonzero, exact degrees deg_T=4 and deg_W=23, and maximum coefficient size 189 digits.

EXACT CLOSURE
Let R(T,W)=sum A_k(T)W^k be the reconstructed primitive polynomial and let h1,h2 be the exact good-frame adjoints in the integral model G(t,u)=0. The six exact integer specializations t=0,...,5 verify

  sum_k A_k(t) h1(t,u)^k h2(t,u)^(23-k) == 0 mod G(t,u).

These are 138 exact integer linear constraints on the 120 coefficient slots. Reduction of the same direct constraint matrix modulo 1000003 has rank 119. Therefore its rational rank is at least 119. The already-proved characteristic-zero bidegree-(4,23) theorem supplies a nonzero rational relation, so the rational rank is at most 119. Hence the kernel is exactly one-dimensional. The reconstructed nonzero vector lies in that kernel, so it is the unique characteristic-zero tetragonal relation up to scalar. Primitive normalization fixes the scalar.

CERTIFIED OUTPUT
  exact characteristic-zero coefficient table: CLOSED
  primitive relation degree in T: 4
  primitive relation degree in W: 23
  term count: 120
  coefficient gcd: 1

Run either:
  python M23_tetragonal_exact_kernel_certificate_v92.py
or
  Magma M23_tetragonal_exact_kernel_v92.m

The Python certificate has been executed successfully in the preparation environment.
