import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import collections
import psutil
import time

StartTime = time.time()

x = collections.deque(np.zeros(10))
y = collections.deque(np.zeros(10))


def DataGenPressure(i):
    PressurePlot.cla()
    x.popleft()
    x.append(time.time() - StartTime)

    y.popleft()
    y.append(psutil.cpu_percent())

    PressurePlot.plot(x, y)

Figure = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
PressurePlot = plt.subplot(111)
PressurePlot.set_facecolor('#DEDEDE')

animatePressure = FuncAnimation(Figure, DataGenPressure, interval = 1000)

plt.show()
