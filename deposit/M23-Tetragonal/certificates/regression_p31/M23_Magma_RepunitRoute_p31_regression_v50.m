print "M23_REPUNIT_ROUTE_REGRESSION_BEGIN";
p := 31;
print "PRIME =", p;
k := GF(p);
A<t> := PolynomialRing(k);
AY<u> := PolynomialRing(A);
b := [ A!0 : i in [1..23] ];
b[2] := (-31740);
b[3] := (139840);
b[4] := (399583002);
b[5] := (-145711496856) + (-6335282472)*t^2;
b[6] := (-56775283856672) + (-126169394688)*t + (-2477993869792)*t^2;
b[7] := (2353269564340584) + (90885386323584)*t + (69899701328472)*t^2;
b[8] := (149300207182735461) + (8192572384010400)*t + (7690149863466435)*t^2;
b[9] := (-18518819166678845600) + (-1840547483855390880)*t + (-181770736706490688)*t^2;
b[10] := (5230550645390156540328) + (-2949856937205019309008)*t + (-72054287980811706816)*t^2 + (-128254649443696491696)*t^3 + (-13020414497067723624)*t^4;
b[11] := (1780732430570005145756424) + (328246325556276597513504)*t + (54631308621463631478480)*t^2 + (14271579372012025978848)*t^3 + (-990949588424086241496)*t^4;
b[12] := (-76226757591131329290382566) + (18690086460439084348196768)*t + (-1792012713435085812396596)*t^2 + (813235953706896182384992)*t^3 + (66027458205719035669658)*t^4;
b[13] := (-3875581272261943207482299424) + (-1272104594358533124234481632)*t + (-28978388560551190877922912)*t^2 + (-57786540191941872595499808)*t^3 + (5516437740989208066312576)*t^4;
b[14] := (6910353957998684922380692854804) + (-1182608554123854417720035133648)*t + (412254292452214768806833373492)*t^2 + (-112352637513414760653499408224)*t^3 + (-268507225604280859145871012)*t^4 + (-2649342360462542679225805776)*t^5 + (-223024171179988438782332580)*t^6;
b[15] := (88514359848681198441339995596152) + (66671928552879672571499601603168)*t + (3059716724605899534195931323384)*t^2 + (6093776240613995660154706708800)*t^3 + (-371653155370716716161147483224)*t^4 + (138912901665864324408428455008)*t^5 + (-14667842854307851869352629528)*t^6;
b[16] := (-14822900658422153993723820208138521) + (1452165788444071252451127163115616)*t + (-1196200268441385838255312662361293)*t^2 + (152476099696291565105489515500864)*t^3 + (-18425610081301084564482099762651)*t^4 + (3884280726976625226796090157664)*t^5 + (241847438376053797282595566017)*t^6;
b[17] := (-37724221633317849821253387809988360) + (-93620123757549254929872648043284768)*t + (-11591484764381099858905769639925000)*t^2 + (-9513428443869186509439824732200896)*t^3 + (-183430444487395254543895866578136)*t^4 + (-236651664369455642319930663132960)*t^5 + (10836296771070547980591633146088)*t^6;
b[18] := (16313110767605628611806394020375426680) + (-1703402197188364617307749292365354672)*t + (2032301462095753658490946401570018888)*t^2 + (-129191517104013848445270031021659552)*t^3 + (66730153393082520871679625793751304)*t^4 + (-2396348444989357771279301994069936)*t^5 + (400540174533969410487588483397176)*t^6;
b[19] := (1042289893847058025879040880566456994672) + (1104530349771039454874170579417691649312)*t + (333274964387577672914755115261072851872)*t^2 + (177834072940944271142086313365199175072)*t^3 + (33713454389094699008417352295983275904)*t^4 + (9164364930275864576578604398808309088)*t^5 + (1384908138976241457553823117871919200)*t^6 + (153061208206234369985720974684614624)*t^7 + (20149993182414522853209191222911248)*t^8;
b[20] := (-146676777647046733368141103212933368381760) + (47248616899864784417985500825997188919648)*t + (-31059705710059767703037569543512462548640)*t^2 + (6607721732088306642342716918797881821280)*t^3 + (-1955502285158879811215641219926699021600)*t^4 + (309985639130842180423097734341104122656)*t^5 + (-43709389872759776381483477984786375904)*t^6 + (4870010697957528157139945192741841696)*t^7 + (-232445893979612361670227977985803808)*t^8;
b[21] := (-583036461536128584530382312820824598910208) + (-368473907347056952685077902822090105858432)*t + (-250848528005315471356262109412820000004480)*t^2 + (-37680222996348867437415628143362965239168)*t^3 + (-35962460177914556876631229408057982882688)*t^4 + (-781880924013941195027394050639518996608)*t^5 + (-1778174960398790720078613827770306312320)*t^6 + (6949635305793713011094772062706710400)*t^7 + (-27863654688345929867754261488819291520)*t^8;
b[22] := (11431517330337822220551952458477060842204160) + (-25809360722373312049323407405759781746499072)*t + (1790686750434671697130166091520203419410944)*t^2 + (-2397163462662484578984858522494100321357312)*t^3 + (173980809918790171381794345879079128660480)*t^4 + (-86205619580095394601076747481250376567296)*t^5 + (9150869839919949982069223354218905122304)*t^6 + (-1337829690063830893124127624391955581440)*t^7 + (175303343058828611905721103152276390400)*t^8;
b[23] := (-636600898150484328800300139882417037526114304) + (-1454239686461893222545991110390844910530811904)*t + (-352689535457875303125555026318811624811247616)*t^2 + (103352070659831277568590719722025029106073600)*t^3 + (15315119499810615305853634694027898506182656)*t^4 + (32961183987151578191197448811534368526176256)*t^5 + (4181405479539036486753938644987111713705984)*t^6 + (1801978935221572204239176449303804249128960)*t^7 + (172171892687016253525660128823927540899840)*t^8 + (29729556023869614361220075333404061337600)*t^9 + (2001532669196828324472937945546023168000)*t^10;

q := t^2 + 23;
G := u^23 + &+[ b[j]*q^(j - ((5*j) div 23))*u^(23-j) : j in [2..23] ];
assert Degree(G) eq 23;
X<uu> := FunctionField(G : Check := false);
if Degree(X) eq 23 then
    print "CHECK 1: mod-p function field degree 23: PASS";
else
    error "CHECK 1 FAIL";
end if;

SetUseMontes(true);


qfac := [ z[1] : z in Factorization(q) ];
if #qfac lt 1 or #qfac gt 2 then
    error "unexpected factorization of t^2+23";
end if;

qprimes := [];
qpolys := [];
totalPdeg := 0;

for r in qfac do
    Montes(X,r);
    Ps := X`PrimeIdeals[r];
    if #Ps ne 1 then
        error "unexpected number of primes above a factor of t^2+23";
    end if;
    P := Ps[1];
    if Valuation(X!r,P) ne 23 then
        error "unexpected ramification above t^2+23";
    end if;
    if Valuation(X!uu,P) ne 19 then
        error "unexpected valuation of integral generator u above t^2+23";
    end if;
    Append(~qprimes,P);
    Append(~qpolys,r);
    totalPdeg +:= Degree(P);
end for;

if totalPdeg ne 2 then
    error "P23 total degree failure";
end if;
print "Q_FACTORS =", #qfac;
print "CHECK 2: P23 prime data recovered, total degree 2: PASS";


// Avoid Divisor(dt) and Basis(Kdt) entirely.
// Magma directly computes a basis of holomorphic differentials.
// If omega = f dt is holomorphic, then f lies in L(div(dt)), so
// BK := omega/dt is exactly a canonical Riemann-Roch basis for our use.
print "CHECK 3 START: direct holomorphic differential basis";
time_diff := Cputime();
dt := Differential(X!t);
HD := BasisOfDifferentialsFirstKind(X);
print "HOLOMORPHIC_DIFFERENTIAL_BASIS_LENGTH =", #HD;
print "TIME_HOLOMORPHIC_DIFFERENTIAL_BASIS =", Cputime(time_diff);
if #HD ne 4 then
    error "holomorphic differential dimension failure";
end if;

BK := [ omega/dt : omega in HD ];
if #BK ne 4 then
    error "canonical function basis conversion failure";
end if;
print "CHECK 3: holomorphic differentials give four canonical functions: PASS";

// Impose P23 by principal-part cancellation instead of forming K-P23.
//
// At every prime P above q=t^2+23:
//   v_P(q-factor)=23, v_P(uu)=19.
// Hence pi = uu^17 / r^14 has valuation 17*19-14*23 = 1.
// For f in L(K), v_P(f)>=-22.  The condition f in L(K-P)
// is exactly that the residue of f*pi^22 vanish at P.
//
// A degree-d prime contributes d linear equations over F_p.
// Since deg(P23)=2, the resulting kernel must have dimension 2.
print "CHECK 5 START: cheap Reduction kernel for L(K-P23)";

condition_rows := [ [] : i in [1..4] ];
total_conditions := 0;

for h in [1..#qprimes] do
    P := qprimes[h];
    r := qpolys[h];
    dP := Degree(P);
    RF := ResidueField(P);

    piP := (X!uu)^17 / (X!r)^14;
    if Valuation(piP,P) ne 1 then
        error "constructed local parameter does not have valuation 1";
    end if;

    for i in [1..4] do
        gi := BK[i] * piP^22;
        vgi := Valuation(gi,P);

        if vgi lt 0 then
            error "canonical section times pi^22 is not regular at P23";
        end if;

        if vgi gt 0 then
            cc := [ k!0 : j in [1..dP] ];
        else
            ri := Reduction(gi,P);
            flag, rfi := IsCoercible(RF,ri);
            if not flag then
                error "Reduction output does not coerce to OM residue field";
            end if;

            cc0 := Eltseq(rfi);
            cc := [ k!x : x in cc0 ];
            while #cc lt dP do
                Append(~cc,k!0);
            end while;

            if #cc ne dP then
                error "unexpected residue-coordinate length";
            end if;
        end if;

        for j in [1..dP] do
            Append(~condition_rows[i], cc[j]);
        end for;
    end for;

    total_conditions +:= dP;
end for;

if total_conditions ne 2 then
    error "P23 should impose exactly two scalar conditions";
end if;

C := Matrix(k,4,total_conditions,
            &cat[ condition_rows[i] : i in [1..4] ]);
N := NullspaceMatrix(C);

print "RESIDUE_CONDITION_RANK =", Rank(C);
print "RESIDUE_KERNEL_DIMENSION =", Nrows(N);

if Rank(C) ne 2 or Nrows(N) ne 2 or Ncols(N) ne 4 then
    error "residue kernel does not have expected dimension 2";
end if;

BD := [];
for j in [1..2] do
    fj := &+[ (X!N[j,i])*BK[i] : i in [1..4] ];
    Append(~BD,fj);
end for;

// Direct local verification of the defining condition.
for P in qprimes do
    for f in BD do
        if Valuation(f,P) lt -21 then
            error "kernel section does not lie in L(K-P23)";
        end if;
    end for;
end for;

print "TETRAGONAL_BASIS_LENGTH =", #BD;
print "CHECK 5: L(K-P23) dimension 2 recovered by cheap Reduction kernel: PASS";

print "CHECK 5 START: kernel-first symmetric first-jet frame";

if #qprimes ne 2 then
    error "kernel-first split-frame script requires Q_FACTORS = 2";
end if;

roots := [];
firstjets := [ [ k!0, k!0 ] : i in [1..2] ];

for h in [1..2] do
    P := qprimes[h];
    r := qpolys[h];

    if Degree(r) ne 1 or Degree(P) ne 1 then
        error "split frame requires degree-one factors and primes";
    end if;

    root := -(k!Coefficient(r,0))/(k!Coefficient(r,1));
    Append(~roots,root);

    piP := (X!uu)^17 / (X!r)^14;
    if Valuation(piP,P) ne 1 then
        error "local parameter valuation is not one";
    end if;

    RF := ResidueField(P);

    // BD already lies in L(K-(b'+c')), so the constant jet coefficient
    // of BD[i]*piP^22 is zero.  The first nonzero jet coefficient is
    // therefore obtained directly from BD[i]*piP^21.
    for i in [1..2] do
        gg := BD[i]*piP^21;
        if Valuation(gg,P) lt 0 then
            error "kernel basis fails first-jet regularity";
        end if;

        aa := k!0;
        if Valuation(gg,P) eq 0 then
            ri := Reduction(gg,P);
            flag, rfi := IsCoercible(RF,ri);
            if not flag then
                error "first-jet residue does not coerce to residue field";
            end if;
            ee := Eltseq(rfi);
            if #ee ne 1 then
                error "degree-one residue field returned non-scalar coordinates";
            end if;
            aa := k!ee[1];
        end if;
        firstjets[i][h] := aa;
    end for;
end for;

if roots[1] eq roots[2] or roots[1] + roots[2] ne 0 then
    error "unexpected roots of t^2+23";
end if;

two := k!2;
if two eq 0 then
    error "characteristic two not supported";
end if;

// Rows correspond to BD[1],BD[2]; columns are trace and divided skew-trace
// of the first jet at the conjugate pair.
Jker := ZeroMatrix(k,2,2);
for i in [1..2] do
    jb := firstjets[i][1];
    jc := firstjets[i][2];
    Jker[i,1] := (jb+jc)/two;
    Jker[i,2] := (jb-jc)/(roots[1]-roots[2]);
end for;

print "KERNEL_FIRST_JET_MATRIX =", Jker;
print "KERNEL_FIRST_JET_RANK =", Rank(Jker);

if Rank(Jker) ne 2 then
    error "kernel first-jet frame is singular";
end if;

// Rows of Cmap combine BD so that the two first-jet functionals are e1,e2.
Cmap := Jker^-1;
print "KERNEL_TO_SYMMETRIC_MATRIX =", Cmap;

print "CHECK 5: kernel-first symmetric frame recovered L(K-P23): PASS";

// The symmetric coordinate is now fixed directly from the first-jet frame.
S1 := (X!Cmap[1,1])*BD[1] + (X!Cmap[1,2])*BD[2];
S2 := (X!Cmap[2,1])*BD[1] + (X!Cmap[2,2])*BD[2];
w := S1/S2;

// Compute the degree-23 relation as the characteristic polynomial of
// multiplication by w on the 23-dimensional coefficient-field vector space.
// Since w has degree 23, characteristic polynomial = minimal polynomial.
// This avoids AbsoluteMinimalPolynomial.
print "CHECK 6 START: multiplication-matrix characteristic polynomial";
time_cp := Cputime();
Kt := BaseRing(X);

rows := [];
for j in [0..22] do
    ee := ElementToSequence(w*(X!uu)^j);
    if #ee ne 23 then
        error "unexpected power-basis coordinate length";
    end if;
    Append(~rows,ee);
end for;

Mw := Matrix(Kt,23,23,&cat rows);
cp := CharacteristicPolynomial(Mw);
print "TIME_CHARACTERISTIC_POLYNOMIAL =", Cputime(time_cp);

if Degree(cp) ne 23 then
    error "characteristic polynomial degree failure";
end if;
if Evaluate(cp,w) ne 0 then
    error "characteristic polynomial does not annihilate symmetric coordinate";
end if;
print "CHECK 6: degree-23 characteristic polynomial annihilates symmetric coordinate: PASS";

// Clear coefficient-field denominators.
cs := Coefficients(cp);
den := A!1;
for coef in cs do
    den := Lcm(den,A!Denominator(coef));
end for;

RW<W> := PolynomialRing(A);
H := RW!0;
for i in [0..#cs-1] do
    H +:= A!(den*cs[i+1])*W^i;
end for;

// Remove polynomial content.
nz := [ Coefficient(H,i) : i in [0..Degree(H)] | Coefficient(H,i) ne 0 ];
content := nz[1];
for qcoef in nz[2..#nz] do
    content := GCD(content,qcoef);
end for;
if not IsUnit(content) then
    H := H div content;
end if;

// Same row-major scalar normalization used by all symmetric tables.
scalar := k!0;
for i in [0..Degree(H)] do
    hi := Coefficient(H,i);
    if hi ne 0 and scalar eq 0 then
        for j in [0..Degree(hi)] do
            cij := k!Coefficient(hi,j);
            if cij ne 0 then
                scalar := cij;
                break;
            end if;
        end for;
    end if;
end for;
if scalar eq 0 then
    error "zero relation";
end if;
H := (A!(1/scalar))*H;

degT := Max([Degree(Coefficient(H,i)) :
             i in [0..Degree(H)] | Coefficient(H,i) ne 0]);

print "DIRECT_CHARPOLY_BIDEGREE_W_T =", Degree(H), degT;
if Degree(H) ne 23 or degT ne 4 then
    error "direct characteristic-polynomial relation is not bidegree (23,4)";
end if;

flat := [];
for i in [0..23] do
    hi := Coefficient(H,i);
    for j in [0..4] do
        Append(~flat,Integers()!Coefficient(hi,j));
    end for;
end for;

print "SYMMETRIC_FLAT120 =", flat;

expected := [ 1, 19, 24, 14, 27, 3, 22, 12, 4, 4, 0, 19, 14, 21, 17, 22, 29, 30, 12, 27, 21, 27, 1, 20, 12, 27, 7, 9, 22, 19, 26, 23, 30, 0, 27, 16, 24, 24, 15, 18, 2, 23, 10, 2, 16, 8, 28, 2, 27, 7, 22, 25, 1, 22, 26, 21, 3, 12, 9, 27, 7, 2, 18, 21, 12, 14, 28, 18, 23, 30, 3, 9, 25, 1, 8, 26, 28, 9, 1, 28, 14, 6, 9, 9, 9, 28, 5, 15, 2, 20, 28, 17, 12, 12, 3, 16, 15, 24, 12, 12, 23, 6, 27, 26, 18, 22, 10, 14, 11, 10, 8, 25, 2, 30, 20, 26, 28, 10, 13, 2 ];

if flat ne expected then
    error "direct differential/charpoly table differs from established p=31 symmetric table";
end if;
print "DIRECT_DIFF_CHARPOLY_MATCHES_ESTABLISHED_P31: PASS";
print "M23_REPUNIT_ROUTE_REGRESSION_PASS";
