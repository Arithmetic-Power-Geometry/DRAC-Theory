import itertools
from drac import Experiment, DRACSystem
from drac.closure import closure_resolvable
from drac.reference import exhaustive_policy_resolvable


def test_admissibility_is_hereditary():
    worlds=(0,1,2,3)
    decisions={0:"A",1:"A",2:"B",3:"B"}
    e=Experiment("e",{0:0,1:0,2:1,3:1},frozenset({"A","B"}))
    s=DRACSystem(worlds,decisions,(e,))
    assert s.admissible(e, worlds)
    for r in range(1,len(worlds)+1):
        for sub in itertools.combinations(worlds,r):
            assert s.admissible(e,sub)


def test_perfect_observability_can_fail_authorized_resolution():
    worlds=(0,1,2,3)
    decisions={0:"A",1:"A",2:"B",3:"B"}
    # Joint signatures uniquely identify every world, but neither experiment
    # is authorized while A/B remains unresolved.
    e1=Experiment("bit0",{0:0,1:0,2:1,3:1},frozenset({"A"}))
    e2=Experiment("bit1",{0:0,1:1,2:0,3:1},frozenset({"B"}))
    s=DRACSystem(worlds,decisions,(e1,e2))
    signatures={(e1.outcome(w),e2.outcome(w)) for w in worlds}
    assert len(signatures)==4
    assert closure_resolvable(s) is False
    assert exhaustive_policy_resolvable(s) is False
