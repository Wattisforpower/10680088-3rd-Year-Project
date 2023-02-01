# Tkinter

# Import Libraries
import tkinter as tk
from tkinter import ttk
import sched, time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections
from tkinter.ttk import Progressbar
import math

import psutil # Remove when real data is used

# Related Files
from MachineLearning import *

# ========================================================================================
# Design Related Code
# ========================================================================================

'''
# Loading Screen
LoadScrn = tk.Tk()
LoadScrnLabel = tk.Label(LoadScrn, text="Loading...", font = 18).pack()
LoadScrn.geometry("400x400")

LoadScrnProgress = Progressbar(LoadScrn, orient='horizontal', length=200, mode='indeterminate', takefocus=True, maximum=100)
LoadScrnProgress.pack()

LoadScrnProgress.start(interval=None)

for i in range(100):
    LoadScrnProgress.step()
    LoadScrn.update()

def LoadScrnDestroy():
    LoadScrn.destroy()

LoadScrn.after(4000, LoadScrnDestroy)

LoadScrn.mainloop()
'''


# Background Colours
BkgndClr = '#0A75AD'
BkgndClr_Graphs = '#84BAD6'
Pressure_LineClr = '#AD0A75'
Humidity_LineClr = '#AD420A'
Temp_LineClr = '#75AD0A'
SoilMoisture_LineClr = '#301708'



# ========================================================================================
# Init Code
# ========================================================================================

StartTime = time.time()

mpl.use('TkAgg')


root = tk.Tk()
root.geometry("1200x800")

root.title("EnviroSense Module")
tabSys = ttk.Notebook(root)

# Init Tabs
tab1 = ttk.Frame(tabSys)
tab2 = ttk.Frame(tabSys)
tab3 = ttk.Frame(tabSys)
tab4 = ttk.Frame(tabSys)
tab5 = ttk.Frame(tabSys)

# Add Tabs
tabSys.add(tab5, text = 'Overview')
tabSys.add(tab1, text = 'Pressure')
tabSys.add(tab2, text = 'Humidity')
tabSys.add(tab3, text = 'Temperature')
tabSys.add(tab4, text = 'Soil Moisture')
tabSys.pack(expand = 1, fill = "both")

# ========================================================================================
# Figures and Plots
# ========================================================================================

# Pressure
FigureP = plt.figure(figsize=(12, 6), facecolor= BkgndClr)
PressurePlot = plt.subplot(111)
PressurePlot.set_facecolor(BkgndClr_Graphs)

# Humidity
FigureH = plt.figure(figsize=(12, 6), facecolor= BkgndClr)
HumidityPlot = plt.subplot(111)
HumidityPlot.set_facecolor(BkgndClr_Graphs)

# Temperature
FigureT = plt.figure(figsize=(12, 6), facecolor= BkgndClr)
TemperaturePlot = plt.subplot(111)
TemperaturePlot.set_facecolor(BkgndClr_Graphs)

# Soil Moisture
FigureSM = plt.figure(figsize=(12,6), facecolor= BkgndClr)
SoilMoisturePlot = plt.subplot(111)
SoilMoisturePlot.set_facecolor(BkgndClr_Graphs)

# Overview
FigureAll = plt.figure(figsize=(12, 6), facecolor= BkgndClr)
plt.suptitle("Data Stream")

AllPlotP = plt.subplot(221)
AllPlotP.set_facecolor(BkgndClr_Graphs)

AllPlotH = plt.subplot(222)
AllPlotH.set_facecolor(BkgndClr_Graphs)

AllPlotT = plt.subplot(223)
AllPlotT.set_facecolor(BkgndClr_Graphs)

AllPlotSM = plt.subplot(224)
AllPlotSM.set_facecolor(BkgndClr_Graphs)

# ========================================================================================
# Allow for MatplotLib Graphing
# ========================================================================================

Tab5Display = FigureCanvasTkAgg(FigureAll, master=tab5);
Tab5Display.get_tk_widget().pack()

Tab1Display = FigureCanvasTkAgg(FigureP, master=tab1)
Tab1Display.get_tk_widget().pack()

Tab2Display = FigureCanvasTkAgg(FigureH, master=tab2)
Tab2Display.get_tk_widget().pack()

Tab3Display = FigureCanvasTkAgg(FigureT, master=tab3)
Tab3Display.get_tk_widget().pack()

Tab4Display = FigureCanvasTkAgg(FigureSM, master=tab4)
Tab4Display.get_tk_widget().pack()


# ========================================================================================
# Functions
# ========================================================================================

# Pressure
x = collections.deque(np.zeros(10))
y = collections.deque(np.zeros(10))

PressureTitleLabel = tk.Label(tab1, text="Pressure: ").pack()
PressureLabel = tk.Label(tab1, text="")
PressureLabel.pack()

def DataGenPressure(i):
    AllPlotP.cla()
    PressurePlot.cla()
    x.popleft()
    x.append(time.time() - StartTime)

    y.popleft()
    y.append(psutil.cpu_percent())

    PressureLabel.config(text=str(y[-1]))
    PressurePlot.plot(x, y, color= Pressure_LineClr)
    PressurePlot.set_title("Pressure")

    AllPlotP.plot(x, y, color= Pressure_LineClr)
    AllPlotP.set_title("Pressure")

# Humidity
xhum = collections.deque(np.zeros(10))
yhum = collections.deque(np.zeros(10))

HumidityTitleLabel = tk.Label(tab2, text="Humidity: ").pack()
HumidityLabel = tk.Label(tab2, text="")
HumidityLabel.pack()

def DataGenHumidity(i):
    AllPlotH.cla()
    HumidityPlot.cla()
    xhum.popleft()
    xhum.append(time.time() - StartTime)

    yhum.popleft()
    yhum.append(psutil.virtual_memory().percent)

    HumidityLabel.config(text=str(yhum[-1]))
    HumidityPlot.plot(xhum, yhum, color = Humidity_LineClr)
    HumidityPlot.set_title("Humidity")

    AllPlotH.plot(xhum, yhum, color = Humidity_LineClr)
    AllPlotH.set_title("Humidity")

# Temperature
xTemp = collections.deque(np.zeros(10))
yTemp = collections.deque(np.zeros(10))

TemperatureTitleLabel = tk.Label(tab3, text="Temperature: ").pack()
TemperatureLabel = tk.Label(tab3, text="")
TemperatureLabel.pack()

def DataGenTemperature(i):
    AllPlotT.cla()
    TemperaturePlot.cla()
    xTemp.popleft()
    xTemp.append(time.time() - StartTime)

    yTemp.popleft()
    yTemp.append(psutil.cpu_percent())

    TemperatureLabel.config(text=str(yTemp[-1]))
    TemperaturePlot.plot(xTemp, yTemp, color = Temp_LineClr)
    TemperaturePlot.set_title("Temperature")

    AllPlotT.plot(xTemp, yTemp, color = Temp_LineClr)
    AllPlotT.set_title("Temperature")


# Soil Moisture
xSM = collections.deque(np.zeros(10))
ySM = collections.deque(np.zeros(10))

SoilMoistureTitleLabel = tk.Label(tab4, text="Soil Moisture: ").pack()
SoilMoistureLabel = tk.Label(tab4, text="")
SoilMoistureLabel.pack()

def DataGenSoilMoisture(i):
    AllPlotSM.cla()
    SoilMoisturePlot.cla()
    xSM.popleft()
    xSM.append(time.time() - StartTime)

    ySM.popleft()
    ySM.append(psutil.virtual_memory().percent)

    SoilMoistureLabel.config(text=str(ySM[-1]))
    SoilMoisturePlot.plot(xSM, ySM, SoilMoisture_LineClr)
    SoilMoisturePlot.set_title("Soil Moisture")

    AllPlotSM.plot(xSM, ySM, SoilMoisture_LineClr)
    AllPlotSM.set_title("Soil Moisture")

def AllFuncs(i):
    DataGenPressure(i)
    DataGenHumidity(i)
    DataGenTemperature(i)
    DataGenSoilMoisture(i)

# ========================================================================================
# Animate Plots
# ========================================================================================

animateAll = FuncAnimation(FigureAll, AllFuncs, interval = 1000)
animatePressure = FuncAnimation(FigureP, DataGenPressure, interval = 1000)
animateHumidity = FuncAnimation(FigureH, DataGenHumidity, interval = 1000)
animateTemperature = FuncAnimation(FigureT, DataGenTemperature, interval = 1000)
animateSoilMoisture = FuncAnimation(FigureSM, DataGenSoilMoisture, interval = 1000)


# ========================================================================================
# Main Panel (tab5)
# ========================================================================================

MainLbl = tk.Label(tab5, text = "Live Data Stream")
MainLbl.pack()

PLbl = tk.Label(tab5, text="")
PLbl.pack()

HLbl = tk.Label(tab5, text="")
HLbl.pack()

TLbl = tk.Label(tab5, text="")
TLbl.pack()

SMLbl = tk.Label(tab5, text="")
SMLbl.pack()

def UpdateLabels():
    PLbl.config(text="Pressure: " + str(y[-1]))
    HLbl.config(text="Humidity: " + str(yhum[-1]))
    TLbl.config(text="Temperature: " + str(yTemp[-1]))
    SMLbl.config(text="Soil Moisture: " + str(ySM[-1]))

    PLbl.after(1000, UpdateLabels)

UpdateLabels()

# ========================================================================================
# Machine Learning
# ========================================================================================

ML = tk.Label(tab5, text="")
ML.pack()


# REGRESSION

def MachineLearningUpdate(Xval, Yval):
    InitX, InitY = InitXY(Xval, Yval)

    regLine, Coeff, B0, B1 = TrainModel(InitX, InitY)

    PredX = Xval[-1] + 1.0

    Prediction = Predict(B0, B1, PredX)

    return Prediction

def UpdateLabel():
    Prediction = MachineLearningUpdate(x, y)

    ML.config(text = "Pressure Prediction: " + str(Prediction))

    ML.after(1000, UpdateLabel)

#UpdateLabel()



root.mainloop()