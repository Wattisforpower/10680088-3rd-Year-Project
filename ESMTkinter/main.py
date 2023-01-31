# Tkinter

# Import Libraries
import tkinter as tk
from tkinter import ttk
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import collections
from tkinter.ttk import Progressbar

import psutil # Remove when real data is used

# Related Files


# ========================================================================================
# Design Related Code
# ========================================================================================

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

# ========================================================================================
# Init Code
# ========================================================================================

StartTime = time.time()

mpl.use('TkAgg')


root = tk.Tk()

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
# Figures and Plos
# ========================================================================================

# Pressure
FigureP = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
PressurePlot = plt.subplot(111)
PressurePlot.set_facecolor('#DEDEDE')

# Humidity
FigureH = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
HumidityPlot = plt.subplot(111)
HumidityPlot.set_facecolor('#DEDEDE')

# Temperature
FigureT = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
TemperaturePlot = plt.subplot(111)
TemperaturePlot.set_facecolor('#DEDEDE')

# Soil Moisture
FigureSM = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
SoilMoisturePlot = plt.subplot(111)
SoilMoisturePlot.set_facecolor('#DEDEDE')

# Overview
FigureAll = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
plt.suptitle("Data Stream")

AllPlotP = plt.subplot(221)

AllPlotH = plt.subplot(222)

AllPlotT = plt.subplot(223)

AllPlotSM = plt.subplot(224)

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
    PressurePlot.plot(x, y)
    AllPlotP.plot(x, y)
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
    HumidityPlot.plot(xhum, yhum)
    AllPlotH.plot(xhum, yhum)
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
    TemperaturePlot.plot(xTemp, yTemp)
    AllPlotT.plot(xTemp, yTemp)
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
    SoilMoisturePlot.plot(xSM, ySM)
    SoilMoisturePlot.set_title("Soil Moisture")

    AllPlotSM.plot(xSM, ySM)
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

root.mainloop()