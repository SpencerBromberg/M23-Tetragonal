#!/usr/bin/env python3
"""Characteristic-zero reconstruction attempt on canonical invariants.

Targets (all canonical in the fixed symmetric jet gauge, all produced by
verify_ramification_structure.py from the published tables alone):

  g0(W)  monic, degree 8  : W-coordinates of the 8 smooth double points of
                            the fiber of t over the third branch value T=0.
  h0(W)  monic, degree 7  : W-coordinates of the 7 unramified points of the
                            same fiber.
  B(W)   monic, degree 14 : branch values of the degree-4 map w in the
                            W-line (multiplicity-1 part of the binary-
                            quartic discriminant Delta_w).

Method per coefficient: CRT across the available training primes, Wang
rational reconstruction against the training modulus, then held-out
verification at p = 1013 (never in the CRT).  A projective (common-
denominator pivot) pass and a per-polynomial LLL lattice pass follow, so a
failure is reported at the same diagnostic depth as the 133-digit tests in
the main paper.

Note p = 31 supplies no clean B (a node collides with the T=0 fiber at 31),
so B uses the 20 large training primes; g0 and h0 use all 21.
"""
import json, math, pathlib
from functools import reduce

HERE = pathlib.Path(__file__).resolve().parent
CERT = json.loads((HERE.parent / "json" /
                   "ramification_structure_certificate.json").read_text())
reps = {r["prime"]: r for r in CERT["primes"]}
HOLD = 1013
TRAIN = sorted(p for p in reps if p != HOLD)

def crt(residues, primes):
    M = reduce(lambda a, b: a*b, primes)
    x = 0
    for r, p in zip(residues, primes):
        Mi = M // p
        x = (x + r * Mi * pow(Mi, -1, p)) % M
    return x, M

def wang_rr(a, m):
    a %= m
    B = math.isqrt(m // 2)
    r0, r1, s0, s1 = m, a, 0, 1
    while abs(r1) > B:
        q = r0 // r1
        r0, r1 = r1, r0 - q*r1
        s0, s1 = s1, s0 - q*s1
    n, d = r1, s1
    if d == 0:
        return None
    if d < 0:
        n, d = -n, -d
    if abs(n) <= B and d <= B and math.gcd(n, d) == 1 and (a*d - n) % m == 0:
        return n, d
    return None

def attempt(name, key, primes):
    primes = [p for p in primes if reps[p].get(key)]
    tables = {p: reps[p][key] for p in primes}
    deg = len(tables[primes[0]]) - 1
    hold = reps[HOLD][key]
    print(f"--- {name}: monic degree {deg}, training primes {len(primes)}, "
          f"modulus digits "
          f"{len(str(reduce(lambda a,b:a*b, primes)))}")
    results = []
    n_cand = n_pass = 0
    for i in range(deg):                      # skip monic leading coeff
        res = [tables[p][i] for p in primes]
        x, M = crt(res, primes)
        rr = wang_rr(x, M)
        entry = {"index": i}
        if rr:
            n, d = rr
            n_cand += 1
            ok = (n - d*hold[i]) % HOLD == 0
            if ok:
                n_pass += 1
            entry.update(numerator=str(n), denominator=str(d),
                         heldout_pass=ok,
                         num_digits=len(str(abs(n))),
                         den_digits=len(str(d)))
        else:
            entry.update(numerator=None)
        results.append(entry)
    print(f"    ordinary RR candidates: {n_cand}/{deg}, "
          f"held-out survivors: {n_pass}")

    # projective pass: common denominator via each invertible pivot
    proj_pass = []
    Mfull = reduce(lambda a, b: a*b, primes)
    resv = [crt([tables[p][i] for p in primes], primes)[0] for i in range(deg)]
    for piv in range(deg):
        if math.gcd(resv[piv], Mfull) != 1 or hold[piv] % HOLD == 0:
            continue
        inv = pow(resv[piv], -1, Mfull)
        recs = []
        complete = True
        for j in range(deg):
            if j == piv:
                continue
            rr = wang_rr(resv[j]*inv % Mfull, Mfull)
            if rr is None:
                complete = False
                break
            recs.append((j, rr))
        if not complete:
            continue
        ok = all((n*hold[piv] - d*hold[j]) % HOLD == 0 for j, (n, d) in recs)
        proj_pass.append({"pivot": piv, "heldout_pass": ok})
    npass = sum(1 for e in proj_pass if e["heldout_pass"])
    print(f"    projective candidates: {len(proj_pass)}, "
          f"held-out passing pivots: {npass}")

    # LLL pass: single lattice for (den, num_0..num_{deg-1}) mod Mfull
    lll = lll_block(resv, Mfull, hold, HOLD)
    print(f"    LLL: training-congruent rows {lll['training_rows']}, "
          f"held-out survivors {lll['heldout_survivors']}, "
          f"shortest den digits {lll['min_den_digits']}")
    return {"name": name, "degree": deg, "training_primes": primes,
            "coefficientwise": results,
            "ordinary_candidates": n_cand, "ordinary_heldout_pass": n_pass,
            "projective": proj_pass, "lll": lll}

def lll_block(resv, M, hold, p):
    """Lattice for a common-denominator vector (d, n_0..n_{k-1}) with
    n_i = d*resv[i] mod M, via sympy's LLL on the standard embedding."""
    from sympy import Matrix
    k = len(resv)
    rows = []
    rows.append([1] + [r % M for r in resv])
    for i in range(k):
        e = [0]*(k+1)
        e[i+1] = M
        rows.append(e)
    L = Matrix(rows)
    R = L.lll()
    train = 0
    surv = 0
    min_den = None
    for i in range(R.rows):
        v = list(R.row(i))
        d0, ns = int(v[0]), [int(x) for x in v[1:]]
        if d0 == 0:
            continue
        if all((d0*resv[j] - ns[j]) % M == 0 for j in range(k)):
            train += 1
            dd = len(str(abs(d0)))
            min_den = dd if min_den is None else min(min_den, dd)
            if d0 % p != 0 and all((ns[j] - d0*hold[j]) % p == 0
                                   for j in range(k)):
                surv += 1
    return {"training_rows": train, "heldout_survivors": surv,
            "min_den_digits": min_den}

def factorization_types(key, primes):
    """Degrees of irreducible factors of the monic target mod each prime:
    gauge-free Frobenius data for the branch-locus etale algebra."""
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location(
        "vrs", HERE / "verify_ramification_structure.py")
    vrs = importlib.util.module_from_spec(spec)
    sys.modules["vrs"] = vrs
    _main, vrs_main = None, None
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(vrs)
        except SystemExit:
            pass
    out = {}
    for p in primes:
        tab = reps[p].get(key)
        if not tab:
            continue
        fpol = [x % p for x in tab]
        # distinct-degree factorization over F_p
        ddf = []
        fcur = fpol[:]
        d = 0
        xq = [0, 1]
        while len(fcur) - 1 >= 1:
            d += 1
            if d > (len(fcur) - 1)//2:
                ddf.append((len(fcur)-1, len(fcur)-1 and 1))
                ddf[-1] = (d if False else len(fcur)-1, 1)
                ddf[-1] = ("deg", len(fcur)-1)
                break
            xq = vrs.powmod_poly(xq, p, fcur, p)
            g = vrs.pgcd(fcur, vrs.padd(xq, [0, p-1], p), p)
            if len(g) - 1 > 0:
                ddf.append((d, (len(g)-1)//d))
                fcur = vrs.poly_div(fcur, g, p)
                xq = vrs.pmod(xq, fcur, p) if len(fcur) > 1 else xq
        typ = []
        for item in ddf:
            if item[0] == "deg":
                typ.append(item[1])
            else:
                dd, cnt = item
                typ.extend([dd]*cnt)
        out[p] = sorted(typ)
    return out

def main():
    out = {"heldout_prime": HOLD, "targets": []}
    for name, key, primes in (
            ("g0 (double points over T=0)", "g0_monic", TRAIN),
            ("h0 (simple points over T=0)", "h0_monic", TRAIN),
            ("B (w-branch polynomial)", "w_branch_polynomial_monic", TRAIN)):
        out["targets"].append(attempt(name, key, primes))
    total_pass = sum(t["ordinary_heldout_pass"] for t in out["targets"])
    total_deg = sum(t["degree"] for t in out["targets"])
    print(f"TOTAL: {total_pass}/{total_deg} coefficients reconstructed "
          f"over Q and verified at held-out p={HOLD}")
    out["factorization_types"] = {
        key: {str(p): v for p, v in factorization_types(key, TRAIN+[HOLD]).items()}
        for key in ("g0_monic", "h0_monic", "w_branch_polynomial_monic")}
    (HERE.parent / "json" / "branch_locus_reconstruction.json").write_text(
        json.dumps(out, indent=1) + "\n")
    if total_pass == total_deg:
        print("M23_BRANCH_LOCUS_RECONSTRUCTION_PASS")
    elif total_pass > 0:
        print("M23_BRANCH_LOCUS_RECONSTRUCTION_PARTIAL")
    else:
        print("M23_BRANCH_LOCUS_RECONSTRUCTION_NEGATIVE")

if __name__ == "__main__":
    main()
