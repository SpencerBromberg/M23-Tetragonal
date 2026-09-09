# Global rational fractional-linear height minimality

Let \(\Phi(X,Y)=Y^{23}f(X/Y)\), let \(g(x)=f(x+1)\), let
\(\Gamma(X,Y)=Y^{23}g(X/Y)\), and put
\(B=H_\infty(\Gamma)=1,938,799,398\).
Every element of \(\mathrm{PGL}_2(\mathbf Q)\) has a primitive integral
matrix representative \(M\), unique up to sign.  Write
\(D=|\det M|\), \(C=\operatorname{cont}(\Phi\circ M)\), and
\(H_M=\operatorname{pp}(\Phi\circ M)\).

## 1. Local content bound

If \(p\nmid D\), the reduction of \(M\) is invertible, so a primitive
binary form cannot become the zero form modulo \(p\); hence \(p\nmid C\).
If \(p^e\Vert D\), Smith reduction over \(\mathbf Z_p\) writes
\(M=U\operatorname{diag}(1,p^e)V\) with \(U,V\in\mathrm{GL}_2(\mathbf Z_p)\).
Content is unchanged by the right factor.  If the first column of \(U\)
reduces to a projective root of multiplicity \(m\), the first nonzero
Taylor coefficient occurs by order \(m\), so
\(v_p(C)\le me\).

A projective root of multiplicity at least three modulo \(p\ne2\) is a
common root of \(f,f',f''\).  Exact computation gives

`gcd(|Disc(f)|, |Res(f,f'')|) = 2^44 * 23^23`.

Therefore every prime other than 2 and 23 has maximum projective root
multiplicity at most two and hence \(v_p(C)\le2e\).

At 2, direct reduction gives \(f(r)\equiv2\pmod4\) for all four residue
classes \(r\pmod4\).  The point at infinity is not a root because \(f\)
is monic.  Thus \(v_2(C)\le1\), for every \(e\).

At 23, \(f(x)\equiv x^{23}-1=(x-1)^{23}\pmod{23}\).  Moreover,
\(f(1)\equiv184=23\cdot8\pmod{23^2}\) and \(f'(1)\equiv0\pmod{23}\).
Hence every \(23\)-adic point in the unique root class has value of exact
23-adic valuation one, and \(v_{23}(C)\le1\).

## 2. Determinant cutoff

Binary discriminants satisfy

\[
 |\operatorname{Disc}(H_M)|
 = |\operatorname{Disc}(\Phi)|
   \left(\frac{D^{23}}{C^2}\right)^{22}.
\]

The preceding local estimates show that
\(q=D^{23}/C^2\) is a positive integer.  If
\(H_\infty(H_M)\le B\), Hadamard's determinant bound on the Sylvester
matrix of \(h(x)=H_M(x,1)\) and \(h'\) gives

\[
 |\operatorname{Disc}(h)|^2
 \le ((24)B^2)^{22}
 \left(\frac{23\cdot24\cdot47}{6}B^2\right)^{23}.
\]

Exact integer extraction therefore gives

\[
 q\le 76,032,571.
\]

For \(p\ne2,23\) dividing \(D\), the local content bound gives
\(v_p(q)\ge19e\), but \(3^{19}>76,032,571\).  Thus no such prime occurs.
At 23, \(v_{23}(q)\ge23e-2\), and \(23^{21}\) already exceeds the bound.
At 2, the same estimate gives \(v_2(q)\ge23e-2\); since
\(2^{44}>76,032,571\), one has \(e\le1\).  Hence

\[
 |\det M|\in\{1,2\}.
\]

## 3. Determinant two

The determinant-one case is the previously certified Hutz--Stoll
reduction.  For determinant two, write \(\Gamma=\Phi\circ T\) with
\(T=\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}\) and
\(N=T^{-1}M\).  A coordinate reflection reduces determinant \(-2\) to
\(+2\) without changing height, so put \(\gamma=N/\sqrt2\in\mathrm{SL}_2(\mathbf R)\).
If \(H_\infty(H_M)\le B\), the local bound \(C\le2\) gives

\[
 H_\infty(\Gamma\circ\gamma)
 =2^{-23/2}C H_\infty(H_M)<B.
\]

The exact Hutz--Stoll bound already certified for \(\Gamma\) therefore
forces \(\cosh d(\gamma^{-1}z(\Gamma),i)<600,000,000\).  Since the
certified Julia point has imaginary part \(u>2\), the bottom row
\((c,d)\) of \(M\) satisfies

\[
 c^2+d^2<1,200,000,000,
 \qquad |c|,|d|\le34,641.
\]

Also, each raw leading or trailing coefficient is at most \(2B\).
Exact Sturm isolation and the same certified real-root neighborhoods as
in the determinant-one proof reduce all possible columns, up to
simultaneous sign, to

\[
 (-2,0),\ (-1,0),\ (0,1),\ (1,0),\ (1,1),\ (2,0),\ (2,1).
\]

Allowing independent signs on the two columns, exactly 32 primitive ordered column pairs of determinant \(\pm2\) arise from these classes.  Exact substitution and primitive-part normalization give
minimum height

\[
 372,261,710,848>B.
\]

Thus determinant two produces no tie or improvement.  Together with the
unimodular theorem and the determinant cutoff, this proves global minimum
ordinary coefficient height over the full rational fractional-linear
orbit.
