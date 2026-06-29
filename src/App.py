"""
BPhO Computational Challenge 2023 - Main Window
Created by Adam and Dominykas
"""

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

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from TaskOne import KeplerPlotCanvas
from TaskTwo import PlotCanvasForTask2_Inner, PlotCanvasForTask2_Outer, BasePlanetOrbitCanvas
from TaskThree import PlotCanvasforTask3_Inner, PlotCanvasforTask3_Outer, BaseAnimatedOrbitCanvas
from TaskFour import PlotCanvas3DforInner, PlotCanvas3DforOuter, Base3DPlanetCanvas
from TaskFive import PlotCanvasForTask5
from TaskSix import PlotCanvasForTask6
from TaskSeven import PlotCanvasForTask7, PlotCanvasForTask7_3D, BaseRelativeOrbitCanvas

from distance import distance
import os, sys

def resource_path(relative_path):
    """
    Get the absolute path to a resource, relative to the script's location.
    Works both when running normally and when bundled by PyInstaller.
    """
    if getattr(sys, '_MEIPASS', None):
        # PyInstaller extracts files to a temp folder
        base = sys._MEIPASS
    else:
        # Use the directory the script file is actually in
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)
# ---------------------------------------------------------------------------
# Shared stylesheet helpers
# ---------------------------------------------------------------------------

def _make_button_style(name):
    """Return a standard rounded QPushButton stylesheet."""
    return (
        f"QPushButton#{name} {{ border-radius: 40px; background-color: #376991; "
        f"color: white; font-size: 18px; font-weight: bold; }}"
        f"QPushButton#{name}:hover {{ background-color: #95CCE9; }}"
        f"QPushButton#{name}:pressed {{ background-color: #D0DCEC; }}"
    )

def _make_shadow():
    """Return a standard drop-shadow graphics effect."""
    shadow = QtWidgets.QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QtGui.QColor(0, 0, 0, 100))
    shadow.setXOffset(5)
    shadow.setYOffset(5)
    return shadow


# ---------------------------------------------------------------------------
# Main window UI
# ---------------------------------------------------------------------------

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            "QWidget {"
            "  background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.7, fx: 0.5, fy: 0.5,"
            "    stop: 0 #303c6a, stop: 1 #181E35);"
            "  color: #D0DCEC;"
            "}"
        )

        plot1layout = QVBoxLayout(self.centralwidget)

        # ---- Plot canvases (all hidden until a task is selected) ----

        self.plot_widget = KeplerPlotCanvas(self.centralwidget)
        self.plot_widget.setGeometry(QtCore.QRect(120, 50, 600, 500))
        plot1layout.addWidget(self.plot_widget)
        self.plot_widget.hide()

        plt.style.use('dark_background')

        self.plot_widget2_inner = PlotCanvasForTask2_Inner(self.centralwidget)
        self.plot_widget2_inner.setGeometry(QtCore.QRect(120, 50, 600, 500))
        plot1layout.addWidget(self.plot_widget2_inner)
        self.plot_widget2_inner.hide()

        self.plot_widget2_outer = PlotCanvasForTask2_Outer(self.centralwidget)
        self.plot_widget2_outer.setGeometry(QtCore.QRect(129, 40, 661, 611))
        plot1layout.addWidget(self.plot_widget2_outer)
        self.plot_widget2_outer.hide()

        self.plot_widget3_inner = PlotCanvasforTask3_Inner(self.centralwidget)
        self.plot_widget3_inner.setGeometry(QtCore.QRect(65, 2, 661, 611))
        self.plot_widget3_inner.setStyleSheet("background-color: transparent;")
        self.plot_widget3_inner.hide()

        self.plot_widget3_outer = PlotCanvasforTask3_Outer(self.centralwidget)
        self.plot_widget3_outer.setGeometry(QtCore.QRect(65, 2, 661, 611))
        self.plot_widget3_outer.setStyleSheet("background-color: transparent;")
        self.plot_widget3_outer.hide()

        self.plot_widget3DforInner = PlotCanvas3DforInner(self.centralwidget)
        self.plot_widget3DforInner.setGeometry(QtCore.QRect(129, 40, 661, 611))
        plot1layout.addWidget(self.plot_widget3DforInner)
        self.plot_widget3DforInner.setStyleSheet("background-color: transparent;")
        self.plot_widget3DforInner.hide()

        self.plot_widget3DforOuter = PlotCanvas3DforOuter(self.centralwidget)
        self.plot_widget3DforOuter.setGeometry(QtCore.QRect(129, 40, 661, 611))
        plot1layout.addWidget(self.plot_widget3DforOuter)
        self.plot_widget3DforOuter.setStyleSheet("background-color: transparent;")
        self.plot_widget3DforOuter.hide()

        plt.style.use("default")

        self.plot_widgetforTask5 = PlotCanvasForTask5(self.centralwidget)
        self.plot_widgetforTask5.setGeometry(QtCore.QRect(80, 40, 650, 550))
        self.plot_widgetforTask5.setStyleSheet("background-color: transparent;")
        self.plot_widgetforTask5.hide()

        self.plot_widgetforTask6 = PlotCanvasForTask6(self.centralwidget)
        self.plot_widgetforTask6.setGeometry(QtCore.QRect(310, 90, 471, 421))
        self.plot_widgetforTask6.setStyleSheet("background-color: transparent;")
        self.plot_widgetforTask6.hide()

        self.plot_widget_task7 = PlotCanvasForTask7(self.centralwidget)
        self.plot_widget_task7.setGeometry(QtCore.QRect(310, 90, 471, 421))
        self.plot_widget_task7.setStyleSheet("background-color: transparent;")
        self.plot_widget_task7.hide()

        self.plot_widget_task7_3D = PlotCanvasForTask7_3D(self.centralwidget)
        self.plot_widget_task7_3D.setGeometry(QtCore.QRect(310, 90, 471, 421))
        self.plot_widget_task7_3D.setStyleSheet("background-color: transparent;")
        self.plot_widget_task7_3D.hide()

        # ---- Task 5: eccentricity slider ----

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(290, 635, 251, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(19)
        self.horizontalSlider.setValue(5)
        self.horizontalSlider.setStyleSheet("background-color: transparent;")
        self.horizontalSlider.valueChanged.connect(self.sliderValueChanged)
        self.horizontalSlider.hide()

        self.eccentricity = QtWidgets.QLabel(self.centralwidget)
        self.eccentricity.setGeometry(QtCore.QRect(345, 600, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.eccentricity.setFont(font)
        self.eccentricity.setStyleSheet("background-color: transparent; color: white;")
        self.eccentricity.hide()

        # ---- Home screen title and credits ----

        self.main_title = QtWidgets.QLabel(self.centralwidget)
        self.main_title.setGeometry(QtCore.QRect(100, 60, 700, 81))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.main_title.setFont(font)
        self.main_title.setStyleSheet("background-color: transparent; color: #FFFFFF;")

        self.our_names = QtWidgets.QLabel(self.centralwidget)
        self.our_names.setGeometry(QtCore.QRect(560, 650, 300, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.our_names.setFont(font)
        self.our_names.setStyleSheet("background-color: transparent; color: #FFFFFF;")

        # ---- Task selection buttons (home screen) ----
        # Each button hides the home screen and routes to its task.

        self.Task1_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task1_button.setGeometry(QtCore.QRect(60, 220, 300, 81))
        self.Task1_button.setObjectName("Task1_button")
        self.Task1_button.setStyleSheet(_make_button_style("Task1_button"))
        self.Task1_button.setGraphicsEffect(_make_shadow())
        self.Task1_button.clicked.connect(self.hide_buttons)
        self.Task1_button.clicked.connect(self.Task1)

        self.Task2_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task2_button.setGeometry(QtCore.QRect(430, 220, 300, 81))
        self.Task2_button.setObjectName("Task2_button")
        self.Task2_button.setStyleSheet(_make_button_style("Task2_button"))
        self.Task2_button.setGraphicsEffect(_make_shadow())
        self.Task2_button.clicked.connect(self.hide_buttons)
        self.Task2_button.clicked.connect(self.Inner_Outer)
        self.Task2_button.clicked.connect(self.Task2_Clicked)

        self.Task3_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task3_button.setGeometry(QtCore.QRect(60, 320, 300, 81))
        self.Task3_button.setObjectName("Task3_button")
        self.Task3_button.setStyleSheet(_make_button_style("Task3_button"))
        self.Task3_button.setGraphicsEffect(_make_shadow())
        self.Task3_button.clicked.connect(self.hide_buttons)
        self.Task3_button.clicked.connect(self.Inner_Outer)
        self.Task3_button.clicked.connect(self.Task3_Clicked)

        self.Task4_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task4_button.setGeometry(QtCore.QRect(430, 320, 300, 81))
        self.Task4_button.setObjectName("Task4_button")
        self.Task4_button.setStyleSheet(_make_button_style("Task4_button"))
        self.Task4_button.setGraphicsEffect(_make_shadow())
        self.Task4_button.clicked.connect(self.hide_buttons)
        self.Task4_button.clicked.connect(self.Inner_Outer)
        self.Task4_button.clicked.connect(self.Task4_Clicked)

        self.Task5_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task5_button.setGeometry(QtCore.QRect(60, 420, 300, 81))
        self.Task5_button.setObjectName("Task5_button")
        self.Task5_button.setStyleSheet(_make_button_style("Task5_button"))
        self.Task5_button.setGraphicsEffect(_make_shadow())
        self.Task5_button.clicked.connect(self.hide_buttons)
        self.Task5_button.clicked.connect(self.Task5)

        self.Task6_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task6_button.setGeometry(QtCore.QRect(430, 420, 300, 81))
        self.Task6_button.setObjectName("Task6_button")
        self.Task6_button.setStyleSheet(_make_button_style("Task6_button"))
        self.Task6_button.setGraphicsEffect(_make_shadow())
        self.Task6_button.clicked.connect(self.hide_buttons)
        self.Task6_button.clicked.connect(self.Inner_Outer)
        self.Task6_button.clicked.connect(self.Task6_Clicked)

        self.Task7_button = QtWidgets.QPushButton(self.centralwidget)
        self.Task7_button.setGeometry(QtCore.QRect(170, 530, 431, 81))
        self.Task7_button.setObjectName("Task7_button")
        self.Task7_button.setStyleSheet(_make_button_style("Task7_button"))
        self.Task7_button.setGraphicsEffect(_make_shadow())
        self.Task7_button.clicked.connect(self.hide_buttons)
        self.Task7_button.clicked.connect(self.Inner_Outer)
        self.Task7_button.clicked.connect(self.Task7_Clicked)

        # ---- Animation controls (Tasks 3 & 4) ----

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(150, 600, 111, 51))
        self.startButton.setObjectName("startButton")
        self.startButton.setStyleSheet(_make_button_style("startButton"))
        self.startButton.clicked.connect(self.start_animation)
        self.startButton.hide()

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(275, 600, 111, 51))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setStyleSheet(_make_button_style("stopButton"))
        self.stopButton.clicked.connect(self.stop_animation)
        self.stopButton.hide()

        self.ResumeButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResumeButton.setGeometry(QtCore.QRect(400, 600, 111, 51))
        self.ResumeButton.setObjectName("ResumeButton")
        self.ResumeButton.setStyleSheet(_make_button_style("ResumeButton"))
        self.ResumeButton.clicked.connect(self.resume_animation)
        self.ResumeButton.hide()

        self.ResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResetButton.setGeometry(QtCore.QRect(525, 600, 111, 51))
        self.ResetButton.setObjectName("ResetButton")
        self.ResetButton.setStyleSheet(_make_button_style("ResetButton"))
        self.ResetButton.clicked.connect(self.reset_animation)
        self.ResetButton.hide()

        # ---- Navigation buttons ----

        # Returns from a task view back to the home screen
        self.Return_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Return_Button.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Return_Button.setObjectName("Return_Button")
        self.Return_Button.setStyleSheet(_make_button_style("Return_Button"))
        self.Return_Button.clicked.connect(self.return_button)
        self.Return_Button.hide()

        # Returns from a plot back to the inner/outer planet selection screen
        self.Return_Inner_Outer = QtWidgets.QPushButton(self.centralwidget)
        self.Return_Inner_Outer.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Return_Inner_Outer.setObjectName("Return")
        self.Return_Inner_Outer.setStyleSheet(_make_button_style("Return"))
        self.Return_Inner_Outer.clicked.connect(self.uncheck_all_checkboxes_and_update_layouts)
        self.Return_Inner_Outer.clicked.connect(self.uncheck_all_checkboxes_and_update_layouts_task7)
        self.Return_Inner_Outer.clicked.connect(self.return_inner_outer)
        self.Return_Inner_Outer.hide()

        # ---- Inner / outer planet image-buttons ----

        self.InnerPlanets_Button = QtWidgets.QPushButton(self.centralwidget)
        self.InnerPlanets_Button.setGeometry(QtCore.QRect(180, 140, 440, 190))
        self.InnerPlanets_Button.setObjectName("InnerPlanets_Button")
        self.InnerPlanets_Button.setIcon(QIcon(resource_path(r'images\inner.jpg')))
        self.InnerPlanets_Button.setIconSize(self.InnerPlanets_Button.size())
        self.InnerPlanets_Button.clicked.connect(self.Task2_Inner)
        self.InnerPlanets_Button.clicked.connect(self.Task4_Inner)
        self.InnerPlanets_Button.clicked.connect(self.Task3_Inner)
        self.InnerPlanets_Button.clicked.connect(self.Task6_Inner)
        self.InnerPlanets_Button.clicked.connect(self.task7_inner)
        self.InnerPlanets_Button.clicked.connect(self.Inner_clicked)
        self.InnerPlanets_Button.hide()

        self.OuterPlanets_Button = QtWidgets.QPushButton(self.centralwidget)
        self.OuterPlanets_Button.setGeometry(QtCore.QRect(180, 410, 440, 190))
        self.OuterPlanets_Button.setObjectName("OuterPlanets_Button")
        self.OuterPlanets_Button.setIcon(QIcon(resource_path(r'images\outer.png')))
        self.OuterPlanets_Button.setIconSize(self.InnerPlanets_Button.size())
        self.OuterPlanets_Button.clicked.connect(self.Task2_Outer)
        self.OuterPlanets_Button.clicked.connect(self.Task4_Outer)
        self.OuterPlanets_Button.clicked.connect(self.Task3_Outer)
        self.OuterPlanets_Button.clicked.connect(self.Task6_Outer)
        self.OuterPlanets_Button.clicked.connect(self.task7_outer)
        self.OuterPlanets_Button.clicked.connect(self.Outer_clicked)
        self.OuterPlanets_Button.hide()

        self.InnerPlanetsLabel = QtWidgets.QLabel(self.centralwidget)
        self.InnerPlanetsLabel.setGeometry(QtCore.QRect(200, 70, 521, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.InnerPlanetsLabel.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.InnerPlanetsLabel.setFont(font)
        self.InnerPlanetsLabel.hide()

        self.OuterPlanetsLabel = QtWidgets.QLabel(self.centralwidget)
        self.OuterPlanetsLabel.setGeometry(QtCore.QRect(200, 350, 521, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.OuterPlanetsLabel.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.OuterPlanetsLabel.setFont(font)
        self.OuterPlanetsLabel.hide()

        # ---- Outer planet labels shown inside task views ----

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setStyleSheet("background-color: transparent;")
        self.label.setFont(font)
        self.label.hide()

        self.inner_planets_label = QtWidgets.QLabel(self.centralwidget)
        self.inner_planets_label.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.inner_planets_label.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.inner_planets_label.setFont(font)
        self.inner_planets_label.hide()

        # ---- Task 6: outer planet checkbox group (planet 1, left column) ----

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 200, 101, 251))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget.setStyleSheet("background-color: transparent;")
        self.layoutWidget.setFont(font)
        self.layoutWidget.hide()

        self.Checkboxgroup = QtWidgets.QGridLayout(self.layoutWidget)
        self.Checkboxgroup.setContentsMargins(0, 0, 0, 0)

        self.JupiterCheckbox1  = self._make_checkbox(self.layoutWidget, self.Checkboxgroup, row=0, text="Jupiter")
        self.SaturnCheckbox1   = self._make_checkbox(self.layoutWidget, self.Checkboxgroup, row=1, text="Saturn")
        self.UranusCheckbox1   = self._make_checkbox(self.layoutWidget, self.Checkboxgroup, row=2, text="Uranus")
        self.NeptuneCheckbox1  = self._make_checkbox(self.layoutWidget, self.Checkboxgroup, row=3, text="Neptune")
        self.PlutoCheckbox1    = self._make_checkbox(self.layoutWidget, self.Checkboxgroup, row=4, text="Pluto")

        # ---- Task 6: outer planet checkbox group (planet 2, right column) ----

        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(180, 200, 101, 251))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget_2.setStyleSheet("background-color: transparent;")
        self.layoutWidget_2.setFont(font)
        self.layoutWidget_2.hide()

        self.Checkboxgroup_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.Checkboxgroup_2.setContentsMargins(0, 0, 0, 0)

        self.JupiterCheckbox2  = self._make_checkbox(self.layoutWidget_2, self.Checkboxgroup_2, row=0, text="Jupiter")
        self.SaturnCheckbox2   = self._make_checkbox(self.layoutWidget_2, self.Checkboxgroup_2, row=1, text="Saturn")
        self.UranusCheckbox2   = self._make_checkbox(self.layoutWidget_2, self.Checkboxgroup_2, row=2, text="Uranus")
        self.NeptuneCheckbox2  = self._make_checkbox(self.layoutWidget_2, self.Checkboxgroup_2, row=3, text="Neptune")
        self.PlutoCheckbox2    = self._make_checkbox(self.layoutWidget_2, self.Checkboxgroup_2, row=4, text="Pluto")

        # ---- Task 6: inner planet checkbox group (planet 1, left column) ----

        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 200, 101, 251))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget3.setStyleSheet("background-color: transparent;")
        self.layoutWidget3.setFont(font)
        self.layoutWidget3.hide()

        self.Checkboxgroup3 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.Checkboxgroup3.setContentsMargins(0, 0, 0, 0)

        self.MercuryCheckbox = self._make_checkbox(self.layoutWidget3, self.Checkboxgroup3, row=0, text="Mercury")
        self.VenusCheckbox   = self._make_checkbox(self.layoutWidget3, self.Checkboxgroup3, row=1, text="Venus")
        self.EarthCheckbox   = self._make_checkbox(self.layoutWidget3, self.Checkboxgroup3, row=2, text="Earth")
        self.MarsCheckbox    = self._make_checkbox(self.layoutWidget3, self.Checkboxgroup3, row=3, text="Mars")

        # ---- Task 6: inner planet checkbox group (planet 2, right column) ----

        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(180, 200, 101, 251))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.layoutWidget4.setStyleSheet("background-color: transparent;")
        self.layoutWidget4.setFont(font)
        self.layoutWidget4.hide()

        self.Checkboxgroup4 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.Checkboxgroup4.setContentsMargins(0, 0, 0, 0)

        self.MercuryCheckbox2 = self._make_checkbox(self.layoutWidget4, self.Checkboxgroup4, row=0, text="Mercury")
        self.VenusCheckbox2   = self._make_checkbox(self.layoutWidget4, self.Checkboxgroup4, row=1, text="Venus")
        self.EarthCheckbox2   = self._make_checkbox(self.layoutWidget4, self.Checkboxgroup4, row=2, text="Earth")
        self.MarsCheckbox2    = self._make_checkbox(self.layoutWidget4, self.Checkboxgroup4, row=3, text="Mars")

        # ---- Task 6: column header labels and orbit controls ----

        self.Planet1 = QtWidgets.QLabel(self.centralwidget)
        self.Planet1.setGeometry(QtCore.QRect(10, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Planet1.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.Planet1.setFont(font)
        self.Planet1.hide()

        self.Planet1_2 = QtWidgets.QLabel(self.centralwidget)
        self.Planet1_2.setGeometry(QtCore.QRect(170, 160, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Planet1_2.setStyleSheet("background-color: transparent; color: #D0DCEC;")
        self.Planet1_2.setFont(font)
        self.Planet1_2.hide()

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(180, 480, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox.setFont(font)
        self.spinBox.setStyleSheet("background-color: transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.hide()

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 480, 140, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: transparent;")
        self.label_2.hide()

        self.PlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlotButton.setGeometry(QtCore.QRect(470, 520, 141, 51))
        self.PlotButton.setObjectName("PlotButton6")
        self.PlotButton.setStyleSheet(_make_button_style("PlotButton6"))
        self.PlotButton.clicked.connect(self.check_checkbox_group1)
        self.PlotButton.clicked.connect(self.check_checkbox_group2)
        self.PlotButton.clicked.connect(self.plot_task6)
        self.PlotButton.hide()

        self.selected_planets = QtWidgets.QLabel(self.centralwidget)
        self.selected_planets.setGeometry(QtCore.QRect(435, 190, 400, 200))
        self.selected_planets.setStyleSheet("background-color: transparent; border: none; color: black;")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.selected_planets.setFont(font)
        self.selected_planets.setText(" ")
        self.selected_planets.hide()

        # ---- Task 7: 2D/3D plot buttons ----

        self.Plot_Button_task7 = QtWidgets.QPushButton(self.centralwidget)
        self.Plot_Button_task7.setGeometry(QtCore.QRect(370, 530, 151, 51))
        self.Plot_Button_task7.setObjectName("Plot_Button_task7")
        self.Plot_Button_task7.setStyleSheet(_make_button_style("Plot_Button_task7"))
        self.Plot_Button_task7.clicked.connect(self.plot_task7_2D)
        self.Plot_Button_task7.hide()

        self.Plot_3d = QtWidgets.QPushButton(self.centralwidget)
        self.Plot_3d.setGeometry(QtCore.QRect(550, 530, 151, 51))
        self.Plot_3d.setObjectName("Plot_3d")
        self.Plot_3d.setStyleSheet(_make_button_style("Plot_3d"))
        self.Plot_3d.clicked.connect(self.plot_task7_3D)
        self.Plot_3d.hide()

        # ---- Task 7: labels ----

        self.Inner_task7 = QtWidgets.QLabel(self.centralwidget)
        self.Inner_task7.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Inner_task7.setStyleSheet("background-color: transparent;")
        self.Inner_task7.setFont(font)
        self.Inner_task7.hide()

        self.Outer_task7 = QtWidgets.QLabel(self.centralwidget)
        self.Outer_task7.setGeometry(QtCore.QRect(30, 50, 331, 121))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Outer_task7.setStyleSheet("background-color: transparent;")
        self.Outer_task7.setFont(font)
        self.Outer_task7.hide()

        self.Choose_Centre = QtWidgets.QLabel(self.centralwidget)
        self.Choose_Centre.setGeometry(QtCore.QRect(40, 150, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Choose_Centre.setStyleSheet("background-color: transparent;")
        self.Choose_Centre.setFont(font)
        self.Choose_Centre.hide()

        # ---- Orbit count hints ----

        self.info_box = QtWidgets.QLabel(self.centralwidget)
        self.info_box.setGeometry(QtCore.QRect(55, 460, 250, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box.setStyleSheet("background-color: transparent;")
        self.info_box.setFont(font)
        self.info_box.hide()

        self.info_box_2 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_2.setGeometry(QtCore.QRect(55, 460, 250, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_2.setStyleSheet("background-color: transparent;")
        self.info_box_2.setFont(font)
        self.info_box_2.hide()

        self.info_box_3 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_3.setGeometry(QtCore.QRect(30, 520, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_3.setStyleSheet("background-color: transparent;")
        self.info_box_3.setFont(font)
        self.info_box_3.hide()

        self.info_box_4 = QtWidgets.QLabel(self.centralwidget)
        self.info_box_4.setGeometry(QtCore.QRect(30, 520, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_box_4.setStyleSheet("background-color: transparent;")
        self.info_box_4.setFont(font)
        self.info_box_4.hide()

        # ---- Task 7: years spin box ----

        self.label_2_task7 = QtWidgets.QLabel(self.centralwidget)
        self.label_2_task7.setGeometry(QtCore.QRect(60, 430, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2_task7.setFont(font)
        self.label_2_task7.setStyleSheet("background-color: transparent;")
        self.label_2_task7.hide()

        self.spinBox_task7 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_task7.setGeometry(QtCore.QRect(220, 450, 71, 31))
        self.spinBox_task7.setMinimum(1)
        self.spinBox_task7.setMaximum(1000)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox_task7.setFont(font)
        self.spinBox_task7.setStyleSheet("background-color: transparent;")
        self.spinBox_task7.hide()

        # ---- Task 7: inner planet centre-selection checkboxes ----

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 200, 201, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.widget.setFont(font)
        self.widget.setStyleSheet("background-color: transparent;")
        self.widget.setVisible(False)

        self.InnerPlanetGrid = QtWidgets.QGridLayout(self.widget)
        self.InnerPlanetGrid.setContentsMargins(0, 0, 0, 0)

        self.Mercury_checkbox = self._make_checkbox(self.widget, self.InnerPlanetGrid, row=0, text="Mercury", font_size=12)
        self.Venus_checkbox   = self._make_checkbox(self.widget, self.InnerPlanetGrid, row=1, text="Venus",   font_size=12)
        self.Earth_checkbox   = self._make_checkbox(self.widget, self.InnerPlanetGrid, row=2, text="Earth",   font_size=12)
        self.Mars_checkbox    = self._make_checkbox(self.widget, self.InnerPlanetGrid, row=3, text="Mars",    font_size=12)

        self.selected_planet = QtWidgets.QLabel(self.centralwidget)
        self.selected_planet.setGeometry(QtCore.QRect(470, 200, 321, 200))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.selected_planet.setStyleSheet("background-color: transparent; border: none; color: white;")
        self.selected_planet.setFont(font)
        self.selected_planet.setText(" ")
        self.selected_planet.hide()

        # ---- Task 7: outer planet centre-selection checkboxes ----

        self.layoutWidget7 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget7.setGeometry(QtCore.QRect(70, 210, 201, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.layoutWidget7.setStyleSheet("background-color: transparent;")
        self.layoutWidget7.setFont(font)
        self.layoutWidget7.hide()

        self.OuterPlanetGrid = QtWidgets.QGridLayout(self.layoutWidget7)
        self.OuterPlanetGrid.setContentsMargins(0, 0, 0, 0)

        self.Jupiter_checkbox = self._make_checkbox(self.layoutWidget7, self.OuterPlanetGrid, row=0, text="Jupiter", font_size=12)
        self.Saturn_checkbox  = self._make_checkbox(self.layoutWidget7, self.OuterPlanetGrid, row=1, text="Saturn",  font_size=12)
        self.Uranus_checkbox  = self._make_checkbox(self.layoutWidget7, self.OuterPlanetGrid, row=2, text="Uranus",  font_size=12)
        self.Neptune_checkbox = self._make_checkbox(self.layoutWidget7, self.OuterPlanetGrid, row=3, text="Neptune", font_size=12)
        self.Pluto_Checkbox   = self._make_checkbox(self.layoutWidget7, self.OuterPlanetGrid, row=4, text="Pluto",   font_size=12)

        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(plot1layout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # -----------------------------------------------------------------------
    # Helper: create a standard auto-exclusive checkbox inside a grid layout
    # -----------------------------------------------------------------------

    def _make_checkbox(self, parent, grid, row, text, font_size=10):
        cb = QtWidgets.QCheckBox(parent)
        cb.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(font_size)
        cb.setFont(font)
        cb.setStyleSheet("background-color: transparent;")
        cb.setAutoExclusive(True)
        cb.setText(text)
        grid.addWidget(cb, row, 0, 1, 1)
        cb.hide()
        return cb

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Task1_button.setText(_translate("MainWindow", "Task 1"))
        self.Task2_button.setText(_translate("MainWindow", "Task 2"))
        self.Task3_button.setText(_translate("MainWindow", "Task 3"))
        self.Task4_button.setText(_translate("MainWindow", "Task 4"))
        self.Task5_button.setText(_translate("MainWindow", "Task 5"))
        self.Task6_button.setText(_translate("MainWindow", "Task 6"))
        self.Task7_button.setText(_translate("MainWindow", "Task 7"))
        self.main_title.setText(_translate("MainWindow", "BPhO Computational challenge 2023"))
        self.our_names.setText(_translate("MainWindow", "Created by Adam and Dominykas"))
        self.Return_Button.setText(_translate("MainWindow", "Return"))
        self.Return_Inner_Outer.setText(_translate("MainWindow", "Return"))
        self.InnerPlanetsLabel.setText(_translate("MainWindow", "Inner planet orbits"))
        self.OuterPlanetsLabel.setText(_translate("MainWindow", "Outer planet orbits"))
        self.label.setText(_translate("MainWindow", "Outer Planets"))
        self.inner_planets_label.setText(_translate("MainWindow", "Inner Planets"))
        self.Planet1.setText(_translate("MainWindow", "Planet Number 1"))
        self.Planet1_2.setText(_translate("MainWindow", "Planet Number 2"))
        self.label_2.setText(_translate("MainWindow", "Number of Orbits:"))
        self.PlotButton.setText(_translate("MainWindow", "Plot!"))
        self.selected_planets.setText(_translate("MainWindow", ""))
        self.Plot_Button_task7.setText(_translate("MainWindow", "Plot in 2D"))
        self.Plot_3d.setText(_translate("MainWindow", "Plot in 3D"))
        self.Inner_task7.setText(_translate("MainWindow", "Inner Planets"))
        self.Outer_task7.setText(_translate("MainWindow", "Outer Planets"))
        self.Choose_Centre.setText(_translate("MainWindow", "Choose Centre Planet:"))
        self.info_box.setText(_translate("MainWindow", "Recommended number of orbits: 400-600*"))
        self.info_box_2.setText(_translate("MainWindow", "Recommended number of orbits: ~20*"))
        self.info_box_3.setText(_translate("MainWindow", "Recommended number of orbits: 400-600*"))
        self.info_box_4.setText(_translate("MainWindow", "Recommended number of orbits: ~20*"))
        self.label_2_task7.setText(_translate("MainWindow", "Number of Years:"))
        self.selected_planet.setText(_translate("MainWindow", "No Planet selected"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.ResumeButton.setText(_translate("MainWindow", "Resume"))
        self.ResetButton.setText(_translate("MainWindow", "Reset"))
        self.eccentricity.setText(_translate("MainWindow", "Eccentricity"))

    # -----------------------------------------------------------------------
    # Navigation state flags (track which task and planet group is active)
    # -----------------------------------------------------------------------

    Task2_clicked = False
    Task3_clicked = False
    Task4_clicked = False
    Task6_clicked = False
    Task7_clicked = False
    inner = False
    outer = False

    def Task2_Clicked(self): self.Task2_clicked = True
    def Task3_Clicked(self): self.Task3_clicked = True
    def Task4_Clicked(self): self.Task4_clicked = True
    def Task6_Clicked(self): self.Task6_clicked = True
    def Task7_Clicked(self): self.Task7_clicked = True
    def Inner_clicked(self): self.inner = True
    def Outer_clicked(self): self.outer = True

    # -----------------------------------------------------------------------
    # Animation controls (Tasks 3 & 4)
    # -----------------------------------------------------------------------

    def start_animation(self):
        if self.Task3_clicked:
            canvas = self.plot_widget3_inner if self.inner else self.plot_widget3_outer
            canvas.start_animation()
        if self.Task4_clicked:
            canvas = self.plot_widget3DforInner if self.inner else self.plot_widget3DforOuter
            canvas.start_animation()

    def stop_animation(self):
        if self.Task3_clicked:
            canvas = self.plot_widget3_inner if self.inner else self.plot_widget3_outer
            canvas.soft_stop()
        if self.Task4_clicked:
            canvas = self.plot_widget3DforInner if self.inner else self.plot_widget3DforOuter
            canvas.soft_stop()

    def resume_animation(self):
        if self.Task3_clicked:
            canvas = self.plot_widget3_inner if self.inner else self.plot_widget3_outer
            canvas.resume()
        if self.Task4_clicked:
            canvas = self.plot_widget3DforInner if self.inner else self.plot_widget3DforOuter
            canvas.resume()

    def reset_animation(self):
        if self.Task3_clicked:
            canvas = self.plot_widget3_inner if self.inner else self.plot_widget3_outer
            canvas.stop_animation()
        if self.Task4_clicked:
            canvas = self.plot_widget3DforInner if self.inner else self.plot_widget3DforOuter
            canvas.stop_animation()

    # -----------------------------------------------------------------------
    # Home screen navigation
    # -----------------------------------------------------------------------

    def hide_buttons(self):
        """Hide home screen elements and show the Return button."""
        self.main_title.setVisible(False)
        self.our_names.setVisible(False)
        for i in range(1, 8):
            getattr(self, f"Task{i}_button").hide()
        self.Return_Button.setVisible(True)

    def return_button(self):
        """Return from any task view back to the home screen."""
        self.Task2_clicked = self.Task3_clicked = self.Task4_clicked = False
        self.Task6_clicked = self.Task7_clicked = False
        for i in range(1, 8):
            getattr(self, f"Task{i}_button").setVisible(True)
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

    # -----------------------------------------------------------------------
    # Inner/outer planet selection screen
    # -----------------------------------------------------------------------

    def Inner_Outer(self):
        """Show the inner/outer planet image-buttons between a task and its plot."""
        self.OuterPlanetsLabel.setVisible(True)
        self.InnerPlanetsLabel.setVisible(True)
        self.OuterPlanets_Button.setVisible(True)
        self.InnerPlanets_Button.setVisible(True)

    def return_inner_outer(self):
        """Return from a task's plot back to the inner/outer selection screen."""
        self.Return_Button.setVisible(True)
        self.OuterPlanetsLabel.setVisible(True)
        self.InnerPlanetsLabel.setVisible(True)
        self.OuterPlanets_Button.setVisible(True)
        self.InnerPlanets_Button.setVisible(True)
        self.Return_Inner_Outer.setVisible(False)

        # Hide all plot canvases and stop animations
        self.plot_widget2_outer.setVisible(False)
        self.plot_widget2_inner.setVisible(False)
        self.plot_widget3DforInner.setVisible(False)
        self.plot_widget3DforInner.stop_animation()
        self.plot_widget3DforOuter.setVisible(False)
        self.plot_widget3DforOuter.stop_animation()
        self.plot_widget3_inner.setVisible(False)
        self.plot_widget3_inner.stop_animation()
        self.plot_widget3_outer.setVisible(False)
        self.plot_widget3_outer.stop_animation()

        # Hide Task 6 widgets
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

        # Hide Task 7 widgets
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

        # Hide animation controls
        self.main_title.setVisible(False)
        self.our_names.setVisible(False)
        self.startButton.setVisible(False)
        self.stopButton.setVisible(False)
        self.ResumeButton.setVisible(False)
        self.ResetButton.setVisible(False)

        self.inner = False
        self.outer = False

    # -----------------------------------------------------------------------
    # Task 1
    # -----------------------------------------------------------------------

    def Task1(self):
        self.plot_widget.setVisible(True)

    # -----------------------------------------------------------------------
    # Task 2 — static orbit plots
    # -----------------------------------------------------------------------

    def Task2_Inner(self):
        if not self.Task2_clicked:
            return
        self.Return_Button.hide()
        self.plot_widget2_inner.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)

    def Task2_Outer(self):
        if not self.Task2_clicked:
            return
        self.Return_Button.hide()
        self.plot_widget2_outer.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)

    # -----------------------------------------------------------------------
    # Task 3 — animated 2-D orbits
    # -----------------------------------------------------------------------

    def Task3_Inner(self):
        if not self.Task3_clicked:
            return
        self.Return_Button.hide()
        self.Return_Inner_Outer.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.plot_widget3_inner.setVisible(True)
        self.startButton.setVisible(True)
        self.stopButton.setVisible(True)
        self.ResumeButton.setVisible(True)
        self.ResetButton.setVisible(True)

    def Task3_Outer(self):
        if not self.Task3_clicked:
            return
        self.Return_Button.hide()
        self.Return_Inner_Outer.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.plot_widget3_outer.setVisible(True)
        self.startButton.setVisible(True)
        self.stopButton.setVisible(True)
        self.ResumeButton.setVisible(True)
        self.ResetButton.setVisible(True)

    # -----------------------------------------------------------------------
    # Task 4 — animated 3-D orbits
    # -----------------------------------------------------------------------

    def Task4_Inner(self):
        if not self.Task4_clicked:
            return
        self.Return_Button.hide()
        self.plot_widget3DforInner.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)
        self.startButton.setVisible(True)
        self.stopButton.setVisible(True)
        self.ResumeButton.setVisible(True)
        self.ResetButton.setVisible(True)

    def Task4_Outer(self):
        if not self.Task4_clicked:
            return
        self.Return_Button.hide()
        self.plot_widget3DforOuter.setVisible(True)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)
        self.startButton.setVisible(True)
        self.stopButton.setVisible(True)
        self.ResumeButton.setVisible(True)
        self.ResetButton.setVisible(True)

    # -----------------------------------------------------------------------
    # Task 5 — eccentricity explorer
    # -----------------------------------------------------------------------

    def Task5(self):
        self.plot_widgetforTask5.setVisible(True)
        self.horizontalSlider.setVisible(True)
        self.plot_widgetforTask5.update_graph(0.25)
        self.eccentricity.setVisible(True)

    def sliderValueChanged(self, value):
        """Convert integer slider position to eccentricity and redraw."""
        eccentricity = value / 20.0
        self.plot_widgetforTask5.update_graph(eccentricity)

    # -----------------------------------------------------------------------
    # Task 6 — synodic / distance plots
    # -----------------------------------------------------------------------

    def Task6_Outer(self):
        if not self.Task6_clicked:
            return
        self.Return_Button.hide()
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)
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
        self.Planet1.setVisible(True)
        self.Planet1_2.setVisible(True)
        self.info_box_3.setVisible(True)
        self.plot_widgetforTask6.clear_graph6()

    def Task6_Inner(self):
        if not self.Task6_clicked:
            return
        self.Return_Button.setVisible(False)
        self.OuterPlanetsLabel.setVisible(False)
        self.InnerPlanetsLabel.setVisible(False)
        self.OuterPlanets_Button.setVisible(False)
        self.InnerPlanets_Button.setVisible(False)
        self.Return_Inner_Outer.setVisible(True)
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
        self.Planet1.setVisible(True)
        self.Planet1_2.setVisible(True)
        self.info_box_4.setVisible(True)
        self.plot_widgetforTask6.clear_graph6()

    def check_checkbox_group1(self):
        """Return the name of the selected planet in column 1, or 'no planet'."""
        for cb, name in [
            (self.PlutoCheckbox1,   "pluto"),
            (self.NeptuneCheckbox1, "neptune"),
            (self.UranusCheckbox1,  "uranus"),
            (self.SaturnCheckbox1,  "saturn"),
            (self.JupiterCheckbox1, "jupiter"),
            (self.MarsCheckbox,     "mars"),
            (self.EarthCheckbox,    "earth"),
            (self.VenusCheckbox,    "venus"),
            (self.MercuryCheckbox,  "mercury"),
        ]:
            if cb.isChecked():
                return name
        return "no planet"

    def check_checkbox_group2(self):
        """Return the name of the selected planet in column 2, or 'no planet'."""
        for cb, name in [
            (self.PlutoCheckbox2,   "pluto"),
            (self.NeptuneCheckbox2, "neptune"),
            (self.UranusCheckbox2,  "uranus"),
            (self.SaturnCheckbox2,  "saturn"),
            (self.JupiterCheckbox2, "jupiter"),
            (self.MarsCheckbox2,    "mars"),
            (self.EarthCheckbox2,   "earth"),
            (self.VenusCheckbox2,   "venus"),
            (self.MercuryCheckbox2, "mercury"),
        ]:
            if cb.isChecked():
                return name
        return "no planet"

    def plot_task6(self):
        planet1 = self.check_checkbox_group1()
        planet2 = self.check_checkbox_group2()
        num_orbits = self.spinBox.value()
        num_points = 130

        if planet1 == "no planet" or planet2 == "no planet":
            self.selected_planets.setText("Please select two planets")
        elif planet1 == planet2:
            self.selected_planets.setText("Please select two different planets")
            self.selected_planets.setGeometry(QtCore.QRect(405, 190, 400, 200))
            self.plot_widgetforTask6.clear_graph6()
        else:
            self.selected_planets.setText(" ")
            self.plot_widgetforTask6.plot_data(planet1, planet2, num_orbits, num_points)

    # -----------------------------------------------------------------------
    # Task 7 — relative orbit view
    # -----------------------------------------------------------------------

    def check_checkbox_group7(self):
        """Return the name of the selected centre planet for Task 7, or 'no planet'."""
        for cb, name in [
            (self.Earth_checkbox,   "earth"),
            (self.Mars_checkbox,    "mars"),
            (self.Venus_checkbox,   "venus"),
            (self.Mercury_checkbox, "mercury"),
            (self.Jupiter_checkbox, "jupiter"),
            (self.Saturn_checkbox,  "saturn"),
            (self.Uranus_checkbox,  "uranus"),
            (self.Neptune_checkbox, "neptune"),
            (self.Pluto_Checkbox,   "pluto"),
        ]:
            if cb.isChecked():
                return name
        return "no planet"

    def plot_task7_2D(self):
        self.plot_widget_task7.setVisible(True)
        self.plot_widget_task7_3D.setVisible(False)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()
        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet")
        else:
            self.selected_planet.setText(" ")
            self.plot_widget_task7.plot_data(central_planet, years)

    def plot_task7_3D(self):
        self.plot_widget_task7.setVisible(False)
        self.plot_widget_task7_3D.setVisible(True)
        central_planet = self.check_checkbox_group7()
        years = self.spinBox_task7.value()
        if central_planet == "no planet":
            self.selected_planet.setText("Please select a planet")
        else:
            self.selected_planet.setText(" ")
            self.plot_widget_task7_3D.plot_data3D(central_planet, years)

    def task7_inner(self):
        if not self.Task7_clicked:
            return
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

    def task7_outer(self):
        if not self.Task7_clicked:
            return
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

    # -----------------------------------------------------------------------
    # Checkbox reset helpers (called on return from task 6 or 7)
    # -----------------------------------------------------------------------

    def _uncheck_group(self, checkboxes):
        """Temporarily disable autoExclusive so every checkbox can be unchecked."""
        for cb in checkboxes:
            cb.setAutoExclusive(False)
        for cb in checkboxes:
            cb.setChecked(False)
        for cb in checkboxes:
            cb.setAutoExclusive(True)

    def uncheck_all_checkboxes_and_update_layouts(self):
        """Reset all Task 6 checkboxes and clear its graph."""
        self.plot_widgetforTask6.clear_graph6()
        self._uncheck_group([
            self.PlutoCheckbox1, self.NeptuneCheckbox1, self.UranusCheckbox1,
            self.SaturnCheckbox1, self.JupiterCheckbox1, self.PlutoCheckbox2,
            self.NeptuneCheckbox2, self.UranusCheckbox2, self.SaturnCheckbox2,
            self.JupiterCheckbox2, self.EarthCheckbox, self.EarthCheckbox2,
            self.MercuryCheckbox, self.MercuryCheckbox2, self.MarsCheckbox,
            self.MarsCheckbox2, self.VenusCheckbox, self.VenusCheckbox2,
        ])
        self.layoutWidget.update()
        self.layoutWidget_2.update()
        self.layoutWidget3.update()
        self.layoutWidget4.update()

    def uncheck_all_checkboxes_and_update_layouts_task7(self):
        """Reset all Task 7 checkboxes and clear its graphs."""
        self.plot_widget_task7_3D.clear_graph()
        self.plot_widget_task7.clear_graph()
        self._uncheck_group([
            self.Pluto_Checkbox, self.Neptune_checkbox, self.Uranus_checkbox,
            self.Saturn_checkbox, self.Jupiter_checkbox, self.Mars_checkbox,
            self.Earth_checkbox, self.Mercury_checkbox, self.Venus_checkbox,
        ])
        self.layoutWidget.update()
        self.layoutWidget7.update()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    MainWindow.setFixedSize(800, 750) 
    sys.exit(app.exec_())