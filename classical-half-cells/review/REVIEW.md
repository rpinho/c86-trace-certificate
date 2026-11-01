# Fresh adversarial review: math_review_c86r3_1101

Reviewed 2026-11-01. **PASS for the claimed bound `C86 <= 1.80580911`.** I found no mathematical defect or remaining attribution error. A supplementary check proves a uniform potential margin greater than `1e-6` on the entire closed support. This is an AI review of a computer-assisted proof, not human peer review or formalization.

The exact result independently recovered from the frozen data is

    C86 <= 361161821571210817 / 199999999999978000
         = 1.805809107856252724... < 1.80580911.

It is **0.001169722143747276... below the filed decimal 1.80697883**, as claimed. It remains **0.003779107856252724... above the official table's lower bound 1.80203**. Thus it is consistent with that lower bound and does not settle the constant. The certificate is also above the stronger reported lower bound `901111277/500000000 = 1.802222554`, by approximately `0.00358655385625`; that lower certificate was not reviewed here.

The input SHA256 is

    59b716d8bcb9860e1d8e0df5b14612c518ee1ac845f0290d7a493814b30a7d51

This matches `../c86r3/certificate.json`, its named frozen copy, my `input/certificate.json`, and both replay receipts. The source files were not changed. Line references below identify the target's original files, snapshotted without modification as `input/target-PROOF.md` and `input/target-REPORT.md`. The JSON certificate occupies one line; references to its fields and zero-based indices locate the data precisely.

## Verdict per proof step

| Step | Exact target location | Verdict | Independent finding |
| --- | --- | --- | --- |
| Correct interpretation of the limiting trace constant | REPORT 3, 7–10; official `sources/86a.md:14–17` | **PASS** | The claim concerns an essential minimum/liminf, not an absolute minimum over exceptional algebraic integers. |
| Positive finite measure with the stated support | PROOF 3, 7; REPORT 42, 45; certificate line 1, `edges`, `node_densities` | **PASS** | Strictly ordered rational nodes, nonnegative heights and zero exterior heights. There are 4,662 nodes, 3,091 support cells and 51 closed support components, with hull `[27/500,5227/1000]`. |
| Integral, primitive, distinct irreducible auxiliaries | PROOF 3; REPORT 14, 44; certificate line 1, `A[0:26]` | **PASS** | Every coefficient is an integer. All 26 selected polynomials have primitive content, positive leading coefficient, distinct arrays and an exact single irreducible FLINT factor of multiplicity one. All are monic. Eight have nonreal roots; the largest degree is 17. |
| Positive weights and degree sum against the ACTUAL mass | PROOF 8; REPORT 42–43; certificate line 1, `b` | **PASS** | All 26 weights are positive. Exact mass minus weighted degree is `2228585641959/20000000000000 > 0`; using an assumed mass of one is unnecessary. |
| Direct logarithmic integral for every selected auxiliary | PROOF 9; REPORT 44, 46 | **PASS** | Independently integrated every linear density segment in 256-bit Arb using certified roots. All 26 integrals are strictly positive, including those with nonreal roots. |
| Potential inequality on ALL of the closed support | PROOF 10; REPORT 46–47 | **PASS** | Fresh replays accept every support cell, including endpoints. My separate exact-rational auditor checks every parent cell and every leaf adjacency. The strengthened cover proves `f(x)>1e-6` throughout the support. |
| Extension to gaps, nonreal points and infinity | PROOF 13 | **PASS** | Bounded density gives continuous finite potential. Harmonicity off support/auxiliary roots, positive infinite root singularities and the strict degree deficit justify the minimum principle. No real-root restriction on auxiliaries is needed. |
| Every integer polynomial, with no degree cap | PROOF 15–23; REPORT 56 | **PASS** | Nonzero integer resultants handle all other irreducibles; the selected irreducibles use their direct integrals. Integer content and factorization handle all remaining nonzero integer polynomials. |
| Normalization and Smith's theorem | PROOF 23–25; REPORT 56 | **PASS** | Divide the measure AND weights by its exact mass. The ambient positive interval `[1/100,6]` has one component and capacity `599/400>1`. Smith's theorem supplies infinitely many distinct totally positive algebraic integers with normalized traces tending to the certificate ratio. |
| Exact ratio and safe decimal rounding | PROOF 11; REPORT 7–10 | **PASS** | Direct trapezoid moments give exactly the advertised rational ratio, strictly below the printed upper decimal. The displayed improvement is arithmetically correct. |
| Classical coefficients and credit | REPORT 60–62; `sources/classical-attribution.md:3–9`; certificate line 1, `A` | **PASS** | All 26 active arrays match fresh primary Flammang TeX. All 70 stored McKee and 97 stored Flammang source arrays match independent parsing. Flammang receives appropriate credit. Direct earlier-source matches strengthen the target's valid degree-twelve attribution inference. |
| Independence and binding of the supplied proof paths | REPORT 36, 48–54 | **PASS** | The supplied earlier-review kernel is byte-identical to `../review_c86/independent_verify.py`; the first checker matches c86r2. Both were inspected and replayed only after my own mathematical/data pass. Their hashes and closed-cover bindings check. This is code independence, not independent human review. |

There is **no GAP or FALSE step in the proof of this bound**. The experimental search history is discussed separately below and is not needed for that proof.

## My derivation from Smith's actual statement

I read the actual Theorem 1.5 and Proposition 5.15 statements and resultant proof in [Smith's author-linked arXiv v2 PDF](https://arxiv.org/pdf/2111.12660v2), printed pp.4 and42, and checked the [Annals publication record](https://annals.math.princeton.edu/2024/200-1/p02). Smith's [own publication page](https://www.asmith-math.org/papers.html) links this manuscript as the Annals paper. Publisher PDF routes returned missing-page or anti-bot responses, so I did not compare the typeset journal PDF byte for byte. The full accessible primary manuscript is retained in `sources/smith-arxiv.pdf`.

Smith uses the negative-log potential. With the target's positive-log convention, set

    V(z) = integral log|z-t| dmu(t),
    f(z) = V(z) - sum_j b_j log|Q_j(z)|,
    m = mu(R), beta = sum_j b_j deg Q_j.

For Smith's probability measure use `nu=mu/m` and `a_j=b_j/m`. The target's signs and normalization then agree with the proposition. Its condition is global in the complex plane; checking a finite grid would not suffice.

Here continuity follows from the bounded compact line density and uniform local integrability of the logarithmic singularity. Outside the support and auxiliary roots, f is harmonic. At any auxiliary root it tends to positive infinity, even for a nonreal root or a root on the support. At infinity,

    f(z) = (m-beta) log|z| - sum_j b_j log|lc Q_j| + o(1),

uniformly in direction. Since `m-beta>0`, a large outer boundary and small boundaries around roots have positive values. The minimum principle on the intervening domains transfers the verified closed-support bound everywhere. Zero-density gaps do not create an unchecked boundary. The same reasoning transfers the strengthened `1e-6` margin.

For any primitive irreducible integer P with leading coefficient c and roots alpha_k, distinct up to sign from the selected Q_j,

    integral log|P| dmu
      >= (m-beta) log|c| + sum_j b_j log|Res(P,Q_j)| >= 0.

Every resultant is a nonzero integer. When P is selected, its resultant with itself vanishes, so its separate integral check is essential. Constants and factorization then cover all nonzero integer polynomials, including nonmonic polynomials and arbitrarily large degrees. No optimizer characterization from a real-rooted auxiliary pool is being used. My derivation was saved before opening any supplied checker in `OWN_PASSES.md`.

Finally, the positive ambient interval contains the actual support and has capacity greater than one. Weak convergence on that compact interval carries the continuous function x to the normalized first moment. Distinct irreducible monic polynomials give infinitely many totally positive algebraic integers. This establishes the limiting trace bound.

## Exact arithmetic and logarithmic integrals

| Quantity | Independent exact result |
| --- | --- |
| Mass m | `99999999999989/100000000000000` |
| First moment T | `361161821571210817/200000000000000000` |
| Weighted degree beta | `44428535895097/50000000000000` |
| m-beta | `2228585641959/20000000000000` |
| beta/m | `88857071790194/99999999999989`, approximately `0.888570717902038` |
| T/m | `361161821571210817/199999999999978000` |

`independent_pass.py` imports no search code, supplied checker or earlier review module. It computes trapezoid mass and first moment directly from the rational node arrays and evaluates logarithmic integrals by segment antiderivatives. For a segment `[a,b]`, slope s, root z and w=t-z, it integrates the real part of

    s*(w^2 log(w)/2-w^2/4)
      + (rho(a)+s*(z-a))*(w log(w)-w).

For a real root it uses log absolute value and exact limiting zero values. For a nonreal root the horizontal segment stays off the log branch cut. Complete certified root balls are summed, with `m log|lc Q|` included. The final receipt is `receipts/own-pass-final.json`.

Every row below independently passes integer coefficients, primitive irreducibility, distinctness, positive weight, primary-source matching and a positive Arb integral. M11 means McKee 2011 Table 1 row; F19 means the first trace list in arXiv:1907.09407v1. Indices are zero-based.

| Index | Degree | Nonreal roots | M11 row | F19 entry | Integral, approximately | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 | 9.99999400722e-8 | **PASS** |
| 1 | 1 | 0 | 2 | 2 | 9.99999797344e-8 | **PASS** |
| 2 | 1 | 0 | 3 | 3 | 9.99998894305e-8 | **PASS** |
| 3 | 2 | 0 | 4 | 4 | 1.00000084089e-7 | **PASS** |
| 4 | 3 | 0 | 7 | 7 | 1.00000031683e-7 | **PASS** |
| 5 | 4 | 0 | 11 | 11 | 9.99998695970e-8 | **PASS** |
| 6 | 4 | 0 | 12 | 12 | 1.00000086635e-7 | **PASS** |
| 7 | 5 | 0 | 14 | 15 | 1.00000117970e-7 | **PASS** |
| 8 | 5 | 0 | 15 | 16 | 9.99999003263e-8 | **PASS** |
| 9 | 5 | 0 | 16 | 13 | 9.99999059237e-8 | **PASS** |
| 10 | 5 | 0 | 13 | 14 | 9.99999238457e-8 | **PASS** |
| 11 | 10 | 0 | 27 | 28 | 9.99998534442e-8 | **PASS** |
| 12 | 10 | 0 | 25 | 30 | 1.00000107798e-7 | **PASS** |
| 13 | 10 | 0 | 26 | 29 | 1.00000122363e-7 | **PASS** |
| 14 | 8 | 0 | 20 | 24 | 9.99999231160e-8 | **PASS** |
| 15 | 8 | 0 | 22 | 23 | 9.99995872399e-8 | **PASS** |
| 16 | 7 | 0 | 19 | 20 | 0.0494206715792 | **PASS** |
| 17 | 2 | 0 | 5 | 6 | 1.00000306931e-7 | **PASS** |
| 18 | 8 | 2 | 23 | 26 | 0.0783163582983 | **PASS** |
| 19 | 12 | 4 | 29 | 33 | 1.00002039985e-7 | **PASS** |
| 20 | 12 | 4 | 30 | 35 | 1.00000061785e-7 | **PASS** |
| 21 | 13 | 2 | — | 40 | 0.159264993949 | **PASS** |
| 22 | 14 | 4 | — | 47 | 1.00000209112e-7 | **PASS** |
| 23 | 14 | 2 | — | 48 | 0.101404350390 | **PASS** |
| 24 | 14 | 4 | — | 54 | 9.99998874683e-8 | **PASS** |
| 25 | 17 | 2 | — | 72 | 1.00000216561e-7 | **PASS** |

The smallest integral, index15, is `9.99995872399467584653...e-8`, with a 256-bit Arb enclosure radius below `2.5e-68`. Full exact arrays and enclosures are in `AUXILIARIES.md` and the own-pass receipt; the displayed approximations do not control acceptance.

## Continuous coverage and attempts to break it

After the independent pass, I inspected both supplied enclosure kernels. `VERIFIER_REVIEW.md` gives exact code lines and checks the Taylor coefficients, geometric and Lagrange tails, sign-dependent near-knot treatment, root distance bounds, quadratic minorants and closed-interval assembly. I found no incorrect sign, remainder, floating acceptance test or real-root restriction in these proof paths.

| Fresh replay | Result |
| --- | --- |
| First checker, order18, 160-bit Arb | PASS; 7,954 pieces; minimum E4 about `9.999958724e-8`; minimum E5 lower enclosure `4.365938159e-9`; maximum depth6; 281.5s. |
| Earlier-review kernel, order8, 192-bit Arb, four workers | PASS; all 3,091 support cells; 12,413 closed pieces; 21,735 tests; maximum depth7; minimum leaf lower enclosure about `4.595143466e-10`; 425.5s. |
| Fresh rational cover/hash auditor, no checker or FLINT imports | PASS; every expected parent cell, both component endpoints and every exact adjacency verified. Eight altered covers rejected. |
| Stronger margin check using the inspected reviewer kernel | PASS; rechecked 1,960 loose leaves with 5,880 tests; 14,373 closed pieces; minimum lower display greater than `1.00005175539e-6`; 86.1s. |

The original minimum leaf lower enclosure is not the actual minimum of f. Independent diagnostic minimization on all3,091 original support cells found its smallest tested value near `x=3.8545644220405797`. Direct 256-bit Arb evaluation at that exact decimal rational gives

    f(x) = 1.851451860139637376253957310113...e-6 > 0.

The initial independent pass also checked466 rational probes, including component endpoints and auxiliary roots assigned positive infinity, and6 off-axis points. A further24 off-axis probes found no negative pocket. These probes and minimizations are falsification attempts; the saved continuous covers provide the proof.

Fresh adversarial controls also reject:

- Eleven structural corruptions: wrong bound, negative density, wrong density length, repeated edge, nonzero exterior height, negative weight, excess weighted degree, reducible polynomial, noninteger coefficient, duplicate polynomial and nonprimitive polynomial.
- Raising every auxiliary weight by `1001/1000`: structural conditions and the degree deficit still pass, but my direct potential calculation certifies `f(5)=-0.000906729829847309352...<0`.
- Lowering the last positive density node (index4619) by1%, with the exact bound recomputed: structural conditions still pass, but `integral log(x) dmu=-1.4117030254363274257...e-5<0`.
- The supplied reviewer independently rejects the wrong-bound, raised-weight and negative-integral certificates for their intended mathematical reasons, rather than an incidental execution error.
- Eight cover corruptions: deleted endpoint leaf, deleted interior leaf, shifted endpoint by `1e-30`, duplicate leaf, wrong parent, zero lower bound, negative lower bound and a displayed ball crossing zero.

The raised weights and negative integral demonstrate that the two substantive analytic obligations are actually being tested. Receipts: `own-adversarial-checks.json`, `replayed-controls.json`, `own-coverage-audit.json`, with detailed logs. Diagnostic development failures in my first endpoint implementation were retained and corrected using exact rational endpoint equality before the successful pre-checker pass; they were not accepted as certificate failures.

## Classical transcription and attribution

The fresh [McKee institutional PDF](https://repository.royalholloway.ac.uk/file/83e374ca-f1d2-52bd-6ddd-84371453b5c2/5/S0025_5718_2010_02424_X.pdf), p.1049 Table1, directly matches the degree-eight pair at rows21/23 and the degree-twelve pair at rows29/30. I inspected the rendered primary page and independently parsed all70 table rows, including wrapped coefficient lines. Every stored target row matches. Appendix6 p.1048 confirms the classification used in the target's credit inference.

The fresh primary [Flammang later source](https://arxiv.org/src/1907.09407) has SHA256 `350d2a28112b1a051270c9c6c18e0f2a3d27d99543f5a40cfad88e9b3e2ced25`. My own parser recovers97 entries and agrees exactly with all97 target arrays and every active polynomial. This is the arXiv note, not the different 2019 IJNT paper with a similar title. It supplies classical inputs, not newly discovered polynomials.

I also read the indexed [primary Flammang2009 manuscript](https://citeseerx.ist.psu.edu/document?doi=e3916f24808f536fa81e57eaa441dc1f4a1ff7f5&repid=rep1&type=pdf). Direct downloading failed, so the retained evidence clearly distinguishes the successful indexed full-text read from failed HTTP requests. Its Table1 and positive Table2 coefficients give these direct matches:

| Earlier source | McKee source | Target use | Verdict |
| --- | --- | --- | --- |
| Flammang2009 Table1 row22 | McKee row21 | Other member of the original degree-eight pair, no longer active in the final certificate | **PASS** |
| Flammang2009 Table1 row23 | McKee row23 | Active index18 | **PASS** |
| Flammang2009 Table1 row33 | McKee row29 | Active index19, degree12 and trace21 | **PASS** |
| Flammang2009 Table1 row32 | McKee row30 | Active index20, degree12 and trace21 | **PASS** |

Thus REPORT60's attribution is correct and can be strengthened with exact earlier row numbers33/32. This resolves the concern raised by the earlier review without relying on its conclusion. Complex-root auxiliaries were already used for the trace problem by Flammang, and Smith's criterion already permits them. The target credits both facts appropriately. See `sources/flammang2009-independent.md` and `receipts/own-source-matches.json`.

## Literature comparison and limits of this review

`PRIOR_ART.md` and `sources/public-refresh*.json` record the initial and final live checks. The official raw table/entry still give lower1.80203 and Koshta's upper1.8084990*. The strongest filed upper claim I identified remains PR298's1.80697883; Tomar's exact public upper candidate is approximately1.80708083258824. All five identified C86 PRs (#298,#292,#270,#242,#223), including discussions, were read. The complete open-PR title audit now finds45 PRs; the two newer #306/#307 concern C91/C89, not C86. This does not contradict the target's earlier timestamped43-PR count.

All eleven freshly checked repository HEADs match the target's pins. Those checks cover the official/rival repositories and BakeLab/Epi-results, both DeepMind AlphaEvolve repositories, openai/math, kisonecat/openai-math and plasma-ai/erdos. Updated public repository search, recent-paper and indexed community searches found no stronger upper bound. README/title/index searches are limited evidence, not an exhaustive priority result. The two later lower-bound reports are distinguished from the published/table1.80203 and remain consistent with the candidate.

**GAP in independent replication of experimental history, not in the bound:** I did not rerun the LP optimizers, all matched ablation models or the200,000 scheduled lattice trials in REPORT18–32 and64–68. I therefore do not independently certify those experiment counts, convergence histories or attribution of the numerical gain between pools and grids. Those claims are unnecessary to the final feasible certificate, and the target explicitly does not claim certified LP optimality or absence of better auxiliaries. The exact gain relative to the filed decimal and the final certificate itself are verified here. No stronger conclusion about optimality, novelty or exhaustive search follows from this review.

## Exact reproduction

All scientific runs took place on a rented pod under `the job directory`, through own detached tmux sessions. `run_remote.sh` sets nice10, all numerical library thread limits to1 and affinity to four allowed CPUs. Python3.12.3 and python-flint0.9.0 were used; `requirements-review.txt` pins the mathematical dependencies. The source-PDF extraction package is unnecessary for any proof replay: its extracted text and original PDFs are retained.

Stage only into this own job directory, without `--delete`, then create an own tmux session:

```sh
rsync -az input sources *.py run_remote.sh requirements-review.txt a rented pod:the job directory
rsync -az input/*.py a rented pod:the job directory
ssh a rented pod
cd the job directory
tmux new-session -s math_review_c86r3_reproduce
```

Inside that tmux session, run these exact scientific commands sequentially:

```sh
test -x venv/bin/python || uv venv venv
UV_CACHE_DIR="$PWD/uv-cache" uv pip install --python venv/bin/python -r requirements-review.txt
mkdir -p receipts logs
bash run_remote.sh independent_pass.py --output receipts/own-pass-final.json
bash run_remote.sh source_match.py
bash run_remote.sh adversarial_checks.py
bash run_remote.sh try_break.py
bash run_remote.sh verify_linear.py input/certificate.json --beat 1.80580911 --output receipts/replay-first.json
bash run_remote.sh parallel_verify.py input/certificate.json --workers 4 --output receipts/replay-independent.json
bash run_remote.sh audit_cover.py
bash run_remote.sh audit_artifact.py input/certificate.json receipts/replay-independent.json --output receipts/replay-supplied-audit.json
bash run_remote.sh replay_controls.py
bash run_remote.sh strengthen_cover.py
venv/bin/python process_audit.py
```

Pull the small receipts back with rsync, without deleting remote files. My actual mathematical runs used the same commands, with the two complete proof paths in separate tmux sessions and the audits after completion. The final archive remains below50MB. `MANIFEST.json` hashes the retained critical inputs, code and receipts.

## End state and next action

The remote `ps -axo pid,ppid,pcpu,command`/own-cwd audit at22:04:18 UTC found **zero own Python workers**. The local worker audit is empty. The pod was left running, and no other job was modified. No commits, pushes, PRs, posts or messages were made.

One operational exception is recorded: PyMuPDF2 unexpectedly initialized ONNX runtime thread pools during primary-PDF extraction. That process finished before the proof replays; its diagnostics are retained, and I cannot retrospectively certify the10-core cap during that brief library initialization. All mathematical proof jobs were explicitly pinned to four CPUs with single-thread numerical libraries. No further PDF-library runs were made.

No mathematical repair is indicated. For the next human review, use the frozen certificate, the exact-step table and the14,373-piece strengthened cover; the earlier degree-twelve provenance can now cite Flammang2009 rows33/32 directly. Retain the unrefereed qualification until the applicable publication/review standard is met.

**Overall verdict: PASS for `C86 <= 1.80580911`, with an experimental-history replication GAP outside the proof. My subjective probability that the bound is correct is 99%.**
