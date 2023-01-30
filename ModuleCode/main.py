# 10680088
# EnviroSense Module

# Import Modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

'''
X = 2.5 * np.random.randn(100) + 1.5
res = 0.5 * np.random.randn(100)      
y = 2 + 0.3 * X + res

df = pd.DataFrame(
    {
        'X' : X,
        'y' : y
    }
)

df.head()

xmean = np.mean(X)
ymean = np.mean(y)

df['xycov'] = (df['X'] - xmean) * (df['y'] - ymean)
df['xvar']  = (df['X'] - xmean)**2

beta = df['xycov'].sum() / df['xvar'].sum()
alpha = ymean - (beta * xmean)

ypred = alpha + beta * X

plt.figure(figsize=(12, 6))
plt.plot(X, ypred)
plt.plot(X, y, 'ro')
plt.title('Actual Vs Predicted')
plt.xlabel('X')
plt.ylabel('Y')

plt.show()
'''


