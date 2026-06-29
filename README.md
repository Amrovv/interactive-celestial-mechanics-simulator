# Interactive Celestial Mechanics Simulator

An interactive desktop application simulating planetary orbital mechanics, built for the British Physics Olympiad Computational Challenge 2023. Awarded Gold 🏆.

All orbital mechanics are computed analytically using the polar equation of an ellipse, with no physics engine or third-party simulation library. The app was packaged with PyInstaller into a standalone .exe so it runs on any Windows machine without a Python installation.

## Features

Seven competition tasks are accessible from a central menu:

| # | Task | Highlights |
|---|---|---|
| 1 | **Kepler's Third Law** | Plots T vs a³/² for all nine planets, confirming the linear relationship |
| 2 | **Static 2D Orbits** | Elliptical orbits rendered from the polar ellipse equation, Sun at the focus |
| 3 | **Animated 2D Orbits** | Real-time animation with Start / Stop / Resume / Reset controls |
| 4 | **Animated 3D Orbits** | Extends Task 3 with true planetary inclinations and a speed modifier for outer planets |
| 5 | **Orbital Angle vs Time** | Numerically integrates Kepler's Second Law via Simpson's Rule, inverted with a cubic spline; interactive eccentricity slider |
| 6 | **Spirograph Patterns** | Connecting lines between any two planets over user-defined orbits, producing synodic Lissajous patterns |
| 7 | **Relative Orbits** | Re-centres the solar system on any chosen planet; available in both 2D and 3D |

Screenshots

<table>
  <tr>
    <td><img src="assets/screenshots/task1.png" alt="Task 1 - Kepler's Third Law" width="360"/></td>
    <td><img src="assets/screenshots/task2.png" alt="Task 2 - Static 2D Orbits" width="360"/></td>
  </tr>
  <tr>
    <td align="center">Task 1 — Kepler's Third Law</td>
    <td align="center">Task 2 — Static 2D Orbits</td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/task3.png" alt="Task 3 - Animated 2D Orbits" width="360"/></td>
    <td><img src="assets/screenshots/task4.png" alt="Task 4 - Animated 3D Orbits" width="360"/></td>
  </tr>
  <tr>
    <td align="center">Task 3 — Animated 2D Orbits</td>
    <td align="center">Task 4 — Animated 3D Orbits</td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/task5.png" alt="Task 5 - Orbital Angle vs Time" width="360"/></td>
    <td><img src="assets/screenshots/task6.png" alt="Task 6 - Spirograph Patterns" width="360"/></td>
  </tr>
  <tr>
    <td align="center">Task 5 — Orbital Angle vs Time</td>
    <td align="center">Task 6 — Spirograph Patterns</td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/task7.png" alt="Task 7 - Relative Orbits" width="360"/></td>
    <td></td>
  </tr>
  <tr>
    <td align="center">Task 7 — Relative Orbits</td>
    <td></td>
  </tr>
</table>
---

## Features

Seven competition tasks are accessible from a central menu:

| # | Task | Highlights |
|---|---|---|
| 1 | **Kepler's Third Law** | Kepler's Third Law — T vs a³/² for all planets |
| 2 | **Static 2D Orbits** | Static 2D elliptical orbits (inner & outer solar system) |
| 3 | **Animated 2D Orbits** | Animated 2D orbits with Start / Stop / Resume / Reset |
| 4 | **Animated 3D Orbits** | Animated 3D orbits with true orbital inclinations |
| 5 | **Orbital Angle vs Time** | Numerically integrates Kepler's Second Law via Simpson's Rule, inverted with a cubic spline; interactive eccentricity slider |
| 6 | **Spirograph Patterns** | Connecting lines between any two planets over user-defined orbits, producing synodic patterns |
| 7 | **Relative Orbits** | Re-centres the solar system on any chosen planet; available in both 2D and 3D |

---

## Technical Overview

All orbital positions are derived analytically from the polar equation of an ellipse with the Sun at the focus:

```
r(θ) = a(1 − e²) / (1 − e·cos θ)
```

3D coordinates apply each planet's true orbital inclination *i*:

```
x = r·cos(θ)·cos(i),   y = r·sin(θ),   z = r·cos(θ)·sin(i)
```

The codebase uses OOP inheritance throughout — each task's canvas inherits from a shared base class (`FigureCanvasQTAgg`) that handles dark-theme styling, axis setup, and animation lifecycle, keeping task-specific code focused purely on physics logic.

**Stack:** Python · PyQt5 · Matplotlib · NumPy · SciPy · PyInstaller

---

## Getting Started

### Option A — Standalone Executable (no Python required)

Download the latest `.exe` from the [Releases](../../releases) page and run it directly. Built with PyInstaller — no installation needed.

### Option B — Run from Source

```bash
git clone https://github.com/<your-username>/bpho-solar-system-2023.git
cd bpho-solar-system-2023
pip install -r requirements.txt
python src/App.py
```

**requirements.txt**
```
PyQt5>=5.15
matplotlib>=3.5
numpy>=1.21
scipy>=1.7
```

---

## Project Structure

```
bpho-solar-system-2023/
├── src/
│   ├── App.py              # Main window, navigation, and event routing
│   ├── distance.py         # Orbital distance formula r(a, θ, e)
│   ├── PlanetClasses.py    # Planet and Planet3D coordinate generators
│   ├── TaskOne.py          # Kepler's Third Law
│   ├── TaskTwo.py          # Static 2D orbits
│   ├── TaskThree.py        # Animated 2D orbits
│   ├── TaskFour.py         # Animated 3D orbits
│   ├── TaskFive.py         # Orbital angle vs time
│   ├── TaskSix.py          # Spirograph synodic patterns
│   └── TaskSeven.py        # Relative orbits (2D & 3D)
├── images/
│   ├── inner.jpg
│   └── outer.png
├── requirements.txt
└── README.md
```

---

## Authors

Built by **Adam** and **Dominykas** for the BPhO Computational Challenge 2023.
