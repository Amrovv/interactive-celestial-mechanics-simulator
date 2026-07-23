import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from planets import PLANETS, INNER, OUTER


class BasePlanetOrbitCanvas(FigureCanvasQTAgg):
    """Base canvas containing shared logic for plotting planetary orbits using Keplerian mechanics."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        # Consistent background styling
        self.ax.set_facecolor("#181E35")
        self.fig.set_facecolor("#181E35")
        
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot_data()

    def _generate_orbit_coords(self, semi_major_axis, eccentricity):
        """Calculates X and Y coordinates for an orbit using vectorized NumPy operations."""
        # Generate 1000 points spanning a complete 360-degree orbit (2*pi radians)
        theta = np.linspace(0, 2 * np.pi, 1000)
        
        # Polar equation for an ellipse relative to a focus (the Sun)
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(theta))
        
        # Convert polar coordinates (r, theta) to Cartesian (x, y)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    def _apply_common_plot_settings(self, title):
        """Applies standard labels, legends, aspect ratios, and draws the canvas."""
        self.ax.scatter(0, 0, color="yellow", label="Sun", zorder=3)
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_title(title, color="white")
        self.ax.set_aspect('equal')
        self.ax.legend()
        
        # Ensure tick markings match the dark theme aesthetic
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        self.draw()

    def plot_data(self):
        # To be overridden by child classes
        pass


class PlotCanvasForTask2_Inner(BasePlanetOrbitCanvas):
    """Canvas displaying orbits of the inner solar system."""
    
    def plot_data(self):
        self.ax.clear()

        for name in INNER:
            p = PLANETS[name]
            x, y = self._generate_orbit_coords(p['au'], p['ecc'])
            self.ax.plot(x, y, color=p['color'], label=name.capitalize())

        self._apply_common_plot_settings("Inner Planets Orbit")


class PlotCanvasForTask2_Outer(BasePlanetOrbitCanvas):
    """Canvas displaying orbits of the outer solar system."""
    
    def plot_data(self):
        self.ax.clear()

        for name in OUTER:
            p = PLANETS[name]
            x, y = self._generate_orbit_coords(p['au'], p['ecc'])
            self.ax.plot(x, y, color=p['color'], label=name.capitalize())

        self._apply_common_plot_settings("Outer Planets Orbit")