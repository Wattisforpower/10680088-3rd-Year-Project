# Import Modules
import tkinter as tk
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import psutil

### Initial Code

StartTime = time.time()

root = tk.Tk()
root.geometry("1200x800")
mpl.use('TkAgg')

root.title("EnviroSense Module")
Tabs = ttk.Notebook(root)
Homepage = ttk.Frame(Tabs)
WeatherPrediction = ttk.Frame(Tabs)

Tabs.add(Homepage, text = "Dashboard")
Tabs.add(WeatherPrediction, text = "Weather Prediction")
Tabs.place(x = 400, y = 10)

Limit = 40
PresX = np.ones(Limit)
PresY = np.ones(Limit)
HumiX = np.ones(Limit)
HumiY = np.ones(Limit)
TempX = np.ones(Limit)
TempY = np.ones(Limit)
SoMoX = np.ones(Limit)
SoMoY = np.ones(Limit)

OverviewPlot = plt.figure(figsize=(12, 6), facecolor='#bbbbbb')
OverviewSubPlot = OverviewPlot.add_subplot(111)
OverviewSubPlot.set_facecolor('#cccccc')
DashboardDisplay = FigureCanvasTkAgg(OverviewPlot, master = Homepage)
DashboardDisplay.get_tk_widget().place(x = 200, y = 20)

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
    global PresX
    global PresY


    # Shift array along 1
    PresX = ShiftArray(PresX)
    PresY = ShiftArray(PresY)

    # Add Latest Data to the end

    PresX[-1] = time.time() - StartTime
    PresY[-1] = psutil.cpu_percent()

    # Return Result
    return PresX, PresY

def HumidityGen() -> tuple:
    ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR HUMIDITY'''
    global HumiX
    global HumiY


    # Shift array along 1
    HumiX = ShiftArray(HumiX)
    HumiY = ShiftArray(HumiY)

    # Add Latest Data to the end
    HumiX[-1] = time.time() - StartTime
    HumiY[-1] = psutil.virtual_memory().percent

    # Return Result
    return HumiX, HumiY

def TemperatureGen() -> tuple:
    ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR TEMPERATURE'''
    global TempX
    global TempY

    # Shift array along 1
    TempX = ShiftArray(TempX)
    TempY = ShiftArray(TempY)

    # Add Latest Data to the end
    TempX[-1] = time.time() - StartTime
    TempY[-1] = psutil.cpu_percent()

    # Return Result
    return TempX, TempY

def SoilMoistureGen() -> tuple:
    ''' TAKE DAT FROM INPUT AND UPDATE X AND Y FOR SOIL MOISTURE'''
    global SoMoX
    global SoMoY

    # Shift array along 1
    SoMoX = ShiftArray(SoMoX)
    SoMoY = ShiftArray(SoMoY)

    # Add Latest Data to the end
    SoMoX[-1] = time.time() - StartTime
    SoMoY[-1] = psutil.virtual_memory().percent
    
    return SoMoX, SoMoY

def PlotAllFunc(i) -> None:
    '''PLOT DATA'''
    # Clear all figures
    OverviewSubPlot.cla()

    ### Pressure Section
    Px, Py = PressureGen()
    Hx, Hy = HumidityGen()
    Tx, Ty = TemperatureGen()
    Sx, Sy = SoilMoistureGen()

    print(Px)

    OverviewSubPlot.set_title("Overview")
    OverviewSubPlot.plot(Px, Py, PressureColour)
    OverviewSubPlot.plot(Hx, Hy, HumidityColour)
    OverviewSubPlot.plot(Tx, Ty, TemperatureColour)
    OverviewSubPlot.plot(Sx, Sy, SoilMoistureColour)

DashboardPlot = FuncAnimation(OverviewPlot, PlotAllFunc, interval = 1000)


root.mainloop()
