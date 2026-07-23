import numpy as np

from distance import distance


class Planet3D:
    """Represents a planet in 3D space with orbital inclination."""

    def __init__(self, period: float, time: np.ndarray):
        """
        Initialize a 3D planet object.
        
        Args:
            period: Orbital period of the planet in years
            time: Array of time points for which to calculate positions
        """
        self.period = period
        self.time = time

    def coordinates(self, Distance: float, eccentricity: float, inclination: float):
        """
        Calculate the 3D coordinates (x, y, z) of the planet over time.
        
        Args:
            Distance: Semi-major axis in AU
            eccentricity: Orbital eccentricity (0 = circular)
            inclination: Orbital inclination in radians
            
        Returns:
            Tuple of (x_coords, y_coords, z_coords) arrays
        """
        theta = (2 * np.pi * self.time) / self.period
        r = distance(Distance, theta, eccentricity)

        # Apply inclination to x and z components
        x = r * np.cos(theta) * np.cos(inclination)
        y = r * np.sin(theta)
        z = r * np.cos(theta) * np.sin(inclination)

        return x, y, z


class Planet:
    """Represents a planet in 2D space (no inclination)."""

    def __init__(self, period: float, time: np.ndarray):
        """
        Initialize a 2D planet object.
        
        Args:
            period: Orbital period of the planet in years
            time: Array of time points for which to calculate positions
        """
        self.period = period
        self.time = time

    def coordinates(self, Distance: float, eccentricity: float):
        """
        Calculate the 2D coordinates (x, y) of the planet over time.
        
        Args:
            Distance: Semi-major axis in AU
            eccentricity: Orbital eccentricity (0 = circular)
            
        Returns:
            Tuple of (x_coords, y_coords) arrays
        """
        theta = (2 * np.pi * self.time) / self.period
        r = distance(Distance, theta, eccentricity)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        return x, y