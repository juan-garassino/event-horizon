"""Varying-mass tests, ported from the legacy ``black_hole.BlackHole(inclination, mass)`` API.

The legacy test built a ``BlackHole`` per mass/inclination, computed isoradials at r = 10, 20, 30
(absolute units) for the direct and ghost images and asserted they contained no NaN, then ran
``calc_isoredshifts([-.1, 0, .2])`` as a smoke test. Isoradials are now
``eventHorizon.core.isoradial_model.Isoradial``; isoredshift curves are drawn as contours of the
redshift field (``draw_blackhole(mode="redshift")``), so the port checks that field instead.
"""

from __future__ import annotations

import numpy as np
import pytest

from eventHorizon.core.isoradial_model import Isoradial
from eventHorizon.physics.fast_geodesics import redshift_vec
from eventHorizon.physics.geodesics import impact_parameter

INCLINATIONS = (0, 45, 90, 135)


@pytest.mark.parametrize("mass", [1.0, 2.0])
def test_varying_mass(mass):
    for inclination in INCLINATIONS:
        for radius in (10.0, 20.0, 30.0):
            for image_order in (0, 1):
                ir = Isoradial(mass=mass, inclination=inclination, radius=radius, image_order=image_order)
                ir.calculate_coordinates(angular_precision=10)
                assert not np.any(np.isnan(ir.impact_parameters)), "Isoradials contain nan values"
                assert not np.any(np.isnan(ir.angles)), "Isoradials contain nan values"


@pytest.mark.parametrize("n", [0, 1])
def test_impact_parameter_scales_linearly_with_mass(objective, n):
    """Schwarzschild has a single length scale: b(alpha; r*M, M) = M * b(alpha; r, 1)."""
    alphas = np.linspace(0.0, 2 * np.pi, 8, endpoint=False)
    incl = np.radians(60)
    b_unit = impact_parameter(alphas, 10.0, incl, n, 1.0, objective_func=objective)
    b_heavy = impact_parameter(alphas, 20.0, incl, n, 2.0, objective_func=objective)
    np.testing.assert_allclose(b_heavy, 2.0 * b_unit, rtol=1e-3)


@pytest.mark.parametrize("mass", [1.0, 2.0])
@pytest.mark.parametrize("inclination", INCLINATIONS)
def test_isoredshift_levels_are_reachable(objective, mass, inclination):
    """Port of the ``calc_isoredshifts([-.1, 0, .2])`` smoke test: the redshift field the contours
    are drawn from is finite, and with line-of-sight orbital motion (inclination != 0) it spans
    blue- and redshift. The -0.1 level is asserted only edge-on: on this sampled grid the
    strongest blueshift at 45 degrees is about -0.098."""
    incl = np.radians(inclination)
    alphas = np.linspace(0.0, 2 * np.pi, 24, endpoint=False)
    z = []
    for radius in mass * np.array([6.5, 10.0, 20.0, 30.0]):
        bs = impact_parameter(alphas, radius, incl, 0, mass, objective_func=objective)
        z.append(redshift_vec(np.full_like(alphas, radius), alphas, incl, mass, bs) - 1.0)
    z = np.concatenate(z)
    assert np.all(np.isfinite(z))
    if inclination == 0:
        assert np.all(z > 0)  # face-on: pure gravitational + transverse Doppler redshift
    else:
        assert z.min() < 0.0 < 0.2 < z.max()
    if inclination == 90:
        assert z.min() < -0.1
