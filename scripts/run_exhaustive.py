import argparse
import csv
import itertools
import json
from pathlib import Path

from drac import Experiment, DRACSystem, closure_resolvable, brute_force_resolvable
from drac.metrics import authorization_reachability_ratio


def nonconstant_binary_decisions(n):
    for bits in itertools.product((0, 1), repeat=n):
        if len(set(bits)) > 1:
            yield bits


def all_binary_outcome_maps(n):
    yield from itertools.product((0, 1), repeat=n)


def all_authorizations():
    # Non-empty subsets of {0,1}
    return (
        frozenset({0}),
        frozenset({1}),
        frozenset({0, 1}),
    )


def generated_systems(n, max_experiments):
    worlds = tuple(range(n))
    outcome_maps = list(all_binary_outcome_maps(n))
    auths = list(all_authorizations())
    experiment_types = [(o, a) for o in outcome_maps for a in auths]

    for decbits in nonconstant_binary_decisions(n):
        decisions = dict(zip(worlds, decbits))
        for k in range(1, max_experiments + 1):
            # combinations_with_replacement keeps the search deterministic and finite.
            for combo in itertools.combinations_with_replacement(experiment_types, k):
                exps = []
                for idx, (omap, auth) in enumerate(combo):
                    exps.append(
                        Experiment(
                            f"e{idx}",
                            dict(zip(worlds, omap)),
                            auth,
                        )
                    )
                yield DRACSystem(worlds, decisions, tuple(exps))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-worlds", type=int, default=4)
    parser.add_argument("--max-experiments", type=int, default=2)
    parser.add_argument("--cap", type=int, default=100000)
    args = parser.parse_args()

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    rows = []
    tested = 0
    mismatches = 0
    blocked_despite_unrestricted_signal = 0

    for n in range(2, args.max_worlds + 1):
        for system in generated_systems(n, args.max_experiments):
            tested += 1
            closure = closure_resolvable(system)
            brute = brute_force_resolvable(system)
            eta = authorization_reachability_ratio(system)

            if closure != brute:
                mismatches += 1
                rows.append({
                    "n_worlds": n,
                    "closure": closure,
                    "bruteforce": brute,
                    "eta": eta,
                    "case": repr(system),
                })

            # Count systems where at least one experiment can separate a
            # decision-incompatible pair, but authorization closure still fails.
            signal_exists = False
            for e in system.experiments:
                for i in range(len(system.worlds)):
                    for j in range(i + 1, len(system.worlds)):
                        wi, wj = system.worlds[i], system.worlds[j]
                        if system.decisions[wi] != system.decisions[wj] and e.outcome(wi) != e.outcome(wj):
                            signal_exists = True
                            break
                    if signal_exists:
                        break
                if signal_exists:
                    break
            if signal_exists and not closure:
                blocked_despite_unrestricted_signal += 1

            if tested >= args.cap:
                break
        if tested >= args.cap:
            break

    summary = {
        "tested_systems": tested,
        "closure_vs_bruteforce_mismatches": mismatches,
        "blocked_despite_available_separating_signal": blocked_despite_unrestricted_signal,
        "conjecture_survived_test": mismatches == 0,
        "parameters": {
            "max_worlds": args.max_worlds,
            "max_experiments": args.max_experiments,
            "cap": args.cap,
        },
    }

    (outdir / "exhaustive_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    with (outdir / "exhaustive_cases.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n_worlds", "closure", "bruteforce", "eta", "case"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(summary, indent=2))

    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
