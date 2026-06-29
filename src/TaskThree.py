import numpy as np
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PlanetClasses import Planet


class BaseAnimatedOrbitCanvas(FigureCanvasQTAgg):
    """Base canvas for handling vectorized planetary orbit animations in Qt5."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        # Style configurations
        self.ax.set_facecolor("#181E35")
        self.fig.set_facecolor("#181E35")
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.animation = None
        self.time = self._get_time_array()
        self.planets_config = self._get_planets_config()
        
        # Stores computed animation trace arrays and Matplotlib scatter plot objects
        self.planet_data = {}
        self.scatter_plots = {}
        
        self._initialize_coordinates()
        self.plot_static_orbits()
        self._initialize_animation_points()

    def _get_time_array(self):
        raise NotImplementedError

    def _get_planets_config(self):
        raise NotImplementedError

    def _initialize_coordinates(self):
        """Pre-computes coordinate histories using the custom Planet instances."""
        for config in self.planets_config:
            name = config["name"]
            # Instantiate the Planet class using its orbital period profile
            planet_inst = Planet(config["period"], self.time)
            x_coords, y_coords = planet_inst.coordinates(config["axis"], config["eccentricity"])
            
            self.planet_data[name] = {
                "x": x_coords,
                "y": y_coords,
                "color": config["color"]
            }

    def plot_static_orbits(self):
        """Draws the static orbital trajectories using pre-calculated arrays."""
        self.ax.clear()
        
        for name, data in self.planet_data.items():
            # Uses the complete array trajectory to map out the permanent orbit paths
            self.ax.plot(data["x"], data["y"], linestyle='-', color=data["color"], label=name)
            
        self.ax.scatter(0, 0, color="yellow", label="Sun", zorder=3)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X / AU')
        self.ax.set_ylabel('Y / AU')
        
        # Match Dark Theme Aesthetics
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.legend()

    def _initialize_animation_points(self):
        """Creates the initial scatter plot placeholders for the moving planets."""
        for name, data in self.planet_data.items():
            # Instantiate scatter objects ONCE. We will manipulate their offsets later.
            self.scatter_plots[name] = self.ax.scatter(
                [data["x"][0]], [data["y"][0]], color=data["color"], zorder=4
            )

    def _animate_frame(self, frame_idx):
        """Updates the positions of all scatter representations dynamically."""
        updated_elements = []
        for name, scatter in self.scatter_plots.items():
            x = self.planet_data[name]["x"][frame_idx]
            y = self.planet_data[name]["y"][frame_idx]
            
            # Efficiently updates positions without teardown/reconstruction cycles
            scatter.set_offsets(np.c_[x, y])
            updated_elements.append(scatter)
            
        return tuple(updated_elements)

    # --- Animation Control Pipeline ---
    
    def start_animation(self):
        if self.animation is None:
            # Dynamically pull frame constraints based on the length of data
            total_frames = len(next(iter(self.planet_data.values()))["x"]) - 1
            self.animation = animation.FuncAnimation(
                self.fig, self._animate_frame, frames=total_frames, 
                interval=50, repeat=True, blit=True
            )
        self.draw()

    def stop_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()
            self.animation = None
            self.reset_to_default()

    def resume(self):
        if self.animation is not None:
            self.animation.event_source.start()

    def soft_stop(self):
        if self.animation is not None:
            self.animation.event_source.stop()

    def reset_to_default(self):
        self.plot_static_orbits()
        self._initialize_animation_points()
        self.draw()

    def reset(self):
        self.reset_to_default()


class PlotCanvasforTask3_Inner(BaseAnimatedOrbitCanvas):
    """Canvas handling animations for the Inner Planets."""
    
    def _get_time_array(self):
        return np.arange(0, 3, 0.0025)

    def _get_planets_config(self):
        return [
            {"name": "Mercury", "period": 0.24, "axis": 0.387, "eccentricity": 0.2056, "color": "grey"},
            {"name": "Venus", "period": 0.62, "axis": 0.723, "eccentricity": 0.0068, "color": "yellow"},
            {"name": "Earth", "period": 1.00, "axis": 1.000, "eccentricity": 0.0167, "color": "blue"},
            {"name": "Mars", "period": 1.88, "axis": 1.523, "eccentricity": 0.0934, "color": "red"}
        ]

    def plot_static_orbits(self):
        super().plot_static_orbits()
        self.ax.set_title("Inner Planets Orbit", color="white")


class PlotCanvasforTask3_Outer(BaseAnimatedOrbitCanvas):
    """Canvas handling animations for the Outer Planets."""
    
    def _get_time_array(self):
        return np.arange(0, 3000, 0.25)

    def _get_planets_config(self):
        return [
            {"name": "Jupiter", "period": 11.86, "axis": 5.20, "eccentricity": 0.048775, "color": "orange"},
            {"name": "Saturn", "period": 29.63, "axis": 9.58, "eccentricity": 0.0555, "color": "yellow"},
            {"name": "Uranus", "period": 84.75, "axis": 19.29, "eccentricity": 0.0472, "color": "cyan"},
            {"name": "Neptune", "period": 166.34, "axis": 30.25, "eccentricity": 0.0086, "color": "blue"},
            {"name": "Pluto", "period": 248.35, "axis": 39.51, "eccentricity": 0.25, "color": "brown"}
        ]

    def plot_static_orbits(self):
        super().plot_static_orbits()
        self.ax.set_title("Outer Planets Orbit", color="white")