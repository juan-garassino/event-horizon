"""Shared fixtures and helpers for the eventHorizon test suite.

Sources that motivated each fixture:

- ``objective`` -- ``eventHorizon/physics/geodesics.py::lambda_objective`` lambdifies the full
  Luminet (1979) eq.13 sympy expression; building it once per session keeps the suite fast.
- ``swept_azimuth`` -- independent check of ``impact_parameter`` / ``calc_impact_parameter_exact``
  (``eventHorizon/physics/disk_physics.py``): integrates the Schwarzschild photon orbit equation
  ``dphi/du = 1 / sqrt(1/b^2 - u^2 (1 - 2 M u))`` by quadrature, without any elliptic functions.

All quantities are in geometric units (G = c = 1); mass ``M`` sets the length scale.
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest
from scipy.integrate import quad

from eventHorizon.physics.geodesics import lambda_objective


@pytest.fixture(scope="session")
def objective():
    """Lambdified eq.13 residual ``f(P, alpha, theta_0, r, N, M)``."""
    return lambda_objective()


def _swept_azimuth(periastron: float, r: float, mass: float) -> tuple[float, float]:
    """Azimuth a photon sweeps travelling from radius ``r`` to infinity.

    Returns ``(outward, via_periastron)``: the sweep if the photon heads straight out
    (only possible when ``r > periastron``), and the sweep if it first falls in to
    ``periastron`` and then escapes. The substitution ``u = u_P - s^2`` removes the
    integrable 1/sqrt singularity at the turning point.
    """
    b = np.sqrt(periastron**3 / (periastron - 2.0 * mass))
    u_p = 1.0 / periastron
    u_r = 1.0 / r

    def integrand(u: float) -> float:
        return 1.0 / np.sqrt(1.0 / b**2 - u**2 * (1.0 - 2.0 * mass * u))

    def substituted(s: float) -> float:
        return 2.0 * s * integrand(u_p - s * s)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        outward = quad(integrand, 0.0, u_r)[0] if r > periastron else np.nan
        to_infinity = quad(substituted, 0.0, np.sqrt(u_p))[0]
        from_r = quad(substituted, 0.0, np.sqrt(u_p - u_r))[0] if u_r < u_p else 0.0
    return outward, to_infinity + from_r


@pytest.fixture(scope="session")
def swept_azimuth():
    return _swept_azimuth
