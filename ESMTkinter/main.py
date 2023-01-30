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


import psutil # Remove when real data is used

mpl.use('TkAgg')

root = tk.Tk()
root.title("EnviroSense Module")
tabSys = ttk.Notebook(root)

# Init Tabs
tab1 = ttk.Frame(tabSys)
tab2 = ttk.Frame(tabSys)
tab3 = ttk.Frame(tabSys)
tab4 = ttk.Frame(tabSys)

# Add Tabs
tabSys.add(tab1, text = 'Pressure')
tabSys.add(tab2, text = 'Humidity')
tabSys.add(tab3, text = 'Temperature')
tabSys.add(tab4, text = 'Soil Moisture')
tabSys.pack(expand = 1, fill = "both")

Figure = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
PressurePlot = plt.subplot(111)
PressurePlot.set_facecolor('#DEDEDE')


#Allow for MatplotLib Graphing
Tab1Display = FigureCanvasTkAgg(Figure, master=tab1)
Tab1Display.get_tk_widget().pack()

x = collections.deque(np.zeros(10))
y = collections.deque(np.zeros(10))

StartTime = time.time()

def DataGenPressure(i):
    PressurePlot.cla()
    x.popleft()
    x.append(time.time() - StartTime)

    y.popleft()
    y.append(psutil.cpu_percent())

    PressurePlot.plot(x, y)

animatePressure = FuncAnimation(Figure, DataGenPressure, interval = 1000)


'''
import collections
import psutil

'''

root.mainloop()