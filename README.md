# Interactive Celestial Mechanics Simulator

`BPHO.py` is a PyQt5 desktop application for visualising orbital mechanics and planet motion. It combines a Qt user interface with `matplotlib` plotting to display:

- 2D and 3D orbital paths
- orbit comparison between inner and outer planets
- orbit animations for inner vs outer zones
- Pluto orbital angular motion and eccentricity visualization
- central-body orbit plots for selected planets
- support for Kepler-style orbit calculations and interpolation

## Requirements

- Python 3.x
- PyQt5
- matplotlib
- numpy
- scipy

Install dependencies with pip if needed:

```bash
pip install pyqt5 matplotlib numpy scipy
```

## Run

From the project directory:

```bash
python BPHO.py
```

## Features

- `Ui_MainWindow` builds the main Qt window and application interface
- embedded `matplotlib` canvases are used for plotting and animation
- helper functions compute orbital radii and coordinates for planets
- separate methods handle inner/outer orbit selection, 2D/3D display, and plot updates

## Notes

- The application is intended as an orbital mechanics demonstration and is designed around interactive UI buttons.
- The file includes data for the major planets plus Pluto, including semi-major axes, eccentricities, and orbital periods.
- If the UI fails to start, ensure PyQt5 is installed and the Python environment matches the dependencies.
