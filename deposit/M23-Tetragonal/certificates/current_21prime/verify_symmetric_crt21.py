import json,math,pathlib
root=pathlib.Path(__file__).resolve().parent
c=json.load(open(root/"CRT120_symmetric_21primes.json"))
d=json.load(open(root/"symmetric_tables_21primes.json"))
runs={r["prime"]:r["flat120"] for r in d["runs"]}
assert math.prod(c["primes"])==c["modulus"]
assert len(c["residues_mod_M"])==120
for p in c["primes"]:
    assert len(runs[p])==120
    for i,x in enumerate(runs[p]):
        assert c["residues_mod_M"][i]%p==x
print("M23_SYMMETRIC_CRT21_VERIFY_PASS")
print("accepted_primes =",len(c["primes"]))
print("digits =",c["modulus_digits"])
print("coefficient_checks =",len(c["primes"])*120)
print("rr_count =",c["rational_reconstruction_count"])
print("ordinary_heldout_survivors =",len(c["heldout_before_inclusion"]["ordinary_survivors"]))
print("row_projective_passing_rows =",len(c["heldout_before_inclusion"]["row_projective_passing_rows"]))
print("two_row_projective_passing_pairs =",len(c["heldout_before_inclusion"]["two_row_projective_passing_pairs"]))
print("stable_20_to_21 =",len(c["rr_stable_20_to_21"]))
