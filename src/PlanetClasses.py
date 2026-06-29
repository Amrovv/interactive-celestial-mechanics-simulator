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
            Tuple of (x_coords, y_coords, z_coords) lists
        """
        theta = (2 * np.pi * self.time) / self.period

        x_coordinate = []
        y_coordinate = []
        z_coordinate = []

        for i in range(len(self.time)):
            r = distance(Distance, theta[i], eccentricity)

            # Apply inclination to x and z components
            x = r * np.cos(theta[i]) * np.cos(inclination)
            y = r * np.sin(theta[i])
            z = r * np.cos(theta[i]) * np.sin(inclination)

            x_coordinate.append(x)
            y_coordinate.append(y)
            z_coordinate.append(z)

        return x_coordinate, y_coordinate, z_coordinate


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
            Tuple of (x_coords, y_coords) lists
        """
        theta = (2 * np.pi * self.time) / self.period

        x_coordinate = []
        y_coordinate = []

        for i in range(len(self.time)):
            r = distance(Distance, theta[i], eccentricity)

            x = r * np.cos(theta[i])
            y = r * np.sin(theta[i])

            x_coordinate.append(x)
            y_coordinate.append(y)

        return x_coordinate, y_coordinate