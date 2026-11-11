"""Physics and math tests for the Luminet (1979) formalism in ``eventHorizon.physics``.

Ported from the legacy ``src.math.*`` test module (SymbolicExpressions, NumericalFunctions,
GeometricFunctions, PhysicalFunctions, Utilities, Optimization, ImpactParameter, Simulation).
Those classes became module-level functions in ``eventHorizon/physics/geodesics.py`` and
``eventHorizon/physics/disk_physics.py``. The legacy tests mocked collaborators and only asserted
types; the ports run the real code and check analytic values instead.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import scipy.special as sps
import sympy as sy

from eventHorizon.core.isoradial_model import Isoradial
from eventHorizon.physics import disk_physics as dp
from eventHorizon.physics import geodesics as geo
from eventHorizon.physics.fast_geodesics import (
    build_impact_table,
    flux_intrinsic_vec,
    flux_observed_vec,
    generate_particles_fast,
    redshift_vec,
)
from eventHorizon.physics.spacetime import SpacetimeGeometry

M, P, Q, N = sy.symbols("M P Q N")
alpha, theta_0, r, b = sy.symbols("alpha theta_0 r b")

INCL_80 = np.radians(80.0)


# ---------------------------------------------------------------------------
# Characteristic radii and the critical impact parameter
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mass", [1.0, 2.5])
def test_schwarzschild_characteristic_radii(mass):
    geometry = SpacetimeGeometry(mass=mass)
    assert geometry.calculate_horizon_radius() == pytest.approx(2.0 * mass)
    assert geometry.calculate_photon_sphere_radius() == pytest.approx(3.0 * mass)
    assert geometry.calculate_isco_radius() == pytest.approx(6.0 * mass)

    model = Isoradial(mass=mass)
    assert model.schwarzschild_radius == pytest.approx(2.0 * mass)
    assert model.isco_radius == pytest.approx(6.0 * mass)
    assert model.critical_impact_parameter == pytest.approx(3.0 * np.sqrt(3.0) * mass)


@pytest.mark.parametrize("mass", [1.0, 2.0])
def test_photon_sphere_periastron_gives_critical_impact_parameter(mass):
    """b(P) = sqrt(P^3 / (P - 2M)) is minimal at the photon sphere P = 3M, where b = 3*sqrt(3)*M."""
    b_c = 3.0 * np.sqrt(3.0) * mass
    assert dp.calc_b_from_periastron(3.0 * mass, mass) == pytest.approx(b_c, rel=1e-12)

    periastra = mass * np.array([2.5, 2.9, 2.99, 3.01, 3.1, 4.0, 10.0])
    assert np.all(dp.calc_b_from_periastron(periastra, mass) > b_c)


# ---------------------------------------------------------------------------
# Symbolic expressions (legacy TestSymbolicExpressions)
# ---------------------------------------------------------------------------


def test_expr_q():
    assert geo.expr_q() == sy.sqrt((P - 2 * M) * (P + 6 * M))


def test_expr_b():
    assert geo.expr_b() == sy.sqrt(P**3 / (P - 2 * M))


def test_expr_k():
    assert geo.expr_k() == sy.sqrt((Q - P + 6 * M) / (2 * Q))


def test_expr_zeta_inf():
    assert geo.expr_zeta_inf() == sy.asin(sy.sqrt((Q - P + 2 * M) / (Q - P + 6 * M)))


def test_expr_gamma():
    expected = sy.acos(sy.cos(alpha) / sy.sqrt(sy.cos(alpha) ** 2 + sy.tan(theta_0) ** -2))
    assert geo.expr_gamma() == expected


def test_expr_u_has_direct_and_ghost_branches():
    u = geo.expr_u()
    assert isinstance(u, sy.Piecewise)
    assert len(u.args) == 2  # n == 0 (direct) and n >= 1 (ghost)


def test_expr_one_plus_z():
    expected = (1 + sy.sqrt(M / r**3) * b * sy.sin(theta_0) * sy.sin(alpha)) / sy.sqrt(1 - 3 * M / r)
    assert geo.expr_one_plus_z() == expected


def test_expr_fs_uses_page_thorne_log_coefficient():
    """Intrinsic disk flux. The legacy test pinned Luminet's printed sqrt(3)/3 log coefficient;
    the code deliberately uses the Page & Thorne (1974) value sqrt(3)/2 (Luminet eq.15 typo,
    see the comment in geodesics.expr_fs). test_flux_intrinsic_peaks_near_9_55M confirms it."""
    m, rstar, mdot = sy.symbols(r"M, r^*, \dot{m}")
    expected = (
        ((3 * m * mdot) / (8 * sy.pi))
        * (1 / ((rstar - 3) * rstar ** (5 / 2)))
        * (
            sy.sqrt(rstar)
            - sy.sqrt(6)
            + (sy.sqrt(3) / 2)
            * sy.ln(
                ((sy.sqrt(rstar) + sy.sqrt(3)) * (sy.sqrt(6) - sy.sqrt(3)))
                / ((sy.sqrt(rstar) - sy.sqrt(3)) * (sy.sqrt(6) + sy.sqrt(3)))
            )
        )
    )
    assert geo.expr_fs() == expected


# ---------------------------------------------------------------------------
# Numerical helpers (legacy TestNumericalFunctions)
# ---------------------------------------------------------------------------

PERIASTRON = 10.0
MASS = 1.0


def test_calc_q():
    expected = np.sqrt((PERIASTRON - 2 * MASS) * (PERIASTRON + 6 * MASS))
    assert dp.calc_q(PERIASTRON, MASS) == pytest.approx(expected, abs=1e-12)


def test_calc_b_from_periastron():
    expected = np.sqrt(PERIASTRON**3 / (PERIASTRON - 2 * MASS))
    assert dp.calc_b_from_periastron(PERIASTRON, MASS) == pytest.approx(expected, abs=1e-12)


def test_k2_and_its_square_root_match_expr_k():
    q = dp.calc_q(PERIASTRON, MASS)
    expected_k2 = (q - PERIASTRON + 6 * MASS) / (2 * q)
    assert dp.k2(PERIASTRON, MASS) == pytest.approx(expected_k2, abs=1e-12)

    k = geo.lambdify(["P", "M", "Q"], geo.expr_k())(PERIASTRON, MASS, q)
    assert k == pytest.approx(np.sqrt(expected_k2), abs=1e-12)
    assert 0.0 < expected_k2 < 1.0  # valid elliptic parameter


def test_zeta_inf():
    q = dp.calc_q(PERIASTRON, MASS)
    expected = np.arcsin(np.sqrt((q - PERIASTRON + 2 * MASS) / (q - PERIASTRON + 6 * MASS)))
    assert dp.zeta_inf(PERIASTRON, MASS) == pytest.approx(expected, abs=1e-12)


# ---------------------------------------------------------------------------
# Geometry (legacy TestGeometricFunctions)
# ---------------------------------------------------------------------------


def test_cos_gamma():
    a, incl = np.pi / 4, np.pi / 3
    expected = np.cos(a) / np.sqrt(np.cos(a) ** 2 + 1 / np.tan(incl) ** 2)
    assert dp.cos_gamma(a, incl) == pytest.approx(expected, abs=1e-12)


def test_cos_gamma_face_on_is_zero():
    """Face-on (inclination 0): every disk point is 90 degrees from the line of sight."""
    assert dp.cos_gamma(np.pi / 4, 0.0) == pytest.approx(0.0, abs=1e-12)


def test_ellipse_fallback_matches_symbolic_ellipse():
    """r*sin(gamma) and r / sqrt(1 + tan^2(i) cos^2(alpha)) are the same Newtonian projection."""
    ellipse = geo.lambdify(["r", "alpha", "theta_0"], geo.expr_ellipse())
    for a in np.linspace(0.0, 2 * np.pi, 9):
        for incl in (np.pi / 6, np.pi / 3, INCL_80):
            assert dp.ellipse_fallback(10.0, a, incl) == pytest.approx(ellipse(10.0, a, incl), rel=1e-12)
    # Face-on the projection is the circle of radius r.
    assert dp.ellipse_fallback(10.0, 1.0, 0.0) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# Redshift and flux (legacy TestPhysicalFunctions)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("radius", [6.0, 10.0, 100.0])
def test_redshift_without_doppler_is_circular_orbit_factor(radius):
    """With no line-of-sight velocity (alpha = 0, or face-on) 1+z = 1/sqrt(1 - 3M/r):
    gravitational redshift combined with the transverse Doppler shift of a circular orbit."""
    expected = 1.0 / np.sqrt(1.0 - 3.0 / radius)
    assert dp.redshift_factor(radius, 0.0, INCL_80, 1.0, 7.0) == pytest.approx(expected, rel=1e-12)
    assert dp.redshift_factor(radius, 1.3, 0.0, 1.0, 7.0) == pytest.approx(expected, rel=1e-12)


def test_redshift_at_isco_is_sqrt2():
    assert dp.redshift_factor(6.0, 0.0, INCL_80, 1.0, 6.0) == pytest.approx(np.sqrt(2.0), rel=1e-12)


def test_redshift_tends_to_one_far_from_hole():
    assert dp.redshift_factor(1e8, np.pi / 2, INCL_80, 1.0, 1e8) == pytest.approx(1.0, abs=1e-3)


def test_redshift_receding_side_is_redder_than_approaching_side():
    receding = dp.redshift_factor(10.0, np.pi / 2, INCL_80, 1.0, 10.0)
    approaching = dp.redshift_factor(10.0, 3 * np.pi / 2, INCL_80, 1.0, 10.0)
    no_doppler = dp.redshift_factor(10.0, 0.0, INCL_80, 1.0, 10.0)
    assert approaching < 1.0 < no_doppler < receding  # the approaching side is net blueshifted


def test_redshift_inside_photon_sphere_returns_neutral_sentinel():
    assert dp.redshift_factor(2.5, np.pi / 2, INCL_80, 1.0, 5.0) == 1.0


def test_redshift_implementations_agree():
    radii = np.array([6.5, 10.0, 25.0])
    angles = np.array([0.3, 2.0, 4.5])
    bs = np.array([6.0, 9.0, 26.0])
    vec = redshift_vec(radii, angles, INCL_80, 1.0, bs)
    sym = sy.lambdify(["alpha", "b", "theta_0", "M", "r"], geo.expr_one_plus_z())
    engine = geo.UnifiedGeodesics(mass=1.0)
    for i in range(3):
        scalar = dp.redshift_factor(radii[i], angles[i], INCL_80, 1.0, bs[i])
        assert vec[i] == pytest.approx(scalar, rel=1e-12)
        assert sym(angles[i], bs[i], INCL_80, 1.0, radii[i]) == pytest.approx(scalar, rel=1e-12)
        assert engine.calculate_redshift_factor(radii[i], angles[i], INCL_80, bs[i]) == pytest.approx(scalar, rel=1e-12)


def test_flux_intrinsic_vanishes_at_and_inside_isco():
    for radius in (2.5, 4.0, 6.0):
        assert dp.flux_intrinsic(radius, 1.0, 1.0) == 0.0
    # Zero-torque inner boundary: the flux rises continuously from zero just outside r = 6M.
    assert 0.0 < dp.flux_intrinsic(6.001, 1.0, 1.0) < 1e-6


def test_flux_intrinsic_is_positive_outside_isco():
    for radius in (6.5, 20.0, 1000.0):
        assert dp.flux_intrinsic(radius, 0.1, 1.0) > 0.0
    assert dp.flux_intrinsic(1000.0, 1.0, 1.0) < 1e-3 * dp.flux_intrinsic(10.0, 1.0, 1.0)


def test_flux_intrinsic_peaks_near_9_55M():
    """Page-Thorne (Novikov-Thorne) flux for a Schwarzschild hole peaks at r ~= 9.55M.
    With Luminet's printed sqrt(3)/3 coefficient the peak would move, so this pins the fix."""
    radii = np.linspace(6.01, 30.0, 4000)
    flux = flux_intrinsic_vec(radii, 1.0)
    assert radii[np.argmax(flux)] == pytest.approx(9.55, abs=0.05)
    scalar = np.array([dp.flux_intrinsic(x, 1.0, 1.0) for x in radii[::400]])
    np.testing.assert_allclose(flux[::400], scalar, rtol=1e-12)


def test_flux_observed_is_intrinsic_over_one_plus_z_to_the_fourth():
    intrinsic = dp.flux_intrinsic(20.0, 0.1, 1.0)
    assert dp.flux_observed(20.0, 0.1, 1.0, 1.5) == pytest.approx(intrinsic / 1.5**4, rel=1e-12)
    assert dp.flux_observed(20.0, 0.1, 1.0, 0.0) == 0.0
    vec = flux_observed_vec(np.array([20.0]), 1.0, np.array([1.5]), accretion_rate=0.1)
    assert vec[0] == pytest.approx(intrinsic / 1.5**4, rel=1e-12)


# ---------------------------------------------------------------------------
# Utilities and root finding (legacy TestUtilities / TestOptimization)
# ---------------------------------------------------------------------------


def test_lambdify_plain_and_elliptic():
    x, y = sy.symbols("x y")
    assert geo.lambdify((x, y), x**2 + y**2)(2, 3) == pytest.approx(13.0)

    u, m = sy.symbols("u m")
    sn = sy.Function("sn")
    f = geo.lambdify((u, m), sn(u, m) ** 2)
    assert f(0.7, 0.3) == pytest.approx(sps.ellipj(0.7, 0.3)[0] ** 2, rel=1e-12)


def test_find_brackets_locates_sign_change():
    x = np.linspace(0.0, 10.0, 11)
    xmin, xmax = geo.find_brackets(lambda xx, yy: xx**2 - 4.0 + 0.0 * yy, x, np.zeros(3), ())
    np.testing.assert_array_equal(xmin, [1.0, 1.0, 1.0])
    np.testing.assert_array_equal(xmax, [2.0, 2.0, 2.0])


def test_fast_root_converges_to_root():
    """Legacy midpoint-method test, ported to fast_root (the bisection used by impact_parameter)."""
    x = np.linspace(0.0, 10.0, 11)
    root = geo.fast_root(lambda xx, yy: xx**2 - 4.0 + 0.0 * yy, x, np.zeros(3), (), tol=1e-6, max_steps=40)
    np.testing.assert_allclose(root, 2.0, atol=1e-5)


def test_fast_root_returns_nan_without_sign_change():
    x = np.linspace(0.0, 10.0, 11)
    root = geo.fast_root(lambda xx, yy: xx**2 + 1.0 + 0.0 * yy, x, np.zeros(2), ())
    assert np.all(np.isnan(root))


# ---------------------------------------------------------------------------
# Impact parameter: eq.13 solvers (legacy TestImpactParameter)
# ---------------------------------------------------------------------------

SOLVER_CASES = [  # (inclination deg, radius, image order)
    (0.0, 10.0, 0),
    (0.0, 10.0, 1),
    (45.0, 10.0, 0),
    (45.0, 20.0, 1),
    (80.0, 6.0, 0),
    (80.0, 6.0, 1),
    (80.0, 30.0, 0),
    (80.0, 30.0, 1),
]


def _solve_periastron(objective, alphas, incl, radius, n, mass=1.0):
    alpha_solve = (alphas + np.pi) % (2 * np.pi) if n % 2 else alphas
    return geo.fast_root(objective, np.linspace(2.1, 50.0, 1000), alpha_solve, (incl, radius, n, mass))


@pytest.mark.parametrize("incl_deg, radius, n", SOLVER_CASES)
def test_eq13_solution_matches_photon_orbit_quadrature(objective, swept_azimuth, incl_deg, radius, n):
    """Independent check of the elliptic-integral solution: the photon with the solved
    periastron must sweep exactly the azimuth that eq.13 asks for. Direct image: gamma.
    Ghost image (angle flipped by pi): 2*pi - gamma'."""
    incl = np.radians(incl_deg)
    alphas = np.linspace(0.0, 2 * np.pi, 8, endpoint=False)
    periastra = _solve_periastron(objective, alphas, incl, radius, n)
    solved = ~np.isnan(periastra)
    assert solved.sum() >= 3, "eq.13 should have periastron solutions on the far side of the disk"

    for a, p in zip(alphas[solved], periastra[solved]):
        assert p > 3.0, "a photon that escapes to the observer cannot dip inside the photon sphere"
        if n == 0:
            target = np.arccos(dp.cos_gamma(a, incl))
            outward, via_periastron = swept_azimuth(p, radius, 1.0)
            error = np.nanmin([abs(outward - target), abs(via_periastron - target)])
        else:
            target = 2 * np.pi - np.arccos(dp.cos_gamma((a + np.pi) % (2 * np.pi), incl))
            error = abs(swept_azimuth(p, radius, 1.0)[1] - target)
        assert error < 1e-3, f"alpha={a:.3f}: swept azimuth off by {error:.2e} rad"


@pytest.mark.parametrize("incl_deg, radius, n", SOLVER_CASES)
def test_vectorized_and_exact_impact_parameter_agree(objective, incl_deg, radius, n):
    incl = np.radians(incl_deg)
    alphas = np.linspace(0.0, 2 * np.pi, 8, endpoint=False)
    vectorized = geo.impact_parameter(alphas, radius, incl, n, 1.0, objective_func=objective)
    exact = [dp.calc_impact_parameter_exact(radius, a, incl, n, 1.0) for a in alphas]
    for a, bv, be in zip(alphas, vectorized, exact):
        assert be is not None, f"no impact parameter at alpha={a:.3f}"
        assert bv == pytest.approx(be, rel=1e-3), f"alpha={a:.3f}"


def test_eq13_residual_vanishes_at_solved_periastron(objective):
    alphas = np.array([np.pi / 2, np.pi])
    periastra = _solve_periastron(objective, alphas, INCL_80, 10.0, 0)
    for a, p in zip(alphas, periastra):
        residual = dp.eq13(p, 10.0, a, INCL_80, 0, 1.0)
        assert isinstance(residual, float)
        assert abs(residual) < 1e-4
        assert dp.calc_impact_parameter_exact(10.0, a, INCL_80, 0, 1.0) == pytest.approx(
            dp.calc_b_from_periastron(p, 1.0), rel=1e-4
        )


def test_exact_solver_uses_newtonian_ellipse_on_near_side():
    """At 80 degrees the near side (alpha = 0) has no periastron solution for the direct image;
    the solver falls back to the Newtonian projection r*cos(i)."""
    b0 = dp.calc_impact_parameter_exact(10.0, 0.0, INCL_80, 0, 1.0)
    assert b0 == pytest.approx(dp.ellipse_fallback(10.0, 0.0, INCL_80))
    assert b0 == pytest.approx(10.0 * np.cos(INCL_80), rel=1e-9)


# ---------------------------------------------------------------------------
# Simulation pipeline (legacy TestSimulation)
# ---------------------------------------------------------------------------


def test_reorient_alpha():
    a = np.array([0, np.pi / 2, np.pi, 3 * np.pi / 2])
    np.testing.assert_array_almost_equal(geo.reorient_alpha(a, 1), [np.pi, 3 * np.pi / 2, 0, np.pi / 2])
    np.testing.assert_array_equal(geo.reorient_alpha(a, 0), a)


def test_simulate_flux_matches_numeric_disk_physics(objective):
    a = np.array([0.0, np.pi / 2, np.pi, 3 * np.pi / 2])
    radius, incl = 10.0, np.pi / 4
    alpha_out, bs, opz, flux = geo.simulate_flux(a, radius, incl, 0, 1.0, objective_func=objective)
    for arr in (alpha_out, bs, opz, flux):
        assert arr.shape == (4,)
    np.testing.assert_array_equal(alpha_out, a)
    for i in range(4):
        assert opz[i] == pytest.approx(dp.redshift_factor(radius, a[i], incl, 1.0, bs[i]), rel=1e-12)
        # normalized bolometric flux = F_obs / (3 M mdot / 8 pi) with M = mdot = 1
        expected = dp.flux_observed(radius, 1.0, 1.0, opz[i]) / (3.0 / (8.0 * np.pi))
        assert flux[i] == pytest.approx(expected, rel=1e-9)


def test_generate_particles_fast_builds_consistent_dataframes():
    """Legacy generate_image_data -> DataFrame, ported to the lookup-table particle generator."""
    tables = {
        n: build_impact_table(1.0, INCL_80, n=n, n_alpha=36, n_r=6, r_min=6.0, r_max=30.0)[0] for n in (0, 1)
    }
    direct, ghost, min_flux, max_flux = generate_particles_fast(
        300, 1.0, INCL_80, r_inner=6.0, r_outer=30.0, table_direct=tables[0], table_ghost=tables[1]
    )
    columns = ["X", "Y", "flux_o", "radius", "angle", "impact_parameter", "z_factor"]
    for df in (direct, ghost):
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == columns
        assert 0 < len(df) <= 300
        assert df[["X", "Y"]].notna().all().all()
        assert df["radius"].between(6.0, 30.0).all()
        assert (df["z_factor"] > 0).all()
        assert (df["flux_o"] >= 0).all()
        np.testing.assert_allclose(np.hypot(df["X"], df["Y"]), df["impact_parameter"].abs(), rtol=1e-9)
    assert min_flux == 0.0
    assert max_flux == pytest.approx(max(direct["flux_o"].max(), ghost["flux_o"].max()))
