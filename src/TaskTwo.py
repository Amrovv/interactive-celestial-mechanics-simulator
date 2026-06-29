import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


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
        
        # Configuration: (semi_major_axis, eccentricity, color, label)
        inner_planets = [
            (0.387, 0.2056, "grey", "Mercury"),
            (0.723, 0.0068, "yellow", "Venus"),
            (1.000, 0.0167, "blue", "Earth"),
            (1.523, 0.0934, "red", "Mars")
        ]
        
        for axis, ecc, color, name in inner_planets:
            x, y = self._generate_orbit_coords(axis, ecc)
            self.ax.plot(x, y, color=color, label=name)
            
        self._apply_common_plot_settings("Inner Planets Orbit")


class PlotCanvasForTask2_Outer(BasePlanetOrbitCanvas):
    """Canvas displaying orbits of the outer solar system."""
    
    def plot_data(self):
        self.ax.clear()
        
        # Configuration: (semi_major_axis, eccentricity, color, label)
        outer_planets = [
            (5.20, 0.048775, "orange", "Jupiter"),
            (9.58, 0.0555, "red", "Saturn"),
            (19.29, 0.0472, "cyan", "Uranus"),
            (30.25, 0.0086, "blue", "Neptune"),
            (39.51, 0.25, "brown", "Pluto")
        ]
        
        for axis, ecc, color, name in outer_planets:
            x, y = self._generate_orbit_coords(axis, ecc)
            self.ax.plot(x, y, linestyle='-', color=color, label=name)
            
        self._apply_common_plot_settings("Outer Planets Orbit")