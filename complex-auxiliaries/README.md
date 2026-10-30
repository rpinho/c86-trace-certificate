# C86 <= 1.80697883 (unrefereed)

Exact upper bound on C86, the Schur-Siegel-Smyth trace constant, Tao table
[86a](https://teorth.github.io/optimizationproblems/constants/86a.html).

    C86 <= 135523412047086487 / 75000000000013500 = 1.8069788272941...

## What changed

Smith's criterion does not require the auxiliary polynomials to have real roots. Adding integer polynomials with complex
roots to the certificate, on an adaptive piecewise-linear density, lowers the bound. Two degree-8 polynomials with one
conjugate pair each give about 90% of the gain below Tomar's public 1.8070808326. `PROOF.md` gives the argument.

## Credit

Smith's theorem and the Orloski, Sardari and Smith construction are the base, with the enlarged sets from Koshta and from
Niedbala Giraudin's PR 270. Tomar's public certificate (1.8070808326, preprint, 21 October 2026) is the best earlier bound
I found. Both degree-8 polynomials are not new: they are in Flammang 2009, Table 1, rows 22 and 23, and McKee 2011, Table 1,
rows 21 and 23, on the auxiliary-function side. What is new here is using them in this certificate.

## Check it

Needs Python 3 and python-flint.

    python3 verify_linear.py certificate.json --output replay.json

`certificate.json` holds the exact density, polynomials and weights. `verification.json` is the job's receipt and
`final-negative-controls.json` records corrupted certificates being rejected.

## Status

Unrefereed. No proof-assistant formalization and no independent human review. The checker was written by an AI agent,
separately from the search. A separate AI review wrote its own verifier and found no mathematical gap. That is not a
second party.

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also
prepared the certificate, checker and this text. This does not claim a line-by-line human verification.
