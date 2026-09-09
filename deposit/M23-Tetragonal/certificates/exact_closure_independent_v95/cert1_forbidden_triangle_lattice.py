#!/usr/bin/env python3
"""Certificate 1: lattice combinatorics of the weighted adjoint slot space.

Proves by exhaustive enumeration (a finite check that constitutes a proof):
  L1. The weighted support {(j,k): 0<=j<=21, 0<=k<=42-2j} has 484 slots,
      253 even-k and 231 odd-k.
  L2. The forbidden odd triangle {k odd, j>=16} has exactly 15 slots with
      weight (k+2j) multiplicities (33,1),(35,2),(37,3),(39,4),(41,5) --
      the "staircase" is pure lattice geometry; the multiplicities carry
      no arithmetic content.
  L3. The q-pair digit space has 469 = 253 even + 216 odd admissible
      slots; the divisibility law r >= 18-j allows exactly 130.
  L4. The seven-band law (d=j+r in {18..21} even with j-caps 4,10,15,21;
      d in {18,19,20} odd with caps 4,10,15) allows exactly
      5+11+16+22+5+11+16 = 86 slots, all satisfying r >= 18-j.
Marker: M23_PATCH_CERT1_PASS
"""
from collections import Counter

slots = [(j, k) for j in range(22) for k in range(43-2*j)]
even = [s for s in slots if s[1] % 2 == 0]
odd = [s for s in slots if s[1] % 2 == 1]
assert (len(slots), len(even), len(odd)) == (484, 253, 231)
forb = [(j, k) for j, k in odd if j >= 16]
wm = Counter(k+2*j for j, k in forb)
assert len(forb) == 15 and sorted(wm.items()) == [(33,1),(35,2),(37,3),(39,4),(41,5)]
print("L1: 484 slots = 253 even + 231 odd: PASS")
print("L2: forbidden odd triangle {k odd, j>=16}: 15 slots, staircase "
      "(33,1)(35,2)(37,3)(39,4)(41,5): PASS  [pure lattice geometry]")

qp = [("EVEN", j, r) for j in range(22) for r in range(22-j)] + \
     [("ODD", j, r) for j in range(16) for r in range(21-j)]
assert len(qp) == 469
assert sum(1 for c, _, _ in qp if c == "EVEN") == 253
allowed = [s for s in qp if s[2] >= 18 - s[1]]
assert len(allowed) == 130
print("L3: q-pair space 469 = 253 + 216; law r>=18-j allows 130: PASS")

caps_even = {18: 4, 19: 10, 20: 15, 21: 21}
caps_odd = {18: 4, 19: 10, 20: 15}
band = []
for c, j, r in qp:
    d = j + r
    caps = caps_even if c == "EVEN" else caps_odd
    if d in caps and j <= caps[d]:
        band.append((c, j, r))
cnt = Counter((c, j+r) for c, j, r in band)
assert len(band) == 86
assert [cnt[("EVEN", d)] for d in (18, 19, 20, 21)] == [5, 11, 16, 22]
assert [cnt[("ODD", d)] for d in (18, 19, 20)] == [5, 11, 16]
assert all(r >= 18-j for _, j, r in band)
print("L4: seven-band law: 86 slots, counts (5,11,16,22|5,11,16), all "
      "within r>=18-j: PASS")
print("M23_PATCH_CERT1_PASS")
