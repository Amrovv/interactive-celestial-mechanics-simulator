from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtGui import QIcon
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Celestial Simulator: orbit calculations and plotting support.
# This file provides an interactive PyQt5 interface for visualizing
# planetary orbits, orbit comparisons, animations, and central-body plots.

# Orbital constants and helper functions for repeated orbit calculations
PLANET_SEMI_MAJOR_AXIS_AU = {
    "mercury": 0.387,
    "venus": 0.723,
    "earth": 1.000,
    "mars": 1.523,
    "jupiter": 5.20,
    "saturn": 9.58,
    "uranus": 19.29,
    "neptune": 30.25,
    "pluto": 39.51,
}

ORBITAL_ECCENTRICITIES = {
    "mercury": 0.2056,
    "venus": 0.0068,
    "earth": 0.0167,
    "mars": 0.0934,
    "jupiter": 0.048775,
    "saturn": 0.0555,
    "uranus": 0.0472,
    "neptune": 0.0086,
    "pluto": 0.25,
}

ORBITAL_PERIODS = {
    "mercury": 0.24,
    "venus": 0.62,
    "earth": 1.00,
    "mars": 1.88,
    "jupiter": 11.86,
    "saturn": 29.63,
    "uranus": 84.75,
    "neptune": 166.34,
    "pluto": 248.35,
}


# Orbit coordinate generators for 2D and 3D presentations.
# These routines convert orbital parameters into plot-ready coordinates.
def orbital_coordinates_2d(distance, eccentricity, points=1000):
    theta = np.radians(np.arange(points))
    radius = orbital_radius(distance, theta, eccentricity)
    return radius * np.cos(theta), radius * np.sin(theta)


def orbital_coordinates_3d(distance, eccentricity, inclination_deg, points=1000):
    theta = np.radians(np.arange(points))
    radius = orbital_radius(distance, theta, eccentricity)
    inclination = np.deg2rad(inclination_deg)
    x = radius * np.cos(theta) * np.cos(inclination)
    y = radius * np.sin(theta)
    z = radius * np.cos(theta) * np.sin(inclination)
    return x, y, z


def orbital_radius(distance, theta, eccentricity, plus=False):
    """Return the orbital radius for a conic section."""
    sign = 1 if plus else -1
    return (distance * (1 - eccentricity**2)) / (1 + sign * eccentricity * np.cos(theta))


def orbital_radius_plus(distance, theta, eccentricity):
    """Return the orbital radius for orbits using the alternate sign convention."""
    return orbital_radius(distance, theta, eccentricity, plus=True)

# Compatibility aliases for legacy code paths in the plot classes.
# These aliases allow older plot code to keep the same function signatures.
distance = orbital_radius

def distance_plus(distance, theta, eccentricity):
    return orbital_radius_plus(distance, theta, eccentricity)


# Base 3D planet model used by the plotting classes.
# Stores orbital period and time values for coordinate generation.
class Planet3D():
    def __init__(self, period, time):
        self.period = period
        self.time = time

   

    def coordinates(self, Distance, eccentricity, inclination):
        theta = 2 * np.pi * np.asarray(self.time) / self.period
        radius = orbital_radius(Distance, theta, eccentricity)
        x_coordinate = radius * np.cos(theta) * np.cos(inclination)
        y_coordinate = radius * np.sin(theta)
        z_coordinate = radius * np.cos(theta) * np.sin(inclination)
        return x_coordinate, y_coordinate, z_coordinate


class Earth3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)

 
class Mars3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)


class Venus3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)


class Mercury3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)

class Jupiter3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)


class Saturn3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)
    

class Neptune3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)
    

class Uranus3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)
    
    
class Pluto3D(Planet3D):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity, inclination):
        return super().coordinates(Distance, eccentricity, inclination)

   




class Planet():
    def __init__(self, period, time):
        self.period = period
        self.time = time

   

    def coordinates(self, Distance, eccentricity):
        theta = 2 * np.pi * np.asarray(self.time) / self.period
        radius = orbital_radius(Distance, theta, eccentricity)
        x_coordinate = radius * np.cos(theta)
        y_coordinate = radius * np.sin(theta)
        return x_coordinate, y_coordinate
        

class Earth(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)

 
class Mars(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)


class Venus(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)


class Mercury(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)

   
class Jupiter(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)


class Saturn(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)
    

class Neptune(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)

class Uranus(Planet):
    def __init__(self, period, time):
        self.period = period
        self.time = time
     
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)
     
class Pluto(Uranus):
    def __init__(self, period, time):
        self.period = period
        self.time = time
        
    def coordinates(self, Distance, eccentricity):
        return super().coordinates(Distance, eccentricity)
        
class KeplersThirdLawCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(KeplersThirdLawCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_data()  

    def plot_data(self):
        # Sample data for the plot
       
     
        AU = [9.58, 19.29, 5.20, 30.25, 39.51, 1.523, 0.723, 0.387, 1.000]
        Orbital_period = [29.63, 84.75, 11.86, 166.34, 248.35, 1.88, 0.62, 0.24, 1.00]
        for i in range(len(AU)):
             AU[i] = AU[i]**(3/2)
       
        self.ax.clear()  # Clear previous plot data
        self.ax.plot(AU, Orbital_period, color = 'red', marker = 'D', markerfacecolor = 'blue', mec = 'blue', label = "Linear ( Kepler's Third Law)")
        self.ax.set_xlabel('Orbital Semi-Major Axis / AU')
        self.ax.set_ylabel('Orbital Period / Yr')
        self.ax.legend()
        self.ax.set_title("Kepler's Third Law", color="white")
        self.ax.spines['left'].set_edgecolor('white')    # Left spine
        self.ax.spines['right'].set_edgecolor('white')  # Right spine
        self.ax.spines['bottom'].set_edgecolor('white')  # Bottom spine
        self.ax.spines['top'].set_edgecolor('white')  # Top spine
        self.ax.xaxis.label.set_color('white')   # Change to your desired color
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(axis='x', colors='white')  # Change color for x-axis tick labels
        self.ax.tick_params(axis='y', colors='white')
        self.ax.set_facecolor("white")
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.draw()

class InnerOrbitCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(InnerOrbitCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_data()  

    def plot_data(self):
        self.ax.clear()
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['earth'], ORBITAL_ECCENTRICITIES['earth']), color='blue', label='Earth')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['mars'], ORBITAL_ECCENTRICITIES['mars']), color='red', label='Mars')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['venus'], ORBITAL_ECCENTRICITIES['venus']), color='yellow', label='Venus')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['mercury'], ORBITAL_ECCENTRICITIES['mercury']), color='grey', label='Mercury')
        self.ax.scatter(0, 0, color='yellow', label='Sun')
        self.ax.set_xlabel(' X / AU')
        self.ax.set_ylabel(' Y / Yr')
        self.ax.legend()
        self.ax.set_aspect('equal')
        self.ax.set_title('Inner Planets Orbit')
        self.draw()
      
class OuterOrbitCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(OuterOrbitCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_data()
        
    def plot_data(self):
        self.ax.clear()
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['jupiter'], ORBITAL_ECCENTRICITIES['jupiter']), linestyle='-', color='orange', label='Jupiter')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['saturn'], ORBITAL_ECCENTRICITIES['saturn']), linestyle='-', color='red', label='Saturn')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['neptune'], ORBITAL_ECCENTRICITIES['neptune']), linestyle='-', color='blue', label='Neptune')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['pluto'], ORBITAL_ECCENTRICITIES['pluto']), linestyle='-', color='brown', label='Pluto')
        self.ax.plot(*orbital_coordinates_2d(PLANET_SEMI_MAJOR_AXIS_AU['uranus'], ORBITAL_ECCENTRICITIES['uranus']), linestyle='-', color='cyan', label='Uranus')
        self.ax.scatter(0, 0, color='yellow', label='Sun')
        self.ax.set_xlabel(' X / AU')
        self.ax.set_ylabel(' Y / AU')
        self.ax.legend()
        self.ax.set_aspect('equal')
        self.ax.set_title('Outer Planets Orbit')
        self.draw()
class InnerOrbitAnimationCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(InnerOrbitAnimationCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.animation = None 
        self.time = np.arange(0, 3, 0.0025)
        
        Earth_co = Earth(1, self.time)
        self.Earth_x = Earth_co.coordinates(1 , 0.0167)[0]
        self.Earth_y = Earth_co.coordinates(1 , 0.0167)[1]
        
        
        Mars_co = Mars(1.88, self.time)
        self.Mars_x = Mars_co.coordinates(1.523, 0.0934)[0]
        self.Mars_y = Mars_co.coordinates(1.523, 0.0934)[1]
        
       
    
        Venus_co = Venus(0.62, self.time)
        self.Venus_x = Venus_co.coordinates(0.723, 0.0068)[0]
        self.Venus_y = Venus_co.coordinates(0.723, 0.0068)[1]
       
        
        
        Mercury_co = Mercury(0.24, self.time)
        self.Mercury_x = Mercury_co.coordinates(0.387, 0.2056)[0]
        self.Mercury_y = Mercury_co.coordinates(0.387, 0.2056)[1]
       
        self.animate_planets(0)
        
              
        self.plot_data()
    
    
    def animate_planets(self, i):
        if hasattr(self, 'earth1'):
            self.earth1.remove()
        
        self.earth1 = self.ax.scatter(self.Earth_x[i], self.Earth_y[i], color='blue')
         
        if hasattr(self, 'mars1'):
            self.mars1.remove()
        self.mars1 = self.ax.scatter(self.Mars_x[i], self.Mars_y[i], color='red')

        if hasattr(self, 'venus1'):
            self.venus1.remove()
        self.venus1 = self.ax.scatter(self.Venus_x[i], self.Venus_y[i], color='yellow')

        if hasattr(self, 'mercury1'):
            self.mercury1.remove()
        self.mercury1 = self.ax.scatter(self.Mercury_x[i], self.Mercury_y[i], color='grey')
        
        return self.earth1, self.mars1, self.venus1, self.mercury1
    
    
    def start_animation(self):
            
            if self.animation is None:  # If animation is not already running, start it
                self.animation = animation.FuncAnimation(self.fig, self.animate_planets, repeat=True,
                                                      frames=len(self.Mars_x) - 1, interval = 16)
            self.draw()
        
    def stop_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()  # Stop the animation
            self.animation = None  # Reset the animation object
            self.ax.clear()
            self.animate_planets(0)  # Reset animation to initial state
            self.plot_data()
            self.draw()


    def resume(self):
        if self.animation is not None:
            self.animation.event_source.start()

    def soft_stop(self):
        if self.animation is not None:
            self.animation.event_source.stop()

    def reset(self):
        self.ax.clear()
        self.animate_planets(0)  # Reset animation to initial state
        self.plot_data()
        
        
        
    def plot_data(self):
        
        def mars(Distance):
            mars_x = []
            mars_y = []
            for theta in np.radians(range(0, 1000)):
            
                x =  distance(Distance, theta, 0.0934) * np.cos(theta)
                mars_x.append(x)
            
                y = distance(Distance, theta, 0.0934) * np.sin(theta)
                mars_y.append(y)
            
            return mars_x, mars_y
        
        def earth(Distance):
            earth_x = []
            earth_y = []
            for theta in np.radians(range(0, 1000)):
            
                x =  distance(Distance, theta, 0.0167) * np.cos(theta)
                earth_x.append(x)
            
                y = distance(Distance, theta, 0.0167) * np.sin(theta)
                earth_y.append(y)
            
            return earth_x, earth_y
    
        def mercury(Distance):
            mercury_x = []
            mercury_y = []
            for theta in np.radians(range(0, 1000)):
            
                x =  distance(Distance, theta, 0.2056) * np.cos(theta)
                mercury_x.append(x)
            
                y = distance(Distance, theta, 0.2056) * np.sin(theta)
                mercury_y.append(y)
            
            return mercury_x, mercury_y
    
        def venus(Distance):
            venus_x = []
            venus_y = []
            for theta in np.radians(range(0, 1000)):
            
                x =  distance(Distance, theta, 0.0068) * np.cos(theta)
                venus_x.append(x)
            
                y = distance(Distance, theta, 0.0068) * np.sin(theta)
                venus_y.append(y)
            
            return venus_x, venus_y
   
        self.ax.plot(earth(1)[0], earth(1)[1], color = "blue", label = "Earth")
        self.ax.plot(mars(1.523)[0], mars(1.523)[1], color = "red", label = "Mars")
        self.ax.plot(venus(0.723)[0], venus(0.723)[1], color = "yellow", label = "Venus")
        self.ax.plot(mercury(0.387)[0], mercury(0.387)[1], color = "grey", label = "Mercury")
    
        self.ax.scatter(0, 0, color = "yellow", label = "Sun")
        
        
        self.ax.set_aspect('equal')
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.set_xlabel(' X / AU')
        self.ax.set_ylabel(' Y / AU')
        self.ax.legend()
        
     
       
        
        self.ax.set_title("Inner Planets Orbit")
        
        self.ax.legend()
   
class OuterOrbitAnimationCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(OuterOrbitAnimationCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.animation = None 

        self.time = np.arange(0, 3000, 0.25)
    
        Jupiter_co = Jupiter(11.86, self.time)
        self.Jupiter_x = Jupiter_co.coordinates(5.20 , 0.048775)[0]
        self.Jupiter_y = Jupiter_co.coordinates(5.20 , 0.048775)[1]
        
        
        
        Saturn_co = Saturn(29.63, self.time)
        self.Saturn_x = Saturn_co.coordinates(9.58, 0.0555)[0]
        self.Saturn_y = Saturn_co.coordinates(9.58, 0.0555)[1]
    
        
        Neptune_co = Neptune(166.34, self.time)
        self.Neptune_x = Neptune_co.coordinates(30.25, 0.0086)[0]
        self.Neptune_y = Neptune_co.coordinates(30.25, 0.0086)[1]
        
        
        Uranus_co = Uranus(84.75, self.time)
        self.Uranus_x = Uranus_co.coordinates(19.29, 0.0472)[0]
        self.Uranus_y = Uranus_co.coordinates(19.29, 0.0472)[1]
      
        
        
        Pluto_co = Pluto(248.35, self.time)
        self.Pluto_x = Pluto_co.coordinates(39.51, 0.25)[0]
        self.Pluto_y = Pluto_co.coordinates(39.51, 0.25)[1]

        self.animate_planets(0)
        
              
        self.plot_data()


    def animate_planets(self, i):
            if hasattr(self, 'saturn1'):
                self.saturn1.remove()
            self.saturn1 = self.ax.scatter(self.Saturn_x[i], self.Saturn_y[i], color='yellow')
            
            if hasattr(self, 'jupiter1'):
                self.jupiter1.remove()
            self.jupiter1 = self.ax.scatter(self.Jupiter_x[i], self.Jupiter_y[i], color='orange')

            if hasattr(self, 'uranus1'):
                self.uranus1.remove()
            self.uranus1 = self.ax.scatter(self.Uranus_x[i], self.Uranus_y[i], color='cyan')

            if hasattr(self, 'neptune1'):
                self.neptune1.remove()
            self.neptune1 = self.ax.scatter(self.Neptune_x[i], self.Neptune_y[i], color='blue')

            if hasattr(self, 'pluto1'):
                self.pluto1.remove()
            self.pluto1 = self.ax.scatter(self.Pluto_x[i], self.Pluto_y[i], color='brown')

            
            
            return self.saturn1, self.jupiter1, self.uranus1, self.neptune1, self.pluto1
    
    
    def start_animation(self):
            if self.animation is None:  # If animation is not already running, start it
                self.animation = animation.FuncAnimation(self.fig, self.animate_planets, repeat=True,
                                                      frames=len(self.Pluto_x) - 1, interval = 16)
            self.draw()
        
    def stop_animation(self):
            if self.animation is not None:
                self.animation.event_source.stop()  # Stop the animation
                self.animation = None  # Reset the animation object
            self.ax.clear()
            self.animate_planets(0)  # Reset animation to initial state
            self.plot_data()
            self.draw()

    def resume(self):
        if self.animation is not None:
            self.animation.event_source.start()

    def soft_stop(self):
        if self.animation is not None:
            self.animation.event_source.stop()


    
    

    def plot_data(self):
        
            def jupiter(Distance):
                jupiter_x = []
                jupiter_y = []
                for theta in np.radians(range(0, 1000)):
                
                    x =  distance(Distance, theta, 0.048775) * np.cos(theta)
                    jupiter_x.append(x)
                
                    y = distance(Distance, theta, 0.048775) * np.sin(theta)
                    jupiter_y.append(y)
                
                return jupiter_x, jupiter_y
            

            def saturn(Distance):
                saturn_x = []
                saturn_y = []
                for theta in np.radians(range(0, 1000)):
                
                    x =  distance(Distance, theta, 0.0555) * np.cos(theta)
                    saturn_x.append(x)
                
                    y = distance(Distance, theta, 0.0555) * np.sin(theta)
                    saturn_y.append(y)
                
                return saturn_x, saturn_y
        
        
    
            def uranus(Distance):
                uranus_x = []
                uranus_y = []
                for theta in np.radians(range(0, 1000)):
                
                    x =  distance(Distance, theta, 0.0472) * np.cos(theta)
                    uranus_x.append(x)
                
                    y =  distance(Distance, theta, 0.0472) * np.sin(theta)
                    uranus_y.append(y)
            
                return uranus_x, uranus_y
        
            def neptune(Distance):
                neptune_x = []
                neptune_y = []
                for theta in np.radians(range(0, 1000)):
                    x =  distance(Distance, theta, 0.0086) * np.cos(theta)
                    neptune_x.append(x)
                
                    y =  distance(Distance, theta, 0.0086) * np.sin(theta)
                    neptune_y.append(y)
        
                return neptune_x, neptune_y
        
            def pluto(Distance):
                pluto_x = []
                pluto_y = []
                for theta in np.radians(range(0, 1000)):
                
                    x =  distance(Distance, theta, 0.25) * np.cos(theta)
                    pluto_x.append(x)
                
                    y =  distance(Distance, theta, 0.25) * np.sin(theta)
                    pluto_y.append(y)
            
                return pluto_x, pluto_y
    
    
            
            self.ax.plot(jupiter(5.20)[0], jupiter(5.20)[1], linestyle = '-', color = 'orange', label = 'jupiter')
            self.ax.plot(saturn(9.58)[0], saturn(9.58)[1],  linestyle = '-', color = 'yellow', label ="saturn")
            self.ax.plot(neptune(30.25)[0], neptune(30.25)[1], linestyle = '-', color = 'blue', label ="netpune")
            self.ax.plot(uranus(19.29)[0], uranus(19.29)[1],   linestyle = '-', color = 'cyan', label = "uranus")
            self.ax.plot(pluto(39.51)[0], pluto(39.51)[1],  linestyle = '-',  color = 'brown', label ="pluto")
        
            self.ax.scatter(0, 0, color = "yellow", label = "Sun")
            
            
            self.ax.set_aspect('equal')

            self.ax.set_xlabel(' X / AU')
            self.ax.set_ylabel(' Y / AU')
            self.ax.legend()
            self.ax.set_facecolor((0, 0, 0, 0)) 
            self.fig.set_facecolor((0, 0, 0, 0)) 
        
        
            
            self.ax.set_title("Outer Planets Orbit")
            
            self.ax.legend()
        

class Inner3DOrbitCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.grid(color='black')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.animation = []
        self.set_dark_background()
        super(Inner3DOrbitCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        
        
        self.time = np.arange(0, 3, 0.0025)
    
        Earth_co = Earth3D(1, self.time)
        self.Earth_x = Earth_co.coordinates(1 , 0.0167, 0)[0]
        self.Earth_y = Earth_co.coordinates(1 , 0.0167, 0)[1]
        self.Earth_z = Earth_co.coordinates(1 , 0.0167, 0)[2]
        self.earth1, = self.ax.plot([self.Earth_x[0]], [self.Earth_y[0]], [self.Earth_z[0]], 'o', color = 'blue')
        
        Mars_co = Mars3D(1.88, self.time)
        self.Mars_x = Mars_co.coordinates(1.523, 0.0934, 0.03228859)[0]
        self.Mars_y = Mars_co.coordinates(1.523, 0.0934, 0.03228859)[1]
        self.Mars_z = Mars_co.coordinates(1.523, 0.0934, 0.03228859)[2]
        self.mars1, = self.ax.plot([self.Mars_x[0]], [self.Mars_y[0]], [self.Mars_z[0]], 'o', color = 'red')
    
        
        Venus_co = Venus3D(0.62, self.time)
        self.Venus_x = Venus_co.coordinates(0.723, 0.0068, 0.05916666)[0]
        self.Venus_y = Venus_co.coordinates(0.723, 0.0068, 0.05916666)[1]
        self.Venus_z = Venus_co.coordinates(0.723, 0.0068, 0.05916666)[2]
        self.venus1, = self.ax.plot([self.Venus_x[0]], [self.Venus_y[0]], [self.Venus_z[0]], 'o', color = 'yellow')
        
        
        Mercury_co = Mercury3D(0.24, self.time)
        self.Mercury_x = Mercury_co.coordinates(0.387, 0.2056, 0.122173)[0]
        self.Mercury_y = Mercury_co.coordinates(0.387, 0.2056, 0.122173)[1]
        self.Mercury_z = Mercury_co.coordinates(0.387, 0.2056, 0.122173)[2]
        self.mercury1, = self.ax.plot([self.Mercury_x[0]], [self.Mercury_y[0]],[self.Mercury_z[0]], 'o', color = 'grey')
    
            
        self.plot_data()
  
    def update_points(self,n, x, y, z, point):
        
         point.set_data([x[n]], [y[n]])
        
         point.set_3d_properties(z[n], 'z')
        
         return point
    
    def start_animation3D(self):
        if not self.animation:  # If animation is not already running, start it
            
            animate_earth = animation.FuncAnimation(self.fig, self.update_points, len(self.Mars_x) -1, fargs = (self.Earth_x, self.Earth_y, self.Earth_z, self.earth1), interval = 16)
        
            animate_mars = animation.FuncAnimation(self.fig, self.update_points, len(self.Mars_x) - 1, fargs = (self.Mars_x, self.Mars_y, self.Mars_z, self.mars1), interval = 16)
                                    
            animate_venus = animation.FuncAnimation(self.fig, self.update_points, len(self.Mars_x) -1, fargs = (self.Venus_x, self.Venus_y, self.Venus_z, self.venus1), interval = 16)
        
            animate_mercury = animation.FuncAnimation(self.fig, self.update_points, len(self.Mars_x) - 1, fargs = (self.Mercury_x, self.Mercury_y, self.Mercury_z, self.mercury1), interval = 16)
            
    
            self.animation.append(animate_earth)
            self.animation.append(animate_mars)
            self.animation.append(animate_venus)
            self.animation.append(animate_mercury)
        
        self.draw()
                      
    def stop_animation3D(self):
         for animate in self.animation:
            animate.event_source.stop()  # Stop the animation
        

         self.animation = []  # Reset the animation list
         self.ax.clear()
         
         

         self.earth1, = self.ax.plot([self.Earth_x[0]], [self.Earth_y[0]], [self.Earth_z[0]], 'o', color = 'blue')
         self.mars1, = self.ax.plot([self.Mars_x[0]], [self.Mars_y[0]], [self.Mars_z[0]], 'o', color = 'red')
         self.venus1, = self.ax.plot([self.Venus_x[0]], [self.Venus_y[0]], [self.Venus_z[0]], 'o', color = 'yellow')
         self.mercury1, = self.ax.plot([self.Mercury_x[0]], [self.Mercury_y[0]],[self.Mercury_z[0]], 'o', color = 'grey')
            
        
            
            # Plot data again
         self.plot_data()
            
            # Draw the canvas
         self.draw()   

    def resume(self):
        for animate in self.animation:
            animate.event_source.start()        

    def soft_stop(self):
        for animate in self.animation:
            animate.event_source.stop()                                  
    
    def set_dark_background(self):
        self.ax.set_facecolor('#181E35')
 
        self.ax.xaxis._axinfo["grid"]["color"] = "black"
        self.ax.yaxis._axinfo["grid"]["color"] = "black"
        self.ax.zaxis._axinfo["grid"]["color"] = "black"

        # Set axis colors
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.xaxis.set_pane_color((1, 1, 1, 1))  # Set X-axis pane color to white
        self.ax.yaxis.set_pane_color((1, 1, 1, 1))  # Set Y-axis pane color to white
        self.ax.zaxis.set_pane_color((1, 1, 1, 1))  # Set Z-axis pane color to white
      
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
    
        self.ax.title.set_color('white')
        
    def plot_data(self):
        
        def mars(Distance):
            mars_x = []
            mars_y = []
            mars_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.0934) * np.cos(theta)) * np.cos(0.03228859)
                mars_x.append(x)
            
                y = distance(Distance, theta, 0.0934) * np.sin(theta)
                mars_y.append(y)
                
                z = (distance(Distance, theta, 0.0934) * np.cos(theta)) * np.sin(0.03228859)
                mars_z.append(z)
            
            return mars_x, mars_y, mars_z
       
        def earth(Distance):
            earth_x = []
            earth_y = []
            earth_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.0167) * np.cos(theta)) * np.cos(0)
                earth_x.append(x)
            
                y = distance(Distance, theta, 0.0167) * np.sin(theta)
                earth_y.append(y)
            
                z = (distance(Distance, theta, 0.0167) * np.cos(theta)) * np.sin(0)
                earth_z.append(z)
            
            return earth_x, earth_y, earth_z
    
        def mercury(Distance):
            mercury_x = []
            mercury_y = []
            mercury_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.2056) * np.cos(theta)) * np.cos(0.122173)
                mercury_x.append(x)
            
                y = distance(Distance, theta, 0.2056) * np.sin(theta)
                mercury_y.append(y)
                
                z = (distance(Distance, theta, 0.2056) * np.cos(theta)) * np.sin(0.122173)
                mercury_z.append(z)
                   
            return mercury_x, mercury_y, mercury_z
    
        def venus(Distance):
            venus_x = []
            venus_y = []
            venus_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.0068) * np.cos(theta)) * np.cos(0.05916666)
                venus_x.append(x)
            
                y = distance(Distance, theta, 0.0068) * np.sin(theta)
                venus_y.append(y)
                
                z = (distance(Distance, theta, 0.0068) * np.cos(theta)) * np.sin(0.05916666)
                venus_z.append(z)
            
            return venus_x, venus_y, venus_z
    
        
        
        self.ax.plot(earth(1)[0], earth(1)[1], earth(1)[2],color = "blue", label = "Earth")
        self.ax.plot(mars(1.523)[0], mars(1.523)[1], mars(1.523)[2], color = "red", label = "Mars")
        self.ax.plot(venus(0.723)[0], venus(0.723)[1], venus(0.723)[2], color = "yellow", label = "Venus")
        self.ax.plot(mercury(0.387)[0], mercury(0.387)[1], mercury(0.387)[2], color = "grey", label = "Mercury")  
        self.ax.scatter(0, 0, 0,  color = "yellow", label = "Sun", s = 150)   
       
        self.ax.set_aspect('equal')

        self.ax.set_xlabel(' X / AU')
        self.ax.set_ylabel(' Y / AU')
        self.ax.legend()
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.set_title("Inner Planets Orbit Animation")
        self.ax.legend()
            
  
class Outer3DOrbitCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.grid(color='black')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.animation = []
        self.set_dark_background()
        super(Outer3DOrbitCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        
        self.ax.grid(color='black')
        
        self.time = np.arange(0, 3000, 0.25)
    
        Jupiter_co = Jupiter3D(11.86, self.time)
        self.Jupiter_x = Jupiter_co.coordinates(5.20 , 0.048775, 0.02286381)[0]
        self.Jupiter_y = Jupiter_co.coordinates(5.20 , 0.048775, 0.02286381)[1]
        self.Jupiter_z = Jupiter_co.coordinates(5.20 , 0.048775, 0.02286381)[2]
        self.jupiter1, = self.ax.plot([self.Jupiter_x[0]], [self.Jupiter_y[0]], [self.Jupiter_z[0]], 'o', color = 'orange')
        
        
        
        Saturn_co = Saturn3D(29.63, self.time)
        self.Saturn_x = Saturn_co.coordinates(9.58, 0.0555, 0.0434587)[0]
        self.Saturn_y = Saturn_co.coordinates(9.58, 0.0555, 0.0434587)[1]
        self.Saturn_z = Saturn_co.coordinates(9.58, 0.0555, 0.0434587)[2]
        self.saturn1, = self.ax.plot([self.Saturn_x[0]], [self.Saturn_y[0]], [self.Saturn_z[0]], 'o', color = 'yellow')
    
        
        Neptune_co = Neptune3D(166.34, self.time)
        self.Neptune_x = Neptune_co.coordinates(30.25, 0.0086, 0.03089233)[0]
        self.Neptune_y = Neptune_co.coordinates(30.25, 0.0086, 0.03089233)[1]
        self.Neptune_z = Neptune_co.coordinates(30.25, 0.0086, 0.03089233)[2]
        self.neptune1, = self.ax.plot([self.Neptune_x[0]], [self.Neptune_y[0]], [self.Neptune_z[0]], 'o', color = 'blue')
        
        
        Uranus_co = Uranus3D(84.75, self.time)
        self.Uranus_x = Uranus_co.coordinates(19.29, 0.0472, 0.01343904)[0]
        self.Uranus_y = Uranus_co.coordinates(19.29, 0.0472, 0.01343904)[1]
        self.Uranus_z = Uranus_co.coordinates(19.29, 0.0472, 0.01343904)[2]
        self.uranus1, = self.ax.plot([self.Uranus_x[0]], [self.Uranus_y[0]], [self.Uranus_z[0]], 'o', color = 'cyan')
        
        
        Pluto_co = Pluto3D(248.35, self.time)
        self.Pluto_x = Pluto_co.coordinates(39.51, 0.25, 0.3054326)[0]
        self.Pluto_y = Pluto_co.coordinates(39.51, 0.25, 0.3054326)[1]
        self.Pluto_z = Pluto_co.coordinates(39.51, 0.25, 0.3054326)[2]
        self.pluto1, = self.ax.plot([self.Pluto_x[0]], [self.Pluto_y[0]], [self.Pluto_z[0]], 'o', color = 'brown')
        
            
        self.plot_data()
  
    def update_points(self,n, x, y, z, point):
        
         point.set_data([x[n]], [y[n]])
        
         point.set_3d_properties(z[n], 'z')
        
         return point
    
    def start_animation3D(self):
        
        if not self.animation:  # If animation is not already running, start it
            
            
            animate_jupiter = animation.FuncAnimation(self.fig, self.update_points, len(self.Pluto_x) -1 , fargs = (self.Jupiter_x, self.Jupiter_y, self.Jupiter_z, self.jupiter1), interval = 16)                       
   
            animate_saturn = animation.FuncAnimation(self.fig, self.update_points, len(self.Pluto_x) -1 , fargs = (self.Saturn_x, self.Saturn_y, self.Saturn_z, self.saturn1), interval = 16) 
    
            animate_uranus = animation.FuncAnimation(self.fig, self.update_points, len(self.Pluto_x) -1 , fargs = (self.Uranus_x, self.Uranus_y, self.Uranus_z, self.uranus1), interval = 16) 
    
            animate_neptune = animation.FuncAnimation(self.fig, self.update_points, len(self.Pluto_x) -1, fargs = (self.Neptune_x, self.Neptune_y, self.Neptune_z, self.neptune1), interval = 16) 
    
            animate_pluto = animation.FuncAnimation(self.fig, self.update_points, len(self.Pluto_x) -1, fargs = (self.Pluto_x, self.Pluto_y, self.Pluto_z, self.pluto1), interval = 16)
            
    
            self.animation.append(animate_jupiter)
            self.animation.append(animate_saturn)
            self.animation.append(animate_uranus)
            self.animation.append(animate_neptune)
            self.animation.append(animate_pluto)
        
        self.draw()
                      
    def stop_animation3D(self):

         for animate in self.animation:
            animate.event_source.stop()  # Stop the animation
        

         self.animation = []  # Reset the animation list
         self.ax.clear()
         
         

         self.jupiter1, = self.ax.plot([self.Jupiter_x[0]], [self.Jupiter_y[0]], [self.Jupiter_z[0]], 'o', color = 'orange')
        
         self.saturn1, = self.ax.plot([self.Saturn_x[0]], [self.Saturn_y[0]], [self.Saturn_z[0]], 'o', color = 'yellow')
        
         self.neptune1, = self.ax.plot([self.Neptune_x[0]], [self.Neptune_y[0]], [self.Neptune_z[0]], 'o', color = 'blue')
            
         self.uranus1, = self.ax.plot([self.Uranus_x[0]], [self.Uranus_y[0]], [self.Uranus_z[0]], 'o', color = 'cyan')
            
         self.pluto1, = self.ax.plot([self.Pluto_x[0]], [self.Pluto_y[0]], [self.Pluto_z[0]], 'o', color = 'brown')
                
        
            
            # Plot data again
         self.ax.set_facecolor((0, 0, 0, 0)) 
         self.fig.set_facecolor((0, 0, 0, 0)) 
         self.plot_data()
            
            # Draw the canvas
         self.draw()   
         
         
    def soft_stop(self):
        for animate in self.animation:
            animate.event_source.stop()
    
    def resume(self):
        for animate in self.animation:
            animate.event_source.start()
    

                                                        
    
    def set_dark_background(self):
        self.ax.set_facecolor('#181E35')
 
        self.ax.xaxis._axinfo["grid"]["color"] = "black"
        self.ax.yaxis._axinfo["grid"]["color"] = "black"
        self.ax.zaxis._axinfo["grid"]["color"] = "black"

        # Set axis colors
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.xaxis.set_pane_color((1, 1, 1, 1))  # Set X-axis pane color to white
        self.ax.yaxis.set_pane_color((1, 1, 1, 1))  # Set Y-axis pane color to white
        self.ax.zaxis.set_pane_color((1, 1, 1, 1))  # Set Z-axis pane color to white
      
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
    
        self.ax.title.set_color('white')
        
    def plot_data(self):
        
        def saturn(Distance):
            saturn_x = []
            saturn_y = []
            saturn_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.0555) * np.cos(theta)) * np.cos(0.0434587)
                saturn_x.append(x)
            
                y = distance(Distance, theta, 0.0555) * np.sin(theta)
                saturn_y.append(y)
                
                z = (distance(Distance, theta, 0.0555) * np.cos(theta)) * np.sin(0.0434587)
                saturn_z.append(z)
                
            return saturn_x, saturn_y, saturn_z
    
        def jupiter(Distance):
            jupiter_x = []
            jupiter_y = []
            jupiter_z = []
            for theta in np.radians(range(0, 1000)):
                x =  (distance(Distance, theta, 0.048775) * np.cos(theta)) * np.cos(0.02286381)
                jupiter_x.append(x)
            
                y =  distance(Distance, theta, 0.048775) * np.sin(theta)
                jupiter_y.append(y)
                
                z = (distance(Distance, theta, 0.048775) * np.cos(theta)) * np.sin(0.02286381)
                jupiter_z.append(z)
        
            return jupiter_x, jupiter_y, jupiter_z
    
        def uranus(Distance):
            uranus_x = []
            uranus_y = []
            uranus_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.0472) * np.cos(theta)) * np.cos(0.01343904)
                uranus_x.append(x)
            
                y =  distance(Distance, theta, 0.0472) * np.sin(theta)
                uranus_y.append(y)
        
                z = (distance(Distance, theta, 0.0472) * np.cos(theta)) * np.sin(0.01343904)
                uranus_z.append(z)
                
            return uranus_x, uranus_y, uranus_z
    
        def neptune(Distance):
            neptune_x = []
            neptune_y = []
            neptune_z = []
            
            for theta in np.radians(range(0, 1000)):
                x =  (distance(Distance, theta, 0.0086) * np.cos(theta)) * np.cos(0.03089233)
                neptune_x.append(x)
            
                y =  distance(Distance, theta, 0.0086) * np.sin(theta)
                neptune_y.append(y)
                
                z = (distance(Distance, theta, 0.0086) * np.cos(theta)) * np.sin(0.03089233)
                neptune_z.append(z)
    
            return neptune_x, neptune_y, neptune_z
    
        def pluto(Distance):
            pluto_x = []
            pluto_y = []
            pluto_z = []
            for theta in np.radians(range(0, 1000)):
            
                x =  (distance(Distance, theta, 0.25) * np.cos(theta)) * np.cos(0.3054326)
                pluto_x.append(x)
            
                y =  distance(Distance, theta, 0.25) * np.sin(theta)
                pluto_y.append(y)
                
                z = (distance(Distance, theta, 0.25) * np.cos(theta)) * np.sin(0.3054326)
                pluto_z.append(z)
        
            return pluto_x, pluto_y, pluto_z
        
        
        self.ax.plot(jupiter(5.20)[0], jupiter(5.20)[1], jupiter(5.20)[2], linestyle = '-', color = 'orange', label = 'jupiter')
        self.ax.plot(saturn(9.58)[0], saturn(9.58)[1], saturn(9.58)[2],  linestyle = '-', color = 'yellow', label ="saturn")
        self.ax.plot(neptune(30.25)[0], neptune(30.25)[1], neptune(30.25)[2],  linestyle = '-', color = 'blue', label ="netpune")
        self.ax.plot(pluto(39.51)[0], pluto(39.51)[1], pluto(39.51)[2],  linestyle = '-',  color = 'brown', label ="pluto")
        self.ax.plot(uranus(19.29)[0], uranus(19.29)[1], uranus(19.29)[2],   linestyle = '-', color = 'cyan', label = "uranus")
   
        self.ax.scatter(0, 0, 0, color='yellow', label='Sun', s = 150)
   
       
        self.ax.set_aspect('equal')

        self.ax.set_xlabel(' X / AU')
        self.ax.set_ylabel(' Y / AU')
        self.ax.legend()
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.set_title("Outer Planets Orbit Animation")
        self.ax.legend()
            



        
            
        
            
        
        
# THIS IS WHERE YOU CAN DESIGN            
            

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)





        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setStyleSheet("color: #D0DCEC ; background-color: #181E35;")
        self.centralwidget.setStyleSheet("QWidget {background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.7, fx: 0.5, fy: 0.5, stop: 0 #303c6a, stop: 1 #181E35); color: #D0DCEC;}")

        ##
        ##D0DCEC

        from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
         
        plot1layout = QVBoxLayout(self.centralwidget)

       
        self.plot_widget = KeplersThirdLawCanvas(self.centralwidget)
        self.plot_widget.setGeometry(QtCore.QRect(120, 50, 600, 500))  # Adjust the geometry as per your requirement
        plot1layout.addWidget(self.plot_widget)
        self.plot_widget.setObjectName("plot_widget")
        self.plot_widget.hide()
        

        
        plt.style.use('dark_background')
        self.plot_widget2_inner = InnerOrbitCanvas(self.centralwidget)
        self.plot_widget2_inner.setGeometry(QtCore.QRect(120, 50, 600, 500))  # Adjust the geometry as per your requirement
        self.plot_widget2_inner.setObjectName("plot_widget2_inner")
        plot1layout.addWidget(self.plot_widget2_inner)
        self.plot_widget2_inner.hide() 
        
        
        self.plot_widget2_outer = OuterOrbitCanvas(self.centralwidget)
        self.plot_widget2_outer.setGeometry(QtCore.QRect(129, 40, 661, 611))  # Adjust the geometry as per your requirement
        self.plot_widget2_outer.setObjectName("plot_widget2_outer")
        plot1layout.addWidget(self.plot_widget2_outer)
        self.plot_widget2_outer.hide()
        
        self.plot_widget3_inner = InnerOrbitAnimationCanvas(self.centralwidget)
        self.plot_widget3_inner.setGeometry(QtCore.QRect(65, 2, 661, 611))
        self.plot_widget3_inner.setObjectName("plot_widget3_inner")
        self.plot_widget3_inner.setStyleSheet("background-color: transparent;")
        self.plot_widget3_inner.hide()

        self.plot_widget3_outer = OuterOrbitAnimationCanvas(self.centralwidget)
        self.plot_widget3_outer.setGeometry(QtCore.QRect(65, 2, 661, 611))
        self.plot_widget3_outer.setObjectName("plot_widget3_outer")
        self.plot_widget3_outer.setStyleSheet("background-color: transparent;")
        self.plot_widget3_outer.hide()
        
       
        
        
        self.plot_widget3DforInner = Inner3DOrbitCanvas(self.centralwidget)
        self.plot_widget3DforInner.setGeometry(QtCore.QRect(129, 40, 661, 611))
        self.plot_widget3DforInner.setObjectName("plot_widget3DforInner")
        plot1layout.addWidget(self.plot_widget3DforInner)
        self.plot_widget3DforInner.setStyleSheet("background-color: transparent;")
        self.plot_widget3DforInner.hide()
        
        self.plot_widget3DforOuter = Outer3DOrbitCanvas(self.centralwidget)
        self.plot_widget3DforOuter.setGeometry(QtCore.QRect(129, 40, 661, 611))
        self.plot_widget3DforOuter.setObjectName("plot_widget3DforOuter")
        plot1layout.addWidget(self.plot_widget3DforOuter)
        self.plot_widget3DforOuter.setStyleSheet("background-color: transparent;")
        self.plot_widget3DforOuter.hide()


        plt.style.use("default")
        self.plot_widgetforTask5 = PlutoAngleGraphCanvas(self.centralwidget)
        self.plot_widgetforTask5.setGeometry(QtCore.QRect(80, 40, 650, 550))
        self.plot_widgetforTask5.setObjectName("plot_widgetforTask5")
        self.plot_widgetforTask5.setStyleSheet("background-color: transparent;")
        self.plot_widgetforTask5.hide()
        
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(290, 610, 251, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(19)
        self.horizontalSlider.setValue(5)
        self.horizontalSlider.valueChanged.connect(self.sliderValueChanged)
        self.horizontalSlider.setStyleSheet("background-color: transparent;")
        self.horizontalSlider.hide()
        
        self.eccentricity = QtWidgets.QLabel(self.centralwidget)
        self.eccentricity.setGeometry(QtCore.QRect(345, 575, 251, 31 ))
        self.eccentricity.setObjectName("eccentricity")
        font = QtGui.QFont()
        font.setPointSize(17)
        self.eccentricity.setStyleSheet("background-color: transparent; color: white;")
        font.setBold(True)
        self.eccentricity.setFont(font)
        self.eccentricity.hide()



        
        self.main_title = QtWidgets.QLabel(self.centralwidget)
        self.main_title.setGeometry(QtCore.QRect(100, 60, 700, 81))
        self.main_title.setObjectName("Computational_challenge")
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.main_title.setFont(font)
        self.main_title.setStyleSheet("background-color: transparent; color: #FFFFFF;")

        self.our_names = QtWidgets.QLabel(self.centralwidget)
        self.our_names.setGeometry(QtCore.QRect(560, 650, 300, 50))
        self.our_names.setObjectName("Computational_challenge")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.our_names.setFont(font)
        self.our_names.setStyleSheet("background-color: transparent; color: #FFFFFF;")
        
        from PyQt5.QtWidgets import QGridLayout

        # main_layout = QGridLayout
        # self.setLayout(main_layout)

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow.setXOffset(5)
        shadow.setYOffset(5)

        shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(10)
        shadow2.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow2.setXOffset(5)
        shadow2.setYOffset(5)

        shadow3 = QtWidgets.QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(10)
        shadow3.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow3.setXOffset(5)
        shadow3.setYOffset(5)

        shadow4 = QtWidgets.QGraphicsDropShadowEffect()
        shadow4.setBlurRadius(10)
        shadow4.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow4.setXOffset(5)
        shadow4.setYOffset(5)

        shadow5 = QtWidgets.QGraphicsDropShadowEffect()
        shadow5.setBlurRadius(10)
        shadow5.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow5.setXOffset(5)
        shadow5.setYOffset(5)

        shadow6 = QtWidgets.QGraphicsDropShadowEffect()
        shadow6.setBlurRadius(10)
        shadow6.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow6.setXOffset(5)
        shadow6.setYOffset(5)
        
        shadow7 = QtWidgets.QGraphicsDropShadowEffect()
        shadow7.setBlurRadius(10)
        shadow7.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow7.setXOffset(5)
        shadow7.setYOffset(5)


        self.Task1_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task1_button.setGeometry(QtCore.QRect(60, 220, 300, 81))
        self.Task1_button.setObjectName("Task1_button")
        self.Task1_button.clicked.connect(self.hide_buttons)
        self.Task1_button.clicked.connect(self.show_keplers_third_law)
        # self.Task1_button.setStyleSheet("QPushButton#Task1_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; }")
        self.Task1_button.setStyleSheet("QPushButton#Task1_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task1_button:hover { background-color: #95CCE9; }")
        self.Task1_button.setGraphicsEffect(shadow2)
        
        
        self.Task2_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task2_button.setGeometry(QtCore.QRect(430, 220, 300, 81))
        self.Task2_button.setObjectName("Task2_button")
        self.Task2_button.clicked.connect(self.hide_buttons)
        self.Task2_button.clicked.connect(self.Inner_Outer)
        self.Task2_button.clicked.connect(self.select_orbit_path_comparison)
        self.Task2_button.setStyleSheet(
            """
            QPushButton#Task2_button {
                border-radius: 40px;
                background-color: #376991;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                text-align: center;
                padding: 10px 20px;
                }
            QPushButton#Task2_button:hover {
                background-color: #95CCE9;
                }
            QPushButton#Task2_button {
                background-color: #376991;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                text-align: center;
                padding: 10px 20px;
                border-image: none;
                border-radius: 40px;
                }
            QPushButton#Task2_button:hover {
                background-color: #95CCE9;
                }
            """
        )
        self.Task2_button.setGraphicsEffect(shadow)

        
        self.Task3_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task3_button.setGeometry(QtCore.QRect(60, 320, 300, 81))
        self.Task3_button.setObjectName("Task3_button")
        self.Task3_button.clicked.connect(self.hide_buttons)
        self.Task3_button.clicked.connect(self.Inner_Outer)
        self.Task3_button.clicked.connect(self.select_orbit_animation_2d)
        self.Task3_button.setStyleSheet("background-color: #376991;" )
        self.Task3_button.setStyleSheet("QPushButton#Task3_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task3_button:hover { background-color: #95CCE9; }")
        self.Task3_button.setGraphicsEffect(shadow3)
        
        self.Task4_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task4_button.setGeometry(QtCore.QRect(430, 320, 300, 81))
        self.Task4_button.setObjectName("Task4_button")
        self.Task4_button.clicked.connect(self.hide_buttons)
        self.Task4_button.clicked.connect(self.Inner_Outer)
        self.Task4_button.clicked.connect(self.select_orbit_animation_3d)
        self.Task4_button.setStyleSheet("background-color: #376991;" )
        self.Task4_button.setStyleSheet("QPushButton#Task4_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task4_button:hover { background-color: #95CCE9; }")
        self.Task4_button.setGraphicsEffect(shadow4)
        
        self.Task5_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task5_button.setGeometry(QtCore.QRect(60, 420, 300, 81))
        self.Task5_button.setObjectName("Task5_button")
        self.Task5_button.clicked.connect(self.hide_buttons)
        self.Task5_button.clicked.connect(self.show_pluto_angular_motion)
        self.Task5_button.setStyleSheet("background-color: #376991;" )
        self.Task5_button.setStyleSheet("QPushButton#Task5_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task5_button:hover { background-color: #95CCE9; }")
        self.Task5_button.setGraphicsEffect(shadow5)
        
        self.Task6_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task6_button.setGeometry(QtCore.QRect(430, 420, 300, 81))
        self.Task6_button.setObjectName("Task6_button")
        self.Task6_button.clicked.connect(self.hide_buttons)
        self.Task6_button.clicked.connect(self.Inner_Outer)
        self.Task6_button.clicked.connect(self.select_orbit_comparison)
        self.Task6_button.setStyleSheet("background-color: #376991;" )
        self.Task6_button.setStyleSheet("QPushButton#Task6_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task6_button:hover { background-color: #95CCE9; }")
        self.Task6_button.setGraphicsEffect(shadow6)
     
        
        self.Task7_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task7_button.setGeometry(QtCore.QRect(170, 530, 431, 81))
        self.Task7_button.setObjectName("Task7_button")
        self.Task7_button.clicked.connect(self.hide_buttons)
        self.Task7_button.clicked.connect(self.Inner_Outer)
        self.Task7_button.clicked.connect(self.select_central_body_orbit)
        self.Task7_button.setStyleSheet("background-color: #376991;" )
        self.Task7_button.setStyleSheet("QPushButton#Task7_button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; font-weight: bold; } QPushButton#Task7_button:hover { background-color: #95CCE9; }")
        self.Task7_button.setGraphicsEffect(shadow7)


        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(150, 600, 111, 51))
        self.startButton.setObjectName("startButton")
        self.startButton.setStyleSheet("QPushButton#startButton { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#startButton:hover { background-color: lightblue; } QPushButton#startButton:pressed { background-color: #D0DCEC; }")
        self.startButton.clicked.connect(self.start_animation)
        self.startButton.hide()

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(275, 600, 111, 51))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setStyleSheet("QPushButton#stopButton { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#stopButton:hover { background-color: lightblue; } QPushButton#stopButton:pressed { background-color: #D0DCEC; }")
        self.stopButton.clicked.connect(self.stop_animation)
        self.stopButton.hide()

        self.ResumeButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResumeButton.setGeometry(QtCore.QRect(400, 600, 111, 51))
        self.ResumeButton.setObjectName("ResumeButton")
        self.ResumeButton.setStyleSheet("QPushButton#ResumeButton { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#ResumeButton:hover { background-color: lightblue; } QPushButton#ResumeButton:pressed { background-color: #D0DCEC; }")
        self.ResumeButton.clicked.connect(self.resume_animation)
        self.ResumeButton.hide()

        self.ResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResetButton.setGeometry(QtCore.QRect(525, 600, 111, 51))
        self.ResetButton.setObjectName("ResetButton")
        self.ResetButton.setStyleSheet("QPushButton#ResetButton { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#ResetButton:hover { background-color: lightblue; } QPushButton#ResetButton:pressed { background-color: #D0DCEC; }")
        self.ResetButton.clicked.connect(self.reset_animation)
        self.ResetButton.hide()

        
        
        self.Return_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Return_Button.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Return_Button.setObjectName("Return_Button")
        self.Return_Button.setStyleSheet("QPushButton#Return_Button { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#Return_Button:hover { background-color: lightblue; } QPushButton#Return_Button:pressed { background-color: #D0DCEC; }")
        self.Return_Button.clicked.connect(self.return_button)
        self.Return_Button.hide()
        
        self.Return_Inner_Outer = QtWidgets.QPushButton(self.centralwidget)
        self.Return_Inner_Outer.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Return_Inner_Outer.setObjectName("Return")
        self.Return_Inner_Outer.setStyleSheet("QPushButton#Return { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#Return:hover { background-color: lightblue; } QPushButton#Return:pressed { background-color: #D0DCEC; }")
        self.Return_Inner_Outer.clicked.connect(self.uncheck_all_checkboxes_and_update_layouts)
        self.Return_Inner_Outer.clicked.connect(self.uncheck_all_checkboxes_and_update_layouts_task7)
        self.Return_Inner_Outer.clicked.connect(self.return_inner_outer)
        self.Return_Inner_Outer.hide()
        
        self.InnerPlanets_Button = QtWidgets.QPushButton(self.centralwidget)
        self.InnerPlanets_Button.setGeometry(QtCore.QRect(180, 140, 440, 190))
        self.InnerPlanets_Button.setObjectName("InnerPlanets_Button")
        icon_path1 = r'images\inner.jpg'
        inner_pixmap = QtGui.QPixmap(icon_path1)
        inner_pixmap = inner_pixmap.scaled(
            QtCore.QSize(440, 190),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.SmoothTransformation,
        )
        self.InnerPlanets_Button.setIcon(QtGui.QIcon(inner_pixmap))
        self.InnerPlanets_Button.setIconSize(QtCore.QSize(440, 190))
        self.InnerPlanets_Button.setStyleSheet("border:none;")
        self.InnerPlanets_Button.clicked.connect(self.show_inner_planet_orbits)
        self.InnerPlanets_Button.clicked.connect(self.show_inner_3d_orbit_animation)
        self.InnerPlanets_Button.clicked.connect(self.show_inner_orbit_animation)
        self.InnerPlanets_Button.clicked.connect(self.show_inner_orbit_comparison)
        self.InnerPlanets_Button.clicked.connect(self.show_inner_central_body_orbit_controls)
        self.InnerPlanets_Button.clicked.connect(self.select_inner_zone)
        self.InnerPlanets_Button.hide()
        
        
        self.OuterPlanets_Button = QtWidgets.QPushButton(self.centralwidget)
        self.OuterPlanets_Button.setGeometry(QtCore.QRect(180, 410, 440, 190))
        self.OuterPlanets_Button.setText("")
        self.OuterPlanets_Button.setObjectName("OuterPlanets_Button")
        icon_path2 = r'images\outer.jpg'
        outer_pixmap = QtGui.QPixmap(icon_path2)
        outer_pixmap = outer_pixmap.scaled(
            QtCore.QSize(440, 190),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.SmoothTransformation,
        )
        self.OuterPlanets_Button.setIcon(QtGui.QIcon(outer_pixmap))
        self.OuterPlanets_Button.setIconSize(QtCore.QSize(440, 190))
        self.OuterPlanets_Button.setStyleSheet("border:none;")
        self.OuterPlanets_Button.clicked.connect(self.show_outer_planet_orbits)
        self.OuterPlanets_Button.clicked.connect(self.show_outer_3d_orbit_animation)
        self.OuterPlanets_Button.clicked.connect(self.show_outer_orbit_animation)
        self.OuterPlanets_Button.clicked.connect(self.show_outer_orbit_comparison)
        self.OuterPlanets_Button.clicked.connect(self.show_outer_central_body_orbit_controls)
        self.OuterPlanets_Button.clicked.connect(self.select_outer_zone)
        self.OuterPlanets_Button.hide()
        
        self.InnerPlanetsLabel = QtWidgets.QLabel(self.centralwidget)
        self.InnerPlanetsLabel.setGeometry(QtCore.QRect(200, 70, 521, 51))
        font = QtGui.QFont()
        font.setBold
        font.setFamily("Arial")
        font.setPointSize(36)
        self.InnerPlanetsLabel.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.InnerPlanetsLabel.setFont(font)
        self.InnerPlanetsLabel.setObjectName("InnerPlanetsLabel")
        self.InnerPlanetsLabel.hide()
        
        
        self.OuterPlanetsLabel = QtWidgets.QLabel(self.centralwidget)
        self.OuterPlanetsLabel.setGeometry(QtCore.QRect(200, 350, 521, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.OuterPlanetsLabel.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.OuterPlanetsLabel.setFont(font)
        self.OuterPlanetsLabel.setObjectName("OuterPlanetsLabel")
        self.OuterPlanetsLabel.hide()

        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setStyleSheet("background-color: transparent;")
        self.label.setFont(font)
        self.label.setObjectName("OuterPlanetlabel")
        self.label.hide()

        self.inner_planets_label = QtWidgets.QLabel(self.centralwidget)
        self.inner_planets_label.setEnabled(True)
        self.inner_planets_label.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.inner_planets_label.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.inner_planets_label.setFont(font)
        self.inner_planets_label.setObjectName("InnerPlanetlabel")
        self.inner_planets_label.hide()
       
        
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setEnabled(True)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 200, 101, 251))
        self.layoutWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget.setStyleSheet("background-color: transparent;")
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.hide()
        
        self.Checkboxgroup = QtWidgets.QGridLayout(self.layoutWidget)
        self.Checkboxgroup.setContentsMargins(0, 0, 0, 0)
        self.Checkboxgroup.setObjectName("Checkboxgroup")
        
        
        
        
        self.PlutoCheckbox1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.PlutoCheckbox1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PlutoCheckbox1.setStyleSheet("background-color: transparent;")
        self.PlutoCheckbox1.setFont(font)
        self.PlutoCheckbox1.setAutoExclusive(True)
        self.PlutoCheckbox1.setObjectName("PlutoCheckbox1")
        self.Checkboxgroup.addWidget(self.PlutoCheckbox1, 4, 0, 1, 1)
        self.PlutoCheckbox1.hide()
        
        self.SaturnCheckbox1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.SaturnCheckbox1.setEnabled(True)
        self.SaturnCheckbox1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SaturnCheckbox1.setStyleSheet("background-color: transparent;")
        self.SaturnCheckbox1.setFont(font)
        self.SaturnCheckbox1.setAutoExclusive(True)
        self.SaturnCheckbox1.setObjectName("SaturnCheckbox1")
        self.Checkboxgroup.addWidget(self.SaturnCheckbox1, 1, 0, 1, 1)
        self.SaturnCheckbox1.hide()
        
        self.NeptuneCheckbox1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.NeptuneCheckbox1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NeptuneCheckbox1.setStyleSheet("background-color: transparent;")
        self.NeptuneCheckbox1.setFont(font)
        self.NeptuneCheckbox1.setAutoExclusive(True)
        self.NeptuneCheckbox1.setObjectName("NeptuneCheckbox1")
        self.Checkboxgroup.addWidget(self.NeptuneCheckbox1, 3, 0, 1, 1)
        self.NeptuneCheckbox1.hide()
        
        self.JupiterCheckbox1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.JupiterCheckbox1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.JupiterCheckbox1.setStyleSheet("background-color: transparent;")
        self.JupiterCheckbox1.setFont(font)
        self.JupiterCheckbox1.setAutoExclusive(True)
        self.JupiterCheckbox1.setObjectName("JupiterCheckbox1")
        self.Checkboxgroup.addWidget(self.JupiterCheckbox1, 0, 0, 1, 1)
        self.JupiterCheckbox1.hide()
        
        self.UranusCheckbox1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.UranusCheckbox1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UranusCheckbox1.setStyleSheet("background-color: transparent;")
        self.UranusCheckbox1.setFont(font)
        self.UranusCheckbox1.setAutoExclusive(True)
        self.UranusCheckbox1.setObjectName("UranusCheckbox1")
        self.Checkboxgroup.addWidget(self.UranusCheckbox1, 2, 0, 1, 1)
        self.UranusCheckbox1.hide()
        
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setEnabled(True)
        self.layoutWidget_2.setGeometry(QtCore.QRect(180, 200, 101, 251))
        self.layoutWidget_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget_2.setStyleSheet("background-color: transparent;")
        self.layoutWidget_2.setFont(font)
        self.layoutWidget_2.setObjectName("Choose_Planets")
        self.layoutWidget_2.hide()
        
        self.Checkboxgroup_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.Checkboxgroup_2.setContentsMargins(0, 0, 0, 0)
        self.Checkboxgroup_2.setObjectName("Checkboxgroup_2")
        
        self.SaturnCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.SaturnCheckbox2.setEnabled(True)
        self.SaturnCheckbox2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SaturnCheckbox2.setStyleSheet("background-color: transparent;")
        self.SaturnCheckbox2.setFont(font)
        self.SaturnCheckbox2.setAutoExclusive(True)
        self.SaturnCheckbox2.setObjectName("SaturnCheckbox2")
        self.Checkboxgroup_2.addWidget(self.SaturnCheckbox2, 1, 0, 1, 1)
        self.SaturnCheckbox2.hide()
        
        self.NeptuneCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.NeptuneCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NeptuneCheckbox2.setStyleSheet("background-color: transparent;")
        self.NeptuneCheckbox2.setFont(font)
        self.NeptuneCheckbox2.setAutoExclusive(True)
        self.NeptuneCheckbox2.setObjectName("NeptuneCheckbox2")
        self.Checkboxgroup_2.addWidget(self.NeptuneCheckbox2, 3, 0, 1, 1)
        self.NeptuneCheckbox2.hide()

        self.JupiterCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.JupiterCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.JupiterCheckbox2.setStyleSheet("background-color: transparent;")
        self.JupiterCheckbox2.setFont(font)
        self.JupiterCheckbox2.setAutoExclusive(True)
        self.JupiterCheckbox2.setObjectName("JupiterCheckbox2")
        self.Checkboxgroup_2.addWidget(self.JupiterCheckbox2, 0, 0, 1, 1)
        self.JupiterCheckbox2.hide()

        self.UranusCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.UranusCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UranusCheckbox2.setStyleSheet("background-color: transparent;")
        self.UranusCheckbox2.setFont(font)
        self.UranusCheckbox2.setAutoExclusive(True)
        self.UranusCheckbox2.setObjectName("UranusCheckbox2")
        self.Checkboxgroup_2.addWidget(self.UranusCheckbox2, 2, 0, 1, 1)
        self.UranusCheckbox2.hide()

        self.PlutoCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.PlutoCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PlutoCheckbox2.setStyleSheet("background-color: transparent;")
        self.PlutoCheckbox2.setFont(font)
        self.PlutoCheckbox2.setAutoExclusive(True)
        self.PlutoCheckbox2.setObjectName("PlutoCheckbox2")
        self.Checkboxgroup_2.addWidget(self.PlutoCheckbox2, 4, 0, 1, 1)
        self.PlutoCheckbox2.hide()


        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setEnabled(True)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 200, 101, 251))
        self.layoutWidget3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget3.setStyleSheet("background-color: transparent;")
        self.layoutWidget3.setFont(font)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.hide()

        self.Checkboxgroup3 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.Checkboxgroup3.setContentsMargins(0, 0, 0, 0)
        self.Checkboxgroup3.setObjectName("Checkboxgroup3")

        self.MercuryCheckbox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.MercuryCheckbox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MercuryCheckbox.setStyleSheet("background-color: transparent;")
        self.MercuryCheckbox.setFont(font)
        self.MercuryCheckbox.setAutoExclusive(True)
        self.MercuryCheckbox.setObjectName("MercuryCheckbox")
        self.Checkboxgroup3.addWidget(self.MercuryCheckbox, 0, 0, 1, 1)
        self.MercuryCheckbox.hide()

        self.VenusCheckbox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.VenusCheckbox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.VenusCheckbox.setStyleSheet("background-color: transparent;")
        self.VenusCheckbox.setFont(font)
        self.VenusCheckbox.setAutoExclusive(True)
        self.VenusCheckbox.setObjectName("VenusCheckbox")
        self.Checkboxgroup3.addWidget(self.VenusCheckbox, 1, 0, 1, 1)
        self.VenusCheckbox.hide()

        self.EarthCheckbox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.EarthCheckbox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.EarthCheckbox.setStyleSheet("background-color: transparent;")
        self.EarthCheckbox.setFont(font)
        self.EarthCheckbox.setAutoExclusive(True)
        self.EarthCheckbox.setObjectName("EarthCheckbox")
        self.Checkboxgroup3.addWidget(self.EarthCheckbox, 2, 0, 1, 1)
        self.EarthCheckbox.hide()

        self.MarsCheckbox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.MarsCheckbox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MarsCheckbox.setStyleSheet("background-color: transparent;")
        self.MarsCheckbox.setFont(font)
        self.MarsCheckbox.setAutoExclusive(True)
        self.MarsCheckbox.setObjectName("MarsCheckbox")
        self.Checkboxgroup3.addWidget(self.MarsCheckbox, 3, 0, 1, 1)
        self.MarsCheckbox.hide()

        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setEnabled(True)
        self.layoutWidget4.setGeometry(QtCore.QRect(180, 200, 101, 251))
        self.layoutWidget4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget4.setStyleSheet("background-color: transparent;")
        self.layoutWidget4.setFont(font)
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.layoutWidget4.hide()

        self.Checkboxgroup4 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.Checkboxgroup4.setContentsMargins(0, 0, 0, 0)
        self.Checkboxgroup4.setObjectName("Checkboxgroup4")

        self.MercuryCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.MercuryCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MercuryCheckbox2.setStyleSheet("background-color: transparent;")
        self.MercuryCheckbox2.setFont(font)
        self.MercuryCheckbox2.setAutoExclusive(True)
        self.MercuryCheckbox2.setObjectName("MercuryCheckbox2")
        self.Checkboxgroup4.addWidget(self.MercuryCheckbox2, 0, 0, 1, 1)
        self.MercuryCheckbox2.hide()

        self.VenusCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.VenusCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.VenusCheckbox2.setStyleSheet("background-color: transparent;")
        self.VenusCheckbox2.setFont(font)
        self.VenusCheckbox2.setAutoExclusive(True)
        self.VenusCheckbox2.setObjectName("VenusCheckbox2")
        self.Checkboxgroup4.addWidget(self.VenusCheckbox2, 1, 0, 1, 1)
        self.VenusCheckbox2.hide()

        self.EarthCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.EarthCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.EarthCheckbox2.setStyleSheet("background-color: transparent;")
        self.EarthCheckbox2.setFont(font)
        self.EarthCheckbox2.setAutoExclusive(True)
        self.EarthCheckbox2.setObjectName("EarthCheckbox")
        self.Checkboxgroup4.addWidget(self.EarthCheckbox2, 2, 0, 1, 1)
        self.EarthCheckbox2.hide()

        self.MarsCheckbox2 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.MarsCheckbox2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MarsCheckbox2.setStyleSheet("background-color: transparent;")
        self.MarsCheckbox2.setFont(font)
        self.MarsCheckbox2.setAutoExclusive(True)
        self.MarsCheckbox2.setObjectName("MarsCheckbox")
        self.Checkboxgroup4.addWidget(self.MarsCheckbox2, 3, 0, 1, 1)
        self.MarsCheckbox2.hide()


        self.Planet1 = QtWidgets.QLabel(self.centralwidget)
        self.Planet1.setGeometry(QtCore.QRect(10, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Planet1.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.Planet1.setFont(font)
        self.Planet1.setObjectName("Planet1")
        self.Planet1.hide()
        
        self.Planet1_2 = QtWidgets.QLabel(self.centralwidget)
        self.Planet1_2.setGeometry(QtCore.QRect(170, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Planet1_2.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.Planet1_2.setFont(font)
        self.Planet1_2.setObjectName("Planet1_2")
        self.Planet1_2.hide()
        
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(180, 480, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox.setStyleSheet("background-color: transparent;")
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.hide()
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 480, 140, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setStyleSheet("background-color: transparent;")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.hide()
        
        self.PlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlotButton.setGeometry(QtCore.QRect(470, 520, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PlotButton.setFont(font)
        self.PlotButton.setObjectName("PlotButton6")
        self.PlotButton.setStyleSheet("QPushButton#PlotButton6 { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#PlotButton6:hover { background-color: lightblue; } QPushButton#PlotButton6:pressed { background-color: #D0DCEC; }")
        self.PlotButton.clicked.connect(self.check_checkbox_group1)
        self.PlotButton.clicked.connect(self.check_checkbox_group2)
        self.PlotButton.clicked.connect(self.plot_orbit_comparison)
        self.PlotButton.hide()


        self.plot_widgetforTask6 = OrbitComparisonCanvas(self.centralwidget)
        self.plot_widgetforTask6.setGeometry(QtCore.QRect(310, 90, 471, 421))  
        self.plot_widgetforTask6.setObjectName("plot_widget6")
        self.plot_widgetforTask6.setStyleSheet("background-color: transparent;")
        self.plot_widgetforTask6.hide()
        
        self.selected_planets = QtWidgets.QLabel(self.centralwidget)
        self.selected_planets.setGeometry(QtCore.QRect(435, 190, 400, 200))
        self.selected_planets.setStyleSheet("background-color: transparent; border: none; color: black;")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.selected_planets.setFont(font)
        self.selected_planets.setObjectName("selected_planets")
        self.selected_planets.setText(" ")
        self.selected_planets.hide()


        self.Plot_Button_task7 = QtWidgets.QPushButton(self.centralwidget)
        self.Plot_Button_task7.setGeometry(QtCore.QRect(370, 530, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Plot_Button_task7.setFont(font)
        self.Plot_Button_task7.setObjectName("Plot_Button_task7")
        self.Plot_Button_task7.clicked.connect(self.plot_central_body_orbit_2d)
        self.Plot_Button_task7.setStyleSheet("QPushButton#Plot_Button_task7 { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#Plot_Button_task7:hover { background-color: lightblue; } QPushButton#Plot_Button_task7:pressed { background-color: #D0DCEC; }")
        self.Plot_Button_task7.hide()


        self.Inner_task7 = QtWidgets.QLabel(self.centralwidget)
        self.Inner_task7.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Inner_task7.setStyleSheet("background-color: transparent;")
        self.Inner_task7.setFont(font)
        self.Inner_task7.setObjectName("Inner_task7")
        self.Inner_task7.hide()

        self.Choose_Centre = QtWidgets.QLabel(self.centralwidget)
        self.Choose_Centre.setGeometry(QtCore.QRect(40, 150, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Choose_Centre.setStyleSheet("background-color: transparent;")
        self.Choose_Centre.setFont(font)
        self.Choose_Centre.setObjectName("Choose_Centre")
        self.Choose_Centre.hide()

        self.info_box = QtWidgets.QLabel(self.centralwidget)
        self.info_box.setGeometry(QtCore.QRect(55,460,250,100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box.setStyleSheet("background-color: transparent;")
        self.info_box.setFont(font)
        self.info_box.setObjectName("Advised_number_of_orbits")
        self.info_box.hide()

        self.info_box_2 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_2.setGeometry(QtCore.QRect(55,460,250,100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_2.setStyleSheet("background-color: transparent;")
        self.info_box_2.setFont(font)
        self.info_box_2.setObjectName("Advised_number_of_orbits_2")
        self.info_box_2.hide()

        self.info_box_3 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_3.setGeometry(QtCore.QRect(30,520,250,30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_3.setStyleSheet("background-color: transparent;")
        self.info_box_3.setFont(font)
        self.info_box_3.setObjectName("Advised_number_of_orbits_3")
        self.info_box_3.hide()

        self.info_box_4 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_4.setGeometry(QtCore.QRect(30,520,250,30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_4.setStyleSheet("background-color: transparent;")
        self.info_box_4.setFont(font)
        self.info_box_4.setObjectName("Advised_number_of_orbits_5")
        self.info_box_4.hide()

        self.label_2_task7 = QtWidgets.QLabel(self.centralwidget)
        self.label_2_task7.setGeometry(QtCore.QRect(60, 430, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2_task7.setFont(font)
        self.label_2_task7.setObjectName("label_2_7")
        self.label_2_task7.setStyleSheet("background-color: transparent;")
        self.label_2_task7.hide()

        self.spinBox_task7 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_task7.setGeometry(QtCore.QRect(220, 450, 71, 31))
        self.spinBox_task7.setMinimum(1)
        self.spinBox_task7.setMaximum(1000)
        self.spinBox_task7.setObjectName("spinBox_task7")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox_task7.setStyleSheet("background-color: transparent;")
        self.spinBox_task7.setFont(font)
        self.spinBox_task7.hide()

        self.Plot_3d = QtWidgets.QPushButton(self.centralwidget)
        self.Plot_3d.setGeometry(QtCore.QRect(550, 530, 151, 51))
        self.Plot_3d.setObjectName("Plot_3d")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Plot_3d.setFont(font)
        self.Plot_3d.setStyleSheet("QPushButton#Plot_3d { border-radius: 40px; background-color: #376991; color: white; font-size: 18px; } QPushButton#Plot_3d:hover { background-color: lightblue; } QPushButton#Plot_3d:pressed { background-color: #D0DCEC; }")
        self.Plot_3d.clicked.connect(self.plot_central_body_orbit_3d)
        self.Plot_3d.hide()

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 200, 201, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.widget.setFont(font)
        self.widget.setStyleSheet("background-color: transparent;")
        self.widget.setObjectName("widget")
        self.widget.setVisible(False)

        self.InnerPlanetGrid = QtWidgets.QGridLayout(self.widget)
        self.InnerPlanetGrid.setContentsMargins(0, 0, 0, 0)
        self.InnerPlanetGrid.setObjectName("InnerPlanetGrid")
        

        checkbox_font = QtGui.QFont()
        checkbox_font.setPointSize(12)

        self.Earth_checkbox = QtWidgets.QCheckBox(self.widget)
        self.Earth_checkbox.setFont(checkbox_font)
        self.Earth_checkbox.setAutoExclusive(True)
        self.Earth_checkbox.setObjectName("Earth_checkbox")
        self.InnerPlanetGrid.addWidget(self.Earth_checkbox, 2, 0, 1, 1)
        self.Earth_checkbox.setStyleSheet("background-color: transparent;")
        self.Earth_checkbox.hide()

        self.Venus_checkbox = QtWidgets.QCheckBox(self.widget)
        self.Venus_checkbox.setFont(checkbox_font)
        self.Venus_checkbox.setAutoExclusive(True)
        self.Venus_checkbox.setObjectName("Venus_checkbox")
        self.InnerPlanetGrid.addWidget(self.Venus_checkbox, 1, 0, 1, 1)
        self.Venus_checkbox.setStyleSheet("background-color: transparent;")
        self.Venus_checkbox.hide()

        self.Mercury_checkbox = QtWidgets.QCheckBox(self.widget)
        self.Mercury_checkbox.setFont(checkbox_font)
        self.Mercury_checkbox.setAutoExclusive(True)
        self.Mercury_checkbox.setObjectName("Mercury_checkbox")
        self.InnerPlanetGrid.addWidget(self.Mercury_checkbox, 0, 0, 1, 1)
        self.Mercury_checkbox.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.Mercury_checkbox.hide()

        self.Mars_checkbox = QtWidgets.QCheckBox(self.widget)
        self.Mars_checkbox.setFont(checkbox_font)
        self.Mars_checkbox.setAutoExclusive(True)
        self.Mars_checkbox.setObjectName("Mars_checkbox")
        self.InnerPlanetGrid.addWidget(self.Mars_checkbox, 3, 0, 1, 1)
        self.Mars_checkbox.setStyleSheet("background-color: transparent;")
        self.Mars_checkbox.hide()

        self.selected_planet = QtWidgets.QLabel(self.centralwidget)
        self.selected_planet.setGeometry(QtCore.QRect(470, 200, 321, 200))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selected_planet.setStyleSheet("background-color: transparent; border: none; color: white")
        self.selected_planet.setFont(font)
        self.selected_planet.setObjectName("selected_planets")
        self.selected_planet.setText(" ")
        self.selected_planet.hide()
        
        self.Outer_task7 = QtWidgets.QLabel(self.centralwidget)
        self.Outer_task7.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Outer_task7.setStyleSheet("background-color: transparent;")
        self.Outer_task7.setFont(font)
        self.Outer_task7.setObjectName("Outer_task7")
        self.Outer_task7.hide()


        self.layoutWidget7 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget7.setGeometry(QtCore.QRect(70, 210, 201, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.layoutWidget7.setStyleSheet("background-color: transparent;")
        self.layoutWidget7.setFont(font)
        self.layoutWidget7.setObjectName("layoutWidget")
        self.layoutWidget7.hide()

        self.OuterPlanetGrid = QtWidgets.QGridLayout(self.layoutWidget7)
        self.OuterPlanetGrid.setContentsMargins(0, 0, 0, 0)
        self.OuterPlanetGrid.setObjectName("OuterPlanetGrid")
        
        
        self.Jupiter_checkbox = QtWidgets.QCheckBox(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Jupiter_checkbox.setStyleSheet("background-color: transparent;")
        self.Jupiter_checkbox.setFont(font)
        self.Jupiter_checkbox.setAutoExclusive(True)
        self.Jupiter_checkbox.setObjectName("Jupiter_checkbox")
        self.OuterPlanetGrid.addWidget(self.Jupiter_checkbox, 0, 0, 1, 1)
        self.Jupiter_checkbox.hide()
        
        self.Uranus_checkbox = QtWidgets.QCheckBox(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Uranus_checkbox.setStyleSheet("background-color: transparent;")
        self.Uranus_checkbox.setFont(font)
        self.Uranus_checkbox.setAutoExclusive(True)
        self.Uranus_checkbox.setObjectName("Uranus_checkbox")
        self.OuterPlanetGrid.addWidget(self.Uranus_checkbox, 2, 0, 1, 1)
        self.Uranus_checkbox.hide()
        
        self.Saturn_checkbox = QtWidgets.QCheckBox(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Saturn_checkbox.setStyleSheet("background-color: transparent;")
        self.Saturn_checkbox.setFont(font)
        self.Saturn_checkbox.setAutoExclusive(True)
        self.Saturn_checkbox.setObjectName("Saturn_checkbox")
        self.OuterPlanetGrid.addWidget(self.Saturn_checkbox, 1, 0, 1, 1)
        self.Saturn_checkbox.hide()
        
        self.Neptune_checkbox = QtWidgets.QCheckBox(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Neptune_checkbox.setStyleSheet("background-color: transparent;")
        self.Neptune_checkbox.setFont(font)
        self.Neptune_checkbox.setAutoExclusive(True)
        self.Neptune_checkbox.setObjectName("Neptune_checkbox")
        self.OuterPlanetGrid.addWidget(self.Neptune_checkbox, 3, 0, 1, 1)
        self.Neptune_checkbox.hide()
        
        self.Pluto_Checkbox = QtWidgets.QCheckBox(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Pluto_Checkbox.setStyleSheet("background-color: transparent;")
        self.Pluto_Checkbox.setFont(font)
        self.Pluto_Checkbox.setAutoExclusive(True)
        self.Pluto_Checkbox.setObjectName("Pluto_Checkbox")
        self.OuterPlanetGrid.addWidget(self.Pluto_Checkbox, 4, 0, 1, 1)
        self.Pluto_Checkbox.hide()
        

        
        
        self.plot_widget_task7 = CentralBodyOrbitCanvas(self.centralwidget)
        self.plot_widget_task7.setGeometry(QtCore.QRect(310, 90, 471, 421))  # Adjust the geometry as per your requirement
        self.plot_widget_task7.setObjectName("plot_widget7")
        self.plot_widget_task7.setStyleSheet("background-color: transparent;")
        self.plot_widget_task7.hide()

        self.plot_widget_task7_3D = CentralBodyOrbit3DCanvas(self.centralwidget)
        self.plot_widget_task7_3D.setGeometry(QtCore.QRect(310, 90, 471, 421))  # Adjust the geometry as per your requirement
        self.plot_widget_task7_3D.setObjectName("plot_widget7v2")
        self.plot_widget_task7_3D.setStyleSheet("background-color: transparent;")
        self.plot_widget_task7_3D.hide()


        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(plot1layout)
       
    
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Task1_button.setText(_translate("MainWindow", "Kepler's 3rd Law"))
        self.Task2_button.setText(_translate("MainWindow", "2D Graph of Orbits"))
        self.Task3_button.setText(_translate("MainWindow", "2D Animation of Orbits"))
        self.Task4_button.setText(_translate("MainWindow", "3D Animation of Orbits"))
        self.Task5_button.setText(_translate("MainWindow", "Orbital Angle vs Time"))
        self.Task6_button.setText(_translate("MainWindow", "Solar System Spirograph"))
        self.Task7_button.setText(_translate("MainWindow", "Set Central Body and Plot Orbits"))
        self.main_title.setText(_translate("MainWindow", "Celestial Orbits Visualiser"))
        self.our_names.setText(_translate("MainWindow", "Created by Adam Wasiak"))
        self.Return_Button.setText(_translate("MainWindow", "Return"))
        self.InnerPlanetsLabel.setText(_translate("MainWindow", "Inner planet orbits"))
        self.OuterPlanetsLabel.setText(_translate("MainWindow", "Outer planet orbits"))
        self.Return_Inner_Outer.setText(_translate("MainWindow","Return"))
        self.label.setText(_translate("MainWindow", "Outer Planets"))
        self.PlutoCheckbox1.setText(_translate("MainWindow", "Pluto"))
        self.SaturnCheckbox1.setText(_translate("MainWindow", "Saturn"))
        self.NeptuneCheckbox1.setText(_translate("MainWindow", "Neptune"))
        self.JupiterCheckbox1.setText(_translate("MainWindow", "Jupiter"))
        self.UranusCheckbox1.setText(_translate("MainWindow", "Uranus"))
        self.SaturnCheckbox2.setText(_translate("MainWindow", "Saturn"))
        self.NeptuneCheckbox2.setText(_translate("MainWindow", "Neptune"))
        self.JupiterCheckbox2.setText(_translate("MainWindow", "Jupiter"))
        self.UranusCheckbox2.setText(_translate("MainWindow", "Uranus"))
        self.PlutoCheckbox2.setText(_translate("MainWindow", "Pluto"))
        self.Planet1.setText(_translate("MainWindow", "Planet Number 1"))
        self.Planet1_2.setText(_translate("MainWindow", "Planet Number 2"))
        self.label_2.setText(_translate("MainWindow", "Number of Orbits:"))
        self.PlotButton.setText(_translate("MainWindow", "Plot!"))
        self.selected_planets.setText(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", "Outer Planets"))
        self.EarthCheckbox.setText(_translate("MainWindow", "Earth"))
        self.VenusCheckbox.setText(_translate("MainWindow", "Venus"))
        self.MercuryCheckbox.setText(_translate("MainWindow", "Mercury"))
        self.MarsCheckbox.setText(_translate("MainWindow", "Mars"))
        self.MarsCheckbox2.setText(_translate("MainWindow", "Mars"))
        self.VenusCheckbox2.setText(_translate("MainWindow", "Venus"))
        self.MercuryCheckbox2.setText(_translate("MainWindow", "Mercury"))
        self.EarthCheckbox2.setText(_translate("MainWindow", "Earth"))
        self.inner_planets_label.setText(_translate("MainWindow", "Inner Planets"))
        self.Plot_Button_task7.setText(_translate("MainWindow", "Plot in 2D"))
        self.Inner_task7.setText(_translate("MainWindow", "Inner Planets"))
        self.Choose_Centre.setText(_translate("MainWindow", "Choose Centre Planet:"))
        self.info_box.setText(_translate("MainWindow", "Recommended number of orbits: 400-600*"))
        self.info_box_2.setText(_translate("MainWindow", "Recommended number of orbits: ~20*"))
        self.info_box_3.setText(_translate("MainWindow", "Recommended number of orbits: 400-600*"))
        self.info_box_4.setText(_translate("MainWindow", "Recommended number of orbits: ~20*"))
        self.label_2_task7.setText(_translate("MainWindow", "Number of Years:"))
        self.Plot_3d.setText(_translate("MainWindow", "Plot in 3D"))
        self.Earth_checkbox.setText(_translate("MainWindow", "Earth"))
        self.Venus_checkbox.setText(_translate("MainWindow", "Venus"))
        self.Mercury_checkbox.setText(_translate("MainWindow", "Mercury"))
        self.Mars_checkbox.setText(_translate("MainWindow", "Mars"))
        self.selected_planet.setText(_translate("MainWindow", "No Planet selected"))
        self.Jupiter_checkbox.setText(_translate("MainWindow", "Jupiter"))
        self.Uranus_checkbox.setText(_translate("MainWindow", "Uranus"))
        self.Saturn_checkbox.setText(_translate("MainWindow", "Saturn"))
        self.Neptune_checkbox.setText(_translate("MainWindow", "Neptune"))
        self.Pluto_Checkbox.setText(_translate("MainWindow", "Pluto"))
        self.Outer_task7.setText(_translate("MainWindow", "Outer Planets"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.ResumeButton.setText(_translate("MainWindow", "Resume"))
        self.ResetButton.setText(_translate("MainWindow", "Reset"))
        self.eccentricity.setText(_translate("MainWindow", "Eccentricty"))
        
        
        
    



    global orbit_path_comparison_selected
    orbit_path_comparison_selected = False   
    def select_orbit_path_comparison(self):
        global orbit_path_comparison_selected
        orbit_path_comparison_selected = True
     
    global orbit_animation_2d_selected
    orbit_animation_2d_selected = False   
    def select_orbit_animation_2d(self):
        global orbit_animation_2d_selected
        orbit_animation_2d_selected = True
    
    global orbit_animation_3d_selected
    orbit_animation_3d_selected = False   
    def select_orbit_animation_3d(self):
        global orbit_animation_3d_selected
        orbit_animation_3d_selected = True
        

    global orbit_comparison_selected
    orbit_comparison_selected = False
    def select_orbit_comparison(self):
        global orbit_comparison_selected
        orbit_comparison_selected = True
        

    global central_body_orbit_selected
    central_body_orbit_selected = False
    def select_central_body_orbit(self):
        global central_body_orbit_selected
        central_body_orbit_selected = True

    global inner
    inner = False
    def select_inner_zone(self):
        global inner
        inner = True
    
    global outer
    outer = False
    def select_outer_zone(self):
        global outer
        outer = True


    def start_animation(self):
        if orbit_animation_2d_selected == True:
            if inner == True:
                self.plot_widget3_inner.start_animation()
            if outer == True:
                self.plot_widget3_outer.start_animation()
        
        if orbit_animation_3d_selected == True:
            if inner == True:
                self.plot_widget3DforInner.start_animation3D()
            if outer == True:
                self.plot_widget3DforOuter.start_animation3D()


    def stop_animation(self):
        if orbit_animation_2d_selected == True:
            if inner == True:
               self.plot_widget3_inner.soft_stop()
            if outer == True:
               self.plot_widget3_outer.soft_stop()
        
        if orbit_animation_3d_selected == True:
            if inner == True:
                self.plot_widget3DforInner.soft_stop()
            if outer == True:
                self.plot_widget3DforOuter.soft_stop()
        
    def resume_animation(self):
         if orbit_animation_2d_selected == True:
            if inner == True:
                self.plot_widget3_inner.resume()
            if outer == True:
                self.plot_widget3_outer.resume()
        
         if orbit_animation_3d_selected == True:
            if inner == True:
                self.plot_widget3DforInner.resume()
            if outer == True:
                self.plot_widget3DforOuter.resume()

    def reset_animation(self):
        if orbit_animation_2d_selected == True:
            if inner == True:
                self.plot_widget3_inner.stop_animation()
            if outer == True:
                self.plot_widget3_outer.stop_animation()
        
        if orbit_animation_3d_selected == True:
            if inner == True:
                self.plot_widget3DforInner.stop_animation3D()
            if outer == True:
                self.plot_widget3DforOuter.stop_animation3D()
    
        

    
       
    
    def hide_buttons(self):
        self.main_title.setVisible(False)
        self.our_names.setVisible(False)
        for i in range(1, 8): 
            button = getattr(self, f"Task{i}_button")  
            button.hide()
        self.Return_Button.setVisible(True)
        
    def uncheck_all_checkboxes_and_update_layouts(self):
            self.plot_widgetforTask6.clear_graph6()
            checkboxes = [
                self.PlutoCheckbox1, self.NeptuneCheckbox1, self.UranusCheckbox1,
                self.SaturnCheckbox1, self.JupiterCheckbox1, self.PlutoCheckbox2,
                self.NeptuneCheckbox2, self.UranusCheckbox2, self.MarsCheckbox,
                self.SaturnCheckbox2, self.JupiterCheckbox2, self.EarthCheckbox2, 
                self.EarthCheckbox, self.MercuryCheckbox, self.MarsCheckbox2,
                self.MercuryCheckbox2, self.MarsCheckbox, self.VenusCheckbox,
                self.VenusCheckbox2 ]

            # Temporarily disable autoExclusive
            for checkbox in checkboxes:
                checkbox.setAutoExclusive(False)

            # Uncheck all checkboxes
            for checkbox in checkboxes:
                checkbox.setChecked(False)

            # Re-enable autoExclusive
            for checkbox in checkboxes:
                checkbox.setAutoExclusive(True)

            # Update the layouts
            self.layoutWidget.update()
            self.layoutWidget_2.update() 
            self.layoutWidget3.update()
            self.layoutWidget4.update()


    def uncheck_all_checkboxes_and_update_layouts_task7(self):
            self.plot_widget_task7_3D.clear_graph()
            self.plot_widget_task7.clear_graph()
            checkboxes = [
                self.Pluto_Checkbox, self.Neptune_checkbox, self.Uranus_checkbox,
                self.Saturn_checkbox, self.Jupiter_checkbox, self.Mars_checkbox, 
                self.Earth_checkbox, self.Mercury_checkbox,self.Venus_checkbox ]

            # Temporarily disable autoExclusive
            for checkbox in checkboxes:
                checkbox.setAutoExclusive(False)

            # Uncheck all checkboxes
            for checkbox in checkboxes:
                checkbox.setChecked(False)

            # Re-enable autoExclusive
            for checkbox in checkboxes:
                checkbox.setAutoExclusive(True)

            # Update the layouts
            self.layoutWidget.update()
            self.layoutWidget7.update()
            

    def return_inner_outer(self):
        self.Return_Button.setVisible(True)
        self.OuterPlanetsLabel.setVisible(True)
        self.InnerPlanetsLabel.setVisible(True)
        self.OuterPlanets_Button.setVisible(True)
        self.InnerPlanets_Button.setVisible(True)
        self.Return_Inner_Outer.setVisible(False)
        self.plot_widget2_outer.setVisible(False)
        self.plot_widget2_inner.setVisible(False)
        self.plot_widget3DforInner.setVisible(False)
        self.plot_widget3DforInner.stop_animation3D()
        self.plot_widget3DforOuter.setVisible(False)
        self.plot_widget3DforOuter.stop_animation3D()
        self.plot_widget3_inner.setVisible(False)
        self.plot_widget3_inner.stop_animation()
        self.plot_widget3_outer.setVisible(False)
        self.plot_widget3_outer.stop_animation()
        self.PlotButton.setVisible(False)
        self.label.setVisible(False)
        self.label_2.setVisible(False)
        self.layoutWidget_2.setVisible(False)
        self.layoutWidget3.setVisible(False)
        self.layoutWidget.setVisible(False)
        self.widget.setVisible(False)
        self.layoutWidget4.setVisible(False)
        self.spinBox.setVisible(False)
        self.PlutoCheckbox1.setVisible(False)
        self.PlutoCheckbox2.setVisible(False)
        self.NeptuneCheckbox1.setVisible(False)
        self.NeptuneCheckbox2.setVisible(False)
        self.UranusCheckbox1.setVisible(False)
        self.UranusCheckbox2.setVisible(False)
        self.JupiterCheckbox1.setVisible(False)
        self.JupiterCheckbox2.setVisible(False)
        self.SaturnCheckbox1.setVisible(False)
        self.SaturnCheckbox2.setVisible(False)
        self.EarthCheckbox.setVisible(False)
        self.EarthCheckbox2.setVisible(False)
        self.MarsCheckbox.setVisible(False)
        self.MarsCheckbox2.setVisible(False)
        self.MercuryCheckbox.setVisible(False)
        self.MercuryCheckbox2.setVisible(False)
        self.VenusCheckbox.setVisible(False)
        self.VenusCheckbox2.setVisible(False)
        self.selected_planets.setVisible(False)
        self.plot_widgetforTask6.setVisible(False)
        self.Planet1.setVisible(False)
        self.Planet1_2.setVisible(False)
        self.inner_planets_label.setVisible(False)
        self.spinBox.setValue(1)
        self.spinBox_task7.setValue(1)
        self.spinBox_task7.setVisible(False)
        self.Plot_Button_task7.setVisible(False)
        self.Inner_task7.setVisible(False)
        self.Choose_Centre.setVisible(False)
        self.info_box.setVisible(False)
        self.info_box_2.setVisible(False)
        self.info_box_3.setVisible(False)
        self.info_box_4.setVisible(False)
        self.label_2_task7.setVisible(False)
        self.Plot_3d.setVisible(False)
        self.Earth_checkbox.setVisible(False)
        self.Venus_checkbox.setVisible(False)
        self.Mercury_checkbox.setVisible(False)
        self.Mars_checkbox.setVisible(False)
        self.selected_planet.setVisible(False)
        self.plot_widget_task7.setVisible(False)
        self.plot_widget_task7_3D.setVisible(False)
        self.Jupiter_checkbox.setVisible(False)
        self.Pluto_Checkbox.setVisible(False)
        self.Neptune_checkbox.setVisible(False)
        self.Uranus_checkbox.setVisible(False)
        self.Saturn_checkbox.setVisible(False)
        self.layoutWidget7.setVisible(False)
        self.Outer_task7.setVisible(False)
        self.stopButton.setVisible(False)
        self.main_title.setVisible(False)
        self.our_names.setVisible(False)
        self.startButton.setVisible(False)
        self.ResumeButton.setVisible(False)
        self.ResetButton.setVisible(False)
        
        global inner
        inner = False
        global outer
        outer = False        

        
    def return_button(self):
        global orbit_path_comparison_selected
        global orbit_animation_2d_selected
        global orbit_animation_3d_selected
        global orbit_comparison_selected
        global central_body_orbit_selected
        for i in range(1, 8): 
            button = getattr(self, f"Task{i}_button")  
            button.setVisible(True)
        self.Return_Button.hide()
        self.plot_widget.setVisible(False)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.plot_widgetforTask5.setVisible(False)
        self.main_title.setVisible(True)
        self.our_names.setVisible(True)
        self.eccentricity.setVisible(False)
        self.horizontalSlider.setVisible(False)
        
        
        
        orbit_path_comparison_selected = False
        orbit_animation_2d_selected = False
        orbit_animation_3d_selected = False
        orbit_comparison_selected = False
        central_body_orbit_selected = False
        
        
           
    def show_keplers_third_law(self):
        self.plot_widget.setVisible(True)
        
        
    def Inner_Outer(self):
        self.OuterPlanetsLabel.setVisible(True)
        self.InnerPlanetsLabel.setVisible(True)
        self.OuterPlanets_Button.setVisible(True)
        self.InnerPlanets_Button.setVisible(True)
        
    def show_inner_planet_orbits(self):
        if orbit_path_comparison_selected == True:
            self.Return_Button.hide()
            self.plot_widget2_inner.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
        
    def show_outer_planet_orbits(self):
        if orbit_path_comparison_selected == True:
            self.Return_Button.hide()
            self.plot_widget2_outer.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            
        
        
    def show_inner_orbit_animation(self):
        if orbit_animation_2d_selected == True:
            self.Return_Button.hide()
            self.Return_Inner_Outer.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.plot_widget3_inner.setVisible(True)
            self.stopButton.setVisible(True)
            self.startButton.setVisible(True)
            self.ResumeButton.setVisible(True)
            self.ResetButton.setVisible(True)
            
    def show_outer_orbit_animation(self):
        if orbit_animation_2d_selected == True:
            self.Return_Button.hide()
            self.Return_Inner_Outer.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.plot_widget3_outer.setVisible(True)
            self.stopButton.setVisible(True)
            self.startButton.setVisible(True)
            self.ResumeButton.setVisible(True)
            self.ResetButton.setVisible(True)
        
        
    def show_inner_3d_orbit_animation(self):
        if orbit_animation_3d_selected == True:
            self.Return_Button.hide()
            self.plot_widget3DforInner.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.stopButton.setVisible(True)
            self.startButton.setVisible(True)
            self.ResumeButton.setVisible(True)
            self.ResetButton.setVisible(True)
            
    def show_outer_3d_orbit_animation(self):
        if orbit_animation_3d_selected == True:
            self.Return_Button.hide()
            self.plot_widget3DforOuter.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.stopButton.setVisible(True)
            self.startButton.setVisible(True)
            self.ResumeButton.setVisible(True)
            self.ResetButton.setVisible(True)

    def show_pluto_angular_motion(self):
        self.plot_widgetforTask5.setVisible(True)
        self.horizontalSlider.setVisible(True)
        self.plot_widgetforTask5.update_graph(0.25)
        self.eccentricity.setVisible(True)
        
    def sliderValueChanged(self, value):
        eccentricity = value / 20.0  
        self.plot_widgetforTask5.update_graph(eccentricity)
        
    def show_outer_orbit_comparison(self):
        if orbit_comparison_selected == True:
            self.Return_Button.hide()
            self.PlotButton.setVisible(True)
            self.label.setVisible(True)
            self.label_2.setVisible(True)
            self.layoutWidget.setVisible(True)
            self.layoutWidget_2.setVisible(True)
            self.spinBox.setVisible(True)
            self.PlutoCheckbox1.setVisible(True)
            self.PlutoCheckbox2.setVisible(True)
            self.NeptuneCheckbox1.setVisible(True)
            self.NeptuneCheckbox2.setVisible(True)
            self.UranusCheckbox1.setVisible(True)
            self.UranusCheckbox2.setVisible(True)
            self.JupiterCheckbox1.setVisible(True)
            self.JupiterCheckbox2.setVisible(True)
            self.SaturnCheckbox1.setVisible(True)
            self.SaturnCheckbox2.setVisible(True)
            self.selected_planets.setVisible(True)
            self.plot_widgetforTask6.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.Planet1.setVisible(True)
            self.info_box_3.setVisible(True)
            self.Planet1_2.setVisible(True)
            self.plot_widgetforTask6.clear_graph6()

    def show_inner_orbit_comparison(self):
        if orbit_comparison_selected == True:   
            self.PlotButton.setVisible(True)
            self.label_2.setVisible(True)
            self.layoutWidget3.setVisible(True)
            self.layoutWidget4.setVisible(True)
            self.spinBox.setVisible(True)
            self.EarthCheckbox.setVisible(True)
            self.EarthCheckbox2.setVisible(True)
            self.MarsCheckbox.setVisible(True)
            self.MarsCheckbox2.setVisible(True)
            self.MercuryCheckbox.setVisible(True)
            self.MercuryCheckbox2.setVisible(True)
            self.VenusCheckbox.setVisible(True)
            self.VenusCheckbox2.setVisible(True)
            self.selected_planets.setVisible(True)
            self.inner_planets_label.setVisible(True)
            self.plot_widgetforTask6.setVisible(True)     
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.info_box_4.setVisible(True)
            self.Return_Button.setVisible(False)
            self.Planet1.setVisible(True)
            self.Planet1_2.setVisible(True)
            self.plot_widgetforTask6.clear_graph6()
            
    def check_checkbox_group1(self):
        if self.PlutoCheckbox1.isChecked():
            return "pluto"
        elif self.NeptuneCheckbox1.isChecked():
            return "neptune"
        elif self.UranusCheckbox1.isChecked():
            return "uranus"
        elif self.SaturnCheckbox1.isChecked():
            return "saturn"
        elif self.JupiterCheckbox1.isChecked():
            return "jupiter"
        elif self.MarsCheckbox.isChecked():
            return "mars"
        elif self.EarthCheckbox.isChecked():
            return "earth"
        elif self.VenusCheckbox.isChecked():
            return "venus"
        elif self.MercuryCheckbox.isChecked():
            return "mercury"
        else:
            return "no planet"
        
    def check_checkbox_group2(self):
        if self.PlutoCheckbox2.isChecked():
            return "pluto"
        elif self.NeptuneCheckbox2.isChecked():
            return "neptune"
        elif self.UranusCheckbox2.isChecked():
            return "uranus"
        elif self.SaturnCheckbox2.isChecked():
            return "saturn"
        elif self.JupiterCheckbox2.isChecked():
            return "jupiter"
        elif self.MarsCheckbox2.isChecked():
            return "mars"
        elif self.EarthCheckbox2.isChecked():
            return "earth"
        elif self.VenusCheckbox2.isChecked():
            return "venus"
        elif self.MercuryCheckbox2.isChecked():
            return "mercury"
        else:
            return "no planet"
        
    
       
        
    def plot_orbit_comparison(self):
        
        planet1 = self.check_checkbox_group1()
        planet2 = self.check_checkbox_group2()
        num_orbits = self.spinBox.value()
        num_points = 130 # You can adjust this as needed
        if planet1 == "no planet":
            self.selected_planets.setText("Please select two planets")
        elif planet1 == planet2:
            self.selected_planets.setText("Please select two different planets")
            self.selected_planets.setGeometry(QtCore.QRect(405, 190, 400, 200))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.plot_widgetforTask6.clear_graph6()
         
        elif planet2 == "no planet":   
            self.selected_planets.setText("Please select two planets") 
        else:
             self.selected_planets.setText(" ")
             self.plot_widgetforTask6.plot_data(planet1, planet2, num_orbits, num_points)
    
    def check_checkbox_group7(self):
            if self.Earth_checkbox.isChecked():
                return "earth"
            elif self.Mars_checkbox.isChecked():
                return "mars"
            elif self.Venus_checkbox.isChecked():
                return "venus"
            elif self.Mercury_checkbox.isChecked():
                return "mercury"
            elif self.Jupiter_checkbox.isChecked():
                return "jupiter"
            elif self.Saturn_checkbox.isChecked():
                return "saturn"
            elif self.Uranus_checkbox.isChecked():
                return "uranus"
            elif self.Neptune_checkbox.isChecked():
                return "neptune"
            elif self.Pluto_Checkbox.isChecked():
                return "pluto"
            else:
                return "no planet"
       
        
    def plot_central_body_orbit_2d(self):
        
        self.plot_widget_task7.setVisible(True)
        self.plot_widget_task7_3D.setVisible(False)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()

        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet") 
        else:
          
            self.selected_planet.setText(" ")
            self.plot_widget_task7.plot_data(central_planet, years)

    def plot_central_body_orbit_3d(self):
        
        self.plot_widget_task7.setVisible(False)
        self.plot_widget_task7_3D.setVisible(True)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()

        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet") 
        else:
          
            self.selected_planet.setText(" ")
            self.plot_widget_task7_3D.plot_data3D(central_planet, years)

             



    def show_inner_central_body_orbit_controls(self):
        if central_body_orbit_selected == True:
             self.OuterPlanetsLabel.setVisible(False)
             self.InnerPlanetsLabel.setVisible(False)
             self.OuterPlanets_Button.setVisible(False)
             self.InnerPlanets_Button.setVisible(False)
             self.Return_Inner_Outer.setVisible(True)
             self.Return_Button.setVisible(False)
             self.Plot_Button_task7.setVisible(True)
             self.Inner_task7.setVisible(True)
             self.Choose_Centre.setVisible(True)
             self.label_2_task7.setVisible(True)
             self.Plot_3d.setVisible(True)
             self.Earth_checkbox.setVisible(True)
             self.Venus_checkbox.setVisible(True)
             self.Mercury_checkbox.setVisible(True)
             self.Mars_checkbox.setVisible(True)
             self.selected_planet.setVisible(True)
             self.plot_widget_task7.setVisible(True)
             self.spinBox_task7.setVisible(True)
             self.info_box_2.setVisible(True)
             self.widget.setVisible(True)
             self.plot_widget_task7_3D.clear_graph()

    def show_outer_central_body_orbit_controls(self):
        if central_body_orbit_selected == True:
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.Return_Button.setVisible(False)
            self.Plot_Button_task7.setVisible(True)
            self.Choose_Centre.setVisible(True)
            self.label_2_task7.setVisible(True)
            self.Plot_3d.setVisible(True)
            self.selected_planet.setVisible(True)
            self.plot_widget_task7.setVisible(True)
            self.spinBox_task7.setVisible(True)
            self.Jupiter_checkbox.setVisible(True)
            self.Pluto_Checkbox.setVisible(True)
            self.Neptune_checkbox.setVisible(True)
            self.Uranus_checkbox.setVisible(True)
            self.Saturn_checkbox.setVisible(True)
            self.layoutWidget7.setVisible(True)
            self.Outer_task7.setVisible(True)
            self.info_box.setVisible(True)
            self.plot_widget_task7.clear_graph()
            self.plot_widget_task7_3D.clear_graph()


class PlutoAngleGraphCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#FFFFFF")
        self.fig.set_facecolor((0, 0, 0, 0))
        super(PlutoAngleGraphCanvas, self).__init__(self.fig)
        self.setParent(parent)

    def update_graph(self, eccentricity):
        self.ax.clear()
        # Update graph using the provided eccentricity value
        self.plot_data(eccentricity)
        self.draw()

    def plot_data(self, eccentricity):
        def angle_vs_time(time, Period, eccentricity, theta0):
            dtheta = 1/1000
            N = np.ceil(time[-1] / Period)
            theta = np.arange(theta0, 2 * np.pi * N + theta0, dtheta)
            f = (1 - eccentricity * np.cos(theta)) ** (-2)
            L = len(theta)
            isodd = np.arange(1, L-1) % 2
            isodd[isodd == 1] = 4
            isodd[isodd == 0] = 2
            c = np.concatenate(([1], isodd, [1]))
            constant_factor = Period * ((1 - eccentricity**2)**(3/2)) * (1 / (2 * np.pi)) * dtheta * (1 / 3)
            c_times_f = c * f
            tt = constant_factor * np.cumsum(c_times_f)
            theta_interpolated = interp1d(tt, theta, kind='cubic', fill_value='extrapolate')
            theta = theta_interpolated(time)
            return theta

        time = np.arange(0, 750)
        theta = angle_vs_time(time, 248.348, eccentricity, 0)
        theta2 = angle_vs_time(time, 248.348, 0, 0)

        self.ax.set_xlim([0, 800])
        self.ax.set_ylim([0, 20])
        self.ax.plot(time, theta, color='green', label=f'Eccentricity =  {eccentricity}')
        self.ax.plot(time, theta2, color='blue', label='Eccentricity =  0')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.set_xlabel('time/years')
        self.ax.set_ylabel("orbital polar angle /")
        self.ax.set_title("Orbital angle vs time for pluto", color="white")
        self.ax.spines['left'].set_edgecolor('white')
        self.ax.spines['right'].set_edgecolor('white')
        self.ax.spines['bottom'].set_edgecolor('white')
        self.ax.spines['top'].set_edgecolor('white')
        self.ax.legend()
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.draw()

class OrbitComparisonManager(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use("default")
        plt.xlabel("x/AU", color='black')
        plt.ylabel("y/AU", color='black')
        plt.tick_params(axis='x', colors='black')
        plt.tick_params(axis='y', colors='black')   
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#FFFFFF")
        self.fig.set_facecolor("#181E35")
        super(OrbitComparisonManager, self).__init__(self.fig)
        self.setParent(parent)
        
    def clear_graph6(self):
        self.ax.clear()
        self.draw()

    def show_outer_orbit_comparison(self):
        if orbit_comparison_selected == True:
            self.Return_Button.hide()
            self.PlotButton.setVisible(True)
            self.label.setVisible(True)
            self.label_2.setVisible(True)
            self.layoutWidget.setVisible(True)
            self.layoutWidget_2.setVisible(True)
            self.spinBox.setVisible(True)
            self.PlutoCheckbox1.setVisible(True)
            self.PlutoCheckbox2.setVisible(True)
            self.NeptuneCheckbox1.setVisible(True)
            self.NeptuneCheckbox2.setVisible(True)
            self.UranusCheckbox1.setVisible(True)
            self.UranusCheckbox2.setVisible(True)
            self.JupiterCheckbox1.setVisible(True)
            self.JupiterCheckbox2.setVisible(True)
            self.SaturnCheckbox1.setVisible(True)
            self.SaturnCheckbox2.setVisible(True)
            self.selected_planets.setVisible(True)
            self.plot_widgetforTask6.setVisible(True)
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.Planet1.setVisible(True)
            self.info_box_3.setVisible(True)
            self.Planet1_2.setVisible(True)
            self.plot_widgetforTask6.clear_graph6()

    def show_inner_orbit_comparison(self):
        if orbit_comparison_selected == True:   
            self.PlotButton.setVisible(True)
            self.label_2.setVisible(True)
            self.layoutWidget3.setVisible(True)
            self.layoutWidget4.setVisible(True)
            self.spinBox.setVisible(True)
            self.EarthCheckbox.setVisible(True)
            self.EarthCheckbox2.setVisible(True)
            self.MarsCheckbox.setVisible(True)
            self.MarsCheckbox2.setVisible(True)
            self.MercuryCheckbox.setVisible(True)
            self.MercuryCheckbox2.setVisible(True)
            self.VenusCheckbox.setVisible(True)
            self.VenusCheckbox2.setVisible(True)
            self.selected_planets.setVisible(True)
            self.inner_planets_label.setVisible(True)
            self.plot_widgetforTask6.setVisible(True)     
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.info_box_4.setVisible(True)
            self.Return_Button.setVisible(False)
            self.Planet1.setVisible(True)
            self.Planet1_2.setVisible(True)
            self.plot_widgetforTask6.clear_graph6()
            
        

    def check_checkbox_group1(self):
        if self.PlutoCheckbox1.isChecked():
            return "pluto"
        elif self.NeptuneCheckbox1.isChecked():
            return "neptune"
        elif self.UranusCheckbox1.isChecked():
            return "uranus"
        elif self.SaturnCheckbox1.isChecked():
            return "saturn"
        elif self.JupiterCheckbox1.isChecked():
            return "jupiter"
        elif self.MarsCheckbox.isChecked():
            return "mars"
        elif self.EarthCheckbox.isChecked():
            return "earth"
        elif self.VenusCheckbox.isChecked():
            return "venus"
        elif self.MercuryCheckbox.isChecked():
            return "mercury"
        else:
            return "no planet"
        
    def check_checkbox_group2(self):
        if self.PlutoCheckbox2.isChecked():
            return "pluto"
        elif self.NeptuneCheckbox2.isChecked():
            return "neptune"
        elif self.UranusCheckbox2.isChecked():
            return "uranus"
        elif self.SaturnCheckbox2.isChecked():
            return "saturn"
        elif self.JupiterCheckbox2.isChecked():
            return "jupiter"
        elif self.MarsCheckbox2.isChecked():
            return "mars"
        elif self.EarthCheckbox2.isChecked():
            return "earth"
        elif self.VenusCheckbox2.isChecked():
            return "venus"
        elif self.MercuryCheckbox2.isChecked():
            return "mercury"
        else:
            return "no planet"
        
    
       
        
    def plot_planet_orbit_comparison(self):
        
        planet1 = self.check_checkbox_group1()
        planet2 = self.check_checkbox_group2()
        num_orbits = self.spinBox.value()
        num_points = 130 # You can adjust this as needed
        if planet1 == "no planet":
            self.selected_planets.setText("Please select two planets")
        elif planet1 == planet2:
            self.selected_planets.setText("Please select two different planets")
            self.selected_planets.setGeometry(QtCore.QRect(405, 190, 400, 200))
            self.selected_planets.setStyleSheet("background-color: transparent; border: none; color: black;")
            font = QtGui.QFont()
            font.setPointSize(12)
            self.plot_widgetforTask6.clear_graph6()
         
        elif planet2 == "no planet":   
            self.selected_planets.setText("Please select two planets") 
        else:
             self.selected_planets.setText(" ")
             self.plot_widgetforTask6.plot_data(planet1, planet2, num_orbits, num_points)
    
    def check_checkbox_group7(self):
            if self.Earth_checkbox.isChecked():
                return "earth"
            elif self.Mars_checkbox.isChecked():
                return "mars"
            elif self.Venus_checkbox.isChecked():
                return "venus"
            elif self.Mercury_checkbox.isChecked():
                return "mercury"
            elif self.Jupiter_checkbox.isChecked():
                return "jupiter"
            elif self.Saturn_checkbox.isChecked():
                return "saturn"
            elif self.Uranus_checkbox.isChecked():
                return "uranus"
            elif self.Neptune_checkbox.isChecked():
                return "neptune"
            elif self.Pluto_Checkbox.isChecked():
                return "pluto"
            else:
                return "no planet"
       
        
    def plot_central_body_orbit_2d(self):
        
        self.plot_widget_task7.setVisible(True)
        self.plot_widget_task7_3D.setVisible(False)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()

        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet") 
        else:
          
            self.selected_planet.setText(" ")
            self.plot_widget_task7.plot_data(central_planet, years)

    def plot_central_body_orbit_3d(self):
        
        self.plot_widget_task7.setVisible(False)
        self.plot_widget_task7_3D.setVisible(True)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()

        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet") 
        else:
          
            self.selected_planet.setText(" ")
            self.plot_widget_task7_3D.plot_data3D(central_planet, years)

            



    def show_inner_central_body_orbit_controls(self):
        if central_body_orbit_selected == True:
             self.OuterPlanetsLabel.setVisible(False)
             self.InnerPlanetsLabel.setVisible(False)
             self.OuterPlanets_Button.setVisible(False)
             self.InnerPlanets_Button.setVisible(False)
             self.Return_Inner_Outer.setVisible(True)
             self.Return_Button.setVisible(False)
             self.Plot_Button_task7.setVisible(True)
             self.Inner_task7.setVisible(True)
             self.Choose_Centre.setVisible(True)
             self.label_2_task7.setVisible(True)
             self.Plot_3d.setVisible(True)
             self.Earth_checkbox.setVisible(True)
             self.Venus_checkbox.setVisible(True)
             self.Mercury_checkbox.setVisible(True)
             self.Mars_checkbox.setVisible(True)
             self.selected_planet.setVisible(True)
             self.plot_widget_task7.setVisible(True)
             self.spinBox_task7.setVisible(True)
             self.info_box_2.setVisible(True)
             self.widget.setVisible(True)
             self.plot_widget_task7_3D.clear_graph()

    def show_outer_central_body_orbit_controls(self):
        if central_body_orbit_selected == True:
            self.OuterPlanetsLabel.setVisible(False)
            self.InnerPlanetsLabel.setVisible(False)
            self.OuterPlanets_Button.setVisible(False)
            self.InnerPlanets_Button.setVisible(False)
            self.Return_Inner_Outer.setVisible(True)
            self.Return_Button.setVisible(False)
            self.Plot_Button_task7.setVisible(True)
            self.Choose_Centre.setVisible(True)
            self.label_2_task7.setVisible(True)
            self.Plot_3d.setVisible(True)
            self.selected_planet.setVisible(True)
            self.plot_widget_task7.setVisible(True)
            self.spinBox_task7.setVisible(True)
            self.Jupiter_checkbox.setVisible(True)
            self.Pluto_Checkbox.setVisible(True)
            self.Neptune_checkbox.setVisible(True)
            self.Uranus_checkbox.setVisible(True)
            self.Saturn_checkbox.setVisible(True)
            self.layoutWidget7.setVisible(True)
            self.Outer_task7.setVisible(True)
            self.info_box.setVisible(True)
            self.plot_widget_task7.clear_graph()
            self.plot_widget_task7_3D.clear_graph()
            
        
        
        
class OrbitComparisonCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use("default")
        plt.xlabel("x/AU", color='black')
        plt.ylabel("y/AU", color='black')
        plt.tick_params(axis='x', colors='black')
        plt.tick_params(axis='y', colors='black')   
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#FFFFFF") 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(OrbitComparisonCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
    def clear_graph6(self):
        self.ax.clear()
        self.draw()

 
        


    def plot_data(self, planet1, planet2, num_orbits, num_points):
        self.ax.clear()
        AU = [0.387, 0.723, 1.000, 1.523, 5.20, 9.58, 19.29, 30.25, 39.51]
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'] 
        inner_planets = ['mercury', 'venus', 'earth', 'mars']
        outer_planets = ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']     
        orbital_eccentricities = {
                'mercury': 0.2056,
                'venus': 0.0068,
                'earth': 0.0167,
                'mars': 0.0934,
                'jupiter': 0.0484,
                'saturn': 0.0542,
                'uranus': 0.0472,
                'neptune': 0.0086,
                'pluto': 0.2488
                                }

        # orbital_eccentricities = {
        #         'mercury': 0.5,
        #         'venus': 0.5,
        #         'earth': 0.5,
        #         'mars': 0.5,
        #         'jupiter': 0.5,
        #         'saturn': 0.5,
        #         'uranus': 0.5,
        #         'neptune': 0.5,
        #         'pluto': 0.5
        #                         }
        
        orbital_periods =       {
                'mercury': 0.24,
                'venus': 0.615,
                'earth': 1,
                'mars': 1.88,
                'jupiter': 11.86,
                'saturn': 29.43,
                'uranus': 83.76,
                'neptune': 163.75,
                'pluto': 248
                                 }
        
        planet_colors =          {
                'mercury': 'grey',
                'venus': 'yellow',
                'earth': 'blue',
                'mars': 'red',
                'jupiter': 'red',
                'saturn': 'yellow',
                'uranus': 'cyan',
                'neptune': 'blue',
                'pluto': 'brown'
                                 }
      
      
            

    
        if (planet1 in inner_planets and planet2 in inner_planets) or (planet1 in outer_planets and planet2 in outer_planets):
                distance_planet1 = AU[planets.index(planet1)]
                distance_planet2 = AU[planets.index(planet2)]
                period_planet1 = orbital_periods[planet1]
                period_planet2 = orbital_periods[planet2]

                eccentricity1 = orbital_eccentricities.get(planet1, 0.0)
                eccentricity2 = orbital_eccentricities.get(planet2, 0.0)

                maximum_period = max(period_planet1, period_planet2)
                time_interval = maximum_period / num_points

                theta_planet1 = (2 * np.pi * np.arange(0, num_orbits * period_planet1, time_interval)) / period_planet1
                theta_planet2 = (2 * np.pi * np.arange(0, num_orbits * period_planet2, time_interval)) / period_planet2

                def get_planet_position(Distance, theta, eccentricity):
                    x = distance(Distance, theta, eccentricity) * np.cos(theta)
                    y = distance(Distance, theta, eccentricity) * np.sin(theta)
                    return x, y

              

                planet1_positions = np.array([get_planet_position(distance_planet1, theta, eccentricity1) for theta in theta_planet1])
                planet2_positions = np.array([get_planet_position(distance_planet2, theta, eccentricity2) for theta in theta_planet2])

                orbital_angle = np.radians(np.arange(1000))
                
                self.ax.plot(get_planet_position(distance_planet1, orbital_angle, eccentricity1)[0],
                        get_planet_position(distance_planet1, orbital_angle, eccentricity1)[1],
                        color=planet_colors.get(planet1), label=planet1)

                self.ax.plot(get_planet_position(distance_planet2, orbital_angle, eccentricity2)[0],
                        get_planet_position(distance_planet2, orbital_angle, eccentricity2)[1],
                        color=planet_colors.get(planet2), label=planet2)

                
                for pos1, pos2 in zip(planet1_positions, planet2_positions):
                    self.ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], color='black', alpha=0.2)

                
                self.ax.set_title(f"{planet1} and {planet2} spirograph", color = "white")
                self.ax.set_xlabel('x/AU', color = "white")
                self.ax.set_ylabel('y/AU', color = "white")
                self.ax.xaxis.label.set_color('white')
                self.ax.yaxis.label.set_color('white')
                self.ax.tick_params(axis='x', colors='white')
                self.ax.tick_params(axis='y', colors='white')
                self.ax.axis('equal')
                self.ax.legend(loc = "lower right")
                self.draw()
       
           
           
class CentralBodyOrbitCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use("dark_background")
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        super(CentralBodyOrbitCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
    def clear_graph(self):
        self.ax.clear()
        plt.style.use("dark_background")
        self.draw()

 
        


    def plot_data(self, central_planet, years):
        self.ax.clear()
        time = np.arange(0, years, 0.001)
        inner_planets = ['mercury', 'venus', 'earth', 'mars']
        outer_planets = ["jupiter", "saturn", "uranus", "neptune", "pluto"]
        planet_colors = {
        'mercury': 'grey',
        'venus': 'yellow',
        'earth': 'blue',
        'mars': 'red',
        'jupiter': 'red',
        'saturn': 'yellow',
        'uranus': 'cyan',
        'neptune': 'blue',
        'pluto': 'brown',
        'sun': 'orange'
                         }

        # Parameters for planets
        planet_params = {
            'mercury': (0.387, 0.2056, 0.24),
            'venus': (0.723, 0.0068, 0.62),
            'earth': (1, 0.0167, 1),
            'mars': (1.523, 0.0934, 1.88),
            'jupiter': (5.20, 0.049, 11.86),
            'saturn': (9.58, 0.056, 29.46),
            'uranus': (19.29, 0.046, 84.01),
            'neptune': (30.25, 0.010, 164.8),
            'pluto': (39.51, 0.2488, 248.09),
                                              }

        def coordinates(Distance, eccentricity, period, time, center_planet):
            pi = np.pi
            theta = (2 * pi * time) / period

            x_coordinate = distance_plus(Distance, theta, eccentricity) * np.cos(theta)
            y_coordinate = distance_plus(Distance, theta, eccentricity) * np.sin(theta)
            
            return x_coordinate, y_coordinate
        
        def calculate_relative_positions(planet1, planet2, time):
            planet1_params = planet_params[planet1]
            planet2_params = planet_params[planet2]

            planet1_x, planet1_y = coordinates(*planet1_params, time, planet1)
            planet2_x, planet2_y = coordinates(*planet2_params, time, planet1)

            relative_x = [p1 - p2 for p1, p2 in zip(planet1_x, planet2_x)]
            relative_y = [p1 - p2 for p1, p2 in zip(planet1_y, planet2_y)]

            return relative_x, relative_y
        
        def plot_relative_positions(planet_name, x, y):
            self.ax.plot(x, y, color=planet_colors[planet_name], label=planet_name)

        if central_planet in inner_planets:
            orbiting_planets = inner_planets.copy()
            orbit_label = "Inner Planets"
        else:
            orbiting_planets = outer_planets.copy()
            orbit_label = "Outer Planets"
        
        orbiting_planets.remove(central_planet)   

        centralplanet_x, centralplanet_y = coordinates(*planet_params[central_planet], time, central_planet)


        for orbiting_planet in orbiting_planets:
            orbitingplanet_x, orbitingplanet_y = calculate_relative_positions(central_planet,orbiting_planet, time)
            plot_relative_positions(orbiting_planet, orbitingplanet_x, orbitingplanet_y)

        sun_x, sun_y = centralplanet_x, centralplanet_y
        self.ax.plot(sun_x, sun_y, color=planet_colors['sun'], label='Sun Orbit')

        self.ax.scatter(0, 0, color=planet_colors[central_planet], label=central_planet, s=10)

        self.ax.set_aspect('equal')

        self.ax.set_xlabel('x/AU')
        self.ax.set_ylabel('y/AU')
        self.ax.set_title(f"Orbits of {orbit_label} relative to {central_planet.capitalize()}")
        self.ax.legend(loc='lower right')

        self.draw()    


class CentralBodyOrbit3DCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use("dark_background")
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.ax.grid(color='black')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        super(CentralBodyOrbit3DCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        self.set_dark_background()
    
    def clear_graph(self):
        self.ax.clear()
        plt.style.use("dark_background")
        self.draw()

    def set_dark_background(self):
        
 
        self.ax.xaxis._axinfo["grid"]["color"] = "black"
        self.ax.yaxis._axinfo["grid"]["color"] = "black"
        self.ax.zaxis._axinfo["grid"]["color"] = "black"

        # Set axis colors
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.xaxis.set_pane_color((1, 1, 1, 1))  # Set X-axis pane color to white
        self.ax.yaxis.set_pane_color((1, 1, 1, 1))  # Set Y-axis pane color to white
        self.ax.zaxis.set_pane_color((1, 1, 1, 1))  # Set Z-axis pane color to white
      
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
    
        self.ax.title.set_color('white')
    

    def plot_data3D(self, central_planet, years):
        self.ax.clear()
        inner_planets = ['mercury', 'venus', 'earth', 'mars']
        outer_planets = ["jupiter", "saturn", "uranus", "neptune", "pluto"]
        if central_planet in inner_planets:
            time = np.arange(0, years, 0.001)
        elif central_planet in outer_planets:
            time = np.arange(0, years, 0.01)
        planet_colors = {
        'mercury': 'grey',
        'venus': 'yellow',
        'earth': 'blue',
        'mars': 'red',
        'jupiter': 'red',
        'saturn': 'yellow',
        'uranus': 'cyan',
        'neptune': 'blue',
        'pluto': 'brown',
        'sun': 'orange'
                         }

        planet_params = {
            'mercury': (0.387, 0.2056, 0.24, 7),    # Distance, eccentricity, period (years), inclination (radians)
            'venus': (0.723, 0.0068, 0.62, 3.4),
            'earth': (1, 0.0167, 1, 0),  # Inclination for Earth set to 0
            'mars': (1.523, 0.0934, 1.88, 1.8),
            'jupiter': (5.20, 0.049, 11.86, 1.3),
            'saturn': (9.58, 0.056, 29.46, 2.5),
            'uranus': (19.29, 0.046, 84.01, 0.8),
            'neptune': (30.25, 0.0086, 164.34, 1.8),
            'pluto': (39.51, 0.25, 248.34, 17.2),
                        }   
        def coordinates_3d(Distance, eccentricity, period, inclination):
            pi = np.pi
            inclination = np.deg2rad(inclination)
            theta = (2*pi*time) / period
            
            x_coordinate = []
            y_coordinate = []
            z_coordinate = []
            
            for i in range(len(time)):
                x = distance_task7(Distance, theta[i], eccentricity) * np.cos(theta[i]) * np.cos(inclination)
                x_coordinate.append(x)
            
                y = distance_task7(Distance, theta[i], eccentricity) * np.sin(theta[i])
                y_coordinate.append(y)
                
                z = distance_task7(Distance, theta[i], eccentricity) * np.cos(theta[i]) * np.sin(inclination)
                z_coordinate.append(z)

            return x_coordinate, y_coordinate, z_coordinate

        def calculate_relative_positions_3d(planet1, planet2):
            planet1_params = planet_params[planet1]
            planet2_params = planet_params[planet2]

            planet1_x, planet1_y, planet1_z = coordinates_3d(*planet1_params)
            planet2_x, planet2_y, planet2_z = coordinates_3d(*planet2_params)

            relative_x = [p1 - p2 for p1, p2 in zip(planet1_x, planet2_x)]
            relative_y = [p1 - p2 for p1, p2 in zip(planet1_y, planet2_y)]
            relative_z = [p1 - p2 for p1, p2 in zip(planet1_z, planet2_z)]

            return relative_x, relative_y, relative_z

        def plot_relative_positions_3d(planet_name, x, y, z):
            self.ax.plot3D(x, y, z, color=planet_colors[planet_name], label=planet_name)

    

        if central_planet in inner_planets:
            orbiting_planets = inner_planets.copy()
            orbit_label = "Inner planets"
        elif central_planet in outer_planets:
            orbiting_planets = outer_planets.copy()
            orbit_label = "Outer planets"
        else:
            print("The selected central planet doesn't belong to either inner or outer planets.")
            exit()

        orbiting_planets.remove(central_planet)


        
        self.ax.set_box_aspect(aspect=(1, 1, 0.25))
        self.ax.set_zlim(bottom=-15, top=10)
        self.ax.set_xlabel('x/AU')
        self.ax.set_ylabel('y/AU')
        self.ax.set_zlabel('z/AU')
        self.ax.set_facecolor((0, 0, 0, 0)) 
        self.fig.set_facecolor((0, 0, 0, 0)) 
        sun_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=planet_colors['sun'], markersize=10, label='Sun')
        central_legend = self.ax.scatter(0, 0, color=planet_colors[central_planet], label=central_planet, s=30)
        orbiting_legends = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=planet_colors[planet], markersize=10, label=planet) for planet in orbiting_planets]
        legends = [central_legend] + orbiting_legends
        legends.append(sun_legend)
        self.ax.legend(handles=legends, loc='lower right')
        self.ax.set_title(f"Orbits of {orbit_label} relative to {central_planet.capitalize()}")

        # Plot orbits
        for orbiting_planet in orbiting_planets:
            orbitingplanet_x, orbitingplanet_y, orbitingplanet_z = calculate_relative_positions_3d(
            central_planet, orbiting_planet
            )
            plot_relative_positions_3d(orbiting_planet, orbitingplanet_x, orbitingplanet_y, orbitingplanet_z)

        # Plot the Sun's orbit as a simple circle
        sun_x, sun_y, sun_z = coordinates_3d(*planet_params[central_planet])
        self.ax.plot(sun_x, sun_y, sun_z, color=planet_colors['sun'], label='Sun Orbit')

        # Show plot
        self.draw()


if __name__ == "__main__":
    # Launch the Qt application and open the simulator window.
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
