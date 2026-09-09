#!/usr/bin/env python3
"""Certificate 2: the exact good-frame adjoints H1, H2 satisfy the
band law and reconstruct polynomial weighted-42 adjoints.

Inputs: data/M23_H1_integer_v91.txt, data/M23_H2_integer_v91.txt
(exact integer polynomials in (t, v)).

Verifies, exactly over Z:
  A. Bidegrees: deg_v <= 21, deg_t <= 6.
  B. Seven-band support: writing H = sum_s q^s P_{18+s}(v)
     + t * sum_s q^s Q_{18+s}(v) with q = t^2+23, the band caps hold:
     deg P18<=4, P19<=10, P20<=15, P21<=21; Q18<=4, Q19<=10, Q20<=15;
     and no further q-digits appear.
  C. Reconstruction h_j = q^(18-j) * c_j for j<=18 and c_j = q^(j-18) * h_j
     exactly for j>=19 (exact divisibility), giving polynomial u-form
     coefficients a_j(t) with deg_t a_j <= 42-2j and top degrees exactly
     [42,40,...,2,0] as recorded (ADJOINT_U_NUM_DEGREES).
  D. 484-slot support: every forbidden odd-triangle slot {k odd, j>=16}
     vanishes (15 slots). Note: the recorded H*_FLAT484 nonzero count 469
     refers to the pre-RREF kernel basis at p=100207139, which is
     generically dense; the exact good-frame vectors here are the q-pair
     pivot-normalized frame and may have incidental extra monomial zeros.
     The 85-slot q-pair sparsity is certified in cert3.
  E. Height report: max |coefficient| digit counts for H1, H2.
Marker: M23_PATCH_CERT2_PASS
"""
import pathlib
import sympy as sp

BASE = pathlib.Path(__file__).resolve().parent
T, V = sp.symbols('t v')
q = sp.Poly(T**2 + 23, T, domain=sp.ZZ)

def load(name):
    e = sp.sympify((BASE/'data'/name).read_text(), locals={'t': T, 'v': V})
    return sp.Poly(e, V, domain=sp.ZZ[T])

def qdigits(c):
    """q-adic digits of c(t) in Z[t]: list of (e, f) with digit e + f*t."""
    out = []
    c = sp.Poly(c, T, domain=sp.ZZ)
    while not c.is_zero:
        quo, rem = sp.div(c, q, domain=sp.QQ)
        rem = sp.Poly(rem, T, domain=sp.QQ)
        e = rem.nth(0); f = rem.nth(1) if rem.degree() >= 1 else 0
        assert e == int(e) and f == int(f)
        out.append((int(e), int(f)))
        c = sp.Poly(quo, T, domain=sp.QQ)
    return out

ok_all = True
for name in ('M23_H1_integer_v91.txt', 'M23_H2_integer_v91.txt'):
    H = load(name)
    label = name.split('_')[1]
    # A
    degv = H.degree()
    degt = max(sp.Poly(H.nth(j), T).degree() for j in range(degv+1))
    assert degv <= 21 and degt <= 6, (degv, degt)
    print(f"{label} A: deg_v = {degv} <= 21, deg_t = {degt} <= 6: PASS")
    # B: band caps via q-digits of each v-coefficient
    caps_even = {0: 4, 1: 10, 2: 15, 3: 21}
    caps_odd = {0: 4, 1: 10, 2: 15}
    maxc = 0
    for j in range(degv+1):
        cj = sp.Poly(H.nth(j), T, domain=sp.ZZ)
        if cj.is_zero:
            continue
        maxc = max(maxc, max(abs(int(x)) for x in cj.all_coeffs()))
        for s, (e, f) in enumerate(qdigits(cj)):
            if e != 0:
                assert s in caps_even and j <= caps_even[s], \
                    (label, "even digit outside band", j, s)
            if f != 0:
                assert s in caps_odd and j <= caps_odd[s], \
                    (label, "odd digit outside band", j, s)
    print(f"{label} B: seven-band caps (4,10,15,21|4,10,15): PASS "
          f"(max |coeff| = {len(str(maxc))} digits)")
    # C: u-form reconstruction
    top_expected = list(range(42, -2, -2))
    a = []
    for j in range(22):
        cj = sp.Poly(H.nth(j) if j <= degv else 0, T, domain=sp.ZZ)
        if j <= 18:
            aj = cj * q**(18-j)
        else:
            quo, rem = sp.div(cj, q**(j-18), domain=sp.QQ)
            assert sp.Poly(rem, T).is_zero, (label, j, "not divisible")
            aj = sp.Poly(quo, T, domain=sp.ZZ)
        a.append(aj)
        assert aj.is_zero or aj.degree() <= 42-2*j, (label, j, aj.degree())
    tops = [aj.degree() if not aj.is_zero else -1 for aj in a]
    assert tops == top_expected[:22], tops
    print(f"{label} C: polynomial u-form, deg_t a_j = 42-2j exactly "
          f"(top degrees [42,40,...,0]): PASS")
    # D: 484-slot support
    nz = 0; zero_slots = []
    for j in range(22):
        co = a[j].all_coeffs()[::-1] if not a[j].is_zero else []
        for k in range(43-2*j):
            v = co[k] if k < len(co) else 0
            if v != 0:
                nz += 1
            else:
                zero_slots.append((j, k))
    forb = sorted((j, k) for j in range(16, 22)
                  for k in range(1, 43-2*j, 2))
    zs = set(zero_slots)
    assert set(forb) <= zs, "a forbidden slot is nonzero"
    extra = sorted(zs - set(forb))
    print(f"{label} D: all 15 forbidden odd-triangle slots vanish; "
          f"{nz}/484 nonzero ({len(extra)} incidental zeros beyond the "
          f"triangle): PASS")
print("M23_PATCH_CERT2_PASS")
