#!/usr/bin/env python3
"""Exact certificate for global translate and SL2(Z) height minimality.

The only numerical discovery input is a list of rational root centers for g.
Each center is certified exactly by a Rouche disk, so no floating-point
approximation enters any retained decision.
"""
from fractions import Fraction as Q
from math import gcd, comb, isqrt
from pathlib import Path
import json, sympy as sp, time

HERE=Path(__file__).resolve().parent
f_asc,g_asc=json.load(open(HERE/'polys.json'))
centers_raw=json.load(open(HERE/'root_centers.json'))
centers=[(Q(a),Q(b)) for a,b in centers_raw]
N=23; HMIN=max(abs(x) for x in g_asc); RHO=Q(1,10**10)
x=sp.symbols('x')
fpoly=sp.Poly(sum(sp.Integer(c)*x**i for i,c in enumerate(f_asc)),x)

# Gaussian rational helpers
def zadd(a,b): return (a[0]+b[0],a[1]+b[1])
def zmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def zscale(a,s): return (a[0]*s,a[1]*s)
def zpow(a,n):
    r=(Q(1),Q(0)); b=a
    while n:
        if n&1:r=zmul(r,b)
        b=zmul(b,b); n//=2
    return r

def taylor_at(center, coeffs):
    n=len(coeffs)-1; pw=[zpow(center,j) for j in range(n+1)]; A=[]
    for k in range(n+1):
        s=(Q(0),Q(0))
        for i in range(k,n+1):
            if coeffs[i]: s=zadd(s,zscale(pw[i-k],Q(coeffs[i]*comb(i,k))))
        A.append(s)
    return A

# 23 exact Rouche disks, one root in each.
assert len(centers)==N
for idx,c0 in enumerate(centers):
    A=taylor_at(c0,g_asc)
    lhs=max(abs(A[1][0]),abs(A[1][1]))*RHO  # <= |A1| rho, so valid lower bound
    rhs=abs(A[0][0])+abs(A[0][1])          # >= |A0|
    for k in range(2,N+1): rhs+=(abs(A[k][0])+abs(A[k][1]))*RHO**k
    assert lhs>rhs, ('Rouche failed',idx)
# disks disjoint, all roots |alpha|<9, pairwise root separation >1/10
for a,b in centers:
    assert a*a+b*b < (Q(9)-RHO)**2
for i,(a,b) in enumerate(centers):
    for c,d in centers[i+1:]:
        assert (a-c)**2+(b-d)**2 > (Q(1,10)+2*RHO)**2
print('ROUCHE_ROOT_DISKS 23/23 PASS')
print('ROOT_MODULUS_LT_9 PASS; ROOT_SEPARATION_GT_1_10 PASS')

# exact rational interval arithmetic for the Julia-point box
Iv=tuple
def iv(a,b=None): a=Q(a); b=a if b is None else Q(b); assert a<=b; return (a,b)
def iadd(A,B): return (A[0]+B[0],A[1]+B[1])
def ineg(A): return (-A[1],-A[0])
def isub(A,B): return iadd(A,ineg(B))
def imul(A,B):
    v=(A[0]*B[0],A[0]*B[1],A[1]*B[0],A[1]*B[1]); return (min(v),max(v))
def iscale(A,s): return imul(A,iv(s))
def isq(A):
    if A[0]<=0<=A[1]: return (Q(0),max(A[0]*A[0],A[1]*A[1]))
    return (min(A[0]*A[0],A[1]*A[1]),max(A[0]*A[0],A[1]*A[1]))
def iinv(A): assert A[0]>0; return (Q(1,A[1]),Q(1,A[0]))
def idiv(A,B): return imul(A,iinv(B))
root_boxes=[(iv(a-RHO,a+RHO),iv(b-RHO,b+RHO)) for a,b in centers]
def grad_box(T,U):
    gt=iv(0); gu=iv(0)
    for A,Y in root_boxes:
        dt=isub(T,A); D=iadd(iadd(isq(dt),isq(Y)),isq(U))
        gt=iadd(gt,idiv(iscale(dt,2),D)); gu=iadd(gu,idiv(iscale(U,2),D))
    gu=isub(gu,idiv(iv(N),U)); return gt,gu
# Subdivide the four sides to avoid interval dependency inflation.
def side_union(which, parts=64):
    outs=[]
    for j in range(parts):
        q0=Q(j,parts); q1=Q(j+1,parts)
        if which=='left': out=grad_box(iv(-1),iv(2+q0,2+q1))[0]
        elif which=='right': out=grad_box(iv(0),iv(2+q0,2+q1))[0]
        elif which=='low': out=grad_box(iv(-1+q0,-1+q1),iv(2))[1]
        else: out=grad_box(iv(-1+q0,-1+q1),iv(3))[1]
        outs.append(out)
    return min(a for a,b in outs), max(b for a,b in outs)
Gleft=side_union('left'); Gright=side_union('right'); Glow=side_union('low'); Ghigh=side_union('high')
print('GRADIENT_BOUNDARY',[(float(a),float(b)) for a,b in (Gleft,Gright,Glow,Ghigh)])
assert Gleft[1]<0<Gright[0] and Glow[1]<0<Ghigh[0]
print('JULIA_POINT_BOX -1<t<0, 2<u<3 PASS')

# Hutz-Stoll bound. Pair separation and Julia box imply eta>1/594050.
# Pair separation also gives theta > (1/20)^23 for every point of H.
ETA_DEN=594050
AUP=(2**23)*24*(HMIN**2)*(ETA_DEN**22)*(20**23)
COSH_BOUND=600_000_000
assert COSH_BOUND**21>AUP
BOTTOM=isqrt(COSH_BOUND)
assert BOTTOM==24494
print('HUTZ_STOLL_HEIGHT_BOUND cosh<',COSH_BOUND,'=> |c|,|d|<=',BOTTOM)

# Translation theorem (all k in Z)
def translate_coeffs(coeffs,k):
    out=[0]*(len(coeffs))
    for i,ai in enumerate(coeffs):
        for j in range(i+1): out[j]+=ai*comb(i,j)*k**(i-j)
    return out
assert translate_coeffs(f_asc,1)==g_asc
# x^20 coefficient from exact expansion
# (ascending index 20)
def C20(k): return translate_coeffs(f_asc,k)[20]
assert all(C20(k)==1771*k**3+966*k-598 for k in [-104,-1,0,1,104])
assert 5313*0**2+966>0 # derivative 5313 k^2+966 positive globally
assert C20(104)>HMIN and C20(-104)<-HMIN
vals=[(max(abs(v) for v in translate_coeffs(f_asc,k)),k) for k in range(-104,105)]
m=min(h for h,k in vals); args=[k for h,k in vals if h==m]
assert m==HMIN and args==[1]
print('M23_TRANSLATE_GLOBAL_PASS K0=104 UNIQUE_k=1')

# Exact global column enumeration for SL2 competitor.
def F_eval(a,c): return sum(fi*a**i*c**(N-i) for i,fi in enumerate(f_asc) if fi)
def rat(v): r=sp.Rational(v); return Q(int(r.p),int(r.q))
# Exact real roots and real critical points; fast Sturm isolation only.
realroots=fpoly.real_roots(); realcrit=fpoly.diff().real_roots()
assert len(realroots)==7 and len(realcrit)==6
small=[]; outer=[]
for r in realroots:
    I=r._get_interval()
    while rat(I.b)-rat(I.a)>Q(1,10**14): I=I.refine()
    l,h=rat(I.a),rat(I.b)
    small.append((l-Q(1,10**12),h+Q(1,10**12)))
    outer.append((l-Q(1,100),h+Q(1,100)))
crit=[]
for r in realcrit:
    I=r._get_interval()
    while rat(I.b)-rat(I.a)>Q(1,10**10): I=I.refine()
    crit.append((rat(I.a),rat(I.b)))
# Small neighborhoods are disjoint and outer neighborhoods contain no critical point.
for i,S in enumerate(small):
    assert outer[i][0]<S[0]<S[1]<outer[i][1]
for i in range(6): assert outer[i][1]<outer[i+1][0]
for i in range(5): assert crit[i][1]<crit[i+1][0]
for O in outer:
    for Cc in crit: assert Cc[1]<O[0] or Cc[0]>O[1]

def piv(coeffs,X):
    R=iv(0)
    for a in reversed(coeffs): R=iadd(imul(R,X),iv(a))
    return R
threshold=Q(HMIN,5**N)
# Every potential minimum of |f| off the small root neighborhoods is > threshold.
for S,O in zip(small,outer):
    for e in (S[0],S[1],O[0],O[1]):
        val=Q(abs(F_eval(e.numerator,e.denominator)),e.denominator**N); assert val>threshold
for Cc in crit:
    V=piv(f_asc,Cc); assert V[1]<-threshold or V[0]>threshold
for e in (Q(-8),Q(8)):
    val=Q(abs(F_eval(e.numerator,e.denominator)),e.denominator**N); assert val>HMIN
# all roots/criticals lie in (-8,8); hence outside tails are monotone and farther from zero.
for S in small: assert -8<S[0]<S[1]<8
for Cc in crit: assert -8<Cc[0]<Cc[1]<8
fp=fpoly.diff(); assert fp.eval(8)>0 and fp.eval(-8)>0 and fpoly.eval(8)>HMIN and fpoly.eval(-8)<-HMIN

cols={(1,0)}
for c in range(1,5):
    for a in range(-8*c,8*c+1):
        if gcd(abs(a),c)==1 and abs(F_eval(a,c))<=HMIN: cols.add((a,c))
for c in range(5,BOTTOM+1):
    for lo,hi in small:
        L=lo*c; U=hi*c
        amin=L.numerator//L.denominator-1; amax=U.numerator//U.denominator+2
        for a in range(amin,amax+1):
            if not (lo<=Q(a,c)<=hi): continue
            if gcd(abs(a),c)==1 and abs(F_eval(a,c))<=HMIN: cols.add((a,c))
cols=sorted(cols); print('COLUMN_SOLUTIONS',cols)
assert cols==[(0,1),(1,0),(1,1),(2,1)]

# Exact binary substitution for every possible determinant +-1 matrix.
def compose(M):
    a,b,c,d=M; out=[0]*(N+1)
    for i,fi in enumerate(f_asc):
        if not fi: continue
        p1=[comb(i,k)*a**k*b**(i-k) for k in range(i+1)]
        p2=[comb(N-i,k)*c**k*d**(N-i-k) for k in range(N-i+1)]
        for k1,v1 in enumerate(p1):
            if not v1: continue
            for k2,v2 in enumerate(p2):
                if v2: out[k1+k2]+=fi*v1*v2
    return out
signed=set()
for a,c in cols: signed|={(a,c),(-a,-c)}
mat=[]; below=[]; eqforms=set(); eqm=0
for a,c in signed:
    for b,d in signed:
        if abs(a*d-b*c)!=1: continue
        M=(a,b,c,d); mat.append(M); v=compose(M)
        # det +-1 preserves content; f is primitive.
        ct=0
        for z in v: ct=gcd(ct,abs(z))
        assert ct==1
        H=max(abs(z) for z in v)
        if H<HMIN: below.append((M,H))
        if H==HMIN:
            eqm+=1; w=tuple(v)
            if w[-1]<0:w=tuple(-z for z in w)
            eqforms.add(w)
assert not below
rev=list(reversed(g_asc))
expected={tuple(g_asc),tuple((-1)**(i+1)*g_asc[i] for i in range(24)),tuple(rev),tuple((-1)**(i+1)*rev[i] for i in range(24))}
expected={tuple(-z for z in w) if w[-1]<0 else w for w in expected}
assert eqforms==expected
print('UNIMODULAR_MATRICES_TESTED',len(mat),'EQUAL_MATRICES',eqm,'EQUAL_FORMS',len(eqforms))
print('M23_SL2_GLOBAL_HEIGHT_PASS')
print('M23_GL2Z_GLOBAL_HEIGHT_PASS')
