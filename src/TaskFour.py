import numpy as np
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PlanetClasses import Planet3D
from distance import distance


class Base3DPlanetCanvas(FigureCanvasQTAgg):
    """Base class for 3D planet orbit visualizations."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, speed_modifier=1):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Styling
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("#181E35")
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        
        self.animation = []        # Store active animations
        self.planets = {}          # Will store planet data: name -> dict of coords and artist
        self.speed_modifier = speed_modifier  # Control step execution velocity via frame sharing
        
        self._setup_dark_background()
        super().__init__(self.fig)
        self.setParent(parent)

    def _setup_dark_background(self):
        """Configure dark theme for the 3D plot."""
        self.ax.xaxis._axinfo["grid"]["color"] = "black"
        self.ax.yaxis._axinfo["grid"]["color"] = "black"
        self.ax.zaxis._axinfo["grid"]["color"] = "black"

        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
            axis.label.set_color('white')
            axis.set_pane_color((1, 1, 1, 1))
            axis.set_tick_params(colors='white')

        self.ax.title.set_color('white')

    def update_point(self, frame: int, x: np.ndarray, y: np.ndarray, z: np.ndarray, point):
        """Update position of a single planet point with dynamic speed modifier safety."""
        idx = (frame // self.speed_modifier) % len(x)
        point.set_data([x[idx]], [y[idx]])
        point.set_3d_properties(z[idx])
        return point

    def start_animation(self):
        """Start animation for all planets scaled smoothly by speed modifier."""
        if self.animation:
            return  # Already running

        for planet in self.planets.values():
            # Multiply total available frame limit so the frame lifecycle accounts for division updates
            total_frames = (len(planet['x']) - 1) * self.speed_modifier
            
            anim = animation.FuncAnimation(
                self.fig,
                self.update_point,
                frames=total_frames,
                fargs=(planet['x'], planet['y'], planet['z'], planet['artist']),
                interval=16,
                blit=False
            )
            self.animation.append(anim)

        self.draw()

    def stop_animation(self):
        """Fully stop animation and reset plot."""
        for anim in self.animation:
            anim.event_source.stop()

        self.animation.clear()
        self.ax.clear()
        
        # Recreate initial points and replot orbits
        self._recreate_planet_points()
        self.plot_orbits()
        self.draw()

    def soft_stop(self):
        """Pause animation without clearing the plot."""
        for anim in self.animation:
            anim.event_source.stop()

    def resume(self):
        """Resume paused animation."""
        for anim in self.animation:
            anim.event_source.start()

    def _recreate_planet_points(self):
        """Recreate initial planet markers after clearing axes."""
        raise NotImplementedError("Subclasses must implement this")


class PlotCanvas3DforInner(Base3DPlanetCanvas):
    """3D visualization of inner planets."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Normal speed (speed_modifier=1)
        super().__init__(parent, width, height, dpi, speed_modifier=1)
        
        self.time = np.arange(0, 3, 0.0025)  # Fine resolution for inner planets
        
        # Planet configurations: (semi_major_axis, eccentricity, inclination)
        self.planet_configs = {
            'Earth':    (1.000, 0.0167, 0.0000),
            'Mars':     (1.523, 0.0934, 0.0323),
            'Venus':    (0.723, 0.0068, 0.0592),
            'Mercury':  (0.387, 0.2056, 0.1222),
        }

        self._initialize_planets()
        self.plot_orbits()

    def _initialize_planets(self):
        """Create Planet3D objects and store coordinates + plot artists."""
        colors = {'Earth': 'blue', 'Mars': 'red', 'Venus': 'yellow', 'Mercury': 'grey'}
        
        for name, (a, e, inc) in self.planet_configs.items():
            planet_obj = Planet3D(1.0, self.time)
            x, y, z = planet_obj.coordinates(a, e, inc)
            
            artist, = self.ax.plot([x[0]], [y[0]], [z[0]], 'o', color=colors[name])
            
            self.planets[name] = {
                'x': x, 'y': y, 'z': z,
                'artist': artist,
                'color': colors[name]
            }

    def _recreate_planet_points(self):
        """Recreate planet markers after axis clear."""
        for name, data in self.planets.items():
            x0, y0, z0 = data['x'][0], data['y'][0], data['z'][0]
            artist, = self.ax.plot([x0], [y0], [z0], 'o', color=data['color'])
            data['artist'] = artist

    def plot_orbits(self):
        """Plot orbital paths for all inner planets."""
        orbit_funcs = {
            'Earth':    lambda d: self._calculate_orbit(d, 0.0167, 0.0),
            'Mars':     lambda d: self._calculate_orbit(d, 0.0934, 0.0323),
            'Venus':    lambda d: self._calculate_orbit(d, 0.0068, 0.0592),
            'Mercury':  lambda d: self._calculate_orbit(d, 0.2056, 0.1222),
        }

        for name, (a, _, _) in self.planet_configs.items():
            x, y, z = orbit_funcs[name](a)
            self.ax.plot(x, y, z, color=self.planets[name]['color'], label=name)

        self.ax.scatter(0, 0, 0, color='yellow', label='Sun', s=150)
        
        self._finalize_plot("Inner Planets Orbit Animation")

    def _calculate_orbit(self, Distance: float, ecc: float, inc: float):
        """Calculate 3D orbital path points."""
        theta = np.linspace(0, 2 * np.pi, 1000)
        r = distance(Distance=Distance, theta=theta, eccentricity=ecc)
        x = r * np.cos(theta) * np.cos(inc)
        y = r * np.sin(theta)
        z = r * np.cos(theta) * np.sin(inc)
        return x, y, z

    def _finalize_plot(self, title: str):
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_title(title)
        self.ax.legend()


class PlotCanvas3DforOuter(Base3DPlanetCanvas):
    """3D visualization of outer planets."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Override Speed for Outer Planets Only (Higher value = Slower)
        super().__init__(parent, width, height, dpi, speed_modifier=1)
        
        self.time = np.arange(0, 3000, 0.0025)  # Coarser resolution for outer planets
        
        # Planet configurations: (semi_major_axis, eccentricity, inclination)
        self.planet_configs = {
            'Jupiter': (5.20,  0.0488, 0.0229),
            'Saturn':  (9.58,  0.0555, 0.0435),
            'Uranus':  (19.29, 0.0472, 0.0134),
            'Neptune': (30.25, 0.0086, 0.0309),
            'Pluto':   (39.51, 0.2500, 0.3054),
        }

        self._initialize_planets()
        self.plot_orbits()

    def _initialize_planets(self):
        """Create Planet3D objects and store coordinates + plot artists."""
        colors = {
            'Jupiter': 'orange', 'Saturn': 'yellow', 'Uranus': 'cyan',
            'Neptune': 'blue', 'Pluto': 'brown'
        }
        
        for name, (a, e, inc) in self.planet_configs.items():
            planet_obj = Planet3D(1.0, self.time)
            x, y, z = planet_obj.coordinates(a, e, inc)
            
            artist, = self.ax.plot([x[0]], [y[0]], [z[0]], 'o', color=colors[name])
            
            self.planets[name] = {
                'x': x, 'y': y, 'z': z,
                'artist': artist,
                'color': colors[name]
            }

    def _recreate_planet_points(self):
        """Recreate planet markers after axis clear."""
        for name, data in self.planets.items():
            x0, y0, z0 = data['x'][0], data['y'][0], data['z'][0]
            artist, = self.ax.plot([x0], [y0], [z0], 'o', color=data['color'])
            data['artist'] = artist

    def plot_orbits(self):
        """Plot orbital paths for all outer planets."""
        for name, (a, e, inc) in self.planet_configs.items():
            x, y, z = self._calculate_orbit(a, e, inc)
            self.ax.plot(x, y, z, color=self.planets[name]['color'], label=name.lower())

        self.ax.scatter(0, 0, 0, color='yellow', label='Sun', s=150)
        
        self._finalize_plot("Outer Planets Orbit Animation")

    def _calculate_orbit(self, Distance: float, ecc: float, inc: float):
        """Calculate 3D orbital path points."""
        theta = np.linspace(0, 2 * np.pi, 1000)
        r = distance(Distance=Distance, theta=theta, eccentricity=ecc)
        x = r * np.cos(theta) * np.cos(inc)
        y = r * np.sin(theta)
        z = r * np.cos(theta) * np.sin(inc)
        return x, y, z

    def _finalize_plot(self, title: str):
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_title(title)
        self.ax.legend()