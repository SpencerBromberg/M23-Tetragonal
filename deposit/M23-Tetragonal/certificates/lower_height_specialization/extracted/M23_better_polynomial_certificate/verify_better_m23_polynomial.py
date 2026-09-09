#!/usr/bin/env python3
"""Exact certificate for a lower coefficient-height defining polynomial
for the HJLPPZ Example 3.7 M23 number field.

No third-party Python packages are required.

Core identity:
    g(x) = f2(x + 1).
Thus if beta = alpha - 1, then Q(alpha)=Q(beta), and the two polynomials
have exactly the same splitting field over Q.

The script also verifies:
  * monicity and degree 23;
  * exact coefficient-height reduction;
  * optimality among all integer translations f2(x+k), -100 <= k <= 100;
  * irreducibility modulo 29 (hence over Q);
  * squarefree factorization modulo 5 into irreducibles of degrees 3,5,15.
"""
from math import comb, gcd

# Coefficients in ascending powers, x^0,...,x^23.
F2 = [
    1243077066,
    -11217790920,
    38754121124,
    -67357061907,
    63691532334,
    -26037806834,
    -5728074376,
    9451874955,
    -2463757240,
    83587888,
    -436105484,
    320807726,
    -71999476,
    17344116,
    -9392096,
    2223732,
    -361974,
    127420,
    -21620,
    1679,
    -598,
    46,
    0,
    1,
]

G = [
    242325562,
    60455178,
    -983586582,
    -482357150,
    727883760,
    1165914252,
    -435568756,
    -1207282236,
    1938799398,
    229352458,
    -727073654,
    -221821982,
    63064206,
    44362906,
    3526406,
    -3657782,
    -1592842,
    -280094,
    -8510,
    8234,
    2139,
    299,
    23,
    1,
]


def trim(a):
    a = a[:]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b, p=None):
    n = max(len(a), len(b))
    c = [0] * n
    for i in range(n):
        c[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
        if p is not None:
            c[i] %= p
    return trim(c)


def sub(a, b, p):
    n = max(len(a), len(b))
    c = [0] * n
    for i in range(n):
        c[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(c)


def mul(a, b, p=None):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
            if p is not None:
                c[i + j] %= p
    return trim(c)


def divmod_poly(a, b, p):
    a = [x % p for x in trim(a)]
    b = [x % p for x in trim(b)]
    assert b != [0]
    q = [0] * max(1, len(a) - len(b) + 1)
    inv_lc = pow(b[-1], -1, p)
    while len(a) >= len(b) and a != [0]:
        k = len(a) - len(b)
        t = a[-1] * inv_lc % p
        q[k] = t
        for j in range(len(b)):
            a[j + k] = (a[j + k] - t * b[j]) % p
        a = trim(a)
    return trim(q), trim(a)


def mod_poly(a, m, p):
    return divmod_poly(a, m, p)[1]


def mulmod(a, b, m, p):
    return mod_poly(mul(a, b, p), m, p)


def powmod_poly(a, e, m, p):
    r = [1]
    b = mod_poly(a, m, p)
    while e:
        if e & 1:
            r = mulmod(r, b, m, p)
        b = mulmod(b, b, m, p)
        e >>= 1
    return r


def monic(a, p):
    a = trim([x % p for x in a])
    inv = pow(a[-1], -1, p)
    return [(x * inv) % p for x in a]


def gcd_poly(a, b, p):
    a = trim([x % p for x in a])
    b = trim([x % p for x in b])
    while b != [0]:
        _, r = divmod_poly(a, b, p)
        a, b = b, r
    return monic(a, p)


def prime_divisors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def irreducible_mod_p(f, p):
    f = monic(f, p)
    n = len(f) - 1
    x = [0, 1]
    # Frobenius ladder x^(p^k) mod f.
    xp = x
    frob = {0: x}
    for k in range(1, n + 1):
        xp = powmod_poly(xp, p, f, p)
        frob[k] = xp
    if trim(sub(frob[n], x, p)) != [0]:
        return False
    for q in prime_divisors(n):
        h = gcd_poly(f, sub(frob[n // q], x, p), p)
        if len(h) != 1:
            return False
    return True


def shift_poly(f, k):
    # f(x+k), ascending coefficients.
    n = len(f) - 1
    out = [0] * (n + 1)
    for i, ai in enumerate(f):
        if ai == 0:
            continue
        for j in range(i + 1):
            out[j] += ai * comb(i, j) * (k ** (i - j))
    return trim(out)


def height(f):
    return max(abs(c) for c in f)


def digit_sum(f):
    return sum(len(str(abs(c))) for c in f if c)


def l1(f):
    return sum(abs(c) for c in f)


def fmt_poly(f, var="x"):
    terms = []
    for i in range(len(f) - 1, -1, -1):
        c = f[i]
        if not c:
            continue
        sign = "-" if c < 0 else "+"
        a = abs(c)
        if i == 0:
            core = str(a)
        elif i == 1:
            core = var if a == 1 else f"{a}*{var}"
        else:
            core = f"{var}^{i}" if a == 1 else f"{a}*{var}^{i}"
        if not terms:
            terms.append(("-" if c < 0 else "") + core)
        else:
            terms.append(f" {sign} {core}")
    return "".join(terms)


def main():
    assert len(F2) == 24 and F2[-1] == 1
    assert len(G) == 24 and G[-1] == 1

    computed = shift_poly(F2, 1)
    assert computed == G, "translation identity failed"

    hf = height(F2)
    hg = height(G)
    assert hg < hf

    best = None
    for k in range(-100, 101):
        h = height(shift_poly(F2, k))
        row = (h, digit_sum(shift_poly(F2, k)), l1(shift_poly(F2, k)), k)
        if best is None or row < best:
            best = row
    assert best[3] == 1 and best[0] == hg

    # p=29: the full degree-23 reduction is irreducible.
    assert irreducible_mod_p(G, 29)

    # p=5: exact factorization into distinct irreducibles of degrees 3,5,15.
    q3 = [-2, -2, 0, 1]  # x^3 - 2x - 2
    q5 = [-1, 0, -2, 2, -1, 1]
    q15 = [
        1, -2, -1, -2, -1, 2, -2, 2, 0, -2, -2, -2, -1, -2, -1, 1
    ]
    prod = mul(mul(q3, q5, 5), q15, 5)
    assert monic(prod, 5) == monic(G, 5)
    assert irreducible_mod_p(q3, 5)
    assert irreducible_mod_p(q5, 5)
    assert irreducible_mod_p(q15, 5)
    # Distinct irreducible factors imply squarefree reduction at 5.

    print("M23 LOWER-HEIGHT POLYNOMIAL CERTIFICATE: PASS")
    print()
    print("Exact field identity: g(x) = f2(x + 1)")
    print("Root change: beta = alpha - 1, alpha = beta + 1")
    print("Therefore Q(alpha)=Q(beta), and the splitting fields are identical.")
    print()
    print(f"degree(f2) = {len(F2)-1}; degree(g) = {len(G)-1}")
    print(f"height(f2) = {hf}")
    print(f"height(g)  = {hg}")
    print(f"height reduction factor = {hf/hg:.12f}")
    print(f"digit-count metric: {digit_sum(F2)} -> {digit_sum(G)}")
    print(f"L1 coefficient norm: {l1(F2)} -> {l1(G)}")
    print("translation search [-100,100]: unique best k = 1")
    print("mod 29: irreducible degree 23")
    print("mod 5: irreducible factor degrees 3, 5, 15 (squarefree)")
    print("Frobenius cycle type at 5: (15)(5)(3), order 15")
    print()
    print("g(x) =")
    print(fmt_poly(G))


if __name__ == "__main__":
    main()
