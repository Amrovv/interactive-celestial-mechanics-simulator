import numpy as np
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PlanetClasses import Planet3D
from distance import distance
from planets import PLANETS, INNER, OUTER


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
        self.planets = {}          # name -> dict of coords and artist
        self.configs = {}          # name -> (au, ecc, inclination in radians)
        self.title = ""
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

    def _build_planets(self, names, time):
        """Create Planet3D objects for the given planets and draw their start markers."""
        self.time = time
        self.configs = {
            name: (PLANETS[name]['au'], PLANETS[name]['ecc'], np.deg2rad(PLANETS[name]['inc']))
            for name in names
        }
        for name in names:
            a, e, inc = self.configs[name]
            # Use the planet's real period so they orbit at different rates
            x, y, z = Planet3D(PLANETS[name]['period'], time).coordinates(a, e, inc)
            artist, = self.ax.plot([x[0]], [y[0]], [z[0]], 'o', color=PLANETS[name]['color'])
            self.planets[name] = {
                'x': x, 'y': y, 'z': z,
                'artist': artist,
                'color': PLANETS[name]['color'],
            }

    def _recreate_planet_points(self):
        """Recreate planet markers after the axes are cleared."""
        for data in self.planets.values():
            artist, = self.ax.plot([data['x'][0]], [data['y'][0]], [data['z'][0]], 'o', color=data['color'])
            data['artist'] = artist

    def plot_orbits(self):
        """Draw the full orbital paths and the Sun."""
        for name, (a, e, inc) in self.configs.items():
            x, y, z = self._calculate_orbit(a, e, inc)
            self.ax.plot(x, y, z, color=self.planets[name]['color'], label=name.capitalize())

        self.ax.scatter(0, 0, 0, color='yellow', label='Sun', s=150)
        self._finalize_plot(self.title)

    def _calculate_orbit(self, Distance, ecc, inc):
        """Calculate one full 3D orbital path."""
        theta = np.linspace(0, 2 * np.pi, 1000)
        r = distance(Distance=Distance, theta=theta, eccentricity=ecc)
        x = r * np.cos(theta) * np.cos(inc)
        y = r * np.sin(theta)
        z = r * np.cos(theta) * np.sin(inc)
        return x, y, z

    def _finalize_plot(self, title):
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        self.ax.set_title(title)
        self.ax.legend()

    def update_point(self, frame, x, y, z, point):
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
            # Multiply total frame limit so the frame lifecycle accounts for division updates
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


class PlotCanvas3DforInner(Base3DPlanetCanvas):
    """3D visualization of inner planets."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi, speed_modifier=1)
        self.title = "Inner Planets Orbit Animation"
        self._build_planets(INNER, np.arange(0, 3, 0.0025))  # Fine resolution for inner planets
        self.plot_orbits()


class PlotCanvas3DforOuter(Base3DPlanetCanvas):
    """3D visualization of outer planets."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(parent, width, height, dpi, speed_modifier=1)
        self.title = "Outer Planets Orbit Animation"
        # Fewer points; outer orbits are slow so this is plenty
        self._build_planets(OUTER, np.arange(0, 500, 0.25))
        self.plot_orbits()
