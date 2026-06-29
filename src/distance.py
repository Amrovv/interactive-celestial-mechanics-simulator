import numpy as np

def distance(Distance, theta, eccentricity):
            e = eccentricity
            r = (Distance*(1-e**2))/ (1 - e * np.cos(theta))    
            return r

