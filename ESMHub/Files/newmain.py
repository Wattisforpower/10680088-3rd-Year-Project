# Import Libraries
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

import time

import MachineLearning.Predict as ML

import psutil

root = tk.Tk()
root.title("EnviroSense Module Hub")
root.geometry('1440x720')
mpl.use('TkAgg')

StartTime = time.time()
limit = 40

PressureX = np.ones(limit)
PressureY = np.ones(limit)
HumidityX = np.ones(limit)
HumidityY = np.ones(limit)
TemperatureX = np.ones(limit)
TemperatureY = np.ones(limit)
SoilMositureX = np.ones(limit)
SoilMositureY = np.ones(limit)


PressureGrad = 0
HumidityGrad = 0
TemperatureGrad = 0
SoilMoistureGrad = 0

PlotAll = plt.Figure(figsize=(12, 6), facecolor='#bbbbbb')
PlotAllsp = PlotAll.add_subplot()
PlotAllsp.set_facecolor('#cccccc')

PlotPrediction = plt.Figure(figsize=(12, 6), facecolor='#bbbbbb')
PlotPredictionsp = PlotPrediction.add_subplot()
PlotPredictionsp.set_facecolor('#cccccc')


PressureColour = '#AD0A75'
HumidityColour = '#AD420A'
TemperatureColour = '#75AD0A'
SoilMoistureColour = '#301708'

def ShiftArray(Array):
    ''' FUNCTION TO SHIFT ARRAY LEFT 1'''
    TempArray = np.ones(len(Array))
    for x in range(len(Array) - 1):
        TempArray[x] = Array[x + 1]
        
    TempArray[-1] = 0

    return TempArray

def PressureGen() -> tuple:
    ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR PRESSURE'''
    global PressureX, PressureY

    # Shift array along 1
    PressureX = ShiftArray(PressureX)
    PressureY = ShiftArray(PressureY)

    # Add Latest Data to the end

    PressureX[-1] = time.time() - StartTime
    PressureY[-1] = psutil.cpu_percent()

    # Return Result
    return PressureX, PressureY

def HumidityGen() -> tuple:
    ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR HUMIDITY'''
    global HumidityX, HumidityY

    # Shift array along 1
    HumidityX = ShiftArray(HumidityX)
    HumidityY = ShiftArray(HumidityY)

    # Add Latest Data to the end
    HumidityX[-1] = time.time() - StartTime
    HumidityY[-1] = psutil.virtual_memory().percent

    # Return Result
    return HumidityX, HumidityY

def TemperatureGen() -> tuple:
    ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR TEMPERATURE'''
    global TemperatureX, TemperatureY

    # Shift array along 1
    TemperatureX = ShiftArray(TemperatureX)
    TemperatureY = ShiftArray(TemperatureY)

    # Add Latest Data to the end
    TemperatureX[-1] = time.time() - StartTime
    TemperatureY[-1] = psutil.cpu_percent()

    # Return Result
    return TemperatureX, TemperatureY

def SoilMoistureGen() -> tuple:
    ''' TAKE DAT FROM INPUT AND UPDATE X AND Y FOR SOIL MOISTURE'''
    global SoilMositureX, SoilMositureY

    # Shift array along 1
    SoilMositureX = ShiftArray(SoilMositureX)
    SoilMositureY = ShiftArray(SoilMositureY)

    # Add Latest Data to the end
    SoilMositureX[-1] = time.time() - StartTime
    SoilMositureY[-1] = psutil.virtual_memory().percent
    
    return SoilMositureX, SoilMositureY

def PlotAllFunc(i) -> None:
    '''PLOT DATA'''
    # Clear all figures
    PlotAllsp.cla()

    ### Pressure Section
    Px, Py = PressureGen()
    Hx, Hy = HumidityGen()
    Tx, Ty = TemperatureGen()
    Sx, Sy = SoilMoistureGen()

    print(Px)

    

    PlotAllsp.set_title("Overview")
    PlotAllsp.plot(Px, Py, PressureColour)
    PlotAllsp.plot(Hx, Hy, HumidityColour)
    PlotAllsp.plot(Tx, Ty, TemperatureColour)
    PlotAllsp.plot(Sx, Sy, SoilMoistureColour)

def PlotOnlypressure(i) -> None:
    ''' PLOTS ONLY PRESSURE'''
    # Clear all figures
    PlotAllsp.cla()

    ### Pressure Section
    Px, Py = PressureGen()

    PlotAllsp.set_title("Pressure")
    PlotAllsp.plot(Px, Py, PressureColour)

def PlotOnlyHumidity(i) -> None:
    ''' PLOTS ONLY HUMIDITY'''

    #clear all figures
    PlotAllsp.cla()
    Hx, Hy = HumidityGen()

    PlotAllsp.set_title("Humidity")
    PlotAllsp.plot(Hx, Hy, HumidityColour)

def PlotonlyTemperature(i) -> None:
    ''' PLOTS ONLY TEMPERATURE'''

    PlotAllsp.cla()
    Tx, Ty = TemperatureGen()

    PlotAllsp.set_title("Temperature")
    PlotAllsp.plot(Tx, Ty, TemperatureColour)

def PlotonlySoilMoisutre(i) -> None:
    ''' PLOTS ONLY SOIL MOISUTRE'''

    PlotAllsp.cla()
    Sx, Sy = SoilMoistureGen()

    PlotAllsp.set_title("Soil Moisture")
    PlotAllsp.plot(Sx, Sy, SoilMoistureColour)


DashboardPPlot = FuncAnimation(PlotAll, PlotOnlypressure, interval = 1000)
DashboardHPlot = FuncAnimation(PlotAll, PlotOnlyHumidity, interval = 1000)
DashboardTPlot = FuncAnimation(PlotAll, PlotonlyTemperature, interval = 1000)
DashboardSMPlot = FuncAnimation(PlotAll, PlotonlySoilMoisutre, interval = 1000)
DashboardAllPlot = FuncAnimation(PlotAll, PlotAllFunc, interval = 1000)

def animateplots() -> None:
    DashboardAllPlot.resume()
    DashboardPPlot.pause()
    DashboardHPlot.pause()
    DashboardTPlot.pause()
    DashboardSMPlot.pause()

def animatePplots() -> None:
    DashboardAllPlot.pause()
    DashboardPPlot.resume()
    DashboardHPlot.pause()
    DashboardTPlot.pause()
    DashboardSMPlot.pause()

def animateHplots() -> None:
    DashboardHPlot.resume()
    DashboardAllPlot.pause()
    DashboardPPlot.pause()
    DashboardTPlot.pause()
    DashboardSMPlot.pause()

def animateTplots() -> None:
    DashboardHPlot.pause()
    DashboardAllPlot.pause()
    DashboardPPlot.pause()
    DashboardTPlot.resume()
    DashboardSMPlot.pause()

def animateSMplots() -> None:
    DashboardHPlot.pause()
    DashboardAllPlot.pause()
    DashboardPPlot.pause()
    DashboardTPlot.pause()
    DashboardSMPlot.resume()

def GradCalcs() -> None:
    PlotPredictionsp.cla()
    
    # Calculate Gradients
    
    # Change in Y
    PresDeltaY = PressureY[-1] - PressureY[0]
    HumiDeltaY = HumidityY[-1] - HumidityY[0]
    TempDeltaY = TemperatureY[-1] - TemperatureY[0]
    SoMoDeltaY = SoilMositureY[-1] - SoilMositureY[0]
    
    # Change In X
    PresDeltaX = PressureX[-1] - PressureX[0]
    HumiDeltaX = HumidityX[-1] - HumidityX[0]
    TempDeltaX = TemperatureX[-1] - TemperatureX[0]
    SoMoDeltaX = SoilMositureX[-1] - SoilMositureX[0]

    # Gradient
    PressureGrad = PresDeltaY / PresDeltaX
    HumidityGrad = HumiDeltaY / HumiDeltaX
    TemperatureGrad = TempDeltaY / TempDeltaX
    SoilMoistureGrad = SoMoDeltaY / SoMoDeltaX

# Tabs
Tabs = ttk.Notebook(root)
Dashboard = ttk.Frame(Tabs)
Prediction = ttk.Frame(Tabs)

Tabs.add(Dashboard, text = "Dashboard")
Tabs.add(Prediction, text = "Prediction")
Tabs.pack(expand=1, fill="both")

######### Dashboard #########

# Buttons
DisplayAllBtn = tk.Button(Dashboard, text = "Show All", command = animateplots)
DisplayAllBtn.place(x=50, y=50)

DisplayPressureBtn = tk.Button(Dashboard, text = "Show Pressure", command = animatePplots)
DisplayPressureBtn.place(x=50, y=100)

DisplayHumidityBtn = tk.Button(Dashboard, text = "Show Humidity", command = animateHplots)
DisplayHumidityBtn.place(x=50, y = 150)

DisplayTemperatureBtn = tk.Button(Dashboard, text = "Show Temperature", command = animateTplots)
DisplayTemperatureBtn.place(x = 50, y = 200)

DisplaySMBtn = tk.Button(Dashboard, text = "Show Soil Moisutre", command = animateSMplots)
DisplaySMBtn.place(x = 50, y = 250)


# Figures
DashboardDisplay = FigureCanvasTkAgg(PlotAll, master = Dashboard)
DashboardDisplay.get_tk_widget().place(x = 200, y = 20)

######### Prediction


print(str(PressureGrad))

root.mainloop()
