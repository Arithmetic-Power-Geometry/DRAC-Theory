from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, Mapping, FrozenSet, Tuple

World = Hashable
Decision = Hashable
Outcome = Hashable


@dataclass(frozen=True)
class Experiment:
    name: str
    outcomes: Mapping[World, Outcome]
    authorized_decisions: FrozenSet[Decision]

    def outcome(self, world: World) -> Outcome:
        return self.outcomes[world]


@dataclass(frozen=True)
class DRACSystem:
    worlds: Tuple[World, ...]
    decisions: Mapping[World, Decision]
    experiments: Tuple[Experiment, ...]

    def decision_set(self, block: Iterable[World]) -> FrozenSet[Decision]:
        return frozenset(self.decisions[w] for w in block)

    def is_homogeneous(self, block: Iterable[World]) -> bool:
        return len(self.decision_set(block)) <= 1

    def admissible(self, experiment: Experiment, block: Iterable[World]) -> bool:
        return self.decision_set(block).issubset(experiment.authorized_decisions)

    def split(self, experiment: Experiment, block: Iterable[World]):
        groups: Dict[Outcome, list] = {}
        for w in block:
            groups.setdefault(experiment.outcome(w), []).append(w)
        return tuple(tuple(v) for v in groups.values())
