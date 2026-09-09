#!/usr/bin/env python3
"""Exact parallel compactified-fiber comparison over F_1013.

This is a resource-stable publication runner for the same computation as
``exact_closure_independent_v95/cert5_frame_invariant_holdout_p1013.py``.
It compares the degree-23 divisors on P^1 at every t in F_1013, restoring
points at infinity when the affine leading coefficient vanishes.
"""
from __future__ import annotations
import multiprocessing as mp
import os
from math import gcd
from pathlib import Path
import re
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'certificates'/'exact_closure_independent_v95'
p=1013
W=sp.symbols('W')

txt=(BASE/'data'/'M23_tetragonal_polynomial_v92.txt').read_text()
flat={}
for c,k,d in re.findall(r'(-?\d+)\s*\*\s*W\^(\d+)\s*\*\s*T\^(\d+)',txt):
    flat[(int(k),int(d))]=int(c)
assert len(flat)==120
ct=0; mx=0
for v in flat.values(): ct=gcd(ct,abs(v)); mx=max(mx,len(str(abs(v))))
assert ct==1 and max(k for k,_ in flat)==23 and max(d for _,d in flat)==4

log=(BASE/'data'/'M23_FastHeldout_p1013_user_output.log').read_text()
tab=[int(x) for x in re.search(r'SYMMETRIC_FLAT120\s*=\s*\[(.*?)\]',log,re.S).group(1).replace('\n',' ').split(',')]
assert len(tab)==120
EX=tuple(tuple(flat[(i,j)]%p for j in range(5)) for i in range(24))
CT=tuple(tuple(tab[5*i+j]%p for j in range(5)) for i in range(24))

def coefficients(table,t0):
    return [sum(table[i][j]*pow(t0,j,p) for j in range(5))%p for i in range(24)]

def fact_type(table,t0):
    co=coefficients(table,t0)
    poly=sp.Poly(list(reversed(co)),W,modulus=p)
    parts=[(f.degree(),m) for f,m in poly.factor_list()[1]]
    degree=sum(d*m for d,m in parts)
    if degree<23:
        parts.append((1,23-degree))
    return tuple(sorted(parts))

def compare_t(t0):
    return t0, fact_type(EX,t0), fact_type(CT,t0)

def main():
    print(f'F3: exact vector: 120 terms, gcd 1, bidegrees (T:4, W:23), max |coeff| = {mx} digits: PASS',flush=True)
    ratio=None; consistent=True
    for i in range(24):
        for j in range(5):
            a,b=EX[i][j],CT[i][j]
            if a==0 and b==0: continue
            if a==0 or b==0: consistent=False; break
            r=a*pow(b,-1,p)%p
            if ratio is None: ratio=r
            elif r!=ratio: consistent=False; break
        if not consistent: break
    assert not consistent
    print('F1: direct projective comparison fails across frames (expected; symmetric vs good frame differ by constant GL2): RECORDED',flush=True)
    workers=max(1,min(int(os.environ.get('M23_FIBER_WORKERS','8')),mp.cpu_count() or 1,p))
    with mp.Pool(workers) as pool:
        rows=pool.map(compare_t,range(p),chunksize=4)
    mism=[t for t,a,b in rows if a!=b]
    assert not mism, f'{len(mism)} fiber mismatches; first={mism[:1]}'
    special=[]
    for t0 in range(p):
        le=coefficients(EX,t0)[23]; lc=coefficients(CT,t0)[23]
        if le==0 or lc==0: special.append((t0,le==0,lc==0))
    assert [t for t,_,_ in special]==[562,782]
    print(f'F2: compactified fiber factorization types agree at all {p}/{p} values of t over F_{p}: PASS',flush=True)
    print(f'    ({len(special)} fibers meet W=infinity in one frame: {[t for t,_,_ in special]}; restored as rational points at infinity)',flush=True)
    print('FIBER_WORKERS =',workers,flush=True)
    print('M23_PATCH_CERT5_PASS',flush=True)
if __name__=='__main__': main()
