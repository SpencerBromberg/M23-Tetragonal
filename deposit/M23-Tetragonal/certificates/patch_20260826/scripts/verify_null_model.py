#!/usr/bin/env python3
"""Null-model certificate for the reconstruction statistics in Sections 5-6.

Claims certified:
  N1. For a uniformly random residue x mod M, Wang rational reconstruction
      with bound B = isqrt(M/2) succeeds with probability ~ 6/pi^2 = 0.6079
      bounded above by 6/pi^2 = 0.6079 (lattice-point count of the Wang
      acceptance region) and empirically ~0.586 on the actual 133-digit
      training modulus (the stopping rule loses a sliver at the
      |n|*d ~ M/2 boundary).  The paper's observed 68/120 = 0.567
      ordinary-RR candidate rate is statistically indistinguishable from
      this null (z ~ -0.4).
  N2. A noise candidate passes the held-out check at p=1013 with
      probability 1/1013; among ~68 candidates the expected number of false
      survivors is ~0.067, so the observed single forced survivor
      (index 0, the normalized coefficient 1) carries no evidential weight,
      exactly as the paper asserts.
Exit marker: M23_NULL_MODEL_VERIFY_PASS
"""
import json, math, pathlib, random
from functools import reduce

HERE = pathlib.Path(__file__).resolve().parent
def find(relp):
    for base in (HERE.parent / "package_root", HERE.parent, HERE.parents[2]):
        q = base / relp
        if q.exists():
            return q
    raise FileNotFoundError(relp)

crt = json.loads(find(
    "certificates/current_21prime/CRT120_symmetric_21primes.json").read_text())
PRIMES = sorted(map(int, crt["primes"]))
M = reduce(lambda a, b: a*b, PRIMES)
assert len(str(M)) == 133

def wang(a, m, B):
    a %= m
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
    return (n, d) if (abs(n) <= B and d <= B and math.gcd(n, d) == 1
                      and (a*d - n) % m == 0) else None

def main():
    B = math.isqrt(M // 2)
    rng = random.Random(23)
    N = 20000
    hits = 0
    false_surv = 0
    p_hold = 1013
    for _ in range(N):
        x = rng.randrange(M)
        rr = wang(x, M, B)
        if rr:
            hits += 1
            n, d = rr
            y = rng.randrange(p_hold)          # independent held-out residue
            if d % p_hold and (n - d*y) % p_hold == 0:
                false_surv += 1
    dens = hits / N
    approx = 6 / math.pi**2
    print(f"N1: Monte Carlo ({N} samples) RR-success density on the actual "
          f"133-digit M:")
    print(f"    observed {dens:.4f}; analytic upper bound 6/pi^2 = "
          f"{approx:.4f} (the Wang stopping rule loses a boundary sliver "
          f"near |n|*d ~ M/2, so the empirical null sits slightly below)")
    assert 0.55 < dens < approx + 0.01, "null density outside expected band"
    obs, tot = 68, 120
    z_paper = (obs/tot - dens)/math.sqrt(dens*(1-dens)/tot)
    print(f"    paper's 68/120 = {obs/tot:.4f} vs empirical null "
          f"{dens:.4f}: z = {z_paper:+.2f} "
          f"(|z|<2: statistically indistinguishable from noise): PASS")
    assert abs(z_paper) < 2
    rate = false_surv / max(hits, 1)
    print(f"N2: false-survivor rate at p=1013: observed {rate:.5f} "
          f"({false_surv}/{hits}), theory 1/1013 = {1/1013:.5f}")
    exp_ratio = rate * 1013
    assert 0.3 < exp_ratio < 3.0, "false-survivor rate off by >3x"
    print(f"    expected false survivors among 68 candidates: "
          f"{68/1013:.3f} -> the single forced survivor (normalized "
          f"coefficient) carries no evidential weight: PASS")
    print("M23_NULL_MODEL_VERIFY_PASS")

if __name__ == "__main__":
    main()
