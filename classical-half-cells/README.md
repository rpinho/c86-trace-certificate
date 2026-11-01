# C86 <= 1.80580911: classical auxiliaries on half cells

Unrefereed. This certifies an upper bound on the Schur-Siegel-Smyth trace constant, Tao table [86a](https://teorth.github.io/optimizationproblems/constants/86a.html). No human expert has reviewed it line by line.

    C86 <= 361161821571210817 / 199999999999978000 < 1.80580911

It improves the 1.80697883 in [`../complex-auxiliaries/`](../complex-auxiliaries/) by about 0.00117. The table's lower bound is 1.80203. The proof uses Smith's arithmetic-measure criterion and converse theorem, as in that folder.

The gain comes from known classical polynomials and from refining the density cells. Fresh degree 9 and 10 searches found nothing useful.

## What's here

- `certificate.json`: 26 auxiliaries, eight with nonreal roots, largest degree 17. SHA-256 `59b716d8bcb9860e1d8e0df5b14612c518ee1ac845f0290d7a493814b30a7d51`.
- `PROOF.md`, `METHOD.md`, `VERIFIER_NOTES.md`.
- `verify_linear.py`, `independent_verify.py`: two checkers, and their receipts.
- `active-provenance.json`: where every auxiliary comes from.
- `review/REVIEW.md`: a separate AI review with its own check of the criterion.

## What this doesn't show

The review passed all proof steps and all 26 auxiliaries. It's AI, so it isn't a second party. No priority or optimality is claimed.

## Credit

The auxiliaries are classical. Flammang's 2009 paper and 2019 note and McKee's 2011 paper supply them, as `active-provenance.json` records. Smith for the criterion and converse theorem, Orloski and Talebizadeh Sardari for the quantitative converse, Tomar for the adaptive nodes behind the density cone, and Niedbala Giraudin for PR #270.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifiers and this text. This does not claim a line-by-line human verification.
