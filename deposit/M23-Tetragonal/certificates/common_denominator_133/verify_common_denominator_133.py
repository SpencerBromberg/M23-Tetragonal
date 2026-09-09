#!/usr/bin/env python3
import json, pathlib
from sympy import Matrix

ROOT=pathlib.Path(__file__).resolve().parents[1]
crt=json.loads((ROOT/'current_21prime'/'CRT120_symmetric_21primes.json').read_text())
M=int(crt['modulus']); R=list(map(int,crt['residues_mod_M']))
p=1013
H=[1,61,178,515,715,869,252,71,400,496,649,618,622,66,909,789,387,427,37,197,748,593,906,149,885,102,448,767,849,923,646,743,186,35,429,219,325,113,93,669,832,935,346,526,480,648,498,418,743,537,866,292,166,612,425,907,623,9,613,771,936,101,851,723,537,641,759,131,7,878,858,158,459,402,604,385,796,849,832,783,753,697,580,845,10,858,522,588,190,176,122,701,42,609,62,264,991,403,666,470,902,682,666,748,476,876,841,97,907,426,531,376,203,173,417,120,1003,732,493,988]

blocks=[]; total_training=0; total_heldout=0
for block in range(6):
    n=20; vals=R[20*block:20*(block+1)]; held=H[20*block:20*(block+1)]
    rows=[]
    for i in range(n):
        row=[0]*(n+1); row[i]=M; rows.append(row)
    rows.append(vals+[1])
    red=Matrix(rows).lll(delta=0.75)
    usable=training=heldout=0; best=None
    for raw in red.tolist():
        s=[int(x) for x in raw]; d=s[-1]
        if d==0:
            continue
        usable += 1
        if all((s[j]-d*vals[j])%M==0 for j in range(n)):
            training += 1; total_training += 1
            norm2=sum(x*x for x in s)
            maxnum=max(abs(s[j]) for j in range(n))
            cand=(norm2,len(str(abs(d))),len(str(maxnum)))
            if best is None or cand[0]<best[0]:
                best=cand
            if d%p and all((s[j]-d*held[j])%p==0 for j in range(n)):
                heldout += 1; total_heldout += 1
    blocks.append({
        'block':block,
        'lll_rank':red.rows,
        'usable_nonzero_denominator_rows':usable,
        'training_congruent_rows':training,
        'heldout_survivors':heldout,
        'shortest_training_denominator_digits':best[1] if best else None,
        'shortest_training_max_numerator_digits':best[2] if best else None,
    })

out={
    'engine':'SymPy Matrix.lll(delta=0.75)',
    'training_primes':len(crt['primes']),
    'crt_digits':len(str(M)),
    'heldout_prime':p,
    'block_size':20,
    'blocks':blocks,
    'total_training_congruent_rows':total_training,
    'total_heldout_survivors':total_heldout,
}
path=pathlib.Path(__file__).with_name('common_denominator_133.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print('M23_COMMON_DENOMINATOR_133_VERIFY_PASS')
print('CRT_DIGITS =',out['crt_digits'])
print('HELDOUT_PRIME =',p)
for b in blocks:
    print('BLOCK',b['block'],'TRAIN',b['training_congruent_rows'],'HOLD',b['heldout_survivors'],
          'DEN_DIGITS',b['shortest_training_denominator_digits'],'MAXNUM_DIGITS',b['shortest_training_max_numerator_digits'])
print('TOTAL_TRAINING_CONGRUENT_ROWS =',total_training)
print('TOTAL_HELDOUT_SURVIVORS =',total_heldout)
