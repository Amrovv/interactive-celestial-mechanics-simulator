from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class KeplerPlotCanvas(FigureCanvasQTAgg):
    """A Qt5-compatible canvas for plotting Kepler's Third Law."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot_data()  

    def plot_data(self):
        # Planetary data: Semi-major axis (AU) and Orbital Period (Years)
        # Pairs are sorted by distance from the Sun to ensure the line plot connects smoothly
        planetary_data = [
            (0.387, 0.24),    # Mercury
            (0.723, 0.62),    # Venus
            (1.000, 1.00),    # Earth
            (1.523, 1.88),    # Mars
            (5.200, 11.86),   # Jupiter
            (9.580, 29.63),   # Saturn
            (19.290, 84.75),  # Uranus
            (30.250, 166.34), # Neptune
            (39.510, 248.35)  # Pluto
        ]
        
        # Unpack sorted data
        semi_major_axes = [data[0] for data in planetary_data]
        orbital_periods = [data[1] for data in planetary_data]
        
        # Apply Kepler's 3rd Law relationship: T^2 proportional to a^3 (or T = a^(3/2))
        transformed_axes = [axis ** (3/2) for axis in semi_major_axes]
       
        self.ax.clear()
        
        # Plotting the relationship
        self.ax.plot(
            transformed_axes, 
            orbital_periods, 
            color='red', 
            marker='D', 
            markerfacecolor='blue', 
            markeredgecolor='blue', 
            label="Linear (Kepler's Third Law)"
        )
        
        # Labels and Titles
        self.ax.set_xlabel('Orbital Semi-Major Axis (a^{3/2}) / AU')
        self.ax.set_ylabel('Orbital Period (T) / Yr')
        self.ax.set_title("Kepler's Third Law", color="white")
        self.ax.legend()
        
        # Styling: Theme customization (Dark mode container, white graph elements)
        self.fig.set_facecolor("#181E35")
        self.ax.set_facecolor("white")
        
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(axis='both', colors='white')
        
        # Batch-update all spines to white instead of writing 4 individual lines
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
            
        self.draw()