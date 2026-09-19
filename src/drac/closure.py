from typing import Iterable, Tuple
from .model import DRACSystem

Partition = Tuple[Tuple[object, ...], ...]


def _canonical(partition: Iterable[Iterable[object]]) -> Partition:
    blocks = [tuple(sorted(block, key=repr)) for block in partition]
    blocks.sort(key=lambda b: tuple(map(repr, b)))
    return tuple(blocks)


def refine_block_by_all_admissible(system: DRACSystem, block):
    current = [tuple(block)]
    admissible = [
        e for e in system.experiments
        if system.admissible(e, block)
    ]
    for e in admissible:
        nxt = []
        for b in current:
            parts = system.split(e, b)
            nxt.extend(parts)
        current = nxt
    return tuple(current)


def closure_partition(system: DRACSystem) -> Partition:
    partition = _canonical([system.worlds])

    while True:
        new_blocks = []
        for block in partition:
            new_blocks.extend(refine_block_by_all_admissible(system, block))
        refined = _canonical(new_blocks)
        if refined == partition:
            return partition
        partition = refined


def closure_resolvable(system: DRACSystem) -> bool:
    return all(system.is_homogeneous(block) for block in closure_partition(system))
