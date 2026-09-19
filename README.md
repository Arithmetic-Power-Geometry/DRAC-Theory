# DRAC-Theory

**Decision-Relative Authority Closure (DRAC)**

A compact research software repository for testing whether a decision can be resolved through an adaptive sequence of experiments whose admissibility depends on the still-unresolved decision class.

## Core model

Let:

- (W): finite set of possible worlds
- (D): decision labels
- (g: W \to D): required decision in each world
- (E): experiments
- (O_e(w)): deterministic outcome of experiment (e) in world (w)
- (ho(e) \subseteq D): decisions under which experiment (e) is authorized

For an unresolved class (C \subseteq W), experiment (e) is admissible iff

[
g(C) \subseteq \rho(e).
]

The central computational question is:

> Can the decision be resolved by repeatedly applying only experiments that are authorized at the class where they are used?

This repository implements:

1. fixed-point authorization closure,
2. brute-force adaptive-tree verification,
3. exhaustive finite-system search for counterexamples,
4. automated theorem-regression tests,
5. GitHub Actions workflow producing machine-readable results.

## Main conjecture tested by the software

Under hereditary decision-relative authorization,

[
	ext{authorization-safe resolution exists}
\iff
g 	ext{ is constant on every block of the authorization closure fixed point.}
]

The workflow compares the closure test against brute-force adaptive search over thousands of generated finite systems.

## Run locally

```bash
python -m pip install -e .
python -m pytest -q
python scripts/run_exhaustive.py --max-worlds 4 --max-experiments 3
```

## Output

The exhaustive script writes:

- `results/exhaustive_summary.json`
- `results/exhaustive_cases.csv`

The GitHub Actions workflow uploads these as artifacts.

## Scope

This is a mathematical and computational testbed. It does **not** claim that the theory is novel merely because the software passes its tests. Prior-art review and formal proof remain separate research tasks.

## License

Apache License 2.0.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
