# Verification results

## Exhaustive finite verification

The repository uses two independent feasibility procedures:

1. fixed-point authorization closure;
2. recursive exhaustive adaptive-policy search.

The deterministic binary sweep tested **19,260** generated systems and found **0 disagreements** between the two procedures.

It also found **16,676** systems in which at least one decision-incompatible pair had an available separating signal while authorization closure still failed. This supplies finite examples of the distinction between technical observability and authorization-resolvability.

Parameters:

- worlds: up to 4
- experiments: up to 2
- binary decisions
- binary experiment outcomes

## Higher-dimensional randomized falsification

A deterministic-seed stress test independently generated **25,000** additional systems with:

- up to 7 worlds,
- up to 6 experiments,
- up to 3 decision classes,
- up to 3 experiment outcomes.

Result:

```json
{
  "seed": 20260919,
  "tested": 25000,
  "mismatch": null,
  "survived": true
}
```

Thus the closure criterion and independent exhaustive adaptive-policy solver agreed in all **44,260 tested systems** across the two reported campaigns.

The computational campaigns provide independent checks of the formalization and implementation. The authorization-closure characterization is established mathematically in `docs/THEORY.md`.

## Current research status

The deterministic hereditary DRAC feasibility model is implemented and computationally checked. A natural next technical direction is the optimization problem of minimum-cost authorization-resolving experiment trees, including formal complexity analysis.

## Citation

Akhtar, M. A. K. (2026). Decision-Relative Authority Closure: When Information Exists but Cannot Be Permissibly Acquired to Resolve a Decision (Version V1). Zenodo. https://doi.org/10.5281/zenodo.22848073
