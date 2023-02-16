# 10680088 Project code for the GUI for the EnviroSense Module

# Import Documents
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

import time

import psutil

# 6 Pages of the document with each page being as follows:
# Page 1 - Dashboard
# Page 2 - 5 - Prediction
# Page 6 - About GUI

###############################################################
# Generations of Data
###############################################################

class DataGenandStats:
    def __init__ (self):
        self.StartTime = time.time()

        ''' GLOBAL DATA'''
        self.limit = 10

        self.PressureX = np.ones(self.limit)
        self.PressureY = np.ones(self.limit)
        self.HumidityX = np.ones(self.limit)
        self.HumidityY = np.ones(self.limit)
        self.TemperatureX = np.ones(self.limit)
        self.TemperatureY = np.ones(self.limit)
        self.SoilMositureX = np.ones(self.limit)
        self.SoilMositureY = np.ones(self.limit)

        self.PlotAll = plt.Figure(figsize=(12, 6), facecolor='#bbbbbb')
        self.PlotAllsp = self.PlotAll.add_subplot()
        self.PlotAllsp.set_facecolor('#cccccc')

        self.PressureColour = '#AD0A75'
        self.HumidityColour = '#AD420A'
        self.TemperatureColour = '#75AD0A'
        self.SoilMoistureColour = '#301708'
        


    def ShiftArray(self, Array):
        ''' FUNCTION TO SHIFT ARRAY LEFT 1'''
        TempArray = np.ones(len(Array))
        for x in range(len(Array) - 1):
            TempArray[x] = Array[x + 1]
        
        TempArray[-1] = 0

        return TempArray

    def PressureGen(self) -> tuple:
        ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR PRESSURE'''


        # Shift array along 1
        self.PressureX = DataGenandStats.ShiftArray(self, self.PressureX)
        self.PressureY = DataGenandStats.ShiftArray(self, self.PressureY)

        # Add Latest Data to the end

        self.PressureX[-1] = time.time() - self.StartTime
        self.PressureY[-1] = psutil.cpu_percent()

        # Return Result
        return self.PressureX, self.PressureY
    
    def HumidityGen(self) -> tuple:
        ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR HUMIDITY'''

        # Shift array along 1
        self.HumidityX = DataGenandStats.ShiftArray(self, self.HumidityX)
        self.HumidityY = DataGenandStats.ShiftArray(self, self.HumidityY)

        # Add Latest Data to the end
        self.HumidityX[-1] = time.time() - self.StartTime
        self.HumidityY[-1] = psutil.virtual_memory().percent

        # Return Result
        return self.HumidityX, self.HumidityY
    
    def TemperatureGen(self) -> tuple:
        ''' TAKE DATA FROM INPUT AND UPDATE X AND Y FOR TEMPERATURE'''

        # Shift array along 1
        self.TemperatureX = DataGenandStats.ShiftArray(self, self.TemperatureX)
        self.TemperatureY = DataGenandStats.ShiftArray(self, self.TemperatureY)

        # Add Latest Data to the end
        self.TemperatureX[-1] = time.time() - self.StartTime
        self.TemperatureY[-1] = psutil.cpu_percent()

        # Return Result
        return self.TemperatureX, self.TemperatureY
    
    def SoilMoistureGen(self) -> tuple:
        ''' TAKE DAT FROM INPUT AND UPDATE X AND Y FOR SOIL MOISTURE'''

        # Shift array along 1
        self.SoilMositureX = DataGenandStats.ShiftArray(self, self.SoilMositureX)
        self.SoilMositureY = DataGenandStats.ShiftArray(self, self.SoilMositureY)

        # Add Latest Data to the end
        self.SoilMositureX[-1] = time.time() - self.StartTime
        self.SoilMositureY[-1] = psutil.virtual_memory().percent
        
        return self.SoilMositureX, self.SoilMositureY

    def PlotAllFunc(self, i) -> None:
        '''PLOT DATA'''
        # Clear all figures
        self.PlotAllsp.cla()

        ### Pressure Section
        Px, Py = DataGenandStats.PressureGen(self)
        Hx, Hy = DataGenandStats.HumidityGen(self)
        Tx, Ty = DataGenandStats.TemperatureGen(self)
        Sx, Sy = DataGenandStats.SoilMoistureGen(self)

        

        self.PlotAllsp.set_title("Overview")
        self.PlotAllsp.plot(Px, Py, self.PressureColour)
        self.PlotAllsp.plot(Hx, Hy, self.HumidityColour)
        self.PlotAllsp.plot(Tx, Ty, self.TemperatureColour)
        self.PlotAllsp.plot(Sx, Sy, self.SoilMoistureColour)
    
    def PlotOnlypressure(self, i) -> None:
        ''' PLOTS ONLY PRESSURE'''
        # Clear all figures
        self.PlotAllsp.cla()

        ### Pressure Section
        Px, Py = DataGenandStats.PressureGen(self)

        self.PlotAllsp.set_title("Pressure")
        self.PlotAllsp.plot(Px, Py, self.PressureColour)
    
    def PlotOnlyHumidity(self, i) -> None:
        ''' PLOTS ONLY HUMIDITY'''

        #clear all figures
        self.PlotAllsp.cla()
        Hx, Hy = DataGenandStats.HumidityGen(self)

        self.PlotAllsp.set_title("Humidity")
        self.PlotAllsp.plot(Hx, Hy, self.HumidityColour)
    
    def PlotonlyTemperature(self, i) -> None:
        ''' PLOTS ONLY TEMPERATURE'''

        self.PlotAllsp.cla()
        Tx, Ty = DataGenandStats.TemperatureGen(self)

        self.PlotAllsp.set_title("Temperature")
        self.PlotAllsp.plot(Tx, Ty, self.TemperatureColour)
    
    def PlotonlySoilMoisutre(self, i) -> None:
        ''' PLOTS ONLY SOIL MOISUTRE'''

        self.PlotAllsp.cla()
        Sx, Sy = DataGenandStats.SoilMoistureGen(self)

        self.PlotAllsp.set_title("Soil Moisture")
        self.PlotAllsp.plot(Sx, Sy, self.SoilMoistureColour)
    
    def InitAnimations(self) -> None:
        self.DashboardPPlot = FuncAnimation(self.PlotAll, self.PlotOnlypressure, interval = 1000)
        self.DashboardHPlot = FuncAnimation(self.PlotAll, self.PlotOnlyHumidity, interval = 1000)
        self.DashboardTPlot = FuncAnimation(self.PlotAll, self.PlotonlyTemperature, interval = 1000)
        self.DashboardSMPlot = FuncAnimation(self.PlotAll, self.PlotonlySoilMoisutre, interval = 1000)
        self.DashboardAllPlot = FuncAnimation(self.PlotAll, self.PlotAllFunc, interval = 1000)

    def animateplots(self) -> None:
        self.DashboardAllPlot.resume()
        self.DashboardPPlot.pause()
        self.DashboardHPlot.pause()
        self.DashboardTPlot.pause()
        self.DashboardSMPlot.pause()

    def animatePplots(self) -> None:
        self.DashboardAllPlot.pause()
        self.DashboardPPlot.resume()
        self.DashboardHPlot.pause()
        self.DashboardTPlot.pause()
        self.DashboardSMPlot.pause()
    
    def animateHplots(self) -> None:
        self.DashboardHPlot.resume()
        self.DashboardAllPlot.pause()
        self.DashboardPPlot.pause()
        self.DashboardTPlot.pause()
        self.DashboardSMPlot.pause()
    
    def animateTplots(self) -> None:
        self.DashboardHPlot.pause()
        self.DashboardAllPlot.pause()
        self.DashboardPPlot.pause()
        self.DashboardTPlot.resume()
        self.DashboardSMPlot.pause()

    def animateSMplots(self) -> None:
        self.DashboardHPlot.pause()
        self.DashboardAllPlot.pause()
        self.DashboardPPlot.pause()
        self.DashboardTPlot.pause()
        self.DashboardSMPlot.resume()
        

def main():
    root = tk.Tk()
    root.title("EnviroSense Module Hub")
    root.geometry('1440x720')
    mpl.use('TkAgg')
    Tabs = ttk.Notebook(root)
    Dashboard = ttk.Frame(Tabs)
    Tabs.add(Dashboard, text = "DashBoard")
    Tabs.pack(expand=1, fill="both")

    Data = DataGenandStats()
    # Buttons
    DisplayAllBtn = tk.Button(Dashboard, text = "Show All", command = Data.animateplots)
    DisplayAllBtn.place(x=50, y=50)
    DisplayPressureBtn = tk.Button(Dashboard, text = "Show Pressure", command = Data.animatePplots)
    DisplayPressureBtn.place(x=50, y=100)
    DisplayHumidityBtn = tk.Button(Dashboard, text = "Show Humidity", command = Data.animateHplots)
    DisplayHumidityBtn.place(x=50, y = 150)
    DisplayTemperatureBtn = tk.Button(Dashboard, text = "Show Temperature", command = Data.animateTplots)
    DisplayTemperatureBtn.place(x = 50, y = 200)
    DisplaySMBtn = tk.Button(Dashboard, text = "Show Soil Moisutre", command = Data.animateSMplots)
    DisplaySMBtn.place(x = 50, y = 250)

    
    # Figures
    DashboardDisplay = FigureCanvasTkAgg(Data.PlotAll, master = Dashboard)
    DashboardDisplay.get_tk_widget().place(x = 200, y = 20)
    
    Data.InitAnimations()
    

    

    root.mainloop()


if __name__ == "__main__":
    main()


