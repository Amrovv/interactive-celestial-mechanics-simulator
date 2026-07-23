"""
A few sanity checks on the orbit maths.

These only cover the plain-Python/NumPy bits (no PyQt or Matplotlib), so
they run quickly and don't need a display.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from distance import distance
from PlanetClasses import Planet, Planet3D
from planets import PLANETS, INNER, OUTER


def test_distance_perihelion_and_aphelion():
    # With r = a(1 - e^2) / (1 - e*cos(theta)):
    #   theta = 0  -> furthest point  a(1 + e)
    #   theta = pi -> closest point   a(1 - e)
    a, e = 1.0, 0.2
    assert np.isclose(distance(a, 0.0, e), a * (1 + e))
    assert np.isclose(distance(a, np.pi, e), a * (1 - e))


def test_circular_orbit_has_constant_radius():
    # A circle (e = 0) should stay exactly one semi-major axis from the Sun.
    time = np.linspace(0, 1, 50)
    x, y = Planet(period=1.0, time=time).coordinates(Distance=1.5, eccentricity=0.0)
    radius = np.sqrt(x ** 2 + y ** 2)
    assert np.allclose(radius, 1.5)


def test_coordinates_return_arrays():
    # The maths used to build these point-by-point in a loop; make sure the
    # vectorised version still hands back NumPy arrays of the right length.
    time = np.arange(0, 2, 0.01)
    x, y = Planet(1.0, time).coordinates(1.0, 0.05)
    assert isinstance(x, np.ndarray) and isinstance(y, np.ndarray)
    assert len(x) == len(time) == len(y)


def test_no_inclination_stays_flat():
    # With zero inclination the orbit should lie in the z = 0 plane.
    time = np.arange(0, 1, 0.01)
    x, y, z = Planet3D(1.0, time).coordinates(1.0, 0.0, inclination=0.0)
    assert np.allclose(z, 0.0)


def test_keplers_third_law_roughly_holds():
    # T^2 should be close to a^3 (years and AU), so T^2 / a^3 ~ 1 for every planet.
    for name, p in PLANETS.items():
        ratio = p["period"] ** 2 / p["au"] ** 3
        assert abs(ratio - 1) < 0.05, f"{name} is off: {ratio:.3f}"


def test_planet_groups_cover_everything():
    assert set(INNER) | set(OUTER) == set(PLANETS)
    assert not (set(INNER) & set(OUTER))
