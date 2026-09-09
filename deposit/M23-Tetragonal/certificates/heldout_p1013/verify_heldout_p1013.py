#!/usr/bin/env python3
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
crt = json.loads((ROOT/'current_21prime'/'CRT120_symmetric_21primes.json').read_text())
M = int(crt['modulus'])
R = list(map(int, crt['residues_mod_M']))
p = 1013
H = [1,61,178,515,715,869,252,71,400,496,649,618,622,66,909,789,387,427,37,197,748,593,906,149,885,102,448,767,849,923,646,743,186,35,429,219,325,113,93,669,832,935,346,526,480,648,498,418,743,537,866,292,166,612,425,907,623,9,613,771,936,101,851,723,537,641,759,131,7,878,858,158,459,402,604,385,796,849,832,783,753,697,580,845,10,858,522,588,190,176,122,701,42,609,62,264,991,403,666,470,902,682,666,748,476,876,841,97,907,426,531,376,203,173,417,120,1003,732,493,988]
assert len(R) == len(H) == 120

def rr(a,m):
    a %= m
    B = math.isqrt(m//2)
    r0,r1 = m,a
    s0,s1 = 0,1
    while abs(r1) > B:
        q = r0//r1
        r0,r1 = r1,r0-q*r1
        s0,s1 = s1,s0-q*s1
    n,d = r1,s1
    if d == 0:
        return None
    if d < 0:
        n,d = -n,-d
    if abs(n) <= B and d <= B and math.gcd(n,d)==1 and (a*d-n)%m==0:
        return n,d
    return None

rrs = [rr(x,M) for x in R]
ordinary=[]
for i,r in enumerate(rrs):
    if r:
        n,d=r
        if (n-d*H[i])%p == 0:
            ordinary.append((i,n,d))

row_candidates=[]; row_pass=[]
for row in range(24):
    tr=R[5*row:5*row+5]; ho=H[5*row:5*row+5]
    cc=pc=0
    for pivot in range(5):
        if math.gcd(tr[pivot],M)!=1 or ho[pivot]%p==0:
            continue
        inv=pow(tr[pivot],-1,M)
        complete=True; ok=True
        for j in range(5):
            if j==pivot:
                continue
            rec=rr((tr[j]*inv)%M,M)
            if rec is None:
                complete=False; break
            n,d=rec
            if (n*ho[pivot]-d*ho[j])%p != 0:
                ok=False
        if complete:
            cc += 1
            if ok:
                pc += 1
    if cc:
        row_candidates.append((row,cc))
    if pc:
        row_pass.append((row,pc))

pair_candidates=[]; pair_pass=[]
for r0 in range(23):
    idxs=list(range(5*r0,5*r0+10))
    tr=[R[i] for i in idxs]; ho=[H[i] for i in idxs]
    cc=pc=0
    for pivot in range(10):
        if math.gcd(tr[pivot],M)!=1 or ho[pivot]%p==0:
            continue
        inv=pow(tr[pivot],-1,M)
        complete=True; ok=True
        for j in range(10):
            if j==pivot:
                continue
            rec=rr((tr[j]*inv)%M,M)
            if rec is None:
                complete=False; break
            n,d=rec
            if (n*ho[pivot]-d*ho[j])%p != 0:
                ok=False
        if complete:
            cc += 1
            if ok:
                pc += 1
    if cc:
        pair_candidates.append(((r0,r0+1),cc))
    if pc:
        pair_pass.append(((r0,r0+1),pc))

out={
    'training_primes':len(crt['primes']),
    'training_modulus_digits':len(str(M)),
    'heldout_prime':p,
    'ordinary_rr_candidates':sum(x is not None for x in rrs),
    'ordinary_heldout_survivors':[{'index':i,'numerator':n,'denominator':d} for i,n,d in ordinary],
    'five_coefficient_projective_candidate_rows':[{'row':r,'candidate_pivots':c} for r,c in row_candidates],
    'five_coefficient_projective_passing_rows':[{'row':r,'passing_pivots':c} for r,c in row_pass],
    'ten_coefficient_projective_candidate_pairs':[{'rows':list(pair),'candidate_pivots':c} for pair,c in pair_candidates],
    'ten_coefficient_projective_passing_pairs':[{'rows':list(pair),'passing_pivots':c} for pair,c in pair_pass],
}
(pathlib.Path(__file__).with_name('heldout_p1013.json')).write_text(json.dumps(out,indent=2)+'\n')
print('M23_HELDOUT_P1013_VERIFY_PASS')
print('training_primes =',out['training_primes'])
print('training_modulus_digits =',out['training_modulus_digits'])
print('ordinary_rr_candidates =',out['ordinary_rr_candidates'])
print('ordinary_heldout_survivors =',ordinary)
print('five_coefficient_candidate_rows =',row_candidates)
print('five_coefficient_passing_rows =',row_pass)
print('ten_coefficient_candidate_pairs =',pair_candidates)
print('ten_coefficient_passing_pairs =',pair_pass)
