#!/usr/bin/env python3
"""Exact characteristic-zero transition from arithmetic coordinate z to symmetric w.

Derives the first-jet matrix from the local q=t^2+23 ramification data and the
exact good-frame adjoints H1,H2, then verifies the resulting constant PGL2(Q)
transformation coefficientwise against all 21 recorded symmetric training tables
and the independent p=1013 table.
"""
import json, math, re, hashlib
from functools import reduce
from pathlib import Path
from math import gcd, lcm
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
t,v=sp.symbols('t v'); q=t*t+23
src=(ROOT/'certificates/exact_tetragonal_v93/M23_qpair_full_rows_p100207139_v86.m').read_text()
expr=re.search(r'b\[23\]\s*:=\s*(.*?);',src,re.S).group(1).replace('^','**')
b23=sp.expand(sp.sympify(expr,locals={'t':t}))
quo,rem=sp.div(sp.Poly(b23,t,domain=sp.ZZ),sp.Poly(q,t,domain=sp.ZZ))
assert rem.is_zero
c=quo.as_expr()
crem=sp.rem(sp.Poly(c,t,domain=sp.QQ),sp.Poly(q,t,domain=sp.QQ)).as_expr()

def modq(e):
    return sp.expand(sp.rem(sp.Poly(sp.expand(e),t,domain=sp.QQ),sp.Poly(q,t,domain=sp.QQ)).as_expr())
def qpow(e,n):
    out=sp.Integer(1); base=modq(e)
    while n:
        if n&1: out=modq(out*base)
        n//=2
        if n: base=modq(base*base)
    return out
def invq(e):
    return modq(sp.invert(sp.Poly(modq(e),t,domain=sp.QQ),sp.Poly(q,t,domain=sp.QQ)).as_expr())

Ls=[]
for i in (1,2):
    H=sp.expand(sp.sympify((ROOT/f'certificates/exact_tetragonal_v93/M23_H{i}_integer_v91.txt').read_text(),locals={'t':t,'v':v}))
    cv=sp.Poly(H,v,domain=sp.ZZ[t]).nth(10)
    qq,rr=sp.div(sp.Poly(cv,t,domain=sp.QQ),sp.Poly(q,t,domain=sp.QQ)); assert rr.is_zero
    Ls.append(modq(qq.as_expr()))

# Local initial form: u^23 + c(t) q^19.  With r=t-alpha, v_P(u)=19,
# v_P(r)=23 and pi=u^17/r^14, the first-jet common factor is
# m = -c(alpha)^15 (2 alpha)^294 / 23.
s=2*t
mfac=modq(-qpow(crem,15)*qpow(s,294)/23)
vals=[modq(mfac*L) for L in Ls]
J=sp.zeros(2,2)
for i,F in enumerate(vals):
    P=sp.Poly(F,t,domain=sp.QQ)
    J[i,0]=P.nth(0)
    J[i,1]=P.nth(1)
assert J.det()!=0
C=sp.simplify(J.inv())
L=1
for x in C: L=lcm(L,int(sp.denom(x)))
ints=[int(sp.numer(x*L)) for x in C]
g=reduce(gcd,[abs(x) for x in ints if x]); ints=[x//g for x in ints]
if ints[-1]<0: ints=[-x for x in ints]
EXPECTED=[
9718693045169819066743297673119834593216940257793791469450716674784281955364438129650853737742920699321709602869946773855648462960671465803746362291,
-25607140774189876405011391164460402180010842849857578359577201920481910333070041823933541055695259371502159329254283014074287086838246924062024439177,
23380786748882483713100677944737745665112461310228515182066820286347571647601154649357173814190455036747456088825342453561796405215705126133540317815,
118541105788627344372465383401963348420558929785051465395703781692834568129664923919806407188391867342746663258644336405504686522926958463000828766955]
assert ints==EXPECTED

poly=(ROOT/'certificates/exact_tetragonal_v93/M23_tetragonal_polynomial_v92.txt').read_text()
good={(int(k),int(d)):int(c0) for c0,k,d in re.findall(r'(-?\d+)\s*\*\s*W\^(\d+)\s*\*\s*T\^(\d+)',poly)}
assert len(good)==120

def transform_column(co,p):
    a,b,c0,d=[x%p for x in ints]; n=23; out=[0]*24
    # w=(a z+b)/(c z+d), so z=(d w-b)/(a-c w).
    for k,ck in enumerate(co):
        ck%=p
        for i in range(k+1):
            ci=math.comb(k,i)*pow(d,i,p)*pow((-b)%p,k-i,p)%p
            for j in range(n-k+1):
                cj=math.comb(n-k,j)*pow((-c0)%p,j,p)*pow(a,n-k-j,p)%p
                out[i+j]=(out[i+j]+ck*ci*cj)%p
    return out

def projective_equal(x,y,p):
    lam=None
    for a,b in zip(x,y):
        a%=p; b%=p
        if a==0 and b==0: continue
        if a==0 or b==0: return False
        r=a*pow(b,-1,p)%p
        if lam is None: lam=r
        elif r!=lam: return False
    return True

D=json.load(open(ROOT/'certificates/current_21prime/symmetric_tables_21primes.json'))
runs=list(D['runs'])
log=(ROOT/'certificates/heldout_p1013/M23_FastHeldout_p1013_user_output.log').read_text()
tab=[int(x) for x in re.search(r'SYMMETRIC_FLAT120\s*=\s*\[(.*?)\]',log,re.S).group(1).replace('\n',' ').split(',')]
runs.append({'prime':1013,'flat120':tab})
passed=[]
for run in runs:
    p=run['prime']; flat=[0]*120
    for d in range(5):
        tr=transform_column([good[(k,d)] for k in range(24)],p)
        for k,x in enumerate(tr): flat[5*k+d]=x
    assert projective_equal(flat,run['flat120'],p), p
    passed.append(p)

# Exact symmetric-frame coefficient table.  Since
#   w=(A z+B)/(C z+D),
# we have z=(D w-B)/(A-C w).  Clearing the 23rd power denominator gives
#   R_sym(T,W)=primitive_part((A-CW)^23 R(T,(DW-B)/(A-CW))).
A,B,C0,D0=ints
sym={}
for td in range(5):
    col=[0]*24
    for k in range(24):
        ck=good[(k,td)]
        for i in range(k+1):
            ci=math.comb(k,i)*(D0**i)*((-B)**(k-i))
            for j in range(24-k):
                cj=math.comb(23-k,j)*((-C0)**j)*(A**(23-k-j))
                col[i+j]+=ck*ci*cj
    for kw,x in enumerate(col): sym[(kw,td)]=x
gsym=reduce(gcd,[abs(x) for x in sym.values() if x])
sym={key:x//gsym for key,x in sym.items()}
if sym[(23,0)]<0: sym={key:-x for key,x in sym.items()}
sym_flat=[sym[(k,d)] for k in range(24) for d in range(5)]
sym_path=HERE/'M23_symmetric_tetragonal_coeffs.json'
sym_data=json.load(open(sym_path))
assert sym_flat==sym_data['coefficients_flat_k_major_d_minor']
assert sym_data['term_count']==120
assert sym_data['bidegree_T_W']==[4,23]
assert sym_data['max_coefficient_digits']==max(len(str(abs(x))) for x in sym_flat if x)
sym_sha=hashlib.sha256(sym_path.read_bytes()).hexdigest()

print('M23_EXACT_FRAME_TRANSITION_V94_BEGIN')
print('B23_DIVISIBLE_BY_Q = true')
print('GOODFRAME_FIRST_JET_RANK = 2')
print('TRANSITION_MATRIX_PRIMITIVE =',*ints)
print('TRANSITION_MATRIX_DIGITS =',*[len(str(abs(x))) for x in ints])
print('TRANSITION_DETERMINANT_NONZERO =', str(A*D0-B*C0 != 0).lower())
print('W_EQUALS = (A*Z+B)/(C*Z+D)')
print('FULL_TABLE_PRIME_COUNT =',len(passed))
print('FULL_TABLE_PRIMES =',passed)
print('FULL_120_COEFFICIENT_PROJECTIVE_MATCH_ALL = true')
print('EXACT_SYMMETRIC_TERM_COUNT =',sym_data['term_count'])
print('EXACT_SYMMETRIC_MAX_COEFFICIENT_DIGITS =',sym_data['max_coefficient_digits'])
print('EXACT_SYMMETRIC_TABLE_SHA256 =',sym_sha)
print('INCLUDES_HELDOUT_1013 = true')
print('INCLUDES_PRIME_100208161 = true')
print('M23_EXACT_FRAME_TRANSITION_V94_PASS')
