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

# Add Tabs
TabSys.add(Dashboard, text="Dashboard")
TabSys.add(Predictions, text="Predictions")
TabSys.pack(expand=1, fill="both")

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

    NullLabel.after(1000, RetrieveData)


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
    GaugeUpdate.after(1000, UpdateGauges)

RetrieveData()
UpdateGauges()

#########################################
# Graphs
#########################################
AllFigures = plt.figure(figsize=(12, 4))
PFig = plt.subplot(141)
HFig = plt.subplot(142)
TFig = plt.subplot(143)
SFig = plt.subplot(144)

DashboardFigures = FigureCanvasTkAgg(AllFigures, master=Dashboard)
DashboardFigures.get_tk_widget.place(x = 104, y = 200)

def PressureData(i):
    global xPres, yPres
    global ProcessedData

    xPres = ShiftArray(xPres)
    yPres = ShiftArray(yPres)

    xPres[-1] = time.time() - StartTime
    yPres[-1] = float(ProcessedData[0])

    PFig.plot(xPres, yPres)

def HumidityData(i):
    global xHumidity, yHumidity
    global ProcessedData

    xHumidity = ShiftArray(xHumidity)
    yHumidity = ShiftArray(yHumidity)

    xHumidity[-1] = time.time() - StartTime
    yHumidity[-1] = float(ProcessedData[[1]])

    HFig.plot(xHumidity, yHumidity)

def Funcs(i):
    PressureData(i)
    HumidityData(i)

PressureAni = FuncAnimation(AllFigures, Funcs, interval = 1000)


root.mainloop()




