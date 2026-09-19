"""Independent slow reference implementations used for theorem regression."""
from functools import lru_cache
from .model import DRACSystem


def exhaustive_policy_resolvable(system: DRACSystem) -> bool:
    """Explore every admissible first experiment recursively.

    Kept deliberately separate from closure.py.
    """
    @lru_cache(None)
    def rec(block):
        block = tuple(block)
        if system.is_homogeneous(block):
            return True
        choices = []
        for e in system.experiments:
            if system.admissible(e, block):
                children = system.split(e, block)
                if len(children) > 1:
                    choices.append(children)
        return any(all(rec(tuple(child)) for child in children) for children in choices)
    return rec(tuple(system.worlds))
