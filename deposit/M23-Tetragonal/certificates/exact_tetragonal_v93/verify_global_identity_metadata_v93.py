import re,json,math,sympy as sp
from pathlib import Path
BASE=Path(__file__).resolve().parent
T,V=sp.symbols('t v'); q=sp.Poly(T*T+23,T,domain=sp.ZZ)
src=(BASE/'M23_qpair_full_rows_p100207139_v86.m').read_text(); b={}
for j in range(2,24):
    m=re.search(rf'b\[{j}\]\s*:=\s*(.*?);',src,re.S)
    e=sp.sympify(re.sub(r'\s+',' ',m.group(1)).replace('^','**'),locals={'t':T})
    b[j]=sp.Poly(e,T,domain=sp.ZZ)
G=[sp.Poly(0,T,domain=sp.ZZ) for _ in range(24)];G[23]=sp.Poly(1,T,domain=sp.ZZ)
for j in range(2,24):G[23-j]=b[j]*(q**(j-(5*j)//23))
wg=max((p.degree() if not p.is_zero else -999)+2*i for i,p in enumerate(G))
wh=[]
expr=[]
for nm in ['M23_H1_integer_v91.txt','M23_H2_integer_v91.txt']:
    e=sp.sympify((BASE/nm).read_text(),locals={'t':T,'v':V});expr.append(e)
    PV=sp.Poly(e,V,domain=sp.ZZ[T]);hc=[]
    for j in range(22):
        cj=sp.Poly(PV.nth(j),T,domain=sp.ZZ)
        if j<=18:hj=cj*q**(18-j)
        else:
            hj,rr=sp.div(cj,q**(j-18),domain=sp.ZZ);assert rr.is_zero
        hc.append(hj)
    wh.append(max((p.degree() if not p.is_zero else -999)+2*j for j,p in enumerate(hc)))
D=json.load(open(BASE/'M23_tetragonal_coeffs_v92.json'));c=D['primitive_integer_coeffs']
assert len(c)==120
g=0
for x in c:g=math.gcd(g,abs(int(x)))
term=sum(1 for x in c if x)
degT=max(d for k in range(24) for d in range(5) if c[5*k+d]);degW=max(k for k in range(24) for d in range(5) if c[5*k+d])
p1=sp.Poly(expr[0].subs(T,0),V,domain=sp.ZZ);p2=sp.Poly(expr[1].subs(T,0),V,domain=sp.ZZ)
det=int(p1.nth(0))*int(p2.nth(1))-int(p1.nth(1))*int(p2.nth(0))
print('M23_TETRAGONAL_GLOBAL_IDENTITY_METADATA_V93_BEGIN')
print('G_MONIC_U_DEGREE = 23')
print('G_MAX_WEIGHT =',wg)
print('H1_H2_MAX_WEIGHTS =',wh)
print('HOMOGENIZED_WEIGHT_BOUND =',4+23*42)
print('R_TERM_COUNT =',term)
print('R_COEFFICIENT_GCD =',g)
print('R_DEG_T =',degT)
print('R_DEG_Z =',degW)
print('NONPROPORTIONAL_MINOR_DEG_0_1 =',det)
assert wg<=46 and wh==[42,42] and term==120 and g==1 and degT==4 and degW==23 and det!=0
print('M23_TETRAGONAL_GLOBAL_IDENTITY_METADATA_V93_PASS')
