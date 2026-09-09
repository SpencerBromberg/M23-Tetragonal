# M23 symmetric two-point frame checkpoint v41

Current result
--------------
The trace/skew-trace two-point jet normalization passed at

    31, 1000003, 1008001, 1022201

with:
- symmetric jet rank 4;
- a 2-dimensional kernel equal to L(K-(b'+c'));
- degree 23 minimal polynomial;
- bidegree (23,4) relation.

The four-prime CRT modulus is

    31941864361536608693

(20 decimal digits).

A three-prime coefficientwise rational reconstruction produced 77 formal
candidates. The fourth prime 1022201 kills every one except the forced
normalizing coefficient 1. This is useful: it shows the frame is coherent,
but the modulus is still too small for naive coefficientwise reconstruction.

Next run
--------
Run the files in `magma/` beginning with:

    M23_Magma_SymmetricTwoPointFrame_p1028201_v41.m

Treat p=1028201 as the next held-out prime. If it passes rank 4 and bidegree
(23,4), record SYMMETRIC_FLAT120. Then extend the CRT and repeat the held-out
test. Continue through the supplied palindromic split-prime ladder only until
a projective/rational candidate stabilizes; do not add primes merely for size.

Mathematical status
-------------------
The normalization is designed over Q: for conjugate local jet coefficients
a_l(b), a_l(c) and roots s_b,s_c of t^2+23, the trace and divided-skew-trace

    A_l = (a_l(b)+a_l(c))/2
    B_l = (a_l(b)-a_l(c))/(s_b-s_c)

are invariant under the quadratic conjugation. The first pair A_0,B_0 gives
the two vanishing conditions defining L(K-(b'+c')); A_1,B_1 completes the
four-dimensional canonical frame.

No characteristic-zero degree-(23,4) polynomial is asserted at this checkpoint.
