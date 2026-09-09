import json,math,sympy as sp
from pathlib import Path
BASE=Path(__file__).resolve().parent
D=json.load(open(BASE/'qpair_15_modular_rows_v93.json'))
runs=D['runs']; support=D['union_support']; pa,pb=231,469

def inv2(a,b,c,d,p):
    det=(a*d-b*c)%p
    if not det:return None
    z=pow(det,-1,p)
    return d*z%p,-b*z%p,-c*z%p,a*z%p

def frame(run):
    p=run['p'];r1=run['r1'];r2=run['r2']
    I=inv2(r1[pa-1],r1[pb-1],r2[pa-1],r2[pb-1],p)
    if I is None:return None
    a,b,c,d=I
    return ([(a*x+b*y)%p for x,y in zip(r1,r2)],[(c*x+d*y)%p for x,y in zip(r1,r2)])

def crt(vals,mods):
    x=vals[0]%mods[0];M=mods[0]
    for b,p in zip(vals[1:],mods[1:]):
        x += (((b-x)%p)*pow(M,-1,p)%p)*M;M*=p;x%=M
    return x,M

def rr(x,M):
    x%=M;B=math.isqrt(M//2);r0,r1=M,x;t0,t1=0,1
    while r1 and abs(r1)>B:
        q=r0//r1;r0,r1=r1,r0-q*r1;t0,t1=t1,t0-q*t1
    if not r1 or not t1:return None
    a,b=r1,t1
    if b<0:a,b=-a,-b
    if abs(a)>B or b>B or math.gcd(a,b)!=1 or (a-x*b)%M:return None
    return a,b

def addr(idx):
    z=0
    for j in range(22):
        for r in range(22-j):
            z+=1
            if z==idx:return ('E',j,r)
    for j in range(16):
        for r in range(21-j):
            z+=1
            if z==idx:return ('O',j,r)
    raise ValueError(idx)

print('M23_QPAIR_GOODFRAME_V93_BEGIN')
print('TRAINING_PRIME_COUNT =',len(runs))
assert len(runs)==15 and len(support)==86
fr=[frame(r) for r in runs];assert all(x is not None for x in fr)
print('UNION_SUPPORT_SIZE = 86')
print('GOODFRAME_PIVOTS = 231 469')
print('GOODFRAME_PIVOTS_INVERTIBLE_ALL_15 = true')
mods=[r['p'] for r in runs];M=math.prod(mods)
rows=[]
for row in (0,1):
    out={pa:(1,1) if row==0 else (0,1),pb:(0,1) if row==0 else (1,1)}
    for col in support:
        if col in (pa,pb):continue
        x,_=crt([f[row][col-1] for f in fr],mods);z=rr(x,M)
        if z is None: raise SystemExit(f'unreconstructed {row} {col}')
        out[col]=z
    rows.append(out)
print('CRT_MODULUS_DIGITS =',len(str(M)))
print('FULL_NONPIVOT_RECONSTRUCTED =',168)
# Reduce reconstructed rationals back to every training prime.
for ri,run in enumerate(runs):
    p=run['p']; good=0
    for row in (0,1):
        for col in support:
            a,b=rows[row][col]
            if b%p==0: raise SystemExit('denominator zero mod training prime')
            if a*pow(b,-1,p)%p != fr[ri][row][col-1]: raise SystemExit(f'reduction mismatch {p} {row} {col}')
            good+=1
    assert good==172
print('TRAINING_REDUCTION_CHECKS =',15*172)
# Convert exact rational q-pair rows to H(t,v) and compare with recorded primitive integers.
t,v=sp.symbols('t v');q=t*t+23
for row in (0,1):
    e=0
    for col,(a,b) in rows[row].items():
        if a==0:continue
        typ,j,r=addr(col); d=j+r-18
        if d<0: raise SystemExit(f'negative carry exponent at slot {col}')
        term=sp.Rational(a,b)*(q**d)*(v**j)
        if typ=='O':term*=t
        e+=term
    e=sp.cancel(e)
    num,den=sp.fraction(e)
    P=sp.Poly(num,t,v,domain=sp.QQ)
    denoms=[c.q for c in P.coeffs()];L=1
    for x in denoms:L=math.lcm(L,int(x))
    ints=[int(c*L) for c in P.coeffs()];g=0
    for x in ints:g=math.gcd(g,abs(x))
    prim=sp.expand(num*sp.Rational(L,g))
    # normalize sign to recorded file
    target=sp.expand(sp.sympify((BASE/f'M23_H{row+1}_integer_v91.txt').read_text(),locals={'t':t,'v':v}))
    if sp.expand(prim-target)!=0 and sp.expand(-prim-target)!=0:
        raise SystemExit(f'H{row+1} mismatch')
print('GOODFRAME_ROWS_TO_H1_H2_EXACT_MATCH = true')
# LOO is a diagnostic, not an acceptance condition.
loo=[]
for h in range(len(runs)):
    idx=[i for i in range(len(runs)) if i!=h]; mm=[mods[i] for i in idx];hp=mods[h];rec=pas=0
    for row in (0,1):
        for col in support:
            if col in (pa,pb): continue
            x,_=crt([fr[i][row][col-1] for i in idx],mm);z=rr(x,math.prod(mm))
            if z is None:continue
            rec+=1;a,b=z
            if b%hp and a*pow(b,-1,hp)%hp==fr[h][row][col-1]:pas+=1
    loo.append((rec,pas))
print('LEAVE_ONE_OUT_DIAGNOSTIC =',loo)
print('NOTE = full 168-entry lift uses all 15 primes; exact acceptance is supplied by the characteristic-zero global identity certificate')
print('M23_QPAIR_GOODFRAME_V93_PASS')
