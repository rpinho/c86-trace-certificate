# Why the certificates bound C86

Let `mu` be the finite positive measure whose density is given by the certificate's exact rational node heights, linearly interpolated on the exact rational edges and zero elsewhere. Let `m=mu(R)>0`, `T=int x dmu`, and let the selected `Q_j` be distinct primitive irreducible integer polynomials with positive leading coefficients. Their roots may be complex. All polynomial arrays in our certificates are constant coefficient first.

The separate checker establishes:

1. Every edge is rational and ordered, every density and weight `b_j` is nonnegative, and the support lies strictly inside the positive real axis.
2. `sum b_j deg(Q_j) < m`, exactly.
3. `int log|Q_j| dmu > 0` for each selected polynomial, using certified roots and Arb analytic integrals.
4. `f(x)=U_mu(x)-sum b_j log|Q_j(x)| > 0` on every support cell, including its endpoints, with `U_mu(z)=int log|z-x| dmu(x)`.
5. The declared rational bound is exactly `T/m`.

The node density is bounded and continuous, so its logarithmic potential is continuous. Away from the support and the finitely many auxiliary roots, `f` is harmonic. At an auxiliary root outside the support it tends to positive infinity; at infinity its leading term is `(m-sum b_j deg(Q_j)) log|z|`, which tends to positive infinity. The minimum principle therefore extends item 4 to `f>=0` throughout the complex plane. Checking support cells is sufficient, including when the selected auxiliaries have nonreal roots.

For any primitive irreducible integer polynomial `P` distinct from the selected polynomials, write its leading coefficient as `c` and its roots as `alpha_k`. The resultant identity gives

    int log|P| dmu
      = m log|c| + sum_k U_mu(alpha_k)
      >= (m-sum_j b_j deg(Q_j)) log|c|
         + sum_j b_j log|Res(P,Q_j)|
      >= 0.

Every resultant here is a nonzero integer. The selected polynomials pass their own integral checks, and integer constants and factorization cover every other nonzero integer polynomial. Thus `mu/m` is an arithmetic probability measure in the sense of Smith's Proposition 5.15. Nonmonicity contributes the constant `log(lc Q_j)` to each `log|Q_j|`; the linear checker includes it both in the direct integrals and the potential.

Choose a compact positive interval of length greater than four containing the support. Smith's Theorem 1.5 supplies distinct totally positive algebraic integers whose conjugate distributions converge to `mu/m`. Their normalized traces converge to `T/m`, proving `C86 <= T/m`. Polynomial degrees restrict the search pool only.

## Implementation boundary

`search_linear.py` uses floating LP and local minimization only. It cannot certify a result. `verify_linear.py` imports no search module; it forms exact rational slope jumps independently, factors with FLINT, encloses roots with acb, integrates the density analytically, and covers every support cell with Arb Taylor bounds and exact rational bisections. Polynomial and root remainder bounds are geometric; near an edge it uses the correct convex tangent or concave chord; near a root it uses a curvature enclosure or a maximal-distance lower bound. Successful receipts contain the certificate SHA256 and minimum proven positive lower bounds. This is separately written same-author code, not an independent human audit.

Primary theorem: Alexander Smith, *Algebraic integers with conjugates in a prescribed distribution*, Theorem 1.5 and Proposition 5.15, https://arxiv.org/html/2111.12660v2 . Method credits and prior code: PRIOR_ART.md and METHOD.md.
