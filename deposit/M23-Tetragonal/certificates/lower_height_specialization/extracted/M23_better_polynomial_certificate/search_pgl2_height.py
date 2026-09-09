#!/usr/bin/env python3
"""Exhaustive bounded PGL_2(Z) coefficient-height search.

Searches primitive integer matrices (a,b,c,d), up to scalar sign, with
max(|a|,|b|,|c|,|d|) <= B and ad-bc != 0, for the generator
    beta = (a*alpha+b)/(c*alpha+d)
where alpha is a root of HJLPPZ Example 3.7 f2.

The defining polynomial is obtained exactly from
    (a-c*y)^23 * f2((d*y-b)/(a-c*y)).
It is divided by integer content and sign-normalized.  The objective is
ordinary polynomial height max |coefficient|, with digit count and L1 norm
used only as tie-breakers.

Default B=8.  This enumerates 37,296 distinct degree-23 transforms and finds
beta=alpha-1 as the unique best normalized matrix in this search.
"""
from itertools import product
from math import comb, gcd
import argparse

F2=[1243077066,-11217790920,38754121124,-67357061907,63691532334,-26037806834,-5728074376,9451874955,-2463757240,83587888,-436105484,320807726,-71999476,17344116,-9392096,2223732,-361974,127420,-21620,1679,-598,46,0,1]
N=23
C=[[comb(k,j) for j in range(k+1)] for k in range(N+1)]

def conv(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        if x:
            for j,y in enumerate(q):
                if y:r[i+j]+=x*y
    return r

def linpow(u,v,k):
    return [C[k][j]*(u**(k-j))*(v**j) for j in range(k+1)]

def primitive(poly):
    g=0
    for z in poly:g=gcd(g,abs(z))
    if g>1:poly=[z//g for z in poly]
    while len(poly)>1 and poly[-1]==0:poly.pop()
    if poly[-1]<0:poly=[-z for z in poly]
    return poly

def transform(a,b,c,d):
    # beta=(a alpha+b)/(c alpha+d), alpha=(d beta-b)/(a-c beta)
    p1=[linpow(-b,d,i) for i in range(N+1)]
    p2=[linpow(a,-c,k) for k in range(N+1)]
    out=[0]*(N+1)
    for i,ai in enumerate(F2):
        if not ai: continue
        t=conv(p1[i],p2[N-i])
        for j,z in enumerate(t):out[j]+=ai*z
    return primitive(out)

def score(p):
    return (max(abs(z) for z in p), sum(len(str(abs(z))) for z in p if z), sum(abs(z) for z in p))

def canonical(a,b,c,d):
    vals=[a,b,c,d]
    g=0
    for q in vals:g=gcd(g,abs(q))
    vals=[q//g for q in vals]
    first=next(q for q in vals if q)
    if first<0:vals=[-q for q in vals]
    return tuple(vals)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('-B','--bound',type=int,default=8)
    args=ap.parse_args(); B=args.bound
    base=(score(F2),(1,0,0,1),F2)
    best_all=base; best_monic=base
    seen=set(); count=0
    R=range(-B,B+1)
    for a,b,c,d in product(R,R,R,R):
        if a*d-b*c==0: continue
        key=canonical(a,b,c,d)
        if key in seen: continue
        seen.add(key)
        p=transform(*key)
        if len(p)!=24: continue
        count+=1; s=score(p)
        if s<best_all[0]:best_all=(s,key,p)
        if p[-1]==1 and s<best_monic[0]:best_monic=(s,key,p)
    print(f"bound={B}")
    print(f"degree-23 transforms checked={count}")
    print(f"best all: score={best_all[0]} matrix={best_all[1]} leading={best_all[2][-1]}")
    print(f"best monic: score={best_monic[0]} matrix={best_monic[1]}")
    assert B != 8 or (count==37296 and best_all[1]==(1,-1,0,1) and best_all[0][0]==1938799398)
    assert B != 8 or best_monic[1]==(1,-1,0,1)
    print("PGL2 SEARCH CERTIFICATE: PASS")

if __name__=='__main__':main()
