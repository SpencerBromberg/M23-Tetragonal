import re, sympy as sp, time, math
from pathlib import Path
BASE = Path(__file__).resolve().parent
T,V=sp.symbols('t v')
# parse b
src=(BASE/'M23_qpair_full_rows_p100207139_v86.m').read_text()
bpol={}
for j in range(2,24):
    m=re.search(rf"b\[{j}\]\s*:=\s*(.*?);",src,re.S)
    s=re.sub(r'\s+',' ',m.group(1).strip()).replace('^','**')
    e=sp.sympify(s,locals={'t':T})
    P=sp.Poly(e,T,domain=sp.ZZ)
    bpol[j]=[(int(c),int(mon[0])) for mon,c in P.terms()]
# parse H as coeff dict (dv,dt)->c
Hs=[]
for nm in ['M23_H1_integer_v91.txt','M23_H2_integer_v91.txt']:
    e=sp.sympify((BASE/nm).read_text(),locals={'t':T,'v':V})
    P=sp.Poly(e,V,T,domain=sp.ZZ)
    Hs.append({(int(m[0]),int(m[1])):int(c) for m,c in P.terms()})

def eval_b(j,t,p): return sum((c%p)*pow(t,d,p) for c,d in bpol[j])%p
def eval_H(H,t,p):
    a=[0]*22
    for (dv,dt),c in H.items(): a[dv]=(a[dv]+(c%p)*pow(t,dt,p))%p
    while a and a[-1]==0:a.pop()
    return a or [0]
def trim(a):
    while len(a)>1 and a[-1]%P==0:a.pop()
    return a

def padd(a,b,p):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]=(c[i]+x)%p
    for i,x in enumerate(b):c[i]=(c[i]+x)%p
    while len(c)>1 and c[-1]==0:c.pop()
    return c
def psub(a,b,p):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]=(c[i]+x)%p
    for i,x in enumerate(b):c[i]=(c[i]-x)%p
    while len(c)>1 and c[-1]==0:c.pop()
    return c
def pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]=(c[i+j]+x*y)%p
    while len(c)>1 and c[-1]==0:c.pop()
    return c
def pdivmod(a,b,p):
    a=a[:]
    while len(a)>1 and a[-1]==0:a.pop()
    while len(b)>1 and b[-1]==0:b.pop()
    if b==[0]:raise ZeroDivisionError
    db=len(b)-1; ib=pow(b[-1],-1,p)
    q=[0]*max(1,len(a)-db)
    while len(a)-1>=db and a!=[0]:
        d=len(a)-1-db; coeff=a[-1]*ib%p; q[d]=coeff
        if coeff:
            for j in range(db+1):a[d+j]=(a[d+j]-coeff*b[j])%p
        while len(a)>1 and a[-1]==0:a.pop()
    while len(q)>1 and q[-1]==0:q.pop()
    return q,a
def pmod(a,f,p): return pdivmod(a,f,p)[1]
def pinv(a,f,p):
    r0,r1=f[:],a[:]; s0,s1=[0],[1]
    while r1!=[0]:
        q,r=pdivmod(r0,r1,p); r0,r1=r1,r
        s0,s1=s1,psub(s0,pmul(q,s1,p),p)
    if len(r0)!=1 or r0[0]==0: return None
    invc=pow(r0[0],-1,p)
    return pmod([(x*invc)%p for x in s0],f,p)
def mul_v_mod(a,f,p):
    n=len(f)-1
    c=[0]+a
    if len(c)<=n:return c+[0]*(n-len(c))
    lead=c[n]%p
    c=c[:n]
    if lead:
        for i in range(n):c[i]=(c[i]-lead*f[i])%p
    return c

def matmul(A,B,p):
    n=len(A); C=[[0]*n for _ in range(n)]
    # transpose B
    BT=list(zip(*B))
    for i,row in enumerate(A):
        for j,col in enumerate(BT):
            s=0
            for k in range(n):s += row[k]*col[k]
            C[i][j]=s%p
    return C
def charpoly(A,p):
    n=len(A)
    B=[[1 if i==j else 0 for j in range(n)] for i in range(n)]
    cs=[]
    for k in range(1,n+1):
        AB=matmul(A,B,p)
        tr=sum(AB[i][i] for i in range(n))%p
        ck=(-tr*pow(k,-1,p))%p
        cs.append(ck)
        for i in range(n): AB[i][i]=(AB[i][i]+ck)%p
        B=AB
    # ascending coeffs c_n,...c_1,1
    return list(reversed(cs))+[1]
def make_F(t,p):
    q=(t*t+23)%p
    if q==0:return None
    f=[0]*24; f[23]=1
    for j in range(2,24):
        e=(5*j)//23
        f[23-j]=eval_b(j,t,p)*pow(pow(q,e,p),-1,p)%p
    return f

def relation_at_t(t,p):
    f=make_F(t,p)
    if f is None:return None
    h1=eval_H(Hs[0],t,p); h2=eval_H(Hs[1],t,p)
    inv=pinv(h2,f,p)
    if inv is None:return None
    z=pmod(pmul(h1,inv,p),f,p); z += [0]*(23-len(z))
    cols=[]; cur=z
    for j in range(23):
        cols.append(cur[:23]); cur=mul_v_mod(cur,f,p)
    A=[[cols[j][i] for j in range(23)] for i in range(23)]
    return charpoly(A,p)

def nullspace1(rows,p,ncol=120):
    A=[r[:] for r in rows]
    piv=[]; rr=0
    for c in range(ncol):
        pivrow=None
        for i in range(rr,len(A)):
            if A[i][c]%p: pivrow=i; break
        if pivrow is None: continue
        A[rr],A[pivrow]=A[pivrow],A[rr]
        inv=pow(A[rr][c],-1,p); A[rr]=[(x*inv)%p for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][c]%p:
                a=A[i][c]%p; A[i]=[(x-a*y)%p for x,y in zip(A[i],A[rr])]
        piv.append(c); rr+=1
        if rr==len(A):break
    free=[c for c in range(ncol) if c not in piv]
    print('rank',rr,'free',free)
    if len(free)!=1:return None
    fcol=free[0]; x=[0]*ncol;x[fcol]=1
    for i,c in enumerate(piv):x[c]=(-A[i][fcol])%p
    return x



def crt_merge_vec(x,M,v,p):
    if x is None: return v[:],p
    inv=pow(M,-1,p)
    out=[]
    for a,b in zip(x,v):
        t=((b-a)%p)*inv%p
        out.append(a+M*t)
    return out,M*p

def ratrec(x,m):
    x%=m; B=math.isqrt(m//2)
    r0,r1=m,x; t0,t1=0,1
    while r1 and abs(r1)>B:
        q=r0//r1; r0,r1=r1,r0-q*r1; t0,t1=t1,t0-q*t1
    if not r1 or t1==0:return None
    a,b=r1,t1
    if b<0:a,b=-a,-b
    if abs(a)>B or b>B or math.gcd(a,b)!=1 or (a-x*b)%m:return None
    return a,b

def relation_mod_p(p):
    vals=[]
    for t in range(0,20):
        cp=relation_at_t(t,p)
        if cp is not None:
            vals.append((t,cp))
        if len(vals)>=6: break
    if len(vals)<6:return None
    rows=[]
    for t,cp in vals:
        tp=[pow(t,d,p) for d in range(5)]
        for k in range(23):
            row=[0]*120
            for d in range(5):row[5*k+d]=tp[d]
            mk=cp[k]
            for d in range(5):row[5*23+d]=(-mk*tp[d])%p
            rows.append(row)
    return nullspace1_silent(rows,p)

def nullspace1_silent(rows,p,ncol=120):
    A=[r[:] for r in rows]; piv=[]; rr=0
    for c in range(ncol):
        pivrow=next((i for i in range(rr,len(A)) if A[i][c]%p),None)
        if pivrow is None:continue
        A[rr],A[pivrow]=A[pivrow],A[rr]
        inv=pow(A[rr][c],-1,p); A[rr]=[(x*inv)%p for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][c]%p:
                a=A[i][c]%p; A[i]=[(x-a*y)%p for x,y in zip(A[i],A[rr])]
        piv.append(c); rr+=1
    free=[c for c in range(ncol) if c not in piv]
    if len(free)!=1:return None
    fcol=free[0]; x=[0]*ncol;x[fcol]=1
    for i,c in enumerate(piv):x[c]=(-A[i][fcol])%p
    return x

start=time.time(); X=None;M=1; used=[]
pr=1000000007
for it in range(220):
    p=int(sp.nextprime(pr-1))
    pr=p+1000
    v=relation_mod_p(p)
    if v is None:
        print('skip',p);continue
    X,M=crt_merge_vec(X,M,v,p);used.append(p)
    rec=[ratrec(a,M) for a in X]
    n=sum(r is not None for r in rec)
    
    if len(used) <= 5 or len(used)%10==0 or n==120:
        print(len(used),p,'digits',len(str(M)),'rec',n,'elapsed',round(time.time()-start,2))
    if n==120 and len(used)>=3:
        # verify at two independent primes
        good=True
        for hp in [1000003,1008001,1013]:
            hv=relation_mod_p(hp)
            if hv is None: continue
            for rr,b in zip(rec,hv):
                a,d=rr
                if d%hp==0 or a*pow(d,-1,hp)%hp != b:
                    good=False; print('held fail',hp);break
            if not good:break
        if good:
            print('ALL RECONSTRUCTED AND HELDOUT PASS')
            break

if sum(r is not None for r in rec)==120:
    from fractions import Fraction
    rats=[Fraction(a,b) for a,b in rec]
    # clear denominators
    L=1
    for r in rats:L=math.lcm(L,r.denominator)
    ints=[r.numerator*(L//r.denominator) for r in rats]
    g=0
    for a in ints:g=math.gcd(g,abs(a))
    ints=[a//g for a in ints]
    if ints[-1]<0: ints=[-a for a in ints]
    print('LCM digits',len(str(L)),'max int digits',max(len(str(abs(a))) for a in ints if a))
    import json
    open(BASE/'M23_tetragonal_coeffs_v92.json','w').write(json.dumps({'primes':used,'coeff_order':'index=5*k+d -> W^k T^d','normalized_rationals':[[r.numerator,r.denominator] for r in rats],'primitive_integer_coeffs':ints},indent=2))
    # polynomial text
    terms=[]
    for k in range(24):
      for d in range(5):
        c=ints[5*k+d]
        if c: terms.append((c,k,d))
    with open(BASE/'M23_tetragonal_polynomial_v92.txt','w') as f:
      f.write('Primitive integer relation R(T,W)=sum c[k,d] W^k T^d\n')
      f.write('Term count = %d\n'%len(terms))
      for c,k,d in terms:f.write(f'{c} * W^{k} * T^{d}\n')
    print('terms',len(terms))
