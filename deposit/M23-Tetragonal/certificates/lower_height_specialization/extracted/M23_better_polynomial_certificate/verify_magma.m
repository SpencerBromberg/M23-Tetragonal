// Independent Magma check for the translated lower-height polynomial.
// The exact identity g(x)=f2(x+1) already proves equality of splitting fields.
// This file optionally reruns Magma's full Galois certification on g itself.
SetVerbose("GaloisGroup", 1);
SetSeed(1);
P<x> := PolynomialRing(Rationals());

f2 := x^23
    + 46*x^21 - 598*x^20 + 1679*x^19 - 21620*x^18 + 127420*x^17
    - 361974*x^16 + 2223732*x^15 - 9392096*x^14 + 17344116*x^13
    - 71999476*x^12 + 320807726*x^11 - 436105484*x^10 + 83587888*x^9
    - 2463757240*x^8 + 9451874955*x^7 - 5728074376*x^6 - 26037806834*x^5
    + 63691532334*x^4 - 67357061907*x^3 + 38754121124*x^2
    - 11217790920*x + 1243077066;

g := x^23 + 23*x^22 + 299*x^21 + 2139*x^20 + 8234*x^19 - 8510*x^18
    - 280094*x^17 - 1592842*x^16 - 3657782*x^15 + 3526406*x^14
    + 44362906*x^13 + 63064206*x^12 - 221821982*x^11 - 727073654*x^10
    + 229352458*x^9 + 1938799398*x^8 - 1207282236*x^7 - 435568756*x^6
    + 1165914252*x^5 + 727883760*x^4 - 482357150*x^3 - 983586582*x^2
    + 60455178*x + 242325562;

assert Evaluate(f2, x+1) eq g;
assert IsIrreducible(g);
printf "translation identity and irreducibility: PASS\n";

G, Rts, S := GaloisGroup(g);
k := TransitiveGroupIdentification(G);
printf "returned group = 23T%o, order %o\n", k, #G;
assert k eq 5;
assert #G eq 10200960;
ok := GaloisProof(g, S);
printf "GaloisProof = %o\n", ok;
assert ok;
printf "CERTIFIED: Gal(g/Q) = 23T5 = M23\n";
