from drac import Experiment, DRACSystem, closure_resolvable, brute_force_resolvable
from drac.closure import closure_partition
from drac.metrics import authorization_reachability_ratio


def test_perfect_but_unauthorized_experiment_is_blocked():
    worlds = (0, 1)
    decisions = {0: "DENY", 1: "ALLOW"}
    e = Experiment(
        "perfect",
        {0: 0, 1: 1},
        frozenset({"ALLOW"}),
    )
    s = DRACSystem(worlds, decisions, (e,))
    assert closure_resolvable(s) is False
    assert brute_force_resolvable(s) is False
    assert authorization_reachability_ratio(s) == 0.0


def test_authorized_separator_resolves():
    worlds = (0, 1)
    decisions = {0: "DENY", 1: "ALLOW"}
    e = Experiment(
        "separator",
        {0: 0, 1: 1},
        frozenset({"ALLOW", "DENY"}),
    )
    s = DRACSystem(worlds, decisions, (e,))
    assert closure_resolvable(s) is True
    assert brute_force_resolvable(s) is True
    assert authorization_reachability_ratio(s) == 1.0


def test_staged_authorization():
    worlds = (0, 1, 2)
    decisions = {0: "A", 1: "B", 2: "B"}

    e1 = Experiment(
        "coarse",
        {0: 0, 1: 0, 2: 1},
        frozenset({"A", "B"}),
    )
    e2 = Experiment(
        "fine",
        {0: 0, 1: 1, 2: 1},
        frozenset({"A", "B"}),
    )

    s = DRACSystem(worlds, decisions, (e1, e2))
    assert closure_resolvable(s) is True
    assert brute_force_resolvable(s) is True
    assert all(s.is_homogeneous(b) for b in closure_partition(s))
