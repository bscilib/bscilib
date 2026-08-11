"""
Benchmark-corpus proof-of-concept: metamorphic tests for artificial organisms.

A metamorphic relation is an invariance or directional prediction that must
hold WITHOUT ground-truth data. Property-based testing (Hypothesis) then
hunts the input space for violations. Any candidate model exposes a small
typed interface; the corpus interrogates it. Two entries are demonstrated:

  MR-1  Generalized matching, ratio scale invariance:
        allocation depends on the RATIO of reinforcer rates, so scaling both
        rates by any positive constant leaves predicted allocation unchanged.

  MR-2  Exponential discounting admits no preference reversal:
        if V_A(0-front-end) >= V_B(0-front-end), adding a common front-end
        delay T to both alternatives cannot reverse the preference.
        (Hyperbolic discounting is EXPECTED to violate this -- the violation
        is the phenomenon -- so for a hyperbolic agent the corpus asserts the
        reversal EXISTS for some T. Directional predictions cut both ways.)

Each relation is run against a conforming agent and a deliberately defective
one, demonstrating that the tests discriminate.

Run:  python3 -m pytest benchmark_poc.py -q
"""

import math

from hypothesis import given, settings, strategies as st

# --------------------------------------------------------------------------
# Candidate agents (the "artificial organisms" under test)
# --------------------------------------------------------------------------

def gml_agent(r1, r2, a=0.85, log_b=0.05):
    """Conforming agent: generalized matching (Baum 1974).
    Returns predicted log behavior ratio log10(B1/B2)."""
    return log_b + a * math.log10(r1 / r2)


def broken_gml_agent(r1, r2, a=0.85, log_b=0.05):
    """Defective agent: allocation leaks absolute-rate information
    (a plausible bug: un-normalized rates entering the choice rule)."""
    return log_b + a * math.log10(r1 / r2) + 0.001 * (r1 + r2)


def exponential_value(A, D, k=0.05):
    return A * math.exp(-k * D)


def hyperbolic_value(A, D, k=0.05):
    return A / (1.0 + k * D)


# --------------------------------------------------------------------------
# MR-1: ratio scale invariance of matching
# --------------------------------------------------------------------------

rates = st.floats(min_value=0.1, max_value=300.0,
                  allow_nan=False, allow_infinity=False)
scales = st.floats(min_value=0.05, max_value=50.0,
                   allow_nan=False, allow_infinity=False)


@settings(max_examples=300)
@given(r1=rates, r2=rates, lam=scales)
def test_mr1_scale_invariance_conforming(r1, r2, lam):
    base = gml_agent(r1, r2)
    scaled = gml_agent(lam * r1, lam * r2)
    assert math.isclose(base, scaled, rel_tol=1e-9, abs_tol=1e-9)


@settings(max_examples=300)
@given(r1=rates, r2=rates, lam=scales)
def test_mr1_scale_invariance_catches_defect(r1, r2, lam):
    """The corpus must FAIL the broken agent. We assert that Hypothesis can
    find a violating input; the test passes iff a violation exists."""
    violation = not math.isclose(
        broken_gml_agent(r1, r2),
        broken_gml_agent(lam * r1, lam * r2),
        rel_tol=1e-6, abs_tol=1e-6,
    )
    # Record that violations occur on a non-trivial share of the space.
    if abs(lam - 1.0) > 1e-3 and abs(r1 + r2) > 1.0:
        assert violation, (
            f"broken agent slipped past MR-1 at r1={r1}, r2={r2}, lam={lam}"
        )


# --------------------------------------------------------------------------
# MR-2: no preference reversal under exponential discounting
# --------------------------------------------------------------------------

amounts = st.floats(min_value=1.0, max_value=1000.0, allow_nan=False)
delays = st.floats(min_value=0.0, max_value=365.0, allow_nan=False)


@settings(max_examples=300)
@given(A_small=amounts, A_large=amounts, D_small=delays,
       D_extra=st.floats(min_value=0.1, max_value=200.0, allow_nan=False),
       T=st.floats(min_value=0.0, max_value=365.0, allow_nan=False))
def test_mr2_exponential_no_reversal(A_small, A_large, D_small, D_extra, T):
    """SS available at D_small, LL at D_small + D_extra. If LL is weakly
    preferred at front-end 0, it stays preferred after adding T to both."""
    D_large = D_small + D_extra
    if exponential_value(A_large, D_large) >= exponential_value(A_small, D_small):
        assert (exponential_value(A_large, D_large + T)
                >= exponential_value(A_small, D_small + T) - 1e-12)


def test_mr2_hyperbolic_reversal_exists():
    """For the hyperbolic agent the corpus asserts the OPPOSITE: some
    parameterization must produce a reversal (the empirical phenomenon).
    SS = 50 now vs LL = 100 in 30 days, k = 0.05: LL preferred at distance,
    SS preferred up close -- i.e., preference depends on the front end."""
    k = 0.05
    # far in advance: add T = 100 to both
    far_ss = hyperbolic_value(50, 0 + 100, k)
    far_ll = hyperbolic_value(100, 30 + 100, k)
    # at the moment of choice: T = 0
    near_ss = hyperbolic_value(50, 0, k)
    near_ll = hyperbolic_value(100, 30, k)
    assert far_ll > far_ss and near_ss > near_ll, "expected reversal missing"


if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-q"]))
