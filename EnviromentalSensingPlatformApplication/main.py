# Environmental Sensing Platform Application
# By Ethan Barrett
# Last Update: 

# Libraries
import ImportData
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import tkinter.font as font
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
import tk_tools
import time
import MachineLearning as ML

# Global Variables
COMPort = ''
BaudRate = 0
xPres = np.ones(10)
yPres = np.ones(10)
xHumidity = np.ones(10)
yHumidity = np.ones(10)
xTemperature = np.ones(10)
yTemperature = np.ones(10)
xSoilMoisture = np.ones(10)
ySoilMoisture = np.ones(10)
ProcessedData = ['0.0', '0.0', '0.0', '0.0']

TimeBetweenchecks = 1000 #ms

RegressedPressure = np.ones(10)
RegressedHumidity = np.ones(10)
RegressedTemperature = np.ones(10)
RegressedSoilMoisture = np.ones(10)

NextPressure, NextHumidity, NextTemperature, NextSoilMositure = 0,0,0,0

PressurePlotting = np.ones(10)
HumidityPlotting = np.ones(10)
TemperaturePlotting = np.ones(10)
SoilMoisturePlotting = np.ones(10)

PB0, PB1, HB0, HB1, TB0, TB1, SB0, SB1 = 0, 0, 0, 0, 0, 0, 0, 0

##############################################
# LOGIN POPUP
##############################################

SignIn = tk.Tk()
SignIn.geometry("1280x800")
SignIn.title("Sign In")
TitleFont = font.Font(family="Bahnschrift", size=20)
Font = font.Font(family="Bahnschrift", size=14)
SignInLabel = tk.Label(SignIn, text = "Enter Details", font = TitleFont).place(x= 550, y = 200)
EnterCOMPort = tk.Text(SignIn, height=2, width=20)
EnterCOMPort.insert(tk.INSERT, "COM Port")
EnterCOMPort.place(x = 550, y = 300)
EnterBaudRate = tk.Text(SignIn, height=2, width=20)
EnterBaudRate.insert(tk.INSERT, "Baud Rate")
EnterBaudRate.place(x = 550, y = 400)

def RetrieveData():
    global COMPort, BaudRate
    COMPort = EnterCOMPort.get("1.0", "end")
    COMPort = COMPort.strip("\n")
    BaudRate = EnterBaudRate.get("1.0", "end")

    print(COMPort)
    print(BaudRate)

    global COMSYS
    COMSYS = ImportData.GetData(COMPort, BaudRate)

    COMSYS.StartConnection()
    print("Starting COMs")


    SignIn.destroy()

SubmitBtn = tk.Button(SignIn, text="SUBMIT", command=RetrieveData, height = 2,  width=20)
SubmitBtn.place(x = 560,y = 500)    


SignIn.mainloop()

#############################################
# Main Application
#############################################


# Initialisation Code
StartTime = time.time()
mpl.use('TkAgg')

root = tk.Tk()
root.geometry("1280x800")
root.title("Enviromental Sensing Platform")

TitleFont = font.Font(family="Bahnschrift", size=20)
Font = font.Font(family="Bahnschrift", size=14)

TabSys = ttk.Notebook(root)

# Initialise Tabs
Dashboard = ttk.Frame(TabSys)
Predictions = ttk.Frame(TabSys)
Graphs = ttk.Frame(TabSys)

# Add Tabs
TabSys.add(Dashboard, text="Dashboard")
TabSys.add(Graphs, text="Graphs")
TabSys.add(Predictions, text="Predictions")
TabSys.pack(expand=1, fill="both")

OverallPrediction = tk.Label(Predictions, text="")
OverallPrediction.place(x = 500, y = 100)

def ShiftArray(Array):
    TempArray = np.ones(len(Array))

    for x in range(len(Array) - 1):
        TempArray[x] = Array[x+1]
    
    TempArray[-1] = 0

    return TempArray

NullLabel = tk.Label(Dashboard)
GaugeUpdate = tk.Label(Dashboard)


def RetrieveData():
    global COMSYS
    global ProcessedData
    res = COMSYS.readConnection()
    resString = str(res)
    # Remove \r\n
    resString = resString[:-5]
    # Remove b'
    resString = resString[2:]

    print(resString)
    ProcessedData = resString.split(',')
    print(ProcessedData)

    NullLabel.after(TimeBetweenchecks, RetrieveData)


PressureGauge = tk_tools.Gauge(Dashboard, min_value= 0.0, max_value=2000.0, label="Pressure", unit="mBar", divisions= 20, yellow_low= 40, red_low= 30, yellow=60, red= 70) # change values once researched
PressureGauge.place(x = 104, y = 100)

HumidityGauge = tk_tools.Gauge(Dashboard, min_value=0.0, max_value=100.0, label="Humidity", unit="%", divisions= 10, yellow= 70, red = 90) # change values once researched
HumidityGauge.place(x = 398, y = 100)

TemperatureGauge = tk_tools.Gauge(Dashboard, min_value=-50.0, max_value=100.0, label="Temperature", unit="°C", divisions= 15, red_low= 20, yellow_low= 33.33, yellow= 80, red = 86.67) # change values once researched
TemperatureGauge.place(x = 692, y = 100)

SoilMoistureGauge = tk_tools.Gauge(Dashboard, min_value=0.0, max_value=100.0, label="Soil Mositure", unit="%", divisions=10, yellow= 50, red= 90) # change values once researched
SoilMoistureGauge.place(x = 986, y = 100)


def UpdateGauges():
    PressureGauge.set_value(ProcessedData[0])
    HumidityGauge.set_value(ProcessedData[1])
    TemperatureGauge.set_value(ProcessedData[2])
    SoilMoistureGauge.set_value(ProcessedData[3])
    GaugeUpdate.after(TimeBetweenchecks, UpdateGauges)

RetrieveData()
UpdateGauges()

#########################################
# Predictions
#########################################

HiddenLabel = tk.Label(Predictions)

def PressureData():
    global xPres, yPres
    global ProcessedData

    xPres = ShiftArray(xPres)
    yPres = ShiftArray(yPres)

    xPres[-1] = time.time() - StartTime
    yPres[-1] = float(ProcessedData[0])

def HumidityData():
    global xHumidity, yHumidity
    global ProcessedData

    xHumidity = ShiftArray(xHumidity)
    yHumidity = ShiftArray(yHumidity)

    xHumidity[-1] = time.time() - StartTime
    yHumidity[-1] = float(ProcessedData[1])

def TemperatureData():
    global xTemperature, yTemperature
    global ProcessedData

    xTemperature = ShiftArray(xTemperature)
    yTemperature = ShiftArray(yTemperature)

    xTemperature[-1] = time.time() - StartTime
    yTemperature[-1] = float(ProcessedData[2])

def SoilMoistureData():
    global xSoilMoisture, ySoilMoisture
    global ProcessedData

    xSoilMoisture = ShiftArray(xSoilMoisture)
    ySoilMoisture = ShiftArray(ySoilMoisture)

    xSoilMoisture[-1] = time.time() - StartTime
    ySoilMoisture[-1] = float(ProcessedData[3])


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
    Testing = 0
    global xPres, yPres, xHumidity, yHumidity, xTemperature, yTemperature, xSoilMoisture, ySoilMoisture

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

    SoilMoistureDeltaX = xSoilMoisture[-1] - xSoilMoisture[0]
    SoilMoistureDeltaY = ySoilMoisture[-1] - ySoilMoisture[0]
    if SoilMoistureDeltaX == 0.0:
        SoilMoistureGraient = 0.0
    else:
        SoilMoistureGraient = SoilMoistureDeltaY / SoilMoistureDeltaX

    Gradients = CheckGradients(PressureGradient, HumidityGradient, TemperatureGradient, SoilMoistureGraient)


    # [0] = Pressure, [1] = Humidity, [2] = Temperature, [3] = Soil Moisture
    #       NEG             POS             NC                  POS             Rainfall                        Test1
    #       POS             NC              POS                 NEU/NEG         Sunshine                        Test2
    #       NC              NC              NC                  POS             Watering of Soil                Test3
    #       NC              NC              NC                  NEU/NEG         Sunshine                        Test2 (4)
    #       NEG             NEG             NEG                 NEG             Rainfall                        Test5
    #       NEG             NEG             NEG                 POS             Rainfall                        Test6
    #       NEG             NEG             POS                 NEG             Rainfall                        Test7
    #       NEG             POS             NEG                 NEG             Rainfall                        Test8
    #       POS             NEG             NEG                 NEG             Rainfall                        Test9
    #       NEG             NEG             POS                 POS             Rainfall                        Test10
    #       NEG             POS             NEG                 POS             Rainfall                        Test11
    #       POS             NEG             NEG                 POS             Watering of Soil                Test12
    #       NEG             POS             POS                 NEG             Rainfall                        Test13
    #       POS             NEG             POS                 NEG             Sunshine                        Test14
    #       POS             POS             NEG                 NEG             Sunshine                        Test15
    #       NEG             POS             POS                 POS             Rainfall                        Test16
    #       POS             NEG             POS                 POS             Sunshine/Watering of Soil       Test17
    #       POS             POS             NEG                 POS             Sunshine                        Test18
    #       POS             POS             POS                 NEG             Sunshine                        Test19
    #       POS             POS             POS                 POS             Sunshine/Watering of Soil       Test20
    #       NEU             NEU             NEU                 NEU             TESTING                         Test21
    #       !!!              Other combinations                 !!!             Unknown

    
    if ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 5
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 5
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 6
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 6
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 7
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 7
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 8
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 8
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] =='NEG')): # Test 9
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 9
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 10
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 10
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 11
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 11
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 12
        OverallPrediction.config(text = "Soil is being watered")
        Testing = 12
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 13
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 13
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 14
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 14
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 15
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 15
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 16
        OverallPrediction.config(text = "Rainfall is Occuring or will Occur")
        Testing = 16
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 17
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 17
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 18
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 18
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 19
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 19
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 20
        OverallPrediction.config(text = "Sunshine is Occuring or will Occur")
        Testing = 20
    elif((Gradients[0] == 'NEU') and (Gradients[1] == 'NEU') and (Gradients[2] == 'NEU') and (Gradients[3] == 'NEU')): # Test 21
        OverallPrediction.config(text = "TESTING!!!")
        Testing = 21
    #else:
    #    OverallPrediction.config(text = "Unknown Result - Please add to elif Ladder")
    

    OverallPrediction.after(1000, FindGradients)

FindGradients()


def Regress():
    global NextPressure, NextHumidity, NextTemperature, NextSoilMositure
    global RegressedPressure, RegressedHumidity, RegressedTemperature, RegressedSoilMoisture
    global PressurePlotting, HumidityPlotting, TemperaturePlotting, SoilMoisturePlotting
    global xPres, xHumidity, xTemperature, xSoilMoisture
    global PB0, PB1, HB0, HB1, TB0, TB1, SB0, SB1

    RegressPressure = ML.Predict(xPres, yPres)
    RegressHumidity = ML.Predict(xHumidity, yHumidity)
    RegressTemperature = ML.Predict(xTemperature, yTemperature)
    RegressSoilMoisture = ML.Predict(xSoilMoisture, ySoilMoisture)  
    
    # Train Models
    j1 , j2 , PB0, PB1 = RegressPressure.TrainModel()
    j1 , j2 , HB0, HB1 = RegressHumidity.TrainModel()
    j1 , j2 , TB0, TB1 = RegressTemperature.TrainModel()
    j1 , j2 , SB0, SB1 = RegressSoilMoisture.TrainModel()

    for i in range(0, 10):
        PressurePlotting[i] = xPres[i] + 10
        HumidityPlotting[i] = xHumidity[i] + 10
        TemperaturePlotting[i] = xTemperature[i] + 10
        SoilMoisturePlotting[i] = xSoilMoisture[i] + 10

    # Predictions (Single)
    NextPressure = RegressPressure.Predict(PressurePlotting[0])
    NextHumidity = RegressHumidity.Predict(HumidityPlotting[0])
    NextTemperature = RegressTemperature.Predict(TemperaturePlotting[0])
    NextSoilMositure = RegressSoilMoisture.Predict(SoilMoisturePlotting[0])

    # Predictions (Array)
    RegressedPressure = RegressPressure.PredictArray(PressurePlotting)
    RegressedHumidity = RegressHumidity.PredictArray(HumidityPlotting)
    RegressedTemperature = RegressTemperature.PredictArray(TemperaturePlotting)
    RegressedSoilMoisture = RegressSoilMoisture.PredictArray(SoilMoisturePlotting)


    print(RegressedPressure)

def Funcs():
    PressureData()
    HumidityData()
    TemperatureData()
    SoilMoistureData()

    #Regress()

    HiddenLabel.after(TimeBetweenchecks, Funcs)

Funcs()

#############################################################
### Graphing
#############################################################

FigureAll = plt.figure(figsize=(12, 6))

AllPlotP = plt.subplot(221)

AllPlotH = plt.subplot(222)

AllPlotT = plt.subplot(223)

AllPlotSM = plt.subplot(224)

Tab5Display = FigureCanvasTkAgg(FigureAll, master=Graphs)
Tab5Display.get_tk_widget().pack()

PlotHiddenLabel = tk.Label(Graphs)

def PlotPressure(i):
    AllPlotP.cla()

    global PressurePlotting, RegressedPressure, xPres, yPres

    AllPlotP.plot(xPres, yPres)
    AllPlotP.set_title("Pressure (mBar)")

def PlotHumidity(i):
    AllPlotH.cla()

    global HumidityPlotting, RegressedHumidity, xHumidity, yHumidity

    AllPlotH.plot(xHumidity, yHumidity)
    AllPlotH.set_title("Humidity (%)")

def PlotTemp(i):
    AllPlotT.cla()

    global TemperaturePlotting, RegressedTemperature, xTemperature, yTemperature

    AllPlotT.plot(xTemperature, yTemperature)
    AllPlotT.set_title("Temperature (°C)")

def PlotSoMo(i):
    AllPlotSM.cla()

    global SoilMoisturePlotting, RegressedSoilMoisture, xSoilMoisture, ySoilMoisture

    AllPlotSM.plot(xSoilMoisture, ySoilMoisture)
    AllPlotSM.set_title("Soil Moisture (%)")




AnimatePressure = FuncAnimation(FigureAll, PlotPressure, interval = 1000)
AnimateHumidity = FuncAnimation(FigureAll, PlotHumidity, interval = 1000)
AnimateTemperature = FuncAnimation(FigureAll, PlotTemp, interval = 1000)
AnimateSoMo = FuncAnimation(FigureAll, PlotSoMo, interval = 1000)
    
root.mainloop()




