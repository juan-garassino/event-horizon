"""Isoradial tests, ported from the legacy ``black_hole.BlackHole.calc_isoradials`` API.

The legacy ``BlackHole`` container is gone; one curve is now an
``eventHorizon.core.isoradial_model.Isoradial(mass, inclination, radius, image_order)`` and the
vectorized solver is ``eventHorizon.physics.geodesics.impact_parameter``. The legacy test drew a
random inclination and random radii; the port uses a fixed grid so failures are reproducible.
"""

from __future__ import annotations

import numpy as np
import pytest

from eventHorizon.core.isoradial_model import Isoradial
from eventHorizon.physics.geodesics import impact_parameter

ANGULAR_PRECISION = 16


def _isoradial(mass, inclination, radius, image_order):
    ir = Isoradial(mass=mass, inclination=inclination, radius=radius, image_order=image_order)
    ir.calculate_coordinates(angular_precision=ANGULAR_PRECISION)
    return ir


@pytest.mark.parametrize("inclination", [10, 80, 135])
def test_isoradials_are_calculated_for_every_radius_and_order(inclination):
    radii = np.linspace(3.01, 60.0, 4)
    isoradials = {r: (_isoradial(1.0, inclination, r, 0), _isoradial(1.0, inclination, r, 1)) for r in radii}
    assert len(isoradials) == len(radii)
    for direct, ghost in isoradials.values():
        for ir in (direct, ghost):
            assert len(ir.angles) == len(ir.impact_parameters) == ANGULAR_PRECISION
            assert np.all(np.isfinite(ir.impact_parameters))
            assert len(ir.cartesian_x) == len(ir.cartesian_y) == ANGULAR_PRECISION


def test_isoradial_redshift_factors_follow_the_curve():
    ir = _isoradial(1.0, 80, 10.0, 0)
    ir.calculate_redshift_factors()
    z = np.asarray(ir.redshift_factors)
    assert z.shape == (ANGULAR_PRECISION,)
    assert np.all(z > 0)
    assert z.min() < 1.0 < z.max()  # approaching side blueshifted, receding side redshifted


@pytest.mark.parametrize("radius", [6.0, 10.0, 30.0])
@pytest.mark.parametrize("n", [0, 1])
def test_face_on_isoradials_are_circles(objective, radius, n):
    alphas = np.linspace(0.0, 2 * np.pi, 12, endpoint=False)
    bs = impact_parameter(alphas, radius, 0.0, n, 1.0, objective_func=objective)
    assert np.ptp(bs) < 1e-9 * bs.mean()
    if n == 0:
        assert bs.mean() > radius  # lensing magnifies the ring
    else:
        assert 3.0 * np.sqrt(3.0) < bs.mean() < radius  # ghost ring hugs the photon ring


@pytest.mark.parametrize("inclination", [30, 80])
@pytest.mark.parametrize("n", [0, 1])
def test_isoradials_are_mirror_symmetric(objective, inclination, n):
    """The disk's apparent shape depends on alpha only through cos(alpha): b(alpha) = b(2*pi - alpha)."""
    alphas = np.linspace(0.1, np.pi - 0.1, 7)
    incl = np.radians(inclination)
    b_upper = impact_parameter(alphas, 15.0, incl, n, 1.0, objective_func=objective)
    b_lower = impact_parameter(2 * np.pi - alphas, 15.0, incl, n, 1.0, objective_func=objective)
    np.testing.assert_allclose(b_upper, b_lower, rtol=1e-9)


def test_ghost_images_lie_inside_direct_images_on_the_far_side(objective):
    alphas = np.linspace(np.pi / 2, 3 * np.pi / 2, 7)
    incl = np.radians(80)
    direct = impact_parameter(alphas, 20.0, incl, 0, 1.0, objective_func=objective)
    ghost = impact_parameter(alphas, 20.0, incl, 1, 1.0, objective_func=objective)
    assert np.all(ghost < direct)
    assert np.all(ghost > 3.0 * np.sqrt(3.0))
