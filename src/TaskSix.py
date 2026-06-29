import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from distance import distance


class PlotCanvasForTask6(FigureCanvasQTAgg):
    """Canvas for plotting spirograph-style orbits and connecting lines between two planets."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        # Dark theme
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("#181E35")
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        self._setup_dark_style()

    def _setup_dark_style(self):
        """Apply consistent dark theme styling."""
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

    def clear_graph6(self):
        """Clear the plot."""
        self.ax.clear()
        self.draw()

    def plot_data(self, planet1: str, planet2: str, num_orbits: int, num_points: int):
        """Plot spirograph-style visualization showing orbits and connecting lines."""
        self.ax.clear()

        # Planet database
        planet_data = {
            'mercury': {'au': 0.387, 'period': 0.24,  'ecc': 0.2056, 'color': 'grey'},
            'venus':   {'au': 0.723, 'period': 0.62,  'ecc': 0.0068, 'color': 'yellow'},
            'earth':   {'au': 1.000, 'period': 1.00,  'ecc': 0.0167, 'color': 'blue'},
            'mars':    {'au': 1.523, 'period': 1.88,  'ecc': 0.0934, 'color': 'red'},
            'jupiter': {'au': 5.20,  'period': 11.86, 'ecc': 0.0484, 'color': 'orange'},
            'saturn':  {'au': 9.58,  'period': 29.46, 'ecc': 0.0542, 'color': 'yellow'},
            'uranus':  {'au': 19.29, 'period': 84.01, 'ecc': 0.0472, 'color': 'cyan'},
            'neptune': {'au': 30.25, 'period': 164.79,'ecc': 0.0086, 'color': 'blue'},
            'pluto':   {'au': 39.51, 'period': 248.59,'ecc': 0.2488, 'color': 'brown'},
        }

        if planet1 not in planet_data or planet2 not in planet_data:
            raise ValueError(f"Invalid planet name(s). Available: {list(planet_data.keys())}")

        p1 = planet_data[planet1]
        p2 = planet_data[planet2]

        # Use maximum period to determine simulation length
        max_period = max(p1['period'], p2['period'])
        time_step = max_period / num_points

        # Generate angles for both planets
        theta1 = (2 * np.pi * np.arange(0, num_orbits * p1['period'], time_step)) / p1['period']
        theta2 = (2 * np.pi * np.arange(0, num_orbits * p2['period'], time_step)) / p2['period']

        # Calculate positions over time
        pos1 = self._get_positions(p1['au'], theta1, p1['ecc'])
        pos2 = self._get_positions(p2['au'], theta2, p2['ecc'])

        # Plot full orbital paths
        orbital_theta = np.radians(np.arange(1000))
        orbit1_x, orbit1_y = self._get_positions(p1['au'], orbital_theta, p1['ecc'])
        orbit2_x, orbit2_y = self._get_positions(p2['au'], orbital_theta, p2['ecc'])

        self.ax.plot(orbit1_x, orbit1_y, color=p1['color'], label=planet1.capitalize())
        self.ax.plot(orbit2_x, orbit2_y, color=p2['color'], label=planet2.capitalize())

        # Unpack coordinate tracks explicitly to fix the ValueError unpacking issue
        pos1_x, pos1_y = pos1
        pos2_x, pos2_y = pos2

        # Plot connecting lines (spirograph effect) smoothly using step arrays
        for x1, y1, x2, y2 in zip(pos1_x, pos1_y, pos2_x, pos2_y):
            self.ax.plot([x1, x2], [y1, y2], color='white', alpha=0.15, lw=0.8)

        # Final plot styling
        self.ax.set_title(f"{planet1.capitalize()} & {planet2.capitalize()} Spirograph", 
                         color="white", pad=20)
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.axis('equal')
        self.ax.legend(loc='lower right')
        self.ax.grid(True, alpha=0.2, color='gray')

        self.draw()

    def _get_positions(self, au_distance: float, theta: np.ndarray, eccentricity: float):
        """Calculate (x, y) positions for a planet at given angles."""
        # Fixed: Changed parameter name from Distance to au_distance to avoid conflict with function name
        r = distance(Distance=au_distance, theta=theta, eccentricity=eccentricity)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y