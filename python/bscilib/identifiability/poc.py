"""
Structural identifiability proof-of-concept for behavioral discounting models.

Method: local structural identifiability via the rank of the symbolic
output-sensitivity (Jacobian) matrix, evaluated at random rational parameter
values and delay points. Full rank at a generic point => parameters are
locally identifiable from noiseless indifference-point data; rank deficiency
=> a structural confound, and the Jacobian nullspace names the parameters
that trade off. This is the lightweight cousin of the differential-algebra
methods in StructuralIdentifiability.jl / SIAN, adequate for closed-form
(static) discounting models.

Models
------
1. Hyperbolic (Mazur):            V = A / (1 + k*D)
2. Hyperboloid (Myerson-Green):   V = A / (1 + k*D)**s
3. A value function with a redundant sensitivity scalar (synthetic example):
                                  V = A / (1 + k*(c*D))**s
   -- pedagogical reconstruction of a parameter-confound defect: c and k
   enter only through the product k*c, so neither is identifiable alone.
4. The repaired form (c removed / absorbed):  V = A / (1 + k*D)**s

Run:  python3 identifiability_poc.py
"""

from fractions import Fraction
import random

import sympy as sp

random.seed(20260808)


def sensitivity_rank(V, params, D, n_points=None, trials=3):
    """Rank of the sensitivity matrix J[i,j] = dV/dparam_j at delay D_i,
    evaluated at random rational parameter values (generic-point test).
    Returns (rank, nullspace_basis) from the best (max-rank) trial."""
    n_points = n_points or (len(params) + 2)
    grads = [sp.diff(V, p) for p in params]
    best = (-1, None)
    for _ in range(trials):
        subs_p = {p: Fraction(random.randint(2, 40), random.randint(2, 40))
                  for p in params}
        rows = []
        for _ in range(n_points):
            d_val = Fraction(random.randint(1, 365), random.randint(1, 4))
            subs = dict(subs_p)
            subs[D] = d_val
            rows.append([sp.nsimplify(g.subs(subs)) for g in grads])
        J = sp.Matrix(rows)
        r = J.rank()
        if r > best[0]:
            best = (r, J.nullspace())
    return best


def report(name, V, params, D):
    rank, null = sensitivity_rank(V, params, D)
    n = len(params)
    verdict = "IDENTIFIABLE (locally, generic point)" if rank == n else \
              f"NOT IDENTIFIABLE  --  rank {rank} < {n} parameters"
    print(f"\n{name}")
    print(f"  V(D) = {sp.pretty(V)}")
    print(f"  parameters: {params}")
    print(f"  sensitivity rank: {rank}/{n}   ->  {verdict}")
    if rank < n and null:
        v = null[0]
        direction = ", ".join(f"{sp.nsimplify(v[i], rational=True)}*d{p}"
                              for i, p in enumerate(params)
                              if sp.simplify(v[i]) != 0)
        print(f"  confounded direction (Jacobian nullspace): {direction}")
        print("  interpretation: moving parameters along this direction leaves")
        print("  every predicted indifference point unchanged -- the data can")
        print("  never separate these parameters, at any sample size.")


def main():
    A, k, s, c, D = sp.symbols("A k s c D", positive=True)

    print("=" * 72)
    print("Structural identifiability check: delay-discounting value functions")
    print("Output assumed observable: indifference value V at chosen delays D")
    print("=" * 72)

    report("1. Hyperbolic (Mazur 1987), A fixed by procedure",
           A / (1 + k * D), [k], D)

    report("2. Hyperbolic, A treated as free",
           A / (1 + k * D), [A, k], D)

    report("3. Hyperboloid (Myerson & Green 1995)",
           A / (1 + k * D) ** s, [A, k, s], D)

    report("4. Synthetic form with redundant sensitivity scalar c "
           "(pedagogical defect)",
           A / (1 + k * (c * D)) ** s, [A, k, c, s], D)

    report("5. Repaired form (c absorbed into k)",
           A / (1 + k * D) ** s, [A, k, s], D)

    print("\n" + "=" * 72)
    print("MIABS item E2 is the reporting requirement this check discharges:")
    print("'Report evidence that fitted parameters are recoverable ... report")
    print(" any confounded or unidentifiable parameters.'")
    print("Model 4 would pass code review, converge in any fitter, and produce")
    print("stable-looking estimates -- while k and c wander a ridge. The rank")
    print("test costs milliseconds and catches it before a single fit is run.")
    print("=" * 72)


if __name__ == "__main__":
    main()
