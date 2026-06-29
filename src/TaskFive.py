import numpy as np
from matplotlib.figure import Figure
from scipy.interpolate import interp1d
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class PlotCanvasForTask5(FigureCanvasQTAgg):
    """Canvas for plotting orbital polar angle vs time for Pluto (Task 5)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        # Dark theme setup
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("#181E35")
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        self._setup_dark_style()

    def _setup_dark_style(self):
        """Apply consistent dark theme styling to the plot."""
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')

    def update_graph(self, eccentricity: float):
        """Update the plot with a new eccentricity value."""
        self.ax.clear()
        self.plot_data(eccentricity)
        self.draw()

    def plot_data(self, eccentricity: float):
        """Plot orbital angle vs time for given eccentricity."""
        time = np.arange(0, 750)

        # Calculate angles for eccentric and circular orbits
        theta_ecc = self._angle_vs_time(time, period=248.348, eccentricity=eccentricity, theta0=0)
        theta_circ = self._angle_vs_time(time, period=248.348, eccentricity=0.0, theta0=0)

        # Plot both curves
        self.ax.plot(time, theta_ecc, color='green', 
                    label=f'Eccentricity = {eccentricity:.4f}')
        self.ax.plot(time, theta_circ, color='blue', 
                    label='Eccentricity = 0 (Circular)')

        # Configure plot appearance
        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 20)
        
        self.ax.set_xlabel('Time (years)', color='white')
        self.ax.set_ylabel('Orbital Polar Angle (radians)', color='white')
        self.ax.set_title('Orbital Angle vs Time for Pluto', color='white')
        
        self.ax.legend()
        self.ax.grid(True, alpha=0.3, color='gray')

    def _angle_vs_time(self, time: np.ndarray, period: float, 
                      eccentricity: float, theta0: float = 0.0) -> np.ndarray:
        """
        Compute true anomaly (orbital polar angle) as a function of time
        using numerical integration of the Kepler problem.
        """
        if eccentricity == 0.0:
            # Simple circular orbit case
            return (2 * np.pi / period) * time + theta0

        dtheta = 1 / 1000
        N = np.ceil(time[-1] / period) + 1
        
        theta = np.arange(theta0, 2 * np.pi * N + theta0, dtheta)
        
        # Instantaneous factor from Kepler's second law
        f = (1 - eccentricity * np.cos(theta)) ** (-2)
        
        L = len(theta)
        # Simpson's rule coefficients: 1, 4, 2, 4, 2, ..., 4, 1
        coefficients = np.ones(L)
        coefficients[1:-1:2] = 4
        coefficients[2:-1:2] = 2
        
        constant_factor = (period * (1 - eccentricity**2)**(3/2) / 
                          (2 * np.pi)) * dtheta / 3
        
        # Cumulative time from integration
        tt = constant_factor * np.cumsum(coefficients * f)
        
        # Interpolate to get theta at desired time points
        theta_interp = interp1d(tt, theta, kind='cubic', 
                               fill_value='extrapolate', bounds_error=False)
        
        return theta_interp(time)

