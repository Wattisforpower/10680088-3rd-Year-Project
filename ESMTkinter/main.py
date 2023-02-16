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
from MachineLearning.MachineLearning import *
#import MachineLearning.TensorflowML as TensorflowML
#import MachineLearning.PyTorch as PyTorch

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
tab6 = ttk.Frame(tabSys)
tab7 = ttk.Frame(tabSys)

# Add Tabs
tabSys.add(tab5, text = 'Overview')
tabSys.add(tab1, text = 'Pressure')
tabSys.add(tab2, text = 'Humidity')
tabSys.add(tab3, text = 'Temperature')
tabSys.add(tab4, text = 'Soil Moisture')
tabSys.add(tab6, text = "Forecasting")
tabSys.add(tab7, text = "Tensor")
tabSys.pack(expand = 1, fill = "both")

# Variables

xPres = np.ones(10)
yPres = np.ones(10)
xHumidity = np.ones(10)
yHumidity = np.ones(10)
xTemperature = np.ones(10)
yTemperature = np.ones(10)
xSoilMositure = np.ones(10)
ySoilMoisture = np.ones(10)

def ShiftArray(Array):
    TempArray = np.ones(len(Array))

    for x in range(len(Array) - 1):
        TempArray[x] = Array[x+1]
    
    TempArray[-1] = 0

    return TempArray

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


# Testing Forecasting Plot
FigureForecast = plt.figure(figsize=(12, 6), facecolor=BkgndClr)
ForecastPressure = plt.subplot(221)
ForecastPressure.set_facecolor(BkgndClr_Graphs)

ForecastHumidity = plt.subplot(222)
ForecastHumidity.set_facecolor(BkgndClr_Graphs)

ForecastTemperature = plt.subplot(223)
ForecastTemperature.set_facecolor(BkgndClr_Graphs)

ForecastSoilMoisture = plt.subplot(224)
ForecastSoilMoisture.set_facecolor(BkgndClr_Graphs)

# TensorFlowTesting
FigureTensor = plt.figure(figsize=(12, 6))
FigureTensorSub = plt.subplot(111)

# ========================================================================================
# Allow for MatplotLib Graphing
# ========================================================================================

Tab5Display = FigureCanvasTkAgg(FigureAll, master=tab5)
Tab5Display.get_tk_widget().pack()

Tab1Display = FigureCanvasTkAgg(FigureP, master=tab1)
Tab1Display.get_tk_widget().pack()

Tab2Display = FigureCanvasTkAgg(FigureH, master=tab2)
Tab2Display.get_tk_widget().pack()

Tab3Display = FigureCanvasTkAgg(FigureT, master=tab3)
Tab3Display.get_tk_widget().pack()

Tab4Display = FigureCanvasTkAgg(FigureSM, master=tab4)
Tab4Display.get_tk_widget().pack()

Tab6Display = FigureCanvasTkAgg(FigureForecast, master=tab6)
Tab6Display.get_tk_widget().pack()

Tab7Display = FigureCanvasTkAgg(FigureTensor, master=tab7)

# ========================================================================================
# Functions
# ========================================================================================

# Pressure

PressureTitleLabel = tk.Label(tab1, text="Pressure: ").pack()
PressureLabel = tk.Label(tab1, text="")
PressureLabel.pack()

def DataGenPressure(i):
    AllPlotP.cla()
    PressurePlot.cla()
    ForecastPressure.cla()
   
    global xPres
    global yPres

    xPres = ShiftArray(xPres)
    yPres = ShiftArray(yPres)

    xPres[-1] = time.time()-StartTime
    yPres[-1] = psutil.cpu_percent()

    PressurePlot.plot(xPres, yPres, color= Pressure_LineClr)
    PressurePlot.set_title("Pressure")
    PressureLabel.config(text=str(yPres[-1]))

    AllPlotP.plot(xPres, yPres, color= Pressure_LineClr)
    AllPlotP.set_title("Pressure")

    # Machine Learning (Regression)

    PredX, PredY, Grad = PressureRegression(xPres, yPres)

    ForecastPressure.plot(PredX, PredY)
    ForecastPressure.set_title("Future Pressure")




# Humidity

HumidityTitleLabel = tk.Label(tab2, text="Humidity: ").pack()
HumidityLabel = tk.Label(tab2, text="")
HumidityLabel.pack()

def DataGenHumidity(i):
    AllPlotH.cla()
    HumidityPlot.cla()

    global xHumidity
    global yHumidity

    xHumidity = ShiftArray(xHumidity)
    yHumidity = ShiftArray(yHumidity)

    xHumidity[-1] = time.time() - StartTime
    yTempVal = psutil.virtual_memory().percent
    yHumidity[-1] = yTempVal

    HumidityPlot.plot(xHumidity, yHumidity, color = Humidity_LineClr)
    HumidityPlot.set_title("Humidity")
    HumidityLabel.config(text=str(yHumidity[-1]))

    AllPlotH.plot(xHumidity, yHumidity, color = Humidity_LineClr)
    AllPlotH.set_title("Humidity")

# Temperature
TemperatureTitleLabel = tk.Label(tab3, text="Temperature: ").pack()
TemperatureLabel = tk.Label(tab3, text="")
TemperatureLabel.pack()

def DataGenTemperature(i):
    AllPlotT.cla()
    TemperaturePlot.cla()

    global xTemperature
    global yTemperature
    
    xTemperature = ShiftArray(xTemperature)
    yTemperature = ShiftArray(yTemperature)

    xTemperature[-1] = time.time() - StartTime
    yTemperature[-1] = psutil.cpu_percent()

    TemperatureLabel.config(text=str(yTemperature[-1]))
    TemperaturePlot.plot(xTemperature, yTemperature, color = Temp_LineClr)
    TemperaturePlot.set_title("Temperature")

    AllPlotT.plot(xTemperature, yTemperature, color = Temp_LineClr)
    AllPlotT.set_title("Temperature")


# Soil Moisture
SoilMoistureTitleLabel = tk.Label(tab4, text="Soil Moisture: ").pack()
SoilMoistureLabel = tk.Label(tab4, text="")
SoilMoistureLabel.pack()

def DataGenSoilMoisture(i):
    AllPlotSM.cla()
    SoilMoisturePlot.cla()

    global xSoilMositure
    global ySoilMoisture
    
    xSoilMositure = ShiftArray(xSoilMositure)
    ySoilMoisture = ShiftArray(ySoilMoisture)

    xSoilMositure[-1] = time.time() - StartTime
    ySoilMoisture[-1] = psutil.virtual_memory().percent

    SoilMoistureLabel.config(text=str(ySoilMoisture[-1]))
    SoilMoisturePlot.plot(xSoilMositure, ySoilMoisture, SoilMoisture_LineClr)
    SoilMoisturePlot.set_title("Soil Moisture")

    AllPlotSM.plot(xSoilMositure, ySoilMoisture, SoilMoisture_LineClr)
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
    PLbl.config(text="Pressure: " + str(yPres[-1]))
    HLbl.config(text="Humidity: " + str(yHumidity[-1]))
    TLbl.config(text="Temperature: " + str(yTemperature[-1]))
    SMLbl.config(text="Soil Moisture: " + str(ySoilMoisture[-1]))

    PLbl.after(1000, UpdateLabels)

UpdateLabels()

# ========================================================================================
# Machine Learning
# ========================================================================================

def PressureRegression(xPres, yPres):

    # Initialise the Prediction
    PressureRegression = Predict(xPres, yPres)

    RegLine, Coeff, C , Grad = PressureRegression.TrainModel()

    Next10XVals = np.ones(10)

    for i in range(10):
        if i == 0:
            Next10XVals[i] = xPres[-1] + 1
        else:
            Next10XVals[i] = Next10XVals[i - 1] + 1
    
    PredictedY = PressureRegression.PredictArray(Next10XVals)

    return Next10XVals, PredictedY, Grad




root.mainloop()