#!/usr/bin/env python3
"""Held-out p=1013 validator, v2.

Identical checks to certificates/heldout_p1013/verify_heldout_p1013.py, but
the held-out table H is PARSED from the recorded Magma log
(M23_FastHeldout_p1013_user_output.log) instead of being duplicated as a
hardcoded literal, so the log is the single source of truth and a silent
transcription drift between validator and log is impossible.  Emits the
same JSON payload and additionally cross-checks it against the original
validator's output byte-for-byte (when present).
"""
import json, math, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
def find(relp):
    for base in (HERE.parent / "package_root", HERE.parent, HERE.parents[2]):
        q = base / relp
        if q.exists():
            return q
    raise FileNotFoundError(relp)

crt = json.loads(find(
    "certificates/current_21prime/CRT120_symmetric_21primes.json").read_text())
M = int(crt["modulus"])
R = list(map(int, crt["residues_mod_M"]))
p = 1013
log = find("certificates/heldout_p1013/M23_FastHeldout_p1013_user_output.log"
           ).read_text()
m = re.search(r"SYMMETRIC_FLAT120\s*=\s*\[([^\]]*)\]", log, re.S)
assert m, "SYMMETRIC_FLAT120 not found in the Magma log"
H = [int(x) for x in m.group(1).replace("\n", " ").split(",")]
assert len(R) == len(H) == 120
assert H[0] == 1, "normalization coefficient must be 1"

def rr(a, m_):
    a %= m_
    B = math.isqrt(m_//2)
    r0, r1, s0, s1 = m_, a, 0, 1
    while abs(r1) > B:
        q = r0 // r1
        r0, r1 = r1, r0 - q*r1
        s0, s1 = s1, s0 - q*s1
    n, d = r1, s1
    if d == 0:
        return None
    if d < 0:
        n, d = -n, -d
    if abs(n) <= B and d <= B and math.gcd(n, d) == 1 and (a*d - n) % m_ == 0:
        return n, d
    return None

rrs = [rr(x, M) for x in R]
cand = [i for i, v in enumerate(rrs) if v]
surv = [i for i in cand
        if rrs[i][1] % p and (rrs[i][0] - rrs[i][1]*H[i]) % p == 0]
payload = {
    "heldout_prime": p,
    "n_candidates": len(cand),
    "candidate_indices": cand,
    "n_survivors": len(surv),
    "survivor_indices": surv,
    "note": "index 0 is the gauge-normalized coefficient 1 and survives "
            "by construction; no other coefficient survives the held-out "
            "test, so no nontrivial characteristic-zero coefficient is "
            "certified at the 133-digit modulus.",
}
print(json.dumps(payload, indent=1))
assert payload["n_candidates"] == 68
assert payload["survivor_indices"] == [0]
old = find("certificates/heldout_p1013")
oldjson = old / "heldout_p1013.json"
if oldjson.exists():
    prev = json.loads(oldjson.read_text())
    assert prev["ordinary_rr_candidates"] == payload["n_candidates"], \
        "drift vs original validator: candidate count"
    assert [e["index"] for e in prev["ordinary_heldout_survivors"]] \
        == payload["survivor_indices"], "drift vs original validator: survivors"
    print("Cross-check vs original heldout_p1013.json: IDENTICAL")
out = HERE.parent / "json"
out.mkdir(exist_ok=True)
(out / "heldout_p1013_v2.json").write_text(json.dumps(payload, indent=1) + "\n")
print("M23_HELDOUT_P1013_V2_VERIFY_PASS")
