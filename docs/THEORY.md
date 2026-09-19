# DRAC formal core

## Model

A finite DRAC instance is
[
M=(W,D,g,E,O,\rho),
]
where (W) is a finite world set, (D) a finite decision set, (g:W\to D), each experiment (e\in E) has deterministic outcome map (O_e:W\to Y_e), and (\rho(e)\subseteq D) is its authorization set.

For nonempty (C\subseteq W), define
[
g(C)=\{g(w):w\in C\}.
]
Experiment (e) is admissible at (C) iff
[
g(C)\subseteq\rho(e).
]

For outcome (y), the nonempty child is
[
C_{e,y}=\{w\in C:O_e(w)=y\}.
]

## Lemma 1: Heredity

If (C'\subseteq C) and (e) is admissible at (C), then (e) is admissible at (C').

**Proof.** (g(C')\subseteq g(C)\subseteq\rho(e)). ∎

## Lemma 2: Persistence

Once an experiment becomes admissible on a branch, it remains admissible at every descendant on that branch.

This follows immediately from Lemma 1.

## Closure operator

For a partition (P), refine every block (C\in P) by the joint outcome signatures of every experiment admissible at (C). Iterate until no block changes. Finiteness of (W) guarantees termination because every strict iteration increases the number of blocks.

Call the terminal partition (P_A^*).

## Theorem 1: Authorization-Closure Characterization

For finite deterministic DRAC systems under the authorization rule above, an adaptive admissible experiment tree resolves (g) on every world iff every block of (P_A^*) is decision-homogeneous.

### Proof

**If.** Each closure refinement uses experiments admissible at its current block. By heredity, sequentializing the simultaneous refinement cannot invalidate any of those experiments. Hence every refinement round can be realized as an adaptive admissible tree. When the fixed-point blocks are decision-homogeneous, the resulting tree resolves (g).

**Only if.** Suppose a terminal closure block (C) is not decision-homogeneous. At the fixed point no experiment admissible at (C) nontrivially splits (C); otherwise closure would refine it. Therefore no admissible first step can shrink (C). Consequently no adaptive admissible tree can distinguish all decision-incompatible worlds inside (C), so no such tree resolves (g) everywhere. ∎

## Corollary 1: Feasibility confluence

Feasibility does not depend on the order in which already-admissible experiments are executed. An admissible experiment cannot disable another already-admissible experiment, by heredity. The closure fixed point therefore characterizes maximal reachable decision refinement.

This statement concerns **feasibility**, not cost. Different orders may have different costs.

## Corollary 2: Finite termination

There are at most (|W|-1) strict global refinement stages that increase the number of blocks by at least one.

## Computational verification

The implementation compares the closure criterion with a separately implemented brute-force recursive adaptive-tree solver. Agreement provides an independent check of the formalization and implementation.

## Citation

Akhtar, M. A. K. (2026). Decision-Relative Authority Closure: When Information Exists but Cannot Be Permissibly Acquired to Resolve a Decision (Version V1). Zenodo. https://doi.org/10.5281/zenodo.22848073
