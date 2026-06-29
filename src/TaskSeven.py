import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from distance import distance  


class BaseRelativeOrbitCanvas(FigureCanvasQTAgg):
    """Base class for relative orbit visualizations (2D and 3D)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

    def clear_graph(self):
        """Clear the current plot."""
        self.ax.clear()
        self.draw()


class PlotCanvasForTask7(BaseRelativeOrbitCanvas):
    """2D relative orbits visualization."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("#181E35")
        self._setup_dark_style()

    def _setup_dark_style(self):
        """Apply dark theme styling."""
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

    def plot_data(self, central_planet: str, years: float):
        """Plot relative orbits of other planets with respect to the central planet."""
        self.ax.clear()

        planet_data = self._get_planet_data()

        if central_planet not in planet_data:
            raise ValueError(f"Unknown planet: {central_planet}")

        time = np.arange(0, years, 0.001)

        inner_planets = ['mercury', 'venus', 'earth', 'mars']
        orbiting_planets = inner_planets.copy() if central_planet in inner_planets else \
                          ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

        orbiting_planets.remove(central_planet)

        # Plot relative orbits
        for planet in orbiting_planets:
            rel_x, rel_y = self._calculate_relative_positions(
                central_planet, planet, time, planet_data
            )
            self.ax.plot(rel_x, rel_y, 
                        color=planet_data[planet]['color'], 
                        label=planet.capitalize())

        # Plot central planet (Sun reference) and fixed point
        central_x, central_y = self._get_positions(central_planet, time, planet_data)
        self.ax.plot(central_x, central_y, 
                    color=planet_data['sun']['color'], 
                    label='Sun Orbit')

        self.ax.scatter(0, 0, color=planet_data[central_planet]['color'], 
                       label=central_planet.capitalize(), s=40)

        self._finalize_plot(f"Orbits relative to {central_planet.capitalize()}", "2D")

    def _get_planet_data(self):
        """Centralized planet parameters."""
        return {
            'mercury': {'au': 0.387, 'ecc': 0.2056, 'period': 0.24,  'color': 'grey'},
            'venus':   {'au': 0.723, 'ecc': 0.0068, 'period': 0.62,  'color': 'yellow'},
            'earth':   {'au': 1.000, 'ecc': 0.0167, 'period': 1.00,  'color': 'blue'},
            'mars':    {'au': 1.523, 'ecc': 0.0934, 'period': 1.88,  'color': 'red'},
            'jupiter': {'au': 5.20,  'ecc': 0.049,  'period': 11.86, 'color': 'orange'},
            'saturn':  {'au': 9.58,  'ecc': 0.056,  'period': 29.46, 'color': 'yellow'},
            'uranus':  {'au': 19.29, 'ecc': 0.046,  'period': 84.01, 'color': 'cyan'},
            'neptune': {'au': 30.25, 'ecc': 0.010,  'period': 164.8, 'color': 'blue'},
            'pluto':   {'au': 39.51, 'ecc': 0.2488, 'period': 248.09,'color': 'brown'},
            'sun':     {'color': 'orange'}
        }

    def _get_positions(self, planet: str, time: np.ndarray, planet_data: dict):
        """Calculate absolute (x, y) positions."""
        p = planet_data[planet]
        theta = 2 * np.pi * time / p['period']
        r = distance(p['au'], theta, p['ecc'])
        return r * np.cos(theta), r * np.sin(theta)

    def _calculate_relative_positions(self, center: str, other: str, 
                                    time: np.ndarray, planet_data: dict):
        """Calculate positions of one planet relative to another."""
        cx, cy = self._get_positions(center, time, planet_data)
        ox, oy = self._get_positions(other, time, planet_data)
        return ox - cx, oy - cy

    def _finalize_plot(self, title: str, dimension: str = "2D"):
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_title(title, color='white', pad=15)
        self.ax.legend(loc='lower right')
        self.ax.grid(True, alpha=0.2, color='gray')
        self.draw()


class PlotCanvasForTask7_3D(BaseRelativeOrbitCanvas):
    """3D relative orbits visualization."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("#181E35")
        self._setup_dark_background()

    def _setup_dark_background(self):
        """Configure dark 3D plot styling matching the overall app theme."""
        # 1. Turn off the opaque background panes or set them to match the dark color
        self.ax.xaxis.set_pane_color((0.094, 0.118, 0.208, 1.0)) # Hex #181E35 in RGB (0-1)
        self.ax.yaxis.set_pane_color((0.094, 0.118, 0.208, 1.0))
        self.ax.zaxis.set_pane_color((0.094, 0.118, 0.208, 1.0))

        # Optional alternative: completely transparent panes
        # self.ax.xaxis.pane.fill = False
        # self.ax.yaxis.pane.fill = False
        # self.ax.zaxis.pane.fill = False

        # 2. Make the grid lines a soft gray instead of stark black or white
        self.ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.15) # Transparent white
        self.ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.15)
        self.ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.15)

        # 3. Configure text, axes labels, and tick markings to be white
        for axis in (self.ax.xaxis, self.ax.yaxis, self.ax.zaxis):
            axis.label.set_color('white')
            axis.set_tick_params(colors='white')

        self.ax.title.set_color('white')
    def plot_data3D(self, central_planet: str, years: float):
        """Plot 3D relative orbits."""
        self.ax.clear()

        planet_data = self._get_planet_data_3d()
        if central_planet not in planet_data:
            raise ValueError(f"Unknown planet: {central_planet}")

        # Higher resolution for inner planets
        dt = 0.001 if central_planet in ['mercury', 'venus', 'earth', 'mars'] else 0.01
        time = np.arange(0, years, dt)

        inner = ['mercury', 'venus', 'earth', 'mars']
        orbiting_planets = inner.copy() if central_planet in inner else \
                          ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
        orbiting_planets.remove(central_planet)

        # Plot relative orbits
        for planet in orbiting_planets:
            rx, ry, rz = self._calculate_relative_positions_3d(
                central_planet, planet, time, planet_data
            )
            self.ax.plot(rx, ry, rz, 
                        color=planet_data[planet]['color'], 
                        label=planet.capitalize())

        # Plot Sun's orbit relative to central planet
        sx, sy, sz = self._get_positions_3d(central_planet, time, planet_data)
        self.ax.plot(sx, sy, sz, 
                    color=planet_data['sun']['color'], 
                    label='Sun Orbit')

        # Fixed central planet marker
        self.ax.scatter(0, 0, 0, color=planet_data[central_planet]['color'], 
                       label=central_planet.capitalize(), s=40)

        self._finalize_3d_plot(f"3D Orbits relative to {central_planet.capitalize()}")

    def _get_planet_data_3d(self):
        """Planet data including inclination (in degrees)."""
        return {
            'mercury': {'au': 0.387, 'ecc': 0.2056, 'period': 0.24,  'inc': 7.0,   'color': 'grey'},
            'venus':   {'au': 0.723, 'ecc': 0.0068, 'period': 0.62,  'inc': 3.4,   'color': 'yellow'},
            'earth':   {'au': 1.000, 'ecc': 0.0167, 'period': 1.00,  'inc': 0.0,   'color': 'blue'},
            'mars':    {'au': 1.523, 'ecc': 0.0934, 'period': 1.88,  'inc': 1.8,   'color': 'red'},
            'jupiter': {'au': 5.20,  'ecc': 0.049,  'period': 11.86, 'inc': 1.3,   'color': 'orange'},
            'saturn':  {'au': 9.58,  'ecc': 0.056,  'period': 29.46, 'inc': 2.5,   'color': 'yellow'},
            'uranus':  {'au': 19.29, 'ecc': 0.046,  'period': 84.01, 'inc': 0.8,   'color': 'cyan'},
            'neptune': {'au': 30.25, 'ecc': 0.010,  'period': 164.8, 'inc': 1.8,   'color': 'blue'},
            'pluto':   {'au': 39.51, 'ecc': 0.2488, 'period': 248.09,'inc': 17.2,  'color': 'brown'},
            'sun':     {'color': 'orange'}
        }

    def _get_positions_3d(self, planet: str, time: np.ndarray, planet_data: dict):
        """Calculate 3D positions with inclination."""
        p = planet_data[planet]
        inc_rad = np.deg2rad(p['inc'])
        theta = 2 * np.pi * time / p['period']
        r = distance(p['au'], theta, p['ecc'])

        x = r * np.cos(theta) * np.cos(inc_rad)
        y = r * np.sin(theta)
        z = r * np.cos(theta) * np.sin(inc_rad)
        return x, y, z

    def _calculate_relative_positions_3d(self, center: str, other: str, 
                                       time: np.ndarray, planet_data: dict):
        """Calculate relative 3D positions."""
        cx, cy, cz = self._get_positions_3d(center, time, planet_data)
        ox, oy, oz = self._get_positions_3d(other, time, planet_data)
        return ox - cx, oy - cy, oz - cz

    def _finalize_3d_plot(self, title: str):
        self.ax.set_box_aspect((1, 1, 0.3))
        self.ax.set_zlim(-15, 10)
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_zlabel('Z / AU')
        self.ax.set_title(title, color='white', pad=20)
        self.ax.legend(loc='lower right')
        self.draw()