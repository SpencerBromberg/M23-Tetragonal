import re,sympy as sp,time,json,math
from pathlib import Path
BASE = Path(__file__).resolve().parent
T,V=sp.symbols('t v'); qpoly=sp.Poly(T*T+23,T,domain=sp.ZZ)
src=(BASE/'M23_qpair_full_rows_p100207139_v86.m').read_text()
# b poly
b={}
for j in range(2,24):
 m=re.search(rf"b\[{j}\]\s*:=\s*(.*?);",src,re.S)
 e=sp.sympify(re.sub(r'\s+',' ',m.group(1)).replace('^','**'),locals={'t':T})
 b[j]=sp.Poly(e,T,domain=sp.ZZ)
# G coeffs asc u
Gpol=[sp.Poly(0,T,domain=sp.ZZ) for _ in range(24)];Gpol[23]=sp.Poly(1,T,domain=sp.ZZ)
for j in range(2,24):Gpol[23-j]=b[j]*(qpoly**(j-(5*j)//23))
# H -> h coeff polys
hs=[]
for nm in ['M23_H1_integer_v91.txt','M23_H2_integer_v91.txt']:
 e=sp.sympify((BASE/nm).read_text(),locals={'t':T,'v':V}); P=sp.Poly(e,V,T,domain=sp.ZZ)
 hc=[]
 for j in range(22):
  cj=sp.Poly(P.coeff_monomial(V**j) if False else 0,T)
 # easier coeff via Poly in V over ZZ[t]
 PV=sp.Poly(e,V,domain=sp.ZZ[T])
 for j in range(22):
  cj=sp.Poly(PV.nth(j),T,domain=sp.ZZ)
  if j<=18: hj=cj*(qpoly**(18-j))
  else:
   den=qpoly**(j-18); qq,rr=sp.div(cj,den,domain=sp.ZZ)
   assert rr.is_zero
   hj=qq
  hc.append(hj)
 hs.append(hc)
print('h degrees',[[p.degree() if not p.is_zero else -1 for p in h][-5:] for h in hs])
D=json.load(open(BASE/'M23_tetragonal_coeffs_v92.json')); coeff=D['primitive_integer_coeffs']
A=[]
for k in range(24):A.append(sp.Poly(sum(coeff[5*k+d]*T**d for d in range(5)),T,domain=sp.ZZ))

def evalp(P,t):return int(P.eval(t))
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def mulmod(a,b,f):
 n=23;c=[0]*(min(len(a)+len(b)-1,45))
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i+j]+=x*y
 # reduce high down
 if len(c)<24:c += [0]*(24-len(c))
 for d in range(len(c)-1,22,-1):
  x=c[d]
  if x:
   shift=d-23
   for i in range(23):c[shift+i]-=x*f[i]
 c=c[:23]
 return trim(c)
def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 return trim(c)
def scale(a,s):return trim([s*x for x in a])

def verify_t(t):
 f=[evalp(P,t) for P in Gpol]
 assert f[23]==1
 h1=trim([evalp(P,t) for P in hs[0]]);h2=trim([evalp(P,t) for P in hs[1]])
 av=[evalp(P,t) for P in A]
 cur=[av[23]]; p2=[1]
 for k in range(22,-1,-1):
  p2=mulmod(p2,h2,f)
  cur=add(mulmod(cur,h1,f),scale(p2,av[k]))
 return cur


def vec_to_len(a,n=23):
    return a+[0]*(n-len(a))

def homogeneous_columns_at_t(t, mod=None):
    # columns indexed (k,d), k=0..23, d=0..4, for
    # t^d h1^k h2^(23-k) mod G.
    if mod is None:
        f=[evalp(P,t) for P in Gpol]
        h1=trim([evalp(P,t) for P in hs[0]])
        h2=trim([evalp(P,t) for P in hs[1]])
        def mm(a,b): return mulmod(a,b,f)
        def sc(a,s): return scale(a,s)
    else:
        p=mod
        f=[evalp(P,t)%p for P in Gpol]
        h1=trim([evalp(P,t)%p for P in hs[0]])
        h2=trim([evalp(P,t)%p for P in hs[1]])
        def mm(a,b):
            n=23;c=[0]*(len(a)+len(b)-1)
            for i,x in enumerate(a):
                if x:
                    for j,y in enumerate(b):
                        if y:c[i+j]=(c[i+j]+x*y)%p
            if len(c)<24:c += [0]*(24-len(c))
            for deg in range(len(c)-1,22,-1):
                x=c[deg]%p
                if x:
                    sh=deg-23
                    for i in range(23):c[sh+i]=(c[sh+i]-x*f[i])%p
            c=[x%p for x in c[:23]]
            return trim(c)
        def sc(a,s): return trim([(s*x)%p for x in a])
    p1=[[1]]
    for k in range(1,24): p1.append(mm(p1[-1],h1))
    p2=[[1]]
    for k in range(1,24): p2.append(mm(p2[-1],h2))
    cols=[]
    for k in range(24):
        basev=mm(p1[k],p2[23-k])
        for d in range(5):
            s=pow(t,d) if mod is None else pow(t,d,mod)
            cols.append(vec_to_len(sc(basev,s)))
    return cols

def rank_mod(M,p):
    A=[[x%p for x in row] for row in M]
    r=0
    for c in range(len(A[0])):
        piv=next((i for i in range(r,len(A)) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        inv=pow(A[r][c],-1,p)
        A[r]=[(x*inv)%p for x in A[r]]
        for i in range(r+1,len(A)):
            if A[i][c]:
                a=A[i][c]
                A[i]=[(x-a*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A): break
    return r

print('M23_TETRAGONAL_EXACT_KERNEL_V92_BEGIN')
# 1) exact integer zero checks at six t-values.
for t0 in range(6):
    rem=verify_t(t0)
    print('EXACT_SPECIALIZATION_T_%d_ZERO ='%t0, rem==[0])
    if rem != [0]: raise SystemExit(1)

# 2) direct 138x120 constraint matrix reduced modulo one prime.
p=1000003
rows=[]
for t0 in range(6):
    cols=homogeneous_columns_at_t(t0,p)
    # transpose 120 columns of length 23 into 23 rows.
    for udeg in range(23):
        rows.append([cols[c][udeg]%p for c in range(120)])
r=rank_mod(rows,p)
print('CONSTRAINT_ROWS =',len(rows))
print('CONSTRAINT_COLS =',len(rows[0]))
print('RANK_MOD_1000003 =',r)
if r != 119: raise SystemExit(2)
print('KERNEL_DIMENSION_OVER_Q = 1')
print('EXACT_BIDEGREE_T = 4')
print('EXACT_BIDEGREE_W = 23')
print('M23_TETRAGONAL_EXACT_KERNEL_V92_PASS')
