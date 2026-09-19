from functools import lru_cache
from .model import DRACSystem


def brute_force_resolvable(system: DRACSystem) -> bool:
    @lru_cache(maxsize=None)
    def solve(block):
        block = tuple(block)
        if system.is_homogeneous(block):
            return True

        for e in system.experiments:
            if not system.admissible(e, block):
                continue
            children = system.split(e, block)
            if len(children) <= 1:
                continue
            if all(solve(tuple(child)) for child in children):
                return True
        return False

    return solve(tuple(system.worlds))
