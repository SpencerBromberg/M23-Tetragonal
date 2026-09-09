import re, json, sympy as sp, math, time, os
from pathlib import Path
BASE=Path(__file__).resolve().parent
T,V=sp.symbols('t v')
qpoly=sp.Poly(T*T+23,T,domain=sp.ZZ)
src=(BASE/'M23_qpair_full_rows_p100207139_v86.m').read_text()
# Integral degree-23 model G(t,u)=u^23+...
b={}
for j in range(2,24):
    m=re.search(rf"b\[{j}\]\s*:=\s*(.*?);",src,re.S)
    e=sp.sympify(re.sub(r'\s+',' ',m.group(1)).replace('^','**'),locals={'t':T})
    b[j]=sp.Poly(e,T,domain=sp.ZZ)
Gpol=[sp.Poly(0,T,domain=sp.ZZ) for _ in range(24)]
Gpol[23]=sp.Poly(1,T,domain=sp.ZZ)
for j in range(2,24):
    Gpol[23-j]=b[j]*(qpoly**(j-(5*j)//23))
# Exact good-frame H(t,v), converted to h(t,u) under u=qv and h(t,qv)=q^18 H(t,v)
hs=[]
for nm in ['M23_H1_integer_v91.txt','M23_H2_integer_v91.txt']:
    e=sp.sympify((BASE/nm).read_text(),locals={'t':T,'v':V})
    PV=sp.Poly(e,V,domain=sp.ZZ[T])
    hc=[]
    for j in range(22):
        cj=sp.Poly(PV.nth(j),T,domain=sp.ZZ)
        if j<=18:
            hj=cj*(qpoly**(18-j))
        else:
            den=qpoly**(j-18)
            qq,rr=sp.div(cj,den,domain=sp.ZZ)
            if not rr.is_zero:
                raise RuntimeError(f'{nm}: q divisibility failed at v^{j}')
            hj=qq
        hc.append(hj)
    hs.append(hc)
# Primitive R(T,W)
D=json.load(open(BASE/'M23_tetragonal_coeffs_v92.json'))
coeff=D['primitive_integer_coeffs']
A=[sp.Poly(sum(coeff[5*k+d]*T**d for d in range(5)),T,domain=sp.ZZ) for k in range(24)]

def evalp(P,t): return int(P.eval(t))
def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def mulmod(a,b,f):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    if len(c)<24:c += [0]*(24-len(c))
    for d in range(len(c)-1,22,-1):
        x=c[d]
        if x:
            sh=d-23
            for i in range(23): c[sh+i]-=x*f[i]
    return trim(c[:23])

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)

def scale(a,s): return trim([s*x for x in a])

def verify_t(t):
    f=[evalp(P,t) for P in Gpol]
    if f[23]!=1: raise RuntimeError('G not monic')
    h1=trim([evalp(P,t) for P in hs[0]])
    h2=trim([evalp(P,t) for P in hs[1]])
    av=[evalp(P,t) for P in A]
    # Horner form for sum A_k h1^k h2^(23-k)
    cur=[av[23]]
    p2=[1]
    for k in range(22,-1,-1):
        p2=mulmod(p2,h2,f)
        cur=add(mulmod(cur,h1,f),scale(p2,av[k]))
    return cur

if __name__ == '__main__':
    import multiprocessing as mp, time
    vals=list(range(-485,486))
    print('M23_TETRAGONAL_GLOBAL_IDENTITY_V96_BEGIN', flush=True)
    print('EVALUATION_RANGE = -485..485', flush=True)
    print('WEIGHTED_DEGREE_BOUND = 970', flush=True)
    st=time.time()
    requested=int(os.environ.get('M23_IDENTITY_WORKERS','4'))
    procs=max(1,min(requested, mp.cpu_count() or 1))
    with mp.Pool(processes=procs) as pool:
        results=pool.map(verify_t, vals, chunksize=4)
    bad=[t for t,r in zip(vals,results) if r != [0]]
    if bad:
        print('FAIL_T =',bad[0], flush=True)
        raise SystemExit(1)
    print('EXACT_ZERO_COUNT = 971', flush=True)
    print('GLOBAL_REMAINDER_IDENTICALLY_ZERO = true', flush=True)
    print('WORKERS =',procs, flush=True)
    print('ELAPSED_SEC =',round(time.time()-st,2), flush=True)
    print('M23_TETRAGONAL_GLOBAL_IDENTITY_V96_PASS', flush=True)
