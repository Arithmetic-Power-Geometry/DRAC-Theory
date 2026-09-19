# Verification results

The repository uses two independent feasibility procedures:

1. fixed-point authorization closure;
2. recursive exhaustive adaptive-policy search.

The initial deterministic binary sweep tested **19,260** generated systems and found **0 disagreements**. It also found **16,676** generated systems in which some decision-incompatible pair had a separating signal while authorization closure still failed.

The CI additionally runs a deterministic-seed randomized stress test with up to 7 worlds, 6 experiments, 3 decisions, and 3 outcomes.

These computations are theorem-regression/falsification tests. They do not establish novelty and do not replace the formal proof.
