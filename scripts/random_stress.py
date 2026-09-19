import argparse, json, random
from drac import Experiment, DRACSystem
from drac.closure import closure_resolvable
from drac.reference import exhaustive_policy_resolvable


def make_case(rng,n,m,k,outcomes):
    worlds=tuple(range(n))
    while True:
        decisions={w:rng.randrange(k) for w in worlds}
        if len(set(decisions.values()))>1:
            break
    exps=[]
    labels=tuple(range(k))
    for j in range(m):
        omap={w:rng.randrange(outcomes) for w in worlds}
        auth=frozenset(d for d in labels if rng.random()<0.65)
        if not auth:
            auth=frozenset({rng.choice(labels)})
        exps.append(Experiment(f"e{j}",omap,auth))
    return DRACSystem(worlds,decisions,tuple(exps))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cases",type=int,default=25000)
    p.add_argument("--seed",type=int,default=20260919)
    p.add_argument("--max-worlds",type=int,default=7)
    p.add_argument("--max-experiments",type=int,default=6)
    p.add_argument("--max-decisions",type=int,default=3)
    p.add_argument("--max-outcomes",type=int,default=3)
    a=p.parse_args()
    rng=random.Random(a.seed)
    mismatch=None
    for i in range(a.cases):
        n=rng.randint(2,a.max_worlds)
        m=rng.randint(1,a.max_experiments)
        k=rng.randint(2,min(a.max_decisions,n))
        o=rng.randint(2,a.max_outcomes)
        s=make_case(rng,n,m,k,o)
        c=closure_resolvable(s)
        b=exhaustive_policy_resolvable(s)
        if c!=b:
            mismatch={"case_index":i,"closure":c,"bruteforce":b,"system":repr(s)}
            break
    result={"seed":a.seed,"tested":i+1,"mismatch":mismatch,"survived":mismatch is None,
            "bounds":{"max_worlds":a.max_worlds,"max_experiments":a.max_experiments,
                      "max_decisions":a.max_decisions,"max_outcomes":a.max_outcomes}}
    print(json.dumps(result,indent=2))
    if mismatch:
        raise SystemExit(1)


if __name__=="__main__":
    main()
