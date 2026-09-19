from itertools import combinations
from .closure import closure_partition


def incompatible_pairs(system):
    return {
        frozenset((a, b))
        for a, b in combinations(system.worlds, 2)
        if system.decisions[a] != system.decisions[b]
    }


def unresolved_pairs_after_closure(system):
    pairs = incompatible_pairs(system)
    unresolved = set()
    for block in closure_partition(system):
        block_set = set(block)
        for pair in pairs:
            if pair.issubset(block_set):
                unresolved.add(pair)
    return unresolved


def authorization_reachability_ratio(system):
    pairs = incompatible_pairs(system)
    if not pairs:
        return 1.0
    unresolved = unresolved_pairs_after_closure(system)
    return 1.0 - (len(unresolved) / len(pairs))
