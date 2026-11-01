# Independent enclosure derivation

Written from PROOF.md without opening target verify_linear.py. The checker imports no target module. All mathematical work runs on the CPU pod; local work is source editing and reading only.

Let e_i be the exact rational nodes and h_i the exact rational heights, extended by zero. On each cell the slope is s_i=(h_{i+1}-h_i)/(e_{i+1}-e_i). With zero exterior slopes, let j_i=s_i-s_{i-1}. Then rho''=sum_i j_i delta_(e_i). Two integrations by parts give

    U(x)=sum_i j_i G(x-e_i),
    G(t)=t^2 log|t|/2-3t^2/4, G(0)=0.

The exact identities sum j_i=sum j_i e_i=0 and sum j_i e_i^2/2=m are checked. They also fix the sign and indexing of the formula. For nonreal z the same formula uses Re G(z-e_i) with a continuous logarithm along the integration segment. Real parts and the two cancellation identities remove branch-dependent affine terms.

Direct logarithmic integrals use a different expression: on each original density cell, write z=x-r, rho(x)=s z+k, k=rho(r). A primitive is

    Re [(s z^2/2+k z) log z - s z^2/4-k z].

At real roots use log|z| and the continuous zero values. At each root r, this integral is cross-checked against the slope-jump U(r). Add m log(lc Q) and sum over all certified roots. FLINT exact factorization checks primitivity and irreducibility; complex root balls account for every root with multiplicity one.

For a closed exact interval [c-r,c+r], the potential is bounded using an order-eight Taylor polynomial. For a density knot t=c-e with |t|>2r, the coefficients are

    G(t), t(log|t|-1), log|t|/2,
    (-1)^(n-3)/(n(n-1)(n-2)t^(n-2)), n>=3.

The Lagrange remainder is bounded in absolute value by

    r^(N+1)/((N+1)N(N-1)(|t|-r)^(N-1)).

For a near knot |t|<=2r (and |t|+r<1), G''(v)=log|v|<=0. Thus

    -2r^2(1-log r) <= G(t+h)-G(t)-hG'(t) <= 0.

Indeed the absolute remainder is at most r times the integral of -log|v| on an interval of length 2r, whose largest possible value is 2r(1-log r). Positive slope jumps incur the negative remainder; negative jumps can discard this nonnegative contribution. This bound includes endpoints and t=0 without evaluating log zero.

For a root alpha at distance d=|c-alpha|>2r, use the real part of the logarithm's Taylor series; its absolute tail after order N is at most

    (r/d)^(N+1)/((N+1)(1-r/d)).

Otherwise -b log|x-alpha| is bounded below by -b log(d+r), including a root in the interval. Leading coefficients contribute -b log(lc Q) explicitly.

The polynomial in h is evaluated on an Arb ball containing the closed interval [-r,r]. All coefficients, logarithms, tails, and acceptance decisions use 192-bit Arb arithmetic; exact rational comparisons choose the cases. Floating point is used only for progress timing and diagnostics.

Each rejected interval is bisected at its exact rational midpoint into two closed intervals. Every accepted leaf is saved with its parent cell, rational endpoints, and positive lower bound. Independently of the recursive traversal, leaves are sorted and checked to start and finish at the original cell endpoints, with equality of adjacent endpoints. Every cell with either height positive is included. The closed union is precisely the support; zero-density gaps are handled by the mathematical minimum principle, not assumed to contain no problem.

The small reported certificate margin is an interval lower bound, not the value of the actual minimum. Numerical minimization is used only to locate diagnostic points; their values are reevaluated with Arb and direct polynomial evaluation. It never substitutes for support coverage.
