# Adjoint modular reconstruction route

These Magma scripts retain the modular computations developed after the 133-digit coefficient reconstruction stalled.

For the symmetric sections C1,C2 and the integral plane equation G(t,u)=0, set

    h_i = C_i * dG/du.

Reported successful runs establish the following modular structure.

- p=1013 and p=100207139: each section has a common v-basis denominator of degree 85 and cleared numerator degree 83; the quotient w has common v-basis denominator degree 88; the u-basis denominator staircase follows q^(j-ceil(4j/23)), q=t^2+23.
- p=100208161 repeats the full 83/85/88 pattern and staircase law.
- At all three generic primes, h1 and h2 are polynomial in t,u with u-degree 21 and weighted degree 42 for wt(t)=1, wt(u)=2. Equivalently, the coefficient of u^j has t-degree at most 42-2j.
- p=1013: gcd(h1,h2)=1.
- p=100207139 and p=100208161: each 484-slot adjoint table has 469 nonzero entries. At p=1013, h2 has 469 and h1 has 468, consistent with one accidental modular zero.
- p=31 retains polynomial adjoints and the weighted-degree-42 bound but exhibits additional degree cancellations and fails the generic common-denominator/staircase equality. It is retained as an exceptional structural regression prime rather than a coefficient-level reconstruction validator.

The scripts are replay sources. The full Magma stdout was supplied interactively during development; the package records the scripts and the article states only the compact structural conclusions above. A future archival pass should save fresh stdout logs beside these scripts.
