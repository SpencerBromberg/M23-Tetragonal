# Historical one-run q-pair reconstruction target

**Archive status:** This directory preserves a pre-closure diagnostic target. The exact characteristic-zero closure and independent held-out validations now supersede the proposed next run; no current manuscript claim depends on executing this file.

The decoder/q-pair reduction folds the PGL2 gauge before coefficient recovery. The two executed primes show that the canonical 469-coordinate row-reduced plane has row supports 85 and 85, union support 86, and intersection support 84. Thus only 168 nonpivot row entries remain after the two fixed pivots.

`M23_qpair_full_rows_p100207139_v86.m` performs one additional generic split-prime replay at the already-tested prime `100207139` and prints the complete two canonical 469-entry RREF rows plus union/intersection support. At the time of creation, it was intended as the next single execution. The output can be fed directly into CRT/rational-reconstruction code without reconstructing the 120 bidegree coefficients first.

A successful run does not by itself prove the characteristic-zero table. Exact closure requires rational reconstruction followed by reduction at an independent held-out prime. The purpose of this run is to decide immediately whether the decoder-locked gauge has lowered the arithmetic height enough for that final reconstruction.
