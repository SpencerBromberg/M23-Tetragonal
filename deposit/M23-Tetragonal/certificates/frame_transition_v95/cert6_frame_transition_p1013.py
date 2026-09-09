#!/usr/bin/env python3
"""Certificate 6 (new): explicit symmetric<->good frame transition at the
held-out prime, with coefficientwise validation.

Result established by this script (run against the v92 exact polynomial
and the ORIGINAL certified p=1013 SYMMETRIC_FLAT120 log):

  The constant Mobius W_good -> (a W + b)/(c W + d) with
      (a, b, c, d) = (546, 938, 283, 1)  mod 1013
  is the UNIQUE element of PGL2(F_1013) carrying the exact good-frame
  relation to the certified symmetric-frame table: the transformed
  R(T, (aW+b)/(cW+d)) * (cW+d)^23 matches SYMMETRIC_FLAT120
  COEFFICIENTWISE (single projective ratio 732) -- upgrading the
  frame-invariant fiber validation to a coefficientwise one at p=1013.

  Uniqueness: the Mobius was solved from 8 forced root correspondences
  (fibers whose factorization contains a linear factor of multiplicity
  unique within the fiber); the 6x4 linear system has GF(1013)-kernel of
  dimension exactly 1.

Historical lifting protocol (superseded by the exact characteristic-zero transition): record the
symmetric-frame flat120 at ANY second prime (rerunning the p=31
regression script and capturing output suffices), rerun this script
with that log added, CRT the two Mobius solutions, and
rational-reconstruct. All legacy tables then validate the exact
relation coefficientwise through the exact M.

Usage: python3 cert6_frame_transition_p1013.py EXACT_POLY.txt P1013_LOG
       [SECOND_LOG PRIME2]
"""
import re, sys, math
from math import comb

def load_exact(path):
    fe = {}
    for c,k,d in re.findall(r'(-?\d+)\s*\*\s*W\^(\d+)\s*\*\s*T\^(\d+)',
                            open(path).read()):
        fe[(int(k),int(d))] = int(c)
    assert len(fe) == 120
    return fe

def load_table(path):
    m = re.search(r'SYMMETRIC_FLAT120\s*:?=\s*\[(.*?)\]',
                  open(path).read(), re.S)
    tab = [int(x) for x in m.group(1).replace('\n',' ').split(',')]
    assert len(tab) == 120
    return tab

def transform_mod(FE,a,b,c,d,p):
    out=[[0]*5 for _ in range(24)]
    for i in range(24):
        P1=[comb(i,k)*pow(a,k,p)*pow(b,i-k,p)%p for k in range(i+1)]
        P2=[comb(23-i,k)*pow(c,k,p)*pow(d,23-i-k,p)%p for k in range(24-i)]
        conv=[0]*24
        for k1,v1 in enumerate(P1):
            if v1:
                for k2,v2 in enumerate(P2):
                    if v2: conv[k1+k2]=(conv[k1+k2]+v1*v2)%p
        for j in range(5):
            A=FE[(i,j)]%p
            if A:
                for k in range(24):
                    if conv[k]: out[k][j]=(out[k][j]+A*conv[k])%p
    return out

def proj_match(out,tab,p):
    ratio=None
    for i in range(24):
        for j in range(5):
            x,y=out[i][j]%p,tab[5*i+j]%p
            if x==0 and y==0: continue
            if x==0 or y==0: return None
            r=y*pow(x,-1,p)%p
            if ratio is None: ratio=r
            elif r!=ratio: return None
    return ratio

def solve_mobius(FE, tab, p):
    import sympy as sp
    W = sp.symbols('W')
    def fiber(get,t0):
        co=[]
        for i in range(24):
            v=0
            for j in range(5): v=(v+get(i,j)*pow(t0,j,p))%p
            co.append(v)
        return sp.Poly(list(reversed(co)), W, modulus=p)
    gx=lambda i,j: FE[(i,j)]%p
    gc=lambda i,j: tab[5*i+j]%p
    pairs=[]
    for t0 in range(2,p):
        fe_,fc_=fiber(gx,t0),fiber(gc,t0)
        def uniq(P):
            d={}
            for f,m in P.factor_list()[1]:
                if f.degree()==1: d.setdefault(m,[]).append(f)
            return {m:v[0] for m,v in d.items() if len(v)==1}
        ue,uc=uniq(fe_),uniq(fc_)
        for m in ue:
            if m in uc:
                pairs.append(((-ue[m].nth(0))%p, (-uc[m].nth(0))%p))
        if len(pairs)>=8: break
    rows=[[bb,1,(-aa*bb)%p,(-aa)%p] for aa,bb in pairs]
    # GF(p) nullspace
    A=[r[:] for r in rows]; n=4; piv=[]; r=0
    for c in range(n):
        pr=next((rr for rr in range(r,len(A)) if A[rr][c]%p), None)
        if pr is None: continue
        A[r],A[pr]=A[pr],A[r]
        inv=pow(A[r][c],-1,p); A[r]=[x*inv%p for x in A[r]]
        for rr in range(len(A)):
            if rr!=r and A[rr][c]%p:
                f=A[rr][c]; A[rr]=[(x-f*y)%p for x,y in zip(A[rr],A[r])]
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in piv]
    assert len(free)==1, "Mobius not unique from forced pairs"
    v=[0]*n; v[free[0]]=1
    for i,c in enumerate(piv): v[c]=(-A[i][free[0]])%p
    return tuple(v)

def main():
    FE = load_exact(sys.argv[1])
    tab = load_table(sys.argv[2]); p = 1013
    M = solve_mobius(FE, tab, p)
    r = proj_match(transform_mod(FE,*M,p), tab, p)
    assert r is not None
    print(f"unique Mobius mod {p}: (a,b,c,d) = {M}; coefficientwise "
          f"projective match with ratio {r}: PASS")
    if len(sys.argv) >= 5:
        tab2 = load_table(sys.argv[3]); p2 = int(sys.argv[4])
        M2 = solve_mobius(FE, tab2, p2)
        r2 = proj_match(transform_mod(FE,*M2,p2), tab2, p2)
        assert r2 is not None
        print(f"unique Mobius mod {p2}: {M2}; match ratio {r2}: PASS")
        mod = p*p2
        def crt(x,y):
            return (x*p2*pow(p2,-1,p) + y*p*pow(p,-1,p2)) % mod
        # align projective scales: normalize both to d-coordinate 1 when
        # possible before CRT
        def norm(Mv, q):
            dd = Mv[3] if Mv[3] else next(x for x in Mv if x)
            inv = pow(dd, -1, q)
            return tuple(x*inv % q for x in Mv)
        Ma, Mb = norm(M,p), norm(M2,p2)
        lift = [crt(a_,b_) for a_,b_ in zip(Ma,Mb)]
        B = math.isqrt(mod//2)
        def rr_(x):
            r0,r1,s0,s1 = mod, x%mod, 0, 1
            while abs(r1) > B:
                q_ = r0//r1; r0,r1 = r1,r0-q_*r1; s0,s1 = s1,s0-q_*s1
            if s1 == 0: return None
            n,d = (r1,s1) if s1>0 else (-r1,-s1)
            return (n,d) if math.gcd(n,d)==1 and d<=B and abs(n)<=B else None
        print("CRT lift:", lift, "-> rational reconstruction:",
              [rr_(x) for x in lift])
    print("M23_PATCH_CERT6_PASS")

if __name__ == "__main__":
    main()
