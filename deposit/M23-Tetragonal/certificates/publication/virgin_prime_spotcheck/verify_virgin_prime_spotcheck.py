#!/usr/bin/env python3
"""Virgin-prime end-to-end spot check for the exact tetragonal closure.

Uses only final exact publication artifacts: the primitive arithmetic relation R,
the exact PGL2 transition matrix, and the primitive symmetric relation.  At two
small split primes absent from the discovery and retained-prime pipeline, both
branches t^2+23=0 are checked for:
  (1) R(t,Z) is an exact 23rd power;
  (2) the PGL2 image of its root satisfies w*t=1;
  (3) R_sym(t,W) is an exact 23rd power with root 1/t.
"""
from pathlib import Path
import json, math, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIMES = (1511, 1531)

arith = json.load(open(ROOT / 'certificates/publication/exact_tetragonal/M23_tetragonal_coeffs.json'))
mat = json.load(open(ROOT / 'certificates/publication/frame_transition/M23_frame_transition_matrix.json'))
sym = json.load(open(ROOT / 'certificates/publication/frame_transition/M23_symmetric_tetragonal_coeffs.json'))

R = [int(x) for x in arith['primitive_integer_coeffs']]
S = [int(x) for x in sym['coefficients_flat_k_major_d_minor']]
assert len(R) == len(S) == 120
A, B = map(int, mat['primitive_integer_matrix'][0])
C, D = map(int, mat['primitive_integer_matrix'][1])
assert A*D-B*C != 0

# Confirm the two test primes were absent from the release before this certificate
# was added.  Search all text-bearing files outside this certificate directory.
text_suffixes = {'.py','.m','.json','.log','.txt','.md','.tex','.cff','.tsv','.sh'}
for p in PRIMES:
    pat = re.compile(rf'(?<!\d){p}(?!\d)')
    hits = []
    for path in (ROOT / 'certificates').rglob('*'):
        if not path.is_file() or path.suffix.lower() not in text_suffixes:
            continue
        if HERE in path.parents:
            continue
        try:
            txt = path.read_text(errors='ignore')
        except Exception:
            continue
        if pat.search(txt):
            hits.append(path.relative_to(ROOT).as_posix())
    if hits:
        raise AssertionError(f'prime {p} already occurs outside virgin-prime certificate: {hits[:10]}')

def roots_minus23(p):
    roots = [x for x in range(p) if (x*x + 23) % p == 0]
    assert len(roots) == 2 and roots[0] != roots[1]
    return roots

def fiber(flat, t0, p):
    # index = 5*k+d corresponds to Z^k T^d or W^k T^d
    return [sum((flat[5*k+d] % p) * pow(t0, d, p) for d in range(5)) % p
            for k in range(24)]

def exact_23rd_power(coeffs, p, expected_root=None):
    lead = coeffs[23] % p
    assert lead != 0
    inv23 = pow(23, -1, p)
    root = (-coeffs[22] * pow(lead, -1, p) * inv23) % p
    if expected_root is not None:
        assert root == expected_root % p, (root, expected_root % p)
    for k in range(24):
        want = lead * math.comb(23, k) * pow((-root) % p, 23-k, p) % p
        assert coeffs[k] % p == want, (k, coeffs[k] % p, want)
    return root, lead

checks = 0
print('M23_VIRGIN_PRIME_SPOTCHECK_BEGIN')
for p in PRIMES:
    assert p not in [int(x) for x in arith.get('primes', [])]
    assert (A*D-B*C) % p != 0
    roots = roots_minus23(p)
    print(f'PRIME {p}: sqrt(-23) roots = {roots}')
    for t0 in roots:
        rco = fiber(R, t0, p)
        z0, _ = exact_23rd_power(rco, p)
        checks += 1

        den = (C*z0 + D) % p
        assert den != 0
        w0 = ((A*z0 + B) % p) * pow(den, -1, p) % p
        assert (w0*t0) % p == 1
        checks += 1

        sco = fiber(S, t0, p)
        expected_w = pow(t0, -1, p)
        w1, _ = exact_23rd_power(sco, p, expected_w)
        assert w1 == w0
        checks += 1
        print(f'  t={t0}: arithmetic 23rd-power PASS; PGL2 wt=1 PASS; symmetric root={w1} PASS')

assert checks == 12
print('VIRGIN_PIPELINE_PRIMES = 1511 1531')
print('TOTAL_SUBCHECKS = 12')
print('ARITHMETIC_FIBER_23RD_POWER_ALL = true')
print('PGL2_TWO_POINT_NORMALIZATION_ALL = true')
print('SYMMETRIC_FIBER_23RD_POWER_ALL = true')
print('M23_VIRGIN_PRIME_SPOTCHECK_PASS')
