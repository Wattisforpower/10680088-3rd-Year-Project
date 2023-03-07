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
from tkinter.ttk import Progressbar
import math


import psutil # Remove when real data is used

# Related Files
from MachineLearning.MachineLearning import *
from ImportData import *
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
tabSys.add(tab7, text = "Settings")
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


# ========================================================================================
# Functions
# ========================================================================================

# Pressure

PressureTitleLabel = tk.Label(tab1, text="Pressure: ").pack()
PressureLabel = tk.Label(tab1, text="")
PressureLabel.pack()

NullLabel = tk.Label(tab7)
ProcessedData = ['0.0', '0.0', '0.0', '0.0']

def RetrieveData():
    global SysData
    global ProcessedData
    res = SysData.readConnection()
    resString = str(res)
    # Remove \r\n
    resString = resString[:-5]
    # Remove b'
    resString = resString[2:]

    print(resString)
    ProcessedData = resString.split(',')
    print(ProcessedData)

    NullLabel.after(1000, RetrieveData)


def DataGenPressure(i):
    AllPlotP.cla()
    PressurePlot.cla()
   
    global xPres
    global yPres
    global ProcessedData

    xPres = ShiftArray(xPres)
    yPres = ShiftArray(yPres)

    xPres[-1] = time.time()-StartTime
    yPres[-1] = float(ProcessedData[0])
    #yPres[-1] = psutil.cpu_percent()
    print(yPres[-1])

    PressurePlot.plot(xPres, yPres, color= Pressure_LineClr)
    PressurePlot.set_title("Pressure")
    PressureLabel.config(text=str(yPres[-1]))

    AllPlotP.plot(xPres, yPres, color= Pressure_LineClr)
    AllPlotP.set_title("Pressure")

    




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
    yTempVal = float(ProcessedData[1])
    #yTempVal = psutil.virtual_memory().percent
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
    yTemperature[-1] = float(ProcessedData[2])
    #yTemperature[-1] = psutil.cpu_percent()

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
    ySoilMoisture[-1] = float(ProcessedData[3])
    #ySoilMoisture[-1] = psutil.virtual_memory().percent

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
# Weather Prediction
# ========================================================================================

# Master is tab6

OverallPrediction = tk.Label(tab6, text = "")
OverallPrediction.place(x = 100, y = 100)

def CheckGradients(PG, HG, TG, SMG):
    array = [PG, HG, TG, SMG]
    GradArray = ['','','','']

    if PG > 0:
        GradArray[0] = 'POS'
    elif PG == 0:
        GradArray[0] = 'NEU'
    else:
        GradArray[0] = 'NEG'

    if HG > 0:
        GradArray[1] = 'POS'
    elif HG == 0:
        GradArray[1] = 'NEU'
    else:
        GradArray[1] = 'NEG'

    if TG > 0:
        GradArray[2] = 'POS'
    elif TG == 0:
        GradArray[2] = 'NEU'
    else:
        GradArray[2] = 'NEG'

    if SMG > 0:
        GradArray[3] = 'POS'
    elif SMG == 0:
        GradArray[3] = 'NEU'
    else:
        GradArray[3] = 'NEG'

    
    return GradArray

def FindGradients():
    # DeltaX, DeltaY

    global xPres, yPres, xHumidity, yHumidity, xTemperature, yTemperature, xSoilMositure, ySoilMoisture

    PressureDeltaX = xPres[-1] - xPres[0]
    PressureDeltaY = yPres[-1] - yPres[0]
    if PressureDeltaX == 0.0:
        PressureGradient = 0.0
    else:
        PressureGradient = PressureDeltaY / PressureDeltaX

    HumidityDeltaX = xHumidity[-1] - xHumidity[0]
    HumidityDeltaY = yHumidity[-1] - xHumidity[0]
    if HumidityDeltaX == 0.0:
        HumidityGradient = 0.0
    else:  
        HumidityGradient = HumidityDeltaY / HumidityDeltaX

    TemperatureDeltaX = xTemperature[-1] - xTemperature[0]
    TemperatureDeltaY = yTemperature[-1] - yTemperature[0]
    if TemperatureDeltaX == 0.0:
        TemperatureGradient = 0.0
    else:
        TemperatureGradient = TemperatureDeltaY / TemperatureDeltaX

    SoilMoistureDeltaX = xSoilMositure[-1] - xSoilMositure[0]
    SoilMoistureDeltaY = ySoilMoisture[-1] - ySoilMoisture[0]
    if SoilMoistureDeltaX == 0.0:
        SoilMoistureGraient = 0.0
    else:
        SoilMoistureGraient = SoilMoistureDeltaY / SoilMoistureDeltaX

    Gradients = CheckGradients(PressureGradient, HumidityGradient, TemperatureGradient, SoilMoistureGraient)


    # [0] = Pressure, [1] = Humidity, [2] = Temperature, [3] = Soil Moisture
    #       NEG             POS                                POS           Rainfall
    #       POS                             POS                NEU/NEG       Sunshine
    #       NC              NC              NC                 POS           Watering of Soil

    if ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[3] == 'POS')):
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
    elif ((Gradients[0] == 'POS') and (Gradients[2] == 'POS') and ((Gradients[3] == 'NEU') or (Gradients[3] == 'NEG'))):
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
    elif (Gradients[3] == 'POS'):
        OverallPrediction.config(text = "Soil is being watered")
    elif((Gradients[0] == 'NEU') and (Gradients[1] == 'NEU') and (Gradients[2] == 'NEU') and (Gradients[3] == 'NEU')):
        OverallPrediction.config(text = "TESTING!!!")
    

    OverallPrediction.after(1000, FindGradients)

FindGradients()


# ========================================================================================
# Settings
# ========================================================================================

# tab7
EnterCOMPort = tk.Text(tab7, height=2, width=20)
EnterCOMPort.place(x = 100, y = 20)
EnterBaudRate = tk.Text(tab7, height=2, width=20)
EnterBaudRate.place(x = 100, y = 40)
COMPort = ''
BaudRate = 0


def GetCOMPort():
    global COMPort
    COMPort = EnterCOMPort.get("1.0", "end")
    print(COMPort)
    COMPort = COMPort.strip('\n')

def GetBaudRate():
    global BaudRate
    BaudRate = EnterBaudRate.get("1.0", "end")
    print(BaudRate)

def StartCOMS():
    global COMPort, BaudRate
    global SysData
    SysData = GetData(COMPort, BaudRate)

    SysData.StartConnection()
    print("Starting COMs")

    RetrieveData()



SubmitCOMPort = tk.Button(tab7, text="Submit Port", command=GetCOMPort)
SubmitCOMPort.place(x=280, y=20)
SubmitBaudRate = tk.Button(tab7, text = "Submit BaudRate", command=GetBaudRate)
SubmitBaudRate.place(x=280, y=40)
StartButton = tk.Button(tab7, text = "Start Connection", command=StartCOMS)
StartButton.place(x = 300, y = 300)

root.mainloop()